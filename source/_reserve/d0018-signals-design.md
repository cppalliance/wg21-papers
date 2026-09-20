---
title: "Signals: Design Rationale"
document: D0018R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

`<csignal>` is a 1989 interface that restricts signal handlers to a handful of async-signal-safe functions and a single `volatile sig_atomic_t` flag. Every production C++ server works around it.

This paper documents the design rationale for `signal_set`, an async signal handling facility that integrates signals with the coroutine execution model proposed in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[1]</sup>. The companion ask paper *Signals*<sup>[2]</sup> proposes the normative vocabulary. This paper is the audit trail: why each facility exists, what alternatives were considered, how each choice was forced by the constraints of the domain, and where the convergence evidence lives.

This paper is Paper 9 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup>. It depends on Paper 1 (IoAwaitable Protocol). It is a Stage Two paper.

Read *Signals*<sup>[2]</sup> first for the specification; read this paper when you need the design audit trail.

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial draft.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author develops and maintains [Capy](https://github.com/cppalliance/capy)<sup>[4]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[5]</sup>, which implement the `signal_set` type documented here. The body of work creates a bias toward coroutine-native signal handling.

This paper documents the signal handling vocabulary that ships in Corosio. The vocabulary is consumed by every server application built on Corosio.

This paper asks for nothing.

---

## 2. Why Signals Need Async

### 2.1 The `<csignal>` Problem

The C standard library provides two facilities for signal handling: `signal()` and `raise()`. POSIX extends these with `sigaction()`, `sigprocmask()`, `sigsuspend()`, and related functions. The fundamental constraint is the same across all of them: **a signal handler runs in signal context, where almost nothing is safe to call.**

The C standard specifies that the behavior is undefined if a signal handler calls any library function other than `abort`, `_Exit`, `quick_exit`, or `signal` itself (with restrictions), or accesses any object other than `volatile sig_atomic_t` or a lock-free atomic<sup>[6]</sup>. POSIX relaxes this to a finite list of async-signal-safe functions<sup>[7]</sup>, but that list excludes `malloc`, `printf`, `new`, and any function that acquires a lock. In practice, a signal handler can set a flag and nothing else.

The result is a universal workaround: The signal handler sets a flag, and a main-loop thread polls the flag. Every C++ server that handles `SIGINT` or `SIGTERM` does this. The polling is manual, the flag is global, the wakeup latency is whatever the poll interval happens to be, and the flag check is scattered across the application.

### 2.2 What Async Signal Handling Provides

An async signal facility converts a POSIX signal into an event on the I/O reactor. The coroutine that calls `co_await signal_set.wait()` suspends like any other I/O operation. When the signal arrives, the reactor wakes the coroutine. No signal handler. No global flag. No polling. The signal is an event like any other.

```cpp
// Before: <csignal> ceremony.
volatile sig_atomic_t got_signal = 0;

void handler(int) { got_signal = 1; }

int main() {
    std::signal(SIGINT, handler);
    while (!got_signal) {
        poll_for_work();
        std::this_thread::sleep_for(100ms);
    }
    shutdown();
}

// After: coroutine-native signal handling.
std::io::task<> run(std::io::execution_context& ctx) {
    std::io::signal_set sigs(ctx);
    sigs.add(SIGINT);
    auto [ec, signo] = co_await sigs.wait();
    co_await shutdown();
}
```

The signal is no longer a control-flow interrupt. It is a value delivered through the same channel as every other I/O completion.

### 2.3 Async-Signal-Safe Functions

POSIX defines approximately 140 async-signal-safe functions<sup>[7]</sup>. The list includes `write`, `read`, `close`, `_exit`, and `sigaction`. It does not include `malloc`, `free`, `printf`, `pthread_mutex_lock`, or any C++ standard library function that may allocate. The restriction means that a signal handler cannot:

- Allocate memory
- Acquire a mutex
- Write to `std::cout` or any buffered stream
- Throw an exception
- Call any function whose implementation may do any of the above

These restrictions make `<csignal>` handlers nearly unusable for application-level logic. The async model sidesteps them entirely: The signal notification crosses from signal context into reactor context through a kernel mechanism (`signalfd`, `kqueue`, or a dedicated thread), and the coroutine that receives the notification runs in normal execution context with no restrictions.

---

## 3. Platform Implementation

Three kernel mechanisms convert POSIX signals into file-descriptor-based events that a reactor can poll. A fourth approach serves Windows.

### 3.1 Linux: `signalfd`

`signalfd(2)` creates a file descriptor that becomes readable when a signal in the specified mask is delivered<sup>[8]</sup>. The signal is consumed by reading a `signalfd_siginfo` structure from the descriptor. The descriptor integrates with `epoll`, `poll`, and `select`. Corosio uses `signalfd` on Linux.

The signal must be blocked with `sigprocmask` before `signalfd` is useful; otherwise the default disposition executes before `signalfd` can intercept the signal. `signal_set::add()` blocks the signal as part of registration.

### 3.2 BSD/macOS: `kqueue` with `EVFILT_SIGNAL`

`kqueue(2)` provides `EVFILT_SIGNAL`, a filter that fires when a specified signal is delivered<sup>[9]</sup>. The signal number is the filter identifier. Unlike `signalfd`, `kqueue` does not require the signal to be blocked first, though blocking is recommended to prevent the default disposition from executing. Corosio uses `EVFILT_SIGNAL` on macOS and FreeBSD.

### 3.3 Windows: Dedicated Thread

Windows does not have POSIX signals in the kernel sense. `SetConsoleCtrlHandler` intercepts `CTRL_C_EVENT` and `CTRL_BREAK_EVENT`<sup>[10]</sup>. The handler runs on a dedicated thread created by the OS. Corosio's Windows implementation uses a dedicated thread that translates console control events into signal completions on the I/O context. The mapping is:

| Console event       | Signal number |
| ------------------- | ------------- |
| `CTRL_C_EVENT`      | `SIGINT`      |
| `CTRL_BREAK_EVENT`  | `SIGBREAK`    |
| `CTRL_CLOSE_EVENT`  | `SIGTERM`     |

The abstraction collapses platform differences into a single `wait()` call. Application code does not know whether the signal arrived through `signalfd`, `kqueue`, or `SetConsoleCtrlHandler`.

### 3.4 Fallback: Self-Pipe Trick

On platforms without `signalfd` or `kqueue` signal support, the self-pipe trick<sup>[11]</sup> converts a signal into a byte written to a pipe. The signal handler (which is async-signal-safe because `write` to a pipe is on the POSIX safe list) writes one byte. The read end of the pipe is registered with the reactor. The technique dates to 1990 and remains the portable fallback.

---

## 4. The `signal_set` Design

### 4.1 Why a Set, Not Individual Signal Objects

The alternative design - one object per signal number - was considered and rejected. Three reasons:

**Lifetime management.** A server typically handles two to four signals (`SIGINT`, `SIGTERM`, `SIGHUP`, `SIGUSR1`). With individual signal objects, the application manages four independent lifetimes, four independent `wait()` calls, and four independent cancellation paths. A set collapses all of them into one wait.

**Composition with `when_any`.** The graceful shutdown pattern is `co_await when_any(work(), signals.wait())`. With individual objects, the pattern becomes `co_await when_any(work(), sig1.wait(), sig2.wait(), sig3.wait())`. The combinatorial expansion scales with the number of signals. The set collapses the expansion.

**Asio precedent.** Asio's `signal_set` has been the established shape for over fifteen years<sup>[12]</sup>. Go, Rust, Python, and .NET all use a set or channel model, not individual signal objects. Section 6 documents the convergence.

### 4.2 Dynamic Registration

`add()` and `remove()` modify the set at runtime. The alternative - a constructor that takes a fixed list of signals - was considered. Dynamic registration was selected for two reasons:

**Configuration-driven signals.** A server that reads its signal configuration from a file or command line cannot enumerate the signals at compile time. Dynamic `add()` accommodates runtime configuration.

**Lifecycle changes.** A server that rotates log files on `SIGHUP` may add `SIGHUP` only after the logging subsystem is initialised. Dynamic registration lets the application match signal registration to subsystem readiness.

### 4.3 `wait()` Returns the Signal Number

`wait()` returns the signal number that was delivered, not a boolean or void. The caller distinguishes between signals without maintaining separate wait operations:

```cpp
sigs.add(SIGINT);
sigs.add(SIGTERM);
sigs.add(SIGHUP);

while (true) {
    auto [ec, signo] = co_await sigs.wait();
    if (ec) break;
    if (signo == SIGHUP)
        reload_config();
    else
        break;  // SIGINT or SIGTERM: shut down.
}
```

The loop handles `SIGHUP` for config reload and exits on `SIGINT` or `SIGTERM`. One wait operation, one set, one loop.

---

## 5. Flags

### 5.1 Why Expose POSIX Flags

The `flags_t` parameter on `add()` exposes POSIX `sigaction` flags. The question is whether a standard library type should carry platform-specific flag semantics.

The answer is yes, for the same reason `std::filesystem` carries platform-specific permission bits: The abstraction is portable, but the underlying resource has platform-specific properties that applications legitimately need to control. A server that forks child processes needs `SA_NOCLDWAIT` to prevent zombie accumulation. A server that must not restart interrupted system calls needs to omit `SA_RESTART`. These are not exotic requirements. They are the basic signal disposition controls that POSIX applications use daily.

### 5.2 Windows Compatibility

On Windows, POSIX signal disposition flags have no kernel equivalent. The `flags_t` type exists on all platforms, but flag values that have no Windows equivalent are silently ignored. The alternative - a compile-time error for unsupported flags - was rejected because it would force `#ifdef` blocks around every `add()` call that uses flags. Silent ignore is the precedent established by `std::filesystem::permissions` when a permission bit has no platform equivalent.

### 5.3 The Default-Flags Overload

The one-argument `add(int signal_number)` overload uses platform-appropriate defaults. On POSIX, this means no special flags (the `sigaction` defaults apply). The two-argument overload is for applications that need explicit flag control. The common case requires no flags knowledge.

---

## 6. Convergence

Six independent ecosystems provide async signal handling. Each arrived at a set-or-channel model.

| Ecosystem           | Facility                                                                     | Model                                  |
| ------------------- | ---------------------------------------------------------------------------- | -------------------------------------- |
| Go (2012)           | `os/signal.Notify(c, sig...)`<sup>[13]</sup>                                | Channel receives signal values         |
| Rust (2018)         | `tokio::signal::unix::signal(kind)`<sup>[14]</sup>                           | Stream yields on signal delivery       |
| .NET (2002)         | `Console.CancelKeyPress`<sup>[15]</sup>                                      | Event handler on Ctrl+C                |
| Python (2015)       | `asyncio.loop.add_signal_handler`<sup>[16]</sup>                             | Callback registered on event loop      |
| Asio (2010)         | `asio::signal_set`<sup>[12]</sup>                                            | Set with async_wait                    |
| libuv (2012)        | `uv_signal_t`<sup>[17]</sup>                                                 | Handle with callback on signal         |

### 6.1 Go

Go's `os/signal.Notify` registers a set of signals on a channel<sup>[13]</sup>. The caller receives signal values from the channel. Cancellation is `signal.Stop(c)`. The model is a set (the signal list passed to `Notify`) that delivers values through a channel (Go's native async primitive).

### 6.2 Rust

Tokio provides `tokio::signal::unix::signal(SignalKind)` for individual signal streams and `tokio::signal::ctrl_c()` for the common `SIGINT` case<sup>[14]</sup>. The stream model yields one event per signal delivery. The shape is per-signal, but multiple signals compose through `tokio::select!`, which serves the same role as `when_any`.

### 6.3 .NET

.NET provides `Console.CancelKeyPress`, an event that fires on `CTRL_C_EVENT` and `CTRL_BREAK_EVENT`<sup>[15]</sup>. The scope is narrower than POSIX signals - only console interrupt events - but the pattern is the same: Register interest, receive notification through the async framework.

### 6.4 Python

Python's `asyncio` provides `loop.add_signal_handler(signum, callback)`<sup>[16]</sup>. The handler runs on the event loop thread, not in signal context. The conversion from signal context to event loop context uses the self-pipe trick internally.

### 6.5 Asio

Asio's `signal_set` is the direct ancestor of the type proposed here<sup>[12]</sup>. The API is `add(signal_number)`, `remove(signal_number)`, `clear()`, `async_wait(handler)`, `cancel()`. The shape is the same; the async model differs (completion handler vs IoAwaitable).

### 6.6 libuv

libuv provides `uv_signal_t`, a handle that invokes a callback when a specified signal is delivered<sup>[17]</sup>. Each handle watches one signal. Multiple signals require multiple handles. The per-signal model is the one `signal_set` collapses into a single wait.

**Six ecosystems. Each converts signals into async events. The C++ standard library does not.**

---

## 7. Anticipated Objections

### 7.1 "But `<csignal>` Already Handles Signals"

`<csignal>` provides `signal()` and `raise()`. `signal()` installs a handler that runs in signal context. Section 2.1 documents the restrictions: no allocation, no locks, no buffered I/O, no exceptions. The handler can set a `volatile sig_atomic_t` flag and almost nothing else. Every production server works around these restrictions with polling loops, self-pipe tricks, or platform-specific mechanisms. `<csignal>` provides signal disposition. It does not provide signal handling that composes with modern C++.

### 7.2 "But Signals Are POSIX-Specific"

Windows has `SetConsoleCtrlHandler`<sup>[10]</sup>, which intercepts `CTRL_C_EVENT`, `CTRL_BREAK_EVENT`, and `CTRL_CLOSE_EVENT`. The abstraction maps console events to signal numbers (Section 3.3). The application writes `sigs.add(SIGINT)` on both platforms. The platform difference is in the implementation, not the interface.

Go, Rust, Python, and .NET all provide cross-platform signal handling that maps platform-specific mechanisms to a common API. The C++ standard can do the same.

### 7.3 "But Signal Handling Should Be OS-Level Only"

The argument is that signal handling is inherently platform-specific and should not be abstracted. The counterargument is that every language runtime listed in Section 6 already abstracts it. The question is not whether signal handling should be abstracted - six ecosystems have answered that - but whether C++ should require every application to re-implement the abstraction.

`std::filesystem` abstracts platform-specific file operations. `std::thread` abstracts platform-specific thread creation. `std::chrono` abstracts platform-specific clock sources. Signal handling is the same category: a platform-specific resource with a portable abstract shape.

### 7.4 "But the Flags Parameter Exposes Platform Details"

The `flags_t` parameter is optional. The one-argument `add()` overload requires no platform knowledge. Applications that need `SA_NOCLDWAIT` or `SA_RESTART` already use those flags through `sigaction` today. The standard library provides a portable path to the same flags through a type-safe parameter, instead of requiring the application to drop to raw POSIX.

The alternative - omitting flags entirely - would force applications that need them to use both `signal_set` for async waiting and raw `sigaction` for flag control. Two mechanisms for one signal is worse than one mechanism with an optional parameter.

---

## 8. Deferrals

Five deferrals. Each is named so the scope is unambiguous.

### 8.1 Signal Masking

Per-thread signal masking (`pthread_sigmask`, `sigprocmask`) is not part of this proposal. `signal_set::add()` blocks the registered signal as an implementation detail (Section 3.1), but the masking API is not exposed. Exposing per-thread signal masks is a concurrency concern that interacts with thread pools and strand-based dispatch in ways that require separate analysis.

### 8.2 Real-Time Signals

POSIX real-time signals (`SIGRTMIN` through `SIGRTMAX`) support queuing and payload delivery through `sigqueue`<sup>[7]</sup>. The `signal_set` type accepts any `int` signal number, so real-time signal numbers work mechanically. Queued payload delivery (`siginfo_t` data) is not exposed. Extending the `wait()` return type to carry `siginfo_t` payloads is a possible future addition.

### 8.3 Windows Console Events Beyond Ctrl+C

Windows console events include `CTRL_LOGOFF_EVENT` and `CTRL_SHUTDOWN_EVENT` in addition to the three events mapped in Section 3.3. These events are service-specific and have different semantics from POSIX signals. Mapping them is deferred pending demand from Windows service applications.

### 8.4 Signal Chaining

Some applications need to install a signal handler that calls a previous handler after performing its own work. Signal chaining is a `sigaction`-level concern. The `signal_set` abstraction replaces signal handlers with awaitable events; chaining in the traditional sense does not apply. Applications that need chaining should use `sigaction` directly.

### 8.5 `signalfd` Flag Propagation

Linux's `signalfd` supports `SFD_NONBLOCK` and `SFD_CLOEXEC` as creation flags. These are implementation details of the reactor, not application-level concerns. The implementation sets them; the application does not need to know.

---

## 9. Why Now

The committee has had signal handling in front of it before.

| Year | Paper                                                                                           | Outcome                                          |
| ---- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 2005 | [N1925](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf)<sup>[18]</sup>      | First networking proposal for TR2                |
| 2018 | [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[19]</sup>      | Networking TS included `signal_set`              |
| 2026 | [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup>  | Network Endeavor frames signals as Paper 9       |

The Networking TS included `basic_signal_set`. The committee did not advance the Networking TS. The type never reached the IS. The shape is the same; the async model is coroutine-native instead of callback-based.

`<csignal>` has not been updated since C89. In the same period, every other language in production use has shipped async signal handling. The gap between the C++ standard and what C++ applications actually need for signal handling is thirty-seven years wide and growing.

---

## 10. Closing

We built this. It works. We are reporting what we found. The proposed wording for the vocabulary documented here lives in *Signals*<sup>[2]</sup>.

---

## Appendix A. `<std::io>` Synopsis (Informative)

Signal-set-only synopsis. The full `std::io` namespace is documented across the series.

```cpp
namespace std::io {

  class signal_set {
  public:
    using flags_t = /* implementation-defined */;

    explicit signal_set(execution_context& ctx);
    ~signal_set();

    signal_set(signal_set const&) = delete;
    signal_set& operator=(signal_set const&) = delete;

    void add(int signal_number);
    void add(int signal_number, flags_t flags);
    void remove(int signal_number);
    void clear();

    IoAwaitable auto wait();
    void cancel();
  };

}
```

---

## Appendix B. Corosio Header Inventory

The signal handling vocabulary ships in the following headers in [Corosio](https://github.com/cppalliance/corosio)<sup>[5]</sup>. The list is a pointer to the implementation for the reader who wants to inspect it.

| Header                                         | Provides                                              |
| ---------------------------------------------- | ----------------------------------------------------- |
| `boost/corosio/signal_set.hpp`                 | `signal_set` type, `add`, `remove`, `clear`, `wait`, `cancel` |
| `boost/corosio/detail/signal_set_service.hpp`  | Platform-specific signal delivery (signalfd, kqueue, Windows) |

---

## Acknowledgments

Christopher Kohlhoff designed the original `signal_set` in Asio<sup>[12]</sup>. The type, its API shape, and its integration with the reactor are his work. This paper recovers the shape for a coroutine-native model.

Mohammad Nejati implemented the Corosio signal handling backend across `signalfd`, `kqueue`, and Windows console events.

The Go, Rust, Python, and libuv teams independently validated the set-or-channel model for async signal handling. Their designs are evidence the C++ committee did not need to commission.

---

## References

[1] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[2] *Signals* (Vinnie Falco, 2026). Companion ask paper. D0017R0.

[3] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[4] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[5] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[6] [C23 Standard](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3220.pdf) - Section 7.14.1.1, signal handler restrictions (ISO/IEC, 2024).

[7] [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) - Signal concepts, async-signal-safe functions (The Open Group, 2024).

[8] [`signalfd(2)` man page](https://man7.org/linux/man-pages/man2/signalfd.2.html) - Linux signal file descriptor (Linux man-pages project, 2008-2026).

[9] [`kqueue(2)` man page](https://man.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2) - BSD event notification with EVFILT_SIGNAL (FreeBSD, 2000-2026).

[10] [`SetConsoleCtrlHandler` function](https://learn.microsoft.com/en-us/windows/console/setconsolectrlhandler) - Windows console control handler (Microsoft, 1999-2026).

[11] Daniel J. Bernstein, [The self-pipe trick](https://cr.yp.to/docs/selfpipe.html) (1990).

[12] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - `signal_set` (Christopher Kohlhoff, 2010-2026).

[13] [Go standard library: `os/signal`](https://pkg.go.dev/os/signal) - `Notify`, `Stop`, `NotifyContext` (The Go Authors, 2012-2026).

[14] [Tokio: `tokio::signal`](https://docs.rs/tokio/latest/tokio/signal/index.html) - Async signal handling for Rust (Tokio Contributors, 2018-2026).

[15] [.NET API: `Console.CancelKeyPress`](https://learn.microsoft.com/en-us/dotnet/api/system.console.cancelkeypress) - Console interrupt event (Microsoft, 2002-2026).

[16] [Python `asyncio` event loop: `add_signal_handler`](https://docs.python.org/3/library/asyncio-eventloop.html#unix-signals) - Signal handler on event loop (Python Software Foundation, 2015-2026).

[17] [libuv: `uv_signal_t`](https://docs.libuv.org/en/v1.x/signal.html) - Signal handle type (libuv contributors, 2012-2026).

[18] [N1925](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf) - "Networking proposal for TR2 (rev. 1)" (Gerhard Wesp, 2005).

[19] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).
