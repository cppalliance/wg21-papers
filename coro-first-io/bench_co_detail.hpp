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
#include "bench_traits.hpp"

#include <coroutine>
#include <cstddef>
#include <exception>
#include <mutex>

namespace co {

// Forward declaration
struct task;

namespace detail {

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
                // block->size stores total allocated size (including header), so we must
                // check against n + sizeof(block) to ensure the block can satisfy the request
                if((*pp)->size >= n + sizeof(block))
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
                // block->size stores total allocated size (including header), so we must
                // check against n + sizeof(block) to ensure the block can satisfy the request
                if((*pp)->size >= n + sizeof(block))
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

    static local_pool& local()
    {
        static thread_local local_pool local;
        return local;
    }

public:
    void* allocate(std::size_t n)
    {
        std::size_t total = n + sizeof(block);
        
        if(auto* b = local().pop(n))
            return static_cast<char*>(static_cast<void*>(b)) + sizeof(block);

        if(auto* b = global().pop(n))
            return static_cast<char*>(static_cast<void*>(b)) + sizeof(block);

        auto* b = static_cast<block*>(::operator new(total));
        b->next = nullptr;
        b->size = total;
        return static_cast<char*>(static_cast<void*>(b)) + sizeof(block);
    }

    void deallocate(void* p, std::size_t)
    {
        // p points to the requested area; we need the block header to access size
        auto* b = static_cast<block*>(static_cast<void*>(
            static_cast<char*>(p) - sizeof(block)));
        // block->size already contains the true allocated size, so we ignore parameter n
        b->next = nullptr;
        local().push(b);
    }

    static global_pool& global()
    {
        static global_pool pool;
        return pool;
    }

    // Shared pool instance for all coroutine frames
    static frame_pool& shared()
    {
        static frame_pool pool;
        return pool;
    }

    // Mixin for promise types to provide frame allocation
    struct promise_allocator
    {
        struct header
        {
            void (*dealloc)(void* ctx, void* ptr, std::size_t size);
            void* ctx;
        };

        template<class Allocator>
        static void* allocate_with(std::size_t size, Allocator& alloc)
        {
            std::size_t total = size + sizeof(header);
            void* raw = alloc.allocate(total);
            
            auto* p = static_cast<header*>(raw);
            p->dealloc = [](void* ctx, void* p, std::size_t n) {
                static_cast<Allocator*>(ctx)->deallocate(p, n);
            };
            p->ctx = &alloc;
            
            return p + 1;
        }

        static void* operator new(std::size_t size)
        {
            return allocate_with(size, frame_pool::shared());
        }

        template<has_frame_allocator Arg0, class... ArgN>
        static void* operator new(std::size_t size, Arg0& arg0, ArgN&...)
        {
            return allocate_with(size, arg0.get_frame_allocator());
        }

        template<class Arg0, has_frame_allocator Arg1, class... ArgN>
        static void* operator new(std::size_t size, Arg0&, Arg1& arg1, ArgN&...)
            requires (!has_frame_allocator<Arg0>)
        {
            return allocate_with(size, arg1.get_frame_allocator());
        }

        static void operator delete(void* ptr, std::size_t size)
        {
            // ptr points to the coroutine frame; we need the header to access the type-erased deallocation callback
            auto* p = static_cast<header*>(ptr) - 1;
            std::size_t total = size + sizeof(header);
            p->dealloc(p->ctx, p, total);
        }
    };
};

template<class Executor>
struct root_task
{
    struct starter : work
    {
        coro h_;

        void operator()() override
        {
            h_.resume();
            // Not deleted here because starter is embedded in promise_type's frame
        }
    };

    struct promise_type : frame_pool::promise_allocator
    {
        Executor ex_;
        starter starter_;

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
                    h.destroy();
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

template<class Executor>
root_task<Executor> wrapper(task t);

} // detail
} // co

#endif
