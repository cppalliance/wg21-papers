//
// Copyright (c) 2025 Vinnie Falco (vinnie dot falco at gmail dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
// Official repository: https://github.com/cppalliance/wg21-papers/coro-first-io
//

#ifndef BENCH_CO_HPP
#define BENCH_CO_HPP

#include "bench.hpp"
#include "bench_co_detail.hpp"

#include <exception>
#include <memory>

#ifdef __clang__
#define CORO_AWAIT_ELIDABLE [[clang::coro_await_elidable]]
#else
#define CORO_AWAIT_ELIDABLE
#endif

namespace co {

//----------------------------------------------------------

/** A concept for types that can dispatch coroutines and post work items.

    An executor is responsible for scheduling and running asynchronous
    operations. It provides mechanisms for symmetric transfer of coroutine
    handles and for queuing work items to be executed later.

    Given:
    @li `t` a const reference to type `T`
    @li `h` a coroutine handle (`std::coroutine_handle<void>`)
    @li `w` a pointer to a work item (`work*`)

    The following expressions must be valid:
    @li `t.dispatch(h)` - Returns a coroutine handle for symmetric transfer
    @li `t.post(w)` - Queues a work item for later execution
    @li `t == t` - Equality comparison returns a boolean-convertible value

    @tparam T The type to check for executor conformance.
*/
template<class T>
concept is_executor = requires(T const& t, coro h, work* w) {
    { t.dispatch(h) } -> std::convertible_to<coro>;
    t.post(w);
    { t == t } -> std::convertible_to<bool>;
};

/** A concept for types that can allocate and deallocate memory for coroutine frames.

    Frame allocators are used to manage memory for coroutine frames, enabling
    custom allocation strategies such as pooling to reduce allocation overhead.

    Given:
    @li `a` a reference to type `A`
    @li `p` a void pointer
    @li `n` a size value (`std::size_t`)

    The following expressions must be valid:
    @li `a.allocate(n)` - Allocates `n` bytes and returns a pointer to the memory
    @li `a.deallocate(p, n)` - Deallocates `n` bytes previously allocated at `p`

    @tparam A The type to check for frame allocator conformance.
*/
template<class A>
concept frame_allocator = requires(A& a, void* p, std::size_t n) {
    { a.allocate(n) } -> std::convertible_to<void*>;
    { a.deallocate(p, n) } -> std::same_as<void>;
};

/** A concept for types that provide access to a frame allocator.

    Types satisfying this concept can be used as the first or second parameter
    to coroutine functions to enable custom frame allocation. The promise type
    will call `get_frame_allocator()` to obtain the allocator for the coroutine
    frame.

    Given:
    @li `t` a reference to type `T`

    The following expression must be valid:
    @li `t.get_frame_allocator()` - Returns a reference to a type satisfying
        `frame_allocator`

    @tparam T The type to check for frame allocator access.
*/
template<class T>
concept has_frame_allocator = requires(T& t) {
    { t.get_frame_allocator() } -> frame_allocator;
};

//----------------------------------------------------------

/** A type-erased reference to an executor.

    This class provides a non-owning, type-erased wrapper around any type
    that satisfies the `is_executor` concept. It enables polymorphic executor
    usage without virtual functions by storing a pointer to a static vtable
    of function pointers.

    The executor_ref does not own the executor it references. The caller must
    ensure the referenced executor outlives the executor_ref.

    @see is_executor
*/
struct executor_ref
{
    struct ops
    {
        coro (*dispatch_coro)(void const*, coro) = nullptr;
        void (*post_work)(void const*, work*) = nullptr;
        bool (*equals)(void const*, void const*) = nullptr;
    };

    template<class Executor>
    static constexpr ops ops_for{
        [](void const* p, coro h) { return static_cast<Executor const*>(p)->dispatch(h); },
        [](void const* p, work* w) { static_cast<Executor const*>(p)->post(w); },
        [](void const* a, void const* b) {
            return *static_cast<Executor const*>(a) == *static_cast<Executor const*>(b);
        }
    };

    ops const* ops_ = nullptr;
    void const* ex_ = nullptr;

    executor_ref() = default;

    executor_ref(executor_ref const&) = default;
    executor_ref& operator=(executor_ref const&) = default;

    template<is_executor Executor>
    executor_ref(Executor const& ex) noexcept
        requires (!std::is_same_v<std::remove_cvref_t<Executor>, executor_ref>)
        : ops_(&ops_for<Executor>)
        , ex_(&ex)
    {
    }

    coro dispatch(coro h) const { return ops_->dispatch_coro(ex_, h); }
    void post(work* w) const { ops_->post_work(ex_, w); }

    bool operator==(executor_ref const& other) const noexcept
    {
        return ops_ == other.ops_ && ops_->equals(ex_, other.ex_);
    }
};

//----------------------------------------------------------

/** A simulated asynchronous socket for benchmarking coroutine I/O.

    This class models an asynchronous socket that provides I/O operations
    returning awaitable types. It demonstrates the affine awaitable protocol
    where the awaitable receives the caller's executor for completion dispatch.

    The socket owns a frame allocator pool that coroutines using this socket
    can access via `get_frame_allocator()`. This enables allocation elision
    for coroutine frames when the socket is passed as a parameter.

    @note This is a simulation for benchmarking purposes. Real implementations
    would integrate with OS-level async I/O facilities.

    @see async_read_some_t
    @see has_frame_allocator
*/
struct socket
{
    struct async_read_some_t
    {
        async_read_some_t(socket& s) : s_(s) {}
        bool await_ready() const noexcept { return false; }
        void await_resume() const noexcept {}

        // Affine overload: receives dispatcher from caller
        // Returns noop_coroutine because we post, not dispatch
        template<class Executor>
        std::coroutine_handle<> await_suspend(coro h, Executor const& ex) const
        {
            s_.do_read_some(h, executor_ref(ex));
            return std::noop_coroutine();
        }

    private:
        socket& s_;
    };

    socket()
        : read_op_(new read_state)
        , pool_(detail::frame_pool::make_global())
    {
    }

    // Asynchronous operation that wraps OS-level I/O
    async_read_some_t async_read_some()
    {
        return async_read_some_t(*this);
    }

    // Frame allocator for coroutines using this socket
    detail::frame_pool& get_frame_allocator()
    {
        return pool_;
    }

private:
    struct read_state : work
    {
        coro h_;
        executor_ref ex_;
    
        void operator()() override
        {
            // Symmetric transfer: dispatch returns the handle
            // The event loop will resume it
            ex_.dispatch(h_)();
        }

        // OVERLAPPED, HANDLE, etc
    }; 

    void do_read_some(coro h, executor_ref const& ex)
    {
        // This definition can go in the TU
        read_op_->h_ = h;
        read_op_->ex_ = ex;
        ex.post(read_op_.get()); // simulate OS call
    }

    std::unique_ptr<read_state> read_op_;
    detail::frame_pool pool_;
};

//----------------------------------------------------------

/** A coroutine task type implementing the affine awaitable protocol.

    This task type represents an asynchronous operation that can be awaited.
    It implements the affine awaitable protocol where `await_suspend` receives
    the caller's executor, enabling proper completion dispatch across executor
    boundaries.

    Key features:
    @li Lazy execution - the coroutine does not start until awaited
    @li Symmetric transfer - uses coroutine handle returns for efficient resumption
    @li Executor inheritance - inherits caller's executor unless explicitly bound
    @li Custom frame allocation - supports frame allocators via first/second parameter

    The task uses `[[clang::coro_await_elidable]]` (when available) to enable
    heap allocation elision optimization (HALO) for nested coroutine calls.

    @par Frame Allocation
    The promise type provides custom operator new overloads that detect
    `has_frame_allocator` on the first or second coroutine parameter,
    enabling pooled allocation of coroutine frames.

    @see executor_ref
    @see has_frame_allocator
    @see detail::frame_pool
*/
struct CORO_AWAIT_ELIDABLE task
{
    struct promise_type
    {
        executor_ref ex_;
        executor_ref caller_ex_;
        coro continuation_;

        // Frame allocator: first parameter has get_frame_allocator()
        template<has_frame_allocator First, class... Rest>
        static void* operator new(std::size_t size, First& first, Rest&...)
        {
            auto& alloc = first.get_frame_allocator();
            std::size_t total = size + sizeof(detail::alloc_header);
            
            void* raw = alloc.allocate(total);
            auto* header = static_cast<detail::alloc_header*>(raw);
            header->dealloc = [](void* ctx, void* p, std::size_t n) {
                static_cast<std::remove_reference_t<decltype(alloc)>*>(ctx)
                    ->deallocate(p, n);
            };
            header->ctx = &alloc;
            
            return header + 1;
        }

        // Frame allocator: second parameter has get_frame_allocator() (member functions)
        template<class First, has_frame_allocator Second, class... Rest>
        static void* operator new(std::size_t size, First&, Second& second, Rest&...)
            requires (!has_frame_allocator<First>)
        {
            auto& alloc = second.get_frame_allocator();
            std::size_t total = size + sizeof(detail::alloc_header);
            
            void* raw = alloc.allocate(total);
            auto* header = static_cast<detail::alloc_header*>(raw);
            header->dealloc = [](void* ctx, void* p, std::size_t n) {
                static_cast<std::remove_reference_t<decltype(alloc)>*>(ctx)
                    ->deallocate(p, n);
            };
            header->ctx = &alloc;
            
            return header + 1;
        }

        // Default: no frame allocator in first two params - use global pool
        static void* operator new(std::size_t size)
        {
            static detail::frame_pool alloc(detail::frame_pool::make_global());
            
            std::size_t total = size + sizeof(detail::alloc_header);
            void* raw = alloc.allocate(total);
            
            auto* header = static_cast<detail::alloc_header*>(raw);
            header->dealloc = [](void* ctx, void* p, std::size_t n) {
                static_cast<detail::frame_pool*>(ctx)->deallocate(p, n);
            };
            header->ctx = &alloc;
            
            return header + 1;
        }

        static void operator delete(void* ptr, std::size_t size)
        {
            auto* header = static_cast<detail::alloc_header*>(ptr) - 1;
            std::size_t total = size + sizeof(detail::alloc_header);
            header->dealloc(header->ctx, header, total);
        }

        task get_return_object()
        {
            return {std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }

        auto final_suspend() noexcept
        {
            struct awaiter
            {
                promise_type* p_;
                bool await_ready() const noexcept { return false; }
                std::coroutine_handle<> await_suspend(coro h) const noexcept
                {
                    std::coroutine_handle<> next = std::noop_coroutine();
                    if(p_->continuation_)
                        next = p_->caller_ex_.dispatch(p_->continuation_);
                    h.destroy();
                    return next;  // Symmetric transfer
                }
                void await_resume() const noexcept {}
            };
            return awaiter{this};
        }

        void return_void() {}
        void unhandled_exception() { std::terminate(); }

        template<class Awaitable>
        struct transform_awaiter
        {
            std::decay_t<Awaitable> a_;
            promise_type* p_;
            bool await_ready() { return a_.await_ready(); }
            auto await_resume() { return a_.await_resume(); }
            template<class Promise>
            auto await_suspend(std::coroutine_handle<Promise> h)
            {
                return a_.await_suspend(h, p_->ex_);
            }
        };
    
        template<class Awaitable>
        auto await_transform(Awaitable&& a)
        {
            return transform_awaiter<Awaitable>{std::forward<Awaitable>(a), this};
        }

        template<class Executor>
        void set_executor(Executor const& ex)
        {
            ex_ = executor_ref(ex);
        }
    };

    std::coroutine_handle<promise_type> h_;
    bool has_own_ex_ = false;

    bool await_ready() const noexcept { return false; }
    void await_resume() const noexcept {}

    // Affine overload: receives dispatcher from caller
    // Returns handle for symmetric transfer
    template<class Executor>
    std::coroutine_handle<> await_suspend(coro continuation, Executor const& caller_ex)
    {
        h_.promise().caller_ex_ = executor_ref(caller_ex);
        h_.promise().continuation_ = continuation;

        if(has_own_ex_)
        {
            // Post to our executor
            struct starter : work
            {
                coro h_;
                starter(coro h) : h_(h) {}
                void operator()() override
                {
                    h_.resume();
                    delete this;
                }
            };
            h_.promise().ex_.post(new starter{h_});
            return std::noop_coroutine();  // Posted, not inline
        }
        else
        {
            // Inherit caller's executor, symmetric transfer
            h_.promise().ex_ = executor_ref(caller_ex);
            return h_;  // Return child handle for symmetric transfer
        }
    }

    // For top-level start
    template<class Executor>
    void start(Executor const& ex)
    {
        h_.promise().set_executor(ex);
        h_.promise().caller_ex_ = executor_ref(ex);
        h_.resume();
    }

    template<class Executor>
    void set_executor(Executor const& ex)
    {
        h_.promise().ex_ = executor_ref(ex);
        has_own_ex_ = true;
    }
};

/** Binds a task to execute on a specific executor.

    This function sets the executor for a task, causing it to run on the
    specified executor rather than inheriting the caller's executor. When
    awaited, the task will be posted to its bound executor instead of
    executing inline via symmetric transfer.

    @param ex The executor on which the task should run.
    @param t The task to bind to the executor.

    @return The same task, now bound to the specified executor.

    @par Example
    @code
    co_await run_on(strand, some_task());
    @endcode
*/
template<class Executor>
task run_on(Executor const& ex, task t)
{
    t.set_executor(ex);
    return t;
}

//----------------------------------------------------------

template<class Executor>
detail::root_task<Executor> detail::wrapper(task t)
{
    co_await t;
}

/** Starts a task for execution on an executor.

    This function initiates execution of a task by posting it to the
    specified executor's work queue. The task will begin running when
    the executor processes the posted work item.

    The task is "fire and forget" - it will self-destruct upon completion.
    There is no mechanism to wait for the result or retrieve exceptions;
    unhandled exceptions will call `std::terminate()`.

    @param ex The executor on which to run the task.
    @param t The task to execute.

    @par Example
    @code
    io_context ioc;
    async_run(ioc.get_executor(), my_coroutine());
    ioc.run();
    @endcode

    @note The executor is captured by value to ensure it remains valid
    for the duration of the task's execution.
*/
template<class Executor>
void async_run(Executor ex, task t)
{
    auto root = detail::wrapper<Executor>(std::move(t));
    root.h_.promise().ex_ = std::move(ex);
    root.h_.promise().starter_.h_ = root.h_;
    root.h_.promise().ex_.post(&root.h_.promise().starter_);
    root.release();
}

//----------------------------------------------------------

/** Performs a composed read operation on a stream.

    This coroutine performs 10 sequential read_some operations on the
    stream, simulating a composed read that continues until a complete
    message or buffer has been received.

    This demonstrates a 2-level composed operation: async_read calls
    the stream's async_read_some member function 10 times.

    @param stream The stream to read from.

    @return A task that completes when all read operations finish.
*/
template<class Stream>
task async_read(Stream& stream)
{
    for(int i = 0; i < 10; ++i)
        co_await stream.async_read_some();
}

/** Performs a composed request operation on a stream.

    This coroutine performs 10 sequential async_read operations,
    simulating a higher-level protocol operation such as reading
    an HTTP request with headers and body.

    This demonstrates a 3-level composed operation: async_request
    calls async_read 10 times, each of which performs 10 read_some
    operations, for a total of 100 I/O operations.

    @param stream The stream to read from.

    @return A task that completes when the entire request is read.
*/
template<class Stream>
task async_request(Stream& stream)
{
    for(int i = 0; i < 10; ++i)
        co_await async_read(stream);
}

/** Performs a composed session operation on a stream.

    This coroutine performs 10 sequential async_request operations,
    simulating a complete session that handles multiple requests
    over a persistent connection.

    This demonstrates a 4-level composed operation: async_session
    calls async_request 10 times, each of which performs 100 I/O
    operations, for a total of 1000 I/O operations.

    @param stream The stream to use for the session.

    @return A task that completes when the session ends.
*/
template<class Stream>
task async_session(Stream& stream)
{
    for(int i = 0; i < 10; ++i)
        co_await async_request(stream);
}

} // co

#endif
