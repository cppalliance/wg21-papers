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

#include <exception>
#include <memory>
#include <mutex>

#ifdef __clang__
#define CORO_AWAIT_ELIDABLE [[clang::coro_await_elidable]]
#else
#define CORO_AWAIT_ELIDABLE
#endif

namespace co {

//----------------------------------------------------------

template<class T>
concept is_executor = requires(T const& t, coro h, work* w) {
    { t.dispatch(h) } -> std::convertible_to<coro>;
    t.post(w);
    { t == t } -> std::convertible_to<bool>;
};

template<class A>
concept frame_allocator = requires(A& a, void* p, std::size_t n) {
    { a.allocate(n) } -> std::convertible_to<void*>;
    { a.deallocate(p, n) } -> std::same_as<void>;
};

template<class T>
concept has_frame_allocator = requires(T& t) {
    { t.get_frame_allocator() } -> frame_allocator;
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

struct socket
{
    struct async_awaitable
    {
        async_awaitable(socket& s) : s_(s) {}
        bool await_ready() const noexcept { return false; }
        void await_resume() const noexcept {}

        // Affine overload: receives dispatcher from caller
        // Returns noop_coroutine because we post, not dispatch
        template<class Executor>
        std::coroutine_handle<> await_suspend(coro h, Executor const& ex) const
        {
            s_.perform(h, executor_ref(ex));
            return std::noop_coroutine();
        }

    private:
        socket& s_;
    };

    socket()
        : op_(new state)
        , pool_(frame_pool::make_global())
    {
    }

    // Asynchronous operation that wraps OS-level I/O
    async_awaitable async_io()
    {
        return async_awaitable(*this);
    }

    // Frame allocator for coroutines using this socket
    frame_pool& get_frame_allocator()
    {
        return pool_;
    }

private:
    struct state : work
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

    void perform(coro h, executor_ref const& ex)
    {
        op_->h_ = h;
        op_->ex_ = ex;
        ex.post(op_.get()); // simulate OS call
    }

    std::unique_ptr<state> op_;
    frame_pool pool_;
};


//----------------------------------------------------------

// Header stored before coroutine frame for deallocation
struct alloc_header
{
    void (*dealloc)(void* ctx, void* ptr, std::size_t size);
    void* ctx;
};

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
            std::size_t total = size + sizeof(alloc_header);
            
            void* raw = alloc.allocate(total);
            auto* header = static_cast<alloc_header*>(raw);
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
            std::size_t total = size + sizeof(alloc_header);
            
            void* raw = alloc.allocate(total);
            auto* header = static_cast<alloc_header*>(raw);
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

template<class Executor>
task run_on(Executor const& ex, task t)
{
    t.set_executor(ex);
    return t;
}

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

template<class Executor>
root_task<Executor> wrapper(task t)
{
    co_await t;
}

template<class Executor>
void async_run(Executor ex, task t)
{
    auto root = wrapper<Executor>(std::move(t));
    root.h_.promise().ex_ = std::move(ex);
    root.h_.promise().starter_.h_ = root.h_;
    root.h_.promise().ex_.post(&root.h_.promise().starter_);
    root.release();
}

//----------------------------------------------------------

inline task async_read_some(socket& sock)
{
    co_await sock.async_io();
}

inline task async_read(socket& sock)
{
    for(int i = 0; i < 10; ++i)
        co_await async_read_some(sock);
}

inline task async_request(socket& sock)
{
    for(int i = 0; i < 10; ++i)
        co_await async_read(sock);
}

} // co

#endif
