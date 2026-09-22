---
title: "Two Ends of One Dangling Reference: Coroutine Parameters and let_value Predecessors"
document: P4253R0
date: 2026-09-14
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

A `std::span` that a `then` produces from its own operation state is well-defined for a `then` successor and reads destroyed storage for an asynchronous read reached through `let_value`, and the completion signature does not record where the owner sits.

Asynchronous I/O requires the memory a buffer descriptor names to stay valid until completion while the descriptor owns nothing, and an I/O sender factory that takes the descriptor as an argument, the shape Asio has through `use_sender`, is reached from a value through `let_value`. The change adopted for C++26 destroys the `let_value` predecessor operation state after its results are copied out and before the sender factory runs, while `then` keeps its predecessor alive throughout. The coroutine parameter problem is the same hazard from the other end, and that end has a standard note, a guideline, and a diagnostic where the `let_value` end has none.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## 1. Introduction

P3373R4<sup>[1]</sup> changed `std::execution::let_value`, `let_error`, and `let_stopped` so that the predecessor operation state is destroyed after decayed copies of its result datums are stored and before the user's sender factory is invoked. The change resolved C++26 Committee Draft (CD) comment CA-338<sup>[2]</sup> and was applied to the working paper at Croydon in March 2026.<sup>[3]</sup> The result datum of interest below is a non-owning view, such as a `std::span<std::byte>`, and the successor of interest is an asynchronous read constructed from that view.

The operation-state design provides three properties that the analysis below depends on. It provides stable storage at a fixed address for the whole of an operation, so child operations may hold pointers into it. It provides static composition, so a pipeline's storage is one object whose size is known at compile time and which can sit on the stack. And it provides nested lifetimes, so a child's operation state is a data member of its parent's and cannot outlive it.<sup>[4]</sup> P3389R0, the LEWG presentation of the proposal, states that "Operation state represents the stack frame (variables with 'automatic storage duration' are members thereof)",<sup>[5]</sup> and P3373R4 proposes that the predecessor's frame end when the predecessor returns, "in the same way that returning from a synchronous function destroys the stack frame thereof."<sup>[1]</sup>

Related work. P3373R4 supplies the change, the design space, and the poll record.<sup>[1]</sup> P2300R10 section 1.3.3 supplies the model's own asynchronous read example, which routes a `std::span` from a `then` into an asynchronous read.<sup>[6]</sup> The C++ Core Guidelines rule CP.53 states the coroutine parameter lifetime problem and its remedy.<sup>[7]</sup> P1179R1 supplies the Owner and Pointer vocabulary and treats `co_await` as invalidating Pointer parameters.<sup>[8]</sup> P3801R0 and P3796R1 debate the coroutine problem as it applies to `std::execution::task`.<sup>[9]</sup><sup>[10]</sup> P4288R1 describes a completion with a reference into an operation state as "the asynchronous analogue of a function which returns a reference to a local variable".<sup>[11]</sup>

Contributions:

1. A matched pair of predecessors with equal completion signatures, one of whose spans dangles under `let_value` and neither of which dangles under `then`, with the working-draft lines that produce the difference.
2. A correspondence between that hazard and the coroutine parameter lifetime problem, stated as a relation between a source that ends and a consumer that continues, with the documentation and tooling each side has.
3. The record of the change: what P3373R4 said about per-algorithm lifetimes, how the polls went, and where the public implementations stand on the order of destruction.

Assumptions. The analysis is of the working-draft wording in the C++ draft sources at commit `999d8ae0`,<sup>[12]</sup> whose [exec.let] text is unchanged from N5054.<sup>[4]</sup> Implementation behavior is reported as of the pinned commits and dates given. The I/O contracts cited are the vendors' own.

## 2. `then` Keeps the Predecessor Alive and `let_value` Destroys It

The two adaptors differ in one line. `then` is specified through `default-impls`, whose `start` is `(execution::start(ops), ...)` and which never destroys a child;<sup>[12]</sup> the child operation state is the data member `inner-ops` of `basic-operation`, so it lives as long as the parent.<sup>[12]</sup> `impls-for<then-cpo>` overrides only `complete`, which invokes the callable and forwards its result.<sup>[12]</sup> The predecessor's callable, its captures, and anything they own remain alive until the whole operation is destroyed.

`let_value` is specified through `let-state`, whose `ops` variant is constructed holding the predecessor operation state.<sup>[12]</sup> On a matching completion it runs the following, quoted from the draft source at lines 4268-4277 with exposition markup stripped:<sup>[12]</sup>

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

`variant::emplace` destroys the active alternative before constructing the new one.<sup>[4]</sup> The second line therefore destroys the predecessor operation state after the result copies exist and before the factory runs. The result datums survive as decayed copies in `args`; the storage they may point into does not. No prose sentence in [exec.let] states when the predecessor operation state ends; the line above is the whole specification.<sup>[12]</sup>

P3373R4 describes the `then` case directly. Of a `then` callable that captures a `std::vector` and returns a reference into it, P3373R4 writes: "The lack of UB stems from the fact that the lifetime of the invocable is bound to the lifetime of the operation state."<sup>[1]</sup> That binding still holds for `then`. It no longer holds for a predecessor of `let_value`.

One adaptor keeps the predecessor's storage and the other frees it, and the completion-signature machinery that describes the result is the same for both.

## 3. One Predecessor, Two Successors, Opposite Validity

The predecessor below stores a buffer in its own operation state and completes with a view of it. The vector is a capture of the `then` callable; the callable is part of the `then` operation state; the span is a `std::span`, which the standard defines as "a view over a contiguous sequence of objects, the storage of which is owned by some other object."<sup>[4]</sup> In P1179R1's terms the vector is an Owner and the span is a Pointer.<sup>[8]</sup>

```cpp
auto ephemeral =
    std::execution::just()
    | std::execution::then(
        [owner = std::vector<std::byte>(4096)]() mutable noexcept {
            return std::span<std::byte>(owner);
        });
```

Two successors consume the span. The first is synchronous. It runs during the predecessor's completion operation, and by Section 2 the `then` operation state, its callable, and the vector are alive for the whole of the enclosing operation.

```cpp
auto a = ephemeral
    | std::execution::then([](std::span<std::byte> s) noexcept {
        return s.size();
    });
```

The second is asynchronous and is constructed from the span. `async_read_some(sock, s)` stands for any function that takes the buffer as an argument and returns a sender, which is what an Asio initiating function invoked with the `use_sender` completion token is.<sup>[13]</sup><sup>[14]</sup> Under the draft, `ops.template emplace<monostate>()` runs before the factory is invoked, so the factory receives a span whose storage has been freed, and the read it constructs targets that storage.

```cpp
auto b = ephemeral
    | std::execution::let_value([&sock](std::span<std::byte> s) {
        return async_read_some(sock, s);
    });
```

A control shows that the difference is not visible in the type. `durable` returns the same span type from a vector that lives outside the sender:

```cpp
std::vector<std::byte> owner(4096);

auto durable =
    std::execution::just()
    | std::execution::then([&owner]() noexcept {
        return std::span<std::byte>(owner);
    });
```

Destroying `durable`'s predecessor destroys a callable holding a reference and leaves the vector alone. Both callables are `noexcept`, both return `std::span<std::byte>`, and `just()` contributes `set_value_t()`, so both predecessors have `completion_signatures<set_value_t(std::span<std::byte>)>`:

```cpp
static_assert(std::same_as<
    std::execution::completion_signatures_of_t<
        decltype(ephemeral), std::execution::env<>>,
    std::execution::completion_signatures_of_t<
        decltype(durable), std::execution::env<>>>);
```

The assertion holds by the completion-signature rules and compiles against stdexec trunk on x86-64 gcc 16.2 with `-std=c++23 -Wall -Wextra`, with no diagnostics.<sup>[15]</sup>

The safe and the unsafe compositions differ in the successor's algorithm and in nothing the type system sees.

## 4. Sender Factories for Asynchronous I/O Are Reached Through `let_value`

A synchronous successor that does not store the span is finished with it before returning, so `then` is sufficient for it and, by Section 2, safe. The successor that holds the span past its own return is an asynchronous one, and the five asynchronous I/O interfaces below each require that the memory a descriptor names remain valid from initiation to completion while the descriptor itself owns nothing.

Boost.Asio 1.92.0, for the buffers of `async_read_some`: "Although the buffers object may be copied as necessary, ownership of the underlying memory blocks is retained by the caller, which must guarantee that they remain valid until the completion handler is called."<sup>[13]</sup> Its `mutable_buffer` "does not own the underlying data, and so is cheap to copy or assign."<sup>[16]</sup> The Networking TS states the same rule for every asynchronous read or write: "The program shall ensure the memory remains valid until" the last copy of the buffer sequence is destroyed or the completion handler is invoked, whichever comes first.<sup>[17]</sup> Windows `ReadFileEx`: "This buffer must remain valid for the duration of the read operation."<sup>[18]</sup> Linux `io_uring(7)`: "the pointers to a buffer used as part of a IORING_OP_WRITE or IORING_OP_READ operation must remain valid until completion."<sup>[19]</sup> POSIX `aio_read`: if the buffer "becomes an illegal address prior to asynchronous I/O completion, then the behavior is undefined."<sup>[20]</sup>

A sender for such a read takes one of two shapes, and P2762R2 section 4.7 shows them side by side, writing that "the following senders have the same effect when started":<sup>[21]</sup>

```cpp
auto s0 = execution::just(buffer) | net::async_read_some(socket);
auto s1 = net::async_read_some(execution::just(buffer), socket);
auto s2 = net::async_read_some(socket, buffer);
```

The first two are the adaptor shape: the read is a sender adaptor whose child produces the buffer, and by Section 2 the child operation state is a data member of the read's and lives as long as it does. P2300R10 section 1.3.3 uses this shape, piping a `then` that returns `std::span(buf.data.get(), buf.size)` directly into `async_read(handle)`, "a pipeable sender adaptor" that "takes a sender parameter which must send an input buffer".<sup>[6]</sup> Under the adaptor shape, `ephemeral | async_read(handle)` keeps the vector alive through the read.

The third form is the factory shape: the buffer is an argument, and the sender exists only once the argument does. Asio has only this shape, because every Asio initiating function takes its buffers as arguments,<sup>[13]</sup> and `use_sender` turns that call into a sender.<sup>[14]</sup> To construct a factory-shape sender from a value produced earlier in a pipeline, the pipeline needs the algorithm that passes "the sender's result datums to a user-specified callable, which returns a new sender that is connected and started",<sup>[12]</sup> which is `let_value`. P3373R4's own `let_value` example is this shape: a `write` function receives a `std::span<const std::byte>` from its caller and, inside `let_value`, calls `writable.write(span)` for a sender.<sup>[1]</sup>

Both documented examples place the owner where the change does not reach. P2300R10's owner is `buf`, a persisted argument of an enclosing `let_value`, of which P2300R10 says "Critically, the lifetime of the sent object will last until the sender returned by the std::invocable completes"<sup>[6]</sup>; P3373R4 preserves that guarantee. P3373R4's owner is outside the sender, in the caller of `write`. Move the owner one stage earlier, into the `then` that produces the span, and under the adaptor shape nothing changes, while under the factory shape the same span, with the same type, reaches the read after its storage is gone.

Of the two shapes sender I/O takes, the adaptor keeps the predecessor alive, and the factory, the one shape an Asio initiating function can take, is reached through `let_value` and does not.

## 5. The Other End: Coroutine Parameters

Coroutines have a lifetime hazard with the same shape, viewed from the opposite end, and it is recorded in the standard, in the Core Guidelines, and in a compiler. A plain function taking a `std::string_view` may be called with a temporary; the temporary outlives the call. Make the function a coroutine and the temporary ends at the end of the full-expression while the coroutine body, holding the view, continues after its first suspension.

```cpp
void       sync_use(std::string_view s);   // temporary outlives the call
task<void> async_use(std::string_view s);  // body outlives the temporary

task<void> caller() {
    sync_use(std::string("payload"));           // well-defined
    auto t = async_use(std::string("payload")); // t views a dead string
    co_await std::move(t);                      // undefined behavior
}
```

The standard says so in a note: "If a coroutine has a parameter passed by reference, resuming the coroutine after the lifetime of the entity referred to by that parameter has ended is likely to result in undefined behavior."<sup>[4]</sup> CP.53, "Parameters to coroutines should not be passed by reference", gives the reason: "Once a coroutine reaches the first suspension point, such as a co_await, the synchronous portion returns. After that point any parameters passed by reference are dangling." Its remedy is by-value parameters, "because the copied parameter will live in the coroutine frame that is safe to access throughout the coroutine", and its enforcement is "Flag all reference parameters to a coroutine."<sup>[7]</sup> P1179R1's lifetime profile encodes the same rule: "On co_await or co_yield, for every Pointer parameter p, KILL(p)."<sup>[8]</sup> Clang 18 ships `[[clang::coro_lifetimebound]]`, under which, for a coroutine return type so annotated, "capturing reference to a temporary which would die after the expression" is a warning.<sup>[22]</sup><sup>[23]</sup> P3796R1 notes that the views can be hidden inside value types, so "preventing const& parameters isn't a solution".<sup>[10]</sup>

The correspondence with Section 3 is a relation between a source whose storage ends and a consumer that continues past that end.

| | Coroutine parameter | `let_value` predecessor |
|---|---|---|
| Boundary | call into a coroutine | value completion into `let_value` |
| Datum | parameter | result datum |
| Storage that ends | caller's temporaries, end of full-expression | predecessor operation state, `emplace<monostate>()` |
| Consumer that continues | coroutine body after suspension | successor operation |
| Safe synchronous control | plain function | `then` |
| Visible in the signature | reference parameter: yes; view-typed parameter: no | no |
| Remedy | the callee takes owners by value | the producer completes with owners |
| Note in the standard | [dcl.fct.def.coroutine] Note 3 | none |
| Guideline with enforcement | CP.53 | none |
| Compiler diagnostic | Clang `coro_lifetimebound` | none |

Table 1. The coroutine parameter problem and the `let_value` predecessor problem, row by row. In the coroutine, the consumer outlives the source; in `let_value`, the source is gone before the consumer begins. The instruments in the last three rows act on reference parameters; a view-typed parameter, as in the example above, escapes them, which is P3796R1's point.

Both ends are in `std::execution`. `task` "represents a sender that can be used as the return type of coroutines",<sup>[4]</sup> and the coroutine end applies to it: P3801R0 raises it under the heading "No protection against dangling references", and P3796R1 answers.<sup>[9]</sup><sup>[10]</sup> P3801R0 also names the cure: "The natural sender/receiver solution is structured concurrency, which ensures references live long enough."<sup>[9]</sup> The sender side has the other end.

A coroutine reading into a local buffer does not choose among owner placements. The buffer is a local of the frame, the frame survives the suspension, and the read completes into storage that is alive because the coroutine is:

```cpp
std::vector<std::byte> buf(4096);
auto [ec, n] = co_await sock.read_some(buf);
```

The frame is the default owner. Under `let_value` the corresponding safety depends on the author having put the owner in `args`, in the factory's captures, or outside the sender, and Section 3 shows the signature does not record which.

P2300R10's stated case against coroutines is allocation and indirection: coroutine frames "require an unavoidable dynamic allocation and indirect function calls", and HALO (heap allocation elision optimization) "requires a sophisiticated compiler".<sup>[6]</sup> Lifetimes are not part of that case. Table 1 holds row by row for the first seven rows, and the `let_value` column is empty for the last three.

## 6. The Record

The case for the change is stated in P3373R4 and in CA-338. Ending the predecessor's operation state "after the values received therefrom have been stored in the parent's operation state allows the storage occupied thereby to be reused for the operation state of the second operation".<sup>[1]</sup> Resources the predecessor holds through RAII (resource acquisition is initialization) are released when it completes rather than when the whole operation ends.<sup>[1]</sup> libunifex "already uses the above-described lifetime management strategy", so the change standardizes existing practice.<sup>[1]</sup> CA-338 states that the maximal lifetime was "unnecessarily increasing the lifetime of those operation states and the storage occupied by a let_value, let_error, or let_stopped operation state."<sup>[2]</sup>

The record of adoption and implementation, as of 2026-09-15:

1. Four polls, none with a vote against. LEWG at Wroc&lstrok;aw 2024, welcoming "a principled reduction of operation state lifetimes for specific S/R algorithms (described as ad-hoc in P3373)": 10-7-0-0-0. LEWG telecon 2025-05-13, approving the design for the `let_*` algorithms and `split` as proposed in P3373R1: 5-7-0-0-0. SG1 at Kona 2025-11-04, forwarding as the fix for CA-338: 3-8-0-0-0. LEWG at Croydon 2026-03-23, forwarding P3373R2 to LWG: 9-6-7-0-0.<sup>[1]</sup>
2. Plenary, Croydon 2026: "Apply the changes in P3373R4 (Of Operation States and Their Lifetimes) to the C++ working paper. CA-338. No discussion. No objection to unanimous consent. Approved." The minutes record the same three sentences for 34 of the 38 LWG motions that day.<sup>[3]</sup>
3. [exec.async.ops]/8 states generally that "The lifetime of an asynchronous operation's operation state can end during the execution of the completion operation."<sup>[12]</sup> [exec.let] does not state that `let_value`'s predecessor does, and contains no prose statement of when the predecessor operation state ends. The `emplace<monostate>()` line is the whole specification.<sup>[12]</sup>
4. P3373R4's wording is a redline. It strikes the `2` from `ops2_variant_t` in the three places it edits and elides, with `[...]`, the paragraph requiring "the types args_variant_t and ops2_variant_t" to be well-formed.<sup>[1]</sup> The editorial application, draft commit `27bd4d47`, applied the redline as written.<sup>[24]</sup> [exec.let]/14 still names `ops2_variant_t`, a type the wording no longer defines.<sup>[12]</sup>
5. P3373R4 reports: "This change has been implemented in nVidia's stdexec."<sup>[1]</sup> The merged code invokes the factory and then destroys the predecessor; the adopted wording destroys the predecessor and then invokes the factory.<sup>[12]</sup> At the pull request's head, commit `4c465db`, the destruction is an explicit `emplace<__monostate>()` after the factory call.<sup>[25]</sup> A later refactor removed that line,<sup>[33]</sup> and at commit `6bac4e1a` the predecessor is destroyed as a side effect of emplacing the successor into the same variant, whose `emplace` destroys the active alternative first.<sup>[26]</sup><sup>[34]</sup> The order did not change. libunifex, the cited existing practice, follows the wording's order: "we need to destroy predOp_ first to make room", then the factory.<sup>[27]</sup>
6. The test added with the stdexec change is titled "let_value destroys the first operation state before invoking the sender factory". Its body checks `ptr.use_count() == 2` inside the factory, where `ptr` is a `shared_ptr` captured by the first operation's `then` callable; that check holds only while the first operation state is alive.<sup>[25]</sup>
7. Beman.Execution at its 2026-09-12 head keeps the predecessor in `basic_operation::inner_ops` for the whole operation and has no `let_value` change for P3373R4;<sup>[28]</sup> libc++ lists P3373R4 as not yet implemented.<sup>[29]</sup> NVIDIA's CCCL `cuda::experimental::execution`,<sup>[35]</sup> pika,<sup>[36]</sup> and kuhllib keep the predecessor alive for the whole operation, and HPX forwards to stdexec. Among maintained public implementations, libunifex alone follows the wording's order. The `let_value` composition of Section 3 is undefined behavior under the draft, dangles once the read starts under stdexec, and runs to completion under Beman.
8. At the LEWG session of 2026-03-23, before the poll forwarding P3373R2 to LWG, Mungo Gill presented a Compiler Explorer example<sup>[37]</sup> of a sender whose operation state owns a 4096-byte buffer and completes with a `std::span` into it, consumed through `let_value` by an `async_write_sender` taking the span as an argument, annotated "Well-defined today. UB under P3373R2." The poll that followed was 9-6-7-0-0.<sup>[1]</sup> P3373R3 (2026-03-23) and P3373R4 (2026-03-27) were published after that session; R3's changes are wording corrections and R4's is the `sender_t`/`receiver_t` rename, and neither adds text on views into the predecessor's operation state.<sup>[38]</sup><sup>[1]</sup> The stdexec pull request and its review contain no discussion of the lifetime of values passed to the factory.<sup>[25]</sup>

P3373R4 weighed four designs. Of the ad hoc option, deciding lifetimes algorithm by algorithm: it "has the added disadvantage of the cognitive load it forces onto users."<sup>[1]</sup> Of the implementation-defined option, in the LEWG presentation: it "Has a Hyrum's Law problem".<sup>[5]</sup> Of the status quo: it "Causes perhaps initially-surprising accesses to have well-defined behavior", with the consequence that "people will write fragile code which works with standard algorithms, but doesn't compose with non-standard algorithms", which "could in turn become a safety issue".<sup>[1]</sup> P3373R4 confines the change to the `let_*` algorithms because other algorithms "only ever contain a single child operation state" so "there are no savings to be gained", and because ending lifetimes there "would add overhead since a std::optional (or equivalent) would need to be used".<sup>[1]</sup> The boundary between `then` and `let_value` is drawn by storage layout, not by any property of the values that cross it. The paper called this option ad hoc; LEWG's Wroc&lstrok;aw poll called it principled. The sentence about fragile code now describes `then` and `let_value`, and, as of the commits above, four implementations of `let_value`.

Items 1 through 8 are the record. The hazard of Section 3 was demonstrated to LEWG before the wording was forwarded, and no document in the record analyzes it: not the paper in its two subsequent revisions, the NB comment, the tracking issue, the plenary minutes, or the implementation's pull request. The position that such a view is the asynchronous analogue of a reference to a local variable is stated of `then`'s captures in P3373R4 and of `split` in P4288R1.<sup>[1]</sup><sup>[11]</sup> Neither states it of a view consumed by a `let_value` factory, and neither addresses the fact that the same view, with the same completion signature, is well-defined under a `then` successor.

## 7. Objections

### "Put the owner in the persisted arguments, as P2300R10 does."

That placement is safe, and Section 4 shows both documented examples use it. The completion signature does not record whether it was used; `ephemeral` and `durable` have the same one. A reader of the pipeline cannot tell the safe composition from the unsafe one without reading the predecessor's callable.

### "A view into the predecessor's own state was already the asynchronous analogue of returning a reference to a local."

It was, and P4288R1 says so of `split`.<sup>[11]</sup> P3373R4 gives four synchronous analogues of the same `then` code, two well-defined because the function object outlives its call and two undefined because the lambda's locals end at its return or the lambda itself is a temporary, and reasons from the stack-frame analogy that the undefined ones govern.<sup>[1]</sup> The coroutine end of Table 1 is equally the analogue of a known synchronous error, a reference to a temporary that has ended, and it received a note, a guideline, and a diagnostic.

### "Under [exec.async.ops]/7 the operation state was already invalid after completion, so nothing changed."

The paragraph reads: "After an asynchronous operation executes a completion operation, its associated operation state is invalid. Accessing any part of an invalid operation state is undefined behavior."<sup>[12]</sup> It is unchanged from P2300R10 and predates the change.<sup>[6]</sup> Whether it reached the asynchronous read is arguable: `ephemeral`'s span points to heap storage owned by a member of the operation state, whether that storage is a "part of" the state is a question the wording does not answer, and P3373R4 describes such accesses under the status quo as having "well-defined behavior".<sup>[1]</sup> The new wording ends the question by destroying the object. The `then` successor runs during the completion operation and is unaffected either way.

### "Coroutines have the same problem, so this is not a cost of senders."

Section 5 agrees, and the last three rows of Table 1 record what each end has.

### "libunifex has done this for years without incident."

No field report of a user's value dangling into the factory is cited here, and none was found: ten searches of the stdexec and libunifex issue trackers for `let_value` with `dangling`, `lifetime`, `use-after-free`, `destroyed`, and `ASAN` returned no such report. libunifex's own history records the bug class on both sides of the algorithm. A 2020 commit, "avoid dangling reference bug in unifex::let", fixed an access through the predecessor's receiver after `predOp_` had been destroyed.<sup>[39]</sup> A 2021 pull request changed the predecessor receiver's `set_error` to take its argument by value, with the comment "Taking by value here to force a copy on the offchange [sic] the error object lives in the operation state, in which case destroying the predecessor operation state would invalidate it."<sup>[40]</sup> A 2022 pull request fixed the same shape on the successor side, for coroutine-evaluated values.<sup>[32]</sup> stdexec #282 asks why libunifex destroys the successor state and values before completing,<sup>[30]</sup> and stdexec #1076 asks "Is it always safe to release operation states early or does it lead to issues elsewhere?"<sup>[31]</sup> The claim is about what the adopted wording permits. P3373R4's own argument about latent issues, that code tested against one set of algorithms is later composed with another "with less rigor", applies to it.<sup>[1]</sup>

### "stdexec implements the change and its test passes."

stdexec invokes the factory before destroying the predecessor; the wording and libunifex destroy before invoking; Beman.Execution has not implemented the change.<sup>[12]</sup><sup>[25]</sup><sup>[27]</sup><sup>[28]</sup> The test's assertion encodes stdexec's order under the wording's title.<sup>[25]</sup> For the asynchronous successor the outcome under stdexec is the same as under the wording: the storage is gone before the read starts.

### "The change saves storage and every poll favored it."

Both are so. The storage saving is the successor's operation state overlapping the predecessor's, and the polls are 10-7-0-0-0, 5-7-0-0-0, 3-8-0-0-0, and 9-6-7-0-0.<sup>[1]</sup>

## 8. Conclusion

A `std::span<std::byte>` produced by a `then` and consumed by an asynchronous read is well-defined when the read is an adaptor whose child is that `then`, and reads destroyed storage when the read is a sender factory reached through `let_value`, which is the only shape Asio offers. The two predecessors that make the difference have the same completion signature. The coroutine parameter problem has this shape from the other end: there the consumer outlives the source, here the source is ended before the consumer starts, and in both the remedy is an owner passed by value across the boundary.

The record shows the change adopted for storage and for the timely release of RAII resources, with no vote against at four polls and a plenary disposition shared with 34 of the 38 LWG motions that day, its lifetime specified by one line of code-equivalent wording and no prose, and the implementation it cites running the factory before the destruction the wording specifies, while libunifex follows the wording and Beman.Execution has not implemented it. The hazard was demonstrated to LEWG before the wording was forwarded, and no document in the record analyzes it. The coroutine end of the hazard has a note in the standard, a guideline with an enforcement rule, and a compiler attribute; the `let_value` end has none.

Those who build on this next are the implementers deciding which order to ship, the authors of `std::execution` I/O layers deciding between the adaptor and factory shapes and where owners go, and anyone writing the `let_value` counterpart of CP.53.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy) and [Corosio](https://github.com/cppalliance/corosio), coroutine-native I/O libraries, and believes coroutine-native I/O is a practical foundation for networking in C++.

The paper places a finding in the record.

The author has a stake in how C++ compares coroutine-native I/O with sender-based I/O, and Section 5 sets a coroutine shape against a sender shape.

The matched pair is a constructed minimal example. Nothing is measured, and no failure in deployed code is cited.

This paper is a companion to P4255R0 and P4286R0, which also examine the boundary between coroutines and `std::execution`.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

This paper asks for nothing.

## Acknowledgments

Robert Leahy, whose P3373R4 supplies the change, the design space, the synchronous analogues, and the `then` analysis on which Sections 2 and 7 rest. Herb Sutter for the Owner and Pointer vocabulary and the `co_await` rule in P1179R1. Christopher Kohlhoff for Boost.Asio's explicit buffer-lifetime contract. Dietmar K&uuml;hl for P2762R2's side-by-side statement of the adaptor and factory shapes, and, with Jonathan M&uuml;ller, for the P3801R0 and P3796R1 exchange on `task` parameters. Mungo Gill for the Compiler Explorer example presented to LEWG at Croydon, for the editorial pass that attributed the dangling example to P3373R4, and for the first compile check of the matched pair.

## References

[1] [P3373R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3373r4.pdf) - "Of Operation States and Their Lifetimes" (Robert Leahy, 2026).

[2] [N5028](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5028.pdf) - "C++26 CD summary of voting and comments" (Herb Sutter, 2025).

[3] [N5040](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5040.pdf) - "WG21 2026-03 Croydon Hybrid Meeting Minutes" (Braden Ganetsky, 2026).

[4] [N5054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5054.pdf) - "Working Draft, Programming Languages - C++" (Thomas K&ouml;ppe, 2026).

[5] [P3389R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3389r0.pdf) - "Of Operation States and Their Lifetimes (LEWG Presentation 2024-09-10)" (Robert Leahy, 2024).

[6] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[7] [C++ Core Guidelines CP.53](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rcoro-reference-parameters) - "Parameters to coroutines should not be passed by reference" (Bjarne Stroustrup, Herb Sutter, editors, accessed 2026-09-15).

[8] [P1179R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1179r1.pdf) - "Lifetime safety: Preventing common dangling" (Herb Sutter, 2019).

[9] [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html) - "Concerns about the design of std::execution::task" (Jonathan M&uuml;ller, 2025).

[10] [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).

[11] [P4288R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4288r1.pdf) - "Stop the Decay" (Robert Leahy, 2026).

[12] [C++ draft source, exec.tex](https://github.com/cplusplus/draft/blob/999d8ae0d2d3d6e76d85d39819cf253caacf6af6/source/exec.tex) - "[exec.async.ops] lines 270-287, [exec.snd.expos] lines 2143-2158 and 2211-2213, [exec.then] lines 4036-4055, [exec.let] lines 4090-4400, at commit 999d8ae0" (ISO C++ project, 2026).

[13] [Boost.Asio basic_stream_socket::async_read_some](https://www.boost.org/doc/libs/1_92_0/doc/html/boost_asio/reference/basic_stream_socket/async_read_some.html) - "Start an asynchronous read" (Christopher M. Kohlhoff, 2026).

[14] [stdexec exec/asio/use_sender.hpp](https://github.com/NVIDIA/stdexec/blob/6bac4e1a8ed065eb5cd8d3b295f00aee753d4f84/include/exec/asio/use_sender.hpp) - "Asio completion token whose async_result::initiate returns a sender, at commit 6bac4e1a" (Robert Leahy, 2025).

[15] [Compiler Explorer](https://godbolt.org/z/qhvq41116) - "Matched predecessors with equal completion signatures, stdexec trunk, x86-64 gcc 16.2, -std=c++23 -Wall -Wextra" (Compiler Explorer, 2026).

[16] [Boost.Asio mutable_buffer](https://www.boost.org/doc/libs/1_92_0/doc/html/boost_asio/reference/mutable_buffer.html) - "Holds a buffer that can be modified" (Christopher M. Kohlhoff, 2026).

[17] [N4771](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).

[18] [Microsoft ReadFileEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfileex) - "ReadFileEx function (fileapi.h)" (Microsoft, accessed 2026-09-15).

[19] [io_uring(7)](https://man7.org/linux/man-pages/man7/io_uring.7.html) - "Asynchronous I/O facility" (Linux manual pages, 2020).

[20] [aio_read(3p)](https://man7.org/linux/man-pages/man3/aio_read.3p.html) - "asynchronous read from a file" (IEEE and The Open Group, 2017).

[21] [P2762R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r2.pdf) - "Sender/Receiver Interface For Networking" (Dietmar K&uuml;hl, 2023).

[22] [Clang Attribute Reference](https://clang.llvm.org/docs/AttributeReference.html#coro-lifetimebound) - "coro_lifetimebound" (LLVM Project, accessed 2026-09-15).

[23] [Clang 18.1.0 Release Notes](https://releases.llvm.org/18.1.0/tools/clang/docs/ReleaseNotes.html) - "Attribute Changes in Clang" (LLVM Project, 2024).

[24] [C++ draft commit 27bd4d47](https://github.com/cplusplus/draft/commit/27bd4d47caa0) - "P3373R4 Of Operation States and Their Lifetimes" (ISO C++ project, 2026).

[25] [NVIDIA/stdexec PR #1715](https://github.com/NVIDIA/stdexec/pull/1715) - "let_value, _error, & _stopped: Destroy Child Operation State After Completion" (Robert Leahy, 2025).

[26] [stdexec __let.hpp](https://github.com/NVIDIA/stdexec/blob/6bac4e1a8ed065eb5cd8d3b295f00aee753d4f84/include/stdexec/__detail/__let.hpp#L266-L283) - "__start_next_fn at commit 6bac4e1a" (NVIDIA, 2026).

[27] [libunifex let_value.hpp](https://github.com/facebookexperimental/libunifex/blob/03a211667e7598311c6bdcefdb3d489d341a42f0/include/unifex/let_value.hpp#L144-L190) - "let_value predecessor destruction, lines 154-180 at commit 03a21166" (Meta Platforms, 2025).

[28] [Beman.Execution let.hpp](https://github.com/bemanproject/execution/blob/c55d8245bea73924a6509c77f68e85008572769a/include/beman/execution/detail/let.hpp#L292-L324) - "let_t state and let_bind at commit c55d8245" (Beman Project, 2026).

[29] [libc++ C++26 Status](https://libcxx.llvm.org/Status/Cxx26.html) - "C++26 implementation status" (LLVM Project, accessed 2026-09-15).

[30] [NVIDIA/stdexec issue #282](https://github.com/NVIDIA/stdexec/issues/282) - "Check the lifetimes in the let_ algorithms" (Eric Niebler, 2021).

[31] [NVIDIA/stdexec issue #1076](https://github.com/NVIDIA/stdexec/issues/1076) - "Upper bound on lifetime of operation states" (msimberg, 2023).

[32] [facebookexperimental/libunifex PR #416](https://github.com/facebookexperimental/libunifex/pull/416) - "Fix asan error for let_value with coroutines" (jesswong, 2022).

[33] [NVIDIA/stdexec PR #1778](https://github.com/NVIDIA/stdexec/pull/1778) - "refactor continues_on and let_value to be more constexpr-friendly" (Eric Niebler, 2026).

[34] [stdexec __variant.hpp](https://github.com/NVIDIA/stdexec/blob/6bac4e1a8ed065eb5cd8d3b295f00aee753d4f84/include/stdexec/__detail/__variant.hpp#L285-L296) - "__variant::emplace, which destroys the active alternative before constructing the new one, at commit 6bac4e1a" (NVIDIA, 2026).

[35] [NVIDIA/cccl let_value.cuh](https://github.com/NVIDIA/cccl/blob/a12115c30f224447508c79c824cc707b84210c63/cudax/include/cuda/experimental/__execution/let_value.cuh) - "cuda::experimental::execution let_value, child operation state as a data member for the whole operation, at commit a12115c3" (NVIDIA, 2026).

[36] [pika let_value.hpp](https://github.com/pika-org/pika/blob/947cf61a14fcafc4d472fb3fcddf3bd2e89d792e/libs/pika/execution/include/pika/execution/algorithms/let_value.hpp) - "let_value with predecessor_op_state as a data member for the whole operation, at commit 947cf61a" (pika, 2026).

[37] [Compiler Explorer](https://godbolt.org/z/Ye67bqbcb) - "async_read_sender completing with a std::span into its own operation state, consumed through let_value by async_write_sender; annotated 'Well-defined today. UB under P3373R2.'" (Mungo Gill, presented to LEWG 2026-03-23).

[38] [P3373R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3373r3.pdf) - "Of Operation States and Their Lifetimes" (Robert Leahy, 2026-03-23).

[39] [facebookexperimental/libunifex commit 9263302e](https://github.com/facebookexperimental/libunifex/commit/9263302eb19d13ad0ba8ba667827d9e842e842ff) - "avoid dangling reference bug in unifex::let" (Eric Niebler, 2020-07-13).

[40] [facebookexperimental/libunifex PR #344](https://github.com/facebookexperimental/libunifex/pull/344) - "back out fix to just[_error] and fix let_value instead" (Eric Niebler, 2021-09-06).
