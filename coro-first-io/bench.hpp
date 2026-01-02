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

//----------------------------------------------------------
// Work item base and intrusive queue

struct work
{
    virtual ~work() = default;
    virtual void operator()() = 0;
    work* next = nullptr;
};

struct queue
{
    work* head = nullptr;
    work* tail = nullptr;

    ~queue()
    {
        while(head)
        {
            auto p = head;
            head = head->next;
            delete p;
        }
    }

    bool empty() const noexcept { return head == nullptr; }

    void push(work* p)
    {
        if(tail)
        {
            tail->next = p;
            tail = p;
            return;
        }
        head = p;
        tail = p;
    }

    work* pop()
    {
        if(head)
        {
            auto p = head;
            head = head->next;
            if(! head)
                tail = nullptr;
            return p;
        }
        return nullptr;
    }
};

//----------------------------------------------------------
// I/O context with unified executor

struct io_context
{
    queue q_;

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
};

#endif
