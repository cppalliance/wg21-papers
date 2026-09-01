---
title: "Examining Six Observations on std::execution"
document: P4253R0
date: 2026-09-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

One practitioner's published observations about `std::execution` share a common property.

Robert Leahy has authored production code in NVIDIA's stdexec<sup>[1]</sup> (the `completion_token`<sup>[2]</sup> and `use_sender`<sup>[3]</sup> adaptors), four WG21 papers (P3373R2<sup>[4]</sup>, P3682R0<sup>[5]</sup>, P3887R1<sup>[6]</sup>, P3950R0<sup>[7]</sup>), and a detailed technical specification of AIO-to-sender bridge invariants<sup>[8]</sup>. This paper examines Leahy's published work and asks what the observations share.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## 1. Background

In broad terms a regular (i.e. synchronous) function call has access to two forms of storage throughout its lifetime (note that the "lifetime" of a regular function call is the time between the call thereto and the return therefrom): stack storage (i.e. "variables with automatic storage duration") and heap storage (i.e. "variables with dynamic storage duration").<sup>[4]</sup>

Leahy establishes in P3373R2<sup>[4]</sup> that asynchronous operations within the framework of `std::execution` analogously have access to two forms of storage throughout their lifetime (note that the "lifetime" of an asynchronous operation is the time between a call to `std::execution::start` on the operation state and the fulfillment of the "receiver contract"): contents of the operation state and heap storage.<sup>[4]</sup> The operation state is the asynchronous analog of a synchronous stack frame - local stable storage the operation can rely upon throughout its lifetime.<sup>[11]</sup> Of course, the analogy is structurally precise: a sender is a fully curried function, a receiver is a call site, connection produces the operation state (i.e. the stack frame), `start` delegates forward progress, and the completion signal is the return.

But despite the structural elegance of the above-described analogues, Leahy identifies one area in which they lack predictive power: the lifetime of the operation state. By the analogy one would expect that the lifetime of the operation state is ended by the invocation of `std::execution::set_value`, `::set_error`, or `::set_stopped`; however this is not guaranteed to be the case in general, and in fact `std::execution` appears to guarantee exactly the opposite.<sup>[4]</sup> Put differently: whereas the stack pointer for regular synchronous code moves both up and down (i.e. "allocating" and "freeing" stack storage) the analogue thereof for asynchronous code under the framework of `std::execution` moves in only one direction (i.e. such storage is only ever "allocated").<sup>[4]</sup>

Note that Leahy frames this observation not as an indictment but as an area requiring careful standardization. His P3373R2 proposes ending predecessor operation state lifetimes early for `let_value`, `let_error`, and `let_stopped` - a change which allows the storage occupied thereby to be reused for the operation state of the second operation,<sup>[4]</sup> standardizing existing practice in libunifex. Leahy's P3682R0<sup>[5]</sup> was adopted by plenary vote, removing `std::execution::split`. His P3887R1<sup>[6]</sup> was forwarded by SG1 (8-3-1-0-0) and LEWG (10-5-0-0-0). His production code in NVIDIA's stdexec<sup>[1]</sup> constitutes the most complete AIO-to-sender bridge in the published record - a bridge whose structured concurrency finalization guarantees exactly-once completion under all paths, and whose abandonment detection addresses a problem no prior integration had solved.

Which brings us to the question this paper examines: what do Leahy's published observations about `std::execution`, taken together, reveal about the scope of the sender model?

## 2. The Simplest Integration

Let us consider the simplest formulation of bridging AIO and `std::execution`. A sender wraps an AIO initiating function. The sender's `connect` produces an operation state containing the initiation and the receiver. The operation state's `start` invokes the initiation with a completion handler that forwards all synthesized values through to the receiver, completing the operation thereby.<sup>[11]</sup>

Leahy demonstrates this formulation in his CppCon 2025 talk<sup>[11]</sup>: a sender that wraps an initiating function, a completion handler that sends values down the value channel to the receiver. The code compiles. The operation state opts into the concepts machinery of `std::execution` by providing the needful nested type alias.<sup>[11]</sup> Of course, the sender curries the initiation, and `connect` propagates it into the operation state together with the receiver.

But then we look at this code further. We notice something curious. Leahy declares `start` as `noexcept`, but the initiation is accepted generically.<sup>[11]</sup> No properties thereof have been established. The implementation can throw an exception and cause `std::terminate` - a consequence which is, as Leahy characterizes it, decidedly unergonomic.<sup>[11]</sup>

And so we are confronted with a question: what does `std::execution` require of `start`?

## 3. Exceptions and the Executor Wrapper

`start` is the point where the synchronous domain transitions to the asynchronous domain. Synchronous reporting mechanisms - such as, for example, throwing an exception - become unavailable.<sup>[11]</sup> It is incumbent upon the implementation of `start` to use only asynchronous reporting mechanisms, such as catching its own exceptions and directing them down the error channel to the receiver.<sup>[11]</sup>

Leahy specifies this requirement precisely in his review of the initial `use_sender` implementation<sup>[8]</sup>: the adaptor "needs to wrap the associated executor, use this wrapping to wrap all submitted intermediate completion handlers, catch all exceptions thrown thereby, and coalesce them to `set_error_t(std::exception_ptr)`."<sup>[8]</sup> And so Leahy wraps the executor. His `completion_token`<sup>[2]</sup> defines an executor wrapper whose `execute` member function wraps every submitted invocable in a `run_` method that creates a frame (as we shall see in the following section) and catches all exceptions:

```cpp
template <typename F>
void execute(T&& t) const noexcept
{
    self_.run_(
        [&]() { ex_.execute(
            wrap_(static_cast<T&&>(t))); });
}
```

Of course, the executive underlying the wrapper embodies whatever execution policy it embodies.<sup>[11]</sup> The work may be placed on a queue and later dequeued and invoked somewhere that is not underneath the wrapper on the call stack. And so it is insufficient to wrap on the outside; Leahy also intrudes inside `execute` and wraps therein as well.<sup>[11]</sup> Two associator specializations - `associated_executor` and `associated_allocator`<sup>[2]</sup> - inject this wrapping into AIO, causing AIO to use Leahy's executor logic at every level of analysis.<sup>[11]</sup>

But if throwing an exception can cause AIO to stop making forward progress on an operation, why do we imagine that throwing an exception is the only way in which AIO can be induced to stop making forward progress on an operation?<sup>[11]</sup>

## 4. Abandonment and the Frame Destructor

Leahy identifies a second category of forward-progress failure beyond exceptions. AIO supports what Leahy terms "abandonment" - one can "simply walk away from a running operation, allow the lifetime of the completion handlers to end, and everything is fine."<sup>[8]</sup> `std::execution` does not tolerate this.<sup>[8]</sup> For an operation which has been started, exactly one completion signal must be sent.<sup>[8]</sup>

The modal way that well-written AIO applications effectuate shutdown is to simply stop calling `run` on the execution context, let destructors run, never make forward progress on outstanding operations, and gracefully exit the scope.<sup>[11]</sup> This formulation works perfectly in AIO applications.<sup>[11]</sup> It does not work under structured concurrency, whereunder it is incumbent upon the bridge to detect abandonment and coalesce it to `set_stopped_t()`.<sup>[8]</sup>

And so Leahy builds the `frame_` class. His `operation_state_base`<sup>[2]</sup> in NVIDIA's stdexec reifies the above-described requirements as five members:

```cpp
Receiver r_;
asio_impl::cancellation_signal signal_;
std::recursive_mutex m_;
frame_* frames_{nullptr};
std::exception_ptr ex_;
bool abandoned_{false};
```

A recursive mutex. An intrusive linked list of stack frames for lifetime tracking. An exception pointer. An abandonment flag. A stop callback (stored separately as an optional). The `frame_` destructor<sup>[2]</sup> implements structured concurrency finalization: if the current frame is the last frame on the linked list and the completion handler has been abandoned, it releases the lock and sends either `set_error` (if an exception was stored) or `set_stopped` (if no exception) through to the receiver. The `completion_handler` destructor<sup>[2]</sup> detects abandonment by creating a frame and setting the `abandoned_` flag to `true`.

Note that Leahy's `frame_` destructor visits every branch of the state machine. Is the pointer null? Then the operation has already completed and there is no work to do. Otherwise: remove the frame from the intrusive linked list. Compute whether this frame should finalize the operation. If there are no frames remaining and the handler has been abandoned, finalize.<sup>[11]</sup> Every path is enumerated. No branch is left unaddressed.

This machinery maintains every invariant of structured concurrency. **The question the machinery raises is why these invariants require this much maintenance.**

The equivalent machinery in a coroutine-native I/O library is a pre-allocated `resume_ctx` containing an executor reference and a continuation pointer, and a callback that posts the continuation to the executor.<sup>[9]</sup> No recursive mutex. No intrusive linked list. No abandonment flag. No frame destructor.

But the bridge machinery is not the only place where Leahy's integration imposes structural costs. Let us examine what happens to the values themselves.

## 5. The Channel Mapping and Partial Success

AIO operations complete by invoking their completion handler with a leading error code and trailing arguments. A call to `async_read` delivers `(boost::system::error_code, std::size_t)` - the status and the byte count. Both values are always present. A read that returns `ECONNRESET` with 47 bytes means 47 bytes arrived before the peer reset the connection. The byte count is not redundant with the error code.

The sender model provides three completion channels: `set_value`, `set_error`, and `set_stopped`. Leahy must route compound AIO results into discrete channels. His `use_sender`<sup>[3]</sup> defines a receiver whose `set_value` overload, when the first argument satisfies `is_error_code`, dispatches along three paths:

```cpp
void set_value(T&& t, Args&&... args)
    && noexcept
{
    if (!t)
    {
        ::STDEXEC::set_value(
            static_cast<Receiver&&>(r_),
            static_cast<Args&&>(args)...);
        return;
    }
    if (/* cancellation check */)
    {
        ::STDEXEC::set_stopped(
            static_cast<Receiver&&>(r_));
        return;
    }
    ::STDEXEC::set_error(
        static_cast<Receiver&&>(r_),
        use_sender::to_exception_ptr(
            static_cast<T&&>(t)));
}
```

On the first path (no error), the error code is stripped and the remaining arguments - including the byte count - are forwarded through `set_value`. On the second path (cancellation), `set_stopped` is sent and all arguments are discarded. On the third path (error), the error code is converted to `std::exception_ptr` and sent through `set_error`. The remaining arguments - including the byte count - are not forwarded. They are discarded.

Leahy recognized this structural tension in his initial review of the `use_sender` design<sup>[8]</sup>. He observed that the error-code-to-channel coalescing is "best left as a separate algorithm to ensure that 'partial success' has its context fully preserved."<sup>[8]</sup> The implementation thereof, however, coalesces truthy error codes to `set_error_t(std::exception_ptr)` and discards the remaining arguments, because the three-channel model affords no alternative which preserves both the error and the values transmitted thereby without routing I/O errors through `set_value`.

The coroutine equivalent:

```cpp
auto [ec, n] =
    co_await stream.read_some(buf);
```

Both values. No channel to choose. No data lost. The application has the full compound result and decides what to do with it.

**Leahy's code discards the byte count on the error path. No mapping within the three-channel model preserves it.**

### 5.1. The Prescribed Algorithm

Leahy prescribed that the error-code-to-channel coalescing is "best left as a separate algorithm to ensure that 'partial success' has its context fully preserved."<sup>[8]</sup> Of course, the prescription is structurally sound - it identifies the correct layer at which the problem should be addressed, and it names the obligation precisely: the context of partial success must be preserved in its entirety.

Which brings us to the question the prescription raises: what completion signature would such an algorithm produce?

The algorithm is incumbent upon routing a compound result - an error code together with a byte count - through the channels available to it. And so it must choose. If the algorithm sends both values through `set_value` - that is, `set_value_t(error_code, size_t)` - then I/O errors travel the value channel, and downstream algorithms (`then`, `let_value`, `when_all`) cannot distinguish success from failure by channel alone. The semantic purpose of channel discrimination - the raison d'etre thereof - is defeated. Every consumer must inspect the error code manually, which is precisely the convention that obtained before channels existed.

If instead the algorithm preserves channel semantics by routing the error code through `set_error`, the byte count has no destination. `set_error` accepts a single argument. The operation state's lifetime ends at completion signal invocation (per P3373R2's<sup>[4]</sup> own formulation of operation state lifetimes). There is no storage thereunto which the byte count could be attached. There is no side channel. The data is destroyed at the abstraction floor.

And so the prescribed algorithm must choose between preserving data and preserving channel semantics. No formulation preserves both. The dilemma is not an engineering difficulty awaiting a sufficiently clever implementation. It is a structural consequence of the three-channel model applied to compound results.

Kohlhoff identified this problem in P2430R0 (2021).<sup>[15]</sup> Five years and ten revisions of P2300 have elapsed. No algorithm has been published - not by Leahy, not by the P2300 authors, not in any sender library in the published record. Leahy's own merged implementation (PR #1503) ships the mapping that discards the byte count, because the three-channel model affords no alternative.

The coroutine model faces no such choice.

But the channel mapping is not the only place where Leahy's published work identifies a structural cost of the sender model applied to I/O. Let us examine what Leahy found when he turned his attention to the algorithms themselves.

## 6. Split: Allocation, Ownership, Eagerness

Leahy's P3682R0<sup>[5]</sup> proposes removing `std::execution::split`. The paper identifies three deficiencies thereof.

The first is dynamic allocation. A state must be dynamically allocated when a `split` sender is created, due to the fact it is shared by the original sender, all senders derived by copying the above, and all operation states derived by connecting either of the above.<sup>[5]</sup> Not only is this an issue due to the performance overhead of dynamic allocation, but the dynamic allocation occurs so early in the `std::execution` workflow (i.e. at sender creation time) that the allocation cannot be parameterized by the custom allocator provided by the receiver's environment (i.e. at connect time).<sup>[5]</sup>

The second is shared ownership. The state associated with a `split` sender is shared, involving reference counting which can usually be avoided through structured concurrency.<sup>[5]</sup>

The third is conditional eagerness. P2300R10<sup>[12]</sup> states that eager execution was removed from earlier revisions because it "has a number of negative semantic and performance implications."<sup>[12]</sup> Despite this, `std::execution::split` represents execution which is, conditionally and from certain points of view, eager.<sup>[5]</sup>

Leahy's alternative is `let_value` composed with `when_all`:

```cpp
std::execution::sender auto shared =
    /* ... */;
(void)std::this_thread::sync_wait(
    std::move(shared)
    | std::execution::let_value(
        [](auto&&... values) {
            return std::execution::when_all(
                std::execution::just(
                    std::ref(values)...)
                | /* a */,
                std::execution::just(
                    std::ref(values)...)
                | /* b */);
        }));
```

No dynamic allocation. No shared ownership. No conditional eagerness. Leahy's proposal: "Remove `std::execution::split`. Replace it with nothing."<sup>[5]</sup> The committee agreed. SG1 forwarded. Plenary adopted.

But `split` is not the only algorithm Leahy found to be doing more than its contract requires.

## 7. When_all: The Ronseal Principle

Leahy's P3887R1<sup>[6]</sup> identifies that `std::execution::when_all` injects stopped completions for children that are not capable of sending stopped, belying the reasonable expectations of the consumer.<sup>[6]</sup> The algorithm does more than what it says on the tin - it is not, in Leahy's terminology, a "Ronseal algorithm."<sup>[6]</sup>

P2300R10<sup>[12]</sup> describes `when_all` thusly: "when_all returns a sender that completes once all of the input senders have completed."<sup>[12]</sup> This articulation, and the single responsibility which springs therefrom, have nothing to do with eager checking for stop requests - functionality which can be provided by a separate algorithm.<sup>[6]</sup> And so the consequence of the current formulation is that even given a set of child senders none of which send `set_stopped_t()`, a `when_all` sender unconditionally reports that it can send `set_stopped_t()`.<sup>[6]</sup>

Were it the case that the additional behavior is advantageous or benign, the above might not be an issue. But operations which the user reasonably believed would be started and allowed to run are skipped,<sup>[6]</sup> which is germane to async scopes (which must be joined for correctness<sup>[6]</sup>) and to generalized async RAII. There is a narrower, less astonishing, Ronseal algorithm inside `std::execution::when_all`.<sup>[6]</sup> C++26 should ship that, not what is currently in the working draft.<sup>[6]</sup>

SG1 agreed (8-3-1-0-0). LEWG agreed (10-5-0-0-0).

But the algorithmic corrections address individual symptoms. Let us examine one more observation before considering what the symptoms share.

## 8. The Language Change

Leahy's P3950R0<sup>[7]</sup> proposes that `return_value` and `return_void` are not mutually exclusive. The standard specifies that if searches for the names `return_void` and `return_value` in the scope of the promise type each find any declarations, the program is ill-formed.<sup>[7]</sup> This restriction has been present in its current form since N4499<sup>[13]</sup>. A different form thereof was present in N4403.<sup>[14]</sup>

No task type in the intervening decade - cppcoro, folly::coro, libunifex's own task, TooManyCooks, Capy - has required this restriction to be removed.

`std::execution::task` requires it to be removed. The library implementation of a function provided by `std::execution`'s senders and receivers is capable of completing successfully in multiple ways, obviating the need for a separate sum type<sup>[7]</sup> - but attempting to map `set_value_t()` (i.e. successful completion with no values) alongside any other `set_value_t(...)` form does not work, not for any conceptual reason, but simply because the standard bans it by fiat.<sup>[7]</sup>

Leahy identifies the restriction as fundamentally arbitrary, unnecessarily making `void` a special case.<sup>[7]</sup> Said restriction should for all the preceding reasons be removed.<sup>[7]</sup>

**Leahy proposes changing the language. The language has not needed changing for any other task type.**

### 8.1. Two Obligations

Both the coroutine-native task and `std::execution::task` are incumbent upon the same obligation: furnish a well-formed promise type that maps the task's successful completion semantics into the coroutine language model. Let us examine how each discharges the obligation thereby imposed.

**The coroutine-native task.** Given `task<T>` under the language rules as given:

- If `T` is `void`, the promise provides `return_void()`.
- If `T` is not `void`, the promise provides `return_value(T)`.
- The cases are mutually exclusive by the type parameter. The promise is well-formed. The obligation is discharged.

Of course, the construction is unremarkable. The type parameter partitions the two cases and no further machinery is needful.

**`std::execution::task`.** Given a task which must accommodate completion signatures `set_value_t()` and `set_value_t(T...)` simultaneously:

- The promise must provide `return_void()` for `set_value_t()`.
- The promise must provide `return_value(T...)` for `set_value_t(T...)`.
- Both names are thereby present in the promise type. Per [dcl.fct.def.coroutine]/p6, the program is ill-formed.
- The obligation cannot be discharged under the rules as given.
- Amend the rules: adopt P3950R0.<sup>[7]</sup> Under the amended rules, both names may coexist. The promise is well-formed. The obligation is discharged.

And so the obligation is fulfilled - but only after the language has been changed to permit it.

Leahy identifies the restriction as arbitrary, and the characterization is not in dispute. But the arbitrariness thereof and its significance as evidence are not in tension. An arbitrary restriction which lay dormant for a decade - encountered by no task type in cppcoro, folly::coro, libunifex, TooManyCooks, or Capy - was encountered by exactly one design. The encounter is germane precisely because the restriction is arbitrary: `std::execution::task` derives its return forms from the sender completion algebra rather than declaring them directly, and it is this derivation which creates the collision. A design that declares its return type is robust to arbitrary language restrictions. A design that derives its return type from an external algebra is not.

Which brings us to the question: is it the restriction that is deficient, or is it the derivation?

## 9. What the Chain Reveals

The preceding sections trace an iterative chain of observations, each arising from the published work of one practitioner. Rather than iteratively discovering the whole problem domain, let us take a step back and look at the totality thereof.<sup>[11]</sup>

Six observations from Leahy's published work:

1. A bridge<sup>[2]</sup> that requires a recursive mutex, an intrusive linked list, structured concurrency finalization in the `frame_` destructor, abandonment detection in the `completion_handler` destructor, two associator specializations, and a wrapped executor - where the equivalent awaitable integration requires a pre-allocated context structure, a continuation node, and a callback.

2. A channel mapping<sup>[3]</sup> that discards the byte count on the error path because the three-channel model affords no mapping which preserves both the error code and the remaining arguments without routing I/O errors through `set_value`.

3. A recommendation<sup>[8]</sup> that partial success should have its context fully preserved, followed by an implementation that cannot preserve it within the constraints of the available channels.

4. An algorithm removed<sup>[5]</sup> for dynamic allocation at sender creation time (before the receiver's allocator is available), shared ownership via reference counting, and conditional eagerness. The committee agreed.

5. An algorithm corrected<sup>[6]</sup> for injecting stopped completions that no child is capable of sending, belying the reasonable expectations of the consumer. The committee agreed.

6. A core language change<sup>[7]</sup> needed by `std::execution::task` and by no other task type in a decade of coroutine libraries - not for any conceptual reason, but because the standard bans a simultaneous capability by fiat.

Each of the above is individually addressable. Leahy has addressed several of them; the committee has adopted or forwarded the remainder. But the question the totality raises is not whether each observation can be resolved in isolation. The question is what property the six observations share - what characteristic of the domain they occupy would cause a single practitioner, working from within the sender model, to encounter all six.

**Six observations from one practitioner. One boundary.**

## 10. Falsification

The above-described observations would be discharged - that is, explained by causes other than a shared domain boundary - if any of the following were demonstrated:

- A sender design that achieves zero per-operation allocation under type erasure for byte-oriented I/O, matching the coroutine model's structural property documented in Section 4.

- A channel mapping that preserves both the error code and the byte count without routing I/O errors through `set_value`, matching the coroutine model's compound result documented in Section 5.

- A motivation for P3950R0<sup>[7]</sup> that does not involve the sender channel model's interaction with coroutine promise types - that is, a reason the language restriction would need to be removed even if `std::execution::task` did not exist.

- Evidence that `split`'s eagerness, dynamic allocation, and shared ownership served a use case within the sender model's natural domain (i.e. compute dispatch and heterogeneous scheduling) that has no alternative expression via `let_value` and `when_all`.

## 11. Conclusion

Leahy's work demonstrates that the sender model maintains its invariants under I/O integration. The bridge works. The channel mapping works. The algorithmic corrections were adopted. The language change was proposed.

The question the work raises is whether those invariants are the right ones for that domain.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[9]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[10]</sup>, coroutine-native I/O libraries under the C++ Alliance. The author has a stake in the coroutine model's adoption.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

Coroutine-native I/O cannot express compile-time work graphs. This is a genuine limitation.

This paper examines the published work of Robert Leahy - production code, WG21 papers, CppCon talks, and open-source review comments - and asks what his observations share. Every claim herein is sourced to Leahy's published work.

This paper asks for nothing.

## Acknowledgements

Robert Leahy, whose published work this paper examines in its entirety. Leahy's contributions to the sender model - production code in NVIDIA's stdexec, four WG21 papers adopted or forwarded by the committee, and CppCon talks whose constructive-proof methodology has informed this paper's argumentation - constitute the most thorough published examination of `std::execution`'s integration with existing asynchronous ecosystems. His exemplary work let us build proofs by iterative refinement: construct the simplest version of a design, identify why it is wrong, fix it, discover what the fix breaks, and repeat until every path is covered and every invariant holds. This paper is indebted to Leahy's exhaustive public record and to the rigor with which he maintains it.

## References

[1] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec) - Reference implementation of `std::execution` (NVIDIA, 2024).

[2] [exec/asio/completion_token.hpp](https://github.com/NVIDIA/stdexec/blob/main/include/exec/asio/completion_token.hpp) - AIO-to-sender bridge (Robert Leahy, 2025).

[3] [exec/asio/use_sender.hpp](https://github.com/NVIDIA/stdexec/blob/main/include/exec/asio/use_sender.hpp) - Sender completion token (Robert Leahy, 2025).

[4] [P3373R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3373r2.pdf) - "Of Operation States and Their Lifetimes" (Robert Leahy, 2025).

[5] [P3682R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3682r0.pdf) - "Remove std::execution::split" (Robert Leahy, 2025).

[6] [P3887R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3887r1.pdf) - "Make when_all a Ronseal Algorithm" (Robert Leahy, 2025).

[7] [P3950R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3950r0.pdf) - "return_value & return_void Are Not Mutually Exclusive" (Robert Leahy, 2025).

[8] [NVIDIA/stdexec PR #1501](https://github.com/NVIDIA/stdexec/pull/1501) - "Adapt boost::asio to stdexec" review comments (Robert Leahy, 2025).

[9] [Capy](https://github.com/cppalliance/capy) (C++ Alliance).

[10] [Corosio](https://github.com/cppalliance/corosio) (C++ Alliance).

[11] [std::execution in Asio Codebases: Adopting Senders Without a Rewrite](https://www.youtube.com/watch?v=S1FEuyD33yA) - CppCon 2025 (Robert Leahy, 2025).

[12] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Eric Niebler, Micha&lstrok; Dominiak, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Bryce Adelstein Lelbach, 2024).

[13] [N4499](https://www.open-std.org/JTC1/SC22/WG21/docs/papers/2015/n4499.pdf) - "Draft wording for Coroutines (Revision 2)" (Gor Nishanov, 2015).

[14] [N4403](https://www.open-std.org/JTC1/SC22/WG21/docs/papers/2015/n4403.pdf) - "Draft wording for Resumable Functions" (Gor Nishanov, 2015).

[15] [P2430R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2430r0.pdf) - "Partial success scenarios with P2300" (Chris Kohlhoff, 2021).
