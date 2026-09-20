---
title: "Symmetric Transfer and Sender Composition"
document: P2583R5
date: 2026-05-01
intent: info
audience: LEWG
reply-to:
  - "Mungo Gill <mungo.gill@me.com>"
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

C++20 provides symmetric transfer ([P0913R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0913r1.html)<sup>[1]</sup>) - a mechanism where `await_suspend` returns a `coroutine_handle<>` and the compiler resumes the designated coroutine as a tail call. Coroutine chains execute in constant stack space. `std::execution` ([P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup>) composes asynchronous operations through sender algorithms. These algorithms create receivers that are structs, not coroutines. No `coroutine_handle<>` exists at any intermediate point in a sender pipeline. When a coroutine co_awaits a sender that completes synchronously, the stack grows by one frame per completion. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup>'s `std::execution::task` inherits this property. A protocol-level fix exists: Completion functions and `start()` return `coroutine_handle<>` instead of `void`, enabling struct receivers to propagate handles from downstream without becoming coroutines. The fix preserves zero-allocation composition but requires changing the return type of every completion function, every `start()`, and every sender algorithm in [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup>. This paper documents the gap, describes the fix, enumerates the changes required, and provides draft proposed wording for the protocol-level changes.

---

## Revision History

### R4: May 2026 (pre-Brno mailing)

* Removed `split` and `ensure_started` from affected algorithm lists (both removed from C++26).
* Formatting corrections.

### R3: April 2026 (post-Croydon mailing)

* Added Section 15: Draft Proposed Wording for the protocol-level fix, motivated by NB comment US 246-373 (#948, LWG4348).
* Updated Disclosure (Section 1) to note AI assistance in wording generation and two open questions requiring LWG expertise.

### R2: March 2026 (Croydon)

* Added Section 10: The Public Record - symmetric transfer is undocumented in P2300R0 through P2300R10 and first described as a limitation by the P3552 author.
* Strengthened trampoline vs. symmetric transfer analysis (Section 7.1).

### R1: March 2026 (Croydon)

* Corrected Section 5's characterization: Struct receivers cannot produce a `coroutine_handle<>`, but they can propagate one from downstream. The gap is a protocol choice, not a structural impossibility.
* Added handle propagation fix (Section 11).
* Added scope of changes analysis (Section 12).
* Added ABI considerations (Section 13).
* Corrected date of R0 revision (March -> February).

### R0: February 2026 (pre-Croydon mailing)

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy) and [Corosio](https://github.com/cppalliance/corosio) and believes coroutine-native I/O is a practical foundation for networking in C++.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

This paper examines the published record. That effort requires re-examining consequential papers, including papers written by people the author respects.

This paper uses AI. The proposed wording in Section 15 was generated with AI assistance and has not been verified against the full specification by the authors.

The authors developed [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[4]</sup> ("A Minimal Coroutine Execution Model") and [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[5]</sup> ("Open Issues in `std::execution::task`"). A coroutine-only design cannot express compile-time work graphs, does not support heterogeneous dispatch, and assumes a cooperative runtime. Those are real costs. We do not claim coroutines are the answer to all problems. The limitation documented here exists independently of any alternative design.

[P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[5]</sup> documents three costs at the boundary where the sender model meets coroutines: error reporting, error returns, and frame allocator propagation. Each is an interface mismatch. This paper documents a cost inside the composition mechanism. Sender algorithms are structs. The completion protocol is void-returning. These are not boundary properties. They are what sender algorithms are.

The wording is offered as a starting point for the [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> and [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup> authors, not as a finished product. This wording changes sections introduced by both papers. We do not claim this wording is correct. We claim the direction is worth exploring. The concept-level and CPO-level changes follow directly from the mechanism in Section 11 and are the most straightforward. The coroutine bridge changes (`sender-awaitable`, `awaitable-receiver`) are drafted from the working draft text. Algorithm-specific and task-specific changes are described in prose rather than specification text, because each algorithm has its own internal state machine that the authors have not traced through the working draft. The wording has not been tested against an implementation. Two open questions requiring LWG expertise are identified in Section 15.1.

This paper asks for nothing.

---

## 2. Symmetric Transfer in C++20

Prior to [P0913R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0913r1.html)<sup>[1]</sup>, coroutines could only return control to their caller or resumer. Gor Nishanov described the problem:

> "Recursive generators, zero-overhead futures and other facilities require efficient coroutine to coroutine control transfer. Involving a queue and a scheduler makes coroutine to coroutine control transfer inefficient. Coroutines need direct and efficient way of expressing the desired behavior."

The solution was a third form of `await_suspend`. C++20 provides three:

```cpp
void await_suspend(coroutine_handle<>);               // unconditional suspend
bool await_suspend(coroutine_handle<>);               // conditional suspend
coroutine_handle<> await_suspend(coroutine_handle<>);  // symmetric transfer
```

The third form returns a `coroutine_handle<>`. The compiler resumes the designated coroutine as if by a tail call. The note in [[expr.await]](https://eel.is/c++draft/expr.await)<sup>[16]</sup> states:

> "Any number of coroutines can be successively resumed in this fashion, eventually returning control flow to the current coroutine caller or resumer."

The stack does not grow. One coroutine suspends and another resumes in constant stack space. This is the mechanism C++20 provides to prevent stack overflow in coroutine chains.

Lewis Baker, author of [cppcoro](https://github.com/lewissbaker/cppcoro)<sup>[9]</sup> and co-author of [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup>, implemented symmetric transfer in cppcoro and documented the motivation in the source:

> "We can eliminate the use of the std::atomic once we have access to coroutine_handle-returning await_suspend() on both MSVC and Clang as this will provide ability to suspend the awaiting coroutine and resume another coroutine with a **guaranteed tail-call to resume()**."

The canonical implementation is cppcoro's `final_awaitable`:

```cpp
struct final_awaitable
{
    bool await_ready() const noexcept { return false; }

    template<typename PROMISE>
    std::coroutine_handle<> await_suspend(
        std::coroutine_handle<PROMISE> coro) noexcept
    {
        return coro.promise().m_continuation;
    }

    void await_resume() noexcept {}
};
```

When the coroutine reaches `final_suspend`, `await_suspend` returns the continuation's handle. The compiler performs a tail call to the continuation. No stack frame is added.

## 3. Production Libraries

Every major C++ coroutine library the authors surveyed uses symmetric transfer in its task type. The following table shows the `await_suspend` return type in each library's `final_suspend` awaiter:

| Library                                                               | `await_suspend` Return |
|-----------------------------------------------------------------------|------------------------|
| [cppcoro](https://github.com/lewissbaker/cppcoro)<sup>[9]</sup>                     | `coroutine_handle<>`   |
| [folly::coro](https://github.com/facebook/folly/tree/main/folly/coro)<sup>[10]</sup> | `coroutine_handle<>`   |
| [Boost.Cobalt](https://github.com/boostorg/cobalt)<sup>[11]</sup>                    | `coroutine_handle<>`   |
| [libcoro](https://github.com/jbaldwin/libcoro)<sup>[12]</sup>                        | `coroutine_handle<>`   |
| [Capy](https://github.com/cppalliance/capy)                           | `coroutine_handle<>`   |
| [asyncpp](https://github.com/petiaccja/asyncpp)<sup>[13]</sup>                       | `void`                 |

Five of six libraries converge on the same mechanism: `await_suspend` returns a `coroutine_handle<>`. This is independent replication. The libraries were developed by different authors, for different platforms, with different design goals. They converged on symmetric transfer because it is the only guaranteed zero-overhead mechanism C++20 provides for preventing stack overflow in coroutine chains.

## 4. `std::execution`'s Coroutine Bridges

[P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> achieves zero-allocation composition of asynchronous operations, compile-time work graph construction, and heterogeneous dispatch across execution contexts. It provides two bridges between coroutines and the sender model. Neither uses symmetric transfer.

### 4.1 Coroutine Completing as Sender

When an awaitable is used where a sender is expected, [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> bridges it via `connect-awaitable`. The completion uses `suspend-complete`:

```cpp
template<class Fun, class... Ts>
auto suspend-complete(Fun fun, Ts&&... as) noexcept {
    auto fn = [&, fun]() noexcept { fun(std::forward<Ts>(as)...); };

    struct awaiter {
        decltype(fn) fn;

        static constexpr bool await_ready() noexcept { return false; }
        void await_suspend(coroutine_handle<>) noexcept { fn(); }
        [[noreturn]] void await_resume() noexcept { unreachable(); }
    };
    return awaiter{fn};
}
```

`await_suspend` returns `void`. The coroutine is unconditionally suspended. The completion function `fn()` - which calls `set_value`, `set_error`, or `set_stopped` on the receiver - runs as a nested function call on the current stack. This is not symmetric transfer.

### 4.2 Sender Co-Awaited by Coroutine

When a coroutine co_awaits a sender, [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> bridges it via `sender-awaitable`:

```cpp
template<class Sndr, class Promise>
class sender-awaitable {
    // ...
    connect_result_t<Sndr, awaitable-receiver> state;

public:
    static constexpr bool await_ready() noexcept { return false; }
    void await_suspend(coroutine_handle<Promise>) noexcept { start(state); }
    value-type await_resume();
};
```

`await_suspend` returns `void`. The sender is started. When the sender completes, the `awaitable-receiver` resumes the coroutine:

```cpp
// awaitable-receiver::set_value (exception handling elided)
rcvr.result-ptr->template emplace<1>(vs...);
rcvr.continuation.resume();
```

The `.resume()` call is a function call within whatever context invokes `set_value`. If the sender completes synchronously inside `start`, the call chain is:

```
await_suspend -> start(state) -> ... -> set_value -> continuation.resume()
```

The stack grows with each synchronous completion. Symmetric transfer would return the continuation handle from `await_suspend`, allowing the compiler to arrange a tail call. The sender model calls `.resume()` as a function call inside `set_value`.

**Both bridges use `void await_suspend`. Neither can perform symmetric transfer.**

## 5. Why Sender Algorithms Do Not Provide a Handle

Symmetric transfer requires `await_suspend` to return a `coroutine_handle<>`. The question is where that handle would come from. The answer has two parts.

### 5.1 The Composition Layer

Sender algorithms (`then`, `let_value`, `when_all`) compose operations by wrapping one receiver in another. The wrapping receiver is a struct. It has `set_value`, `set_error`, and `set_stopped` member functions that invoke the wrapped callable and forward to the next receiver. It is not a coroutine. It has no `coroutine_handle<>`.

A sender pipeline with three algorithms produces a chain: coroutine -> struct -> struct -> struct -> coroutine. The structs are sender algorithm receivers. Under the current protocol, no `coroutine_handle<>` exists at any intermediate point. These struct receivers have void-returning completion functions. No return channel exists. A `coroutine_handle<>` at the end of the chain cannot propagate back through the intermediate structs to `await_suspend`.

Making each sender algorithm a coroutine would produce a handle at every intermediate point. It would also produce a heap-allocated frame at every intermediate point. A struct receiver cannot *produce* a `coroutine_handle<>` - it is not a coroutine and has no frame. However, it could *propagate* one received from further down the chain, if the protocol provided a return channel. Under the current protocol, no such channel exists. Section 11 describes a protocol-level fix that provides one.

### 5.2 The Protocol

Even when a receiver IS backed by a coroutine - as `awaitable-receiver` is, holding a `coroutine_handle<Promise> continuation` member - the completion protocol does not help. `set_value` is void-returning:

```cpp
// awaitable-receiver::set_value (exception handling elided)
rcvr.result-ptr->template emplace<1>(vs...);
rcvr.continuation.resume();
```

The handle exists inside the receiver. The protocol calls `.resume()` on it as a function call. It does not return the handle to the caller. The caller of `set_value` - which is the sender algorithm's receiver, which is a struct - cannot receive a `coroutine_handle<>` back from a void-returning function.

Four facts:

1. Sender algorithms create receivers that are structs, not coroutines. These structs have no `coroutine_handle<>`.
2. Even coroutine-backed receivers complete through void-returning `set_value`.
3. The handle exists inside the receiver but the protocol provides no way to return it.
4. `await_suspend` cannot return what neither the composition layer nor the protocol provides.

Could the protocol be changed? A struct receiver cannot produce a `coroutine_handle<>`, but it does not need to. If `set_value` returned `coroutine_handle<>`, each struct receiver could forward the handle it receives from the next receiver downstream. The handle originates from the coroutine-backed receiver at the end of the chain and propagates back through every intermediate struct to `await_suspend`. Under the current protocol, no such return channel exists. `set_value` returns `void`.

## 6. `std::execution::task` and `affine_on`

[P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup>'s `task` wraps every `co_await`ed sender in `affine_on` for scheduler affinity. The `await_transform` is defined in [[task.promise] p9](https://eel.is/c++draft/exec#task.promise-9)<sup>[16]</sup>:

```cpp
as_awaitable(affine_on(std::forward<Sender>(sndr), SCHED(*this)), *this)
```

Even when one `task` co_awaits another `task`, the inner task is wrapped in `affine_on`, producing a different sender type. Dietmar K&uuml;hl, a co-author of P3552R3, documented this in [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html)<sup>[6]</sup> ("Coroutine Task Issues"), Section 3.2.3:

> "The specification doesn't mention any use of symmetric transfer. Further, the `task` gets adapted by `affine_on` in `await_transform` ([[task.promise] p10](https://eel.is/c++draft/exec#task.promise-10)<sup>[16]</sup>) which produces a different sender than `task` which needs special treatment to use symmetric transfer."

Jonathan M&uuml;ller demonstrated the consequence in [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html)<sup>[7]</sup> ("Concerns about the design of std::execution::task"), Section 3.1:

```cpp
ex::task<void> f(int i);

ex::task<void> g(int total) {
    for (auto i = 0; i < total; ++i) {
        co_await f(i);
    }
}
```

> "Depending on the value of `total` and the scheduler used to execute `g` on, this can lead to a stack overflow. Concretely, if the `ex::inline_scheduler` is used, each call to `f` will execute eagerly, but, because `ex::task` does not support symmetric transfer, each schedule back-and-forth will add additional stack frames."

M&uuml;ller added:

> "Having iterative code that is actually recursive is a potential security vulnerability."

## 7. The Proposed Fix and Its Limits

K&uuml;hl suggested a fix direction in [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html)<sup>[6]</sup>, Section 3.2.3:

> "To address the different scheduling problems (schedule on `start`, schedule on completion, and symmetric transfer) it may be reasonable to mandate that `task` customises `affine_on` and that the result of this customisation also customises `as_awaitable`."

This would allow a `task` co_awaiting another `task` to bypass the sender machinery and use a direct awaiter with symmetric transfer. The fix addresses one case: task-to-task.

It does not address the general case. M&uuml;ller stated this directly in [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html)<sup>[7]</sup>, Section 3.1:

> "A potential fix is adding symmetric transfer to `ex::task` with an `operator co_await` overload. However, while this would solve the example above, it would not solve the general problem of stack overflow when awaiting other senders. A thorough fix is non-trivial and requires support for guaranteed tail calls."

Three cases remain after the proposed fix:

1. A `task` co_awaiting a sender that is not a `task` - no symmetric transfer. The sender completes through the receiver, which calls `.resume()` as a function call.

2. A `task` co_awaiting a `task` whose body co_awaits a synchronously completing sender (e.g. `co_await just()`) - the inner task's `co_await` goes through the `sender-awaitable` bridge, which uses `void await_suspend`. Stack frames accumulate inside the inner task.

3. Any sender chain where coroutines are composed through sender algorithms (`then`, `let_value`, `when_all`) - each sender algorithm is not a coroutine. It is a struct with `set_value` member functions. No coroutine handle exists as a transfer target.

K&uuml;hl acknowledged the general case requires a different mitigation:

> "There is a general issue that stack size needs to be bounded when operations complete synchronously. The general idea is to use a trampoline scheduler which bounds stack size and reschedules when the stack size or the recursion depth becomes too big."

A trampoline scheduler is a runtime mitigation. It detects excessive stack depth and reschedules. This is the runtime overhead in the completion path that [P0913R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0913r1.html)<sup>[1]</sup> was specifically adopted to eliminate.

M&uuml;ller identifies a language-level alternative: guaranteed tail calls. If C++ adopted such a feature, `set_value` could transfer control without growing the stack, potentially closing the gap without changing the receiver abstraction. No such feature exists in C++.

### 7.1 The Cost

A coroutine that co_awaits N synchronously-completing senders in a loop accumulates O(N) stack frames. With symmetric transfer, the same loop executes in O(1) stack space. The difference is the composition mechanism.

The stack growth is not specific to `inline_scheduler`. Any sender that completes synchronously grows the stack: `just()`, `then()` on a ready value, a cached result, an in-memory lookup.

Two mitigations exist. Both have costs:

| Mitigation     | Mechanism                                                           | Cost                                                                    |
|----------------|---------------------------------------------------------------------|-------------------------------------------------------------------------|
| Real scheduler | Every `co_await` round-trips through the scheduler queue            | Latency per iteration, even when the work completes immediately         |
| Trampoline     | Detect stack depth at runtime, reschedule when threshold is reached | Runtime check on every completion, plus occasional rescheduling latency |

Neither mitigation is zero-cost. Symmetric transfer is zero-cost.

The distinction is structural. Symmetric transfer is a compile-time guarantee: The compiler arranges a tail call from `await_suspend` to the designated coroutine. The trampoline is a runtime heuristic: It monitors stack depth and reschedules when a threshold is exceeded. The trampoline requires choosing that threshold. Too low and the scheduler reschedules unnecessarily, adding latency to every deep completion chain. Too high and the stack overflows on platforms with small stacks - embedded systems, WebAssembly, threads with reduced stack size. No single threshold is correct across deployment targets.

[P0913R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0913r1.html)<sup>[1]</sup> was adopted into C++20 specifically to eliminate this class of runtime mitigation. Nishanov wrote: *"Involving a queue and a scheduler makes coroutine to coroutine control transfer inefficient."* The trampoline scheduler reintroduces the queue-and-scheduler overhead that symmetric transfer was designed to remove.

Symmetric transfer does not prevent all stack overflow. Infinite recursion exhausts any finite stack regardless. What symmetric transfer prevents is the specific case where a finite coroutine chain overflows due to accumulated frames from non-tail calls. Sender composition creates exactly this case.

---

## 8. Failure To Launch

Section 7 showed that the proposed task-to-task fix does not reach the general case of co_awaiting arbitrary senders. This section shows that the gap extends further: No launch mechanism in [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup> avoids the sender composition layer.

### 8.1 Two Entry Points

[P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup> provides two ways to start a `task` from non-coroutine code:

- [`sync_wait(task)`](https://eel.is/c++draft/exec.sync.wait)<sup>[16]</sup> - blocks the calling thread until the task completes.
- [`spawn(task, token)`](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3149r11.html)<sup>[8]</sup> ("async_scope") - launches the task into a `counting_scope`.

The paper's only complete example uses `sync_wait`:

```cpp
int main() {
    return std::get<0>(*ex::sync_wait([]->ex::task<int> {
        std::cout << "Hello, world!\n";
        co_return co_await ex::just(0);
    }()));
}
```

### 8.2 `spawn` Does Not Compile

`task` is scheduler-affine by default. The scheduler is obtained from the receiver's environment when `start` is called. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup>, Section 4.5:

> "An example where no scheduler is available is when starting a task on a `counting_scope`. The scope doesn't know about any schedulers and, thus, the receiver used by `counting_scope` when `connect`ing to a sender doesn't support the `get_scheduler` query, i.e., this example doesn't work:"

```cpp
ex::spawn([]->ex::task<void> { co_await ex::just(); }(), token);
```

The paper acknowledges this is not a corner case:

> "Using `spawn()` with coroutines doing the actual work is expected to be quite common."

The working pattern wraps the task in `on`:

```cpp
ex::spawn(ex::on(sch, my_task()), scope.get_token());
```

### 8.3 `on` Is a Sender Algorithm

[`on(sch, sndr)`](https://eel.is/c++draft/exec.on)<sup>[16]</sup> is a sender algorithm. Its receiver is a struct with void-returning `set_value`. This is the composition layer that Section 5 showed does not support symmetric transfer under the current protocol. The task's completion traverses the `on` algorithm's receiver before reaching the scope's receiver. No `coroutine_handle<>` exists at any point in this path.

`sync_wait` connects to its own receiver - a struct with void-returning `set_value`. The `run_loop` scheduler inside `sync_wait` resumes the coroutine through `.resume()` as a function call.

Both entry points route through sender algorithms. Both use void-returning completions. Neither can perform symmetric transfer.

### 8.4 Implementation Experience

A coroutine-native launcher avoids the sender pipeline entirely. [Capy](https://github.com/cppalliance/capy)<sup>[14]</sup> starts a task directly on an executor:

```cpp
corosio::io_context ioc;
run_async(ioc.get_executor())(do_session());
ioc.run();
```

The launcher creates a trampoline coroutine that owns the task. The task chain uses symmetric transfer throughout. No sender algorithm participates. The gap documented in Sections 5 through 7 does not arise because the composition layer is the awaitable protocol, not the sender protocol.

This is not an argument for one design over another. It is evidence that the symmetric transfer gap is specific to the sender launch path, not inherent to launching coroutines.

**Every path into `std::execution::task` enters the sender composition layer. No path out preserves symmetric transfer.**

---

## 9. The Symmetric Transfer Gap

The prior papers document the symptom. K&uuml;hl's [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html)<sup>[6]</sup> states that the specification does not mention symmetric transfer and suggests a partial fix through domain customization of `affine_on`. M&uuml;ller's [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html)<sup>[7]</sup> confirms the partial fix does not reach the general case and identifies guaranteed tail calls as a language-level direction. Neither paper claims the gap is architectural. Both frame it as a missing feature - absent, difficult to add, but not structurally precluded.

This paper makes a stronger claim. The analysis in Section 5 identifies two structural causes. Sender algorithms create receivers that are structs, not coroutines - no `coroutine_handle<>` exists at the composition layer. Even coroutine-backed receivers complete through void-returning `set_value` - the protocol does not return the handle. The gap is not a missing feature. It is a consequence of the design choices that define the sender model.

The distinction matters. If symmetric transfer is merely missing, it can be added independently. If it is a consequence of protocol choices, it can only be closed by changing one of those choices - as Section 11 demonstrates by changing the return type while preserving struct receivers - or by a language feature that does not exist. The characterization matters for what comes next.

Symmetric transfer requires `await_suspend` to return a `coroutine_handle<>`. Sender algorithms create receivers that are structs. These structs are not coroutines and have no handle. Even when the final receiver is coroutine-backed, `set_value` is void-returning and does not propagate the handle to the caller.

| Sender composition                                              | Symmetric transfer                                        |
|-----------------------------------------------------------------|-----------------------------------------------------------|
| Sender algorithms compose through non-coroutine structs         | `await_suspend` must return a `coroutine_handle<>`        |
| Completion is a void-returning call to `set_value`              | Completion is a tail jump to the continuation             |
| Zero-allocation pipelines, compile-time work graphs             | Constant-stack coroutine chains                           |

**Symmetric transfer requires a handle. The sender model provides a function call. Under the current protocol, no bridge exists between the two.**

Section 11 describes a protocol-level fix. Completion functions and `start()` return `coroutine_handle<>` instead of `void`. Struct receivers propagate handles from downstream without becoming coroutines. Zero-allocation composition is preserved. The fix closes the gap - but the scope of changes enumerated in Section 12 is pervasive, and Section 13 shows that the change becomes ABI-breaking once `std::execution` ships. If the fix is not adopted, the characterization above applies: The gap is permanent.

Three directions could be explored if the fix is not adopted: domain customization that short-circuits the receiver abstraction for known coroutine types, a language feature for guaranteed tail calls, or coroutine task types that use the awaitable protocol directly for coroutine-to-coroutine composition and reserve the sender model for the boundaries where it is needed.

This is a tradeoff, not a defect. [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> was designed for GPU dispatch and heterogeneous computing - domains where symmetric transfer provides no benefit. The cost appears only when the same model is applied to coroutine composition, where symmetric transfer is the primary stack-overflow prevention mechanism that C++20 provides.

**The fix is pervasive. Without it, the gap is permanent.**

---

## 10. The Public Record

Three facts from the public record bear on how this gap came to exist.

1. [P2300R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2300r0.html)<sup>[17]</sup> (2021) through [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> (2024): The phrase "symmetric transfer" does not appear. The void return type of completion functions is specified but never discussed as a tradeoff against `coroutine_handle<>` propagation. No design rationale section explains why `set_value`, `set_error`, `set_stopped`, and `start()` return `void` instead of `coroutine_handle<>`. No revision history entry across ten revisions mentions symmetric transfer as a considered and rejected alternative.

2. [P3552R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r0.pdf)<sup>[18]</sup> through [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup> (K&uuml;hl, 2025): The task paper is the first to document the limitation. K&uuml;hl writes: *"With senders it is also not possible to use symmetric transfer to combat the problem: to achieve the full generality and composing senders, there are still multiple function calls used, e.g., when producing the completion signal."* The characterization is "not possible" - a limitation discovered downstream, not a tradeoff documented upstream.

3. [P3796R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r0.html)<sup>[19]</sup> through [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html)<sup>[6]</sup> (K&uuml;hl, 2025): K&uuml;hl proposes the trampoline scheduler as a mitigation and notes that symmetric transfer *"can be possible to avoid both the expensive scheduling operation and the stack overflow, at least in some cases."* Again framed as a limitation with a workaround, not a design choice with a rationale.

The first documentation of the symmetric transfer gap came from within the `std::execution` ecosystem - from the author of the coroutine task type, not from the authors of the sender protocol. The gap is undocumented in the public record of [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup>. The evidence is consistent with a gap that was not identified during the design of the sender protocol, not a tradeoff that was weighed and accepted.

---

## 11. Handle Propagation

The fix changes the return type of completion functions and `start()` from `void` to `coroutine_handle<>`. A null handle means no transfer is needed. The `coroutine_handle<>` type already provides null semantics: A default-constructed handle is null, and `operator bool` tests for non-null.

### 11.1 The Mechanism

Three changes to the protocol:

1. `set_value`, `set_error`, and `set_stopped` return `coroutine_handle<>` instead of `void`.
2. `start()` returns `coroutine_handle<>` instead of `void`.
3. The `sender-awaitable` bridge uses the symmetric transfer form of `await_suspend`.

The coroutine-backed receiver at the end of a sender pipeline returns its continuation handle instead of calling `.resume()`:

```cpp
// current awaitable-receiver
void set_value(Args&&... args) noexcept {
    result_ptr_->template emplace<1>(std::forward<Args>(args)...);
    continuation_.resume();
}

// proposed awaitable-receiver
coroutine_handle<> set_value(Args&&... args) noexcept {
    result_ptr_->template emplace<1>(std::forward<Args>(args)...);
    return continuation_;
}
```

The `sender-awaitable` bridge uses the third form of `await_suspend` from [P0913R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0913r1.html)<sup>[1]</sup> ("Add symmetric coroutine control transfer"):

```cpp
// current sender-awaitable
void await_suspend(coroutine_handle<Promise>) noexcept {
    start(state_);
}

// proposed sender-awaitable
coroutine_handle<> await_suspend(coroutine_handle<Promise>) noexcept {
    auto h = start(state_);
    return h ? h : noop_coroutine();
}
```

If `start()` completes synchronously and the downstream receiver returns a handle, the handle propagates through `start()` to `await_suspend`, which returns it for symmetric transfer. If the operation is pending, `start()` returns a null handle, and `await_suspend` returns `noop_coroutine()` to suspend the coroutine.

### 11.2 `then`: Propagation

A `then` receiver calls its callable, then forwards the result to the next receiver. The handle originates downstream and propagates upward:

```cpp
// current then_receiver (adapted from P2300R10's _send_receiver)
void set_value(Args&&... args) noexcept {
    auto result = invoke(f_, std::forward<Args>(args)...);
    execution::set_value(next_, std::move(result));
}

// proposed then_receiver (adapted; exception handling elided)
coroutine_handle<> set_value(Args&&... args) noexcept {
    auto result = invoke(f_, std::forward<Args>(args)...);
    return execution::set_value(next_, std::move(result));
}
```

Exception handling is elided for clarity. If `invoke(f_, args...)` throws, the implementation catches the exception and routes it through `set_error(next_, current_exception())`, which also returns `coroutine_handle<>`. The protocol is self-consistent across error boundaries: The handle from `set_error` propagates identically to one from `set_value`.

The `then` receiver does not produce a handle. It returns whatever the next receiver returned. The handle originates from the coroutine-backed receiver at the end of the chain and propagates through every intermediate struct receiver to `start()`, to `await_suspend`, and into the compiler's symmetric transfer machinery.

### 11.3 `when_all`: Partial Completion

A `when_all` receiver stores its values and decrements a counter. Only the last completing sub-sender propagates the handle:

```cpp
coroutine_handle<> set_value(Args&&... args) noexcept {
    store(std::forward<Args>(args)...);
    if (--count_ == 0)
        return execution::set_value(final_, get_values());
    return {};
}
```

Receivers that are not the last to complete return a null handle. The caller receives null, propagates it through `start()`, and `when_all`'s own `start()` proceeds to the next sub-sender. Only the final completion produces a non-null handle.

The `set_stopped` path requires care. When a sub-sender completes with an error or cancellation, `when_all` calls `request_stop()` on the remaining sub-senders. Stop callbacks registered by those sub-senders may fire synchronously inside `request_stop()`. P2300's stop callbacks are `void`-returning. If a sibling sub-sender completes inside a stop callback and its counter decrement is the last one, the returned handle has no propagation path through the `void`-returning callback.

The ordering constraint resolves this: The counter decrement must occur after `request_stop()` returns.

```cpp
coroutine_handle<> set_stopped() noexcept {
    stopped_.store(true, std::memory_order_relaxed);
    stop_source_.request_stop();
    if (--count_ == 0)
        return execution::set_stopped(final_);
    return {};
}
```

Sibling completions that fire synchronously inside `request_stop()` decrement the counter but cannot be the last decrement, because the caller's own decrement has not yet occurred. The last decrement always occurs in a normal completion context where the returned handle can propagate.

### 11.4 `let_value`: Dynamic Chains

A `let_value` receiver calls its factory function, connects the resulting sender, and starts the new operation:

```cpp
// exception handling elided
coroutine_handle<> set_value(Args&&... args) noexcept {
    auto sndr = invoke(f_, std::forward<Args>(args)...);
    auto& op = emplace_op(connect(std::move(sndr), next_));
    return start(op);
}
```

Exception handling is elided. If `invoke(f_, args...)` or `connect` throws, the implementation catches the exception and routes it through `set_error(next_, current_exception())`. As with `then`, both completion channels return `coroutine_handle<>` and the handle propagates identically regardless of which channel produced it.

The inner sender's `start()` may complete synchronously and return a handle. The `let_value` receiver propagates it. The pattern is the same: Return what is received from downstream.

### 11.5 Synchronous and Asynchronous Paths

Two paths through the protocol:

**Synchronous.** The sender completes inside `start()`. The handle propagates from the receiver through `start()` to `await_suspend`, which performs symmetric transfer. The stack does not grow.

**Asynchronous.** The sender does not complete inside `start()`. `start()` returns a null handle. `await_suspend` returns `noop_coroutine()`. The coroutine suspends. When the asynchronous operation later completes, the completion context calls `set_value` on the receiver, receives the continuation handle, and calls `.resume()`. The coroutine resumes on whatever thread the completion occurred.

The synchronous path uses symmetric transfer. The asynchronous path uses `.resume()`. Both are correct. The stack growth documented in Sections 5 through 8 occurs only on the synchronous path, and handle propagation eliminates it.

Every coroutine bridge point where `await_suspend` receives a handle from `start()` or a completion function must convert a null handle to `noop_coroutine()`. The `sender-awaitable` bridge in Section 11.1 demonstrates the pattern. The `connect-awaitable` / `suspend-complete` bridge requires the same conversion. This is a general invariant of the proposed protocol: Null means "no transfer needed," and `noop_coroutine()` is the mechanism by which the compiler suspends the coroutine without transferring to another.

### 11.6 Zero Allocation Preserved

Sender algorithm receivers remain structs. No coroutine frames are allocated at intermediate points. The return value is a `coroutine_handle<>` - a pointer-sized value passed on the stack. The compile-time type-level composition is unchanged. The zero-allocation property is preserved.

### 11.7 Conditional Return Types

The proposed protocol changes every completion function to return `coroutine_handle<>` unconditionally. An alternative approach is possible: Make the return type a compile-time property of the receiver. Receivers that participate in coroutine composition would return `coroutine_handle<>`; receivers that do not (terminal receivers, GPU-targeted receivers) would return `void`. Sender algorithms, which are already templates parameterized on the receiver type, could branch on a trait to select the return type at compile time.

This approach would eliminate the null-handle check at async completion sites for non-coroutine paths. The cost of the unconditional approach on those paths is one branch per completion - a `test`/`jz` pair on x86-64 - which is small but not zero.

The conditional approach doubles the implementation surface: Every sender algorithm must implement two code paths for every completion function, one returning `coroutine_handle<>` and one returning `void`. It also introduces a trait that must propagate correctly through every wrapper receiver in the chain. A wrapper that fails to propagate the trait silently disables symmetric transfer for the entire pipeline, with no compile-time diagnostic. We note these costs without implementation experience in [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup>. The P2300R10 architects are in a better position to determine whether this approach is viable within the existing algorithm implementations.

---

## 12. Scope of Changes to `std::execution`

The fix requires changing the return type of every completion function and every `start()` in the sender model. The following enumeration covers [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> and [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup> ("Add a Coroutine Task Type").

### 12.1 Concepts

The `receiver` and `operation_state` concepts do not constrain the return types of completion functions or `start()`. The return type is unconstrained - all existing receivers in the standard library return `void` by convention, not by requirement. The proposed change adds a return type requirement:

| Concept           | Expression                 | Current       | Proposed             |
|-------------------|----------------------------|---------------|----------------------|
| `receiver`        | `set_value(rcvr, args...)` | unconstrained | `coroutine_handle<>` |
| `receiver`        | `set_error(rcvr, err)`     | unconstrained | `coroutine_handle<>` |
| `receiver`        | `set_stopped(rcvr)`        | unconstrained | `coroutine_handle<>` |
| `operation_state` | `start(op)`                | unconstrained | `coroutine_handle<>` |

Every type that models `receiver` or `operation_state` - in the standard library and in user code - must change.

### 12.2 Sender Factory Algorithms

Sender factories complete inside `start()`. The return type of `start()` changes from `void` to `coroutine_handle<>`. The factory propagates whatever the receiver's completion function returns.

Example - `just`:

```cpp
// current
void start() noexcept {
    execution::set_value(rcvr_, values_...);
}

// proposed
coroutine_handle<> start() noexcept {
    return execution::set_value(rcvr_, values_...);
}
```

Affected factories: `just`, `just_error`, `just_stopped`, `read_env`.

### 12.3 Sender Adaptor Algorithms

Sender adaptors create internal receivers that forward completions to the next receiver. Every internal receiver's `set_value`, `set_error`, and `set_stopped` must change return type. Every operation state's `start()` must change return type.

Affected adaptors: `then`, `upon_error`, `upon_stopped`, `let_value`, `let_error`, `let_stopped`, `bulk`, `into_variant`, `stopped_as_optional`, `stopped_as_error`.

### 12.4 Scheduler Algorithms

Scheduler algorithms create internal receivers that manage transitions between execution contexts. Every internal receiver's completion functions and every operation state's `start()` must change return type.

Affected algorithms: `starts_on`, `continues_on`, `on`, `schedule_from`, `affine_on` ([P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup>).

### 12.5 Multi-Sender Algorithms

Multi-sender algorithms create per-sub-sender receivers with counter-based fan-in logic. Every per-sub-sender receiver's completion functions and every operation state's `start()` must change return type.

Affected algorithms:

- `when_all`
- `when_all_with_variant`

### 12.6 Consumer Algorithms

Consumer algorithms provide terminal receivers. These receivers store results and signal completion (e.g. through a condition variable or `run_loop`). Their completion functions return a null handle - there is no coroutine to transfer to at the terminal point.

Affected consumers:

- `sync_wait`
- `sync_wait_with_variant`

### 12.7 Coroutine Integration

The coroutine bridges in [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> and [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup> are the primary beneficiaries of the fix. The following must change:

- `sender-awaitable`: `await_suspend` changes from `void` return to `coroutine_handle<>` return (Section 11.1).
- `connect-awaitable` / `suspend-complete`: `await_suspend` changes from `void` return to `coroutine_handle<>` return.
- `task` promise type: Internal awaiters and completion machinery must propagate handles.
- `awaitable-receiver`: `set_value`, `set_error`, and `set_stopped` return the continuation handle instead of calling `.resume()` (Section 11.1).

### 12.8 New Correctness Requirement

The current protocol has one completion path: The receiver calls `.resume()` or signals a synchronization primitive. The proposed protocol has two:

1. **Synchronous completion.** The receiver returns a handle through `set_value`. The caller propagates it through `start()`. `await_suspend` performs symmetric transfer.

2. **Asynchronous completion.** An I/O completion handler, thread pool callback, or scheduler invokes `set_value` on the receiver outside of `start()`. The caller receives the handle and must call `.resume()`.

Every asynchronous completion context must check the returned handle and call `.resume()` if it is non-null. Failure to do so silently leaves the coroutine suspended. The program does not crash. It hangs. The requirement does not exist in the current protocol.

The synchronous path is self-correcting: Handles propagate through return values and the compiler's symmetric transfer machinery consumes them. The asynchronous path requires explicit action from the caller of `set_value`. Standard library algorithms (sender factories, adaptors, consumers) are written once and reviewed. Custom senders that wrap OS I/O operations, timers, or other async primitives are the risk population. An author who tests with synchronous completions will see correct behavior; the bug manifests only when the sender completes asynchronously.

The return types of `set_value`, `set_error`, `set_stopped`, and `start()` should be marked `[[nodiscard]]`. A discarded `coroutine_handle<>` return is always a bug under this protocol. The `[[nodiscard]]` attribute catches the most common form of misuse - calling a completion function as a statement without using the return value - at compile time.

### 12.9 Third-Party Impact

The concept changes in Section 12.1 affect every type that models `receiver` or `operation_state`, including types outside the standard library. The following must be updated:

- [stdexec](https://github.com/NVIDIA/stdexec)<sup>[15]</sup> (NVIDIA's reference implementation)
- Every stdexec-based project
- Every user-written sender algorithm
- Every user-written receiver
- Every user-written operation state
- Every custom scheduler's `schedule` sender

Code that models the current `receiver` or `operation_state` concepts with `void`-returning functions will fail to compile against the updated concepts.

---

## 13. ABI Considerations

Changing the return type of a function changes its calling convention and, for template specializations, its mangled symbol name. Code compiled against `void`-returning `set_value`, `set_error`, `set_stopped`, and `start()` cannot link with code compiled against `coroutine_handle<>`-returning versions. Template instantiations of sender algorithms in different translation units must agree on the return types of receiver completion functions.

`std::execution` is in the C++26 working draft. Once a standard ships function signatures, subsequent changes to those return types are ABI-breaking. The sender algorithms are templates, but `std::execution::task` and `sync_wait` produce concrete instantiations in the standard library whose signatures become part of the implementation's binary interface.

---

## 14. Conclusion

[P0913R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0913r1.html)<sup>[1]</sup> was adopted into C++20 to solve a specific problem: stack overflow in coroutine chains. The solution is `coroutine_handle<>`-returning `await_suspend`. Every major coroutine library adopted it.

Under the current protocol, the sender model's architectural choice - composing operations through non-coroutine sender algorithms with void-returning completions - prevents this mechanism from operating. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup>'s `std::execution::task` inherits this limitation. The proposed task-to-task fix does not reach the general case. No launch mechanism avoids the sender composition layer. The trampoline scheduler mitigation reintroduces the runtime cost that symmetric transfer was designed to eliminate.

A protocol-level fix exists. Section 11 describes a mechanism where completion functions and `start()` return `coroutine_handle<>` instead of `void`. Struct receivers propagate handles from downstream without becoming coroutines. Zero-allocation composition is preserved. The fix requires changing the return type of four concept-level expressions, the internal receivers and operation states of twenty-five sender algorithms, the coroutine integration bridges, and every third-party type that models `receiver` or `operation_state`. Once `std::execution` ships with void-returning completions, the change becomes ABI-breaking.

Three directions could be explored if the fix is not adopted: domain customization that short-circuits the receiver abstraction for known coroutine types, a language feature for guaranteed tail calls, or coroutine task types that use the awaitable protocol directly for coroutine-to-coroutine composition and reserve the sender model for the boundaries where it is needed.

This cost exists when evaluating coroutine integration with `std::execution`. Section 15 provides draft proposed wording to make the scope of the protocol-level fix concrete.

---

## 15. Draft Proposed Wording

### 15.1 Preamble

NB comment US 246-373 ([#948](https://github.com/cplusplus/nbballot/issues/948), LWG4348)<sup>[20]</sup> asks the committee to specify symmetric transfer when a `task` co_awaits another `task`. SG1 and LEWG reviewed the comment in Kona (November 2025) and requested a paper. This section provides draft wording for the broad fix described in Section 11 - the protocol-level change where completion functions and `start()` return `coroutine_handle<>` instead of `void`. The narrow fix (task-to-task only) does not reach the general case (Section 7).

This wording is a draft. It was generated with AI assistance and has not been verified against the full specification by the authors. It has not been reviewed by LWG. It is offered as a starting point for the [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[2]</sup> and [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[3]</sup> authors.

The draft wording covers the protocol-level changes: the completion function CPOs, the `operation_state` concept's `start()`, and the coroutine bridges (`sender-awaitable`, `awaitable-receiver`). Algorithm-specific changes (Section 12.2 through 12.6) and task-specific changes follow the same pattern - return what downstream returned - but are left to the respective authors for specification text. The following P3552R3 sections require changes: [task.state] p4, [task.promise] p6, p7-8, p9, p12-13, and [exec.affine.on].

Two open questions require LWG expertise:

1. **Return type constraint pattern.** The CPOs are defined as "expression-equivalent to `MANDATE-NOTHROW(rcvr.set_value(vs...))`." `MANDATE-NOTHROW` constrains `noexcept` but not the return type. The authors are uncertain whether the return type requirement belongs in a `Mandates` clause on each CPO, in the semantic requirements of `receiver`, or in a new concept requirement. The draft below uses a `Mandates` clause on each CPO because it is the pattern the authors are most familiar with. LWG may prefer a different specification pattern - for example, adding the requirement to the semantic requirements of `receiver`, introducing a new exposition-only concept, or modifying `MANDATE-NOTHROW` to accept a return type parameter. The intent is the same regardless of pattern: The expression must have type `std::coroutine_handle<>`.

2. **`unhandled_stopped` interaction.** The current `awaitable-receiver::set_stopped` calls `unhandled_stopped()`, casts the result to `coroutine_handle<>`, and calls `.resume()`. The proposed change returns that handle instead. The authors have not traced the `unhandled_stopped` contract to verify that returning the handle for symmetric transfer by the caller preserves the intended semantics. Review from someone familiar with the `unhandled_stopped` contract is invited.

Mandating `[[nodiscard]]` on the return values of completion functions and `start()` may be worth considering but has not been included in the draft wording below. SD-9 states that library wording should not use `[[nodiscard]]`, leaving it as a quality-of-implementation decision for vendors.

### 15.2 [exec.async.ops] Completion Functions

In [exec.async.ops] paragraph 6, after "A valid invocation of a completion function is called a *completion operation*," add:

:::wording-add

A completion function returns `std::coroutine_handle<>`. A null handle indicates that no symmetric transfer is needed. A non-null handle designates a coroutine to be resumed.

*[Note: A null handle is used rather than `noop_coroutine()` to avoid an unconditional `.resume()` call on the asynchronous completion path. The `sender-awaitable` bridge converts a null handle to `noop_coroutine()` at the `await_suspend` boundary, where the language requires it. -- end note]*

:::

### 15.3 [exec.set.value], [exec.set.error], [exec.set.stopped]

Modify [exec.set.value] paragraph 1 as follows:

:::wording

`set_value` is a value completion function. Its associated completion tag is `set_value_t`. The expression `set_value(rcvr, vs...)` for a subexpression `rcvr` and pack of subexpressions `vs` is ill-formed if `rcvr` is an lvalue or an rvalue of const type. Otherwise, it is expression-equivalent to `MANDATE-NOTHROW(rcvr.set_value(vs...))`.

<ins>*Mandates:* The expression has type `std::coroutine_handle<>`.</ins>

:::

Modify [exec.set.error] paragraph 1 as follows:

:::wording

`set_error` is an error completion function. Its associated completion tag is `set_error_t`. The expression `set_error(rcvr, err)` for some subexpressions `rcvr` and `err` is ill-formed if `rcvr` is an lvalue or an rvalue of const type. Otherwise, it is expression-equivalent to `MANDATE-NOTHROW(rcvr.set_error(err))`.

<ins>*Mandates:* The expression has type `std::coroutine_handle<>`.</ins>

:::

Modify [exec.set.stopped] paragraph 1 as follows:

:::wording

`set_stopped` is a stopped completion function. Its associated completion tag is `set_stopped_t`. The expression `set_stopped(rcvr)` for a subexpression `rcvr` is ill-formed if `rcvr` is an lvalue or an rvalue of const type. Otherwise, it is expression-equivalent to `MANDATE-NOTHROW(rcvr.set_stopped())`.

<ins>*Mandates:* The expression has type `std::coroutine_handle<>`.</ins>

:::

### 15.4 [exec.opstate.start]

Modify [exec.opstate.start] paragraph 1 as follows:

:::wording

For a subexpression `op`, the expression `start(op)` is ill-formed if `op` is an rvalue. Otherwise, it is expression-equivalent to `MANDATE-NOTHROW(op.start())`.

<ins>*Mandates:* The expression has type `std::coroutine_handle<>`.</ins>

:::

### 15.5 Coroutine Bridges

#### sender-awaitable ([exec.as.awaitable] p2)

Modify the class definition as follows:

:::wording

<pre><code>static constexpr bool await_ready() noexcept {
    return false;
}
<del>void</del><ins>coroutine_handle&lt;&gt;</ins> await_suspend(
    coroutine_handle&lt;Promise&gt;) noexcept
{
    <del>start(state);</del>
    <ins>auto h = start(state);</ins>
    <ins>return h ? h : noop_coroutine();</ins>
}</code></pre>

:::

#### awaitable-receiver ([exec.as.awaitable] p4)

Modify paragraph 4.1 `set_value` effects as follows:

:::wording

<pre><code>try {
    rcvr.result-ptr-&gt;template emplace&lt;1&gt;(vs...);
} catch(...) {
    rcvr.result-ptr-&gt;template emplace&lt;2&gt;(
        current_exception());
}
<del>rcvr.continuation.resume();</del>
<ins>return rcvr.continuation;</ins></code></pre>

:::

Modify paragraph 4.2 `set_error` effects as follows:

:::wording

<pre><code><del>rcvr.continuation.resume();</del>
<ins>return rcvr.continuation;</ins></code></pre>

:::

Modify paragraph 4.3 `set_stopped` effects as follows:

:::wording

<pre><code><del>static_cast&lt;coroutine_handle&lt;&gt;&gt;(
    rcvr.continuation.promise()
        .unhandled_stopped()).resume();</del>
<ins>return static_cast&lt;coroutine_handle&lt;&gt;&gt;(
    rcvr.continuation.promise()
        .unhandled_stopped());</ins></code></pre>

:::

*[Note: Open Question 2 applies here. The authors have not verified that returning the handle from `unhandled_stopped()` instead of calling `.resume()` preserves the intended semantics. The `unhandled_stopped` contract may assume immediate resumption. -- end note]*

### 15.6 Semantic Requirements

Add to [exec.async.ops] after the new paragraph from Section 15.2:

:::wording-add

When a completion function is invoked outside the dynamic extent of a call to `start()` on the associated operation state (i.e., the operation completed asynchronously), the caller of the completion function shall call `.resume()` on the returned `coroutine_handle<>` if it is non-null. Failure to do so leaves the associated coroutine permanently suspended.

:::

### 15.7 Sections Requiring Algorithm-Specific Wording

The following sections require changes that follow the pattern described in Section 11: Completion functions return whatever the downstream receiver returned; `start()` returns whatever the completion function returned. The changes are mechanical but each algorithm has its own internal state machine. Specification text for these sections is left to the respective authors.

**P2300R10 sender factories** ([exec.just]): `just`, `just_error`, `just_stopped`, `read_env`.

**P2300R10 sender adaptors**: `then`, `upon_error`, `upon_stopped`, `let_value`, `let_error`, `let_stopped`, `bulk`, `into_variant`, `stopped_as_optional`, `stopped_as_error`.

**P2300R10 scheduler algorithms**: `starts_on`, `continues_on`, `on`, `schedule_from`.

**P2300R10 multi-sender algorithms**: `when_all`, `when_all_with_variant`.

**P2300R10 consumers**: `sync_wait`, `sync_wait_with_variant`.

**P3552R3 task sections**: [task.state] p4 (`start()`), [task.promise] p6 (`final_suspend` completion propagation), [task.promise] p7-8 (`yield_value` completion propagation), [task.promise] p9 (`await_transform` / `affine_on`), [task.promise] p12-13 (`unhandled_stopped`).

**P3552R3 scheduler affinity**: [exec.affine.on] (also under NB comments #939/#940).

---

# Acknowledgements

The authors would like to thank Gor Nishanov for the design of symmetric
transfer, Lewis Baker for demonstrating it in cppcoro, and Dietmar K&uuml;hl
and Jonathan M&uuml;ller for documenting the limitation in
[P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html) and [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html).

---

## References

### WG21 Papers

[1] [P0913R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0913r1.html) - "Add symmetric coroutine control transfer" (Gor Nishanov, 2018).

[2] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[3] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[4] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[5] [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf) - "Open Issues in `std::execution::task`" (Vinnie Falco, Mungo Gill, 2026).

[6] [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).

[7] [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html) - "Concerns about the design of std::execution::task" (Jonathan M&uuml;ller, 2025).

[8] [P3149R11](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3149r11.html) - "async_scope" (Ian Petersen, Jessica Wong, Kirk Shoop, et al., 2025).

### Libraries

[9] [cppcoro](https://github.com/lewissbaker/cppcoro) - A library of C++ coroutine abstractions (Lewis Baker).

[10] [folly::coro](https://github.com/facebook/folly/tree/main/folly/coro) - Facebook's coroutine library.

[11] [Boost.Cobalt](https://github.com/boostorg/cobalt) - Coroutine task types for Boost (Klemens Morgenstern).

[12] [libcoro](https://github.com/jbaldwin/libcoro) - C++20 coroutine library (Josh Baldwin).

[13] [asyncpp](https://github.com/petiaccja/asyncpp) - Async coroutine library (P&eacute;ter Kardos).

[14] [Capy](https://github.com/cppalliance/capy) - Coroutines for I/O (Vinnie Falco).

[15] [stdexec](https://github.com/NVIDIA/stdexec) - NVIDIA's reference implementation of std::execution.

### Other

[16] [C++ Working Draft](https://eel.is/c++draft/) - (Richard Smith, ed.).

[17] [P2300R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2300r0.html) - "std::execution" (Micha&#322; Dominiak, Lewis Baker, Lee Howes, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2021).

[18] [P3552R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r0.pdf) - "Add a Coroutine Lazy Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[19] [P3796R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r0.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).

[20] [US 246-373 (#948)](https://github.com/cplusplus/nbballot/issues/948) - "Support symmetric transfer" (LWG4348, CD C++26).
