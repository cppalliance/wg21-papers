---
title: "IoAwaitables for GPU Data Movement: Convergent Findings"
document: P4251R0
date: 2026-07-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

A protocol handler compiled once writes to a TCP socket or to GPU device memory without recompilation.

C++ has a standard model for asynchronous execution in `std::execution`, validated in GPU kernel dispatch and heterogeneous scheduling. The byte-oriented data movement that feeds those kernels - host-device memcpy, inter-GPU collectives over NVLink, RDMA transfers between nodes, and TCP sockets - has no standard interface. These four transports share a common async completion model, and the IoAwaitable protocol captures it with an ABI-stable, type-erased interface. Independent projects at NVIDIA Labs, the University of Wisconsin-Madison, and Schr&ouml;dinger converged on the same coroutine-based async completion pattern for GPU data movement without coordination, and CERN ported a GPU track-reconstruction pipeline onto the IoAwaitable protocol directly. Bidirectional bridges connect IoAwaitables and senders where byte-oriented I/O meets GPU dispatch, so each model serves its natural domain.

---

## Revision History

### R0: July 2026 (post-Brno mailing)

- Initial revision.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup>, coroutine-native I/O libraries under the C++ Alliance.

This paper examines how C++20 coroutines integrate with CUDA's async completion model for byte-oriented data movement and places the findings in the record for evaluation by domain experts.

The author has a stake in the coroutine model's adoption. The competing model, `std::execution`, is in the C++26 working draft, while the IoAwaitable protocol is proposed but not standardized.

The author is a networking domain expert, not a GPU domain expert, and each coroutine suspension potentially allocates a frame. Both limitations are examined in the body (Sections 17 and 19).

Companion papers: [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup> specifies the protocol this paper examines. P4088R1<sup>[4]</sup>, P4091R1<sup>[5]</sup>, P4092R1<sup>[6]</sup>, P4093R1<sup>[7]</sup>, and P4123R0<sup>[8]</sup> examine adjacent questions.

The CUDA data-movement examples were produced with AI assistance and are presented as a research exercise. A compileable demonstration accompanies the paper.<sup>[9]</sup>

This paper asks for nothing.

## 2. Introduction

`std::execution` gives C++ a composable model for asynchronous execution, validated in GPU kernel dispatch and heterogeneous scheduling (Section 3). The byte-oriented data movement that feeds those kernels - host-device memcpy, collectives, RDMA (Remote Direct Memory Access) transfers, socket reads - has no standard interface, and which async model serves that layer is an open question in the committee's record: [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[10]</sup> defines the sender model and stdexec<sup>[11]</sup> implements it, [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup> proposes the coroutine-based IoAwaitable protocol, and [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf)<sup>[12]</sup> records SG14's position on sender-based networking. This paper examines the GPU corner of that question: how CUDA's async completion model integrates with coroutines for byte-oriented data movement.

The paper reports five findings:

1. Four data-movement APIs that cross four different hardware boundaries - `cudaMemcpyAsync`, NCCL collectives, RDMA verbs, and TCP sockets - fit one abstract interface: submit a buffer, receive an async completion, dispatch a compound result. POSIX and RDMA present the compound result natively. For CUDA and NCCL the wrapper synthesizes it (Sections 4 and 12).
2. The IoAwaitable protocol captures this interface, and the notification mechanism is a free variable: callback, event polling, and deferred synchronization all satisfy it (Section 6). Working `cuda_stream` and `cuda_device_stream` demonstrations accompany the paper (Sections 8-9).
3. Under type erasure, the awaitable form allocates nothing per operation and has a fixed vtable, which yields an ABI-stable stream interface. The sender form heap-allocates per operation (Sections 10-11).
4. Eight independent projects - at NVIDIA Labs, the University of Wisconsin-Madison, Oddity AI, Schr&ouml;dinger, the EPEXA project, and in the RDMA ecosystem - converged on coroutine-based async completion for data movement without coordination, and CERN ported its traccc track-reconstruction pipeline onto the IoAwaitable protocol itself (Section 15).
5. The sender model's strengths - zero-allocation compile-time composition, scheduler portability, structured concurrency for dynamic fan-out - are strongest in kernel dispatch, and bidirectional bridges connect the two domains (Sections 3, 16, and 18).

Related work beyond the papers named above: P4088R1<sup>[4]</sup> analyzes what C++20 coroutines already buy the standard, P4091R1<sup>[5]</sup> the error models of regular C++ and the sender sub-language, P4123R0<sup>[8]</sup> the cost of senders for coroutine I/O, and P4092R1<sup>[6]</sup> and P4093R1<sup>[7]</sup> the two bridge directions between senders and coroutines.

The paper's assumptions: the CUDA examples were produced with AI assistance and are offered for evaluation by domain experts rather than as expert testimony (Section 1); the benchmark figures in Section 10 come from the measurement setup documented in P4088R1<sup>[4]</sup>; and the surveys of sender-based networking (Section 14) and of convergent projects (Section 15) are bounded by the public record their methods searched.

## 3. What std::execution Provides

`std::execution` provides four properties that this paper's findings do not contest.

**Zero-allocation composition.** Sender pipelines collapse into a single `operation_state` at compile time. No heap allocation, no virtual dispatch, no reference counting. This is a real property that coroutines do not match for multi-stage pipelines.<sup>[10]</sup>

**Domain customization.** A scheduler's `transform_sender` can replace `bulk` with a GPU kernel launch transparently. This enables writing algorithm code once and retargeting to CPU or GPU by swapping the scheduler.<sup>[13]</sup>

**Structured concurrency.** `counting_scope` tracks dynamically spawned work and prevents scope destruction until all work completes. Coroutines provide lexical-scope safety via `when_all`, but dynamic fan-out to an unknown number of tasks needs explicit library support.

**Scheduler-agnostic portability.** The Maxwell FDTD (finite-difference time-domain) benchmark in the [stdexec](https://github.com/NVIDIA/stdexec)<sup>[11]</sup> repository demonstrates the same algorithm achieving parity with raw CUDA on GPU and running correctly on a CPU thread pool.

These properties are strongest in GPU dispatch and heterogeneous scheduling, the domains for which `std::execution` was designed.

## 4. Four Transports, One Completion Model

Four APIs that move bytes across different hardware boundaries share a common async completion model:

**CUDA `cudaMemcpyAsync`.**<sup>[14]</sup> Bytes between host and device. Completion via callback, event query, or stream synchronization (Section 6).<sup>[15]</sup>

**NCCL (NVIDIA Collective Communications Library) `ncclAllReduce`.**<sup>[16]</sup> Bytes between GPUs over NVLink or InfiniBand. Completion via CUDA stream synchronization.

**RDMA `ibv_post_send`.**<sup>[17]</sup> Bytes between nodes. Completion via `ibv_comp_channel.fd` - a plain file descriptor that works with epoll, io_uring, or kqueue.

**TCP `read`/`write`.** Bytes between hosts. Completion via IOCP (I/O completion ports) or io_uring, readiness via epoll.

All four share the same structural pattern: submit a buffer of bytes, receive async completion via callback, poll, or file descriptor, receive a compound result (status plus byte count), and dispatch the result to the application thread via a reactor. The hardware boundaries differ - PCIe, NVLink, InfiniBand, Ethernet - and the abstract interface does not. Two of the four report the compound result natively (POSIX, RDMA). For CUDA and NCCL the wrapper synthesizes the byte count (Section 12). IoAwaitable handles all four with the same mechanism. Section 9 demonstrates a protocol handler written against this interface, and Section 11 traces the ABI consequence.

The type vocabulary builds from this pattern:

The `IoAwaitable` concept requires `await_suspend(coroutine_handle<>, io_env const*)` - the execution environment flows into each operation at the suspension point. The concept is defined in [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup>.

The compound result type `io_result<std::size_t>` delivers both status and byte count via structured bindings:

```cpp
auto [ec, n] = co_await stream.write_some(buf);
```

`WriteStream` requires `write_some(buffers)` returning an `IoAwaitable` whose `await_resume` returns `io_result<std::size_t>`, and `WriteSink` refines it with `write(buffers)` for complete-buffer writes and `write_eof()` for graceful shutdown.

The type-erased wrappers `any_write_stream` and `any_write_sink` wrap any `WriteStream` or `WriteSink` (respectively) behind a vtable whose per-operation entries - `await_ready`, `await_suspend`, `await_resume`, and `destroy` - have fixed signatures. The awaitable has a fixed, compile-time-known size, so the wrapper preallocates a single awaitable buffer at construction and reuses it for every operation. Section 10 explains why and analyzes the structural consequences, and Section 11 draws the ABI conclusion.

P2300R10<sup>[10]</sup> Section 4.15 agrees with the user-facing pattern: "we expect that coroutines and awaitables will be how a great many will choose to express their asynchronous code."

One completion model spans all four transports, and the type vocabulary above expresses it. The rest of the paper examines what follows from that fact.

## 5. The IoAwaitable Protocol

The IoAwaitable protocol from [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> extends the standard awaitable with an execution environment designed for I/O operations:

```cpp
template<typename A>
concept IoAwaitable =
    requires(A a, std::coroutine_handle<> h,
             io_env const* env) {
        a.await_suspend(h, env);
    };
```

The `io_env`<sup>[18]</sup> bundles three properties:

```cpp
struct io_env
{
    executor_ref executor;
    std::stop_token stop_token;
    std::pmr::memory_resource* frame_allocator
        = nullptr;
};
```

The `executor_ref`<sup>[19]</sup> is a type-erased executor with `dispatch(continuation&)` returning `coroutine_handle<>` for symmetric transfer<sup>[20]</sup>, and `post(continuation&)` for deferred execution. The `continuation`<sup>[21]</sup> type is a simple intrusive-list node:

```cpp
struct continuation
{
    std::coroutine_handle<> h;
    continuation* next = nullptr;
};
```

The `io_env` flows forward through `co_await` chains via `task`'s<sup>[22]</sup> `await_transform`, which wraps each child awaitable and passes the environment into its `await_suspend`. The critical difference from a hand-rolled awaitable: the awaitable knows which executor to resume on, carries a cancellation token, and has access to the frame allocator.

These three properties - executor affinity, cancellation, and frame allocation control - are the same concerns that `std::execution` addresses through a different mechanism. The IoAwaitable protocol provides them in a form designed for byte-oriented I/O, where type-erased streams and compound results are the natural vocabulary.

The full execution model built on this protocol is specified in [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup>. That paper defines the launch functions that connect coroutine chains to the rest of the program: `run_async` starts a coroutine from regular code (the topmost caller that cannot `co_await`), and `run` switches executor, stop token, or allocator for a subtask from within a coroutine. IoAwaitables are lazy - submission happens in `await_suspend`, not at construction. The two-phase invocation of launch functions ensures the frame allocator is cached before the child coroutine's frame is allocated. P4003R3 also demonstrates a `counting_scope` built from launch function handlers, providing spawn, cancel, and join-before-destruction - the same structured concurrency guarantees that `std::execution`'s `counting_scope` provides, expressed through the IoAwaitable protocol's own primitives.

Whether this forward-propagation model - where the execution environment flows into each awaitable via `await_suspend` - addresses the concerns GPU schedulers have about coroutine integration, and whether a GPU-aware awaitable needs properties beyond these three, are open questions the record does not yet settle. This paper places the model before domain experts for that evaluation.

## 6. GPU Completion Notification: Three Mechanisms, One Protocol

CUDA streams are in-order queues where operations execute sequentially.<sup>[23]</sup> When GPU work completes, the host needs notification. Three mechanisms exist, and the IoAwaitable protocol is independent of which one a given awaitable uses:

- **Event polling**: a service thread loops `cudaEventQuery` on a recorded event.<sup>[24]</sup> Costs a spinning thread, but stays stable as the number of worker threads grows.
- **Deferred synchronization**: a service thread runs the blocking `cudaStreamSynchronize`.<sup>[25]</sup> Costs one parked thread per outstanding wait, but keeps the worker threads free.
- **Callback**: `cudaLaunchHostFunc` enqueues a host function into the stream.<sup>[15]</sup> No busy-wait and the simplest to wire up, but a single CUDA-internal worker may service every callback across all streams, so it scales poorly as the number of worker threads grows.

`cudaLaunchHostFunc` is the recommended replacement for `cudaStreamAddCallback`, which is slated for deprecation.<sup>[23]</sup> Its host function fires on a dedicated internal CPU thread created by the CUDA driver, not the application thread.<sup>[26]</sup><sup>[27]</sup> It cannot call CUDA APIs and must not create transitive dependencies on outstanding CUDA work.

Among the three, the choice is a scaling tradeoff. All three satisfy `IoAwaitable` and, driving the same GPU pipeline, produce identical results at runtime, which the accompanying notification-strategies example<sup>[9]</sup> demonstrates directly. The slides of a CHEP (Computing in High Energy and Nuclear Physics) 2026 contribution on trigger scheduling<sup>[28]</sup> report that callback-based handlers scale poorly for multi-threaded jobs, while event polling and deferred synchronization are viable alternatives. In a multi-threaded framework, prefer polling or deferred synchronization. Use the callback for its simplicity in low-concurrency settings.

This is the same structural pattern as epoll readiness events or IOCP and io_uring completions arriving on arbitrary threads. In all cases, an async operation completes on a thread that is not the application's, and the application must dispatch the result to the correct execution context. This is the exact problem that Capy's executor-affinity dispatch was designed to solve.

Each mechanism is a distinct `await_suspend` over the same protocol. The excerpts below are from the accompanying notification-strategies example,<sup>[9]</sup> which compiles and runs. Trimmed to the suspension point, the three awaitables differ only in how they arrange for the continuation to be posted back through `env->executor`:

```cpp
// Callback: a CUDA host function re-posts through the executor.
std::coroutine_handle<>
callback_awaitable::await_suspend(
    std::coroutine_handle<> h, io_env const* env)
{
    cont_.h = h;
    ctx_ = resume_ctx{env->executor, &cont_, &ec_};
    if (cudaLaunchHostFunc(stream, &on_complete, &ctx_) != cudaSuccess)
        return h;                  // Could not register; resume inline.
    return std::noop_coroutine();
}
// The on_complete callback runs ctx->ex.post(*ctx->cont).

// Poll: a service thread loops cudaEventQuery, then posts.
std::coroutine_handle<>
poll_awaitable::await_suspend(
    std::coroutine_handle<> h, io_env const* env)
{
    cont_.h = h;
    svc_.register_wait({event_, env->executor, &cont_, &ec_});
    return std::noop_coroutine();
}

// Deferred sync: a service thread runs the blocking call, then posts.
std::coroutine_handle<>
deferred_sync_awaitable::await_suspend(
    std::coroutine_handle<> h, io_env const* env)
{
    cont_.h = h;
    svc_.post([ex = env->executor, s = stream_,
               ec = &ec_, cont = &cont_]() mutable {
        auto err = cudaStreamSynchronize(s);
        *ec = err == cudaSuccess
            ? std::error_code{} : make_cuda_error(err);
        ex.post(*cont);
    });
    return std::noop_coroutine();
}
```

The remainder of this paper uses the callback mechanism as the running example because it is the simplest to present. Polling and deferred-synchronization awaitables appear in full in the accompanying example.<sup>[9]</sup> The mechanism is a parameter of the awaitable. Across all three, the protocol and the calling code are identical.

## 7. Hand-Rolled Awaitables Lose the Execution Environment

Strip the execution environment from Section 6's callback awaitable and what remains is the simplest possible integration - and a demonstration of why the environment exists:

```cpp
struct cuda_stream_awaiter
{
    cudaStream_t stream;

    bool await_ready() const noexcept
    {
        return false;
    }

    void await_suspend(std::coroutine_handle<> h)
    {
        cudaLaunchHostFunc(stream,
            [](void* data) {
                std::coroutine_handle<>
                    ::from_address(data)
                    .resume();
            },
            h.address());
    }

    void await_resume() noexcept {}
};
```

This works. But `resume()` executes on the CUDA driver callback thread. There is no executor affinity, no cancellation support, and no frame allocation control. The coroutine's continuation runs on whatever thread the CUDA driver chose, which may not be safe for application logic that touches shared state.

## 8. `cuda_stream`: Data Movement as IoAwaitables

The `cuda_stream` class wraps a CUDA stream handle and provides data-movement member functions that return IoAwaitables. It follows the Rule of Five (copy deleted, move implemented, null-guarded destructor). The helper function `make_cuda_error`, defined by the accompanying demonstration<sup>[9]</sup> rather than by Capy, converts a `cudaError_t` to `std::error_code` via a CUDA error category.

The key mechanism is `resume_ctx`: a pre-allocated member that captures the executor and continuation for `cudaLaunchHostFunc`. The `on_complete` callback posts the continuation back to the application's executor, providing the executor-affinity dispatch that the hand-rolled awaitable in Section 7 lacks.

```cpp
class cuda_stream
{
    cudaStream_t stream_ = nullptr;
    continuation cont_;
    std::error_code error_;

    struct resume_ctx
    {
        executor_ref ex;
        continuation* cont;
    };

    resume_ctx ctx_;

    static void CUDART_CB
    on_complete(void* arg)
    {
        auto* ctx =
            static_cast<resume_ctx*>(arg);
        ctx->ex.post(*ctx->cont);
    }

public:
    // Rule of Five: create, destroy, move.
    // Copy is deleted.
    cuda_stream();
    ~cuda_stream();
    cuda_stream(cuda_stream&&) noexcept;
    cuda_stream& operator=(
        cuda_stream&&) noexcept;
    cuda_stream(cuda_stream const&) = delete;
    cuda_stream& operator=(
        cuda_stream const&) = delete;

    cudaStream_t native_handle()
        const noexcept
    {
        return stream_;
    }

    auto memcpy_h2d(
        void* dst, void const* src,
        std::size_t count)
    {
        struct awaitable
        {
            cuda_stream* self;
            void* dst;
            void const* src;
            std::size_t count;

            bool await_ready()
                const noexcept
            {
                return false;
            }

            std::coroutine_handle<>
            await_suspend(
                std::coroutine_handle<> h,
                io_env const* env)
            {
                auto err = cudaMemcpyAsync(
                    dst, src, count,
                    cudaMemcpyHostToDevice,
                    self->stream_);
                if (err != cudaSuccess)
                {
                    self->error_ =
                        make_cuda_error(err);
                    return h;
                }
                self->cont_.h = h;
                self->ctx_ = resume_ctx{
                    env->executor,
                    &self->cont_};
                err = cudaLaunchHostFunc(
                    self->stream_,
                    &on_complete,
                    &self->ctx_);
                if (err != cudaSuccess)
                {
                    self->error_ =
                        make_cuda_error(err);
                    return h;
                }
                return std::noop_coroutine();
            }

            void await_resume()
            {
                if (self->error_)
                    throw std::system_error(
                        self->error_);
                self->error_ = {};
            }
        };
        return awaitable{
            this, dst, src, count};
    }

    auto memcpy_d2h(
        void* dst, void const* src,
        std::size_t count);
        // same pattern, cudaMemcpyDeviceToHost

    auto synchronize();
        // cudaLaunchHostFunc only (no preceding op)
};
```

The `resume_ctx` lives inside `cuda_stream` as a pre-allocated member, so no per-operation heap allocation occurs. This is safe under a single-owner discipline, which is a precondition rather than a consequence of suspension: one coroutine owns the `cuda_stream`, and because that coroutine suspends on each `co_await`, only one operation is in flight at a time. Two coroutines sharing a `cuda_stream` would race on the pre-allocated state. In the networking domain, the same contract governs Capy's sockets and their pre-allocated op states. The CUDA Programming Guide<sup>[23]</sup> confirms that operations in a stream execute in enqueue order, and the CUDA Runtime API documentation<sup>[15]</sup> states that `cudaLaunchHostFunc` callbacks block later work in the stream until they return.<sup>[29]</sup> Under the discipline, the pre-allocated `resume_ctx` is never accessed concurrently.

`cudaLaunchHostFunc` has documented constraints that production code must respect. The callback must not call CUDA APIs or synchronize on outstanding CUDA work.<sup>[15]</sup> A single CUDA-internal worker thread may service all callbacks across all streams. On loaded systems, OS scheduling can starve this thread, producing latency spikes up to 12ms between callback completion and stream resumption.<sup>[30]</sup> The 12ms figure is a single user report that NVIDIA's forum responder could not reproduce on other GPU models. If the callback blocks on a user lock while the CUDA launch queue is full, the enqueuing thread blocks too, producing deadlock.<sup>[31]</sup> Notification is unidirectional: `cudaLaunchHostFunc` provides stream-to-CPU notification only and cannot make the stream wait for a CPU-side signal.<sup>[32]</sup> These constraints apply equally to any pattern that uses `cudaLaunchHostFunc` for completion notification, including the hand-rolled awaitable in Section 7 and any sender-based wrapper that uses the same mechanism. They do not invalidate the pattern but they bound its applicability in high-throughput pipelines. The first three are specific to the callback mechanism, and the polling and deferred-synchronization awaitables of Section 6 sidestep them. Unidirectional notification, the fourth, is a property of GPU-to-host completion generally. The CHEP 2026 slides<sup>[28]</sup> show the alternatives scaling better in multi-threaded jobs, and CERN's traccc port<sup>[33]</sup> implements all three strategies over this one protocol so the mechanism can be selected per deployment. In every case, the IoAwaitable protocol is the same. Only the notification source changes.

One caveat: `cudaMemcpyAsync` is only truly asynchronous with pinned (page-locked) memory.<sup>[34]</sup> With pageable memory allocated via `malloc` or `new`, the call blocks the host thread despite the `Async` suffix.<sup>[35]</sup> For multi-gigabyte model weight transfers, this distinction matters.

### NCCL interop

NCCL collectives enqueue onto a CUDA stream. The `native_handle()` accessor provides the raw stream, and `synchronize()` awaits completion:

```cpp
ncclAllReduce(
    sendbuf, recvbuf, count,
    ncclFloat, ncclSum,
    comm, cs.native_handle());
co_await cs.synchronize();
```

When using grouped NCCL calls, `cudaLaunchHostFunc` must be enqueued after `ncclGroupEnd()` returns. For standalone calls, `co_await cs.synchronize()` immediately after the collective is correct.

## 9. `cuda_device_stream`: GPU Memory as a WriteStream

The `cuda_device_stream` class reshapes the memcpy pattern to satisfy the `WriteStream` concept, enabling GPU device memory to hide behind `any_write_stream`. Errors travel through `io_result` instead of exceptions:

```cpp
class cuda_device_stream
{
    cudaStream_t stream_;
    std::byte* d_ptr_;
    std::size_t offset_ = 0;
    continuation cont_;
    std::error_code error_;

    struct resume_ctx
    {
        executor_ref ex;
        continuation* cont;
    };

    resume_ctx ctx_;

    static void CUDART_CB
    on_complete(void* arg)
    {
        auto* ctx =
            static_cast<resume_ctx*>(arg);
        ctx->ex.post(*ctx->cont);
    }

public:
    cuda_device_stream(
        cudaStream_t s,
        std::byte* device_ptr)
        : stream_(s)
        , d_ptr_(device_ptr) {}

    // each call transfers the first buffer of
    // the sequence; the transfer completes in
    // full or fails with an error
    template<ConstBufferSequence Buffers>
    auto write_some(Buffers buffers)
    {
        struct awaitable
        {
            cuda_device_stream* self;
            const_buffer buf;

            bool await_ready()
                const noexcept
            {
                return false;
            }

            std::coroutine_handle<>
            await_suspend(
                std::coroutine_handle<> h,
                io_env const* env)
            {
                auto n = buffer_size(buf);
                auto err = cudaMemcpyAsync(
                    self->d_ptr_ +
                        self->offset_,
                    buf.data(), n,
                    cudaMemcpyHostToDevice,
                    self->stream_);
                if (err != cudaSuccess)
                {
                    self->error_ =
                        make_cuda_error(err);
                    return h;
                }
                self->cont_.h = h;
                self->ctx_ = resume_ctx{
                    env->executor,
                    &self->cont_};
                err = cudaLaunchHostFunc(
                    self->stream_,
                    &on_complete,
                    &self->ctx_);
                if (err != cudaSuccess)
                {
                    self->error_ =
                        make_cuda_error(err);
                    return h;
                }
                return std::noop_coroutine();
            }

            io_result<std::size_t>
            await_resume()
            {
                if (self->error_)
                {
                    auto ec = self->error_;
                    self->error_ = {};
                    return {ec, 0};
                }
                auto n = buffer_size(buf);
                self->offset_ += n;
                return {{}, n};
            }
        };
        return awaitable{this,
            *capy::begin(buffers)};
    }
};
```

`cuda_device_stream` satisfies `WriteStream`. Each `write_some` call transfers the first buffer of the sequence - the standard `write_some` contract - and the `cudaMemcpyAsync` behind it either transfers that buffer in full or fails with an error. It can be wrapped in `any_write_stream`.

### Link-time polymorphism

The type-erased interface enables a protocol handler compiled once to link against any transport:

```cpp
// protocol.cpp - compiled once as .o/.so/.dll
task<> ingest(
    any_write_stream& dest,
    std::span<std::byte const> data)
{
    auto [ec, n] = co_await dest.write_some(
        capy::make_buffer(data));
    if (ec) co_return;
    // ...protocol logic...
}
```

```cpp
// gpu_main.cpp - link against GPU transport
cuda_device_stream gpu_sink(stream, d_ptr);
any_write_stream dest(&gpu_sink);  // non-owning
co_await ingest(dest, payload);    // -> GPU memory
```

```cpp
// net_main.cpp - link same .o against TCP
tcp_socket sock(ioc, ep);
any_write_stream dest(&sock);  // non-owning
co_await ingest(dest, payload);  // -> network
```

The `ingest` handler and the GPU leg are exercised by the accompanying demonstration,<sup>[9]</sup> with an in-memory `WriteStream` standing in for the socket. The TCP leg is the same pattern over Capy's existing socket streams.

The algorithm in `protocol.cpp` is compiled once. At link time, swap the transport. No recompilation. Zero per-operation allocation in all cases, by the fixed-size-awaitable mechanism of Section 10. Section 11 traces the design lineage and the ABI consequence.

## 10. The Type Erasure Asymmetry

Shown in Section 9, the link-time polymorphism is a structural property of how the two models interact with the type system.

**Awaitable under type erasure.** `await_suspend` takes `coroutine_handle<>` - type-erased by the language itself. The awaitable has a fixed, compile-time-known size. At construction, the type-erased wrapper preallocates one awaitable buffer and placement-constructs each operation into it. Its per-operation vtable entries - `await_ready`, `await_suspend`, `await_resume`, `destroy` - have fixed signatures. Result: zero per-operation allocation, even through a virtual stream interface.

**Sender under type erasure.** `connect(sender, receiver)` produces an operation state whose type depends on both the sender and the receiver. Under type erasure (`any_sender`), the receiver's type is unknown at compile time. The operation state's size is unknown. The coroutine frame cannot absorb it. `any_sender::connect` must heap-allocate.<sup>[8]</sup> stdexec mitigates this with a 64-byte small buffer optimization,<sup>[36]</sup> but this paper estimates a nested `starts_on` operation state under `any_sender`/`any_receiver` double erasure at 72-152 bytes from its components - the schedule operation state, the result variant, the `starts_on` glue, and the erasure wrappers - exceeding that buffer, so the allocation stands.

Table 1 shows per-operation time and heap allocations for native and type-erased stream reads, 100 million `read_some` calls on a single thread. The measurement setup is documented in P4088R1.<sup>[4]</sup>

| Stream type | Coroutine (Capy) | Sender pipeline |
|---|---|---|
| Native | 31.4 ns/op, 0 alloc/op | 30.0 ns/op, 0 alloc/op |
| Type-erased | 36.4 ns/op, **0 alloc/op** | 53.4 ns/op, **1 alloc/op** |

Native performance is comparable - 30.0 ns vs 31.4 ns, a 1.4 ns difference. Under type erasure the two paths separate: the coroutine path stays at 36.4 ns with zero allocations, while the sender path rises to 53.4 ns and incurs one heap allocation per operation. The 17 ns gap and the per-operation allocation are structural, following from how each model interacts with type erasure.

The same asymmetry applies to any byte-oriented operation that goes through a type-erased interface - GPU memory transfers, network sockets, RDMA queue pairs. For domains where type erasure is the natural interface (a protocol compiled once, linked against any conforming transport), the coroutine model has a structural advantage.

This asymmetry also determines which model can provide a stable binary interface for I/O. Section 11 takes it up.

## 11. ABI Stability as a Structural Consequence

The type erasure asymmetry in Section 10 has a further consequence: an ABI-stable interface for async I/O.

The type-erased wrapper's per-operation vtable entries - `await_ready`, `await_suspend`, `await_resume`, and `destroy` - have fixed signatures. The signature `await_suspend(coroutine_handle<>, io_env const*)` is fixed because `coroutine_handle<>` is type-erased by the language itself. Awaitable size and vtable layout are known at compile time, so the interface can be compiled into a shared library (`.so`/`.dll`) and the implementation swapped without recompiling the consumer.

Sender pipelines provide this only at the cost the previous section measured. Without type erasure, `connect(sender, receiver)` produces an operation state whose type and size depend on both the sender and the receiver. Every new combination is a new type - a new ABI surface - and changing the I/O implementation forces recompilation of every consumer. With type erasure (`any_sender`), the boundary becomes fixed but every operation heap-allocates (Section 10).

This ABI stability requires no engineering effort and no policy constraint. It falls out of the coroutine model's type erasure, because the language provides the fixed-type boundary. Three consequences follow: a design lineage (the abstraction arc), a maintenance property (security patching), and a deployment story (the inference stack).

### The abstraction arc

The interface/implementation split follows the design trajectory of Thrust and the C++17 parallel algorithms - a standard interface over hardware-specific implementation. The precedent covers the interface, not the ABI: both precedents are compile-time template interfaces with no stable binary boundary. What this design adds is the fixed vtable.

**Thrust (2009).** GPU parallel algorithms behind an STL-compatible interface. Customers wrote to the STL vocabulary, ran on NVIDIA's GPU. The interface was vendor-neutral: customers could retarget to TBB or OpenMP. N3408 (2012) carried this into C++17 parallel algorithms.<sup>[37]</sup>

**C++17 parallel algorithms.** Standard interface, hardware-specific implementation. Write `std::sort(std::execution::par, ...)`, link against NVIDIA's implementation or Intel's. The standard owns the interface, and the vendor owns the implementation.

**IoAwaitable streams.** Write `ingest(any_write_stream&, payload)`, link against the demonstrated `cuda_device_stream`, a TCP socket, or - hypothetically today - a ROCm or RDMA transport written to the same concepts. Same pattern, applied to data transport instead of parallel algorithms. The abstraction level rises again, and the application code stays the same. A demonstration accompanies this paper<sup>[9]</sup> in which the same `ingest` handler is compiled once and exercised against both `cuda_device_stream` and an in-memory `WriteStream`.

### Security patching without recompilation

The ABI-stable boundary means a TLS (Transport Layer Security) stream implementation can be upgraded for a security patch - or swapped out for a different implementation entirely - without recompiling the application. The protocol handler was compiled against `any_write_stream`. Behind that interface sits the TLS implementation. Replace the shared library, restart the process.

This is how security-critical infrastructure is maintained in practice: the application binary does not change, only the transport layer underneath it. At `connect`, a non-erased sender pipeline stamps both types into the operation state, so changing the TLS implementation changes the type and with it the ABI. The sender route to the same property is `any_sender`, which incurs the per-operation allocation of Section 10.

### The complete inference stack

An inference server receives HTTP requests (TCP transport), dispatches to GPU compute (`stdexec` scheduler), moves results through NVLink or InfiniBand (NCCL/RDMA transport), and responds over HTTP. Today, no C++ standard interface covers the data-transport layer. IoAwaitable's ABI-stable streams complete the stack. The protocol handler compiles once and deploys across the full topology - PCIe, NVLink, InfiniBand, Ethernet - without recompilation. Each model serves its natural domain: senders for GPU kernel dispatch where compile-time work graphs deliver their full value, IoAwaitables for data transport where type-erased streams and ABI stability are the natural interface.

## 12. Partial Success Requires a Compound Result

Byte-oriented operations deliver results as a compound pair, status plus byte count, and the pattern spans hardware boundaries. A POSIX `read` returns `(errno, bytes_read)`. An RDMA work completion returns `(wr_id, status, byte_len)`. CUDA and NCCL report only a status at completion: the transfer count is the caller's own argument, which the IoAwaitable wrapper echoes back, and the transfer either completes in full or fails (Section 9). Where partial success is native, both values are always present and the byte count is not redundant with the error code: a `read` that returns 0 bytes with no error means EOF, and a `read` that returns `ECONNRESET` with 47 bytes means 47 bytes arrived before the peer reset the connection.

P2300R10<sup>[10]</sup> Section 4.14, titled "Senders can represent partial success," poses this directly: "This begs the question of how they can be used to represent async operations that partially succeed." P2300R10 answers it by passing both the error code and the result through the value channel. The cost of that answer is what the rest of this section examines.

The sender model provides three completion channels: `set_value`, `set_error`, and `set_stopped`. A compound I/O result must be routed to one of them:

- Route both values through `set_value`: downstream `upon_error` and `retry` algorithms cannot see the error.
- Route the error through `set_error`: the byte count is lost.
- Route through `set_stopped`: both values are lost.

The best available option is routing both through `set_value` as a compound type. But this means I/O errors bypass the `set_error` channel, disadvantaging sender algorithms that operate on error and stopped channels. P4091R1<sup>[5]</sup> documents all six positions that have been proposed. Each carries a cost.

The coroutine version sidesteps the channel choice entirely:

```cpp
auto [ec, n] = co_await stream.read_some(buf);
if (ec == errc::connection_reset)
{
    // 'n' bytes arrived before the reset
    process(buf, n);
    co_return;
}
```

Structured bindings deliver both values, with no data loss and no channel to choose. The application has the full compound result and decides how to handle it.

This is a domain mismatch, not a sender defect. The three-channel model was designed for operations that succeed, fail, or are cancelled - a natural fit for GPU kernel dispatch, where `cudaErrorLaunchFailure` is fatal and carries no partial result. Byte-oriented data movement operates in a domain where partial success is routine and both the status and the byte count must reach the application.

## 13. HPC Networking Plans at Runtime

The sender model's compile-time pipeline visibility eliminates virtual dispatch and heap allocation - costs on the order of tens of nanoseconds per operation (Table 3 lists 30-60 ns for a malloc-backed frame). These are real costs in nanosecond-scale GPU kernel dispatch. But are they measurable at the latency scale of network data transfers?

HPC networking APIs use runtime completion models:

```c
// NCCL: CUDA stream completion
ncclAllReduce(send, recv, count,
    type, op, comm, stream);

// UCX: callback from progress engine
ucp_tag_send_nbx(ep, buffer, length,
    tag, &amp;param);

// NVSHMEM: GPU-initiated put with fence
nvshmem_int_put(dest, src, count,
    target_pe);

// libfabric: completion queue poll
fi_send(ep, buffer, len, desc,
    dest_addr, &context);

// libibverbs: completion channel fd
ibv_post_send(qp, &wr, &bad_wr);
```

Five libraries, five different async models: streams, callbacks, GPU-initiated operations, completion queues, and file-descriptor-based reactor patterns. Zero compile-time work graphs. These are the communication layers used in large-scale GPU training, weather simulation, and molecular dynamics.

Planning decisions in HPC networking are runtime:

- **Topology discovery** happens at communicator creation via `ncclCommInitRank`.<sup>[16]</sup> NCCL discovers NVLink/NVSwitch/InfiniBand topology and selects ring vs tree algorithms, chooses transports, and builds channel structures. These decisions are driven by hardware probing rather than compile-time type information.
- **Compute/communication overlap** is expressed through CUDA stream dependencies via `cudaEventRecord` and `cudaStreamWaitEvent`.<sup>[24]</sup> The scheduler does not need to see the type of the collective to overlap it with compute. It needs the data dependency, captured by the event.
- **Memory registration** is setup-time: `ibv_reg_mr` pins pages, maps GPU base address register (BAR) regions, and exchanges rkeys with peers.<sup>[17]</sup> All done before the first byte moves.

The RDMA completion channel exposes a plain file descriptor (`ibv_comp_channel.fd`) that works with epoll - the same reactor pattern as TCP sockets. The work completion returns `(wr_id, status, byte_len)`, the same compound result pattern, and the `wr_id` is a natural coroutine dispatch key.

The stdexec repository focuses on compute scheduling. HPC networking integration is not yet represented. The Maxwell FDTD example uses MPI (Message Passing Interface) for communication, invoked manually inside `then()` callbacks - the network I/O is not expressed as senders. Coroutine-based integration could complement stdexec here: NCCL, RDMA, and NVLink all use runtime completion models (streams, callbacks, file descriptors) that map naturally to the IoAwaitable pattern, providing the data-movement layer that compute scheduling sits on top of.

In active development, the closest project to sender-based HPC networking is LCI (Lightweight Communication Interface), a C++17 async communication library with libibverbs and libfabric backends and prototype GPU-Direct RDMA, published at SC'25.<sup>[38]</sup> The LCI paper documents its integration with the HPX runtime as an RDMA transport layer. This is sender-adjacent HPC networking through a runtime wrapper rather than direct sender composition over the wire protocol, but it suggests the space is being explored.

Whether any per-operation planning decision in HPC networking benefits from compile-time type visibility of the send and receive calls themselves remains an open question. For communication patterns known at compile time, the answer may be yes. For data-dependent communication patterns determined at runtime, the record shows no example.

## 14. Sender-Based Networking: Deployed Evidence

At scale, the sender/receiver model has been deployed for compute scheduling and infrastructure (Section 3). Has it been deployed for byte-oriented data movement, the domain this paper examines?

Meta deploys the sender/receiver model in production through libunifex. Their internal guidance is instructive. From GitHub issue #586<sup>[39]</sup> (December 2023):

> "Our experience at Meta has been that coroutines are easier to read, write, debug, and just generally maintain than composition-of-sender algorithms-style code. The cost of that ease is basically overhead; coroutines don't optimize as well as raw senders (either for size or speed). The advice we give to internal teams adopting Unifex is that they should prefer coroutines until they know that the overheads are unacceptable, at which point they can refactor to the lower-level abstraction of raw senders."

In libunifex, coroutines consume senders, so the guidance concerns the authoring surface on top of a sender substrate: the team that ships sender/receiver in production directs that surface to coroutines for the common case. The public record does not show whether Meta's production use includes byte-oriented networking of the kind this section surveys. The deployment is sender implementation experience, with its data-movement domain unresolved.

Table 2 lists the sender-based networking projects outside Meta that the survey found, with each project's foundation and status:

| Project | Built on | Status |
|---|---|---|
| uring_exec<sup>[40]</sup> | io_uring + stdexec | Single-developer echo server |
| execution-ucx<sup>[41]</sup> | UCX + libunifex | RDMA/RPC, not on stdexec |
| beman.net<sup>[42]</sup> | P2762 + beman.execution | "not yet ready for production use" |
| senders-io<sup>[43]</sup> | stdexec | Experimental I/O and networking adaptation |
| kuhllib<sup>[44]</sup> | Custom senders | Conference demo |
| snp<sup>[45]</sup> | libunifex + Boost | Inactive since August 2023 |
| Asio adapter PR<sup>[46]</sup> | stdexec PR #1501 | Closed unmerged |

None are production-grade. The most complete (uring_exec) is a single developer's project with a TCP echo server. P2300R10<sup>[10]</sup> presents its HTTP server examples at a level that, in its own words (Section 1.7), "ignore[s] the low-level details of the HTTP server".

SG14, the study group for low-latency systems practitioners, has formally recommended ([P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf)<sup>[12]</sup> Section 2): "Networking (SG4) should not be built on top of P2300."

The gap between networking ambition and deployed evidence suggests that data movement and compute dispatch have different enough completion models that a single abstraction does not serve both optimally. Section 15's independent validation shows where each model fits, and the bridge in Section 18 connects the two domains.

## 15. Eight Projects Converged; CERN Adopted

Eight independent projects have arrived at the same design - coroutine-based async completion for GPU and HPC data movement - and a ninth, CERN's Next Generation Triggers project, ported a working track-reconstruction pipeline onto the IoAwaitable protocol itself. The notification mechanism that bridges GPU completion to coroutine resumption varies - a host-function callback (`cudaLaunchHostFunc`, or its driver-level equivalent `cuLaunchHostFunc`), event polling, or deferred stream synchronization - but the coroutine completion model is common to all of them. Where a project documents a single bridge (cuda-oxide, Taro), it is the callback, the simplest to wire up. CERN's port implements all three.

**cuda-oxide (NVIDIA Labs, Rust).**<sup>[47]</sup> NVIDIA's own research lab implemented the same mechanism in Rust. Their `DeviceFuture` submits GPU work, enqueues a `cuLaunchHostFunc` callback that sets an `AtomicBool` and wakes a Tokio `Waker`, and the async runtime resumes the task on the next poll. Zero busy-wait. The three-state machine (Idle, Executing, Complete) is structurally identical to a network socket future. The vendor's own research lab reached the same `cudaLaunchHostFunc`-to-async-runtime pattern independently, in a different language.

**CERN wp1.7-traccc (adoption, not convergence).**<sup>[33]</sup> As part of the Next Generation Triggers wp1.7 work package evaluating C++20 coroutines for task scheduling, the CERN team ported the traccc GPU track-reconstruction pipeline - research code rather than production - from stdexec to Capy, in a pull request open as of this writing. This is an outside team adopting the published protocol, evidence of a different kind: the protocol as published is usable by a team that did not design it. Because it cuts the other way, the pre-port state is recorded here: traccc's coroutine layer ran on stdexec first, so the same repository is also sender implementation experience. The pull request does not state the team's reasons for moving, and this paper does not infer them. It implements its CUDA completion strategies behind a single `await_strategy` selector: a `cudaLaunchHostFunc` callback, event polling, and deferred `cudaStreamSynchronize`. Each is an awaitable with the signature `await_suspend(std::coroutine_handle<>, boost::capy::io_env const*)` that posts the coroutine handle back to `env->executor`. That a real reconstruction workload exercises all three notification mechanisms over one protocol is the most concrete evidence in this survey that the coroutine model is not bound to the callback.

**Taro (University of Wisconsin-Madison).**<sup>[48]</sup> A C++20 coroutine task-graph system for CPU-GPU workloads. GPU tasks suspend the CPU thread via coroutines when waiting for GPU completion, allowing other tasks to run. Uses `cudaLaunchHostFunc` for the callback. Published at Euro-Par 2024 (as TaroRTL) and presented at CppCon 2023. TaroRTL reported a 40-80% speedup over RTLflow, a state-of-the-art GPU-accelerated register-transfer-level (RTL) simulator.

**async-cuda (Oddity AI, Rust).**<sup>[49]</sup> A library (its README marks it work-in-progress) whose authors state, in the project README: "Since the GPU is just another I/O device (from the point of view of your program), the async model actually fits surprisingly well."

**Schr&ouml;dinger Desmond (production, GTC 2024).**<sup>[50]</sup> The Desmond molecular dynamics engine uses C++ coroutines to overlap multiple GPU simulations. Coroutines suspend when a simulation hits a serial bottleneck, allowing another simulation to use the GPU. Presented at GTC 2024. Achieved up to 2.02x speedup in FEP+ (free energy perturbation) drug discovery workloads. The NVIDIA developer-blog account<sup>[50]</sup> describes the approach as "improving GPU utilization without complex code restructuring".

**TTG/PaRSEC (TESSE/EPEXA).**<sup>[51]</sup> A template task graph framework where `co_await ttg::device::select(...)` and `co_await ttg::device::wait(...)` are the primary mechanism for GPU task dispatch. Supports CUDA, HIP/ROCm, and Intel Level Zero. The project's README states that "the use of coroutines is the primary reason why TTG requires C++20 support by the C++ compiler".

**RDMA coroutine libraries.** Three independent projects wrap RDMA verbs as coroutine awaitables: RDMA++ (rdmapp)<sup>[52]</sup> wraps libibverbs with C++20 coroutines, completing operations from a completion-queue polling thread; Loom<sup>[53]</sup> provides C++23 typed bindings over libfabric with `co_await ep.async_receive(buf, asio::use_awaitable)`; and FORD<sup>[54]</sup> (USENIX FAST 2022) implements coroutine-enabled distributed transactions over one-sided RDMA, spawning multiple follow-on systems (Motor, CREST at ASPLOS 2026).

These projects span GPU compute, molecular dynamics, high-energy physics, RDMA networking, and distributed systems, and they range in maturity: Desmond ships in production, cuda-oxide and the CERN work are research code, and Taro and the RDMA libraries are academic or single-developer projects. Judged by the deployment standard Section 14 applies to sender networking, this survey too contains exactly one production system. The convergence claim is about independent design choice rather than deployment success. The eight converging projects were built by independent teams with no coordination. Two caveats bound what the convergence shows: the two Rust projects had no sender alternative in their language, and FORD (published 2022) and Taro (presented 2023) predate a usable `std::execution`, so part of the convergence reflects what was available. What remains is a finding: teams that needed GPU data movement inside an async runtime repeatedly built awaitable completion on the GPU's own notification primitives. And three of these projects (Taro, TTG/PaRSEC, Desmond) extend the coroutine pattern to kernel dispatch and GPU pipeline orchestration, placing that evidence in the record without this paper needing to reproduce it. That three of the eight operate in the dispatch domain cuts both ways: it strengthens the case that the coroutine completion model generalizes, and it complicates any strict assignment of dispatch to senders. This paper's domain split describes the centers of the two domains, not a border. Section 19.5 states the survey's limits.

## 16. CUDA Graphs Optimize a Different Layer

Sender pipelines provide compile-time `operation_state` fusion. [P3425R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3425r1.html)<sup>[55]</sup> documents 8 bytes saved per nesting level via constant pointer offsets. This is real.

CUDA Graphs<sup>[56]</sup> provide GPU-side work-graph optimization at the driver level. The driver sees streaming multiprocessor (SM) count, memory bandwidth, occupancy, and hardware topology. Stream capture<sup>[25]</sup> records kernel DAGs (directed acyclic graphs):

```c
cudaStreamBeginCapture(stream,
    cudaStreamCaptureModeGlobal);
kernel_A<<<grid, block, 0, stream>>>(args);
kernel_B<<<grid, block, 0, stream>>>(args);
cudaStreamEndCapture(stream, &graph);

cudaGraphInstantiate(&instance, graph, 0);
cudaGraphLaunch(instance, stream);
```

The CUDA Graph documentation quantifies per-kernel launch overhead at 20-200 us in deep-learning applications.<sup>[57]</sup> That figure includes framework dispatch above the raw C++ launch cost that Table 3 lists at 1-5 us. In DALLE2 inference (740 kernels, 3.4ms GPU time on an H100), 75% of end-to-end latency is CPU launch delays.<sup>[58]</sup> Replaying a captured graph replaces those per-kernel round trips with a single launch.

CUDA Graphs and sender compile-time fusion optimize different layers. CUDA Graphs eliminate per-kernel CPU-GPU dispatch round trips at the driver level: the language transitions, runtime processing, and driver operations that make up the 20-200 us per-kernel cost above. Sender fusion eliminates host-side C++ abstraction overhead - allocations, virtual dispatch, type erasure - at the language level. nvexec intercepts sender algorithms and replaces them with CUDA kernel launches on streams. A code search of the stdexec repository finds no CUDA Graph API use in nvexec, and a machine-generated documentation site over the repository reports the same,<sup>[59]</sup> so per-kernel host launch overhead appears to remain unless CUDA Graphs are used separately. These optimizations are complementary.

CUDA Graph replay composes naturally with coroutine-based data movement: the coroutine provides the outer loop with data-dependent control flow (memcpy in, graph launch, memcpy out, check result), and the pre-captured graph is the inner optimized hot path. Schr&ouml;dinger's Desmond engine (GTC 2024)<sup>[50]</sup> uses both techniques in the same production engine - coroutine-overlapped simulations and CUDA Graphs - with up to 2.02x speedup in drug discovery workloads. The published account lists the techniques together without describing their composition.

Two questions remain open in the record: whether sender fusion adds measurable value once graph capture has eliminated the driver-level dispatch overhead, and whether GPU pipelines beyond Desmond's structure benefit from coroutine orchestration around pre-captured graphs.

## 17. PMR Pools Amortize Frame Allocation

Each coroutine suspension potentially allocates a frame. Sender `operation_state` is a single compile-time allocation. This is a real structural difference.

### HALO

Heap Allocation eLision Optimization<sup>[60]</sup> allows the compiler to place the coroutine frame in the caller's frame when the lifetime is provably bounded. Capy's `task` is annotated with `[[clang::coro_await_elidable]]`<sup>[61]</sup> to enable this.

HALO is fragile: the attribute was introduced<sup>[62]</sup> because "Task types are rarely simple enough for the destroy logic of the task to reference the SSA value from coro.begin() directly. Hence, the pass is very ineffective for even the most trivial C++ Task types." Confirmed regressions in Clang 19-20.<sup>[63]</sup> Correctness bug with `suspend_never`.<sup>[64]</sup> Parentheses around a `co_await` operand silently break elision.<sup>[65]</sup> Clang-only. HALO is nice when it fires. It is not something to rely on.

### PMR pools

Capy's `io_env` carries a `std::pmr::memory_resource*`.<sup>[66]</sup> Thread-local recycling pools amortize allocation cost to near zero. This is reliable, portable, and works regardless of compiler optimization.

Table 3 places frame allocation next to the GPU operations a frame orchestrates. All rows are order-of-magnitude estimates offered for scale rather than measurements.

| Operation | Time |
|---|---|
| Coroutine frame alloc (PMR pool) | 2-5 ns |
| Coroutine frame alloc (malloc) | 30-60 ns |
| CUDA kernel launch (C++) | 1,000-5,000 ns |
| `cudaMemcpy` (4 bytes) | 10,000 ns |
| Conv2d forward (A100, BS=1) | 24,000 ns |
| NCCL AllReduce (600B model) | 1,000,000,000+ ns |

A coroutine frame allocation with a PMR pool is roughly two to nine orders of magnitude cheaper than the GPU operations it orchestrates. For a 600B-parameter model's AllReduce that takes seconds, the 5 ns frame allocation is at least eight orders of magnitude smaller.

One caveat: the latency table assumes GPU operations in the microsecond-to-second range. For high-frequency kernel dispatch where individual kernel execution times approach the sub-microsecond range, the frame allocation cost relative to the operation cost may be different, and whether it becomes a measurable bottleneck there is an open question for domain experts. A second caveat: `cudaLaunchHostFunc` callback latency can spike to 12ms on loaded multi-GPU systems, per the single unreproduced report discussed in Section 8,<sup>[30]</sup> which means the callback dispatch latency can dominate both frame allocation and the GPU operation itself. The 2-5 ns frame allocation cost is not always the relevant comparison.

## 18. The Bridge Between Domains

The preceding sections argue that senders and IoAwaitables each serve a domain well: senders for GPU kernel dispatch and heterogeneous scheduling, IoAwaitables for byte-oriented I/O and type-erased streams. The bridge is where the domains meet.

Capy provides two bridge functions with working implementations in its bench and example code<sup>[9]</sup>: `await_sender`<sup>[6]</sup> consumes a sender from within a coroutine via `co_await`, and `as_sender`<sup>[7]</sup> wraps an IoAwaitable as a P2300R10 sender for use in a sender pipeline. Both compile and run today. One bridge direction currently relies on behavior the standard would need to bless. [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf)<sup>[6]</sup> and [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf)<sup>[7]</sup> are the dedicated design papers for each direction.

`await_sender` is the natural bridge for the common case: a coroutine that performs I/O and dispatches to a GPU scheduler. An inference pipeline that uses each model in its natural domain:

```cpp
task<> handle_request(
    any_read_source& client,
    any_write_sink& response,
    nvexec::stream_context& gpu_ctx,
    exec::static_thread_pool::scheduler cpu)
{
    // receive request (coroutine, type-erased)
    std::array<std::byte, 4096> buf;
    auto [ec, n] = co_await client.read_some(
        capy::mutable_buffer(
            buf.data(), buf.size()));
    if (ec) co_return;

    // dispatch to GPU (sender); continues_on(cpu) hops back to
    // the host for the host-only bridge
    auto gpu = gpu_ctx.get_scheduler();
    constexpr int N = 64;
    float* d_out = nullptr;
    cudaMalloc(&d_out, N * sizeof(float));
    co_await await_sender(
        stdexec::just(N, d_out)
        | stdexec::continues_on(gpu)
        | nvexec::launch(
            {.grid_size = 1, .block_size = N},
            [] (cudaStream_t, int len, float* y) {
                int i = blockIdx.x * blockDim.x
                    + threadIdx.x;
                if (i < len)
                    y[i] = run_model(i);
            })
        | stdexec::continues_on(cpu));

    // copy result to host, send it back (type-erased)
    std::array<float, N> result;
    cudaMemcpy(result.data(), d_out,
        N * sizeof(float),
        cudaMemcpyDeviceToHost);
    cudaFree(d_out);
    co_await write(response, capy::make_buffer(
        result.data(),
        result.size() * sizeof(float)));
}
```

Network I/O uses `any_read_source` and `any_write_sink` - type-erased, zero per-operation allocation, compound results via structured bindings. GPU dispatch uses `nvexec::launch` on the stream scheduler - compile-time composition, scheduler-agnostic portability. Because nvexec runs the launched work on the device, `run_model` is a `__device__` function and the trailing `stdexec::continues_on(cpu)` returns completion to the host before the host-only `await_sender` bridge resumes the coroutine. Therefore the handler takes a host scheduler alongside the GPU context. The `await_sender` bridge connects the two without requiring either model to subsume the other.

The device-to-host `cudaMemcpy` and the per-request `cudaMalloc`/`cudaFree` in the example are deliberate simplifications that keep the bridge visible. A production handler would use `cuda_stream`'s `memcpy_d2h` awaitable and pooled device allocations.

Behind `client` and `response`, the network transport can be TCP, TLS, RDMA, or any transport that satisfies the stream concepts. The GPU scheduler can be `nvexec::stream_scheduler`, a CPU thread pool, or any scheduler that provides `schedule()`. Neither side needs to know about the other's implementation.

`as_sender` provides the reverse direction: a sender pipeline that consumes an IoAwaitable. This is useful when an existing sender pipeline needs to incorporate a byte-oriented operation:

```cpp
auto pipeline =
    stdexec::schedule(sched)
    | stdexec::then([&] {
        return prepare_buffer();
    })
    | as_sender(gpu_sink.write_some(buf))
    | stdexec::then(
        [](io_result<std::size_t> r) {
            return r.value();
        });
```

The `as_sender` bridge wraps the awaitable's completion as a sender value channel, preserving the compound result for downstream sender algorithms. Neither bridge requires rewriting the wrapped operation - the IoAwaitable and the sender each retain their native interface.

## 19. Considerations

The preceding sections present convergent findings. This section addresses foreseeable concerns about the conclusions drawn from them, grouped into five: laziness and composition, consumer choice, type erasure and allocation, composition algebra, and scope of evidence.

### 19.1 Laziness and Composition

**Awaitables commit to eager execution.** Awaitables are lazy. `write_some` returns an inert object. Until `co_await` triggers `await_suspend`, no `cudaMemcpyAsync` is issued and no syscall is made. In both models, the trigger is explicit: senders do no work until `start()` is called, and awaitables do no work until `co_await` is evaluated. A coroutine can capture the awaitable, defer the `co_await`, and decide at runtime whether to submit the operation. This concern does not distinguish the two models.

**The scheduler cannot see the full task graph.** Sender pipelines compose as a graph the scheduler can inspect before `start()`. This is valuable for GPU kernel dispatch where the work graph is known ahead of time - CUDA Graphs (Section 16) exploit this property at the driver level, replacing per-kernel launch overhead of 20-200 us with a single graph launch.<sup>[57]</sup> Data movement is different. The next transfer depends on the result of the previous one: how many bytes arrived, whether the peer reset the connection, whether the RDMA completion carried an error. There is no static graph to inspect because control flow branches on runtime data. NCCL topology discovery, RDMA memory registration, and NVLink channel selection are all runtime decisions driven by hardware probing (Section 13). Coroutine control flow - `if`, `for`, `while` - is the natural expression of data-dependent sequential decisions.

**Senders separate description from execution. Coroutines conflate them.** The separation is valuable when the same algorithm can run on CPU or GPU by swapping the scheduler. The Maxwell FDTD benchmark demonstrates this: identical sender code achieves parity with raw CUDA on GPU and runs correctly on a CPU thread pool (Section 3). Data movement operations are bound to specific hardware resources at submission time. A `cudaMemcpyAsync` targets a specific CUDA stream on a specific device, an `ibv_post_send` a specific queue pair on a specific host channel adapter (HCA), and a `read` a specific file descriptor. The description cannot be retargeted by swapping a scheduler because the operation is bound to the resource. For compute dispatch, description-execution separation enables scheduler-agnostic portability. For data transport, the binding to hardware resources makes the separation vacuous.

### 19.2 Consumer Choice and Return Types

**Data movement operations should return senders so the caller can choose how to consume them.** The choice is symmetric. `as_sender`<sup>[7]</sup> wraps an awaitable for sender pipeline consumption. `await_sender`<sup>[6]</sup> wraps a sender for coroutine consumption. Neither return type gives every consumer zero-cost access. Returning a sender forces a per-operation allocation under type erasure (Section 10: 53.4 ns/op, 1 alloc/op). Returning an awaitable preserves zero-allocation type erasure (Section 10: 36.4 ns/op, 0 alloc/op) and gives sender pipeline consumers access through `as_sender`. The question is which consumer bears the cost. For data movement where the protocol handler is compiled once against a type-erased stream (Section 9), the type-erased consumer is the common case. P4088R1<sup>[4]</sup> Section 10 documents the full design fork analysis.

**The bridge proves senders are more fundamental.** The bridge is symmetric: each model can consume the other's operations through the pair of functions described in Section 18. CPU and GPU interact through memory copies. That does not make one side more fundamental. The bridge is evidence of complementarity between models that serve different domains - compute dispatch and data transport. P4088R1<sup>[4]</sup> Section 9 addresses this directly.

### 19.3 Type Erasure and Allocation

**Type erasure should be opt-in, not baked into the abstraction.** Byte-oriented data movement is a domain where the transport is inherently runtime-determined. An inference server does not know at compile time whether input arrives over TCP, RDMA, or NVLink - the transport depends on the deployment topology, which is discovered at communicator creation time via `ncclCommInitRank` or equivalent (Section 13). Type erasure is the natural interface for this domain. Senders' compile-time visibility optimizes for static dispatch, which is not the bottleneck when every operation crosses a kernel boundary (1,000-5,000 ns) or a PCIe bus (10,000+ ns). This is the same design trajectory traced in Section 11. P4088R1<sup>[4]</sup> Section 7.1 documents the structural mechanism.

**Coroutine frames allocate. Sender operation states do not.** Acknowledged. Sender `operation_state` is a compile-time construct with no heap allocation. Coroutine frames allocate. PMR pools amortize this to near zero (Section 17). For data movement, the relevant comparison is total allocation across the stream's lifetime. Under type erasure, the sender model allocates once per `any_sender::connect` (Section 10). The coroutine model allocates once per frame (Section 10). For N operations through a type-erased stream, the coroutine model allocates once. The sender model allocates N times. P4088R1<sup>[4]</sup> Sections 4 and 7.9 cover the general case.

**Compile-time optimization is lost.** Coroutine handles are opaque. The compiler cannot see through `resume()`. Sender pipelines are fully visible, statically dispatched, inlinable. This visibility matters for GPU kernel dispatch where individual operations cost nanoseconds and the compiler can fuse host-side abstraction overhead (Section 3). The latency scale of data movement dwarfs indirect-call overhead (Section 17). For data movement, the optimization target is allocation elimination under type erasure (Section 10). P4088R1<sup>[4]</sup> Section 4 documents the optimization barrier.

### 19.4 Composition and Algorithms

**Senders provide 30 generic algorithms. Awaitables provide none.** The awaitable composition mechanism is the language's own control flow: `if`, `for`, `while`, `try/catch`, structured bindings. These compose naturally with data-dependent decisions - the `if(ec == errc::connection_reset)` in Section 12 is a branch on runtime data that determines the next operation. For GPU dispatch where the full work graph must be visible to the scheduler before launch, the sender composition algebra is justified (Section 3). For data movement where each operation depends on the result of the previous one, ordinary control flow is the natural mechanism and is debuggable with standard tools. P4088R1<sup>[4]</sup> Section 2.2 compares the two vocabularies.

**Compound results can be routed through set_value.** Route `(error_code, bytes_transferred)` through `set_value` as a compound type. This is physically possible. It is also what Section 12 documents: if all data-movement results route through `set_value`, then `set_error` and `set_stopped` are vestigial for these operations. The three-channel model's value - that different channels enable different downstream algorithms (`retry`, `upon_error`) - is nullified. P2300R10<sup>[10]</sup> Section 4.14, "Senders can represent partial success," poses the question - "This begs the question of how they can be used to represent async operations that partially succeed" - and answers it with exactly this value-channel routing. The three channels match GPU kernel dispatch, where `cudaErrorLaunchFailure` is fatal and carries no partial result. Byte-oriented operations produce compound results where both status and byte count are always present. P4091R1<sup>[5]</sup> analyzes all six positions.

### 19.5 Scope and Evidence

**Structured concurrency is weaker in the coroutine model.** Acknowledged (Section 3). Senders provide `counting_scope` for dynamic fan-out with guaranteed completion before scope destruction. Coroutines provide lexical-scope safety via `when_all` but dynamic fan-out needs explicit library support. Data movement is ordered per stream or connection - one buffer at a time, one completion at a time, the one-at-a-time invariant on the CUDA stream (Section 8) - and practical overlap comes from multiple streams or connections in flight, each individually ordered. Dynamic fan-out across an unknown number of tasks belongs to the compute dispatch domain, where senders provide it.

**The sender-based networking survey may be incomplete.** Acknowledged. The survey (Section 14) reports every project its search of the public record found. Its recall is bounded by that record. Production-grade sender-based networking that the search missed would strengthen the case for sender-based I/O and belongs in a future revision. The search method for both surveys was not recorded when they were run. The tables list what was found, and the absence claims carry that caveat.

**The CUDA examples were generated with AI assistance.** Disclosed in Section 1. The examples are presented as a research exercise for evaluation by domain experts. Errors in the CUDA code would indicate where the examples need refinement. The structural observation stands on the independent projects in Section 15, whose code this paper did not write.

**The paper's P2300R10 quotations may be taken out of context.** Both quotations state positions P2300R10 holds in its own voice: Section 4.14 poses the partial-success question and the paper presents P2300R10's own answer (value-channel routing) in the same paragraph, and Section 4.15 states the coroutine-consumption expectation as the design's intent. Each is quoted with its section number.<sup>[10]</sup>

## 20. Conclusion

From three directions, the findings converge. Structurally, the four transports examined here present one abstract interface - submit a buffer, await completion, receive a compound result - and the IoAwaitable protocol expresses that interface with zero per-operation allocation. A coroutine suspends on each `co_await`, so at most one operation is in flight per single-owner stream and the pre-allocated op-state pattern that networking sockets use carries over. The CUDA Programming Guide's stream-ordering guarantee<sup>[23]</sup> secures the invariant for every notification mechanism. Empirically, independent projects at NVIDIA Labs (cuda-oxide),<sup>[47]</sup> the University of Wisconsin-Madison (Taro),<sup>[48]</sup> and Schr&ouml;dinger (Desmond)<sup>[50]</sup> arrived at coroutine-based completion for data movement without coordination, and CERN<sup>[33]</sup> moved its traccc reconstruction pipeline onto the protocol directly. The notification mechanism is a free variable the protocol does not fix: the traccc port implements the callback, event polling, and deferred synchronization as interchangeable awaitables, and the slides of a CHEP 2026 contribution<sup>[28]</sup> find that only the callback fails to scale in their multi-threaded setup.

`cudaLaunchHostFunc` has documented limitations (Section 8) that bound the applicability of the callback mechanism in high-throughput GPU pipelines. Those limitations are specific to the callback: the protocol equally admits event polling and deferred synchronization, which sidestep them where they apply.

`std::execution` provides real properties for GPU dispatch: zero-allocation compile-time composition, scheduler-agnostic portability, domain customization via `transform_sender`, and structured concurrency for dynamic fan-out. CUDA Graphs and sender fusion optimize at different layers - graphs reduce driver-level dispatch overhead, sender fusion reduces host-side C++ abstraction overhead - and they are complementary.

Taro, TTG/PaRSEC, and Desmond demonstrate the coroutine pattern extending beyond byte movement to kernel dispatch and GPU pipeline orchestration, placing that evidence in the record alongside this paper's byte-movement analysis.

Bridges (`await_sender`<sup>[6]</sup>, `as_sender`<sup>[7]</sup>) connect the two models where the domains meet: a networking coroutine consumes a GPU sender for compute dispatch, and a sender pipeline wraps an IoAwaitable for composition. Neither model needs to subsume the other. Senders serve compute dispatch, where compile-time work graphs and scheduler-agnostic portability are decisive. Awaitables serve data transport, where type-erased streams, zero-allocation link-time polymorphism, and ABI stability (Section 11) are the working interface.

The record bears on [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup>, which proposes the IoAwaitable protocol for standardization. The surveyed projects each rebuilt coroutine completion on the GPU's own notification primitives, and the three properties that protocol specifies - executor affinity, cancellation, and frame allocation control - are the properties this paper's analysis (Sections 5 and 7) finds those hand-built integrations leave out. Now the evaluation of these findings sits with the domain experts of SG1 and with the authors of P4003R3. This paper places the record before them.

## Acknowledgements

Eric Niebler, Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Bryce Adelstein Lelbach, Dietmar K&uuml;hl, and Jens Maurer, whose work on `std::execution` (P2300R10) this paper examines and builds upon.

Richard Smith and Gor Nishanov for P0981R0 (HALO analysis). Yuxuan Chen for the `[[clang::coro_await_elidable]]` attribute. Chuanqi Xu for P2477R3 (coroutine allocation elision). Dietmar K&uuml;hl and Maikel Nadolski for P3552R3 (`std::execution::task`). Lewis Baker for cppcoro, the operator `co_await` and symmetric transfer blog posts, and P3425R1 (operation-state sizes). Michael Wong for P4029R0 (SG14 priority list).

Michael Garland and the NVIDIA stdexec team for the nvexec GPU schedulers and the Maxwell FDTD benchmark. The CERN wp1.7 team for their C++20 coroutine task-scheduling experiments and the Capy IoAwaitable integration. Dian-Lun Lin (University of Wisconsin-Madison) for Taro and its CppCon 2023 presentation. The NVIDIA Labs team for cuda-oxide. Jiqun Tu (NVIDIA) and Ellery Russell (Schr&ouml;dinger) for the Desmond coroutine integration presented at GTC 2024. The TTG/PaRSEC team for demonstrating coroutine-based heterogeneous GPU dispatch.

This paper was generated with AI assistance (Claude, via Cursor).

## References

[1] [Capy](https://github.com/cppalliance/capy) (C++ Alliance).

[2] [Corosio](https://github.com/cppalliance/corosio) (C++ Alliance).

[3] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[4] [P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[5] [P4091R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4091r1.pdf) - "Error Models of Regular C++ and the Sender Sub-Language" (Vinnie Falco, 2026).

[6] [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[7] [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[8] [P4123R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4123r0.pdf) - "The Cost of Senders for Coroutine I/O" (Vinnie Falco, 2026).

[9] [Accompanying examples](https://github.com/cppalliance/capy/tree/a226b793a3409f07723d2e90dd154e7461fffe89/example) - the compileable demonstrations for this paper, pinned at commit `a226b79` of the official repository (C++ Alliance). Section 6 (the three notification mechanisms, `callback_awaitable`, `poll_awaitable`, `deferred_sync_awaitable`): [`example/cuda/notification-strategies`](https://github.com/cppalliance/capy/tree/a226b793a3409f07723d2e90dd154e7461fffe89/example/cuda/notification-strategies). Sections 8-9 and 16 (`cuda_stream`, `cuda_device_stream`, CUDA Graphs): [`example/cuda/datamovement`](https://github.com/cppalliance/capy/tree/a226b793a3409f07723d2e90dd154e7461fffe89/example/cuda/datamovement). Section 18 (the `await_sender` bridge, `handle_request`): [`example/cuda/pipeline/cuda_pipeline.cu`](https://github.com/cppalliance/capy/blob/a226b793a3409f07723d2e90dd154e7461fffe89/example/cuda/pipeline/cuda_pipeline.cu). Sections 12-13 (compound results and HPC-fabric signatures): [`example/fabrics/fabrics.cpp`](https://github.com/cppalliance/capy/blob/a226b793a3409f07723d2e90dd154e7461fffe89/example/fabrics/fabrics.cpp).

[10] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[11] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec) - Reference implementation of `std::execution`.

[12] [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf) - "The SG14 Priority List for C++29/32" (Michael Wong, 2026).

[13] [nvexec stream_context.cuh](https://github.com/NVIDIA/stdexec/blob/main/include/nvexec/stream_context.cuh) - NVIDIA stdexec GPU scheduler.

[14] [CUDA Runtime API: Memory Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY.html) (NVIDIA, 2024).

[15] [CUDA Runtime API: Execution Control](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EXECUTION.html) (NVIDIA, 2024).

[16] [NCCL User Guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html) (NVIDIA).

[17] [ibv_create_comp_channel(3)](https://man7.org/linux/man-pages/man3/ibv_create_comp_channel.3.html) - rdma-core manual page.

[18] [Capy io_env](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/include/boost/capy/ex/io_env.hpp) (C++ Alliance).

[19] [Capy executor_ref](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/include/boost/capy/ex/executor_ref.hpp) (C++ Alliance).

[20] [Understanding Symmetric Transfer](https://lewissbaker.github.io/2020/05/11/understanding_symmetric_transfer) (Lewis Baker, 2020).

[21] [Capy continuation](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/include/boost/capy/continuation.hpp) (C++ Alliance).

[22] [Capy task](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/include/boost/capy/task.hpp) (C++ Alliance).

[23] [CUDA Programming Guide: Asynchronous Concurrent Execution](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html) (NVIDIA, 2024).

[24] [CUDA Runtime API: Event Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EVENT.html) (NVIDIA, 2024).

[25] [CUDA Runtime API: Stream Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__STREAM.html) (NVIDIA, 2024).

[26] [CUDA Handbook: Stream Callbacks](https://www.cudahandbook.com/2012/09/stream-callbacks/) (Nicholas Wilt, 2012).

[27] [Stack Overflow: Exception Handling in cudaLaunchHostFunc Callbacks](https://stackoverflow.com/questions/75145603/catching-an-exception-thrown-from-a-callback-in-cudalaunchhostfunc) (2023).

[28] [Scheduling for Next Generation Triggers](https://indico.cern.ch/event/1471803/contributions/6967272/) - CHEP 2026 contribution; the scaling findings appear in the attached presentation slides (Eric Cano, Mateusz Jakub Fila, Attila Krasznahorkay, 2026).

[29] [Stack Overflow: CUDA Graph host execution nodes in different streams](https://stackoverflow.com/questions/75739969/is-it-possible-to-execute-more-than-one-cuda-graphs-host-execution-node-in-diff) - Robert Crovella (NVIDIA) on single-stream callback serialization (2023).

[30] [NVIDIA Developer Forums: cuLaunchHostFunc overhead latency](https://forums.developer.nvidia.com/t/culaunchhostfunc-overhead-latency-usage-cpu-gpu-signaling/327066) - Latency spikes up to 12ms on loaded A100/H100 systems (2025).

[31] [NVIDIA Developer Forums: Do stream callbacks hold CUDA-internal locks?](https://forums.developer.nvidia.com/t/do-stream-callbacks-hold-any-cuda-internal-locks/337769) - Deadlock risk with user locks in callbacks (2025).

[32] [Multipath Memory Access: Breaking Host-GPU Bandwidth Bottlenecks in LLM Serving](https://arxiv.org/html/2512.16056v2) - cudaLaunchHostFunc unidirectional notification limitation (2025).

[33] [cern-nextgen/wp1.7-traccc PR #18](https://github.com/cern-nextgen/wp1.7-traccc/pull/18) - CERN port of the traccc GPU track-reconstruction pipeline from stdexec to Capy, implementing callback, event-polling, and deferred-synchronization await strategies as IoAwaitables behind a single selector (2026).

[34] [CUDA Programming Guide: Page-Locked Host Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html) (NVIDIA, 2024).

[35] [CUDA Runtime API: API Synchronization Behavior](https://docs.nvidia.com/cuda/cuda-runtime-api/api-sync-behavior.html) (NVIDIA, 2024).

[36] [NVIDIA/stdexec any_sender_of.hpp](https://github.com/NVIDIA/stdexec/blob/main/include/exec/any_sender_of.hpp) - 64-byte small-buffer optimization for type-erased sender operation states.

[37] [N3408](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3408.pdf) - "Parallelizing the Standard Algorithms Library" (Jared Hoberock, Michael Garland, Olivier Giroux, Vinod Grover, Ujval Kapasi, Jaydeep Marathe, 2012).

[38] [LCI](https://arxiv.org/html/2505.01864v2) - "LCI: a Lightweight Communication Interface for Efficient Asynchronous Multithreaded Communication" - C++17 async communication library with libibverbs and libfabric backends, prototype GPU-Direct RDMA, SC'25 (2025).

[39] [libunifex Issue #586](https://github.com/facebookexperimental/libunifex/issues/586#issuecomment-1845934903) - Meta internal guidance on senders vs coroutines (Ian Petersen, 2023).

[40] [uring_exec](https://github.com/Caturra000/uring_exec) - io_uring networking over stdexec (Caturra000).

[41] [execution-ucx](https://github.com/MoFHeka/execution-ucx) - UCX transport over libunifex (MoFHeka).

[42] [beman.net](https://github.com/bemanproject/net) - Beman project implementation of the P2762 sender networking interface.

[43] [senders-io](https://github.com/maikel/senders-io) - "An adaption of Senders/Receivers for async networking and I/O" (Maikel Nadolski).

[44] [kuhllib](https://github.com/dietmarkuehl/kuhllib) - experimental standard C++ library with sender-based networking (Dietmar K&uuml;hl).

[45] [snp](https://github.com/deepgrace/snp) - "Structured Network Programming with Sender / Receiver" (deepgrace).

[46] [stdexec PR #1501](https://github.com/NVIDIA/stdexec/pull/1501) - "Adapt boost::asio to stdexec" (closed unmerged).

[47] [cuda-oxide: The DeviceOperation Model](https://nvlabs.github.io/cuda-oxide/async-programming/the-device-operation-model.html) - NVIDIA Labs async GPU programming in Rust (2026).

[48] [Taro](https://github.com/dian-lun-lin/taro) - C++20 coroutine task-graph system for CPU-GPU workloads (Dian-Lun Lin, University of Wisconsin-Madison, 2024).

[49] [async-cuda](https://github.com/oddity-ai/async-cuda) - Async CUDA for Rust (Oddity AI, 2024).

[50] [Optimizing Drug Discovery with CUDA Graphs, Coroutines, and GPU Workflows](https://developer.nvidia.com/blog/optimizing-drug-discovery-with-cuda-graphs-coroutines-and-gpu-workflows/) - NVIDIA Developer Blog (Jiqun Tu, Ellery Russell, 2024).

[51] [TTG (Template Task Graph)](https://github.com/TESSEorg/ttg) - C++20 coroutine-based heterogeneous task graph on PaRSEC (2024).

[52] [rdmapp](https://github.com/howardlau1999/rdmapp) - C++20 coroutine wrapper for libibverbs (2024).

[53] [Loom](https://github.com/sielicki/loom) - C++23 typed interface over libfabric with Asio coroutine integration.

[54] [FORD](https://github.com/minghust/ford) - Coroutine-enabled distributed transactions over one-sided RDMA (USENIX FAST 2022).

[55] [P3425R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3425r1.html) - "Reducing operation-state sizes for subobject child operations" (Lewis Baker, 2024).

[56] [CUDA Programming Guide: CUDA Graphs](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html) (NVIDIA, 2024).

[57] [NVIDIA CUDA Graph Best Practices: Quantitative Benefits](https://docs.nvidia.com/dl-cuda-graph/cuda-graph-basics/cuda-graph.html) (NVIDIA, 2024).

[58] [PyGraph: Robust Compiler Support for CUDA Graphs in PyTorch](https://arxiv.org/html/2503.19779v3) (2025).

[59] [DeepWiki: nvexec GPU Execution](https://deepwiki.com/NVIDIA/stdexec/6-gpu-execution-with-nvexec).

[60] [P0981R0](https://www.open-std.org/JTC1/SC22/WG21/docs/papers/2018/p0981r0.html) - "Halo: coroutine Heap Allocation eLision Optimization: the joint response" (Richard Smith, Gor Nishanov, 2018).

[61] [Clang Attribute Reference: coro_await_elidable](https://clang.llvm.org/docs/AttributeReference.html#coro-await-elidable) (LLVM).

[62] [LLVM PR #99282: Introduce coro_await_elidable](https://github.com/llvm/llvm-project/pull/99282) (Yuxuan Chen, 2024).

[63] [LLVM Issue #64586: CoroElide failures and regressions](https://github.com/llvm/llvm-project/issues/64586).

[64] [LLVM Issue #188230: HALO + suspend_never bad-free](https://github.com/llvm/llvm-project/issues/188230).

[65] [LLVM Issue #178256: Parentheses break coro_await_elidable](https://github.com/llvm/llvm-project/issues/178256).

[66] [std::pmr::memory_resource](https://en.cppreference.com/w/cpp/memory/memory_resource) (cppreference).
