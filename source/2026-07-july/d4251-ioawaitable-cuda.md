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

A protocol handler compiled once links against TCP, RDMA, or GPU device memory without recompilation. This is possible because byte-oriented data movement - host-device memcpy, inter-GPU collectives over NVLink, RDMA transfers between nodes, and TCP sockets - shares a common async completion model that the IoAwaitable protocol captures with an ABI-stable, type-erased interface. Independent projects at NVIDIA Research, CERN, the University of Wisconsin-Madison, and Schr&ouml;dinger have converged on the same coroutine-based async completion pattern for GPU data movement. Bidirectional bridges connect IoAwaitables and senders where byte-oriented I/O meets GPU dispatch, allowing each model to serve its natural domain.

---

## Revision History

### R0: July 2026 (post-Brno mailing)

- Initial revision.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup>, coroutine-native I/O libraries under the C++ Alliance. The author has a stake in the coroutine model's adoption.

The author is a networking domain expert. The CUDA data-movement examples were produced with AI assistance. The findings are presented as a research exercise, not as expert testimony.

This paper explores how C++20 coroutines integrate with CUDA's async completion model for byte-oriented data movement and places the findings in the record for evaluation by domain experts.

Each coroutine suspension potentially allocates a frame. The IoAwaitable protocol is not standardized.

This paper asks for nothing.

## 2. What std::execution Provides

Before examining coroutine alternatives, we acknowledge what `std::execution` achieves. These are specific, genuine properties.

**Zero-allocation composition.** Sender pipelines collapse into a single `operation_state` at compile time. No heap allocation, no virtual dispatch, no reference counting. This is a real property that coroutines do not match for multi-stage pipelines.<sup>[3]</sup>

**Domain customization.** A scheduler's `transform_sender` can replace `bulk` with a GPU kernel launch transparently. This enables writing algorithm code once and retargeting to CPU or GPU by swapping the scheduler.<sup>[4]</sup>

**Structured concurrency.** `counting_scope` tracks dynamically spawned work and prevents scope destruction until all work completes. Coroutines provide lexical-scope safety via `when_all`, but dynamic fan-out to an unknown number of tasks needs explicit library support.

**Scheduler-agnostic portability.** The Maxwell FDTD benchmark in the [stdexec](https://github.com/NVIDIA/stdexec)<sup>[5]</sup> repository demonstrates the same algorithm achieving parity with raw CUDA on GPU and running correctly on a CPU thread pool.

These are real. They stand without qualification. These properties are strongest in GPU dispatch and heterogeneous scheduling, the domains for which `std::execution` was designed.

## 3. The Byte-Oriented Pattern

Four APIs that move bytes across different boundaries share a common async completion model:

**CUDA `cudaMemcpyAsync`.**<sup>[18]</sup> Bytes between host and device. Completion via `cudaLaunchHostFunc` callback.<sup>[9]</sup>

**NCCL `ncclAllReduce`.** Bytes between GPUs over NVLink or InfiniBand. Completion via CUDA stream synchronization.

**RDMA `ibv_post_send`.** Bytes between nodes. Completion via `ibv_comp_channel.fd` - a plain file descriptor that works with epoll, io_uring, or kqueue.

**TCP `read`/`write`.** Bytes between hosts. Completion via epoll, IOCP, or io_uring.

All four share the same structural pattern: submit a buffer of bytes, receive async completion via callback or file descriptor, receive a compound result (status plus byte count), and dispatch the result to the application thread via a reactor. IoAwaitable handles all of them with the same mechanism.

These four APIs span different hardware boundaries - PCIe, NVLink, InfiniBand, Ethernet - but present the same abstract interface to the application: submit a buffer, await completion, receive a compound result. Section 8 demonstrates a protocol handler written against this interface, and Section 10 traces the ABI consequence.

The type vocabulary builds from this pattern:

The `IoAwaitable` concept requires `await_suspend(coroutine_handle<>, io_env const*)` - the execution environment flows into each operation at the suspension point. The concept is defined in [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.html).<sup>[46]</sup>

The compound result type `io_result<std::size_t>` delivers both status and byte count via structured bindings:

```cpp
auto [ec, n] = co_await stream.write_some(buf);
```

The `WriteStream` concept requires `write_some(buffers)` returning an `IoAwaitable` whose `await_resume` returns `io_result<std::size_t>`. The `WriteSink` concept refines `WriteStream`, adding `write(buffers)` for complete-buffer writes and `write_eof()` for graceful shutdown.

The type-erased wrappers `any_write_stream` and `any_write_sink` wrap any `WriteStream` or `WriteSink` (respectively) behind a vtable with fixed-size entries: `await_ready`, `await_suspend`, `await_resume`, and `destroy`. Because `await_suspend` takes `coroutine_handle<>` - already type-erased by the language - the vtable has a fixed, compile-time-known size. Section 9 analyzes the structural consequences; Section 10 draws the ABI conclusion.

P2300R10<sup>[3]</sup> agrees with the user-facing pattern: "we expect that coroutines and awaitables will be how a great many will choose to express their asynchronous code."

## 4. The IoAwaitable Protocol

The IoAwaitable protocol from [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> extends the standard awaitable with an execution environment designed for I/O operations:

```cpp
template<typename A>
concept IoAwaitable =
    requires(A a, std::coroutine_handle<> h,
             io_env const* env) {
        a.await_suspend(h, env);
    };
```

The `io_env`<sup>[13]</sup> bundles three properties:

```cpp
struct io_env
{
    executor_ref executor;
    std::stop_token stop_token;
    std::pmr::memory_resource* frame_allocator
        = nullptr;
};
```

The `executor_ref`<sup>[14]</sup> is a type-erased executor with `dispatch(continuation&)` returning `coroutine_handle<>` for symmetric transfer<sup>[15]</sup>, and `post(continuation&)` for deferred execution. The `continuation`<sup>[16]</sup> type is a simple intrusive-list node:

```cpp
struct continuation
{
    std::coroutine_handle<> h;
    continuation* next = nullptr;
};
```

The `io_env` flows forward through `co_await` chains via `task`'s<sup>[17]</sup> `await_transform`, which wraps each child awaitable and passes the environment into its `await_suspend`. The critical difference from a hand-rolled awaitable: the awaitable knows which executor to resume on, carries a cancellation token, and has access to the frame allocator.

These three properties - executor affinity, cancellation, and frame allocation control - are the same concerns that `std::execution` addresses through a different mechanism. The IoAwaitable protocol provides them in a form designed for byte-oriented I/O, where type-erased streams and compound results are the natural vocabulary.

The full execution model built on this protocol is specified in [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.html).<sup>[46]</sup> That paper defines the launch functions that connect coroutine chains to the rest of the program: `run_async` starts a coroutine from regular code (the topmost caller that cannot `co_await`), and `run` switches executor, stop token, or allocator for a subtask from within a coroutine. IoAwaitables are lazy - submission happens in `await_suspend`, not at construction. The two-phase invocation of launch functions ensures the frame allocator is cached before the child coroutine's frame is allocated. P4003R3 also demonstrates a `counting_scope` built from launch function handlers, providing spawn, cancel, and join-before-destruction - the same structured concurrency guarantees that `std::execution`'s `counting_scope` provides, expressed through the IoAwaitable protocol's own primitives.

**Question for the reader:** Does this forward-propagation model - where the execution environment flows into each awaitable via `await_suspend` - address the concerns that GPU schedulers have about coroutine integration? Are there additional properties a GPU-aware awaitable would need?

## 5. The Bridge: `cudaLaunchHostFunc`

CUDA streams are in-order queues where operations execute sequentially.<sup>[6]</sup> When GPU work completes, the host needs notification. Three mechanisms exist:

- **Polling**: `cudaEventQuery` checks whether an event has completed.<sup>[7]</sup> Burns CPU cycles.
- **Blocking**: `cudaStreamSynchronize` blocks the calling thread.<sup>[8]</sup> Wastes a thread.
- **Callback**: `cudaLaunchHostFunc` enqueues a host function into the stream.<sup>[9]</sup> Zero busy-wait.

`cudaLaunchHostFunc` is the recommended replacement for the deprecated `cudaStreamAddCallback`.<sup>[6]</sup> The host function fires on a dedicated internal CPU thread created by the CUDA driver, not the application thread.<sup>[10]</sup><sup>[11]</sup> It cannot call CUDA APIs and must not create transitive dependencies on outstanding CUDA work.

This is the same structural pattern as epoll, IOCP, or io_uring completions arriving on arbitrary threads. In all cases, an async operation completes on a thread that is not the application's, and the application must dispatch the result to the correct execution context. This is the exact problem that Capy's executor-affinity dispatch was designed to solve.

## 6. Hand-Rolled Awaitables

The simplest integration writes a minimal awaitable that resumes the coroutine from the CUDA callback:

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

## 7. `cuda_stream`: Data Movement as IoAwaitables

The `cuda_stream` class wraps a CUDA stream handle and provides data-movement member functions that return IoAwaitables. The class follows the Rule of Five (copy deleted, move implemented, null-guarded destructor). The helper function `make_cuda_error`, defined by the accompanying demonstration<sup>[54]</sup> rather than by Capy, converts a `cudaError_t` to `std::error_code` via a CUDA error category.

The key mechanism is `resume_ctx`: a pre-allocated member that captures the executor and continuation for `cudaLaunchHostFunc`. The `on_complete` callback posts the continuation back to the application's executor, providing the executor-affinity dispatch that the hand-rolled awaitable in Section 6 lacks.

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

The `resume_ctx` is a pre-allocated member of `cuda_stream`, not heap-allocated per operation. This is safe because the coroutine suspends on each `co_await`, so only one operation is in-flight per `cuda_stream` at a time. The CUDA Programming Guide<sup>[6]</sup> confirms that operations in a stream execute in enqueue order, and the CUDA Runtime API documentation<sup>[9]</sup> states that `cudaLaunchHostFunc` callbacks block later work in the stream until they return.<sup>[47]</sup> The pre-allocated `resume_ctx` is never accessed concurrently. This is the same one-at-a-time invariant that Capy's sockets rely on for their pre-allocated op states in the networking domain.

`cudaLaunchHostFunc` has documented constraints that production code must respect. The callback must not call CUDA APIs or synchronize on outstanding CUDA work.<sup>[9]</sup> A single CUDA-internal worker thread may service all callbacks across all streams; on loaded systems, OS scheduling can starve this thread, producing latency spikes up to 12ms between callback completion and stream resumption.<sup>[48]</sup> If the callback blocks on a user lock while the CUDA launch queue is full, the enqueuing thread blocks too, producing deadlock.<sup>[49]</sup> Notification is unidirectional: `cudaLaunchHostFunc` provides stream-to-CPU notification only and cannot make the stream wait for a CPU-side signal.<sup>[50]</sup> These constraints apply equally to any pattern that uses `cudaLaunchHostFunc` for completion notification, including the hand-rolled awaitable in Section 6 and any sender-based wrapper that uses the same mechanism. They do not invalidate the pattern but they bound its applicability in high-throughput pipelines.

One caveat: `cudaMemcpyAsync` is only truly asynchronous with pinned (page-locked) memory.<sup>[19]</sup> With pageable memory allocated via `malloc` or `new`, the call blocks the host thread despite the `Async` suffix.<sup>[20]</sup> For multi-gigabyte model weight transfers, this distinction matters.

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

The `cuda_device_stream` class reshapes the memcpy pattern to satisfy the `WriteStream` concept, enabling GPU device memory to hide behind `any_write_stream`. Error handling delivers errors via `io_result` rather than exceptions:

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

    // cudaMemcpyAsync always transfers the
    // entire buffer in one operation, so
    // write_some never performs a partial write.
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

`cuda_device_stream` satisfies `WriteStream`. Because `cudaMemcpyAsync` always transfers the entire buffer in one operation, `write_some` never performs a partial write. It can be wrapped in `any_write_stream`.

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

The algorithm in `protocol.cpp` is compiled once. At link time, swap the transport. No recompilation. Zero per-operation allocation in all cases because `await_suspend` takes `coroutine_handle<>` - the caller is already type-erased by the language. Section 10 traces the design lineage and the ABI consequence.

## 9. The Type Erasure Asymmetry

The link-time polymorphism shown in Section 8 is not an ergonomic convenience. It is a structural property of how the two models interact with the type system.

**Awaitable under type erasure.** `await_suspend` takes `coroutine_handle<>` - type-erased by the language itself. The awaitable has a fixed, compile-time-known size. The coroutine frame absorbs it. The vtable for `any_write_sink` has four fixed-size entries. Result: zero per-operation allocation, even through a virtual stream interface.

**Sender under type erasure.** `connect(sender, receiver)` produces an operation state whose type depends on both the sender and the receiver. Under type erasure (`any_sender`), the receiver's type is unknown at compile time. The operation state's size is unknown. The coroutine frame cannot absorb it. `any_sender::connect` must heap-allocate. stdexec mitigates this with a 64-byte small buffer optimization, but stdexec's own `system_context` produces operation states of 72-152 bytes - exceeding its own buffer.<sup>[45]</sup>

Benchmark data (20M operations, single thread)<sup>[44]</sup>:

| Stream type | Coroutine (Capy) | Sender pipeline |
|---|---|---|
| Native | 31 ns/op, 0 alloc/op | 34 ns/op, 0 alloc/op |
| Type-erased | 36 ns/op, **0 alloc/op** | 57 ns/op, **1 alloc/op** |

Native performance is comparable - 31 ns vs 34 ns. Under type erasure, the gap widens to 36 ns vs 57 ns, and the sender path incurs one heap allocation per operation. The 21 ns gap and the per-operation allocation are structural. They follow from how each model interacts with type erasure, not from implementation quality.

The same asymmetry applies to any byte-oriented operation that goes through a type-erased interface - GPU memory transfers, network sockets, RDMA queue pairs. For domains where type erasure is the natural interface (protocols compiled once, linked against many transports), the coroutine model has a structural advantage.

The same asymmetry determines which model can provide a stable binary interface for I/O. Section 10 draws this consequence.

## 10. ABI Stability

The type erasure asymmetry in Section 9 has a consequence the committee has wanted for decades: an ABI-stable interface for async I/O.

The vtable for `any_write_stream` has four fixed-size entries: `await_ready`, `await_suspend`, `await_resume`, and `destroy`. The signature `await_suspend(coroutine_handle<>, io_env const*)` is fixed because `coroutine_handle<>` is type-erased by the language itself. The vtable size is known at compile time. The interface can be compiled into a shared library (`.so`/`.dll`) and the implementation swapped without recompiling the consumer.

Sender pipelines cannot provide this property. `connect(sender, receiver)` produces an operation state whose type and size depend on both the sender and the receiver. Every new sender/receiver combination produces a new type - a new ABI surface. There is no fixed vtable. Changing the I/O implementation changes the type, which forces recompilation of every consumer.

This is ABI stability achieved not through heroic engineering or policy constraints but as a structural consequence of the coroutine model's type erasure. The language provides the fixed-type boundary. The committee has struggled with ABI stability for `std::string`, `std::regex`, and across the ABI breakage debates. IoAwaitable delivers it for async I/O as a structural property of the model.

### The abstraction arc

This is the same design trajectory that produced Thrust and C++17 parallel algorithms - a standard interface over hardware-specific implementation.

**Thrust (2009).** GPU parallel algorithms behind an STL-compatible interface. Customers wrote to the STL vocabulary, ran on NVIDIA's GPU. The interface was vendor-neutral: customers could retarget to TBB or OpenMP. N3408 (2012) carried this into C++17 parallel algorithms.<sup>[3]</sup>

**C++17 parallel algorithms.** Standard interface, hardware-specific implementation. Write `std::sort(std::execution::par, ...)`, link against NVIDIA's implementation or Intel's. The standard owns the interface; the vendor owns the implementation.

**IoAwaitable streams.** Write `ingest(any_write_stream&, payload)`, link against NVIDIA's `cuda_device_stream`, AMD's ROCm transport, an RDMA transport, or TCP. Same pattern, applied to data transport instead of parallel algorithms. The abstraction level rises again; the application code stays the same. A demonstration accompanies this paper<sup>[54]</sup> in which the same `ingest` handler is compiled once and exercised against both `cuda_device_stream` and an in-memory `WriteStream`.

### Security patching without recompilation

The ABI-stable boundary means a TLS (Transport Layer Security) stream implementation can be upgraded for a security patch - or swapped out for a different implementation entirely - without recompiling the application. The protocol handler was compiled against `any_write_stream`. The TLS implementation sits behind that interface. Replace the shared library, restart the process.

This is how security-critical infrastructure is maintained in practice: the application binary does not change, only the transport layer underneath it. Senders cannot provide this property because `connect(sender, receiver)` stamps both types into the operation state; changing the TLS implementation changes the type, which forces recompilation of every consumer.

### The complete inference stack

An inference server receives HTTP requests (TCP transport), dispatches to GPU compute (`stdexec` scheduler), moves results through NVLink or InfiniBand (NCCL/RDMA transport), and responds over HTTP. Today, no C++ standard interface covers the data-transport layer. IoAwaitable's ABI-stable streams complete the stack. The protocol handler compiles once and deploys across the full topology - PCIe, NVLink, InfiniBand, Ethernet - without recompilation. Each model serves its natural domain: senders for GPU kernel dispatch where compile-time work graphs deliver their full value, IoAwaitables for data transport where type-erased streams and ABI stability are the natural interface.

## 11. Complicated Success

Byte-oriented operations deliver results as a compound pair: status plus byte count. The pattern spans hardware boundaries. A POSIX `read` returns `(errno, bytes_read)`. A `cudaMemcpyAsync` completion delivers `cudaError_t` alongside the transfer count. An RDMA work completion returns `(wr_id, status, byte_len)`. Both values are always present. A `read` that returns 0 bytes with no error means EOF. A `read` that returns `ECONNRESET` with 47 bytes means 47 bytes arrived before the peer reset the connection. The byte count is not redundant with the error code.

P2300R10<sup>[3]</sup> Section 5.8 acknowledges this: "This begs the question of how they can be used to represent async operations that partially succeed."

The sender model provides three completion channels: `set_value`, `set_error`, and `set_stopped`. A compound I/O result must be routed to one of them:

- Route both values through `set_value`: downstream `upon_error` and `retry` algorithms cannot see the error.
- Route the error through `set_error`: the byte count is lost.
- Route through `set_stopped`: both values are lost.

The best available option is routing both through `set_value` as a compound type. But this means I/O errors bypass the `set_error` channel, disadvantaging sender algorithms that operate on error and stopped channels. P4091R1<sup>[43]</sup> documents all six positions that have been proposed; each carries a cost.

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

Structured bindings deliver both values. No data loss, no channel to choose, no impedance mismatch with downstream algorithms. The application has the full compound result and decides how to handle it.

This is a domain mismatch, not a sender defect. The three-channel model was designed for operations that succeed, fail, or are cancelled - a natural fit for GPU kernel dispatch, where `cudaErrorLaunchFailure` is fatal and carries no partial result. Byte-oriented data movement operates in a domain where partial success is routine and both the status and the byte count must reach the application.

## 12. HPC Networking and Compile-Time Visibility

The sender model's compile-time pipeline visibility eliminates virtual dispatch (approximately 10 ns) and heap allocation (approximately 100 ns). These are real costs in nanosecond-scale GPU kernel dispatch. The question is whether they are measurable at the latency scale of network data transfers.

HPC networking APIs use runtime completion models:

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

Five libraries, five different async models: streams, callbacks, GPU-initiated operations, completion queues, and file-descriptor-based reactor patterns. Zero compile-time work graphs. These are the libraries that run every LLM training cluster, every weather simulation, and every molecular dynamics workload.

Planning decisions in HPC networking are runtime:

- **Topology discovery** happens at communicator creation via `ncclCommInitRank`. NCCL discovers NVLink/NVSwitch/InfiniBand topology and selects ring vs tree algorithms, chooses transports, and builds channel structures. These decisions are driven by hardware probing, not compile-time type information.
- **Compute/communication overlap** is expressed through CUDA stream dependencies via `cudaEventRecord` and `cudaStreamWaitEvent`. The scheduler does not need to see the type of the collective to overlap it with compute; it needs the data dependency, captured by the event.
- **Memory registration** is setup-time: `ibv_reg_mr` pins pages, maps GPU BAR regions, and exchanges rkeys with peers. All done before the first byte moves.

The RDMA completion channel exposes a plain file descriptor (`ibv_comp_channel.fd`) that works with epoll - the same reactor pattern as TCP sockets. The work completion returns `(wr_id, status, byte_len)` - the same compound result pattern. The `wr_id` is a natural coroutine dispatch key.

The stdexec repository focuses on compute scheduling; HPC networking integration is not yet represented. The Maxwell FDTD example uses MPI for communication, invoked manually inside `then()` callbacks - the network I/O is not expressed as senders. Coroutine-based integration could complement stdexec here: NCCL, RDMA, and NVLink all use runtime completion models (streams, callbacks, file descriptors) that map naturally to the IoAwaitable pattern, providing the data-movement layer that compute scheduling sits on top of.

The closest project to sender-based HPC networking in active development is LCI (Lightweight Communication Interface), a C++17 async communication library with libibverbs and libfabric backends and prototype GPU-Direct RDMA, published at SC'25.<sup>[51]</sup> HPX is actively migrating its parallel runtime to stdexec senders, with LCI providing the RDMA transport underneath. This is sender-adjacent HPC networking through a runtime wrapper rather than direct sender composition over the wire protocol, but it suggests the space is being explored.

**Question for the reader:** Is there a per-operation planning decision in HPC networking that benefits from compile-time type visibility of the send/receive calls themselves? For communication patterns known at compile time, the answer may be yes. For data-dependent communication patterns determined at runtime, the question is open.

## 13. Sender-Based Networking: Deployed Evidence

The sender/receiver model has been deployed at scale for compute scheduling and infrastructure (Section 2). The question is whether it has been deployed for byte-oriented data movement - the domain this paper examines.

The largest production deployment of the sender/receiver model is Meta's libunifex, operating at massive scale. Their internal guidance is instructive. From GitHub issue #586<sup>[21]</sup> (December 2023):

> "Our experience at Meta has been that coroutines are easier to read, write, debug, and just generally maintain than composition-of-sender algorithms-style code. The advice we give to internal teams adopting Unifex is that they should prefer coroutines until they know that the overheads are unacceptable."

The team that has shipped sender/receiver at the largest scale recommends coroutines for the common case. This is production evidence from practitioners, not a theoretical preference.

A survey of sender-based networking projects outside Meta:

| Project | Built on | Status |
|---|---|---|
| uring_exec | io_uring + stdexec | Single-developer echo server |
| execution-ucx | UCX + libunifex | RDMA/RPC, not on stdexec |
| beman.net | P2762 + beman.execution | "Not yet ready for production use" |
| kuhllib | Custom senders | Conference demo |
| snp | libunifex + Boost | Dead since August 2023 |
| Asio adapter PR | stdexec PR #1501 | Incomplete |

None are production-grade. The most complete (uring_exec) is a single developer's project with a TCP echo server. P2300R10's<sup>[3]</sup> own HTTP server example is explicitly labeled pseudocode.

SG14, the study group for low-latency systems practitioners, has formally recommended ([P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf))<sup>[22]</sup>: "Networking (SG4) should not be built on top of P2300."

The gap between networking ambition and deployed evidence suggests that data movement and compute dispatch have different enough completion models that a single abstraction does not serve both optimally. The independent validation in Section 14 shows where each model fits naturally. The bridge between models (Section 17) connects the two domains without requiring either to subsume the other.

## 14. Independent Validation

Several independent projects have arrived at the same design: coroutine-based async completion for GPU and HPC data movement, using `cudaLaunchHostFunc` (or its driver-level equivalent `cuLaunchHostFunc`) as the bridge between GPU completion and coroutine resumption.

**cuda-oxide (NVIDIA Labs, Rust).**<sup>[35]</sup> NVIDIA's own research lab implemented the same mechanism in Rust. Their `DeviceFuture` submits GPU work, enqueues a `cuLaunchHostFunc` callback that sets an `AtomicBool` and wakes a Tokio `Waker`, and the async runtime resumes the task on the next poll. Zero busy-wait. The three-state machine (Idle, Executing, Complete) is structurally identical to a network socket future. When NVIDIA's own research lab arrives at the same `cudaLaunchHostFunc`-to-async-runtime pattern independently, in a different language, the convergence is a data point about where the pattern fits naturally.

**CERN wp1.7-coroutine-tests.**<sup>[34]</sup> The ATLAS and LHCb experiments at CERN are evaluating C++20 coroutine patterns for task scheduling, including a Gaudi-framework-inspired coroutine hierarchy and CUDA examples. The project's [`StreamIoAwaitable`](https://github.com/cern-nextgen/wp1.7-coroutine-tests/blob/5049a37d7e74b6e2241b39dca5c81ff3aaece0e3/examples/capy_stream_await.hpp) is built directly on Capy's IoAwaitable protocol: `await_suspend(std::coroutine_handle<>, boost::capy::io_env const*)` enqueues a `cudaLaunchHostFunc` callback that, on CUDA-stream completion, posts the coroutine handle back to `env->executor` - the same `cudaLaunchHostFunc`-to-coroutine resumption described here, implemented independently against Capy's `io_env`.

**Taro (University of Wisconsin-Madison).**<sup>[36]</sup> A C++20 coroutine task-graph system for CPU-GPU workloads. GPU tasks suspend the CPU thread via coroutines when waiting for GPU completion, allowing other tasks to run. Uses `cudaLaunchHostFunc` for the callback. Published at Euro-Par 2024 and presented at CppCon 2023. Reported 40-80% speedup over blocking approaches.

**async-cuda (Oddity AI, Rust, production).**<sup>[37]</sup> A production library whose authors state: "Since the GPU is just another I/O device (from the point of view of your program), the async model actually fits surprisingly well."

**Schr&ouml;dinger Desmond (production, GTC 2024).**<sup>[38]</sup> The Desmond molecular dynamics engine uses C++ coroutines to overlap multiple GPU simulations. Coroutines suspend when a simulation hits a serial bottleneck, allowing another simulation to use the GPU. Presented at GTC 2024. Achieved up to 2.02x speedup in FEP+ drug discovery workloads. Coroutines were chosen because they could "retrofit into existing CUDA code without complex code restructuring."

**TTG/PaRSEC (DOE Exascale Computing Project).**<sup>[39]</sup> A template task graph framework where `co_await ttg::device::select(...)` and `co_await ttg::device::wait(...)` are the primary mechanism for GPU task dispatch. Supports CUDA, HIP/ROCm, and Intel Level Zero. The project states that "the use of coroutines is the primary reason why TTG requires C++20 support."

**RDMA coroutine libraries.** Three independent projects wrap RDMA verbs as coroutine awaitables: RDMA++ (rdmapp)<sup>[40]</sup> wraps libibverbs with C++20 coroutines using `ibv_comp_channel` fd; Loom<sup>[41]</sup> provides C++23 typed bindings over libfabric with `co_await ep.async_receive(buf, asio::use_awaitable)`; and FORD<sup>[42]</sup> (USENIX FAST 2022) implements coroutine-enabled distributed transactions over one-sided RDMA, spawning multiple follow-on systems (Motor, CREST at ASPLOS 2026).

These projects span GPU compute, molecular dynamics, high-energy physics, RDMA networking, and distributed systems. They were built by independent teams with no coordination. The convergence on coroutine-based async completion for data movement is a data point about where the pattern fits naturally. Several of these projects (Taro, TTG/PaRSEC, Desmond) also demonstrate coroutine-based kernel dispatch and GPU pipeline orchestration in production, placing that evidence in the record without this paper needing to reproduce it.

**Question for the reader:** Are we reading this landscape correctly? Are there significant projects using the `cudaLaunchHostFunc`-to-coroutine pattern that we have missed?

## 15. CUDA Graphs

Sender pipelines provide compile-time `operation_state` fusion. [P3425R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3425r1.html)<sup>[23]</sup> documents 8 bytes saved per nesting level via constant pointer offsets. This is real.

CUDA Graphs<sup>[24]</sup> provide GPU-side work-graph optimization at the driver level. The driver sees SM count, memory bandwidth, occupancy, and hardware topology. Stream capture<sup>[8]</sup> records kernel DAGs:

```c
cudaStreamBeginCapture(stream,
    cudaStreamCaptureModeGlobal);
kernel_A<<<grid, block, 0, stream>>>(args);
kernel_B<<<grid, block, 0, stream>>>(args);
cudaStreamEndCapture(stream, &graph);

cudaGraphInstantiate(&instance, graph, 0);
cudaGraphLaunch(instance, stream);
```

The quantitative picture:

- Graph replay: approximately 2.5 us for the entire graph on CUDA 12.6+.<sup>[25]</sup>
- For 100 sequential kernels: stream launch approximately 400 us vs graph launch approximately 2.5 us - a 160x reduction.<sup>[25]</sup>
- In DALLE2 inference (740 kernels, 3.4ms GPU time), 75% of end-to-end latency is CPU launch delays.<sup>[26]</sup>

CUDA Graphs and sender compile-time fusion optimize different layers. CUDA Graphs eliminate per-kernel CPU-GPU dispatch round trips at the driver level - language transitions, runtime processing, driver operations totaling 20-200 us per kernel in DL applications.<sup>[25]</sup> Sender fusion eliminates host-side C++ abstraction overhead - allocations, virtual dispatch, type erasure - at the language level. nvexec intercepts sender algorithms and replaces them with CUDA kernel launches on streams, but does not automatically batch them into CUDA Graphs; per-kernel host launch overhead remains unless CUDA Graphs are used separately.<sup>[12]</sup> These are complementary optimizations, not substitutes.

CUDA Graph replay composes naturally with coroutine-based data movement: the coroutine provides the outer loop with data-dependent control flow (memcpy in, graph launch, memcpy out, check result), and the pre-captured graph is the inner optimized hot path. Schr&ouml;dinger's Desmond engine (GTC 2024)<sup>[38]</sup> demonstrates this composition in production, using coroutines to overlap multiple GPU simulations around CUDA Graph replay with up to 2.02x speedup in drug discovery workloads.

**Question for the reader:** Sender fusion and CUDA Graphs optimize at different layers. Does sender fusion provide value in combination with CUDA Graphs, or does graph capture at the driver level subsume the host-side optimization? Are there GPU workloads where coroutine orchestration around pre-captured graphs would be useful, or does this pattern miss something fundamental about how GPU pipelines are structured?

## 16. The Frame Allocation Question

Each coroutine suspension potentially allocates a frame. Sender `operation_state` is a single compile-time allocation. This is a real structural difference.

### HALO

Heap Allocation eLision Optimization<sup>[27]</sup> allows the compiler to place the coroutine frame in the caller's frame when the lifetime is provably bounded. Capy's `task` is annotated with `[[clang::coro_await_elidable]]`<sup>[28]</sup> to enable this.

HALO is fragile: the attribute was introduced<sup>[29]</sup> because "real-world Task types are rarely simple enough for CoroElide's SSA analysis." Confirmed regressions in Clang 19-20.<sup>[30]</sup> Correctness bug with `suspend_never`.<sup>[31]</sup> Parentheses around a `co_await` operand silently break elision.<sup>[32]</sup> Clang-only. HALO is nice when it fires. It is not something to rely on.

### PMR pools

Capy's `io_env` carries a `std::pmr::memory_resource*`.<sup>[33]</sup> Thread-local recycling pools amortize allocation cost to near zero. This is reliable, portable, and works regardless of compiler optimization.

| Operation | Time |
|---|---|
| Coroutine frame alloc (PMR pool) | 2-5 ns |
| Coroutine frame alloc (malloc) | 30-60 ns |
| CUDA kernel launch (C++) | 1,000-5,000 ns |
| `cudaMemcpy` (4 bytes) | 10,000 ns |
| CUDA Graph replay (entire graph) | 2,500 ns |
| Conv2d forward (A100, BS=1) | 24,000 ns |
| NCCL AllReduce (600B model) | 1,000,000,000+ ns |

A coroutine frame allocation with a PMR pool is 200x-100,000x cheaper than the GPU operations it orchestrates. For a 900B-parameter model's AllReduce that takes seconds, the 5 ns frame allocation is nine orders of magnitude smaller.

One caveat: the latency table assumes GPU operations in the microsecond-to-second range. For high-frequency kernel dispatch where individual kernel execution times approach the sub-microsecond regime, the frame allocation cost relative to the operation cost may be different. Additionally, `cudaLaunchHostFunc` callback latency can spike to 12ms on loaded multi-GPU systems,<sup>[48]</sup> which means the callback dispatch latency can dominate both frame allocation and the GPU operation itself. The 2-5 ns frame allocation cost is not always the relevant comparison.

**Question for the reader:** Is our assumption about the relative cost of frame allocation accurate at GPU workload scale? Are there scenarios in high-frequency kernel dispatch where coroutine frame allocation becomes a measurable bottleneck?

## 17. The Bridge Between Domains

The preceding sections argue that senders and IoAwaitables each serve a domain well: senders for GPU kernel dispatch and heterogeneous scheduling, IoAwaitables for byte-oriented I/O and type-erased streams. The bridge is where the domains meet.

Capy provides two bridge functions with working implementations in its bench and example code<sup>[54]</sup>: `await_sender`<sup>[52]</sup> consumes a sender from within a coroutine via `co_await`, and `as_sender`<sup>[53]</sup> wraps an IoAwaitable as a P2300 sender for use in a sender pipeline. Both compile and run today. One bridge direction currently relies on behavior the standard would need to bless; [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf)<sup>[52]</sup> and [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf)<sup>[53]</sup> are the dedicated design papers for each direction.

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

Network I/O uses `any_read_source` and `any_write_sink` - type-erased, zero per-operation allocation, compound results via structured bindings. GPU dispatch uses `nvexec::launch` on the stream scheduler - compile-time composition, scheduler-agnostic portability. Because nvexec runs the launched work on the device, `run_model` is a `__device__` function and the trailing `stdexec::continues_on(cpu)` returns completion to the host before the host-only `await_sender` bridge resumes the coroutine - so the handler takes a host scheduler alongside the GPU context. The `await_sender` bridge connects the two without requiring either model to subsume the other.

The network transport behind `client` and `response` can be TCP, TLS, RDMA, or any transport that satisfies the stream concepts. The GPU scheduler can be `nvexec::stream_scheduler`, a CPU thread pool, or any scheduler that provides `schedule()`. Neither side needs to know about the other's implementation.

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

## 18. Considerations

The preceding sections present convergent findings. This section addresses foreseeable concerns about the conclusions drawn from them.

### 18.1 Laziness and Composition

**Awaitables commit to eager execution.** Awaitables are lazy. `write_some` returns an inert object. No `cudaMemcpyAsync` is issued, no syscall is made, until `co_await` triggers `await_suspend`. The trigger is explicit in both models: senders do no work until `start()` is called; awaitables do no work until `co_await` is evaluated. A coroutine can capture the awaitable, defer the `co_await`, and decide at runtime whether to submit the operation. This concern does not distinguish the two models.

**The scheduler cannot see the full task graph.** Sender pipelines compose as a graph the scheduler can inspect before `start()`. This is valuable for GPU kernel dispatch where the work graph is known ahead of time - CUDA Graphs (Section 15) exploit this property at the driver level, achieving 160x launch-overhead reduction for 100 sequential kernels.<sup>[25]</sup> Data movement is different. The next transfer depends on the result of the previous one: how many bytes arrived, whether the peer reset the connection, whether the RDMA completion carried an error. There is no static graph to inspect because control flow branches on runtime data. NCCL topology discovery, RDMA memory registration, and NVLink channel selection are all runtime decisions driven by hardware probing (Section 12). Coroutine control flow - `if`, `for`, `while` - is the natural expression of data-dependent sequential decisions.

**Senders separate description from execution; coroutines conflate them.** The separation is valuable when the same algorithm can run on CPU or GPU by swapping the scheduler. The Maxwell FDTD benchmark demonstrates this: identical sender code achieves parity with raw CUDA on GPU and runs correctly on a CPU thread pool (Section 2). Data movement operations are bound to specific hardware resources at submission time. A `cudaMemcpyAsync` targets a specific CUDA stream on a specific device. An `ibv_post_send` targets a specific queue pair on a specific HCA. A `read` targets a specific file descriptor. The description cannot be retargeted by swapping a scheduler because the operation is bound to the resource. For compute dispatch, description-execution separation enables scheduler-agnostic portability. For data transport, the binding to hardware resources makes the separation vacuous.

### 18.2 Consumer Choice and Return Types

**Data movement operations should return senders so the caller can choose how to consume them.** The choice is symmetric. `as_sender`<sup>[53]</sup> wraps an awaitable for sender pipeline consumption. `await_sender`<sup>[52]</sup> wraps a sender for coroutine consumption. Neither return type gives every consumer zero-cost access. Returning a sender forces a per-operation allocation under type erasure (Section 9: 57 ns/op, 1 alloc/op). Returning an awaitable preserves zero-allocation type erasure (Section 9: 36 ns/op, 0 alloc/op) and gives sender pipeline consumers access through `as_sender`. The question is which consumer bears the cost. For data movement where the protocol handler is compiled once against a type-erased stream (Section 8), the type-erased consumer is the common case. P4088R1<sup>[44]</sup> Section 10 documents the full design fork analysis.

**The bridge proves senders are more fundamental.** The bridge is symmetric. `as_sender`<sup>[53]</sup> wraps an awaitable for sender consumption. `await_sender`<sup>[52]</sup> wraps a sender for coroutine consumption. CPU and GPU interact through memory copies; that does not make one side more fundamental. The bridge is evidence of complementarity between models that serve different domains - compute dispatch and data transport - not evidence of hierarchy. P4088R1<sup>[44]</sup> Section 9 addresses this directly.

### 18.3 Type Erasure and Allocation

**Type erasure should be opt-in, not baked into the abstraction.** Byte-oriented data movement is a domain where the transport is inherently runtime-determined. An inference server does not know at compile time whether input arrives over TCP, RDMA, or NVLink - the transport depends on the deployment topology, which is discovered at communicator creation time via `ncclCommInitRank` or equivalent (Section 12). Type erasure is the natural interface for this domain, not an optional convenience. Senders' compile-time visibility optimizes for static dispatch, which is not the bottleneck when every operation crosses a kernel boundary (1,000-5,000 ns) or a PCIe bus (10,000+ ns). This is the same design trajectory traced in Section 10. P4088R1<sup>[44]</sup> Section 7.1 documents the structural mechanism.

**Coroutine frames allocate; sender operation states do not.** Acknowledged. Sender `operation_state` is a compile-time construct with no heap allocation. Coroutine frames allocate. PMR pools amortize this to near zero (Section 16). The relevant comparison for data movement is total allocation across the stream's lifetime. Under type erasure, the sender model allocates once per `any_sender::connect` (Section 9). The coroutine model allocates once per frame (Section 9). For N operations through a type-erased stream, the coroutine model allocates once; the sender model allocates N times. P4088R1<sup>[44]</sup> Sections 4 and 7.9 cover the general case.

**Compile-time optimization is lost.** Coroutine handles are opaque; the compiler cannot see through `resume()`. Sender pipelines are fully visible, statically dispatched, inlinable. This visibility matters for GPU kernel dispatch where individual operations cost nanoseconds and the compiler can fuse host-side abstraction overhead (Section 2). The latency scale of data movement dwarfs indirect-call overhead (Section 16). The optimization target for data movement is allocation elimination under type erasure (Section 9), not call devirtualization. P4088R1<sup>[44]</sup> Section 4 documents the optimization barrier.

### 18.4 Composition and Algorithms

**Senders provide 30 generic algorithms; awaitables provide none.** The awaitable composition mechanism is the language's own control flow: `if`, `for`, `while`, `try/catch`, structured bindings. These compose naturally with data-dependent decisions - the `if(ec == errc::connection_reset)` in Section 11 is a branch on runtime data that determines the next operation. For GPU dispatch where the full work graph must be visible to the scheduler before launch, the sender composition algebra is justified (Section 2). For data movement where each operation depends on the result of the previous one, ordinary control flow is the natural mechanism and is debuggable with standard tools. P4088R1<sup>[44]</sup> Section 2.2 compares the two vocabularies.

**Compound results can be routed through set_value.** Route `(error_code, bytes_transferred)` through `set_value` as a compound type. This is physically possible. It is also what Section 11 documents: if all data-movement results route through `set_value`, then `set_error` and `set_stopped` are vestigial for these operations. The three-channel model's value - that different channels enable different downstream algorithms (`retry`, `upon_error`) - is nullified. P2300R10<sup>[3]</sup> Section 5.8 acknowledges: "This begs the question of how they can be used to represent async operations that partially succeed." The three channels match GPU kernel dispatch, where `cudaErrorLaunchFailure` is fatal and carries no partial result. Byte-oriented operations produce compound results where both status and byte count are always present. P4091R1<sup>[43]</sup> analyzes all six positions.

### 18.5 Scope and Evidence

**Structured concurrency is weaker in the coroutine model.** Acknowledged (Section 2). Senders provide `counting_scope` for dynamic fan-out with guaranteed completion before scope destruction. Coroutines provide lexical-scope safety via `when_all` but dynamic fan-out needs explicit library support. Data movement is inherently sequential - one buffer at a time, one completion at a time, the one-at-a-time invariant on the CUDA stream (Section 7). Dynamic fan-out belongs to the compute dispatch domain, where senders provide it.

**The sender-based networking survey may be incomplete.** The survey (Section 13) is as comprehensive as the authors could make it. If production-grade sender-based networking or data-movement implementations exist that the survey has missed, their evidence would strengthen the case for sender-based I/O. The paper will be updated with any additions.

**The CUDA examples were generated with AI assistance.** Disclosed in Section 1. The examples are presented as a research exercise for evaluation by domain experts. Corrections are invited. Errors in the CUDA code would indicate where the examples need refinement; they would not invalidate the structural observation that five independent projects (Section 14) converged on the same `cudaLaunchHostFunc`-to-coroutine pattern without coordination.

**The paper's P2300R10 quotations may be taken out of context.** All quotations include section numbers. Readers can verify context at the cited locations in P2300R10.<sup>[3]</sup> Corrections are welcome if any quotation misrepresents the original intent.

## 19. Conclusion

A protocol handler compiled once links against TCP, RDMA, or GPU device memory without recompilation. This is possible because byte-oriented data movement - host-device memcpy, inter-GPU collectives over NVLink, RDMA transfers between nodes, and TCP sockets - shares a common async completion model that the IoAwaitable protocol captures with zero per-operation allocation. The CUDA Programming Guide confirms that single-stream callbacks are strictly serialized,<sup>[6]</sup> enabling the same pre-allocated op-state pattern that networking sockets use. Independent projects at NVIDIA Research (cuda-oxide),<sup>[35]</sup> CERN,<sup>[34]</sup> the University of Wisconsin-Madison (Taro),<sup>[36]</sup> and Schr&ouml;dinger (Desmond)<sup>[38]</sup> have converged on the same `cudaLaunchHostFunc`-to-coroutine pattern without coordination.

`cudaLaunchHostFunc` has documented limitations (Section 7) that bound the applicability of the pattern in high-throughput GPU pipelines.

`std::execution` provides real properties for GPU dispatch: zero-allocation compile-time composition, scheduler-agnostic portability, domain customization via `transform_sender`, and structured concurrency for dynamic fan-out. These properties stand without qualification. CUDA Graphs and sender fusion optimize at different layers - graphs reduce driver-level dispatch overhead, sender fusion reduces host-side C++ abstraction overhead - and they are complementary.

Independent projects (Taro, TTG/PaRSEC, Desmond) have demonstrated the extension of the coroutine pattern to kernel dispatch and GPU pipeline orchestration in production, placing that evidence in the record alongside this paper's byte-movement analysis.

Bridges (`await_sender`<sup>[52]</sup>, `as_sender`<sup>[53]</sup>) connect the two models where the domains meet. A networking coroutine consumes a GPU sender for compute dispatch. A sender pipeline wraps an IoAwaitable for composition. Neither model needs to subsume the other. Each serves the domain where its design choices pay off: senders for compute dispatch where compile-time work graphs and scheduler-agnostic portability deliver their full value, awaitables for data transport where type-erased streams, zero-allocation link-time polymorphism, and ABI stability (Section 10) are the natural interface. The abstraction level rises; the application code stays the same.

This convergent evidence supports the standardization of the IoAwaitable protocol proposed in [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.html).<sup>[46]</sup> The committee should not assume senders are the only viable model for GPU async when GPU practitioners are independently choosing coroutines for data movement. The IoAwaitable protocol provides the minimal execution model - executor affinity, cancellation, frame allocation - that these convergent projects need from the standard. Standardizing it gives the ecosystem a stable foundation without requiring either model to subsume the other.

## Acknowledgements

Eric Niebler, Micha&lstrok; Dominiak, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Bryce Adelstein Lelbach, Dietmar K&uuml;hl, and Jens Maurer, whose work on `std::execution` (P2300R10) this paper examines and builds upon.

Richard Smith and Gor Nishanov for P0981R0 (HALO analysis). Chuanqi Xu for the `[[clang::coro_await_elidable]]` attribute and P2477R3 (coroutine allocation elision). Dietmar K&uuml;hl and Maikel Nadolski for P3552R3 (`std::execution::task`). Lewis Baker for cppcoro, the operator `co_await` and symmetric transfer blog posts, and P3425R1 (operation-state sizes). Michael Wong for P4029R0 (SG14 priority list).

Michael Garland and the NVIDIA stdexec team for the nvexec GPU schedulers and the Maxwell FDTD benchmark. The CERN wp1.7 team for their C++20 coroutine task-scheduling experiments and the Capy IoAwaitable integration. Dian-Lun Lin (University of Wisconsin-Madison) for Taro and its CppCon 2023 presentation. The NVIDIA Labs team for cuda-oxide. Jiqun Tu (NVIDIA) and Ellery Russell (Schr&ouml;dinger) for the Desmond coroutine integration presented at GTC 2024. The TTG/PaRSEC team for demonstrating coroutine-based heterogeneous GPU dispatch at DOE Exascale scale.

This paper was generated with AI assistance (Claude, via Cursor).

## References

[1] [Capy](https://github.com/cppalliance/capy) (C++ Alliance).

[2] [Corosio](https://github.com/cppalliance/corosio) (C++ Alliance).

[3] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Eric Niebler, Micha&lstrok; Dominiak, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Bryce Adelstein Lelbach, 2024).

[4] [nvexec stream_context.cuh](https://github.com/NVIDIA/stdexec/blob/main/include/nvexec/stream_context.cuh) - NVIDIA stdexec GPU scheduler.

[5] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec) - Reference implementation of `std::execution`.

[6] [CUDA Programming Guide: Asynchronous Concurrent Execution](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html) (NVIDIA, 2024).

[7] [CUDA Runtime API: Event Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EVENT.html) (NVIDIA, 2024).

[8] [CUDA Runtime API: Stream Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__STREAM.html) (NVIDIA, 2024).

[9] [CUDA Runtime API: Execution Control](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EXECUTION.html) (NVIDIA, 2024).

[10] [CUDA Handbook: Stream Callbacks](https://www.cudahandbook.com/2012/09/stream-callbacks/) (Nicholas Wilt, 2012).

[11] [Stack Overflow: Exception Handling in cudaLaunchHostFunc Callbacks](https://stackoverflow.com/questions/75145603/catching-an-exception-thrown-from-a-callback-in-cudalaunchhostfunc) (2023).

[12] [DeepWiki: nvexec GPU Execution](https://deepwiki.com/NVIDIA/stdexec/6-gpu-execution-with-nvexec).

[13] [Capy io_env](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/include/boost/capy/ex/io_env.hpp) (C++ Alliance).

[14] [Capy executor_ref](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/include/boost/capy/ex/executor_ref.hpp) (C++ Alliance).

[15] [Understanding Symmetric Transfer](https://lewissbaker.github.io/2020/05/11/understanding_symmetric_transfer) (Lewis Baker, 2020).

[16] [Capy continuation](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/include/boost/capy/continuation.hpp) (C++ Alliance).

[17] [Capy task](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/include/boost/capy/task.hpp) (C++ Alliance).

[18] [CUDA Runtime API: Memory Management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY.html) (NVIDIA, 2024).

[19] [CUDA Programming Guide: Page-Locked Host Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html) (NVIDIA, 2024).

[20] [CUDA Runtime API: API Synchronization Behavior](https://docs.nvidia.com/cuda/cuda-runtime-api/api-sync-behavior.html) (NVIDIA, 2024).

[21] [libunifex Issue #586](https://github.com/facebook/libunifex/issues/586) - Meta internal guidance on senders vs coroutines (2023).

[22] [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf) - "The SG14 Priority List for C++29/32" (Michael Wong, 2026).

[23] [P3425R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3425r1.html) - "Reducing operation-state sizes for subobject child operations" (Lewis Baker, 2025).

[24] [CUDA Programming Guide: CUDA Graphs](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html) (NVIDIA, 2024).

[25] [NVIDIA CUDA Graph Best Practices: Quantitative Benefits](https://docs.nvidia.com/dl-cuda-graph/cuda-graph-basics/cuda-graph.html) (NVIDIA, 2024).

[26] [PyGraph: Robust Compiler Support for CUDA Graphs in PyTorch](https://arxiv.org/html/2503.19779v3) (2025).

[27] [P0981R0](https://www.open-std.org/JTC1/SC22/WG21/docs/papers/2018/p0981r0.html) - "Halo: coroutine Heap Allocation eLision Optimization: the joint response" (Richard Smith, Gor Nishanov, 2018).

[28] [Clang Attribute Reference: coro_await_elidable](https://clang.llvm.org/docs/AttributeReference.html#coro-await-elidable) (LLVM).

[29] [LLVM PR #99282: Introduce coro_await_elidable](https://github.com/llvm/llvm-project/pull/99282) (Chuanqi Xu, 2024).

[30] [LLVM Issue #64586: CoroElide failures and regressions](https://github.com/llvm/llvm-project/issues/64586).

[31] [LLVM Issue #188230: HALO + suspend_never bad-free](https://github.com/llvm/llvm-project/issues/188230).

[32] [LLVM Issue #178256: Parentheses break coro_await_elidable](https://github.com/llvm/llvm-project/issues/178256).

[33] [std::pmr::memory_resource](https://en.cppreference.com/w/cpp/memory/memory_resource) (cppreference).

[34] [cern-nextgen/wp1.7-coroutine-tests](https://github.com/cern-nextgen/wp1.7-coroutine-tests/tree/5049a37d7e74b6e2241b39dca5c81ff3aaece0e3) - CERN C++20 coroutine task-scheduling experiments, including a Capy IoAwaitable that resumes a coroutine from a `cudaLaunchHostFunc` callback ([`examples/capy_stream_await.hpp`](https://github.com/cern-nextgen/wp1.7-coroutine-tests/blob/5049a37d7e74b6e2241b39dca5c81ff3aaece0e3/examples/capy_stream_await.hpp)), pinned at commit `5049a37` (2026).

[35] [cuda-oxide: The DeviceOperation Model](https://nvlabs.github.io/cuda-oxide/async-programming/the-device-operation-model.html) - NVIDIA Labs async GPU programming in Rust (2026).

[36] [Taro](https://github.com/dian-lun-lin/taro) - C++20 coroutine task-graph system for CPU-GPU workloads (Dian-Lun Lin, University of Wisconsin-Madison, 2024).

[37] [async-cuda](https://github.com/oddity-ai/async-cuda) - Async CUDA for Rust (Oddity AI, 2024).

[38] [Optimizing Drug Discovery with CUDA Graphs, Coroutines, and GPU Workflows](https://developer.nvidia.com/blog/optimizing-drug-discovery-with-cuda-graphs-coroutines-and-gpu-workflows/) - NVIDIA Developer Blog (Jiqun Tu, Ellery Russell, 2024).

[39] [TTG (Template Task Graph)](https://github.com/TESSEorg/ttg) - C++20 coroutine-based heterogeneous task graph on PaRSEC (2024).

[40] [rdmapp](https://github.com/howardlau1999/rdmapp) - C++20 coroutine wrapper for libibverbs (2024).

[41] [Loom](https://github.com/sielicki/loom) - C++23 typed interface over libfabric with Asio coroutine integration.

[42] [FORD](https://github.com/minghust/ford) - Coroutine-enabled distributed transactions over one-sided RDMA (USENIX FAST 2022).

[43] [P4091R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4091r1.pdf) - "Error Models of Regular C++ and the Sender Sub-Language" (Vinnie Falco, 2026).

[44] [P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[45] [P4123R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4123r0.pdf) - "The Cost of Senders for Coroutine I/O" (Vinnie Falco, 2026).

[46] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.html) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[47] [Stack Overflow: CUDA Graph host execution nodes in different streams](https://stackoverflow.com/questions/75739969/is-it-possible-to-execute-more-than-one-cuda-graphs-host-execution-node-in-diff) - Robert Crovella (NVIDIA) on single-stream callback serialization (2023).

[48] [NVIDIA Developer Forums: cuLaunchHostFunc overhead latency](https://forums.developer.nvidia.com/t/culaunchhostfunc-overhead-latency-usage-cpu-gpu-signaling/327066) - Latency spikes up to 12ms on loaded A100/H100 systems (2024).

[49] [NVIDIA Developer Forums: Do stream callbacks hold CUDA-internal locks?](https://forums.developer.nvidia.com/t/do-stream-callbacks-hold-any-cuda-internal-locks/337769) - Deadlock risk with user locks in callbacks (2024).

[50] [Multipath Memory Access: Breaking Host-GPU Bandwidth Bottlenecks in LLM Serving](https://arxiv.org/html/2512.16056v2) - cudaLaunchHostFunc unidirectional notification limitation (2025).

[51] [LCI: A Lightweight Communication Interface](https://arxiv.org/html/2505.01864v2) - C++17 async communication library with libibverbs and libfabric backends, prototype GPU-Direct RDMA, SC'25 (2025).

[52] [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[53] [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[54] [Accompanying examples](https://github.com/cppalliance/capy/tree/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/example) - the compileable demonstrations for this paper, pinned at commit `98be9fd` of the official repository (C++ Alliance). Sections 6-8 and 14 (`cuda_stream`, `cuda_device_stream`, CUDA Graphs): [`example/cuda/datamovement`](https://github.com/cppalliance/capy/tree/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/example/cuda/datamovement). Section 16 (the `await_sender` bridge, `handle_request`): [`example/cuda/pipeline/cuda_pipeline.cu`](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/example/cuda/pipeline/cuda_pipeline.cu). Sections 10-11 (compound results and HPC-fabric signatures): [`example/fabrics/fabrics.cpp`](https://github.com/cppalliance/capy/blob/98be9fdd59b2099b2f4f3a0f2abd4f3d4034d0a6/example/fabrics/fabrics.cpp).
