---
title: "The Hidden Ownership Boundary in std::execution::let_value"
document: P4253R0
date: 2026-09-07
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Default `let_value` can make a valid non-owning result dangle by destroying the predecessor operation state that owns its referent.

The adopted P3373R4 transition persists predecessor result datums, destroys the predecessor state, and then invokes the successor factory, permitting storage reuse and earlier resource release. Because a copied `std::span` survives this transition without preserving its referent, and its completion signature cannot distinguish predecessor-owned storage from storage with a surviving external owner, an asynchronous I/O successor that later accesses the bytes violates its buffer-lifetime precondition in the predecessor-owned case. The composition remains safe when the owner survives in persisted arguments, factory state, external state, or an owning result; sender-based I/O generally remains representable.

---

## Revision History

### R0: September 2026

- Initial version.

---

## Introduction

`std::execution` provides typed completion channels, static composition of operation states, and structured lifetime management for asynchronous work. P3373R4<sup>[1]</sup> refined one part of that model by allowing `let_value`, `let_error`, and `let_stopped` to reuse predecessor operation-state storage. The adopted rule has a direct consequence when a result object borrows from storage owned by that predecessor.

The case examined here has four objects with distinct lifetimes: a predecessor operation state, an owner stored within it, a non-owning result datum such as `std::span`, and a successor operation that uses the datum. The concrete witness concerns default `let_value` behavior and a successor that accesses predecessor-owned storage. External owners, owning result types, callable captures, and domain customizations are separate cases.

This analysis provides four contributions:

1. A step-by-step account of the P3373R4<sup>[1]</sup> transition as incorporated into the working draft.
2. A matched pair of predecessors with the same `set_value_t(std::span<std::byte>)` completion signature and different owner placement.
3. An application of that pair to Boost.Asio's documented asynchronous buffer-lifetime contract.
4. Safe ownership placements, implementation differences, and unranked design directions.

P3373R4<sup>[1]</sup> supplies the operation-state tradeoff. P1179R1<sup>[2]</sup> supplies established vocabulary for owners and non-owning pointer-like values. P2300R10<sup>[3]</sup> explains the intended `let_value` lifetime of persisted result objects. The current working draft, versioned I/O documentation, and pinned implementation sources supply the remaining evidence.

Three assumptions bound the result. The code-equivalent wording of N5054, the current working draft, is the normative baseline.<sup>[4]</sup> A non-owning descriptor does not extend its referent's lifetime. The asynchronous successor eventually accesses the referenced bytes. No frequency claim about deployed programs follows from the constructed case.

## 1. Earlier Predecessor Destruction Provides Reusable Storage

P3373R4 addresses two child operation states in the `let_*` adaptors: a predecessor and a successor created by a user-supplied factory. The operations do not overlap. Retaining both states until the containing operation ends consumes their combined storage even though only one is active at a time.<sup>[1]</sup>

The adopted design persists the predecessor's result datums, ends the predecessor operation-state lifetime, and then constructs the successor. This permits the two child states to share storage. P3373R4 also records a resource-lifetime benefit: An object held in the predecessor state can release a lock or another resource when that suboperation completes instead of when the containing operation is destroyed.<sup>[1]</sup>

The tradeoff is explicit in P3373R4.<sup>[1]</sup> Longer predecessor lifetimes make accesses into predecessor state remain valid, while earlier destruction makes more of those accesses undefined. The selected rule applies the earlier lifetime to `let_value`, `let_error`, and `let_stopped`, where storage reuse provides a concrete reduction. N5047 records application of P3373R4 to the working paper as LWG Poll 10.<sup>[5]</sup>

P3373R4 therefore provides reusable operation-state storage and earlier resource release by ending the predecessor lifetime before the successor is formed.<sup>[1]</sup>

## 2. `let_value` Destroys the Predecessor Before Calling the Factory

The adopted wording creates a specific destruction boundary inside `let_value`. The boundary is narrower than the general completion rules and requires three lifetime concepts to remain separate.

The **async lifetime** of an operation begins when `start` begins and ends when its completion operation begins. The associated **operation state** becomes invalid after completion executes. Its C++ object lifetime can continue beyond that point or end during completion. These are separate rules in `[exec.async.ops]`; completion does not generally destroy every operation-state object.<sup>[4]</sup>

`let_value` adds an explicit object-lifetime operation. Its state contains a variant named `ops`. That variant initially contains the predecessor operation state. On a matching value completion, `[exec.let]` performs six steps:

1. Store decayed copies of the predecessor's result datums in `args`.
2. Replace the active `ops` alternative with `monostate`.
3. Invoke the user-supplied factory with references to the stored copies.
4. Connect the returned sender to the downstream receiver.
5. Store the successor operation state in `ops`.
6. Start the successor.

The following excerpt is from the C++ draft source at commit `999d8ae0`, lines 4268-4277, with the exposition-only markup stripped and nothing else altered.<sup>[6]</sup> These ten lines are byte-identical in N5046, in N5054, and at that commit. Other parts of `[exec.let]` did change over the same interval, the exposition-only `let-env` having acquired a second parameter, so the claim here concerns the quoted block and not the subclause as a whole.

```cpp
auto& tuple = args.template emplace<args_t>(std::forward<Ts>(ts)...);
ops.template emplace<monostate>();
auto&& sndr = apply(std::move(fn), tuple);
using op_t = connect_result_t<sender_type, receiver_type>;
auto mkop2 = [&] {
  return connect(std::forward<sender_type>(sndr),
  receiver_type{rcvr, env});
};
auto& op = ops.template emplace<op_t>(emplace-from{mkop2});
start(op);
```

`variant::emplace` destroys the active alternative before constructing its replacement.<sup>[4]</sup> The first `ops.emplace` therefore destroys the predecessor operation state after the result copies exist but before the factory is invoked.

For default `let_value`, the adaptor wording defines the C++ object-lifetime boundary independently of the completion signal.

## 3. Persisting a Descriptor Does Not Preserve Its Referent

The result datum persisted by `let_value` can be an owner or a non-owning descriptor. That distinction determines whether persisting the datum also preserves the objects reached through it.

The standard defines `std::span` in `[span.overview]` as "a view over a contiguous sequence of objects, the storage of which is owned by some other object."<sup>[4]</sup> A span is trivially copyable. Copying it preserves a pointer and an extent; the copy does not copy the objects in the viewed sequence.

P1179R1 uses the terms **Owner** and **Pointer** for this distinction. Its examples classify `string` and `vector` as Owners, while raw pointers, `string_view`, `span`, and `vector::iterator` are non-owning Pointers.<sup>[2]</sup> The terminology is broader than built-in pointer syntax because each listed type can remain alive after the object it denotes has been destroyed.

### Terms Used in the Example

- **Owner:** an object, such as `vector`, that owns the referenced byte storage.
- **Descriptor:** a non-owning object, such as `span`, containing access information.
- **Referent:** the byte sequence reached through the descriptor.
- **Predecessor:** the operation whose result triggers `let_value`.
- **Persisted result:** the decayed result object stored in `let_value::args`.
- **Successor factory:** the callable that returns the next sender.

Completion signatures provide a different category of information. `[exec.cmplsig]` permits `set_value_t(Vs...)`, `set_error_t(Err)`, and `set_stopped_t()`. A completion signature describes a completion operation through its tag and argument types.<sup>[4]</sup>

Consider `set_value_t(std::span<std::byte>)`. The type states that successful completion sends a span. It does not identify whether the span refers to external storage, static storage, state owned by `let_value`, or state owned by its predecessor. A different completion datum can carry ownership: `vector`, `shared_ptr`, or an explicit owner token can make that property part of the result.

`let_value` persists the completion datum it receives. When that datum is a span, persisting the span does not preserve storage owned by a different object.

## 4. Identical Completion Signatures Can Have Opposite Validity

Two predecessors isolate the ownership property. Each sends `std::span<std::byte>` through the value channel. The first stores the owner in its `then` callable; the second refers to an owner outside the sender.

The dangling half of the pair is P3373R4's own example. Its Examples section pipes `just()` into a `then` callable that captures a `std::vector`, returns `std::cref(vec.front())`, and continues on a scheduler; the paper then walks the synchronous analogue and reports the AddressSanitizer diagnostic that analogue produces.<sup>[1]</sup> Two substitutions follow here. The result datum becomes `std::span<std::byte>` so that it is a buffer descriptor rather than a reference wrapper, which is what an I/O operation receives. The control is then added: a second predecessor with the same completion signature and the owner placed outside the sender. The matched pair is what this section contributes, not the dangling case, which P3373R4 established.

The following constructed sender stores the vector in the predecessor operation state after connection.

```cpp
auto ephemeral =
    std::execution::just()
    | std::execution::then(
        [owner = std::vector<std::byte>(4096)]()
            mutable noexcept {
            return std::span<std::byte>(owner);
        });
```

The `then` callable returns a valid span while its vector capture is alive. `let_value` receives that span, copies it into `args`, and replaces the predecessor operation state with `monostate`. Replacement destroys the `then` callable and its vector. The persisted span remains alive and denotes storage whose lifetime has ended.

The control changes only the owner's location. Both fragments are block-scope declarations; at namespace scope the reference capture would name a variable with non-automatic storage duration, which compilers diagnose.

```cpp
std::vector<std::byte> owner(4096);

auto durable =
    std::execution::just()
    | std::execution::then([&owner]() noexcept {
        return std::span<std::byte>(owner);
    });
```

Destroying the second predecessor destroys a callable containing a reference. It does not destroy `owner`, so the persisted span remains usable while the external vector remains alive.

Both `noexcept` callables return the same type. Their value completion signatures are therefore equal:

```cpp
using ephemeral_sigs =
    std::execution::completion_signatures_of_t<
        decltype(ephemeral), std::execution::env<>>;
using durable_sigs =
    std::execution::completion_signatures_of_t<
        decltype(durable), std::execution::env<>>;

static_assert(std::same_as<ephemeral_sigs, durable_sigs>);
```

The assertion holds by the completion-signature rules, which do not depend on any implementation: Both callables are `noexcept`, `just()` contributes `set_value_t()`, and decay-copying a `std::span` cannot throw, so both predecessors carry `completion_signatures<set_value_t(std::span<std::byte>)>`.

The assertion also compiles. Against stdexec at x86-64 gcc 16.2 with `-std=c++23 -Wall -Wextra`, the pair builds with no diagnostics and the `static_assert` passes.<sup>[7]</sup> That build substitutes `stdexec::` for `std::execution::` because stdexec is not the standard library, and it tracks the stdexec trunk branch, so it is reproducible today rather than fixed for all time. The deduction above, not the build, is what the section rests on.

Table 1. Matched predecessors with one completion signature and two owner locations.

| Property | Predecessor-owned case | External-owner control |
|---|---|---|
| Value completion | `set_value_t(span<byte>)` | `set_value_t(span<byte>)` |
| Owner location | `then` callable in predecessor state | enclosing block |
| Predecessor destruction | destroys the vector | destroys a reference capture |
| Persisted span | refers to expired storage | refers to live storage |

The matched pair differs in owner provenance, a property absent from their equal completion signatures.

## 5. The Same Boundary Violates an Asynchronous I/O Precondition

The matched pair becomes consequential when the successor is an asynchronous I/O operation. The three APIs examined below separate a pointer-size descriptor from storage that must remain alive until completion.

### 5.1. I/O Requires the Referent Through Completion

Boost.Asio 1.92.0 defines `mutable_buffer` as a copyable representation that "does not own the underlying data."<sup>[8]</sup> Its `basic_stream_socket::async_read_some` operation accepts one or more mutable buffers and returns immediately.<sup>[9]</sup> The parameter contract states:

> Although the buffers object may be copied as necessary, ownership of the underlying memory blocks is retained by the caller, which must guarantee that they remain valid until the completion handler is called.

The descriptor can therefore survive while its referent does not. The precondition applies from initiation through completion, the same interval for which the successor sender uses the buffer.

The public stdexec Asio adapter exposes `async_read_some` as a sender through `exec::asio::use_sender`.<sup>[10]</sup> The following constructed factory converts the persisted span to Asio's descriptor:

```cpp
auto read_from =
    [&socket](std::span<std::byte>& buffer) {
        return socket.async_read_some(
            boost::asio::buffer(
                buffer.data(), buffer.size()),
            exec::asio::use_sender);
    };
```

Applying that factory to the two predecessors from Section 4 produces two well-typed compositions:

```cpp
auto first =
    std::move(ephemeral)
    | std::execution::let_value(read_from);

auto second =
    std::move(durable)
    | std::execution::let_value(read_from);
```

For `first`, the adopted order copies the span and destroys the vector owner before invoking `read_from`. The factory can copy the invalid pointer into an Asio descriptor, but the read cannot satisfy its requirement that the referenced memory remain valid through completion. Access through that descriptor has undefined behavior.

For `second`, the same factory receives the same span type. The external vector remains alive, so the I/O precondition remains satisfied while the containing scope retains `owner`.

Windows `ReadFileEx` independently requires its buffer to remain valid for the read duration.<sup>[11]</sup> Linux `io_uring(7)` states the same rule for pointers used by `IORING_OP_READ` and `IORING_OP_WRITE`.<sup>[12]</sup> These APIs use completion routines and completion queues rather than Asio completion tokens, yet impose the same owner-lifetime requirement.

The hidden owner location determines whether equal sender metadata satisfies an ordinary asynchronous I/O precondition.

## 6. Safe Ownership Placements Survive the Successor

The adopted rule supports safe asynchronous I/O when the owner resides in state that remains alive through the successor. Three placements meet that condition without retaining the predecessor operation state.

The first placement sends the owner itself into `let_value`. The adaptor moves the vector into its persisted argument storage before destroying the predecessor:

```cpp
auto safe_value =
    std::execution::just(
        std::vector<std::byte>(4096))
    | std::execution::let_value(
        [&socket](auto& owner) {
            auto buffer = boost::asio::buffer(
                owner.data(), owner.size());
            return socket.async_read_some(
                buffer, exec::asio::use_sender);
        });
```

The successor depends on the vector stored in `let_value::args`. The destroyed `just` operation state owns no required storage. P2300R10 describes this use of `let_value`: the persisted sent object remains alive until the sender returned by the factory completes.<sup>[3]</sup>

The second placement stores the owner in the factory. P3373R4 deliberately leaves the callable alive because successor operations can depend on its captures.<sup>[1]</sup>

```cpp
auto safe_capture =
    std::execution::just()
    | std::execution::let_value(
        [&socket,
         owner = std::vector<std::byte>(4096)]()
            mutable {
            auto buffer = boost::asio::buffer(
                owner.data(), owner.size());
            return socket.async_read_some(
                buffer, exec::asio::use_sender);
        });
```

The third placement lies outside the containing sender, as in the durable control of Section 4. Static storage, a caller-owned vector, or shared ownership can satisfy the same lifetime requirement when its owner outlives the operation.

An owning completion datum provides another representation. A result type containing the vector, a `shared_ptr`, or an explicit owner token can make ownership part of the transmitted value. This changes the completion type, unlike the two matched span signatures.

The P3373R4 transition supports safe I/O when ownership is placed in argument storage, callable state, external state, or an owning result.<sup>[1]</sup>

## 7. Coroutine Scope Makes the Compared Ownership Relation Lexical

The comparable coroutine composition places the owner and the asynchronous operation in one block. Ordinary lexical scope expresses the lifetime relation without requiring knowledge of an adaptor's operation-state representation.

Boost.Asio 1.92.0 documents this pattern with a local array passed to `async_read_some` inside a coroutine loop.<sup>[13]</sup> The same shape with a vector is:

```cpp
boost::asio::awaitable<void>
read_once(tcp::socket& socket)
{
    std::vector<std::byte> owner(4096);
    co_await socket.async_read_some(
        boost::asio::buffer(
            owner.data(), owner.size()));
}
```

Automatic storage lasts until its block exits. `[expr.await]` specifies that suspension returns control to the caller or resumer "without exiting any scopes."<sup>[4]</sup> The vector therefore remains alive while the read is pending, provided the coroutine state itself remains alive.

Coroutines can also dangle. Returning a descriptor into a local owner leaves the caller with an expired referent:

```cpp
task<std::span<std::byte>>
bad()
{
    std::vector<std::byte> owner(4096);
    co_return std::span<std::byte>(owner);
}
```

Destroying a suspended coroutine state also destroys its local objects. The coroutine model does not infer ownership or extend a referent beyond its ordinary C++ lifetime.

The comparison is therefore about visibility. In the coroutine control, block structure shows that the owner spans the `co_await`. In the sender witness, the owner sits in an ancestor operation state and the following adaptor supplies the destruction boundary.

## 8. Implementations Differ at the Factory Boundary

Two public implementations provide evidence about the transition. They agree that result datums are persisted and the predecessor state is replaced. They differ on whether replacement occurs before or after the successor factory invocation.

The libunifex implementation cited by P3373R4<sup>[1]</sup> constructs a decayed result tuple, destroys `predOp_`, invokes the factory, connects the returned sender, and starts the successor.<sup>[14]</sup> Its source comment states that `predOp_` is destroyed first to make room for the successor operation. This order matches the adopted wording.

NVIDIA stdexec at commit `2c56ffe7` invokes the factory while the predecessor owner remains alive, then replaces the predecessor before connecting and starting the successor.<sup>[15]</sup> A test named for destruction before factory invocation checks that a captured `shared_ptr` still has use count 2 inside the factory and has use count 1 after `start`.<sup>[16]</sup> The observed test condition documents the implementation order even though its name describes the standard order.

### 8.1. The Normative Finding Does Not Depend on Either Ordering

The code-equivalent wording controls the standard result: the predecessor is destroyed before the factory. A synchronous access to predecessor-owned bytes inside the factory can therefore be undefined under the wording while appearing to work in the pinned stdexec implementation.

The asynchronous I/O witness places the access later. In libunifex, the owner is gone before the factory. In the pinned stdexec implementation, the factory first returns an Asio sender containing the descriptor, then predecessor replacement destroys the owner before successor connection and start. The referenced bytes have expired in both implementations by the time the asynchronous child can access them.

The implementation comparison therefore bounds two claims. Factory-time behavior varies in the public implementations. Successor-time access still requires ownership that survives predecessor replacement.

## 9. Expected Objections Bound the Finding

The constructed case admits direct objections. Four concern whether the program already violates an ordinary borrowing discipline. Four concern the scope of what follows from one default adaptor.

### "The Predecessor Never Promised That Its Borrow Would Survive Completion"

Correct. The predecessor sends a span that is valid during its completion operation. Neither the span type nor the sender promises that the referent survives later destruction of the predecessor operation state.

The relevant composition remains well-typed, and replacing the following `then` with `let_value` changes when the owner is destroyed. The claim concerns information available at that composition point and attributes no broken promise to the predecessor.

### "Completion Signatures Were Never a Lifetime Type System"

Correct. Completion signatures describe completion operations. Section 3 relies on that definition rather than assigning them a stronger purpose.

Generic composition can inspect `set_value_t(std::span<std::byte>)` and cannot recover the omitted owner location from that type. An owning result or an explicit token can put additional lifetime information into the completion datum.

### "`span` Already Says That It Does Not Own"

The span type identifies the risk category. It does not identify whether the referent is external, static, stored in `let_value::args`, captured by the factory, or owned by the predecessor operation state. The matched pair in Section 4 differs among those locations while preserving the descriptor type.

### "This Is Ordinary C++ Dangling-View Behavior"

The underlying object-lifetime rule is ordinary C++. The additional fact is where the owner dies. In the sender witness, the owner is nested in an operation state and its destruction is prescribed by the following adaptor rather than by a lexical block boundary.

### "Putting the Owner in `let_value` Solves the Problem"

Yes. Section 6 shows two such constructions. They are evidence that sender-based I/O can satisfy the lifetime contract, and they identify the owner placement required by the adopted rule.

### "A Domain Can Customize `let_value`"

Yes. The constructed proof concerns the default transformation and code-equivalent wording. A domain customization can select different storage and lifetime behavior, with that behavior becoming part of the domain's contract.

### "Coroutines Can Dangle Too"

Yes. Section 7 includes a coroutine returning a span into a local vector. The comparison concerns lexical visibility of the owner across one `co_await` and establishes no universal coroutine-safety result.

### "The Example Does Not Cover Every `let_*` Adaptor"

The ordinary buffer witness concerns `let_value`. `let_error` can carry one compound error datum that contains a non-owning view. `let_stopped` carries no result datum, so the same direct buffer-result construction does not apply.

These objections limit the result to a well-typed default `let_value` composition whose predecessor owns the referent. They do not alter the ownership relations shown in Sections 2 through 5.

## 10. Design Directions Trade Visibility Against Storage

The evidence determines no unique remedy. Five directions expose different parts of the ownership relation and preserve different parts of P3373R4's storage result.<sup>[1]</sup>

1. **Owner-placement conventions.** Library guidance can require owners to reside in `let_value` arguments, callable captures, or external state. This preserves the adopted wording and requires users to recognize the boundary.
2. **Owning completion data.** APIs can send an owner, shared owner, or explicit lifetime token with the descriptor. This makes lifetime information available to composition and changes the completion type or ownership cost.
3. **Diagnostics or ownership metadata.** Static analysis can track an Owner-to-Pointer relation of the kind described by P1179R1.<sup>[2]</sup> Such analysis requires information beyond an ordinary span completion signature.
4. **Domain transformation.** An I/O domain can customize `let_value` or provide an adaptor with a domain-specific lifetime contract. This keeps generic wording unchanged and makes behavior depend on the selected domain.
5. **Longer predecessor lifetime.** An adaptor can retain the predecessor through the successor. This preserves predecessor-owned borrows and gives up the storage reuse and earlier resource release that motivated P3373R4.<sup>[1]</sup>

The five directions differ in ownership visibility, static storage reuse, generic metadata, and implementation cost. The evidence identifies the tradeoff without ranking those selections.

## 11. Conclusion

Non-owning buffers are representable in sender completions, and `let_value` safely sequences I/O when the buffer owner resides in state that survives the successor. The adopted P3373R4 transition first persists the buffer descriptor, then destroys the predecessor operation state, then invokes the successor factory. When the destroyed state owns the descriptor's referent, an ordinary `set_value_t(std::span<std::byte>)` completion signature does not distinguish that dangling result from an equal signature whose referent remains alive. The resulting adaptor-specific ownership boundary is consequential for I/O while sender/receiver remains capable of representing I/O.

The record also identifies the tradeoff that produced the boundary. Earlier destruction permits predecessor and successor states to reuse storage and releases predecessor-held resources sooner. Longer lifetime preserves predecessor-owned borrows. Library authors can place owners in surviving state, domain authors can select different transformations, and lifetime-analysis tools can seek the owner relation that the ordinary descriptor type omits. Each builds on a separate part of the evidence rather than on a claim that one representation fits every asynchronous domain.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy) and [Corosio](https://github.com/cppalliance/corosio) and believes coroutine-native I/O is a practical foundation for networking in C++.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

This paper uses AI.

The author has a stake in how C++ compares coroutine-native I/O with sender-based I/O. The analysis gives coroutine block scope a visibility advantage in one matched lifetime comparison.

The constructed witness concerns default `let_value` and predecessor-owned storage. It does not measure the frequency of this pattern in deployed programs. The coroutine comparison in Section 7 addresses lexical visibility only; it does not compare compile-time inspection or optimization of a complete sender graph.

Related work includes P3373R4, P2300R10, and the author's coroutine I/O papers. The method compares code-equivalent standard wording, equal-signature ownership controls, versioned I/O contracts, and pinned implementation sources.

This paper asks for nothing.

## Acknowledgments

The author thanks Robert Leahy for P3373R4 and its precise account of operation-state storage and lifetime choices; Herb Sutter for the Owner and Pointer vocabulary in P1179R1; and Christopher Kohlhoff for Boost.Asio's explicit asynchronous buffer-lifetime contract. The public libunifex and stdexec implementations made the ordering comparison reproducible.

## References

[1] [P3373R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3373r4.pdf) - "Of Operation States and Their Lifetimes" (Robert Leahy, 2026).

[2] [P1179R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1179r1.pdf) - "Lifetime safety: Preventing common dangling" (Herb Sutter, 2019).

[3] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[4] [N5054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5054.pdf) - "Working Draft, Programming Languages - C++" (Thomas K&ouml;ppe, 2026).

[5] [N5047](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5047.html) - "Editors' Report: Programming Languages - C++" (Thomas K&ouml;ppe, Jens Maurer, Dawn Perchik, Richard Smith, 2026).

[6] [C++ draft source](https://github.com/cplusplus/draft/blob/999d8ae0d2d3d6e76d85d39819cf253caacf6af6/source/exec.tex#L4268-L4277) - "`let_value` code-equivalent wording at commit `999d8ae0`" (ISO C++ project, 2026).

[7] [Compiler Explorer](https://godbolt.org/z/qhvq41116) - "Matched-predecessor completion signatures compiled against stdexec trunk, x86-64 gcc 16.2, `-std=c++23 -Wall -Wextra`" (Compiler Explorer, 2026).

[8] [Boost.Asio `mutable_buffer`](https://www.boost.org/doc/libs/1_92_0/doc/html/boost_asio/reference/mutable_buffer.html) - "A non-owning mutable buffer descriptor" (Christopher M. Kohlhoff, 2026).

[9] [Boost.Asio `async_read_some`](https://www.boost.org/doc/libs/1_92_0/doc/html/boost_asio/reference/basic_stream_socket/async_read_some.html) - "Asynchronous socket read and buffer-lifetime requirements" (Christopher M. Kohlhoff, 2026).

[10] [stdexec `use_sender.hpp`](https://github.com/NVIDIA/stdexec/blob/2c56ffe7f8a2b8b5221918159092be379ae8b40f/include/exec/asio/use_sender.hpp) - "Asio sender completion token at commit `2c56ffe7`" (NVIDIA, 2026).

[11] [Microsoft `ReadFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfileex) - "Asynchronous file read and buffer-lifetime requirements" (Microsoft, accessed 2026-09-07).

[12] [`io_uring(7)`](https://man7.org/linux/man-pages/man7/io_uring.7.html) - "Linux asynchronous I/O interface" (Linux manual page, 2020).

[13] [Boost.Asio C++20 coroutine support](https://www.boost.org/doc/libs/1_92_0/doc/html/boost_asio/overview/composition/cpp20_coroutines.html) - "C++20 Coroutines Support" (Christopher M. Kohlhoff, 2026).

[14] [libunifex `let_value.hpp`](https://github.com/facebookexperimental/libunifex/blob/03a211667e7598311c6bdcefdb3d489d341a42f0/include/unifex/let_value.hpp#L150-L189) - "Predecessor replacement at commit `03a21166`" (Meta Platforms, 2025).

[15] [stdexec `__let.hpp`](https://github.com/NVIDIA/stdexec/blob/2c56ffe7f8a2b8b5221918159092be379ae8b40f/include/stdexec/__detail/__let.hpp#L259-L283) - "Successor construction at commit `2c56ffe7`" (NVIDIA, 2026).

[16] [stdexec `test_let_value.cpp`](https://github.com/NVIDIA/stdexec/blob/2c56ffe7f8a2b8b5221918159092be379ae8b40f/test/stdexec/algos/adaptors/test_let_value.cpp#L467-L485) - "`let_value` predecessor-lifetime test at commit `2c56ffe7`" (NVIDIA, 2026).
