//
// Copyright (c) 2025 Vinnie Falco (vinnie dot falco at gmail dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
// Official repository: https://github.com/cppalliance/wg21-papers/coro-first-io
//

#ifndef BENCH_HPP
#define BENCH_HPP

#include <concepts>
#include <coroutine>
#include <cstddef>
#include <utility>

using coro = std::coroutine_handle<void>;

struct work_queue;

/** Abstract base class for executable work items.

    Work items are heap-allocated objects that can be queued for later
    execution. They form the foundation of the async operation model,
    allowing callbacks and coroutine resumptions to be posted to an
    executor for deferred invocation.

    Derived classes must implement `operator()` to define the work
    to be performed when the item is executed.

    @note Work items are typically allocated with custom allocators
    (such as op_cache or frame_pool) to minimize allocation overhead
    in high-frequency async operations.

    @see work_queue
*/
struct work
{
    virtual ~work() = default;
    virtual void operator()() = 0;

private:
    friend struct work_queue;
    work* next_ = nullptr;
};

/** An intrusive FIFO queue of work items.

    This queue manages work items using an intrusive singly-linked list,
    avoiding additional allocations for queue nodes. Work items are
    executed in the order they were pushed (first-in, first-out).

    The queue takes ownership of pushed work items and will delete
    any remaining items when destroyed.

    @note This is not thread-safe. External synchronization is required
    for concurrent access.

    @see work
*/
struct work_queue
{
    ~work_queue()
    {
        while(head_)
        {
            auto p = head_;
            head_ = head_->next_;
            delete p;
        }
    }

    bool empty() const noexcept { return head_ == nullptr; }

    void push(work* p)
    {
        if(tail_)
        {
            tail_->next_ = p;
            tail_ = p;
            return;
        }
        head_ = p;
        tail_ = p;
    }

    work* pop()
    {
        if(head_)
        {
            auto p = head_;
            head_ = head_->next_;
            if(! head_)
                tail_ = nullptr;
            return p;
        }
        return nullptr;
    }

private:
    work* head_ = nullptr;
    work* tail_ = nullptr;
};

/** A simple I/O context for running asynchronous operations.

    The io_context provides an execution environment for async operations.
    It maintains a queue of pending work items and processes them when
    `run()` is called.

    The nested `executor` type provides the interface for dispatching
    coroutines and posting work items. It implements both synchronous
    dispatch (for symmetric transfer) and deferred posting.

    @par Example
    @code
    io_context ioc;
    auto ex = ioc.get_executor();
    async_run(ex, my_coroutine());
    ioc.run();  // Process all queued work
    @endcode

    @note This is a simplified implementation for benchmarking purposes.
    Production implementations would integrate with OS-level async I/O.

    @see work
    @see work_queue
*/
struct io_context
{
    struct executor
    {
        io_context* ctx_;

        // For coroutines: return handle for symmetric transfer
        coro dispatch(coro h) const
        {
            return h;
        }

        // For callbacks: invoke immediately  
        template<class F>
            requires (!std::same_as<std::decay_t<F>, coro>)
        void dispatch(F&& f) const
        {
            std::forward<F>(f)();
        }

        void post(work* w) const
        {
            ctx_->q_.push(w);
        }

        bool operator==(executor const& other) const noexcept
        {
            return ctx_ == other.ctx_;
        }
    };

    executor get_executor() { return {this}; }

    void run()
    {
        while(!q_.empty())
        {
            (*q_.pop())();
        }
    }

private:
    work_queue q_;
};

#endif
