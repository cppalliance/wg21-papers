---
title: "Timers: Design Rationale"
document: D0016R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Every async framework ships a timer. The shape is always the same.

This paper documents why the timer is the first Stage Two paper in the [Network Endeavor](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[1]</sup>, why it uses `std::chrono::steady_clock`, how it maps to three operating system primitives, why the cancellation model returns a count, and what six ecosystems converged on independently. The companion ask paper *Timers*<sup>[2]</sup> contains the proposal. This paper contains the reasoning.

This paper is Paper 8 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[1]</sup>. It depends on Paper 1 (IoAwaitable Protocol, [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup>).

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author maintains [Boost.Beast](https://github.com/boostorg/beast)<sup>[4]</sup> and develops [Capy](https://github.com/cppalliance/capy)<sup>[5]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[6]</sup>, plus three further Boost libraries built on them. Corosio ships a timer type on three platforms. The body of work creates a bias toward a dedicated timer type in the standard.

This paper asks for nothing.

---

## 2. Why Timers First

Stage Two begins with timers because the timer is the cheapest proof that the IoAwaitable protocol works end-to-end with a real kernel.

**The argument has three parts.**

**First: minimal surface.** The timer has one operation (`wait()`). One operation means one code path to audit, one error condition to handle, one awaitable to return. If the protocol breaks, the diagnostic is simple. If the protocol works, the contract holds for every subsequent platform operation - sockets, files, signals - because the mechanism is the same.

**Second: no data movement.** The timer does not read bytes. It does not write bytes. It does not allocate buffers. The only interaction with the kernel is "wake me at this time." Every complexity that `read_some` or `write_some` introduces - buffer ownership, partial completion, scatter-gather - is absent. The timer isolates the question: Does the IoAwaitable protocol deliver a kernel completion to a waiting coroutine?

**Third: cross-platform from day one.** Every operating system provides a timer primitive. IOCP has `CreateWaitableTimer`. Linux has `timerfd_create`. BSD/macOS has `EVFILT_TIMER` in kqueue. There is no "platform that does not support timers." The paper cannot be blocked by platform availability.

The committee reviews one type, five member functions, three platform mappings, and has full evidence that the IoAwaitable protocol is production-ready for platform I/O. Then Stage Two continues with the harder operations: signals, files, sockets, TLS.

---

## 3. Platform Implementation

The timer is implemented using the platform's native event notification mechanism. The kernel manages the deadline; the application does not poll.

### 3.1 Windows: IOCP

Windows provides `CreateWaitableTimer` and `SetWaitableTimer`. The timer handle is associated with the I/O completion port via `CreateThreadpoolTimer` or direct OVERLAPPED association. When the deadline expires, a completion packet arrives on the IOCP queue. The event loop dequeues it and resumes the waiting coroutine.

```cpp
// Pseudocode: Windows timer submission
HANDLE h = CreateWaitableTimer(nullptr, FALSE, nullptr);
LARGE_INTEGER due;
due.QuadPart = -duration_to_100ns(d);
SetWaitableTimer(h, &due, 0, completion_callback,
    state, FALSE);
```

The negative value indicates a relative deadline. The completion callback posts to the IOCP. The event loop picks it up in `GetQueuedCompletionStatus`.

### 3.2 Linux: timerfd

Linux provides `timerfd_create`, which returns a file descriptor that becomes readable when the timer expires. The file descriptor is registered with `epoll_ctl` like any other descriptor. When the timer fires, `epoll_wait` returns the event. The event loop reads eight bytes from the timerfd (the expiration count), then resumes the waiting coroutine.

```cpp
// Pseudocode: Linux timer submission
int fd = timerfd_create(CLOCK_MONOTONIC, TFD_NONBLOCK);
struct itimerspec ts = {};
ts.it_value = duration_to_timespec(d);
timerfd_settime(fd, 0, &ts, nullptr);
epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &event);
```

`CLOCK_MONOTONIC` maps directly to `steady_clock`. No conversion is needed.

### 3.3 BSD/macOS: kqueue

BSD and macOS provide `EVFILT_TIMER` in kqueue. The filter accepts a timeout in milliseconds (or nanoseconds with `NOTE_NSECONDS`). When the timer fires, `kevent` returns the event. No separate file descriptor is allocated - the timer lives inside the kqueue itself.

```cpp
// Pseudocode: kqueue timer submission
struct kevent ev;
EV_SET(&ev, ident, EVFILT_TIMER, EV_ADD | EV_ONESHOT,
    NOTE_NSECONDS, duration_to_ns(d), state);
kevent(kq, &ev, 1, nullptr, 0, nullptr);
```

`EV_ONESHOT` means the timer fires once and is automatically removed. The ident is an application-chosen identifier that correlates the completion with the waiting coroutine.

### 3.4 Summary

| Platform     | Primitive                   | Registration          | Completion delivery |
| ------------ | --------------------------- | --------------------- | ------------------- |
| Windows IOCP | `CreateWaitableTimer`       | IOCP association      | Completion packet   |
| Linux epoll  | `timerfd_create`            | `epoll_ctl`           | `epoll_wait` event  |
| BSD kqueue   | `EVFILT_TIMER`              | `kevent` registration | `kevent` return     |

Three platforms. Three primitives. One abstract shape: Set a deadline, receive a completion. The IoAwaitable protocol maps each completion to a coroutine resumption through `await_suspend` and symmetric transfer.

---

## 4. Clock Choice

### 4.1 Why `steady_clock`

`std::chrono::steady_clock` is monotonic. It advances at a uniform rate regardless of system clock adjustments. This property is required for correctness in timeout-based code.

Consider a 30-second timeout:

- **steady_clock**: always expires 30 seconds from now. Correct.
- **system_clock**: If NTP adjusts the system clock backward by 60 seconds during the wait, the timeout fires 90 seconds from now. If adjusted forward by 60 seconds, the timeout fires immediately. Both are bugs.

Wall-clock drift is not hypothetical. Cloud VMs experience clock jumps when migrated. Containers inherit host clock corrections. Laptops resume from sleep with stale system clocks. Every production deployment that uses `system_clock` for timeouts eventually encounters the bug.

### 4.2 Relationship to `std::chrono`

The timer does not introduce a new time representation. It consumes `std::chrono::steady_clock::time_point` and `std::chrono::steady_clock::duration` - types the standard library already provides. The user writes:

```cpp
using namespace std::chrono_literals;
timer t(ctx, 5s);
timer t2(ctx, steady_clock::now() + 30min);
```

No new duration types. No new clock types. The standard's chrono library is sufficient. The timer is a consumer, not a producer, of time vocabulary.

### 4.3 Absolute vs. Relative Deadlines

Both `expires_at` (absolute) and `expires_after` (relative) are provided. Absolute deadlines are necessary for implementing periodic work without drift accumulation:

```cpp
auto next = steady_clock::now();
for (;;)
{
    next += 100ms;
    t.expires_at(next);
    co_await t.wait();
    do_periodic_work();
}
```

If only `expires_after` existed, each iteration would accumulate the execution time of `do_periodic_work()`, causing drift. Absolute deadlines prevent this.

---

## 5. Cancellation Design

### 5.1 Cancel All vs. Cancel One

Two cancellation functions exist because the two use cases are structurally different.

`cancel()` is for teardown. A server is shutting down. All pending timers must complete immediately so their coroutines can unwind. The caller does not care which specific operations were pending - all of them must go.

`cancel_one()` is for selective wakeup. A timer pool reuses one `timer` object across multiple logical deadlines by cancelling and resetting. `cancel_one()` wakes the earliest waiter without disturbing later ones.

### 5.2 Return Count

Both `cancel()` and `cancel_one()` return the number of operations actually cancelled. The return value distinguishes three situations:

| Return value | Meaning |
| ------------ | ------- |
| 0            | No operations were pending (timer already expired or never started) |
| 1            | One operation was cancelled (`cancel_one()` maximum) |
| N > 1        | N operations were cancelled (`cancel()` with multiple waiters) |

The count is necessary for resource tracking. A connection manager that cancels a timeout needs to know whether the cancellation succeeded or whether the timeout already fired and the completion is in flight. Without the count, the manager must maintain a separate flag - duplicating state that the timer already knows.

### 5.3 Error Reporting

A cancelled `wait()` completes with `std::errc::operation_canceled`. The error is delivered through the normal result path, not through an exception. The waiting coroutine inspects the result:

```cpp
auto r = co_await t.wait();
if (r.has_error() &&
    r.error() == std::errc::operation_canceled)
{
    // Cancelled. Clean up.
}
```

This is cooperative cancellation. The timer does not destroy the coroutine frame. It does not throw into the coroutine. It delivers an error code through the same channel as any other completion. The coroutine decides what to do.

### 5.4 Implicit Cancellation on Deadline Reset

Setting a new deadline via `expires_at()` or `expires_after()` implicitly cancels all pending `wait()` operations. This prevents a class of bugs where a caller resets a timer but forgets to cancel the old waiter, resulting in a spurious wakeup at the old deadline.

The implicit cancellation matches [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[7]</sup> semantics. Twenty years of deployment confirm that the alternative - requiring explicit `cancel()` before every `expires_at()` - is a bug farm.

---

## 6. Convergence

Six ecosystems provide async timers. The shapes converge on the same design: a deadline, a wait operation, and cancellation.

### 6.1 Go: `time.Timer` / `time.After`

```go
timer := time.NewTimer(5 * time.Second)
<-timer.C            // blocks until deadline
timer.Stop()         // cancellation
timer.Reset(10 * time.Second)  // new deadline
```

Go's `time.Timer` returns a channel. Reading from the channel blocks until the deadline expires. `Stop()` is cancellation. `Reset()` sets a new deadline. The shape is: construct with deadline, wait, cancel.

### 6.2 Rust: `tokio::time::sleep`

```rust
let sleep = tokio::time::sleep(Duration::from_secs(5));
sleep.await;  // completes at deadline
```

Tokio's `sleep` returns a future that completes at the deadline. Cancellation is implicit - dropping the future cancels the timer. `tokio::time::timeout` wraps another future with a deadline; if the inner future does not complete in time, the timeout fires.

### 6.3 .NET: `Task.Delay` / `CancellationTokenSource`

```csharp
var cts = new CancellationTokenSource();
await Task.Delay(TimeSpan.FromSeconds(5), cts.Token);
cts.Cancel();  // cancellation
```

.NET provides `Task.Delay` for simple waits and `CancellationToken` for cancellation. The cancellation token is a separate object, not a method on the timer. The pattern is: Create delay, pass cancellation token, cancel externally.

### 6.4 Python: `asyncio.sleep`

```python
await asyncio.sleep(5)
task.cancel()  # cancellation via task handle
```

Python's `asyncio.sleep` is a coroutine that sleeps for the given duration. Cancellation is achieved by cancelling the task that awaits the sleep. The sleep itself has no `cancel()` method; the cancellation propagates from the task.

### 6.5 Asio: `steady_timer`

```cpp
asio::steady_timer t(ctx, 5s);
t.async_wait([](error_code ec) { /* ... */ });
t.cancel();
t.expires_after(10s);  // implicitly cancels
```

Asio's `steady_timer` is the direct ancestor of this proposal. The interface is identical in shape: construct with context and optional deadline, `async_wait`, `cancel`, `cancel_one`, `expires_at`, `expires_after`. The Corosio timer replaces the callback-based `async_wait` with an awaitable `wait()`.

### 6.6 libuv: `uv_timer_t`

```c
uv_timer_init(loop, &timer);
uv_timer_start(&timer, callback, 5000, 0);  // 5s, no repeat
uv_timer_stop(&timer);  // cancellation
```

libuv provides `uv_timer_t`. `uv_timer_start` sets the deadline and callback. `uv_timer_stop` cancels. The repeat parameter enables periodic timers (deferred in this paper - see Section 8).

### 6.7 Convergence Summary

| Ecosystem | Type                    | Wait          | Cancel           | Reset deadline |
| --------- | ----------------------- | ------------- | ---------------- | -------------- |
| Go        | `time.Timer`            | `<-timer.C`  | `Stop()`         | `Reset(d)`     |
| Rust      | `tokio::time::Sleep`    | `.await`      | drop             | `reset()`      |
| .NET      | `Task.Delay`            | `await`       | `cts.Cancel()`   | (new delay)    |
| Python    | `asyncio.sleep`         | `await`       | `task.cancel()`  | (new sleep)    |
| Asio      | `steady_timer`          | `async_wait`  | `cancel()`       | `expires_at()` |
| libuv     | `uv_timer_t`            | callback      | `uv_timer_stop`  | `uv_timer_start` |

Six ecosystems. Six timers. One shape: Set a deadline, wait for it, cancel it if needed. The proposed `std::io::timer` is this shape expressed as an IoAwaitable.

---

## 7. Anticipated Objections

### 7.1 "But `std::chrono` already handles time"

**Acknowledged.** `std::chrono` provides clocks, durations, and time points. It does not provide an awaitable deadline. A `steady_clock::time_point` tells you *when*. A `timer` tells the kernel to *wake you then*. The gap between "knowing when" and "being woken then" is what the timer fills. `std::chrono` is the vocabulary for expressing the deadline. The timer is the mechanism for enforcing it.

### 7.2 "But timers belong in the OS layer, not the standard"

**Rejected.** Every async framework provides timers because raw OS primitives are not portable and not composable with the framework's completion model. A `timerfd_create` on Linux requires `epoll_ctl` registration, read of eight bytes on expiry, and manual correlation with application state. A kqueue `EVFILT_TIMER` requires a different registration path. A Windows waitable timer requires IOCP association. The `std::io::timer` hides three platform-specific mechanisms behind one interface. That is the purpose of a standard library.

### 7.3 "But the timer should be templated on clock type"

**Deferred.** A clock-generic timer (`timer<Clock>`) is a reasonable future extension. It is deferred because:

1. `steady_clock` covers the dominant use case (timeouts, periodic work, debouncing).
2. `system_clock` timers are rarely correct for I/O deadlines (Section 4.1).
3. Custom clocks (`high_resolution_clock`, user-defined simulation clocks) are niche.
4. A template complicates the type-erased stream model. `any_stream` wraps a concrete type; if the timer is templated on its clock, the type erasure boundary must accommodate clock-dependent completions.

The extension path is clear: A future paper can propose `basic_timer<Clock>` and make `timer` an alias for `basic_timer<steady_clock>`. The non-templated form ships first because it is simpler, covers the common case, and unblocks Stage Two.

### 7.4 "But cancellation semantics are unclear"

**Addressed.** Section 5 defines cancellation precisely:

- `cancel()` cancels all pending `wait()` operations. Returns the count.
- `cancel_one()` cancels at most one. Returns 0 or 1.
- Setting a new deadline implicitly cancels all pending operations.
- Cancelled operations complete with `std::errc::operation_canceled` through the normal result path.
- The coroutine is resumed, not destroyed. It inspects the error and decides.

There is no ambiguity. The semantics are identical to Asio's twenty-year-deployed `steady_timer`.

### 7.5 "But what if the timer has already expired when cancel is called?"

**Specified.** If the timer has already expired and the completion is queued for dispatch, `cancel()` returns 0. The operation completed - it was not cancelled. The waiting coroutine will be resumed with a success result, not a cancellation error. The caller observes this through the return value and handles it accordingly.

---

## 8. Deferrals

The following features are not part of this proposal. Each is a candidate for a future paper.

### 8.1 High-Resolution Timers

Some platforms provide sub-millisecond timer resolution (Windows `timeBeginPeriod`, Linux `CLOCK_MONOTONIC` with `hrtimer`). The proposed timer does not mandate a resolution - it expresses deadlines in `steady_clock::duration`, which has nanosecond or sub-nanosecond representation on most platforms. The actual resolution is implementation-defined and platform-dependent. A future paper may expose resolution queries.

### 8.2 Custom Clock Types

A `basic_timer<Clock>` template is the natural extension path. It requires defining requirements on `Clock` (monotonic? steady? convertible to kernel time?) and deciding whether the kernel uses native clock support or a user-space conversion. Deferred until demand materialises.

### 8.3 Periodic Timers

A repeating timer (libuv's repeat parameter, Go's `time.Ticker`) is implementable as a loop over `expires_after` + `wait()`. The loop is three lines. A dedicated periodic timer type adds API surface without enabling new functionality. Deferred unless measurement shows that the loop pattern has unacceptable drift or overhead.

### 8.4 Timer Wheels and Hierarchical Timing

High-performance servers with millions of concurrent connections use timer wheels (hashed timing wheels, hierarchical timing wheels) to manage per-connection timeouts. These are implementation strategies, not interface changes. A conforming implementation may use a timer wheel internally. The `std::io::timer` interface does not preclude it.

---

## 9. Why Now

The timer is the first Stage Two paper because it is the minimum viable proof that the IoAwaitable protocol works with a real kernel. The protocol was proposed in [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[3]</sup>. The protocol defines how a coroutine suspends, how the platform delivers a completion, and how the coroutine resumes. Until a real platform operation exercises that path, the protocol is theoretical.

The timer exercises it with the simplest possible operation. One submission to the kernel. One completion from the kernel. No data. No buffers. No partial completions. If the protocol works for timers, it works for everything else in Stage Two. If it does not work for timers, the defect is in the protocol and must be fixed before sockets, files, and signals compound the complexity.

Corosio ships the timer on IOCP, epoll, and kqueue today. The implementation is tested. The protocol is exercised. The paper documents what works.

---

## 10. Closing

The timer is one type with one operation that exercises one protocol on three platforms. It is the smallest possible standard library addition that proves coroutine-native I/O works end-to-end. Every ecosystem provides it. Every production server needs it. The design converged decades ago. The committee's task is not to invent - it is to adopt.

---

## Appendix A: Synopsis

```cpp
namespace std::io {

  class timer {
  public:
    // Construction and destruction
    explicit timer(execution_context& ctx);
    timer(execution_context& ctx,
        std::chrono::steady_clock::time_point expiry);
    timer(execution_context& ctx,
        std::chrono::steady_clock::duration after);

    timer(timer const&) = delete;
    timer& operator=(timer const&) = delete;
    timer(timer&&) noexcept;
    timer& operator=(timer&&) noexcept;

    ~timer();

    // Wait
    IoAwaitable auto wait();

    // Deadline
    void expires_at(
        std::chrono::steady_clock::time_point t);
    void expires_after(
        std::chrono::steady_clock::duration d);
    std::chrono::steady_clock::time_point expiry() const;

    // Cancellation
    std::size_t cancel();
    std::size_t cancel_one();
  };

}
```

---

## Appendix B: Corosio Header Inventory

The timer implementation in Corosio spans the following headers:

| Header | Role |
| ------ | ---- |
| `corosio/timer.hpp` | Public `timer` class definition |
| `corosio/detail/timer_service.hpp` | Per-context timer queue management |
| `corosio/detail/timer_op.hpp` | Timer operation state (coroutine handle, deadline) |
| `corosio/detail/iocp_timer.hpp` | Windows IOCP waitable timer backend |
| `corosio/detail/timerfd_timer.hpp` | Linux timerfd + epoll backend |
| `corosio/detail/kqueue_timer.hpp` | BSD/macOS kqueue EVFILT_TIMER backend |

The public interface is one header. The platform backends are three headers. The shared infrastructure (timer queue, operation state) is two headers. Total: six headers, approximately 800 lines across all platforms.

---

## Acknowledgments

Christopher Kohlhoff designed the Asio `steady_timer` whose interface this paper recovers for coroutine-native I/O. The Asio timer has been stable for nearly twenty years.

Mohammad Nejati implemented the Corosio timer on IOCP, epoll, and kqueue, proving the IoAwaitable protocol works end-to-end on three operating systems.

---

## References

[1] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[2] *Timers* (Vinnie Falco, 2026). Companion ask paper. D0015R0.

[3] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "The IoAwaitable Protocol" (Vinnie Falco, 2026).

[4] [Boost.Beast](https://github.com/boostorg/beast) - HTTP and WebSocket built on Boost.Asio (Vinnie Falco, 2017-2026).

[5] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[6] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[7] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - Asio steady_timer and timer services (Christopher Kohlhoff, 2003-2026).
