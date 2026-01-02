# Affine Awaitable Protocol (Specification)

Minimal, library-agnostic requirements for propagating scheduler affinity through coroutine `co_await` chains.

## 1. Dispatcher

- A dispatcher is any callable object `D` such that:
  - For some promise type `P` (default `void`), `D(h)` is valid where `h` is `std::coroutine_handle<P>`.
  - Calling `D(h)` eventually resumes `h` (typically by scheduling it on a specific execution context).
- **Lifetime:** In `await_suspend`, the dispatcher is received by lvalue reference. The callee treats it as *borrowed for the duration of the await* (do not retain past completion). Ownership and lifetime are the caller’s responsibility. The caller may store the dispatcher by value (if owning) or by pointer/reference (if externally owned) but must present it to callees as an lvalue reference.

## 2. Awaitable Requirements (callee role)

An awaitable **participates in the affinity protocol** if it provides an overload:

```cpp
template<class Dispatcher>
auto await_suspend(std::coroutine_handle<> h, Dispatcher& d);
```

Semantics:
- The awaitable must use the dispatcher `d` to resume the caller, e.g. `d(h);`.
- It may run its own work on any context; only resumption must use `d`.

## 3. Task/Promise Requirements (caller role)

A task type (its promise) **propagates affinity** if it:

1) **Stores the caller’s dispatcher.**  
   - Provides a way to set/hold a dispatcher instance for the lifetime of the promise.

2) **Forwards the dispatcher on every await.**  
   - In `await_transform`, when awaiting `A`, pass the stored dispatcher to the awaited object via an affine awaiter:
     ```cpp
     // dispatcher_handle: whatever you store for the caller's dispatcher (pointer or reference)
     return affine_awaiter{std::forward<Awaitable>(a), dispatcher_handle};
     ```
   - The callee receives it as `Dispatcher&` in `await_suspend(h, d)`.
   - If `A` is not affine and you still want affinity, wrap it (e.g. `make_affine(A, dispatcher)`) or reject it (strict mode).

3) **Provides both await paths for its own awaitability.**  
   - `await_suspend(caller)` (legacy, no dispatcher available).
   - `await_suspend(caller, dispatcher)` (affine, dispatcher available) that stores dispatcher + continuation before resuming the task’s coroutine.

   In the affine path, `await_suspend(caller, d)` typically:
   - Stores the continuation handle (caller) and the dispatcher `d` in the promise, then
   - Returns the task’s coroutine handle to start execution, enabling later forwarding (via `await_transform`) and final resumption via the stored dispatcher.

4) **Final resumption uses the dispatcher when set.**  
   - In `final_suspend`, if a dispatcher is stored, resume the continuation via that dispatcher; otherwise use direct symmetric transfer.

## 4. Propagation Rule

- The dispatcher is set once at the top-level task (e.g., `run_on(ex, task)`).
- Each `co_await` forwards the same dispatcher to the awaited object.
- Any awaited object that implements `await_suspend(h, d)` uses that dispatcher to resume its caller, preserving affinity through arbitrary nesting.
- If an awaited object is non-affine and not adapted, affinity may be lost at that point. A trampoline (e.g., `make_affine`) can restore it at the cost of one allocation per await; strict mode instead rejects non-affine awaits.

## 5. Notes

- The helper types in `affine.hpp` (`affine_promise`, `affine_task`, `affine_awaiter`, `make_affine`) are convenience implementations of this protocol. They are not the protocol itself.
- Zero-allocation across the chain requires awaited objects to be affine (or adapted with a zero-alloc awaiter). Trampoline fallback preserves affinity but allocates once per `co_await`.
