---
title: "IoAwaitables for GPU Data Movement: Convergent Findings"
document: P4251R0
date: 2026-09-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

GPU data movement fits the same completion interface as sockets and RDMA, a design that independent projects converged on without coordination.

C++ has a standard model for asynchronous execution in `std::execution`, validated in GPU kernel dispatch, where its compile-time composition, scheduler portability, and structured concurrency are strongest; the byte transfers that feed those kernels - host-device copies, NCCL collectives, RDMA verbs, and TCP reads - have no standard interface. On the transport side, each of the four presents the same shape - submit a buffer, receive an asynchronous completion, receive a compound result of status and byte count - and the IoAwaitable protocol expresses that shape with a fixed vtable and no per-operation allocation under type erasure, where `any_sender` heap-allocates on every connect. A protocol handler compiled once against an awaitable stream can therefore be relinked against a GPU, TCP, or TLS transport without recompilation, within one standard library and compiler ABI. Seven projects across NVIDIA Labs, academia, molecular dynamics, and the RDMA ecosystem suspend coroutines on GPU or RDMA work, six by independent design and two in Rust with no sender alternative, and CERN has an open port of a GPU track-reconstruction pipeline onto the protocol itself with callback, event polling, and deferred synchronization as interchangeable strategies, so the notification mechanism is a variable the protocol leaves free.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## 1. Introduction

`std::execution` gives C++ a composable model for asynchronous execution, validated in GPU kernel dispatch and heterogeneous scheduling (Section 2). The byte-oriented data movement that feeds those kernels - host-device memcpy, collectives, RDMA (Remote Direct Memory Access) transfers, socket reads - has no standard interface, and which async model serves that layer is an open question in the committee's record: [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[1]</sup> defines the sender model and stdexec<sup>[2]</sup> implements it, [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup> proposes the coroutine-based IoAwaitable protocol, and [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf)<sup>[4]</sup> records SG14's position on sender-based networking. This paper examines the GPU corner of that question: how CUDA's async completion model integrates with coroutines for byte-oriented data movement.

The paper reports five findings:

1. Four data-movement APIs that cross four different hardware boundaries - `cudaMemcpyAsync`, NCCL collectives, RDMA verbs, and TCP sockets - fit one abstract interface: submit a buffer, receive an async completion, dispatch a compound result. POSIX and RDMA present the compound result natively. For CUDA and NCCL the wrapper synthesizes it (Sections 3 and 11).
2. The IoAwaitable protocol captures this interface, and the notification mechanism is a free variable: callback, event polling, and deferred synchronization all satisfy it (Section 5). Compile-validated `cuda_stream` and `cuda_device_stream` listings accompany the paper (Sections 7-8), and a runnable example exercises all three notification mechanisms (Section 5).
3. Under type erasure, the awaitable form allocates nothing per operation and has a fixed vtable, which yields an ABI-stable stream interface. The sender form heap-allocates per operation (Sections 9-10).
4. Seven projects, six of them independent designs - at NVIDIA Labs, the University of Wisconsin-Madison, Oddity AI, Schr&ouml;dinger, the EPEXA project, and in the RDMA ecosystem - converged on coroutine-based suspension on GPU and RDMA work without coordination, three of them (cuda-oxide, Taro, rdmapp) plus the CERN port documenting the completion bridge, and CERN has an open port of its traccc track-reconstruction pipeline onto the IoAwaitable protocol itself (Section 14).
5. The sender model's strengths - zero-allocation compile-time composition, scheduler portability, structured concurrency for dynamic fan-out - are strongest in kernel dispatch, and bidirectional bridges connect the two domains (Sections 2, 15, and 17).

Related work beyond the papers named above: P4088R1<sup>[5]</sup> analyzes what C++20 coroutines already buy the standard, P4091R1<sup>[6]</sup> the error models of regular C++ and the sender sub-language, P4123R0<sup>[7]</sup> the cost of senders for coroutine I/O, and P4092R1<sup>[8]</sup> and P4093R1<sup>[9]</sup> the two bridge directions between senders and coroutines.

The paper's assumptions: the CUDA examples were produced with AI assistance and are offered for evaluation by domain experts rather than as expert testimony (the Disclosure); Table 1 in Section 9 reproduces P4088R1's<sup>[5]</sup> measurements while the operation-state sizes in the same section are this paper's own; and the surveys of sender-based networking (Section 13) and of convergent projects (Section 14) are bounded by the public record their methods searched.

## 2. What std::execution Provides

`std::execution` provides four properties that this paper's findings do not contest.

**Zero-allocation composition.** Sender pipelines collapse into a single `operation_state` at compile time. No heap allocation, no virtual dispatch, no reference counting. This is a real property that coroutines do not match for multi-stage pipelines.<sup>[1]</sup>

**Domain customization.** A scheduler's `transform_sender` can replace `bulk` with a GPU kernel launch transparently. This enables writing algorithm code once and retargeting to CPU or GPU by swapping the scheduler.<sup>[10]</sup>

**Structured concurrency.** `counting_scope` tracks dynamically spawned work and prevents scope destruction until all work completes. Coroutines provide lexical-scope safety via `when_all`, but dynamic fan-out to an unknown number of tasks needs explicit library support.

**Scheduler-agnostic portability.** The Maxwell FDTD (finite-difference time-domain) benchmark in the [stdexec](https://github.com/NVIDIA/stdexec)<sup>[2]</sup> repository runs the same algorithm from one source on a CUDA GPU and on a CPU thread pool by swapping the scheduler.

These properties are strongest in GPU dispatch and heterogeneous scheduling, the domains for which `std::execution` was designed.

## 3. Four Transports, One Completion Model

Four APIs that move bytes across different hardware boundaries share a common async completion model:

**CUDA `cudaMemcpyAsync`.**<sup>[11]</sup> Bytes between host and device. Completion via callback, event query, or stream synchronization (Section 5).<sup>[12]</sup>

**NCCL (NVIDIA Collective Communications Library) `ncclAllReduce`.**<sup>[13]</sup> Bytes between GPUs over NVLink or InfiniBand. Completion via CUDA stream synchronization.

**RDMA `ibv_post_send`.**<sup>[14]</sup> Bytes between nodes. Completion via `ibv_comp_channel.fd` - a plain file descriptor that works with epoll, io_uring, or kqueue.

**TCP `read`/`write`.** Bytes between hosts. Completion via IOCP (I/O completion ports) or io_uring, readiness via epoll.

All four share the same structural pattern: submit a buffer of bytes, receive async completion via callback, poll, or file descriptor, receive a compound result (status plus byte count), and dispatch the result to the application thread via a reactor. The hardware boundaries differ - PCIe, NVLink, InfiniBand, Ethernet - and the abstract interface does not. Two of the four report the compound result natively (POSIX, RDMA). For CUDA and NCCL the wrapper synthesizes the byte count (Section 11). IoAwaitable handles all four with the same mechanism. Of the four, the accompanying code<sup>[15]</sup> implements the CUDA transport as an IoAwaitable (Sections 7 and 8); NCCL is driven through the same stream (Section 7); the TCP transport is Corosio's,<sup>[16]</sup> outside the pinned examples; and the RDMA transport is inferred from the shape of its API (Section 12) with no implementation in this paper. Section 8 demonstrates a protocol handler written against this interface, and Section 10 traces the ABI consequence.

The type vocabulary builds from this pattern:

The `IoAwaitable` concept requires `await_suspend(coroutine_handle<>, io_env const*)` - the execution environment flows into each operation at the suspension point. The concept is defined in [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup>.

The compound result type `io_result<std::size_t>` delivers both status and byte count via structured bindings:

```cpp
auto [ec, n] = co_await stream.write_some(buf);
```

`WriteStream` requires `write_some(buffers)` returning an `IoAwaitable` whose `await_resume` returns `io_result<std::size_t>`; the free algorithm `write(stream, buffers)` loops over it for complete-buffer writes. `ReadStream` is the mirror image with `read_some`.

The type-erased wrappers `any_read_stream` and `any_write_stream` wrap any `ReadStream` or `WriteStream` (respectively) behind a vtable of fixed per-operation signatures (Section 9 names the entries). The awaitable has a fixed, compile-time-known size, so the wrapper preallocates a single awaitable buffer at construction and reuses it for every operation. Section 9 explains why and analyzes the structural consequences, and Section 10 draws the ABI conclusion.

P2300R10<sup>[1]</sup> Section 4.15, where the awaited objects are senders, expects the same user-facing form: "we expect that coroutines and awaitables will be how a great many will choose to express their asynchronous code."

One completion model spans all four transports, and the type vocabulary above expresses it. 

## 4. The IoAwaitable Protocol

The IoAwaitable protocol from [Capy](https://github.com/cppalliance/capy)<sup>[17]</sup> extends the standard awaitable with an execution environment designed for I/O operations:

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

The `executor_ref`<sup>[19]</sup> is a type-erased executor with `dispatch(continuation&)` returning `coroutine_handle<>` for symmetric transfer<sup>[20]</sup>, and `post(continuation&)` for deferred execution. The `continuation`<sup>[21]</sup> type pairs the handle with one pointer-sized slot the executor uses to queue it without allocating:

```cpp
struct continuation
{
    std::coroutine_handle<> h;
    void* reserved = nullptr;
};
```

The slot is the executor's; it is overwritten on submission and carries no meaning afterward.

The `io_env` flows forward through `co_await` chains via `task`'s<sup>[22]</sup> `await_transform`, which wraps each child awaitable and passes the environment into its `await_suspend`. The critical difference from a hand-rolled awaitable: the awaitable knows which executor to resume on, carries a cancellation token, and has access to the frame allocator.

These three properties - executor affinity, cancellation, and frame allocation control - are the same concerns that `std::execution` addresses through a different mechanism. The IoAwaitable protocol provides them in a form designed for byte-oriented I/O, where type-erased streams and compound results are the natural vocabulary.

The full execution model built on this protocol is specified in [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup>. That paper defines the launch functions that connect coroutine chains to the rest of the program: `run_async` starts a coroutine from regular code (the topmost caller that cannot `co_await`), and `run` switches executor, stop token, or allocator for a subtask from within a coroutine. IoAwaitables are lazy - submission happens in `await_suspend`, not at construction. The two-phase invocation of launch functions ensures the frame allocator is cached before the child coroutine's frame is allocated. P4003R3 also demonstrates a `counting_scope` built from launch function handlers, providing spawn, cancel, and join-before-destruction - the same structured concurrency guarantees that `std::execution`'s `counting_scope` provides, expressed through the IoAwaitable protocol's own primitives.

Whether this forward-propagation model - where the execution environment flows into each awaitable via `await_suspend` - addresses the concerns GPU schedulers have about coroutine integration, and whether a GPU-aware awaitable needs properties beyond these three, are open questions the record does not yet settle.

## 5. GPU Completion Notification: Three Mechanisms, One Protocol

CUDA streams are in-order queues where operations execute sequentially.<sup>[23]</sup> When GPU work completes, the host needs notification. Three mechanisms exist, and the IoAwaitable protocol is independent of which one a given awaitable uses:

- **Polling**: a thread periodically calls `cudaStreamQuery`.<sup>[24]</sup> The polling can be implemented with a dedicated thread, but it can also be integrated into an existing work loop by interleaving completion checks with other work items. This avoids blocking threads, but requires periodic polling activity.
- **Deferred synchronization**: a service thread runs the blocking `cudaStreamSynchronize`.<sup>[24]</sup> Costs one parked thread per outstanding wait, but keeps the worker threads free.
- **Callback**: `cudaLaunchHostFunc` enqueues a host function into the stream.<sup>[12]</sup> No busy-wait, and the simplest to wire up because it needs no service thread, but the host function receives no completion status, and the CERN measurements below find it scales less well than the other two as worker threads are added. One plausible mechanism, offered by an NVIDIA forum responder,<sup>[25]</sup> is that a single CUDA-internal worker services every callback across all streams; NVIDIA could not reproduce the reported latency on other GPUs, and the mechanism is unconfirmed.

`cudaLaunchHostFunc` is the recommended replacement for `cudaStreamAddCallback`, which is slated for deprecation.<sup>[23]</sup> Its host function fires on a dedicated internal CPU thread created by the CUDA driver, not the application thread.<sup>[26]</sup><sup>[27]</sup> It cannot call CUDA APIs and must not create transitive dependencies on outstanding CUDA work.

For cases where waiting for the entire stream is too coarse, CUDA events provide finer-grained completion points. An event can be recorded at a specific position in a stream, and the host can then wait for that event instead of the entire stream. The same polling and blocking approaches apply: `cudaEventQuery` can be used to poll event completion, and `cudaEventSynchronize` can be used to block until the event is complete.<sup>[28]</sup> Unlike streams, events do not support callback-based notification.

Among the three, the choice is a scaling tradeoff. All three satisfy `IoAwaitable` and, driving the same GPU pipeline, produce identical results at runtime, which the accompanying notification-strategies example<sup>[15]</sup> demonstrates directly. The slides of a CERN Next Generation Triggers contribution<sup>[29]</sup> state (slide 12) that "All the handlers can be implemented with any async model", that "For CUDA, callback is easy to implement but doesn't scale as good as other handlers", that "Impact depends on the workload", and that "Polling and deferred synchronization are good alternatives for multi-threaded jobs". In a multi-threaded framework, prefer polling or deferred synchronization. Use the callback for its simplicity in low-concurrency settings.

This is the same structural pattern as epoll readiness events or IOCP and io_uring completions arriving on arbitrary threads. In all cases, an async operation completes on a thread that is not the application's, and the application must dispatch the result to the correct execution context. This is the exact problem that Capy's executor-affinity dispatch was designed to solve.

Each mechanism is a distinct `await_suspend` over the same protocol. The listings below are adapted from the accompanying notification-strategies example,<sup>[15]</sup> which compiles and runs, with locals and comments condensed. Trimmed to the suspension point, the three awaitables differ only in how they arrange for the continuation to be posted back through `env->executor`:

```cpp
// Callback: a CUDA host function re-posts through the executor.
std::coroutine_handle<>
callback_awaitable::await_suspend(
    std::coroutine_handle<> h, io_env const* env)
{
    cont_.h = h;
    ctx_ = resume_ctx{env->executor, &cont_, &ec_};
    if (auto err = cudaLaunchHostFunc(stream, &on_complete, &ctx_);
        err != cudaSuccess)
    {
        ec_ = make_cuda_error(err);
        return h;                  // Could not register; resume inline.
    }
    return std::noop_coroutine();
}
// The on_complete callback runs ctx->ex.post(*ctx->cont). The host
// function receives no status, so await_resume calls cudaStreamQuery
// back on the worker thread to recover a stream fault.

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

The remainder of this paper uses the callback mechanism as the running example because it is the simplest to present. The complete polling and deferred-synchronization awaitables are in the accompanying example.<sup>[15]</sup> The mechanism is a parameter of the awaitable. Across all three, the protocol and the calling code are identical.

## 6. Hand-Rolled Awaitables Lose the Execution Environment

Strip the execution environment from Section 5's callback awaitable and what remains is the simplest possible integration - and a demonstration of why the environment exists:

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

This compiles and resumes. But `resume()` executes on the CUDA driver callback thread, where the CUDA Runtime API documentation<sup>[12]</sup> forbids CUDA calls, so any continuation that touches CUDA violates the host-function contract. There is no executor affinity, no cancellation support, and no frame allocation control. The coroutine's continuation runs on whatever thread the CUDA driver chose, which may not be safe for application logic that touches shared state.

## 7. `cuda_stream`: Data Movement as IoAwaitables

The `cuda_stream` class wraps a CUDA stream handle and provides data-movement member functions that return IoAwaitables. It follows the Rule of Five (copy deleted, move implemented, null-guarded destructor). The helper function `make_cuda_error`, defined by the accompanying demonstration<sup>[15]</sup> rather than by Capy, converts a `cudaError_t` to `std::error_code` via a CUDA error category.

The key mechanism is `resume_ctx`: a pre-allocated member that captures the executor and continuation for `cudaLaunchHostFunc`. The `on_complete` callback posts the continuation back to the application's executor, providing the executor-affinity dispatch that the hand-rolled awaitable in Section 6 lacks. Because the host function receives no completion status, `await_resume` calls `stream_error`, a helper that wraps `cudaStreamQuery` and maps anything other than `cudaSuccess` or `cudaErrorNotReady` to a `std::error_code`; the query runs on the worker thread, where CUDA calls are permitted. Of the three properties the protocol carries, these awaitables implement executor affinity and inherit frame allocation from `task`; none reads `env->stop_token`, because CUDA offers no way to abort a transfer once `cudaMemcpyAsync` has enqueued it, so cancellation of an in-flight GPU transfer is not expressible on this transport.

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
                if (!self->error_)
                    self->error_ = stream_error(
                        self->stream_);
                if (self->error_)
                    throw std::system_error(
                        std::exchange(
                            self->error_, {}));
            }
        };
        return awaitable{
            this, dst, src, count};
    }

    auto memcpy_d2h(
        void* dst, void const* src,
        std::size_t count);
        // Same pattern, cudaMemcpyDeviceToHost.

    auto synchronize();
        // cudaLaunchHostFunc only (no preceding op).
};
```

The `resume_ctx` lives inside `cuda_stream` as a pre-allocated member, so no per-operation heap allocation occurs. This is safe under a single-owner discipline, which is a precondition rather than a consequence of suspension: one coroutine owns the `cuda_stream`, and because that coroutine suspends on each `co_await`, only one operation is in flight at a time. Two coroutines sharing a `cuda_stream` would race on the pre-allocated state. In the networking domain, the same contract governs Corosio's sockets and their pre-allocated op states. The CUDA Programming Guide<sup>[23]</sup> confirms that operations in a stream execute in enqueue order, and the CUDA Runtime API documentation<sup>[12]</sup> states that `cudaLaunchHostFunc` callbacks block later work in the stream until they return; an NVIDIA engineer's Stack Overflow answer<sup>[30]</sup> adds that host functions in independent streams may also be serialized, in undefined order. Under the discipline, the pre-allocated `resume_ctx` is never accessed concurrently.

The discipline has a cost in the GPU domain that the networking domain does not pay, and it is a cost of continuing on the host rather than of coroutines. A CUDA stream is a queue, and its throughput comes from depth: the host enqueues several operations and runs ahead while the device drains them. A coroutine that awaits each transfer separately drains the stream to empty between transfers, so a single owner never has more than one operation queued, and under the callback mechanism `cudaLaunchHostFunc` blocks any later work in the stream until the host function returns.<sup>[12]</sup> The `WriteStream` contract already carries the remedy: `write_some` takes a buffer sequence and may transfer any prefix of it, so the `cuda_device_stream` listing in Section 8 enqueues every buffer as its own `cudaMemcpyAsync`, follows the last with one host function, and suspends once per call, the GPU form of a gather write on a socket. A static burst is therefore one buffer sequence, not a loop of awaits; the NCCL and CUDA Graphs listings<sup>[15]</sup> reach the same depth for raw stream work by enqueuing through `native_handle()` and awaiting one `synchronize()`.

The same drain applies to senders whenever a receiver runs host code. nvexec's stream scheduler enqueues a static chain of `then` and `bulk` stages onto the stream in one pass, each stage as a kernel, and the stream stays deep; at a `let_value`, where the host must run the user's function to obtain the next sender, it calls `cudaStreamSynchronize` and the stream drains.<sup>[10]</sup> For byte-oriented data movement, where the neighbouring steps are host I/O, both models drain at the same points and recover depth the same way: enqueue the burst, notify once. For a static burst, an nvexec chain and a batched awaitable put the same work in the stream with the same single completion; the sender's advantage is composing device-side stages as callables, which belongs to dispatch, and the awaitable's is that the single completion suspends the coroutine where `sync_wait` blocks the thread. Per-transfer awaiting remains the form for data-dependent sequences, where the next transfer cannot be enqueued until the host has seen the last result and every model drains the stream at that point. The trade in the batched form is one status for the batch instead of one per buffer: a fault in the middle surfaces as the stream's sticky error at resumption, without naming the buffer. Overlap between independent work comes from multiple streams (Section 18.5).

`cudaLaunchHostFunc` has documented constraints that production code must respect. The callback must not call CUDA APIs or synchronize on outstanding CUDA work.<sup>[12]</sup> One user reported latency spikes of up to 12ms between callback completion and stream resumption on A100 and H100 systems with CUDA 12.6, and the NVIDIA responder, unable to reproduce them, suggested OS starvation of the CUDA-created callback thread as one explanation;<sup>[25]</sup> whether a single such thread services every stream is the unconfirmed mechanism of Section 5. The 12ms figure is a single user report on A100 and H100 with CUDA 12.6; the reporter supplied a reproducer, and the NVIDIA responder, who had tentatively attributed the spikes to serialization on a single CUDA-created thread, ran it on an L4 (CUDA 12.2) and an A40 (CUDA 12.8.1) and observed no variability, so the cause is unexplained. If the callback blocks on a user lock while the CUDA launch queue is full, the enqueuing thread blocks too, producing deadlock.<sup>[31]</sup> Notification is unidirectional: `cudaLaunchHostFunc` provides stream-to-CPU notification only and cannot make the stream wait for a CPU-side signal.<sup>[32]</sup>

The host function also receives no completion status. `cudaHostFn_t` takes only a `void*`, where the older `cudaStreamCallback_t` received a `cudaError_t`, and the documentation states the function is not called at all after an error in the CUDA context.<sup>[12]</sup> A callback-based awaitable therefore cannot see a stream fault from inside the callback. The accompanying notification-strategies example<sup>[15]</sup> probes this with a `--fault` mode that launches a null-pointer kernel. On the test system (an RTX 4060, CUDA 13.3) the host function still fired, and before the `cudaStreamQuery` in `await_resume` was added the coroutine resumed with success; the polling and deferred-synchronization awaitables reported `cudaErrorIllegalAddress`, because `cudaEventQuery` and `cudaStreamSynchronize` return the status. With the query in place all three report the fault.

These constraints apply equally to any pattern that uses `cudaLaunchHostFunc` for completion notification, including the hand-rolled awaitable in Section 6 and any sender-based wrapper that uses the same mechanism. They do not invalidate the pattern but they bound its applicability in high-throughput pipelines. The scaling, deadlock, and missing-status constraints are specific to the callback mechanism, and the polling and deferred-synchronization awaitables of Section 5 sidestep them. Unidirectional notification is a property of GPU-to-host completion generally. CERN's open traccc port<sup>[33]</sup> implements a callback, event polling, and two deferred-synchronization variants (event and stream) behind one selector, the callback as an IoAwaitable and the others as tasks moved onto a service executor (Section 14), allowing the notification mechanism to be selected per deployment, and the CHEP 2026 slides<sup>[29]</sup> report that the callback scales less well than polling and deferred synchronization as worker threads are added (Section 5).

One caveat: `cudaMemcpyAsync` is only truly asynchronous with pinned (page-locked) memory.<sup>[34]</sup> With pageable memory allocated via `malloc` or `new`, the call may block the host thread despite the `Async` suffix.<sup>[35]</sup> For multi-gigabyte model weight transfers, this distinction matters.

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

## 8. `cuda_device_stream`: GPU Memory as a WriteStream

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

    // a buffer sequence is one batch: every
    // buffer is enqueued, one host function
    // follows the last, the coroutine suspends
    // once; each transfer completes in full or
    // fails with an error
    template<ConstBufferSequence Buffers>
    auto write_some(Buffers buffers)
    {
        struct awaitable
        {
            cuda_device_stream* self;
            Buffers buffers;
            std::size_t total = 0;

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
                auto const end =
                    capy::end(buffers);
                for (auto it = capy::begin(buffers);
                     it != end; ++it)
                {
                    const_buffer b = *it;
                    auto err = cudaMemcpyAsync(
                        self->d_ptr_ +
                            self->offset_ + total,
                        b.data(), b.size(),
                        cudaMemcpyHostToDevice,
                        self->stream_);
                    if (err != cudaSuccess)
                    {
                        self->error_ =
                            make_cuda_error(err);
                        return h;
                    }
                    total += b.size();
                }
                self->cont_.h = h;
                self->ctx_ = resume_ctx{
                    env->executor,
                    &self->cont_};
                auto err = cudaLaunchHostFunc(
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
                if (!self->error_)
                    self->error_ = stream_error(
                        self->stream_);
                if (self->error_)
                    return {std::exchange(
                        self->error_, {}), 0};
                self->offset_ += total;
                return {{}, total};
            }
        };
        return awaitable{this,
            std::move(buffers)};
    }
};
```

`cuda_device_stream` satisfies `WriteStream`. Each `write_some` call transfers the whole buffer sequence as one batch - a prefix of the sequence, which is the standard `write_some` contract - enqueuing one `cudaMemcpyAsync` per buffer and one host function after the last, so the stream keeps its queue depth and the coroutine suspends once per call (Section 7); each `cudaMemcpyAsync` either transfers its buffer in full or fails with an error. It can be wrapped in `any_write_stream`.

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

The `ingest` handler is compiled once against both `cuda_device_stream` and an in-memory `WriteStream` in the accompanying demonstration.<sup>[15]</sup> That demonstration is build-only. The accompanying batched-write example<sup>[15]</sup> runs the same `cuda_device_stream`: it gathers three host buffers through `any_write_stream` in a single `write_some`, awaits once, and checks that the device holds their concatenation (RTX 4060, CUDA 13.3, clang 22). The TCP leg is the same pattern over Corosio's socket streams and is not part of the demonstration.

The algorithm in `protocol.cpp` is compiled once. At link time, swap the transport. No recompilation. Zero per-operation allocation in all cases, by the fixed-size-awaitable mechanism of Section 9. Section 10 traces the design lineage and the ABI consequence.

## 9. The Type Erasure Asymmetry

The link-time polymorphism shown in Section 8 is a structural property of how the two models interact with the type system.

**Awaitable under type erasure.** `await_suspend` takes `coroutine_handle<>` - type-erased by the language itself. The awaitable has a fixed, compile-time-known size. At construction, the type-erased wrapper preallocates one awaitable buffer and placement-constructs each operation into it. Its per-operation vtable entries - `await_ready`, `await_suspend`, `await_resume`, `destroy_awaitable` - have fixed signatures. Result: zero per-operation allocation, even through a virtual stream interface.

**Sender under type erasure.** `connect(sender, receiver)` produces an operation state whose type depends on both the sender and the receiver. Under type erasure (`any_sender`), the receiver's type is unknown at compile time. The operation state's size is unknown. The coroutine frame cannot absorb it. `any_sender::connect` must heap-allocate.<sup>[7]</sup> stdexec mitigates this with a 64-byte small buffer optimization,<sup>[36]</sup> and measurement shows the buffer is exceeded. For `starts_on(sched, just(42))` connected through `exec::any_sender` and `exec::any_receiver`, `connect` performs one heap allocation in every case and `start` performs none: 112 bytes (clang 22.1.8) or 128 bytes (GCC 16.1.1) with `stdexec::inline_scheduler`, and 192 or 200 bytes with `exec::static_thread_pool::scheduler`. The erased operation state itself is a fixed 88 bytes on both compilers; the connected pipeline it points to is what exceeds the buffer.

The measurement is the accompanying `any-sender-size` example<sup>[15]</sup> against stdexec commit 307b83c5 (2026-05-18), x86-64 Linux, CMake Release configuration, counting calls to the replaceable `operator new`; the concrete, non-erased operation state for the same pipeline is 88-176 bytes and allocates nothing. The measurement, Table 1, and P4123R0<sup>[7]</sup> are all the author's own; a delegate who discounts them can reach the allocation from stdexec's source alone, since `any_sender_of.hpp` fixes the inline buffer at 64 bytes and `sizeof` the concrete `starts_on` operation state exceeds it on both compilers.

Table 1 reproduces P4088R1's<sup>[5]</sup> per-operation time and heap allocations for native and type-erased stream reads, 100 million `read_some` calls on a single thread. The measurements are that paper's, and its setup section documents them; they were not re-run for this revision.

| Stream type | Coroutine (Capy) | Sender pipeline |
|---|---|---|
| Native | 31.4 ns/op, 0 alloc/op | 30.0 ns/op, 0 alloc/op |
| Type-erased | 36.4 ns/op, **0 alloc/op** | 53.4 ns/op, **1 alloc/op** |

Native performance is comparable - 30.0 ns vs 31.4 ns, a 1.4 ns difference. Under type erasure the two paths separate: the coroutine path stays at 36.4 ns with zero allocations, while the sender path rises to 53.4 ns and incurs one heap allocation per operation. The 17 ns gap and the per-operation allocation are structural, following from how each model interacts with type erasure.

The same asymmetry applies to any byte-oriented operation that goes through a type-erased interface - GPU memory transfers, network sockets, RDMA queue pairs. For domains where type erasure is the natural interface (a protocol compiled once, linked against any conforming transport), the coroutine model has a structural advantage.

This asymmetry also determines which model can provide a stable binary interface for I/O. Section 10 takes it up.

## 10. ABI Stability as a Structural Consequence

The type erasure asymmetry in Section 9 has a further consequence, an ABI-stable interface for async I/O.

The fixed vtable of Section 9 is what makes the interface a stable boundary. The signature `await_suspend(coroutine_handle<>, io_env const*)` is fixed because `coroutine_handle<>` is type-erased by the language itself. Awaitable size and vtable layout are known at compile time, so the interface can be compiled into a shared library (`.so`/`.dll`) and the implementation swapped without recompiling the consumer.

Sender pipelines provide this only at the cost the previous section measured. Without type erasure, `connect(sender, receiver)` produces an operation state whose type and size depend on both the sender and the receiver. Every new combination is a new type - a new ABI surface - and changing the I/O implementation forces recompilation of every consumer. With type erasure (`any_sender`), the boundary becomes fixed but every operation heap-allocates (Section 9).

This ABI stability costs one type-erasing wrapper per stream concept - `any_write_stream` is a vtable with four per-operation entries and a preallocated awaitable buffer - and no policy constraint, because the language provides the fixed-type boundary in `coroutine_handle<>`. The boundary passes `io_env const*`, whose layout depends on `std::stop_token` and `std::pmr::memory_resource*`, so the stability holds within one standard library and compiler ABI, not across them. Three consequences follow: a design lineage (the abstraction arc), a maintenance property (security patching), and a deployment story (the inference stack).

### The abstraction arc

The interface/implementation split follows the design trajectory of Thrust and the C++17 parallel algorithms - a standard interface over hardware-specific implementation. The precedent covers the interface, not the ABI: both precedents are compile-time template interfaces with no stable binary boundary. What this design adds is the fixed vtable.

**Thrust (2009).** GPU parallel algorithms behind an STL-compatible interface. Customers wrote to the STL vocabulary, ran on NVIDIA's GPU. The interface was vendor-neutral: customers could retarget to TBB or OpenMP. N3408 (2012) carried this into C++17 parallel algorithms.<sup>[37]</sup>

**C++17 parallel algorithms.** Standard interface, hardware-specific implementation. Write `std::sort(std::execution::par, ...)`, link against NVIDIA's implementation or Intel's. The standard owns the interface, and the vendor owns the implementation.

**IoAwaitable streams.** Write `ingest(any_write_stream&, payload)`, link against the compile-validated `cuda_device_stream`, a TCP socket, or - hypothetically today - a ROCm or RDMA transport written to the same concepts. Same pattern, applied to data transport instead of parallel algorithms. The abstraction level rises again, and the application code stays the same. Section 8 describes the demonstration<sup>[15]</sup> of this pattern.

### Security patching without recompilation

The ABI-stable boundary means a TLS (Transport Layer Security) stream implementation can be upgraded for a security patch - or swapped out for a different implementation entirely - without recompiling the application. The protocol handler was compiled against `any_write_stream`. Behind that interface sits the TLS implementation. Replace the shared library, restart the process.

At `connect`, a non-erased sender pipeline stamps both types into the operation state, so changing the TLS implementation changes the type and with it the ABI. The sender route to the same property through `any_sender` incurs the per-operation allocation of Section 9. A library could instead ship a fixed sender type whose operation state is instantiated in the consumer and which reaches its implementation through a vtable with a type-erased completion; that is the awaitable's own mechanism restated on the sender side, and it is unmeasured here. The asymmetry measured here is between `any_sender` and `any_write_stream`, not between the two models in the abstract.

### The complete inference stack

An inference server receives HTTP requests (TCP transport), dispatches to GPU compute (`stdexec` scheduler), moves results through NVLink or InfiniBand (NCCL/RDMA transport), and responds over HTTP. Today, no C++ standard interface covers the data-transport layer. IoAwaitable's ABI-stable streams complete the stack. The protocol handler compiles once and, given a conforming transport for each link, would deploy across the full topology - PCIe, NVLink, InfiniBand, Ethernet - without recompilation; the CUDA and TCP transports exist, the NCCL and RDMA ones are projected. The data-transport layer of that stack is the one the fixed vtable makes ABI-stable.

## 11. Partial Success Requires a Compound Result

Byte-oriented operations deliver results as a compound pair, status plus byte count, and the pattern spans hardware boundaries. A POSIX `read` returns `(errno, bytes_read)`. An RDMA work completion returns `(wr_id, status, byte_len)`. CUDA and NCCL report only a status at completion: the transfer count is the caller's own argument, which the IoAwaitable wrapper echoes back, and the transfer either completes in full or fails (Section 8). Where partial success is native, both values are always present and the byte count is not redundant with the error code: a `read` that returns 0 bytes with no error means EOF, and a `read` that returns `ECONNRESET` with 47 bytes means 47 bytes arrived before the peer reset the connection.

P2300R10<sup>[1]</sup> Section 4.14, titled "Senders can represent partial success," poses this directly: "This begs the question of how they can be used to represent async operations that partially succeed." P2300R10 answers it, for the socket-read case, by passing both the error code and the result through the value channel. The same section notes that bundling an error with an incomplete result and sending it through the error channel "makes more sense" in other cases, and offers a range of senders as a third form. The cost of the first answer is what the rest of this section examines.

The sender model provides three completion channels: `set_value`, `set_error`, and `set_stopped`. A compound I/O result must be routed to one of them:

- Route both values through `set_value`: downstream `upon_error` and `retry` algorithms cannot see the error.
- Route the error through `set_error`: the byte count is lost.
- Route through `set_stopped`: both values are lost.

The best available option is routing both through `set_value` as a compound type. But this means I/O errors bypass the `set_error` channel, disadvantaging sender algorithms that operate on error and stopped channels. P4091R1<sup>[6]</sup> documents all six positions that have been proposed. Each carries a cost.

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

This is a domain mismatch. The three-channel model was designed for operations that succeed, fail, or are cancelled - a natural fit for GPU kernel dispatch, where `cudaErrorLaunchFailure` is fatal and carries no partial result. Where partial success is native - POSIX and RDMA - both the status and the byte count must reach the application, and the cost argument above applies. For CUDA and NCCL the compound result is uniformity rather than information: the transfer completes or fails, and the three channels fit those two transports as well as they fit kernel dispatch.

## 12. HPC Networking Plans at Runtime

The sender model's compile-time pipeline visibility eliminates virtual dispatch and heap allocation - costs on the order of tens of nanoseconds per operation (Table 3 lists 30-60 ns for a malloc-backed frame). These are real costs in nanosecond-scale GPU kernel dispatch. This section shows that the planning decisions in HPC networking - topology, path selection, completion handling - are made at runtime by the libraries themselves, so compile-time pipeline visibility has no planning decision to inform there.

HPC networking APIs use runtime completion models. The signatures below are existing library calls, reproduced from their public headers; the accompanying `fabrics` example<sup>[15]</sup> compiles the libibverbs, libfabric, and UCX ones where those libraries are found.

```c
// NCCL: CUDA stream completion
ncclAllReduce(send, recv, count,
    type, op, comm, stream);

// UCX: callback from progress engine
ucp_tag_send_nbx(ep, buffer, length,
    tag, &param);

// NVSHMEM: GPU-initiated put with fence
nvshmem_int_put(dest, src, count,
    target_pe);

// libfabric: completion queue poll
fi_send(ep, buffer, len, desc,
    dest_addr, &context);

// libibverbs: completion channel fd
ibv_post_send(qp, &wr, &bad_wr);
```

Five libraries, five different async models: streams, callbacks, GPU-initiated operations, completion queues, and file-descriptor-based reactor patterns. None of the five builds a compile-time work graph. These are the communication layers used in large-scale GPU training, weather simulation, and molecular dynamics.

Planning decisions in HPC networking are runtime:

- **Topology discovery** happens at communicator creation via `ncclCommInitRank`.<sup>[13]</sup> NCCL discovers NVLink/NVSwitch/InfiniBand topology and selects ring vs tree algorithms, chooses transports, and builds channel structures. These decisions are driven by hardware probing rather than compile-time type information.
- **Compute/communication overlap** is expressed through CUDA stream dependencies via `cudaEventRecord` and `cudaStreamWaitEvent`.<sup>[28]</sup> The scheduler does not need to see the type of the collective to overlap it with compute. It needs the data dependency, captured by the event.
- **Memory registration** is setup-time: `ibv_reg_mr` pins pages, maps GPU base address register (BAR) regions, and exchanges rkeys with peers.<sup>[14]</sup> All done before the first byte moves.

The RDMA completion channel exposes a plain file descriptor (`ibv_comp_channel.fd`) that works with epoll - the same reactor pattern as TCP sockets. The work completion returns `(wr_id, status, byte_len)`, the same compound result pattern, and the `wr_id` is a natural coroutine dispatch key.

The stdexec repository focuses on compute scheduling. HPC networking integration is not yet represented; at commit 307b83c5 no example performs real network I/O as senders, and the `server_theme` example wraps a stub socket read in `then`. The same commit ships `exec/linux/io_uring_context.hpp`, a sender-based io_uring context used in the examples for timers only. Coroutine-based integration could complement stdexec here: NCCL, RDMA, and NVLink all use runtime completion models (streams, callbacks, file descriptors) that map naturally to the IoAwaitable pattern, providing the data-movement layer that compute scheduling sits on top of.

In active development, the closest project to sender-based HPC networking is LCI (Lightweight Communication Interface), a C++17 async communication library with libibverbs and libfabric backends, host-initiated GPU-Direct RDMA, and prototype device-initiated operations, published at SC'25.<sup>[38]</sup> The LCI paper documents its integration with the HPX runtime as an RDMA transport layer. This is sender-adjacent HPC networking through a runtime wrapper rather than direct sender composition over the wire protocol, but it suggests the space is being explored.

Whether any per-operation planning decision in HPC networking benefits from compile-time type visibility of the send and receive calls themselves remains an open question. For communication patterns known at compile time, the answer may be yes. For data-dependent communication patterns determined at runtime, the record shows no example.

## 13. Sender-Based Networking: Deployed Evidence

At scale, the sender/receiver model has been deployed for compute scheduling and infrastructure (Section 2). This section surveys whether it has been deployed for byte-oriented data movement, the domain this paper examines.

Meta uses the sender/receiver model internally through libunifex. Its published guidance to adopting teams, from GitHub issue #586<sup>[39]</sup> (December 2023):

> "Our experience at Meta has been that coroutines are easier to read, write, debug, and just generally maintain than composition-of-sender algorithms-style code. The cost of that ease is basically overhead; coroutines don't optimize as well as raw senders (either for size or speed). The advice we give to internal teams adopting Unifex is that they should prefer coroutines until they know that the overheads are unacceptable, at which point they can refactor to the lower-level abstraction of raw senders."

In libunifex, coroutines consume senders, so the guidance concerns the authoring surface on top of a sender substrate: the team that maintains libunifex directs that surface to coroutines for the common case. The cited comment does not say where or at what scale libunifex is deployed, nor whether that use includes byte-oriented networking of the kind this section surveys. It is sender implementation experience, with its data-movement domain unresolved.

Table 2 lists the sender-based networking projects outside Meta that the survey found, with each project's foundation, status, and repository creation year and last push date as of August 2026:

| Project | Built on | Status | Created / last push |
|---|---|---|---|
| uring_exec<sup>[40]</sup> | io_uring + stdexec | Single-developer echo server | 2024 / 2026-05 |
| execution-ucx<sup>[41]</sup> | UCX + libunifex | RDMA/RPC with CUDA device-memory (GPU-Direct RDMA) support, not on stdexec | 2025 / 2026-05 |
| beman.net<sup>[42]</sup> | P2762R2<sup>[43]</sup> + beman.execution | "not yet ready for production use" | 2024 / 2026-08 |
| senders-io<sup>[44]</sup> | stdexec | Experimental I/O and networking adaptation | 2023 / 2025-04 |
| kuhllib<sup>[45]</sup> | Custom senders | Conference demo | 2012 / 2024-04 |
| snp<sup>[46]</sup> | libunifex + Boost | Inactive since August 2023 | 2023 / 2023-08 |
| Asio adapter PR<sup>[47]</sup> | stdexec PR #1501 | Closed unmerged | 2025-03 / 2025-03 |

None are production-grade. The most complete (uring_exec) is a single developer's project with a TCP echo server. P2300R10<sup>[1]</sup> presents its HTTP server examples at a level that, in its own words (Section 1.7), "ignore the low-level details of the HTTP server".

P4029R0 records the position of SG14, the study group for low-latency systems practitioners ([P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf)<sup>[4]</sup> Section 2): "SG14 advise that Networking (SG4) should not be built on top of P2300."

The survey found no production-grade sender-based networking - its search method was not recorded and its recall is bounded by the public record it reached (Section 18.5) - and the SG14 chair's priority paper, written with SG14 as contributor, advises against building networking on P2300R10.<sup>[1]</sup> Section 14 turns to what the coroutine side of the record shows.

## 14. Seven Projects, Six Independent Designs; CERN Has an Open Port

Seven projects have arrived at the same design - coroutine-based suspension on GPU and HPC work - six by independent design and one (Loom) by adoption, and an eighth, CERN's Next Generation Triggers project, has an open pull request porting a track-reconstruction pipeline onto the IoAwaitable protocol itself. The notification mechanism that bridges GPU completion to coroutine resumption varies - a host-function callback (`cudaLaunchHostFunc`, or its driver-level equivalent `cuLaunchHostFunc`), event or stream polling, or deferred synchronization. Suspension on GPU or RDMA work is common to all of them. cuda-oxide, Taro, rdmapp, and the CERN port document the completion bridge; Desmond, async-cuda, and TTG document suspension on GPU work without documenting the bridge, or with a different one (async-cuda drives the GPU from a single runtime thread). Where a project documents a single bridge (cuda-oxide, Taro), it is the callback, the simplest to wire up, and it inherits the missing-status limitation of Section 7. CERN's port implements all three, with deferred synchronization in two variants.

**cuda-oxide (NVIDIA Labs, Rust; project page undated).**<sup>[48]</sup> NVIDIA's own research lab implemented the same mechanism in Rust. Their `DeviceFuture` submits GPU work, enqueues a `cuLaunchHostFunc` callback that sets an `AtomicBool` and wakes an `AtomicWaker`, and the async runtime resumes the task on the next poll. Zero busy-wait. The three-state machine (Idle, Executing, Complete) is structurally identical to a network socket future. The vendor's own research lab reached the same `cudaLaunchHostFunc`-to-async-runtime pattern independently, in a different language.

**CERN wp1.7-traccc (adoption).**<sup>[33]</sup> As part of its evaluation of C++20 coroutines for task scheduling, the CERN Next Generation Triggers project has an open pull request (opened 2026-04-20) porting the traccc GPU track-reconstruction pipeline - research code rather than production - onto Capy. This is an outside team adopting the published protocol, evidence of a different kind: the protocol as published is usable by a team that did not design it. Because it cuts the other way, the sibling work is recorded here: the same repository carries a parallel, also open, port of the same layer onto stdexec, so it is sender implementation experience as well. The Capy pull request is branched from the stdexec one; its description reads "Builds on top of #16 but replaces the stdexec implementation of coroutines and related utilities with Boost.Capy" and notes that "Some of the tests don't compile as they weren't ported to Capy yet". Measured against its base branch `develop`, the diff removes no stdexec code and three tests still include stdexec headers. Neither pull request states the team's reasons for either port, and they are left unstated here. The team's CHEP 2026 summary<sup>[29]</sup> reports (slide 16) "The same performance with C++20 coroutines, C++26 senders/receivers and TBB suspension" and that "coroutines and senders/receivers appear to be the desired models despite the higher investment required"; the scaling difference it reports is between notification mechanisms, not between the two async models.

The Capy port implements its CUDA completion strategies behind a single `await_strategy` selector with four suspending values: a `cudaLaunchHostFunc` callback, event polling, deferred event synchronization, and deferred stream synchronization (plus two non-suspending synchronous values). The callback strategy is an IoAwaitable whose `await_suspend(std::coroutine_handle<>, boost::capy::io_env const*)` posts the coroutine handle back to `env->executor` from the host function; polling is a `task<void>` that re-posts itself through a small `retry` awaitable of the same signature until the event is ready, and the two deferred strategies are blocking synchronization coroutines; all three non-callback strategies are moved onto a service executor with `boost::capy::run`. All four are selected through the same `task`-based interface. That a real reconstruction workload implements all three notification mechanisms behind one selector is the most concrete evidence in this survey that the coroutine model is not bound to the callback.

**Taro (University of Wisconsin-Madison; repository created 2023, last push 2024-02).**<sup>[49]</sup> A C++20 coroutine task-graph system for CPU-GPU workloads. GPU tasks suspend the CPU thread via coroutines when waiting for GPU completion, allowing other tasks to run. Uses `cudaLaunchHostFunc` for the callback. Published at Euro-Par 2024 (as TaroRTL)<sup>[50]</sup> and presented at CppCon 2023. TaroRTL reported a 40-80% speedup over RTLflow, a state-of-the-art GPU-accelerated register-transfer-level (RTL) simulator.

**async-cuda (Oddity AI, Rust; created 2023, last push 2026-06).**<sup>[51]</sup> A library (its README marks it work-in-progress) whose authors state, in the project README: "Since the GPU is just another I/O device (from the point of view of your program), the async model actually fits surprisingly well."

**Schr&ouml;dinger Desmond (production, GTC 2024).**<sup>[52]</sup> The Desmond molecular dynamics engine uses C++ coroutines to overlap multiple GPU simulations. Coroutines suspend when a simulation hits a serial bottleneck, allowing another simulation to use the GPU. Presented at GTC 2024. Achieved up to 2.02x speedup in FEP+ (free energy perturbation) drug discovery workloads. The NVIDIA developer-blog account<sup>[52]</sup> describes the approach as "improving GPU utilization without complex code restructuring".

**TTG/PaRSEC (TESSE/EPEXA; created 2016, last push 2026-05).**<sup>[53]</sup> A template task graph framework where `co_await ttg::device::select(...)` and `co_await ttg::device::wait(...)` are the primary mechanism for GPU task dispatch. Supports CUDA, HIP/ROCm, and Intel Level Zero. The project's README states that "the use of coroutines is the primary reason why TTG requires C++20 support by the C++ compiler".

**RDMA coroutine libraries.** Three projects put coroutines over RDMA verbs, with differing degrees of design independence and one falling outside the awaitable design: RDMA++ (rdmapp)<sup>[54]</sup> (created 2022, last push 2026-08) wraps libibverbs with C++20 coroutines, completing operations from a completion-queue polling thread; Loom<sup>[55]</sup> (created 2026-01, last push 2026-01) provides C++23 typed bindings over libfabric with `co_await ep.async_receive(buf, asio::use_awaitable)`, adopting Asio's completion model rather than designing one; and FORD<sup>[56]</sup> (USENIX FAST 2022; repository last push 2024-06) implements coroutine-enabled distributed transactions over one-sided RDMA. FORD's README lists Boost.Coroutine and Boost.Context as dependencies, so its coroutines are stackful user-level coroutines rather than C++20 awaitables; it shares the latency-hiding idea and not the awaitable design, and is not counted below.

These projects span GPU compute, molecular dynamics, high-energy physics, RDMA networking, and distributed systems, and they range in maturity: Desmond ships in production, cuda-oxide and the CERN work are research code, and Taro and the RDMA libraries are academic or single-developer projects. Judged by the deployment standard Section 13 applies to sender networking, this survey too contains exactly one production system, and that system, Desmond, is orchestration rather than data movement. For byte-oriented data movement specifically, neither survey found a production system, and the one sender-side project that moves bytes into GPU memory, execution-ucx, is a libunifex library with no deployment claim; the count is zero on both sides.

The convergence claim is about independent design choice rather than deployment success. The seven converging projects were built by independent teams with no coordination. By that same standard, the seven sender-networking projects of Table 2 are also independent teams choosing one model without coordination. The difference the record supports is narrower than a count: every Table 2 project is C++ code built on a WG21 paper, whereas two of the seven coroutine projects are Rust code with no sender alternative and one is the GPU vendor's own research lab, so the coroutine convergence includes designs reached outside the C++ debate. Two caveats bound what the convergence shows: the two Rust projects had no sender alternative in their language, and Taro (presented 2023) predates a usable `std::execution`, so part of the convergence reflects what was available. And three of these projects (Taro, TTG/PaRSEC, Desmond) extend the coroutine pattern to kernel dispatch and GPU pipeline orchestration, placing that evidence in the record independently of the examples here. That three of the seven operate in the dispatch domain cuts both ways: it strengthens the case that the coroutine completion model generalizes, and it complicates any strict assignment of dispatch to senders. The dispatch/transport split names the centers of the two domains rather than a border. Section 18.5 states the survey's limits.

## 15. CUDA Graphs Optimize a Different Layer

Sender pipelines provide compile-time `operation_state` fusion. [P3425R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3425r1.html)<sup>[57]</sup> documents one stored pointer saved per child operation state via constant pointer offsets, more where padding allows. This is real.

CUDA Graphs<sup>[58]</sup> provide GPU-side work-graph optimization at the driver level. The driver sees streaming multiprocessor (SM) count, memory bandwidth, occupancy, and hardware topology. Stream capture<sup>[24]</sup> records kernel DAGs (directed acyclic graphs). The sequence below is the existing CUDA API; the accompanying `datamovement` example<sup>[15]</sup> compiles it inside a coroutine that drives `cuda_stream`:

```c
cudaStreamBeginCapture(stream,
    cudaStreamCaptureModeGlobal);
kernel_A<<<grid, block, 0, stream>>>(args);
kernel_B<<<grid, block, 0, stream>>>(args);
cudaStreamEndCapture(stream, &graph);

cudaGraphInstantiate(&instance, graph, 0);
cudaGraphLaunch(instance, stream);
```

The CUDA Graph documentation quantifies per-kernel launch overhead at 20-200 us in deep-learning applications.<sup>[59]</sup> That figure includes framework dispatch above the raw C++ launch cost that Table 3 lists at 1-5 us. In DALLE2 inference (over 740 kernels, 3.4ms GPU time on an H100), 75% of end-to-end latency is CPU launch delays.<sup>[60]</sup> Replaying a captured graph replaces those per-kernel round trips with a single launch.

CUDA Graphs and sender compile-time fusion optimize different layers. CUDA Graphs eliminate per-kernel CPU-GPU dispatch round trips at the driver level: the language transitions, runtime processing, and driver operations that make up the 20-200 us per-kernel cost above. Sender fusion eliminates host-side C++ abstraction overhead - allocations, virtual dispatch, type erasure - at the language level. nvexec intercepts sender algorithms and replaces them with CUDA kernel launches on streams. A search of `include/nvexec` at stdexec commit 307b83c5 for `cudaGraph` finds no CUDA Graph API use, and a machine-generated documentation site over the repository does not mention CUDA Graphs either,<sup>[61]</sup> so per-kernel host launch overhead appears to remain unless CUDA Graphs are used separately. These optimizations are complementary.

CUDA Graph replay composes naturally with coroutine-based data movement: the coroutine provides the outer loop with data-dependent control flow (memcpy in, graph launch, memcpy out, check result), and the pre-captured graph is the inner optimized hot path. Schr&ouml;dinger's Desmond engine (GTC 2024)<sup>[52]</sup> uses both techniques in the same production engine - coroutine-overlapped simulations and CUDA Graphs - and the NVIDIA blog account of the session reports up to 2.02x speedup for the approach as a whole. The account lists the techniques together without describing their composition or attributing the speedup to either one.

Two questions remain open in the record: whether sender fusion adds measurable value once graph capture has eliminated the driver-level dispatch overhead, and whether GPU pipelines beyond Desmond's structure benefit from coroutine orchestration around pre-captured graphs.

## 16. PMR Pools Amortize Frame Allocation

Each coroutine suspension potentially allocates a frame. Sender `operation_state` is a single compile-time allocation. This is a real structural difference. Two mitigations follow: compiler elision (HALO), which is compiler-dependent, and PMR pools, which are portable and amortize the cost.

### HALO

Heap Allocation eLision Optimization<sup>[62]</sup> allows the compiler to place the coroutine frame in the caller's frame when the lifetime is provably bounded. Capy's `task` is annotated with `[[clang::coro_await_elidable]]`<sup>[63]</sup> to enable this.

HALO is fragile: the attribute was introduced<sup>[64]</sup> because "Task types are rarely simple enough for the destroy logic of the task to reference the SSA value from coro.begin() directly. Hence, the pass is very ineffective for even the most trivial C++ Task types." A user reported regressions in Clang 19-20,<sup>[65]</sup> a correctness bug with `suspend_never`,<sup>[66]</sup> and that parentheses around a `co_await` operand silently break elision.<sup>[67]</sup> The attribute is Clang-only. HALO removes the allocation when it applies; the four reports show it cannot be relied on across compilers and code shapes.

### PMR pools

Capy's `io_env` carries a `std::pmr::memory_resource*`.<sup>[68]</sup> Thread-local recycling pools amortize allocation cost to near zero. This is reliable, portable, and works regardless of compiler optimization.

Table 3 places frame allocation next to the GPU operations a frame orchestrates. The two allocation rows are order-of-magnitude figures for a pooled and a `malloc`-backed frame: the 17 ns delta between the allocating and non-allocating type-erased paths in Table 1 (53.4 ns against 36.4 ns per operation) is a floor the `malloc` row exceeds, its upper end reflecting typical glibc `malloc`/`free` costs. The pooled row is an estimate. Each GPU row cites the vendor figure, measurement, or vendor formula it is drawn from, and the hardware and workload named in the row are those of the source.

| Operation | Time |
|---|---|
| Coroutine frame alloc (PMR pool) | 2-5 ns |
| Coroutine frame alloc (malloc) | 30-60 ns |
| CUDA kernel launch, driver and hardware overhead<sup>[69]</sup> | 1,000-5,000 ns |
| `cudaMemcpy`, small host-to-device copy (DGX-1V)<sup>[70]</sup> | 7,000 ns |
| cuDNN convolution, 1x1 filters, batch size 1 (V100)<sup>[71]</sup> | 19,000-24,000 ns |
| NCCL AllReduce, 350 GB of gradients over a 50 GB/s port per rank<sup>[72]</sup> | 1,000,000,000+ ns |

The AllReduce row is derived rather than measured: the nccl-tests performance note<sup>[72]</sup> gives the ring all-reduce time as `t = (S/B) * (2*(n-1)/n)`, and for 350 GB of gradients (a 175-billion-parameter model in 16-bit) over a 50 GB/s port per rank that is about 14 seconds for large `n`. A coroutine frame allocation with a PMR pool is roughly two to nine orders of magnitude cheaper than the GPU operations it orchestrates; against an all-reduce that takes seconds, the 5 ns frame allocation is at least eight orders of magnitude smaller.

One caveat: the latency table assumes GPU operations in the microsecond-to-second range. For high-frequency kernel dispatch where individual kernel execution times approach the sub-microsecond range, the frame allocation cost relative to the operation cost may be different, and whether it becomes a measurable bottleneck there is an open question for domain experts. A second caveat: `cudaLaunchHostFunc` callback latency can spike to 12ms on A100 and H100 systems, per the single report, not reproduced by NVIDIA, discussed in Section 7,<sup>[25]</sup> which means the callback dispatch latency can dominate both frame allocation and the GPU operation itself. The 2-5 ns frame allocation cost is not always the relevant comparison.

## 17. The Bridge Between Domains

This section covers the two bridge functions that connect a sender pipeline and a coroutine at the point where GPU dispatch meets byte-oriented I/O, and what each bridge can and cannot carry.

Capy provides two bridge functions with working implementations in its bench and example code<sup>[15]</sup>: `await_sender`<sup>[8]</sup> consumes a sender from within a coroutine via `co_await`, and `as_sender`<sup>[9]</sup> wraps an IoAwaitable as a P2300R10<sup>[1]</sup> sender for use in a sender pipeline. Both compile and run today. The `as_sender` direction drives the awaitable from a sender operation state without a compiler-generated coroutine frame: it hands the awaitable a `coroutine_handle<>` built over a struct whose first two members are the resume and destroy function pointers, the de facto frame layout that P3203R0<sup>[73]</sup> documents for MSVC, GCC, and Clang and proposes to make implementation-defined rather than undefined; P4126R1<sup>[74]</sup> describes the technique. Until that wording lands, this direction relies on behavior the standard does not yet bless. [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf)<sup>[8]</sup> and [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf)<sup>[9]</sup> are the dedicated design papers for each direction.

`await_sender` is the natural bridge for the common case: a coroutine that performs I/O and dispatches to a GPU scheduler. An inference pipeline that uses each model in its natural domain:

```cpp
task<> handle_request(
    any_read_stream& client,
    any_write_stream& response,
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
                    y[i] = static_cast<float>(i);
            })
        | stdexec::continues_on(cpu));

    // copy result to host, send it back (type-erased)
    std::array<float, N> result;
    cudaMemcpy(result.data(), d_out,
        N * sizeof(float),
        cudaMemcpyDeviceToHost);
    cudaFree(d_out);
    auto [wec, wn] = co_await write(response,
        capy::make_buffer(
            result.data(),
            result.size() * sizeof(float)));
}
```

The listing is the `handle_request` function of the accompanying pipeline example,<sup>[15]</sup> which compiles it alongside two scenes that run; `handle_request` itself is compiled but not called. The kernel body stands in for a model; a real inference kernel would be a `__device__` function invoked in its place.

Network I/O uses `any_read_stream` and `any_write_stream` - type-erased, zero per-operation allocation, compound results via structured bindings. GPU dispatch uses `nvexec::launch` on the stream scheduler - compile-time composition, scheduler-agnostic portability. Because nvexec runs the launched work on the device, the kernel body must be device code, and the trailing `stdexec::continues_on(cpu)` returns completion to the host before the host-only `await_sender` bridge resumes the coroutine. Therefore the handler takes a host scheduler alongside the GPU context. The `await_sender` bridge connects the two without requiring either model to subsume the other.

The device-to-host `cudaMemcpy` and the per-request `cudaMalloc`/`cudaFree` in the example are deliberate simplifications that keep the bridge visible. A production handler would use `cuda_stream`'s `memcpy_d2h` awaitable and pooled device allocations.

Behind `client` and `response`, the network transport can be TCP, TLS, RDMA, or any transport that satisfies the stream concepts. The GPU scheduler can be `nvexec::stream_scheduler`, a CPU thread pool, or any scheduler that provides `schedule()`. Neither side needs to know about the other's implementation.

`as_sender` provides the reverse direction: a sender pipeline that consumes an IoAwaitable. This is useful when an existing sender pipeline needs to incorporate a byte-oriented operation:

```cpp
// as_sender rejects an awaitable whose result is
// (error_code, ...) at compile time. A task wrapper
// moves the byte count out through a side channel
// and hands the bridge only the error code.
task<std::error_code>
write_to_gpu(cuda_device_stream& gpu_sink,
    const_buffer buf, std::size_t& n_out)
{
    auto [ec, n] = co_await gpu_sink.write_some(buf);
    n_out = n;
    co_return ec;
}

std::size_t n = 0;
auto pipeline =
    stdexec::write_env(
        as_sender(write_to_gpu(gpu_sink, buf, n)),
        stdexec::prop{get_io_executor, ex})
    | stdexec::then([&] { return n; })
    | stdexec::upon_error(
        [&](std::error_code) {
            return n;   // Bytes written before the error.
        });
```

The `as_sender` bridge refuses, with a `static_assert`, any awaitable whose result destructures to `(error_code, ...)`: sender completion channels are exclusive, so routing the error through `set_error` would silently drop the byte count of a partial write. The wrapping task inspects the full result, moves the count out through a side channel, and returns only the error code, so the wrapper rather than the bridge decides the payload's fate; `upon_error` and `retry` then see the error on its own channel. This is the channel choice of Section 11 made explicit at the boundary. The rejection and the `task<std::error_code>` route are pinned by the tests of the `awaitable-sender` example, and scene 2 of the `cuda/pipeline` example runs the same wrapper shape over a stream read.<sup>[15]</sup> `await_sender` wraps a sender unchanged; `as_sender` wraps a non-compound awaitable unchanged and a compound one through the task shown.

## 18. Considerations

This section addresses foreseeable concerns about the conclusions drawn above, grouped into five: laziness and composition, consumer choice, type erasure and allocation, composition algebra, and scope of evidence.

### 18.1 Laziness and Composition

**Awaitables commit to eager execution.** Awaitables are lazy. `write_some` returns an inert object. Until `co_await` triggers `await_suspend`, no `cudaMemcpyAsync` is issued and no syscall is made. In both models, the trigger is explicit: senders do no work until `start()` is called, and awaitables do no work until `co_await` is evaluated. A coroutine can capture the awaitable, defer the `co_await`, and decide at runtime whether to submit the operation. This concern does not distinguish the two models.

**The scheduler cannot see the full task graph.** Sender pipelines compose as a graph the scheduler can inspect before `start()`. This is valuable for GPU kernel dispatch where the work graph is known ahead of time - CUDA Graphs (Section 15) exploit this property at the driver level, replacing per-kernel launch overhead of 20-200 us with a single graph launch.<sup>[59]</sup> Data movement is different. The next transfer depends on the result of the previous one: how many bytes arrived, whether the peer reset the connection, whether the RDMA completion carried an error. There is no static graph to inspect because control flow branches on runtime data. NCCL topology discovery, RDMA memory registration, and NVLink channel selection are all runtime decisions driven by hardware probing (Section 12). Coroutine control flow - `if`, `for`, `while` - is the natural expression of data-dependent sequential decisions.

**Senders separate description from execution. Coroutines conflate them.** The separation is valuable when the same algorithm can run on CPU or GPU by swapping the scheduler. The Maxwell FDTD benchmark demonstrates this: identical sender code runs on a CUDA GPU and on a CPU thread pool (Section 2). Data movement operations are bound to specific hardware resources at submission time. A `cudaMemcpyAsync` targets a specific CUDA stream on a specific device, an `ibv_post_send` a specific queue pair on a specific host channel adapter (HCA), and a `read` a specific file descriptor. The description cannot be retargeted by swapping a scheduler because the operation is bound to the resource. For compute dispatch, description-execution separation enables scheduler-agnostic portability. For data transport, the binding to hardware resources makes the separation vacuous.

### 18.2 Consumer Choice and Return Types

**Data movement operations should return senders so the caller can choose how to consume them.** The choice is symmetric. `as_sender`<sup>[9]</sup> wraps an awaitable for sender pipeline consumption. `await_sender`<sup>[8]</sup> wraps a sender for coroutine consumption. Neither return type gives every consumer zero-cost access. Returning a sender forces a per-operation allocation under type erasure (Table 1, from P4088R1:<sup>[5]</sup> 53.4 ns/op, 1 alloc/op). Returning an awaitable preserves zero-allocation type erasure (36.4 ns/op, 0 alloc/op) and gives sender pipeline consumers access through `as_sender`. The question is which consumer bears the cost. For data movement where the protocol handler is compiled once against a type-erased stream (Section 8), the type-erased consumer is the common case. P4088R1<sup>[5]</sup> Section 10 documents the full design fork analysis.

**The bridge proves senders are more fundamental.** The bridge is symmetric: each model can consume the other's operations through the pair of functions described in Section 17. CPU and GPU interact through memory copies. That does not make one side more fundamental. The bridge is evidence of complementarity between models that serve different domains - compute dispatch and data transport. P4088R1<sup>[5]</sup> Section 9 addresses this directly.

### 18.3 Type Erasure and Allocation

**Type erasure should be opt-in, not baked into the abstraction.** Byte-oriented data movement is a domain where the transport is inherently runtime-determined. An inference server does not know at compile time whether input arrives over TCP, RDMA, or NVLink - the transport depends on the deployment topology, which is discovered at communicator creation time via `ncclCommInitRank` or equivalent (Section 12). Type erasure is the natural interface for this domain. Senders' compile-time visibility optimizes for static dispatch, which is not the bottleneck when every operation crosses a kernel boundary (1,000-5,000 ns) or a PCIe bus (about 7,000 ns). This is the same design trajectory traced in Section 10. P4088R1<sup>[5]</sup> Section 7.1 documents the structural mechanism.

**Coroutine frames allocate. Sender operation states do not.** Acknowledged. Sender `operation_state` is a compile-time construct with no heap allocation. Coroutine frames allocate. PMR pools amortize this to near zero (Section 16). For data movement, the relevant comparison is total allocation across the stream's lifetime. Under type erasure, the sender model allocates once per `any_sender::connect` (Section 9). The coroutine model allocates once per frame (Section 16). For N operations through a type-erased stream, the coroutine model allocates once. The sender model allocates N times. P4088R1<sup>[5]</sup> Sections 4 and 7.9 cover the general case.

**Compile-time optimization is lost.** Coroutine handles are opaque. The compiler cannot see through `resume()`. Sender pipelines are fully visible, statically dispatched, inlinable. This visibility matters for GPU kernel dispatch where individual operations cost nanoseconds and the compiler can fuse host-side abstraction overhead (Section 2). The latency scale of data movement dwarfs indirect-call overhead (Section 16). For data movement, the optimization target is allocation elimination under type erasure (Section 9). P4088R1<sup>[5]</sup> Section 4 documents the optimization barrier.

### 18.4 Composition and Algorithms

**Senders provide 30 generic algorithms. Awaitables provide none.** The awaitable composition mechanism is the language's own control flow: `if`, `for`, `while`, `try/catch`, structured bindings. These compose naturally with data-dependent decisions - the `if(ec == errc::connection_reset)` in Section 11 is a branch on runtime data that determines the next operation. For GPU dispatch where the full work graph must be visible to the scheduler before launch, the sender composition algebra is justified (Section 2). For data movement where each operation depends on the result of the previous one, ordinary control flow is the natural mechanism and is debuggable with standard tools. P4088R1<sup>[5]</sup> Section 2.2 compares the two vocabularies.

**Compound results can be routed through set_value.** Route `(error_code, bytes_transferred)` through `set_value` as a compound type. This is physically possible. It is also what Section 11 documents: if all data-movement results route through `set_value`, then `set_error` and `set_stopped` are vestigial for these operations. The three-channel model's value - that different channels enable different downstream algorithms (`retry`, `upon_error`) - is nullified. P2300R10<sup>[1]</sup> Section 4.14, quoted in Section 11, gives this value-channel routing as its first answer, alongside error-channel bundling and a range of senders. The three channels match GPU kernel dispatch, where `cudaErrorLaunchFailure` is fatal and carries no partial result. Byte-oriented operations produce compound results where both status and byte count are always present. P4091R1<sup>[6]</sup> analyzes all six positions.

### 18.5 Scope and Evidence

**Structured concurrency is weaker in the coroutine model.** Acknowledged (Section 2). Senders provide `counting_scope` for dynamic fan-out with guaranteed completion before scope destruction. Coroutines provide lexical-scope safety via `when_all` but dynamic fan-out needs explicit library support. Data movement is ordered per stream or connection - one buffer at a time, one completion at a time, the one-at-a-time invariant on the CUDA stream (Section 7) - and practical overlap comes from multiple streams or connections in flight, each individually ordered. Dynamic fan-out across an unknown number of tasks belongs to the compute dispatch domain, where senders provide it.

**No GPU throughput is measured.** The structural claims - completion shape, allocation, ABI - are demonstrated by the examples; the throughput of awaiting on a CUDA stream is not measured here. Awaiting per transfer fits data-dependent and host-orchestrated sequences (Section 7); a static burst of independent transfers is one buffer sequence awaited once, a captured graph (Section 15), or an all-device sender chain, and awaiting it per transfer is a misuse of the awaitable rather than a property of it.

**The sender-based networking survey may be incomplete.** Acknowledged. The survey (Section 13) reports every project its search of the public record found. Its recall is bounded by that record. Production-grade sender-based networking that the search missed would strengthen the case for sender-based I/O and belongs in a future revision. The search method for both surveys was not recorded when they were run. The tables list what was found, and the absence claims carry that caveat.

**The CUDA examples were generated with AI assistance.** Disclosed in the Disclosure. The examples are presented as a research exercise for evaluation by domain experts. Errors in the CUDA code would indicate where the examples need refinement. The structural observation stands on the independent projects in Section 14, whose code is the projects' own.

**The paper's P2300R10 quotations may be taken out of context.** Both quotations state positions P2300R10 holds in its own voice: Section 4.14 poses the partial-success question and Section 11 quotes P2300R10's own answer (value-channel routing) in the same paragraph, and Section 4.15 states the coroutine-consumption expectation as the design's intent.<sup>[1]</sup>

## 19. Conclusion

From three directions, the findings converge. Structurally, the four transports examined here present one abstract interface - submit a buffer, await completion, receive a compound result - and the IoAwaitable protocol expresses that interface with zero per-operation allocation. A coroutine suspends on each `co_await`, so at most one operation is in flight per single-owner stream and the pre-allocated op-state pattern that networking sockets use carries over. The single-owner discipline secures the invariant on the host side, and the CUDA Programming Guide's stream-ordering guarantee<sup>[23]</sup> secures that completion is signaled after the transfer, for every notification mechanism. Empirically, independent projects at NVIDIA Labs (cuda-oxide),<sup>[48]</sup> the University of Wisconsin-Madison (Taro),<sup>[49]</sup> and Schr&ouml;dinger (Desmond)<sup>[52]</sup> reached coroutine suspension on GPU work by separate routes: a `cuLaunchHostFunc` bridge in Rust, a `cudaLaunchHostFunc` bridge for task graphs, and simulation interleaving in production. CERN<sup>[33]</sup> has an open port of its traccc reconstruction pipeline onto the protocol, beside an open stdexec port of the same layer, with four suspending strategies behind one selector. The notification mechanism is a free variable the protocol does not fix: the traccc port implements the callback, event polling, and deferred synchronization as interchangeable strategies, and the slides of a CHEP 2026 contribution<sup>[29]</sup> report that the callback scales less well than the other two in their multi-threaded setup.

`cudaLaunchHostFunc` has documented limitations (Section 7) that bound the applicability of the callback mechanism in high-throughput GPU pipelines, and the callback carries no status (Section 7), so a callback awaitable must query the stream after resumption to see a fault. Those limitations are specific to the callback: the protocol equally admits event polling and deferred synchronization, which sidestep them where they apply.

`std::execution` provides real properties for GPU dispatch: zero-allocation compile-time composition, scheduler-agnostic portability, domain customization via `transform_sender`, and structured concurrency for dynamic fan-out. CUDA Graphs and sender fusion optimize at different layers - graphs reduce driver-level dispatch overhead, sender fusion reduces host-side C++ abstraction overhead - and they are complementary.

Taro, TTG/PaRSEC, and Desmond demonstrate the coroutine pattern extending beyond byte movement to kernel dispatch and GPU pipeline orchestration, placing that evidence in the record alongside this paper's byte-movement analysis.

Bridges (`await_sender`<sup>[8]</sup>, `as_sender`<sup>[9]</sup>) connect the two models where the domains meet: a networking coroutine consumes a GPU sender for compute dispatch, and a sender pipeline wraps an IoAwaitable for composition. Neither model needs to subsume the other. Senders serve compute dispatch, where compile-time work graphs and scheduler-agnostic portability are decisive. Awaitables serve data transport, where type-erased streams, zero-allocation link-time polymorphism, and ABI stability (Section 10) are the working interface.

The record bears on [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup>, which proposes the IoAwaitable protocol for standardization. The surveyed projects that document a bridge each rebuilt coroutine completion on the GPU's own notification primitives. Section 6 shows that an awaitable built on the callback alone provides none of the three properties that protocol specifies - executor affinity, cancellation, and frame allocation control; whether each surveyed project supplies them by other means is not examined here. Now the evaluation of these findings sits with the domain experts of SG1 and with the authors of P4003R3. This paper places the record before them.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[17]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[16]</sup>, coroutine-native I/O libraries under the C++ Alliance.

This paper examines how C++20 coroutines integrate with CUDA's async completion model for byte-oriented data movement and places the findings in the record for evaluation by domain experts.

The author has a stake in the coroutine model's adoption. The competing model, `std::execution`, is in the C++26 working draft, while the IoAwaitable protocol is proposed but not standardized.

The author is a networking domain expert, not a GPU domain expert, and each coroutine suspension potentially allocates a frame. Both limitations are examined in the body (Sections 16 and 18).

Companion papers: [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup> specifies the protocol this paper examines. P4088R1<sup>[5]</sup>, P4091R1<sup>[6]</sup>, P4092R1<sup>[8]</sup>, P4093R1<sup>[9]</sup>, and P4123R0<sup>[7]</sup> examine adjacent questions.

The CUDA data-movement examples were produced with AI assistance and are presented as a research exercise. Compilable demonstrations accompany the paper,<sup>[15]</sup> and the notification-strategies, bridge, and batched-write examples among them run.

This paper was generated with AI assistance (Claude, via Cursor).

This paper asks for nothing.

## Acknowledgments

Eric Niebler, Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Bryce Adelstein Lelbach, Dietmar K&uuml;hl, and Jens Maurer, whose work on `std::execution` (P2300R10<sup>[1]</sup>) this paper examines and builds upon.

Richard Smith and Gor Nishanov for P0981R0<sup>[62]</sup> (HALO analysis). Yuxuan Chen for the `[[clang::coro_await_elidable]]` attribute. Chuanqi Xu for P2477R3<sup>[75]</sup> (coroutine allocation elision). Dietmar K&uuml;hl and Maikel Nadolski for P3552R3<sup>[76]</sup> (`std::execution::task`). Lewis Baker for cppcoro, the operator `co_await` and symmetric transfer blog posts, and P3425R1<sup>[57]</sup> (operation-state sizes). Michael Wong for P4029R0<sup>[4]</sup> (SG14 priority list).

Michael Garland and the NVIDIA stdexec team for the nvexec GPU schedulers and the Maxwell FDTD benchmark. Mateusz Jakub Fila, Attila Krasznahorkay, and Eric Cano (CERN Next Generation Triggers project) for their C++20 coroutine task-scheduling experiments and the Capy IoAwaitable integration. Dian-Lun Lin (University of Wisconsin-Madison) for Taro and its CppCon 2023 presentation. The NVIDIA Labs team for cuda-oxide. Jiqun Tu (NVIDIA) and Ellery Russell (Schr&ouml;dinger) for the Desmond coroutine integration presented at GTC 2024. The TTG/PaRSEC team for demonstrating coroutine-based heterogeneous GPU dispatch.

## References

[1] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[2] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec) - Reference implementation of `std::execution` (NVIDIA, 2021).

[3] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[4] [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf) - "The SG14 Priority List for C++29/32" (Michael Wong, 2026).

[5] [P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[6] [P4091R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4091r1.pdf) - "Error Models of Regular C++ and the Sender Sub-Language" (Vinnie Falco, 2026).

[7] [P4123R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4123r0.pdf) - "The Cost of Senders for Coroutine I/O" (Vinnie Falco, 2026).

[8] [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[9] [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[10] [nvexec stream_context.cuh](https://github.com/NVIDIA/stdexec/blob/307b83c5689ea7c2e5b31561cdc428697705333e/include/nvexec/stream_context.cuh) - NVIDIA stdexec GPU scheduler; `stream/then.cuh` launches each `then` stage as a kernel on the stream and `stream/let_xxx.cuh` calls `cudaStreamSynchronize` before invoking a `let_value` function (NVIDIA, commit 307b83c5, 2026).

[11] [CUDA Runtime API: Memory Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY.html) (NVIDIA, 2024).

[12] [CUDA Runtime API: Execution Control](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EXECUTION.html) (NVIDIA, 2024).

[13] [NCCL User Guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html) (NVIDIA, accessed 2026).

[14] [ibv_create_comp_channel(3)](https://man7.org/linux/man-pages/man3/ibv_create_comp_channel.3.html) - rdma-core manual page (accessed 2026).

[15] [Accompanying examples](https://github.com/cppalliance/capy/tree/ee317c4c26250c3da82ecd17931a97191087bd1b/example) - the compilable demonstrations for this paper, pinned at commit `ee317c4c26250c3da82ecd17931a97191087bd1b` of the official repository (C++ Alliance, 2026). Of the CUDA targets, `notification-strategies`, `pipeline`, and `batched-write` run; `datamovement` and `fabrics` are build-only. Section 5 (the three notification mechanisms, `callback_awaitable`, `poll_awaitable`, `deferred_sync_awaitable`): [`example/cuda/notification-strategies`](https://github.com/cppalliance/capy/tree/ee317c4c26250c3da82ecd17931a97191087bd1b/example/cuda/notification-strategies). Sections 7-8 and 15 (`cuda_stream`, `cuda_device_stream`, CUDA Graphs): [`example/cuda/datamovement`](https://github.com/cppalliance/capy/tree/ee317c4c26250c3da82ecd17931a97191087bd1b/example/cuda/datamovement). Section 8 (batched `write_some`, runs): [`example/cuda/batched-write/batched_write.cu`](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/example/cuda/batched-write/batched_write.cu). Section 17 (the `await_sender` bridge, `handle_request`): [`example/cuda/pipeline/cuda_pipeline.cu`](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/example/cuda/pipeline/cuda_pipeline.cu); the `as_sender` bridge, its compile-time rejection of compound results, and the `task<std::error_code>` route: [`example/awaitable-sender`](https://github.com/cppalliance/capy/tree/ee317c4c26250c3da82ecd17931a97191087bd1b/example/awaitable-sender), used by `cuda/pipeline` scene 2: [`example/cuda/pipeline/cuda_pipeline.cu`](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/example/cuda/pipeline/cuda_pipeline.cu). Sections 11-12 (compound results and HPC-fabric signatures): [`example/fabrics/fabrics.cpp`](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/example/fabrics/fabrics.cpp). Section 9 (the `any_sender` operation-state measurement, runs): [`example/any-sender-size/any_sender_size.cpp`](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/example/any-sender-size/any_sender_size.cpp).

[16] [Corosio](https://github.com/cppalliance/corosio) (C++ Alliance, 2026).

[17] [Capy](https://github.com/cppalliance/capy) (C++ Alliance, 2025).

[18] [Capy io_env](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/include/boost/capy/ex/io_env.hpp) (C++ Alliance, 2026).

[19] [Capy executor_ref](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/include/boost/capy/ex/executor_ref.hpp) (C++ Alliance, 2026).

[20] [Understanding Symmetric Transfer](https://lewissbaker.github.io/2020/05/11/understanding_symmetric_transfer) (Lewis Baker, 2020).

[21] [Capy continuation](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/include/boost/capy/continuation.hpp) (C++ Alliance, 2026).

[22] [Capy task](https://github.com/cppalliance/capy/blob/ee317c4c26250c3da82ecd17931a97191087bd1b/include/boost/capy/task.hpp) (C++ Alliance, 2026).

[23] [CUDA Programming Guide: Asynchronous Concurrent Execution](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html) (NVIDIA, 2024).

[24] [CUDA Runtime API: Stream Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__STREAM.html) (NVIDIA, 2024).

[25] [NVIDIA Developer Forums: cuLaunchHostFunc overhead latency](https://forums.developer.nvidia.com/t/culaunchhostfunc-overhead-latency-usage-cpu-gpu-signaling/327066) - Latency spikes up to 12ms on loaded A100/H100 systems (2025).

[26] [CUDA Handbook: Stream Callbacks](https://www.cudahandbook.com/2012/09/stream-callbacks/) (Nicholas Wilt, 2012).

[27] [Stack Overflow: Exception Handling in cudaLaunchHostFunc Callbacks](https://stackoverflow.com/questions/75145603/catching-an-exception-thrown-from-a-callback-in-cudalaunchhostfunc) (2023).

[28] [CUDA Runtime API: Event Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EVENT.html) (NVIDIA, 2024).

[29] [Scheduling for Next Generation Triggers](https://indico.cern.ch/event/1471803/contributions/6967272/) - CHEP 2026 contribution; the scaling findings appear in the attached presentation slides (Mateusz Jakub Fila, Attila Krasznahorkay, Eric Cano, 2026).

[30] [Stack Overflow: CUDA Graph host execution nodes in different streams](https://stackoverflow.com/questions/75739969/is-it-possible-to-execute-more-than-one-cuda-graphs-host-execution-node-in-diff) - Robert Crovella (NVIDIA) on host functions in independent streams executing in undefined order and possibly serialized (2023).

[31] [NVIDIA Developer Forums: Do stream callbacks hold CUDA-internal locks?](https://forums.developer.nvidia.com/t/do-stream-callbacks-hold-any-cuda-internal-locks/337769) - Deadlock risk with user locks in callbacks (2025).

[32] [Multipath Memory Access: Breaking Host-GPU Bandwidth Bottlenecks in LLM Serving](https://arxiv.org/html/2512.16056v2) - cudaLaunchHostFunc unidirectional notification limitation (Lingfeng Tang, Daoping Zhang, Junjie Chen, Peihao Huang, Feng Jin, Chengguang Xu, Yuxin Chen, Feiqiang Sun, Guo Chen, 2025).

[33] [cern-nextgen/wp1.7-traccc PR #18](https://github.com/cern-nextgen/wp1.7-traccc/pull/18) - "Port to Boost.Capy", CERN port of the traccc GPU track-reconstruction pipeline onto Capy, open as of this writing, implementing callback, event-polling, and deferred-synchronization await strategies behind a single selector, the callback as an IoAwaitable and the others as tasks run on a service executor; a sibling open pull request (#16) ports the same layer onto stdexec (2026).

[34] [CUDA Programming Guide: Page-Locked Host Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html) (NVIDIA, 2024).

[35] [CUDA Runtime API: API Synchronization Behavior](https://docs.nvidia.com/cuda/cuda-runtime-api/api-sync-behavior.html) (NVIDIA, 2024).

[36] [NVIDIA/stdexec any_sender_of.hpp](https://github.com/NVIDIA/stdexec/blob/main/include/exec/any_sender_of.hpp) - 64-byte small-buffer optimization for type-erased sender operation states (NVIDIA, accessed 2026).

[37] [N3408](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3408.pdf) - "Parallelizing the Standard Algorithms Library" (Jared Hoberock, Michael Garland, Olivier Giroux, Vinod Grover, Ujval Kapasi, Jaydeep Marathe, 2012).

[38] [LCI](https://arxiv.org/html/2505.01864v2) - "LCI: a Lightweight Communication Interface for Efficient Asynchronous Multithreaded Communication" - C++17 async communication library with libibverbs and libfabric backends, host-initiated GPU-Direct RDMA, SC'25 (Jiakun Yan, Marc Snir, 2025).

[39] [libunifex Issue #586](https://github.com/facebookexperimental/libunifex/issues/586#issuecomment-1845934903) - Meta internal guidance on senders vs coroutines (Ian Petersen, 2023).

[40] [uring_exec](https://github.com/Caturra000/uring_exec) - io_uring networking over stdexec (Caturra000, 2024).

[41] [execution-ucx](https://github.com/MoFHeka/execution-ucx) - UCX transport over libunifex (MoFHeka, 2025).

[42] [beman.net](https://github.com/bemanproject/net) - Beman project implementation of the P2762R2 sender networking interface (Beman Project, 2024).

[43] [P2762R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r2.pdf) - "Sender/Receiver Interface For Networking" (Dietmar K&uuml;hl, 2023).

[44] [senders-io](https://github.com/maikel/senders-io) - "An adaption of Senders/Receivers for async networking and I/O" (Maikel Nadolski, 2023).

[45] [kuhllib](https://github.com/dietmarkuehl/kuhllib) - experimental standard C++ library with sender-based networking (Dietmar K&uuml;hl, 2012).

[46] [snp](https://github.com/deepgrace/snp) - "Structured Network Programming with Sender / Receiver" (deepgrace, 2023).

[47] [stdexec PR #1501](https://github.com/NVIDIA/stdexec/pull/1501) - "Adapt boost::asio to stdexec" (shyeyian, 2025; closed unmerged).

[48] [cuda-oxide: The DeviceOperation Model](https://nvlabs.github.io/cuda-oxide/async-programming/the-device-operation-model.html) - NVIDIA Labs async GPU programming in Rust (2026).

[49] [Taro](https://github.com/dian-lun-lin/taro) - C++20 coroutine task-graph system for CPU-GPU workloads (Dian-Lun Lin, University of Wisconsin-Madison, 2024).

[50] [TaroRTL](https://doi.org/10.1007/978-3-031-69583-4_11) - "TaroRTL: Accelerating RTL Simulation Using Coroutine-Based Heterogeneous Task Graph Scheduling" (Dian-Lun Lin, Umit Ogras, Joshua San Miguel, Tsung-Wei Huang, 2024).

[51] [async-cuda](https://github.com/oddity-ai/async-cuda) - Async CUDA for Rust (Oddity AI, 2024).

[52] [Optimizing Drug Discovery with CUDA Graphs, Coroutines, and GPU Workflows](https://developer.nvidia.com/blog/optimizing-drug-discovery-with-cuda-graphs-coroutines-and-gpu-workflows/) - NVIDIA Developer Blog account of the GTC 2024 session by Jiqun Tu and Ellery Russell (Michelle Horton, 2024).

[53] [TTG (Template Task Graph)](https://github.com/TESSEorg/ttg) - C++20 coroutine-based heterogeneous task graph on PaRSEC (2024).

[54] [rdmapp](https://github.com/howardlau1999/rdmapp) - C++20 coroutine wrapper for libibverbs (2024).

[55] [Loom](https://github.com/sielicki/loom) - C++23 typed interface over libfabric with Asio coroutine integration (sielicki, 2026).

[56] [FORD](https://github.com/minghust/ford) - Coroutine-enabled distributed transactions over one-sided RDMA (USENIX FAST 2022).

[57] [P3425R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3425r1.html) - "Reducing operation-state sizes for subobject child operations" (Lewis Baker, 2024).

[58] [CUDA Programming Guide: CUDA Graphs](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html) (NVIDIA, 2024).

[59] [NVIDIA CUDA Graph Best Practice for PyTorch: CUDA Graph](https://docs.nvidia.com/dl-cuda-graph/cuda-graph-basics/cuda-graph.html) (NVIDIA, 2024).

[60] [PyGraph: Robust Compiler Support for CUDA Graphs in PyTorch](https://arxiv.org/html/2503.19779v3) (Abhishek Ghosh, Ajay Nayak, Ashish Panwar, Arkaprava Basu, 2025).

[61] [DeepWiki: nvexec GPU Execution](https://deepwiki.com/NVIDIA/stdexec/6-gpu-execution-with-nvexec) (machine-generated, accessed 2026).

[62] [P0981R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0981r0.html) - "Halo: coroutine Heap Allocation eLision Optimization: the joint response" (Richard Smith, Gor Nishanov, 2018).

[63] [Clang Attribute Reference: coro_await_elidable](https://clang.llvm.org/docs/AttributeReference.html#coro-await-elidable) (LLVM, accessed 2026).

[64] [LLVM PR #99282: Introduce coro_await_elidable](https://github.com/llvm/llvm-project/pull/99282) (Yuxuan Chen, 2024).

[65] [LLVM Issue #64586](https://github.com/llvm/llvm-project/issues/64586) - "[Coroutines] The Coroutine elision optimization (or HALO) is not performed" (2023).

[66] [LLVM Issue #188230: HALO + suspend_never bad-free](https://github.com/llvm/llvm-project/issues/188230) (StephanDollberg, 2026).

[67] [LLVM Issue #178256: Parentheses break coro_await_elidable](https://github.com/llvm/llvm-project/issues/178256) (snarkmaster, 2026).

[68] [std::pmr::memory_resource](https://en.cppreference.com/w/cpp/memory/memory_resource) (cppreference, accessed 2026).

[69] [CUDA Graphs: Quantitative Benefits](https://docs.nvidia.com/dl-cuda-graph/cuda-graph-basics/quantitative-benefits.html) - "you can assume ~1-5 &mu;s per kernel for driver and hardware overhead" (NVIDIA, 2024).

[70] [GDRCopy](https://developer.nvidia.com/gdrcopy) - "around 1 &mu;s vs 7 &mu;s with cudaMemcpy for host-to-device copies", measured on a DGX-1V with CUDA 10.1 (NVIDIA, accessed 2026).

[71] [cuConv: A CUDA Implementation of Convolution for CNN Inference](https://arxiv.org/abs/2103.16234) - Table 3, batch-size-1 configuration, cuDNN implicit GEMM 19.20 &mu;s and precomputed implicit GEMM 24.29 &mu;s on a Tesla V100 (Marc Jord&agrave;, Pedro Valero-Lara, Antonio J. Pe&ntilde;a, 2021).

[72] [nccl-tests PERFORMANCE.md](https://github.com/NVIDIA/nccl-tests/blob/master/doc/PERFORMANCE.md) - ring all-reduce time `t = (S/B) * (2*(n-1)/n)` (NVIDIA, accessed 2026).

[73] [P3203R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3203r0.html) - "Implementation defined coroutine extensions" (Klemens David Morgenstern, 2024).

[74] [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf) - "A Universal Continuation Model" (Vinnie Falco, Klemens Morgenstern, 2026).

[75] [P2477R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2477r3.html) - "Allow programmers to control coroutine elision" (Chuanqi Xu, 2022).

[76] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).
