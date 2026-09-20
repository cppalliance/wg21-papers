---
title: "A Universal Continuation Model"
document: P4126R2
date: 2026-05-01
intent: info
audience: EWG, SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
  - "Klemens Morgenstern <klemens.d.morgenstern@gmail.com>"
  - "C++ Alliance Proposal Team"
---

## Abstract

Senders pay a frame allocation to enter the awaitable protocol. They do not have to.

The IoAwaitable protocol ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[1]</sup>) defines a contract between a coroutine and an I/O reactor: The coroutine suspends, the reactor performs the operation, and the executor resumes the coroutine when the result is ready. The only way to obtain a `coroutine_handle<>` today is from a coroutine, and a coroutine requires a frame allocation. A sender pipeline that wants to invoke an IoAwaitable must allocate a coroutine frame to get a handle - even though the sender already has its own operation state and does not need a frame.

This paper is additive. It does not take anything away from senders, from coroutines, or from any existing design. It gives senders something they do not have today: zero-allocation access to every IoAwaitable ever written - timers, channels, semaphores, I/O operations, and anything else the ecosystem produces. A general bridge to standard awaitables would also need to handle the `void`-returning and `bool`-returning variants of `await_suspend`. It gives awaitable authors a new consumer base without modifying a single line of their code.

This paper traces the history of alternative coroutine designs that explored the boundary between type erasure and type visibility, observes that C++ can support multiple coroutine models serving different domains, and explores language-level options to let senders invoke awaitables without allocating a coroutine frame. The goal is one I/O implementation consumed by both coroutines and senders with zero allocation overhead.

---

## Revision History

### R1: May 2026 (pre-Brno mailing)

- Formatting corrections.

### R0: April 2026 (post-Croydon mailing)

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

This paper is part of the [Network Endeavor](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf) ([P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf)<sup>[2]</sup>), a project to bring coroutine-native I/O to C++.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[3]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[4]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

This paper examines the published record. That effort requires re-examining consequential papers, including papers written by people the author respects.

This paper seeks input from EWG, SG1, LEWG, and the sender/receiver community. The ideas are presented for discussion, not as a finished proposal. The author invites collaboration from compiler implementers, language designers, and anyone who has thought about the boundary between coroutines and senders.

This paper asks for nothing.

---

## 2. The Goal

One I/O implementation. Both coroutines and senders consume it. Zero allocation for either path.

### 2.1 The Executor

The coroutine executor ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[1]</sup>) has two operations:

```cpp
coroutine_handle<>
dispatch(coroutine_handle<> h) const;

void post(coroutine_handle<> h) const;
```

`post` schedules a handle for later resumption on the execution context. `dispatch` may resume the handle inline - it returns a `coroutine_handle<>` that the caller's `await_suspend` returns to the compiler for symmetric transfer. If `dispatch` defers, it returns `noop_coroutine()`.

The reactor does not call `h.resume()` directly. When an I/O operation completes, the reactor calls the executor - either `executor.dispatch(h)` or `executor.post(h)`. The executor is the policy point that determines how and where the handle resumes.

### 2.2 The Awaitable

Consider `read_some`, the canonical IoAwaitable:

```cpp
struct read_some_awaitable {
    stream& s_;
    mutable_buffer buf_;
    io_result<size_t> result_;

    bool await_ready() noexcept
    {
        return false;
    }

    coroutine_handle<>
    await_suspend(
        coroutine_handle<> h,
        io_env const* env) noexcept
    {
        s_.impl_->async_read(
            buf_, h, env);
        return noop_coroutine();
    }

    io_result<size_t>
    await_resume() noexcept
    {
        return result_;
    }
};
```

A coroutine user writes:

```cpp
auto [ec, n] = co_await stream.read_some(buf);
```

The compiler provides the handle. When the I/O completes, the reactor calls the executor, and the executor resumes the coroutine. Zero user effort.

A sender pipeline wants to do the same thing - pass a handle to `await_suspend`, have the executor resume it when the I/O completes. The sender is not a coroutine. It has a receiver. It has operation state. It does not have a frame. It needs a `coroutine_handle<>` that, when the executor calls `.resume()`, invokes a function on the sender's own state.

The handle is the only thing the executor sees. It calls `.resume()`. It does not know or care whether the handle points at a coroutine frame or a callback.

---

## 3. The Problem

The only way to obtain a `coroutine_handle<>` today is from a coroutine. A coroutine requires a frame allocation. The awaitable-to-sender bridge in [P4093R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r0.pdf)<sup>[5]</sup> demonstrates this: The bridge creates a coroutine whose sole purpose is to hold a handle that the reactor can resume. The coroutine frame is the tax.

[P4093R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r0.pdf)<sup>[5]</sup> Appendix A shows the bridge implementation. The `bridge_task` coroutine exists to produce a `coroutine_handle<>`. The coroutine body calls `co_await` on the IoAwaitable, and the `await_suspend` receives the handle from the compiler. The bridge works. It allocates a coroutine frame per I/O operation.

For a coroutine user, the frame allocation is the cost of doing business - the frame holds the coroutine's local variables, its suspension-point state, and its promise. The frame earns its allocation. For a sender pipeline, the frame holds nothing the sender needs. The sender already has its own operation state. The frame is overhead.

One allocation per I/O operation. For high-throughput networking - millions of operations per second - that matters.

---

## 4. The Shape of an I/O Operation

An I/O operation can take one of two shapes: a sender or an awaitable. The choice determines which consumption model pays a tax and which runs at zero cost.

**If the I/O operation is a sender,** coroutines consume it through `co_await` on the sender. The sender's `connect` produces an operation state. The coroutine must store that operation state somewhere - typically in the coroutine frame or in a bridge object. The sender's completion calls `set_value` on a receiver, which must resume the coroutine. The machinery to connect a sender to a coroutine - `execution::task`, or a bridge like the one in [P4093R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r0.pdf)<sup>[5]</sup> - is the tax coroutines pay. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[6]</sup>, "Add a Coroutine Task Type," is this tax made standard: It type-erases the operation state, allocates, and converts an `error_code` to `exception_ptr` through the execution framework's error-conversion machinery ([P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[7]</sup>).

**If the I/O operation is an awaitable,** coroutines consume it directly. `co_await stream.read_some(buf)` is the language feature working as designed. The compiler provides the handle. The awaitable suspends the coroutine. The reactor completes the operation. The executor resumes the coroutine. No bridge. No type erasure. No allocation beyond the coroutine frame that the coroutine already needs for its own state.

The asymmetry is structural. Coroutines are a language feature. Awaitables are the native protocol of that language feature. A coroutine consuming an awaitable is zero-cost by construction. A coroutine consuming a sender requires a bridge - and every bridge has a cost.

The question is whether senders can consume an awaitable at zero cost. Today they cannot - they need a coroutine frame to get a handle. This paper proposes to eliminate that cost. If a callback handle exists, senders consume awaitables at zero cost too.

The awaitable is the right shape for an I/O operation because it is the shape that makes the language feature free, and this paper makes it free for senders as well.

---

## 5. The Timeline

The tension between "frame hidden from the caller" and "frame visible to the caller" has been present since the earliest coroutine proposals. This section traces the published record so the reader can follow the trail.

| Year | Paper                                                             | Author(s)                          | Design                                                                                  |
| ---- | ----------------------------------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------- |
| 2015 | [N4453](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4453.pdf)<sup>[8]</sup>                   | Kohlhoff                           | Resumable Expressions. Single `resumable` keyword, "suspend down."                      |
| 2015 | [P0114R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0114r0.pdf)<sup>[9]</sup>               | Kohlhoff                           | Resumable Expressions (revised).                                                        |
| 2015 | [P0158R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0158r0.html)<sup>[10]</sup>               | Allsop et al.                      | Coroutines belong in a TS. Argued for more time.                                        |
| 2018 | [P0057R8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0057r8.pdf)<sup>[11]</sup>               | Nishanov                           | Coroutines TS. Frame-erased. The design that shipped.                                   |
| 2018 | [P0973R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0973r0.pdf)<sup>[12]</sup>              | Romer, Dennett                     | Coroutines TS Use Cases and Design Issues. Critique: implicit allocation, hidden frame.  |
| 2018 | [P1063R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1063r0.pdf)<sup>[13]</sup>              | Romer, Dennett, Carruth            | Core Coroutines. Frame-visible alternative. Expose minimal primitives.                   |
| 2018 | [P1134R0](https://vinniefalco.github.io/papers/drafts/d1134r0.html)<sup>[14]</sup> | Falco                   | An Elegant Coroutine Abstraction. Library-only stackless coroutines.                     |
| 2018 | [P1342R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1342r0.pdf)<sup>[15]</sup>              | Baker                              | Unifying Coroutines TS and Core Coroutines. Attempted compromise.                        |
| 2018 | [P1362R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1362r0.pdf)<sup>[16]</sup>              | Nishanov                           | Incremental Approach: Coroutine TS + Core Coroutines.                                    |
| 2019 | [P1492R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1492r0.pdf)<sup>[17]</sup>              | Smith, Vandevoorde et al.          | Language and implementation impact of coroutine proposals.                                |
| 2019 | [P1493R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1493r0.pdf)<sup>[18]</sup>              | Romer, Nishanov, Baker, Mihailov   | Coroutines: Use-cases and Trade-offs.                                                    |
| 2019 | [P0912R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0912r5.html)<sup>[19]</sup>              | Nishanov                           | Merge Coroutines TS into C++20. The frame-erased model ships.                            |
| 2024 | [P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup>              | Morgenstern                        | Implementation defined coroutine extensions. Legalizes `coroutine_handle` specialization. |
| 2026 | [P0876R22](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p0876r22.pdf)<sup>[21]</sup>            | Kowalke, Goodspeed                 | `fiber_context`. Stackful coroutines. Complementary, not competing.                      |

The committee explored both frame-erased and frame-visible designs. It chose frame-erased. That was the right choice for I/O - type erasure through `coroutine_handle<>` gives type-erased streams, split compilation, and ABI stability. The I/O library compiles once.

Senders need frame visibility. The sender pipeline owns its operation state, knows its size at compile time, and inlines it. A coroutine frame that the sender cannot see, cannot size, and cannot place is a foreign object in the sender's world.

The two needs are not in conflict.

---

## 6. Three Kinds of Coroutines

C++ has shipped multiple models for parallel execution (`std::execution_policy` and [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[7]</sup> senders with `bulk`), multiple models for formatted output (`iostream` and `std::format`), and multiple models for error handling (exceptions and `error_code`). Multiple coroutine models serving different domains is consistent with the committee's practice. Unlike `iostream` and `std::format`, which overlap significantly, the three coroutine models serve non-overlapping domains: Stackful coroutines serve deep suspension through coroutine-unaware APIs, frame-erased coroutines serve type-erased I/O with split compilation and ABI stability, and frame-visible coroutines (if they ever exist) serve compile-time work graphs that need the frame in the type system. Each addresses a use case the others structurally cannot.

### 6.1 Stackful (fibers)

[P0876R22](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p0876r22.pdf)<sup>[21]</sup> (Kowalke) proposes `fiber_context` - stackful coroutines that maintain a separate stack and support deep suspension. Stackful coroutines address a different set of use cases than stackless coroutines: interacting with coroutine-unaware APIs, deep call chains that suspend at arbitrary depth, and integration with legacy code. The committee has been working on this for over a decade. It is complementary, not competing.

### 6.2 Stackless, frame-erased (C++20 coroutines)

C++20 coroutines type-erase the frame through `coroutine_handle<>`. The promise type is invisible to the caller. The caller sees only a handle. This is ideal for I/O: Type erasure gives type-erased streams, split compilation, and ABI stability. The I/O library compiles once. Transport changes do not break the ABI.

`std::execution` ([P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[7]</sup>) provides compile-time sender composition, structured concurrency guarantees, and a customization point model that enables heterogeneous dispatch. These are real achievements. The sender model serves GPU dispatch, parallel algorithms, and infrastructure well.

### 6.3 Stackless, frame-visible

Senders want to see everything in the type system. The frame is part of the operation state. The sender pipeline owns the frame, knows its size, and can inline it.

Romer, Dennett, and Carruth identified this need in [P1063R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1063r0.pdf)<sup>[13]</sup>, "Core Coroutines." Their proposal sought to expose minimal coroutine primitives that map directly to the underlying implementation, giving the caller direct access to the coroutine frame in the C++ type system. Baker attempted to unify the two models in [P1342R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1342r0.pdf)<sup>[15]</sup>.

If C++ had frame-visible stackless coroutines, senders could invoke IoAwaitables by constructing the frame inline in their operation state. No allocation. The frame is part of the sender's storage.

This is a large language change. This paper names it as the deeper solution and invites exploration. The pragmatic solution follows.

---

## 7. The Pragmatic Solution: Callback Handles

Even without frame-visible coroutines, the immediate problem is solvable.

What a sender needs is a `coroutine_handle<>` that, when `.resume()` is called, invokes a function on the sender's operation state. The minimum viable representation is two pointers: a function pointer and a data pointer. In practice, three - the coroutine frame ABI requires both a `resume` and a `destroy` function pointer at offsets 0 and 1, plus the data pointer. No frame. No promise. No suspension points. No heap allocation. When the executor calls `.resume()`, it calls the function with the data pointer. When `.destroy()` is called, it is a no-op - the sender owns its own lifetime.

### 7.1 Symmetric Transfer

The coroutine executor's `dispatch` returns a `coroutine_handle<>` to enable symmetric transfer - the compiler tail-calls the returned handle, avoiding stack buildup in coroutine chains. A sender pipeline is not a coroutine. It does not have an `await_suspend` that the compiler can tail-call out of. Symmetric transfer is a coroutine mechanism that senders do not need.

The sender provides an executor that maps `dispatch` to `post`:

```cpp
struct sender_executor {
    underlying_executor exec_;

    void post(coroutine_handle<> h) const
    {
        exec_.post(h);
    }

    coroutine_handle<>
    dispatch(coroutine_handle<> h) const
    {
        exec_.post(h);
        return noop_coroutine();
    }
};
```

When the reactor completes an I/O operation and calls `executor.dispatch(h)`, the sender's executor posts the handle for later resumption and returns `noop_coroutine()`. The callback handle is resumed from the event loop. No symmetric transfer. No stack buildup. The executor is the policy point - a sender-provided executor that collapses `dispatch` to `post` is a policy choice, not a limitation.

### 7.2 The Sender Path

A sender pipeline would use a callback handle like this. The following code works on all three major compilers today but relies on the de facto coroutine frame ABI documented by [P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup> - it is not guaranteed by the current standard. Sections 8 and 9 discuss the standardisation path.

```cpp
struct callback_frame {
    void (*resume)(callback_frame*);
    void (*destroy)(callback_frame*);
    void* data;
};

template<class Receiver>
struct read_op_state {
    stream& s_;
    mutable_buffer buf_;
    Receiver rcvr_;
    read_some_awaitable aw_;
    io_env env_;
    callback_frame cb_;

    static void on_resume(
        callback_frame* p) noexcept
    {
        auto* self = static_cast<
            read_op_state*>(p->data);
        auto result =
            self->aw_.await_resume();
        set_value(
            std::move(self->rcvr_),
            result);
    }

    void start() noexcept
    {
        if (aw_.await_ready()) {
            set_value(
                std::move(rcvr_),
                aw_.await_resume());
            return;
        }

        cb_.resume = &on_resume;
        cb_.destroy =
            +[](callback_frame*) {};
        cb_.data = this;

        auto h =
            coroutine_handle<>::from_address(
                &cb_);
        aw_.await_suspend(h, &env_).resume();
    }
};
```

The `callback_frame` struct has `resume` and `destroy` function pointers at offsets 0 and 1 - matching the coroutine frame layout that all three major compilers use. `coroutine_handle<>::from_address(&cb_)` produces a handle whose `.resume()` calls the function pointer at offset 0. The awaitable cannot tell the difference between this handle and one from a real coroutine.

The `await_ready` check is a no-op for `read_some_awaitable` (which always returns `false`). Calling `.resume()` on the `coroutine_handle<>` returned by `await_suspend` handles both completion paths: `noop_coroutine().resume()` is a no-op for asynchronous completion, and a real handle's `.resume()` invokes the callback for synchronous completion. IoAwaitable's `await_suspend` returns `coroutine_handle<>`; a general sender-to-awaitable bridge for standard awaitables would also need to handle the `void`-returning and `bool`-returning variants of `await_suspend`.

The `io_env` carries the sender's executor. The awaitable submits the operation to the reactor. The reactor calls the executor. The executor calls `.resume()` on the callback handle. The sender's completion function runs. No coroutine frame was allocated.

---

## 8. Prior Art: P3203R0

[P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup> (Morgenstern, 2024), "Implementation defined coroutine extensions," was presented at Sofia (June 2025) by Niall Douglas on behalf of the author. The paper proposes changing the standard's prohibition on specializing `coroutine_handle` from undefined behavior to implementation defined behavior. The EWG poll to forward the paper was not consensus (SF 0 / F 9 / N 8 / A 2 / SA 1). Committee feedback indicated the paper needed a more complete design with constraints on specialisations, and that the change from undefined to implementation-defined may have no practical effect on implementations. The interest - nine in favour - suggests the use case resonates; the concerns point to the design space this paper explores.

[P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup> documents that all three major compilers (MSVC, GCC, Clang) use the same coroutine frame layout:

```cpp
struct coroutine_frame {
    void (*resume)(coroutine_frame*);
    void (*destroy)(coroutine_frame*);
    promise_type promise;
};
```

The `.resume()` member function of `coroutine_handle<>` calls the function pointer at offset 0. A user-provided struct with the same two-pointer prefix works on every compiler today.

[P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup> identifies the same use case this paper describes: allowing non-coroutine code to provide a `coroutine_handle` that participates in the awaitable protocol. Morgenstern demonstrates this in Boost.Cobalt for Python bindings and stackful coroutine integration.

The wording change in [P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup> is the legal prerequisite for the callback handle approach described in Section 9.

---

## 9. The Design

The approach requires no `coroutine_handle` specialization, no factory function, and no compiler-generated frame. The user defines a struct whose first two members match the coroutine frame prefix, and `coroutine_handle<>::from_address` does the rest.

### 9.1 The Callback Frame

The user defines a struct with `resume` and `destroy` function pointers at offsets 0 and 1:

```cpp
struct callback_frame {
    void (*resume)(callback_frame*);
    void (*destroy)(callback_frame*);
    void* data;
};
```

The struct's first two members match the coroutine frame layout documented by [P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup>. `coroutine_handle<>::from_address(&cb)` produces a `coroutine_handle<>` that, when `.resume()` is called, calls the function pointer at offset 0. The awaitable receives this handle. It cannot tell the difference between this handle and one from a real coroutine.

The `destroy` pointer is a no-op - the sender owns its own lifetime. If a component calls `destroy()` on the callback handle - for example, during shutdown - the no-op means the sender's operation completes without calling `set_value` or `set_stopped`. In the IoAwaitable protocol, the reactor and executor call only `resume()`, never `destroy()`. If cancellation support is needed, the `destroy` pointer can map to a function that calls `set_stopped` on the receiver. The `data` pointer points back to the operation state. Three pointers. Twenty-four bytes on a 64-bit platform. No heap allocation.

### 9.2 The Type-Erasure Constraint

Any callback handle must be convertible to `coroutine_handle<void>`. This is non-negotiable. Awaitables accept `coroutine_handle<>`. Executors traffic in `coroutine_handle<>`. The handle is the type-erased boundary between the awaitable and its consumer.

A `coroutine_handle<>` is a pointer to a frame. The storage for that frame must come from somewhere. A factory function cannot conjure storage without allocating - and allocation is the cost this paper eliminates. The compiler cannot rewrite the user's struct into something else. The only zero-allocation path is: The user provides the storage, and `coroutine_handle<>` points directly at it.

This means the standard would need to mandate the two-pointer prefix layout - `resume` and `destroy` function pointers at offsets 0 and 1 - so that `from_address` on a user-provided struct produces a valid handle. There is no alternative design that avoids allocation without this guarantee.

### 9.3 What the Standard Would Need

[P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup> formalizes what all three major compilers already do. The coroutine frame layout with two function pointers at the front is not an implementation accident - it is the layout every compiler chose independently, and it is the layout that makes `coroutine_handle<>::from_address` work. The question is whether the committee will mandate it.

The standard could also provide convenience wrappers on top of the mandated layout - a standard `callback_frame` type, a factory function that fills in the pointers, or a named concept that constrains the prefix. These are API sugar. The layout mandate is the prerequisite. Without it, none of them can produce a zero-allocation `coroutine_handle<>` from user-owned storage.

---

## 10. What This Enables

A callback handle gives senders a zero-allocation entry into the awaitable protocol. The consequences go beyond I/O.

- **The entire awaitable ecosystem opens to senders.** Every IoAwaitable anyone has written - timers, mutexes, channels, semaphores, file I/O, database queries, HTTP clients - becomes consumable by sender pipelines at zero allocation cost. Awaitable authors change nothing. Sender authors gain a new universe of composable operations. The sender ecosystem and the awaitable ecosystem merge.

- **One I/O implementation.** The I/O library implements each operation once as an IoAwaitable. Coroutine users `co_await` it. Sender users invoke `await_suspend` with a callback handle. Both go through the same reactor, the same executor, the same platform implementation.

- **Zero-allocation bridge.** The awaitable-to-sender bridge in [P4093R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r0.pdf)<sup>[5]</sup> currently allocates a coroutine frame. With a callback handle, the bridge is three pointers.

- **Type-erased streams.** Streams are type-erasable because the executor is type-erased and the handle is type-erased. Both coroutines and senders see the same stream type.

- **Split compilation.** The I/O library compiles once. It does not need to know whether its caller is a coroutine or a sender pipeline.

- **ABI stability.** Transport changes do not break the ABI. The handle is the boundary.

The I/O library does not need two APIs - one for coroutines and one for senders. It needs one API and two ways to produce a handle.

---

## 11. Anticipated Objections

**Q: This breaks the coroutine abstraction.**

A: The reactor already treats the handle as opaque. It calls `.resume()`. It does not inspect the frame, access the promise, or query the suspension point. A callback handle is a `coroutine_handle<>` that does less, not more.

**Q: Senders should use their own I/O protocol.**

A: They can. This gives them a zero-cost entry into the awaitable protocol when they need I/O. Two protocols for the same socket operation means two implementations to maintain, two sets of bugs, and two surfaces to audit.

**Q: Just use a coroutine.**

A: That is one allocation per I/O operation. For high-throughput networking - millions of operations per second - that matters. The sender pipeline already has operation state. Allocating a frame to hold nothing the sender needs is overhead.

**Q: Frame-visible coroutines are too ambitious.**

A: Section 6.3 names frame-visible coroutines as the deeper solution. Section 7 presents the pragmatic fallback. A callback handle solves the immediate problem without a large language change.

**Q: C++ should have only one kind of coroutine.**

A: C++ has multiple models for parallel execution, formatted output, and error handling. Multiple coroutine models serving different domains is consistent with the committee's practice.

---

## Acknowledgments

The author thanks Gor Nishanov for the C++20 coroutine model and its explicit support for task type diversity; Christopher Kohlhoff for the original continuation framing in [P0113R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0113r0.html)<sup>[22]</sup> and for Resumable Expressions, which explored the boundary between type erasure and type visibility before most of the committee was thinking about it; Geoff Romer, James Dennett, and Chandler Carruth for [P1063R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1063r0.pdf)<sup>[13]</sup>, which identified the frame-visibility need with precision; Lewis Baker for [P1342R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1342r0.pdf)<sup>[15]</sup>, which attempted to unify the two models; Klemens Morgenstern for [P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup>, which removes the legal barrier and documents the ABI reality; Niall Douglas for presenting [P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html)<sup>[20]</sup> at Sofia; Oliver Kowalke and Nat Goodspeed for a decade of work on stackful coroutines; and Steve Gerbino and Mungo Gill for [Capy](https://github.com/cppalliance/capy)<sup>[3]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[4]</sup> implementation work.

---

## References

[1] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[2] [P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf) - "The Network Endeavor: Coroutine-Native I/O for C++29" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[3] [cppalliance/capy](https://github.com/cppalliance/capy) - Coroutine I/O primitives library.

[4] [cppalliance/corosio](https://github.com/cppalliance/corosio) - Coroutine-native networking library.

[5] [P4093R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r0.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[6] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[7] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Lewis Baker, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[8] [N4453](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4453.pdf) - "Resumable Expressions" (Christopher Kohlhoff, 2015).

[9] [P0114R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0114r0.pdf) - "Resumable Expressions" (Christopher Kohlhoff, 2015).

[10] [P0158R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0158r0.html) - "Coroutines belong in a TS" (Jamie Allsop, Jonathan Wakely, Christopher Kohlhoff, Anthony Williams, Roger Orr, Andy Sawyer, Jonathan Coe, Arash Partow, 2015).

[11] [P0057R8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0057r8.pdf) - "Working Draft, C++ Extensions for Coroutines" (Gor Nishanov, 2018).

[12] [P0973R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0973r0.pdf) - "Coroutines TS Use Cases and Design Issues" (Geoff Romer, James Dennett, 2018).

[13] [P1063R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1063r0.pdf) - "Core Coroutines" (Geoff Romer, James Dennett, Chandler Carruth, 2018).

[14] [P1134R0](https://vinniefalco.github.io/papers/drafts/d1134r0.html) - "An Elegant Coroutine Abstraction" (Vinnie Falco, 2018).

[15] [P1342R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1342r0.pdf) - "Unifying Coroutines TS and Core Coroutines" (Lewis Baker, 2018).

[16] [P1362R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1362r0.pdf) - "Incremental Approach: Coroutine TS + Core Coroutines" (Gor Nishanov, 2018).

[17] [P1492R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1492r0.pdf) - "Language and implementation impact of coroutine proposals" (Richard Smith, Daveed Vandevoorde et al., 2019).

[18] [P1493R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1493r0.pdf) - "Coroutines: Use-cases and Trade-offs" (Geoffrey Romer, Gor Nishanov, Lewis Baker, Mihail Mihailov, 2019).

[19] [P0912R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0912r5.html) - "Merge Coroutines TS into C++20 working draft" (Gor Nishanov, 2019).

[20] [P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html) - "Implementation defined coroutine extensions" (Klemens Morgenstern, 2024).

[21] [P0876R22](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p0876r22.pdf) - "fiber_context - fibers without scheduler" (Oliver Kowalke, Nat Goodspeed, 2026).

[22] [P0113R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0113r0.html) - "Executors and Asynchronous Operations, Revision 2" (Christopher Kohlhoff, 2015).
