---
title: "Executor Utilities"
document: D0005R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper asks the committee to advance two executor utilities - `strand<Ex>` and `any_executor` - as standard library vocabulary.

`strand<Ex>` serializes coroutine resumption over any executor without locks. `any_executor` type-erases any `Executor` behind an owning handle. Both are general-purpose. Neither has an I/O dependency. Neither has a platform dependency. Both ship in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> today.

The companion paper *Executor Utilities: Design Rationale*<sup>[8]</sup> provides the design rationale, the convergence record, anticipated objections, and the implementation inventory. Read this paper for the proposal; read the companion when you need the audit trail.

This paper is Paper 3 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup>. It depends on Paper 1 ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[2]</sup>), the IoAwaitable Protocol.

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author develops and maintains [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[4]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

This paper is the proposal-only ask paper for `strand` and `any_executor`. The design rationale lives in the companion *Executor Utilities: Design Rationale*<sup>[8]</sup>.

This paper asks for nothing.

---

## 2. What This Paper Asks

The committee is asked to advance the following vocabulary for the standard library:

```cpp
namespace std::io {

  template<Executor Ex>
  class strand;

  class any_executor;

}
```

One class template. One class. Two general-purpose executor utilities.

---

## 3. `strand<Ex>`

### 3.1 Purpose

A `strand` serializes coroutine execution over any executor. No two coroutines dispatched through the same strand execute concurrently. The guarantee holds regardless of how many threads drive the underlying execution context.

```cpp
io_context ctx;
auto ex = ctx.get_executor();
strand<decltype(ex)> s(ex);

task<> writer_a(strand<decltype(ex)>& s, shared_state& st)
{
    co_await run(s)([&]() -> task<> {
        st.value += 1;       // no lock needed
        co_return;
    }());
}

task<> writer_b(strand<decltype(ex)>& s, shared_state& st)
{
    co_await run(s)([&]() -> task<> {
        st.value += 2;       // no lock needed
        co_return;
    }());
}
```

Both writers access `st.value` without a mutex. The strand guarantees non-concurrent execution.

### 3.2 Template Parameter

`strand` is parameterized on the executor type:

```cpp
template<Executor Ex>
class strand;
```

The executor must satisfy the `Executor` concept defined in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[2]</sup>. The strand wraps the executor and forwards its `context()` call. The underlying executor controls which threads run work; the strand controls ordering.

### 3.3 Interface

```cpp
template<Executor Ex>
class strand
{
public:
    using inner_executor_type = Ex;

    strand() = delete;
    explicit strand(Ex ex);

    strand(strand const&) = delete;
    strand& operator=(strand const&) = delete;

    strand(strand&& other) noexcept;
    strand& operator=(strand&& other) noexcept;

    ~strand();

    Ex const& get_inner_executor() const noexcept;

    execution_context& context() const noexcept;
    void on_work_started() const noexcept;
    void on_work_finished() const noexcept;

    std::coroutine_handle<>
    dispatch(continuation& c) const;

    void post(continuation& c) const;

    bool operator==(strand const& other) const noexcept;
    bool operator!=(strand const& other) const noexcept;
};
```

### 3.4 Serialization Guarantee

The strand maintains an internal queue. When a continuation is dispatched or posted:

1. If no continuation is currently executing in the strand, the continuation runs immediately (for `dispatch`) or is deferred to the inner executor (for `post`).
2. If a continuation is already executing in the strand, the new continuation is enqueued. It runs after the current one completes.

At no point do two continuations dispatched through the same strand execute concurrently, even if the underlying execution context has multiple threads.

### 3.5 `dispatch` vs `post`

`dispatch` may execute the continuation inline if the caller is already executing within the strand. This avoids unnecessary context switches. `post` always defers: The continuation is enqueued and runs later, even if the caller is already in the strand.

The distinction is the same as on the underlying executor. The strand inherits the semantics and adds the serialization invariant.

### 3.6 Nested Strands

Strands compose. A strand constructed over another strand serializes against the outer strand's guarantee:

```cpp
strand<decltype(ex)> outer(ex);
strand<strand<decltype(ex)>> inner(outer);
```

Both `outer` and `inner` independently guarantee non-concurrent execution within their own scope. Work dispatched through `inner` is also serialized by `outer`. The nesting is structural - the inner strand dispatches through the outer strand's `dispatch`/`post`, inheriting its ordering.

### 3.7 Move Semantics

`strand` is move-only. Copying a strand would create two handles to the same serialization state, making the ownership ambiguous. Move transfers the internal queue and the associated executor. The moved-from strand is in a valid but unspecified state.

---

## 4. `any_executor`

### 4.1 Purpose

`any_executor` type-erases any `Executor` behind an owning handle. Where `executor_ref` ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[2]</sup>) is a non-owning two-pointer view, `any_executor` owns the erased executor and manages its lifetime.

```cpp
any_executor make_executor(io_context& ctx)
{
    return any_executor(ctx.get_executor());
}

void store_executor(std::vector<any_executor>& v,
                    io_context& ctx)
{
    v.push_back(any_executor(ctx.get_executor()));
}
```

### 4.2 Interface

```cpp
class any_executor
{
public:
    any_executor() noexcept;
    any_executor(std::nullptr_t) noexcept;

    template<Executor Ex>
        requires (!std::same_as<
            std::decay_t<Ex>, any_executor>)
    any_executor(Ex ex);

    any_executor(any_executor const& other);
    any_executor(any_executor&& other) noexcept;

    any_executor& operator=(any_executor const& other);
    any_executor& operator=(any_executor&& other) noexcept;
    any_executor& operator=(std::nullptr_t) noexcept;

    ~any_executor();

    explicit operator bool() const noexcept;

    execution_context& context() const;
    void on_work_started() const noexcept;
    void on_work_finished() const noexcept;

    std::coroutine_handle<>
    dispatch(continuation& c) const;

    void post(continuation& c) const;

    bool operator==(any_executor const& other)
        const noexcept;
    bool operator!=(any_executor const& other)
        const noexcept;
    bool operator==(std::nullptr_t) const noexcept;
};
```

### 4.3 Type Erasure

`any_executor` erases the concrete executor type behind a vtable. It satisfies the `Executor` concept, so any algorithm or type that accepts an `Executor` works with `any_executor` transparently.

```cpp
template<Executor Ex>
void schedule_work(Ex const& ex, continuation& c)
{
    ex.post(c);
}

any_executor ex = ctx.get_executor();
schedule_work(ex, c);  // works
```

### 4.4 Owning Semantics

Unlike `executor_ref`, `any_executor` owns the erased executor. Copying an `any_executor` copies the underlying executor. Moving transfers ownership. Destruction destroys the underlying executor. The lifetime of the erased executor is tied to the `any_executor` instance.

This enables polymorphic executor storage:

```cpp
struct connection
{
    any_executor ex;
    tcp_socket socket;
};
```

The connection stores its executor without knowing the concrete type. Different connections may use different executor types (an `io_context` executor, a strand, a thread pool executor) behind the same `any_executor` handle.

### 4.5 Small Buffer Optimization

Implementations should use small buffer optimization (SBO) to avoid heap allocation for executors that fit within a reasonable inline buffer. The `io_context` executor and `strand` executor are expected to fit within the SBO in quality implementations.

The SBO threshold is implementation-defined. The interface does not expose it. The observable behavior is identical regardless of whether the SBO applies.

### 4.6 Comparison

Two `any_executor` instances compare equal if they hold the same type and the underlying executors compare equal. A default-constructed or null `any_executor` compares equal to `nullptr` and to other null instances. The comparison enables strand identity checks - two strands wrapping the same underlying state compare equal regardless of how they were obtained.

### 4.7 Relationship to `executor_ref`

`executor_ref` and `any_executor` serve different roles:

| Property           | `executor_ref`          | `any_executor`           |
|--------------------|-------------------------|--------------------------|
| Ownership          | Non-owning (borrows)    | Owning (manages)         |
| Size               | Two pointers            | Implementation-defined   |
| Copy               | Trivially copyable      | Copies underlying        |
| Use case           | Inside `io_env`, short-lived | Storage, polymorphic containers |
| Template parameter | No                      | No                       |

`executor_ref` is the right choice inside `io_env` and across suspension points where the executor's lifetime is guaranteed by the launch function. `any_executor` is the right choice when the executor must outlive the scope that created it.

---

## 5. Suggested Straw Poll

> LEWG agrees that the executor utilities `strand<Ex>` and `any_executor` documented in this paper and its companion *Executor Utilities: Design Rationale* should be advanced as standard library vocabulary.

---

## Acknowledgments

Christopher Kohlhoff designed Asio's strand and `any_executor`. Their production deployment across two decades established both abstractions as essential executor infrastructure.

The Networking TS authors ([N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[5]</sup>) codified the strand and executor type erasure semantics.

---

## References

[1] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[2] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[3] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[4] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[5] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).

[6] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - Strand and executor type erasure (Christopher Kohlhoff, 2003-2026).

[7] [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[8] *Executor Utilities: Design Rationale* (Vinnie Falco, 2026). Companion design paper. D0006R0.
