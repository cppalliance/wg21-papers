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
#include "bench_traits.hpp"

#include <exception>
#include <memory>

#if defined(__clang__) && !defined(__apple_build_version__)
#define CORO_AWAIT_ELIDABLE [[clang::coro_await_elidable]]
#else
#define CORO_AWAIT_ELIDABLE
#endif

namespace co {

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

        std::coroutine_handle<> await_suspend(coro h, any_executor const& ex) const
        {
            s_.do_read_some(h, &ex);
            // Affine awaitable: receive caller's executor for completion dispatch.
            // Return noop because we post work rather than resuming inline.
            return std::noop_coroutine();
        }

    private:
        socket& s_;
    };

    socket()
        : read_op_(new read_state)
    {
    }

    async_read_some_t async_read_some()
    {
        return async_read_some_t(*this);
    }

    detail::frame_pool& get_frame_allocator()
    {
        return pool_;
    }

private:
    struct read_state : work
    {
        coro h_;
        any_executor const* ex_;
    
        void operator()() override
        {
            // dispatch() returns the handle for symmetric transfer, allowing
            // the event loop to resume the coroutine without additional stack frames
            ex_->dispatch(h_)();
        }
    }; 

    void do_read_some(coro h, any_executor const* ex)
    {
        ++g_io_count;
        read_op_->h_ = h;
        read_op_->ex_ = ex;
        ex->post(read_op_.get());
    }

    std::unique_ptr<read_state> read_op_;
    detail::frame_pool pool_;
};

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

    @see any_executor
    @see has_frame_allocator
    @see detail::frame_pool
*/
struct CORO_AWAIT_ELIDABLE task
{
    struct promise_type : detail::frame_pool::promise_allocator
    {
        any_executor const* ex_ = nullptr;
        any_executor const* caller_ex_ = nullptr;
        coro continuation_;

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
                        next = p_->caller_ex_->dispatch(p_->continuation_);
                    h.destroy();
                    // Return continuation handle for symmetric transfer to
                    // avoid stack growth when resuming the caller
                    return next;
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
                return a_.await_suspend(h, *p_->ex_);
            }
        };
    
        template<class Awaitable>
        auto await_transform(Awaitable&& a)
        {
            return transform_awaiter<Awaitable>{std::forward<Awaitable>(a), this};
        }

        void set_executor(any_executor const& ex)
        {
            ex_ = &ex;
        }
    };

    std::coroutine_handle<promise_type> h_;
    bool has_own_ex_ = false;

    bool await_ready() const noexcept { return false; }
    void await_resume() const noexcept {}
    // Affine awaitable: receive caller's executor for completion dispatch
    std::coroutine_handle<> await_suspend(coro continuation, any_executor const& caller_ex)
    {
        h_.promise().caller_ex_ = &caller_ex;
        h_.promise().continuation_ = continuation;

        if(has_own_ex_)
        {
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
            h_.promise().ex_->post(new starter{h_});
            // Return noop because we posted work; executor will resume us later
            return std::noop_coroutine();
        }
        else
        {
            // Return our handle for symmetric transfer to avoid stack growth
            h_.promise().ex_ = &caller_ex;
            return h_;
        }
    }

    void start(any_executor const& ex)
    {
        h_.promise().set_executor(ex);
        h_.promise().caller_ex_ = &ex;
        h_.resume();
    }

    void set_executor(any_executor const& ex)
    {
        h_.promise().ex_ = &ex;
        has_own_ex_ = true;
    }
};

/** A TLS stream adapter that wraps another stream.

    This class wraps a stream and provides an async_read_some
    operation that invokes the wrapped stream's async_read_some
    once, simulating TLS record layer behavior.

    @tparam Stream The stream type to wrap.
*/
template<class Stream>
struct tls_stream
{
    Stream stream_;

    template<class... Args>
    explicit tls_stream(Args&&... args)
        : stream_(std::forward<Args>(args)...) {}

    auto get_executor() const { return stream_.get_executor(); }

    task async_read_some()
    {
        co_await stream_.async_read_some();
    }

    template<class Stream2 = Stream>
    requires requires(Stream2& s) { s.get_frame_allocator(); }
    auto& get_frame_allocator()
    {
        return stream_.get_frame_allocator();
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
task run_on(any_executor const& ex, task t)
{
    t.set_executor(ex);
    return t;
}

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

/** Performs a composed read operation on a stream.

    This coroutine performs 5 sequential read_some operations on the
    stream, simulating a composed read that continues until a complete
    message or buffer has been received.

    This demonstrates a 2-level composed operation: async_read calls
    the stream's async_read_some member function 5 times.

    @param stream The stream to read from.

    @return A task that completes when all read operations finish.
*/
template<class Stream>
task async_read(Stream& stream)
{
    for(int i = 0; i < 5; ++i)
        co_await stream.async_read_some();
}

/** Performs a composed request operation on a stream.

    This coroutine performs 10 sequential read_some operations,
    simulating a higher-level protocol operation such as reading
    an HTTP request with headers and body.

    This demonstrates a 2-level composed operation: async_request
    calls the stream's async_read_some member function 10 times.

    @param stream The stream to read from.

    @return A task that completes when the entire request is read.
*/
template<class Stream>
task async_request(Stream& stream)
{
    for(int i = 0; i < 10; ++i)
        co_await stream.async_read_some();
}

/** Performs a composed session operation on a stream.

    This coroutine performs 100 sequential async_request operations,
    simulating a complete session that handles multiple requests
    over a persistent connection.

    This demonstrates a 3-level composed operation: async_session
    calls async_request 100 times, each of which performs 10 I/O
    operations, for a total of 1000 I/O operations.

    @param stream The stream to use for the session.

    @return A task that completes when the session ends.
*/
template<class Stream>
task async_session(Stream& stream)
{
    for(int i = 0; i < 100; ++i)
        co_await async_request(stream);
}

} // co

#endif
