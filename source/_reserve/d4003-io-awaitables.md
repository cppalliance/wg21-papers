---
title: "A Minimal Coroutine Execution Model"
document: P4003R4
date: 2026-07-01
intent: ask
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
  - "Steve Gerbino <steve@gerbino.co>"
  - "Mungo Gill <mungo.gill@me.com>"
---

## Abstract

C++20 coroutines suspend and resume, but the language does not determine where resumption occurs, how cancellation propagates, or where coroutine frames are allocated. No standard protocol exists for these concerns. Every library invents its own execution model, and tasks from one framework do not compose with executors from another.

The _IoAwaitable_ protocol resolves three concerns at every suspension point: executor affinity determines where the coroutine resumes, stop token propagation carries cancellation forward, and frame allocator delivery controls where frames are allocated. The motivating use case is a single line:

```cpp
co_await f();
```

For this to work, something must decide where the coroutine resumes, whether it should stop, and where its frame is allocated. The _IoAwaitable_ protocol provides these three things through a two-argument `await_suspend` that makes protocol violations a compile error.

A companion paper, [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup>, provides the design rationale, evidence framework, preemptive objections, and analysis of alternative approaches.

Everything in this paper comes from a complete implementation on three platforms: [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup> (protocol) and [Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup>. A self-contained demonstration is available on [Compiler Explorer](https://godbolt.org/z/Wzrb7McrT)<sup>[4]</sup>.

This paper asks LEWG to advance the _IoAwaitable_ protocol as a standard coroutine execution model.

---

## Revision History

### R4: July 2026 (post-Brno mailing)

* Added Section 7 "One Operation Type Satisfies Both Protocols": the _AwaitableSender_ concept and `awaitable_sender_base` mixin prototyped in Capy, the completion channel mapping, receiver-environment interop, and the frame-free crossing. Conclusion and straw poll renumbered to Sections 8 and 9.
* P4092R0 and P4093R2 links in the conclusion promoted to formal references. Added P3164R4 reference.
* Abstract rewritten. Expanded from a brief committee ask to a full abstract: problem statement, three named concerns, two-argument `await_suspend` as the key mechanism, LEWG ask moved to end.
* Section 2 commentary replaced with description of the eight standard facilities and what users build against them. Companion protocol description expanded to name four alternatives evaluated in P4172R0.
* Section 3 introduction replaced with structural overview mapping subsections 3.1-3.5 to their concerns. Section 3.1 reworded from rhetorical questions to specification language.
* Section 4 introduction replaced with structural overview of six facilities (4.1-4.6). Generic P4172R0 cross-references replaced with specific section citations (5.1, 5.2, 7, 8) and substantive descriptions. Added P4127R0 citation in Section 4.5.
* Section 5 opening paragraph added defining structured concurrency and the three-phase ownership chain. Bold emphatic conclusion replaced with declarative summary.
* Section 6: bare superscript references to P4090R0 and P4091R0 expanded to substantive inline descriptions. Added P4172R0 Section 6.2 citation for type erasure analysis.
* Conclusion expanded from one sentence to four paragraphs: protocol description, adoption benefits (TAPS, bridge papers P4092R0/P4093R2), consequences of non-adoption, and the LEWG ask.

### R3: May 2026 (pre-Brno mailing)

* Corrected internal section cross-reference in Acknowledgements (symmetric transfer is Section 4.3, not 4.2).
* Formatting corrections.

### R2: April 2026 (post-Croydon mailing)

* Title changed from "Coroutines for I/O" to "A Minimal Coroutine Execution Model".
* Reframed as a coroutine execution model. Networking is one consumer, not the identity.
* Motivating example changed from `socket.read_some(buf)` to `co_await f()`.
* Introduction replaced with Disclosure. Paper repositioned within the Network Endeavor.
* Sections 2-7 (Networking's Essentials, The Protocol, Executor concept, The Frame Allocator, Ergonomics of Type Erasure, io_awaitable_promise_base Mixin) replaced with new Sections 2-6 (What We Get, What Coroutines Need, The IoAwaitable Protocol, IoAwaitable Is Structured Concurrency, Why Not `exec::as_awaitable`?).
* Evidence Framework (Section 9), example wording (Section 11), and Appendices A-B removed. Design choices, rationale, and post-adoption retrospectives moved to companion paper [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup>.
* Networking quotes, Kona poll context, and SG14 position moved to [P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf)<sup>[5]</sup>.
* Five straw polls replaced with one.
* References pruned and renumbered.

### R1: March 2026 (pre-Croydon mailing)

* Added "Why Standardize" subsection to Section 1: committee record, tower of abstraction argument, P4133 cost/benefit analysis.
* Expanded implementation evidence in Section 3.
* Added Section 9 "Evidence Framework" addressing P4133 requirements: competing designs, case against standardization, decision record, domain coverage, post-adoption metrics, retrospective commitment, prediction registry.
* Expanded sequence diagram with explicit `set_environment`, `set_continuation`, and `handle.resume()` steps.
* Renamed "Boost.Http" to "Http" in body and references.
* Closed TLS spoilage gap in Section 5.4: intervening code between resume and child creation can overwrite the thread-local frame allocator. Introduced `safe_resume` save/restore protocol.
* Added non-normative note to executor concept (Section 11.3.3) requiring event loop pump sites to save and restore TLS around `.resume()` calls.
* Replaced `std::coroutine_handle<>` with `continuation` in the executor interface. The `continuation` struct embeds an intrusive list pointer, eliminating per-post heap allocation.
* Editorial: fixed list formatting, code line wrapping, acknowledgements.

### R0: March 2026 (pre-Croydon mailing)

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

This paper is part of the [Network Endeavor](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf) ([P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf))<sup>[5]</sup>, a project to bring coroutine-native I/O to C++.

Falco and Gerbino developed and maintain [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup> and believe coroutine-native I/O is a practical foundation for networking in C++.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

---

## 2. What We Get

If only this proposal ships and nothing else, we get:

| What `std` provides | What users can write |
|---|---|
| _IoAwaitable_ | Interoperable tasks, awaitables |
| _IoRunnable_ | Interoperable launch functions |
| _Executor_ | Interoperable executors |
| _ExecutionContext_ | User-defined execution contexts |
| `execution_context` | Platform event loops |
| `get_cached_frame_allocator`, `set_cached_frame_allocator` | Custom frame allocators |
| `executor_ref` | (protocol) |
| `io_env` | (protocol) |

The left column is the standard's commitment - eight named facilities. The right column is what library authors and users build against that surface: interoperable tasks, awaitables, launch functions, executors, and custom frame allocators from any vendor.

This protocol is a companion to [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[6]</sup> `std::execution`. [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> evaluates four alternatives - sender/receiver, Boost.Asio completion handlers, pure coroutine libraries, and ecosystem-only - and concludes that each has structural limitations for I/O: sender/receiver requires a second template parameter on task types, Asio lacks standard frame allocator propagation, pure coroutine libraries are mutually incompatible, and twenty years of ecosystem behavior shows a shared vocabulary requires standardization. See [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> for the full design rationale and analysis.

---

## 3. What Coroutines Need

A coroutine that suspends needs three things resolved at the moment of suspension: who resumes it, whether it should stop, and where child frames come from. These map to five operational questions. Sections 3.1-3.2 address resumption - the executor. Section 3.3 addresses cancellation - the stop token. Section 3.4 addresses launching from non-coroutine code. Section 3.5 addresses frame allocation.

### 3.1 How to Suspend

Standard C++ coroutine syntax provides one statement for suspension:

```cpp
co_await f();
```

When this executes, the coroutine suspends and control passes to the awaitable returned by `f()`. That awaitable holds the coroutine handle and must eventually resume it. The specification does not determine which thread the coroutine resumes on or which component controls resumption.

```cpp
std::coroutine_handle<> h = /* ...the suspended coroutine... */;

h.resume();  // resumes on the current thread - which may be wrong
```

This is the question that drives the entire protocol. The awaitable cannot just call `h.resume()` - that resumes on the current thread, possibly while holding a lock, possibly re-entering code that is not re-entrant. Something must decide where and how the coroutine wakes up.

Every awaitable needs three things at the moment of suspension: who resumes me (executor), should I stop (stop token), and where do child frames come from (frame allocator).

The I/O payoff is immediate. Consider the awaitable for a platform operation:

```
auto [ec, n] = co_await stream.read_some(buf);
```

The same three concerns apply: the reactor completes the read and holds a coroutine handle that must resume on the right thread. Synchronous awaitables return `true` from `await_ready` and never suspend at all. The protocol handles both.

### 3.2 How to Resume

The reactor has a coroutine handle. It cannot just call `resume()`. Something decides where and how the coroutine wakes up. That something is the executor:

```cpp
executor ex = /* ...the coroutine's executor... */;

ex.post( h ); // (notional)
```

The executor queues the coroutine for resumption under the application's control. That is its entire job. The full _Executor_ concept is presented in Section 4.

### 3.3 How to Stop

The stop mechanism should be invisible until you need it. Most coroutines never touch it. But when you need it, it should be obvious:

```cpp
auto token = co_await get_stop_token;

if (token.stop_requested())
    co_return;
```

One line to get the token. One check. Built on `std::stop_token`.

### 3.4 How to Launch

A regular function cannot `co_await` (see [P4035R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4035r0.pdf)<sup>[7]</sup> for a discussion of coroutine escape hatches). To start a coroutine chain, you call a launch function:

```cpp
run_async( ex )( my_coroutine() );
```

The executor is required. The stop token and frame allocator are optional. This is where the three concerns from 3.1-3.3 come together - the launch function binds them to the coroutine chain.

### 3.5 How to Allocate

Every coroutine has a frame, and every frame must be allocated. This is why coroutines look slow. Despite the cost, the right frame allocator makes coroutines performant. Thus, the frame allocator must be a first-class citizen.

Frame allocators come in two versions:

1. A classic typed allocator (e.g. `std::allocator`, a custom pool allocator) - the user's own type
2. A `std::pmr::memory_resource*` - type-erased, for when the concrete type does not matter

| Platform    | Frame Allocator  | Time (ms) | Speedup |
|-------------|------------------|----------:|--------:|
| MSVC        | Recycling        |   1265.2  |   3.10x |
| MSVC        | mimalloc         |   1622.2  |   2.42x |
| MSVC        | `std::allocator` |   3926.9  |       - |
| Apple clang | Recycling        |   2297.08 |   1.55x |
| Apple clang | `std::allocator` |   3565.49 |       - |

The protocol must:

- Provide a reasonable, customizable default
- Propagate the frame allocator to every coroutine frame in the chain automatically
- Keep function signatures clean, unless the programmer needs otherwise
- Allow a coroutine to `co_await` a new chain with a different frame allocator

---

## 4. The _IoAwaitable_ Protocol

The protocol resolves the three concerns from Section 3 through six facilities. `io_env` (4.1) bundles executor, stop token, and frame allocator into a single struct. _IoAwaitable_ (4.2) defines the two-argument suspension contract that delivers the environment to every awaitable. _Executor_ (4.3) and `execution_context` (4.4) define resumption and the platform reactor. Frame allocator delivery (4.5) solves the `operator new` timing problem. _IoRunnable_ (4.6) extends the contract for launch functions that cannot `co_await`.

### 4.1 `io_env`

The `io_env` struct contains the three members a coroutine needs: the executor, the stop token, and the frame allocator:

```cpp
struct io_env
{
    executor_ref executor;
    std::stop_token stop_token;
    std::pmr::memory_resource* frame_allocator = nullptr;
};
```

### 4.2 _IoAwaitable_

Implementations and library authors provide types satisfying _IoAwaitable_:

```cpp
template< typename A >
concept IoAwaitable =
    requires(
        A a, std::coroutine_handle<> h, io_env const* env )
    {
        a.await_suspend( h, env );
    };
```

The two-argument `await_suspend` is the mechanism. The C++20 compiler only calls the standard one-argument `await_suspend(coroutine_handle<>)`. The promise type's `await_transform` bridges the two forms by wrapping every IoAwaitable in a `transform_awaiter`:

```cpp
template<class Awaitable>
struct transform_awaiter
{
    std::decay_t<Awaitable> a_;
    promise_type* p_;

    bool await_ready() noexcept
        { return a_.await_ready(); }

    template<class Promise>
    auto await_suspend(
        std::coroutine_handle<Promise> h) noexcept
    {
        return a_.await_suspend(
            h, p_->environment());
    }

    decltype(auto) await_resume()
        { return a_.await_resume(); }
};
```

When a parent coroutine evaluates `co_await child`, the compiler calls `await_transform` on the parent's promise, which wraps the child in a `transform_awaiter` that captures the promise pointer. The compiler then calls the wrapper's one-argument `await_suspend(handle)`. The wrapper reads the parent's environment via `p_->environment()` and forwards both the handle and the `io_env const*` to the child's two-argument `await_suspend`. The child stores the environment in its own promise via `set_environment`. When the child itself does `co_await`, the same three steps repeat - propagation is automatic and invisible to the coroutine author.

A `task` needs only one template parameter. The environment is passed as a pointer because the launch function owns the `io_env` and every coroutine in the chain borrows it - pointer semantics make the ownership model explicit. The `io_awaitable_promise_base` CRTP mixin (see [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> Appendix C) provides the `await_transform` dispatch and the `transform_awaitable` override point; derived promise types install the `transform_awaiter` by overriding `transform_awaitable`.

The two-argument signature is also a compile-time boundary check. A non-compliant awaitable fails to compile. A compliant awaitable in a non-compliant coroutine fails to compile. Both sides of every suspension point are statically verified. In a world with multiple coexisting async models, a coroutine that accidentally `co_await`s across model boundaries should fail at compile time, not silently misbehave at runtime. [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> Section 5.1 demonstrates that the standard C++20 `await_suspend(coroutine_handle<Promise>)` compiles silently when promise and awaitable are mismatched across async models; the two-argument signature is the only form that makes protocol violations a compile error. See [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> for the full alternative design discussion.

### 4.3 _Executor_

```cpp
struct continuation
{
    std::coroutine_handle<> h;
    continuation* next = nullptr;
};

template<class E>
concept Executor =
    std::is_nothrow_copy_constructible_v<E> &&
    std::is_nothrow_move_constructible_v<E> &&
    requires( E& e, E const& ce, E const& ce2,
              continuation& c ) {
        { ce == ce2 } noexcept -> std::convertible_to<bool>;
        { ce.context() } noexcept;
        requires std::is_lvalue_reference_v<
            decltype(ce.context())> &&
            std::derived_from<
                std::remove_reference_t<
                    decltype(ce.context())>,
                execution_context>;
        { ce.on_work_started() } noexcept;
        { ce.on_work_finished() } noexcept;
        { ce.dispatch( c ) }
            -> std::same_as< std::coroutine_handle<> >;
        { ce.post(c) };
    };

class executor_ref
{
    void const* ex_ = nullptr;
    detail::executor_vtable const* vt_ = nullptr;

public:
    template<Executor E>
    executor_ref(E const& e) noexcept
        : ex_(&e), vt_(&detail::vtable_for<E>) {}

    std::coroutine_handle<> dispatch(continuation& c) const;
    void post(continuation& c) const;
    execution_context& context() const noexcept;
};
```

The `continuation` struct pairs a `coroutine_handle<>` with an intrusive `next` pointer, allowing executors to queue continuations without allocating a separate node - eliminating the last steady-state allocation in the hot path. `dispatch` returns a `coroutine_handle<>` for symmetric transfer: if the caller is already in the executor's context, it returns `c.h` directly for zero-overhead resumption. Otherwise it queues and returns `noop_coroutine()`. `post` always defers. The `executor_ref` type-erases any _Executor_ as two pointers - one indirection (~1-2 nanoseconds<sup>[8]</sup>) is negligible for I/O operations at 10,000+ nanoseconds. [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> Section 5.2 traces each of the seven executor concept requirements to a concrete failure on removal: nothrow copy/move for exception safety at suspension points, `context()` for frame allocator discovery, `on_work_started`/`on_work_finished` to prevent premature return from `ctx.run()`, and `operator==` as forward investment for strand support. See [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> for full semantics.

### 4.4 `execution_context`

```cpp
class execution_context
{
public:
    class service
    {
    public:
        virtual ~service() = default;
    protected:
        service() = default;
        virtual void shutdown() = 0;
    };

    execution_context( execution_context const& ) = delete;
    execution_context& operator=(
        execution_context const& ) = delete;
    ~execution_context();
    execution_context();

    template<class T> T& use_service();
    template<class T, class... Args>
        T& make_service( Args&&... args );

    std::pmr::memory_resource*
        get_frame_allocator() const noexcept;
    void set_frame_allocator(
        std::pmr::memory_resource* mr ) noexcept;

protected:
    void shutdown() noexcept;
    void destroy() noexcept;
};

template<class X>
concept ExecutionContext =
    std::derived_from<X, execution_context> &&
    requires(X& x) {
        typename X::executor_type;
        requires Executor<typename X::executor_type>;
        { x.get_executor() } noexcept
            -> std::same_as<typename X::executor_type>;
    };
```

An executor's `context()` returns the `execution_context` - the base class for anything that runs work. The platform reactor lives here. Services provide singletons with ordered shutdown. I/O objects hold a reference to their execution context, not to an executor. This design borrows from [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[9]</sup>.

The execution context holds the default frame allocator. The user can optionally override it, and every coroutine chain launched through that context uses it. This is how the "reasonable, customizable default" from Section 3.5 works in practice.

### 4.5 Frame Allocator Delivery

[P4127R0](https://isocpp.org/files/papers/P4127R0.pdf)<sup>[10]</sup> enumerates every C++20 coroutine customization point and identifies two delivery channels for the allocator to reach `operator new`:

1. **The parameter list.** This is `allocator_arg_t` - it always works and is always available as a fallback, but it should not be the only option.
2. **Out of band.** The allocator is temporarily stashed somewhere the `operator new` can find it.

The protocol specifies accessor functions but leaves the storage mechanism to the implementer:

```cpp
std::pmr::memory_resource*
get_cached_frame_allocator() noexcept;

void
set_cached_frame_allocator(
    std::pmr::memory_resource* mr) noexcept;
```

[P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> Section 8 documents the execution window: `operator new` runs before the coroutine body, so the frame allocator must be in place before the coroutine is called. The `safe_resume` protocol saves and restores one pointer per `.resume()` call, preventing slot spoilage when intervening code resumes coroutines from other chains. See [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> for the full timing constraint analysis and responses to common concerns.

### 4.6 `IoRunnable` and Launch Functions

Someone has to launch the first coroutine. Within a coroutine chain, _IoAwaitable_ alone is sufficient - `co_await` handles lifetime, result extraction, and exception propagation natively. But launch functions cannot `co_await`. They need access to the promise to manage lifetime and extract results. This paper does not propose launch functions - the ecosystem provides them. _IoRunnable_ is the concept that supports them.

Launch functions come in two kinds:

**From regular code: `run_async`.** You cannot `co_await` in `main()`. This is the entry point - the place where synchronous code starts an asynchronous chain. The executor is required. The stop token and frame allocator are optional. Without handlers, the result is discarded and exceptions rethrow on the executor thread. With handlers, both outcomes are explicitly routed:

```cpp
// Fire and forget
run_async( ex )( server_main() );

// Structured: both outcomes routed
run_async( ex,
    [](int result)         { /* use result */   },
    [](std::exception_ptr) { /* handle error */ }
)( compute() );
```

**From a coroutine: `run`.** Switches executor, stop token, or allocator for a subtask. Always `co_await`ed. The parent suspends and resumes only when the child completes - the lexical boundary is enforced by the language. There is no unstructured path through `run`:

```cpp
co_await run( worker_ex )( compute() );
co_await run( source.get_token() )( sensitive_op() );
co_await run( pool )( alloc_heavy_op() );
co_await run( worker_ex, source.get_token(), pool )(
    compute() );
```

Both kinds use two-phase invocation to ensure the frame allocator is cached before the child coroutine's frame is allocated. _IoRunnable_ provides the interface both need:

```cpp
template<typename T>
concept IoRunnable =
    IoAwaitable<T> &&
    requires { typename T::promise_type; } &&
    requires( T& t, T const& ct,
              typename T::promise_type const& cp,
              typename T::promise_type& p )
    {
        { ct.handle() } noexcept
            -> std::same_as<
                std::coroutine_handle<
                    typename T::promise_type> >;
        { cp.exception() } noexcept
            -> std::same_as< std::exception_ptr >;
        { t.release() } noexcept;
        { p.set_continuation(
            std::coroutine_handle<>{} ) } noexcept;
        { p.set_environment(
            static_cast<io_env const*>(
                nullptr) ) } noexcept;
    } &&
    ( std::is_void_v<
        decltype(
            std::declval<T&>().await_resume()) > ||
      requires( typename T::promise_type& p ) {
          p.result();
      });
```

[P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> Section 7 demonstrates both launch functions with full listings. The two-phase invocation syntax - `run_async(ex)(task())` - exists because `operator new` executes before the coroutine body; the first call sets up the environment, the second call invokes the coroutine whose `operator new` reads it. See [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> for detailed examples and implementation guidance.

---

## 5. _IoAwaitable_ Is Structured Concurrency

Structured concurrency requires that every concurrent operation has a known owner at every point in its lifetime. The _IoAwaitable_ protocol provides this guarantee through a three-phase ownership chain:

1. The awaitable owns the suspended coroutine handle.
2. The awaitable submits the operation and transfers ownership to the executor.
3. The executor resumes the coroutine, returning ownership to the coroutine body.

There is always an owner: the coroutine body, the awaitable, or the executor.

This ownership model is possible because the language provides the mechanism:

- `co_await` enforces a lexical boundary. The child completes before the parent continues.
- RAII works inside coroutines. Deterministic destruction is guaranteed.
- Cancellation propagates forward. Destruction propagates backward. Both are automatic.
- The language provides what a library would reimplement.
- The synchronous entry point requires an escape hatch in every async framework. Senders call theirs `sync_wait`.
- `when_all` and `when_any` in [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup> (`include/boost/capy/when_all.hpp`, `when_any.hpp`)

```cpp
auto [ec, counts] = co_await when_all(std::move(reads));

auto result = co_await when_any(std::move(reads));
```

The protocol satisfies structured concurrency: every operation has a known owner, every lifetime is lexically bounded, and cancellation propagates without escape.

### 5.1 Structurable Building Blocks Are More Fundamental

When handlers are provided, the launch is structured - both outcomes are
explicitly routed by the caller:

```cpp
run_async( ex,
    [](int result)         { /* use result */   },
    [](std::exception_ptr) { /* handle error */ }
)( compute() );
```

Without handlers, the result is discarded and exceptions rethrow on the
executor thread. This unstructured path is intentional - [P4035R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4035r0.pdf)<sup>[7]</sup>
explains why launch functions cannot `co_await` and therefore need an escape
hatch. The protocol provides structure when the caller uses it; it does not
forbid escape when the caller needs it.

The handlers are the primitive. Higher-level structured concurrency abstractions
are built from them. A `counting_scope` - tracking N concurrent tasks,
joining when all complete, propagating exceptions - is a handler policy:

```cpp
class counting_scope {
    /* atomic state machine: idle -> waiting -> done */

public:
    template<Executor Ex, IoRunnable Task>
    void spawn(Ex ex, Task t) {
        run_async(ex,
            [this](auto&&...) noexcept          { on_done(); },
            [this](std::exception_ptr e) noexcept { on_except(e); }
        )(std::move(t));
    }

    [[nodiscard]] /* awaitable */ join() noexcept;

private:
    void on_done() noexcept;  // decrements count, resumes
                              // waiter on zero
    void on_except(std::exception_ptr) noexcept; // stores first ep, then on_done()
};
```

A full implementation is available in [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup>
(`include/boost/capy/ex/when_all.hpp`).

The protocol provides the building block. `counting_scope` is one policy built
on it. The argument that senders provide structured concurrency and coroutines
do not has it backwards: the _IoAwaitable_ protocol is the layer from which
structured concurrency constructs are assembled.

---

## 6. Why Not `exec::as_awaitable`?

`std::execution` provides `exec::as_awaitable`, which wraps a sender as an awaitable. Both models work. The table shows the cost differential under type erasure:

| Property                                       | Returns awaitable                | Returns sender                                |
|------------------------------------------------|----------------------------------|-----------------------------------------------|
| Frame allocations                              | 1                                | 1                                             |
| Per-operation allocation (under type erasure)  | 0 (preallocated awaitable)       | 1 (`op_state` heap-allocated per `connect`)   |
| Inline completion (`await_ready`)              | Yes - completes, no suspend      | No - `start()` is post-suspend                |
| Synchronous-complete overhead                  | 0 (symmetric transfer)           | `connect`/`start` + trampoline                |

Under type erasure, `connect(sndr, rcvr)` produces a type-dependent `op_state` that must be heap-allocated when either side is erased.

The sender composition algebra does not apply to compound results - such as `[ec, n]` - without data loss or shared state; the sender three-channel model is in tension with `error_code` as a value-channel result. [P4090R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4090r0.pdf)<sup>[11]</sup> demonstrates that sender composition under type erasure requires per-operation heap allocation that awaitables avoid. [P4091R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4091r0.pdf)<sup>[12]</sup> shows that the sender three-channel completion model (value/error/stopped) conflicts with C++ functions that return compound results containing `error_code`.

[P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> Section 6.2 concludes that type erasure through `executor_ref` enables separate compilation and ABI stability at a cost of one vtable indirection per dispatch - bounded, constant, and negligible relative to I/O latency. See [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[1]</sup> for the full analysis.

[P3482R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3482r1.html)<sup>[13]</sup> ("Design for C++ networking based on IETF TAPS") defines a TAPS-shaped networking API surface. The _IoAwaitable_ protocol provides the coroutine execution model beneath it. A TAPS implementation needs coroutines that suspend, resume correctly, cancel, and allocate frames - exactly what this protocol provides. The two are not competing; TAPS is a consumer.

---

## 7. One Operation Type Satisfies Both Protocols

Section 6 compared the cost of awaitable-returning and sender-returning designs. The remaining interoperability question is whether adopting _IoAwaitable_ isolates coroutine I/O from `std::execution`. It does not. The two protocols require no common members, so a single operation type can satisfy both, and a prototype in [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup> (`example/awaitable-sender`) demonstrates the combination. The concept below is the prototype's definition:

```cpp
template<class S>
concept AwaitableSender =
    IoAwaitable<S> &&
    std::execution::sender<S>;
```

An operation models the sender half by deriving a CRTP mixin. The excerpt below is the prototype's mock I/O operation, which follows the shape of a real Corosio operation:

```cpp
struct read_op : awaitable_sender_base<read_op>
{
    // usual IoAwaitable members; the completion
    // signatures follow await_resume()'s result type
};
```

The mixin provides `connect` and deduces the completion signatures from `Derived::await_resume()` through the C++26 `get_completion_signatures` static member function ([exec.getcomplsigs]; [P3164R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3164r4.html)<sup>[14]</sup> removed the earlier nested-typedef form). Nothing is stated twice, so the advertised signatures cannot drift from the implementation. The same object is driven by `co_await` inside a coroutine or by `connect`/`start` inside a sender pipeline, and the two drives call the identical awaitable members.

The completion channels follow the operation's result type, with the mapping [P4093R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r2.pdf)<sup>[15]</sup> establishes for wrapped awaitables:

| `await_resume()` result                         | Completion                                                  |
|-------------------------------------------------|-------------------------------------------------------------|
| `void`                                          | `set_value()`                                               |
| `error_code`, or a one-element tuple-like holding `error_code` | `set_value()` on success, `set_error(ec)` on failure, `set_stopped()` on `operation_canceled` |
| any other single value `T`                      | `set_value(T)`                                              |
| tuple-like `(error_code, payload...)`           | rejected at compile time                                    |

For results that carry an `error_code`, the operation's own outcome selects the channel: a completion reporting `operation_canceled` surfaces as `set_stopped()`, and a successful result is delivered even when a stop request lands while the operation is finishing. The rejection in the last row is the abstraction floor from [P4093R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r2.pdf)<sup>[15]</sup>: completion channels are exclusive, so a partial success - an `error_code` alongside bytes already transferred - cannot cross on any single channel without dropping data. The constraint is structural: the `(error_code, size_t)` result of `read_some` from Section 3.1, `std::tuple<error_code, size_t>`, and any user-defined type of the same shape are refused alike.

The sender half consumes standard receiver environments. At `start()`, the operation state populates `io_env` from sender-side queries: the executor from a `get_io_executor` query when the environment provides one, otherwise from `std::execution::get_scheduler` - so `sync_wait` works unmodified - the stop token from `get_stop_token`, including stoppable tokens other than `std::stop_token`, and the frame allocator from `get_allocator` when the environment supplies a `std::pmr` allocator. The three concerns of Section 3 are filled from the sender vocabulary; `io_env` requires nothing the sender side cannot express.

Crossing into a sender pipeline adds no coroutine frame. The bridge in [P4093R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r2.pdf)<sup>[15]</sup> Appendix A spends one coroutine frame per crossing; the prototype removes the frame by completing through a callback-shaped handle instead of a coroutine. Receivers that supply an executor through `get_io_executor` cross with zero allocations, and bridging a foreign scheduler costs one small allocation per resumption. The handle synthesis relies on the coroutine frame header layout shared by MSVC, GCC, and Clang - a de-facto convention rather than a guarantee of the standard - and a portable implementation would specify the resumption hook directly.

The example below condenses the prototype's test suite; `read_op` is the mock operation shown above:

```cpp
namespace ex = std::execution;

// the same operation, both drives
auto [ec] = co_await read_op{};     // as an IoAwaitable

ex::sync_wait(                      // as a sender
    ex::then(read_op{}, on_read));
```

The test suite verifies that the two drives over the identical operation deliver the same result on the value, error, and stopped channels, and covers cancellation through `std::stop_token` and in-place stop tokens, adaptor pipelines, `sync_wait`, and allocator delivery. [P4092R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r0.pdf)<sup>[16]</sup> demonstrates the opposite direction - consuming senders from coroutine-native code. For generic code, the prototype's `ensure_sender` normalizes either kind of operation: one that already models _AwaitableSender_ passes through unchanged, and an awaitable-only operation is lifted with the `as_sender` wrapper from [P4093R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r2.pdf)<sup>[15]</sup>.

A type that satisfies _IoAwaitable_ can also satisfy the `std::execution` sender concept, with completion signatures deduced from the members it already has. Adopting the protocol selects a coroutine execution model for I/O while leaving the sender path open, and an operation author can serve both callers with one type.

---

## 8. Conclusion

The _IoAwaitable_ protocol provides a standard coroutine execution model. At every suspension point, the protocol delivers three things: an executor that determines where the coroutine resumes, a stop token that carries cancellation forward, and a frame allocator that controls where frames are allocated. The two-argument `await_suspend` makes protocol violations a compile error. Type erasure through `executor_ref` keeps `task<T>` at one template parameter, enabling separate compilation and ABI stability. The protocol is implemented on three platforms and deployed at a derivatives exchange.

If adopted, C++ gains a shared vocabulary for coroutine-based I/O. Library authors build interoperable tasks, executors, and awaitables against a fixed surface. TAPS-shaped networking ([P3482R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3482r1.html)<sup>[13]</sup>) gains a coroutine execution model beneath it. The protocol complements `std::execution` - each serves the domain where its design choices pay off. Bridge papers ([P4092R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r0.pdf)<sup>[16]</sup>, [P4093R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r2.pdf)<sup>[15]</sup>) connect them, and a single operation type can satisfy both protocols (Section 7).

Without a standard protocol, each library continues to invent its own execution model. Tasks from one framework do not compose with executors from another. The higher layers of the abstraction tower - HTTP frameworks, database drivers, RPC stacks that interoperate across vendors - remain blocked on a foundation that is not shared.

This paper asks LEWG to advance the _IoAwaitable_ protocol.

---

## 9. Suggested Straw Poll

**Poll.** The _IoAwaitable_ protocol is the minimum vocabulary for coroutines that need executor affinity, a stop token, and a frame allocator.

---

## Acknowledgements

**Gor Nishanov** - The C++20 coroutines language feature is the foundation every word
of this paper rests on. Without the coroutines TS, the _IoAwaitable_ protocol has nothing
to build on.

**Christopher Kohlhoff** - The `execution_context`, executor, and service model in
Section 4 derives directly from Boost.Asio. The design choices in this paper are
possible because Kohlhoff built them first and proved them in production.

**Eric Niebler, Bryce Adelstein Lelbach, Micha&lstrok; Dominiak, Lewis Baker, Lee Howes,
Kirk Shoop, Jeff Garland, Georgy Evtushenko, and Lucian Radu Teodorescu** - The authors
of P2300R10. The structured concurrency guarantees, completion channel model, and
scheduler design in `std::execution` defined the async vocabulary this paper
complements. The bridge papers in the Network Endeavor exist because P2300 is in the
standard.

**Lewis Baker** - The symmetric transfer technique, documented in the published
[blog post](https://lewissbaker.github.io/2020/05/11/understanding_symmetric_transfer),
is the mechanism that makes the zero-overhead coroutine resumption path in Section 4.3
possible.

---

## References

[1] [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf) - "Design: IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[2] [Capy](https://github.com/cppalliance/capy/tree/de7c94834d640497392530b494fa4b1f74b84e4e) - _IoAwaitable_ protocol implementation (Vinnie Falco, Steve Gerbino).

[3] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O library (Vinnie Falco, Steve Gerbino).

[4] [Compiler Explorer](https://godbolt.org/z/Wzrb7McrT) - Self-contained _IoAwaitable_ demonstration.

[5] [P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf) - "The Network Endeavor: Coroutine-Native I/O for C++29" (Vinnie Falco et al., 2026).

[6] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Dominiak, Baker, Evtushenko, Teodorescu, Howes, Shoop, Garland, Niebler, Lelbach, 2024).

[7] [P4035R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4035r0.pdf) - "Support: The Need for Escape Hatches" (Vinnie Falco, 2026).

[8] [Optimizing Away C++ Virtual Functions May Be Pointless](https://www.youtube.com/watch?v=i5MAXAxp_Tw) - CppCon 2023 (Shachar Shemesh).

[9] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - Asynchronous I/O library (Christopher Kohlhoff).

[10] [P4127R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4127r0.pdf) - "Info: The Coroutine Frame Allocator Timing Problem" (Vinnie Falco, 2026).

[11] [P4090R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4090r0.pdf) - "Info: Sender I/O: A Constructed Comparison" (Vinnie Falco, Steve Gerbino, 2026).

[12] [P4091R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4091r0.pdf) - "Info: Error Models of Regular C++ and the Sender Sub-Language" (Vinnie Falco, 2026).

[13] [P3482R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3482r1.html) - "Design for C++ networking based on IETF TAPS" (Thomas Rodgers, Dietmar K&uuml;hl, 2024).

[14] [P3164R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3164r4.html) - "Early Diagnostics for Sender Expressions" (Eric Niebler, 2025).

[15] [P4093R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r2.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[16] [P4092R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r0.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).
