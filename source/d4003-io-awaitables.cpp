// IoAwaitable Protocol — Self-Contained Compiler Explorer Demo
//
// Inlined from Boost.Capy (https://github.com/cppalliance/capy)
// Copyright (c) 2025 Vinnie Falco (vinnie.falco@gmail.com)
// Distributed under the Boost Software License, Version 1.0.
//
// Compile with: -std=c++20

#include <cassert>
#include <concepts>
#include <coroutine>
#include <cstddef>
#include <cstdint>
#include <exception>
#include <memory_resource>
#include <optional>
#include <stop_token>
#include <type_traits>
#include <utility>

#include <cstdio>

// ============================================================

namespace capy {

// ============================================================
// execution_context (minimal for demo)
// ============================================================

class execution_context
{
public:
    execution_context() = default;
    virtual ~execution_context() = default;

    execution_context(execution_context const&) = delete;
    execution_context& operator=(execution_context const&) = delete;
};

// ============================================================
// Executor concept
// ============================================================

template<class E>
concept Executor =
    std::is_nothrow_copy_constructible_v<E> &&
    std::is_nothrow_move_constructible_v<E> &&
    requires(E& e, E const& ce, E const& ce2, std::coroutine_handle<> h) {
        { ce == ce2 } noexcept -> std::convertible_to<bool>;
        { ce.context() } noexcept;
        requires std::is_lvalue_reference_v<decltype(ce.context())> &&
            std::derived_from<
                std::remove_reference_t<decltype(ce.context())>,
                execution_context>;
        { ce.on_work_started() } noexcept;
        { ce.on_work_finished() } noexcept;
        { ce.dispatch(h) } -> std::same_as<std::coroutine_handle<>>;
        { ce.post(h) };
    };

// ============================================================
// executor_ref (type-erased executor wrapper)
// ============================================================

namespace detail {

struct executor_vtable
{
    execution_context& (*context)(void const*) noexcept;
    void (*on_work_started)(void const*) noexcept;
    void (*on_work_finished)(void const*) noexcept;
    void (*post)(void const*, std::coroutine_handle<>);
    std::coroutine_handle<> (*dispatch)(void const*, std::coroutine_handle<>);
    bool (*equals)(void const*, void const*) noexcept;
};

template<class Ex>
inline constexpr executor_vtable vtable_for = {
    [](void const* p) noexcept -> execution_context& {
        return const_cast<Ex*>(static_cast<Ex const*>(p))->context();
    },
    [](void const* p) noexcept {
        const_cast<Ex*>(static_cast<Ex const*>(p))->on_work_started();
    },
    [](void const* p) noexcept {
        const_cast<Ex*>(static_cast<Ex const*>(p))->on_work_finished();
    },
    [](void const* p, std::coroutine_handle<> h) {
        static_cast<Ex const*>(p)->post(h);
    },
    [](void const* p, std::coroutine_handle<> h) -> std::coroutine_handle<> {
        return static_cast<Ex const*>(p)->dispatch(h);
    },
    [](void const* a, void const* b) noexcept -> bool {
        return *static_cast<Ex const*>(a) == *static_cast<Ex const*>(b);
    },
};

} // namespace detail

class executor_ref
{
    void const* ex_ = nullptr;
    detail::executor_vtable const* vt_ = nullptr;

public:
    executor_ref() = default;
    executor_ref(executor_ref const&) = default;
    executor_ref& operator=(executor_ref const&) = default;

    template<class Ex>
        requires (!std::same_as<std::decay_t<Ex>, executor_ref>)
    executor_ref(Ex const& ex) noexcept
        : ex_(&ex)
        , vt_(&detail::vtable_for<Ex>)
    {
    }

    explicit operator bool() const noexcept { return ex_ != nullptr; }

    execution_context& context() const noexcept { return vt_->context(ex_); }
    void on_work_started() const noexcept { vt_->on_work_started(ex_); }
    void on_work_finished() const noexcept { vt_->on_work_finished(ex_); }
    std::coroutine_handle<> dispatch(std::coroutine_handle<> h) const { return vt_->dispatch(ex_, h); }
    void post(std::coroutine_handle<> h) const { vt_->post(ex_, h); }

    bool operator==(executor_ref const& other) const noexcept
    {
        if (ex_ == other.ex_)
            return true;
        if (vt_ != other.vt_)
            return false;
        return vt_->equals(ex_, other.ex_);
    }
};

// ============================================================
// io_env - execution environment
// ============================================================

struct io_env
{
    executor_ref executor;
    std::stop_token stop_token;
    std::pmr::memory_resource* allocator = nullptr;
};

// ============================================================
// this_coro tags
// ============================================================

namespace this_coro {

struct environment_tag {};
struct executor_tag {};
struct stop_token_tag {};
struct allocator_tag {};

inline constexpr environment_tag environment{};
inline constexpr executor_tag executor{};
inline constexpr stop_token_tag stop_token{};
inline constexpr allocator_tag allocator{};

} // namespace this_coro

// ============================================================
// get/set_current_frame_allocator (thread-local)
// ============================================================

namespace detail {
inline std::pmr::memory_resource*& tls_frame_allocator() noexcept
{
    static thread_local std::pmr::memory_resource* mr = nullptr;
    return mr;
}
} // namespace detail

inline std::pmr::memory_resource*
get_current_frame_allocator() noexcept
{
    return detail::tls_frame_allocator();
}

inline void
set_current_frame_allocator(std::pmr::memory_resource* mr) noexcept
{
    detail::tls_frame_allocator() = mr;
}

// ============================================================
// IoAwaitable concept
// ============================================================

template<typename A>
concept IoAwaitable =
    requires(
        A a,
        std::coroutine_handle<> h,
        io_env const* env)
    {
        a.await_suspend(h, env);
    };

// ============================================================
// IoRunnable concept
// ============================================================

template<typename T>
concept IoRunnable =
    IoAwaitable<T> &&
    requires { typename T::promise_type; } &&
    requires(T& t, T const& ct,
             typename T::promise_type const& cp,
             typename T::promise_type& p)
    {
        { ct.handle() } noexcept
            -> std::same_as<std::coroutine_handle<typename T::promise_type>>;
        { cp.exception() } noexcept -> std::same_as<std::exception_ptr>;
        { t.release() } noexcept;
        { p.set_continuation(std::coroutine_handle<>{}) } noexcept;
        { p.set_environment(static_cast<io_env const*>(nullptr)) } noexcept;
    } &&
    (std::is_void_v<decltype(std::declval<T&>().await_resume())> ||
     requires(typename T::promise_type& p) {
         p.result();
     });

// ============================================================
// io_awaitable_promise_base CRTP mixin
// ============================================================

template<typename Derived>
class io_awaitable_promise_base
{
    io_env const* env_ = nullptr;
    mutable std::coroutine_handle<> cont_{std::noop_coroutine()};

    static constexpr std::size_t ptr_alignment = alignof(void*);

    static std::size_t
    aligned_offset(std::size_t n) noexcept
    {
        return (n + ptr_alignment - 1) & ~(ptr_alignment - 1);
    }

public:
    static void*
    operator new(std::size_t size)
    {
        auto* mr = get_current_frame_allocator();
        if(!mr)
            mr = std::pmr::new_delete_resource();

        std::size_t ptr_offset = aligned_offset(size);
        std::size_t total = ptr_offset + sizeof(std::pmr::memory_resource*);
        void* raw = mr->allocate(total, alignof(std::max_align_t));

        auto* ptr_loc = reinterpret_cast<std::pmr::memory_resource**>(
            static_cast<char*>(raw) + ptr_offset);
        *ptr_loc = mr;

        return raw;
    }

    static void
    operator delete(void* ptr, std::size_t size)
    {
        std::size_t ptr_offset = aligned_offset(size);
        auto* ptr_loc = reinterpret_cast<std::pmr::memory_resource**>(
            static_cast<char*>(ptr) + ptr_offset);
        auto* mr = *ptr_loc;

        std::size_t total = ptr_offset + sizeof(std::pmr::memory_resource*);
        mr->deallocate(ptr, total, alignof(std::max_align_t));
    }

    ~io_awaitable_promise_base()
    {
        if(cont_ != std::noop_coroutine())
            cont_.destroy();
    }

    void set_continuation(std::coroutine_handle<> cont) noexcept
    {
        cont_ = cont;
    }

    std::coroutine_handle<> continuation() const noexcept
    {
        return std::exchange(cont_, std::noop_coroutine());
    }

    void set_environment(io_env const* env) noexcept
    {
        env_ = env;
    }

    io_env const* environment() const noexcept
    {
        return env_;
    }

    template<typename A>
    decltype(auto) transform_awaitable(A&& a)
    {
        return std::forward<A>(a);
    }

    template<typename T>
    auto await_transform(T&& t)
    {
        using Tag = std::decay_t<T>;

        if constexpr (std::is_same_v<Tag, this_coro::environment_tag>)
        {
            struct awaiter
            {
                io_env const* env_;
                bool await_ready() const noexcept { return true; }
                void await_suspend(std::coroutine_handle<>) const noexcept {}
                io_env const* await_resume() const noexcept { return env_; }
            };
            return awaiter{env_};
        }
        else if constexpr (std::is_same_v<Tag, this_coro::executor_tag>)
        {
            struct awaiter
            {
                executor_ref executor_;
                bool await_ready() const noexcept { return true; }
                void await_suspend(std::coroutine_handle<>) const noexcept {}
                executor_ref await_resume() const noexcept { return executor_; }
            };
            return awaiter{env_->executor};
        }
        else if constexpr (std::is_same_v<Tag, this_coro::stop_token_tag>)
        {
            struct awaiter
            {
                std::stop_token token_;
                bool await_ready() const noexcept { return true; }
                void await_suspend(std::coroutine_handle<>) const noexcept {}
                std::stop_token await_resume() const noexcept { return token_; }
            };
            return awaiter{env_->stop_token};
        }
        else if constexpr (std::is_same_v<Tag, this_coro::allocator_tag>)
        {
            struct awaiter
            {
                std::pmr::memory_resource* allocator_;
                bool await_ready() const noexcept { return true; }
                void await_suspend(std::coroutine_handle<>) const noexcept {}
                std::pmr::memory_resource* await_resume() const noexcept { return allocator_; }
            };
            return awaiter{env_->allocator};
        }
        else
        {
            return static_cast<Derived*>(this)->transform_awaitable(
                std::forward<T>(t));
        }
    }
};

// ============================================================
// task<T> — lazy coroutine task satisfying IoRunnable
// ============================================================

namespace detail {

template<typename T>
struct task_return_base
{
    std::optional<T> result_;

    void return_value(T value) { result_ = std::move(value); }
    T&& result() noexcept { return std::move(*result_); }
};

template<>
struct task_return_base<void>
{
    void return_void() {}
};

} // namespace detail

template<typename T = void>
struct [[nodiscard]] task
{
    struct promise_type
        : io_awaitable_promise_base<promise_type>
        , detail::task_return_base<T>
    {
        std::exception_ptr ep_;

        std::exception_ptr exception() const noexcept { return ep_; }

        task get_return_object()
        {
            return task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        auto initial_suspend() noexcept
        {
            struct awaiter
            {
                promise_type* p_;

                bool await_ready() const noexcept { return false; }

                void await_suspend(std::coroutine_handle<>) const noexcept
                {
                }

                void await_resume() const noexcept
                {
                    set_current_frame_allocator(p_->environment()->allocator);
                }
            };
            return awaiter{this};
        }

        auto final_suspend() noexcept
        {
            struct awaiter
            {
                promise_type* p_;

                bool await_ready() const noexcept { return false; }

                std::coroutine_handle<> await_suspend(std::coroutine_handle<>) const noexcept
                {
                    return p_->continuation();
                }

                void await_resume() const noexcept {}
            };
            return awaiter{this};
        }

        void unhandled_exception()
        {
            ep_ = std::current_exception();
        }

        template<class Awaitable>
        struct transform_awaiter
        {
            std::decay_t<Awaitable> a_;
            promise_type* p_;

            bool await_ready() noexcept { return a_.await_ready(); }

            decltype(auto) await_resume()
            {
                set_current_frame_allocator(p_->environment()->allocator);
                return a_.await_resume();
            }

            template<class Promise>
            auto await_suspend(std::coroutine_handle<Promise> h) noexcept
            {
                return a_.await_suspend(h, p_->environment());
            }
        };

        template<class Awaitable>
        auto transform_awaitable(Awaitable&& a)
        {
            using A = std::decay_t<Awaitable>;
            if constexpr (IoAwaitable<A>)
            {
                return transform_awaiter<Awaitable>{
                    std::forward<Awaitable>(a), this};
            }
            else
            {
                static_assert(sizeof(A) == 0, "requires IoAwaitable");
            }
        }
    };

    std::coroutine_handle<promise_type> h_;

    ~task()
    {
        if(h_)
            h_.destroy();
    }

    bool await_ready() const noexcept { return false; }

    auto await_resume()
    {
        if(h_.promise().ep_)
            std::rethrow_exception(h_.promise().ep_);
        if constexpr (! std::is_void_v<T>)
            return std::move(*h_.promise().result_);
        else
            return;
    }

    std::coroutine_handle<> await_suspend(std::coroutine_handle<> cont, io_env const* env)
    {
        h_.promise().set_continuation(cont);
        h_.promise().set_environment(env);
        return h_;
    }

    std::coroutine_handle<promise_type> handle() const noexcept { return h_; }

    void release() noexcept { h_ = nullptr; }

    task(task const&) = delete;
    task& operator=(task const&) = delete;

    task(task&& other) noexcept
        : h_(std::exchange(other.h_, nullptr))
    {
    }

    task& operator=(task&& other) noexcept
    {
        if(this != &other)
        {
            if(h_)
                h_.destroy();
            h_ = std::exchange(other.h_, nullptr);
        }
        return *this;
    }

private:
    explicit task(std::coroutine_handle<promise_type> h)
        : h_(h)
    {
    }
};

// ============================================================
// Concept satisfaction checks
// ============================================================

static_assert(IoAwaitable<task<int>>);
static_assert(IoRunnable<task<int>>);
static_assert(IoAwaitable<task<>>);
static_assert(IoRunnable<task<>>);

// ============================================================
// inline_executor — trivial synchronous executor for demo
// ============================================================

struct inline_context : execution_context {};

struct inline_executor
{
    inline_context* ctx_;

    execution_context& context() const noexcept { return *ctx_; }
    void on_work_started() const noexcept {}
    void on_work_finished() const noexcept {}

    std::coroutine_handle<> dispatch(std::coroutine_handle<> h) const
    {
        return h;
    }

    void post(std::coroutine_handle<> h) const
    {
        h.resume();
    }

    bool operator==(inline_executor const& other) const noexcept
    {
        return ctx_ == other.ctx_;
    }
};

static_assert(Executor<inline_executor>);

// ============================================================
// Minimal run_sync — synchronous launcher for demonstration
// ============================================================

template<IoRunnable Task>
auto run_sync(executor_ref ex, std::stop_token token, Task t)
{
    auto h = t.handle();
    auto& p = h.promise();
    io_env env{ex, token};
    p.set_continuation(std::noop_coroutine());
    p.set_environment(&env);
    t.release();
    h.resume();

    if(p.exception())
        std::rethrow_exception(p.exception());

    if constexpr (!std::is_void_v<decltype(t.await_resume())>)
        return p.result();
}

template<IoRunnable Task>
auto run_sync(executor_ref ex, Task t)
{
    return run_sync(ex, std::stop_token{}, std::move(t));
}

// ============================================================
// Demo: IoAwaitable protocol in action
// ============================================================

// A simple IoAwaitable that completes immediately with a value
struct immediate_value
{
    int value_;

    bool await_ready() const noexcept { return true; }

    std::coroutine_handle<> await_suspend(std::coroutine_handle<>, io_env const*)
    {
        return std::noop_coroutine();
    }

    int await_resume() const noexcept { return value_; }
};

static_assert(IoAwaitable<immediate_value>);

// Child task: receives context from parent
task<int> compute(int x)
{
    // Retrieve the propagated environment
    auto env = co_await this_coro::environment;

    std::printf("  compute(%d): has executor=%s, stop_possible=%s\n",
        x,
        env->executor ? "yes" : "no",
        env->stop_token.stop_possible() ? "yes" : "no");

    // Await an IoAwaitable — context propagates automatically
    int v = co_await immediate_value{x * 10};
    co_return v + 1;
}

// Parent task: composes child tasks
task<int> parent_task()
{
    auto env = co_await this_coro::environment;
    std::printf("parent_task: has executor=%s\n", env->executor ? "yes" : "no");

    int a = co_await compute(3);
    int b = co_await compute(7);
    co_return a + b;
}

// Void task
task<> void_task()
{
    auto env = co_await this_coro::environment;
    std::printf("void_task: stop_requested=%s\n",
        env->stop_token.stop_requested() ? "yes" : "no");
    co_return;
}

int main()
{
    inline_context ctx;
    inline_executor ex{&ctx};

    std::printf("--- Running parent_task ---\n");
    int result = run_sync(ex, parent_task());
    std::printf("result = %d\n\n", result);

    std::printf("--- Running void_task with stop token ---\n");
    std::stop_source source;
    run_sync(ex, source.get_token(), void_task());

    std::printf("--- Running void_task with stop requested ---\n");
    source.request_stop();
    run_sync(ex, source.get_token(), void_task());

    std::printf("\nAll concept checks passed. Protocol works.\n");
    return 0;
}

} // namespace capy

// Trampoline main
int main() { return capy::main(); }
