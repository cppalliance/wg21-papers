//
// Copyright (c) 2025 Vinnie Falco (vinnie dot falco at gmail dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
// Official repository: https://github.com/cppalliance/wg21-papers/coro-first-io
//

#ifndef BENCH_CO_DETAIL_HPP
#define BENCH_CO_DETAIL_HPP

#include "bench.hpp"

#include <coroutine>
#include <cstddef>
#include <exception>
#include <mutex>

namespace co {
namespace detail {

// Header stored before coroutine frame for deallocation
struct alloc_header
{
    void (*dealloc)(void* ctx, void* ptr, std::size_t size);
    void* ctx;
};

//----------------------------------------------------------
// Frame pool: thread-local with global overflow
// Tracks block sizes to avoid returning undersized blocks

class frame_pool
{
    struct block
    {
        block* next;
        std::size_t size;
    };

    struct global_pool
    {
        std::mutex mtx;
        block* head = nullptr;

        ~global_pool()
        {
            while(head)
            {
                auto p = head;
                head = head->next;
                ::operator delete(p);
            }
        }

        void push(block* b)
        {
            std::lock_guard<std::mutex> lock(mtx);
            b->next = head;
            head = b;
        }

        block* pop(std::size_t n)
        {
            std::lock_guard<std::mutex> lock(mtx);
            block** pp = &head;
            while(*pp)
            {
                if((*pp)->size >= n)
                {
                    block* p = *pp;
                    *pp = p->next;
                    return p;
                }
                pp = &(*pp)->next;
            }
            return nullptr;
        }
    };

    struct local_pool
    {
        block* head = nullptr;

        void push(block* b)
        {
            b->next = head;
            head = b;
        }

        block* pop(std::size_t n)
        {
            block** pp = &head;
            while(*pp)
            {
                if((*pp)->size >= n)
                {
                    block* p = *pp;
                    *pp = p->next;
                    return p;
                }
                pp = &(*pp)->next;
            }
            return nullptr;
        }
    };

    global_pool& global_;

    static local_pool& get_local()
    {
        static thread_local local_pool local;
        return local;
    }

public:
    explicit frame_pool(global_pool& g) : global_(g) {}

    void* allocate(std::size_t n)
    {
        // First try thread-local (with size check)
        if(auto* b = get_local().pop(n))
            return b;

        // Then try global (with size check)
        if(auto* b = global_.pop(n))
            return b;

        // Fall back to heap
        auto* b = static_cast<block*>(::operator new(n));
        b->size = n;
        return b;
    }

    void deallocate(void* p, std::size_t n)
    {
        // Restore the size (was overwritten by alloc_header::ctx)
        auto* b = static_cast<block*>(p);
        b->size = n;
        // Return to thread-local pool
        get_local().push(b);
    }

    // Factory for creating a global pool
    static global_pool& make_global()
    {
        static global_pool pool;
        return pool;
    }
};

//----------------------------------------------------------

template<class Executor>
struct root_task
{
    // Embedded starter - no separate allocation needed
    struct starter : work
    {
        coro h_;

        void operator()() override
        {
            h_.resume();
            // Don't delete - we're embedded in the promise
        }
    };

    struct promise_type
    {
        Executor ex_;
        starter starter_;  // Embedded in coroutine frame

        // Use global frame pool for allocation
        static void* operator new(std::size_t size)
        {
            static frame_pool alloc(frame_pool::make_global());
            
            std::size_t total = size + sizeof(alloc_header);
            void* raw = alloc.allocate(total);
            
            auto* header = static_cast<alloc_header*>(raw);
            header->dealloc = [](void* ctx, void* p, std::size_t n) {
                static_cast<frame_pool*>(ctx)->deallocate(p, n);
            };
            header->ctx = &alloc;
            
            return header + 1;
        }

        static void operator delete(void* ptr, std::size_t size)
        {
            auto* header = static_cast<alloc_header*>(ptr) - 1;
            std::size_t total = size + sizeof(alloc_header);
            header->dealloc(header->ctx, header, total);
        }

        root_task get_return_object()
        {
            return {std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }

        auto final_suspend() noexcept
        {
            struct awaiter
            {
                bool await_ready() const noexcept { return false; }
                std::coroutine_handle<> await_suspend(coro h) const noexcept
                {
                    h.destroy();  // self-destruct
                    return std::noop_coroutine();
                }
                void await_resume() const noexcept {}
            };
            return awaiter{};
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
    };

    std::coroutine_handle<promise_type> h_;

    void release() { h_ = nullptr; }

    ~root_task()
    {
        if(h_)
            h_.destroy();
    }
};

} // detail

// Forward declaration
struct task;

namespace detail {

template<class Executor>
root_task<Executor> wrapper(task t);

} // detail
} // co

#endif
