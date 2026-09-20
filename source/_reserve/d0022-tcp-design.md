---
title: "TCP: Design Rationale"
document: D0022R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The committee has been trying to standardize TCP since 2005. This paper documents the design that ships.

[N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf)<sup>[1]</sup> proposed TCP sockets for TR2. The Networking TS ([N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[2]</sup>) codified the operational semantics. Neither reached the IS. The types in the companion ask paper *TCP*<sup>[19]</sup> are the same shapes - `tcp_socket`, `tcp_acceptor`, `endpoint`, `ipv4_address`, `ipv6_address` - recovered on the coroutine-native path with the _IoAwaitable_ protocol ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[3]</sup>). A `tcp_socket` satisfies `Stream` (Paper 6). A `tcp_acceptor` produces `tcp_socket` objects. The vocabulary ships in [Corosio](https://github.com/cppalliance/corosio)<sup>[4]</sup>, is used by three Boost libraries and validated in production trading infrastructure ([P4125R1](https://isocpp.org/files/papers/P4125R1.pdf)<sup>[5]</sup>).

This paper is Paper 11 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[6]</sup>. Read *TCP*<sup>[19]</sup> for the proposal; read this paper when you need the design audit trail.

---

## Revision History

### R0: May 2026

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author develops [Capy](https://github.com/cppalliance/capy)<sup>[7]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[4]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

This paper examines the published record. That effort requires re-examining consequential papers.

This paper asks for nothing.

---

## 2. Twenty Years of Trying

TCP sockets have been proposed, specified, revised, and deferred more times than any other standard library facility. The timeline records why the committee does not have them.

| Year | Paper | What happened |
|------|-------|---------------|
| 2005 | [N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf)<sup>[1]</sup> | First networking proposal for TR2. TCP sockets, UDP sockets, name resolution. |
| 2005 | [N1926](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1926.pdf)<sup>[8]</sup> | Kohlhoff's networking library proposal. The shape that became Asio. |
| 2014 | [N4242](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4242.html)<sup>[9]</sup> | Executors and Asynchronous Operations. TCP in the context of executor design. |
| 2018 | [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[2]</sup> | Networking TS Working Draft. Full TCP specification with named requirements. |
| 2021 | [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[10]</sup> | LEWG polls. Networking to be built on sender/receiver. No sender-based TCP has shipped. |
| 2026 | [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[6]</sup> | Network Endeavor. TCP is Paper 11 in a 14-paper series with implementation. |

Twenty-one years between the first TCP proposal and this paper. The shapes have not changed. The completion model has. The Networking TS specified TCP with callback-based completion tokens. This paper specifies TCP with the _IoAwaitable_ protocol. The socket operations are the same. The async mechanism is different. The implementation ships.

---

## 3. TCP Socket as Stream

A `tcp_socket` satisfies `Stream` - the concept defined in Paper 6 (Stream Concepts) of the series. This is the central design decision.

### 3.1 Why Stream

`Stream` requires `read_some` and `write_some`, each returning `IoAwaitable`. A `tcp_socket` provides both. The consequence:

```cpp
std::io::task<> echo(any_stream& stream)
{
    char buf[4096];
    for (;;)
    {
        auto [ec, n] =
            co_await stream.read_some(
                mutable_buffer(buf, sizeof(buf)));
        if (ec)
            co_return;
        auto [wec, wn] =
            co_await stream.write_some(
                const_buffer(buf, n));
        if (wec)
            co_return;
    }
}
```

This function works with TCP sockets, TLS streams, Unix domain sockets, memory streams, and any future transport that satisfies `Stream`. The function is compiled once. It ships as a binary. The transport behind `any_stream` is invisible.

### 3.2 ABI Stability through `any_stream`

`any_stream` type-erases any `Stream` behind a vtable. Libraries accept `any_stream&` in their public interfaces and compile against it. The concrete transport - `tcp_socket`, `tls_stream`, or a test mock - is bound at runtime.

```cpp
// Public header - no Corosio, no Asio, no platform headers.
std::io::task<response>
    handle_request(any_stream& stream);

// .cpp file - the only file that knows the concrete type.
tcp_socket sock(ctx);
co_await sock.connect(ep);
auto resp = co_await handle_request(sock);
```

The HTTP library does not know it is talking to TCP. It does not need to. The type erasure boundary is the compilation boundary. New transports plug in without recompiling the library.

### 3.3 The Frame Subsidy

When a coroutine calls `co_await stream.read_some(buf)`, the caller's frame persists across suspension. That frame is already allocated - HALO cannot apply when frame lifetime depends on an external event ([P2477R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2477r3.html)<sup>[11]</sup>). The operation state lives in the coroutine frame, not in a template. `any_stream` type-erases without per-operation allocation because the frame allocation we cannot avoid subsidizes the type erasure we want.

---

## 4. Acceptor Design

The acceptor follows the BSD sockets bind/listen/accept pattern. Each step is explicit. No constructor combines them.

### 4.1 Bind, Listen, Accept

```cpp
tcp_acceptor acceptor(ctx);
acceptor.bind(
    endpoint(ipv4_address::any(), 8080));
acceptor.listen();

for (;;)
{
    auto [ec, sock] =
        co_await acceptor.accept();
    if (ec)
        break;
    run_async(ctx.get_executor())(
        handle_connection(std::move(sock)));
}
```

**`bind`** is synchronous. It associates the acceptor with a local endpoint. Failure is immediate and synchronous - the port is in use, the address is invalid.

**`listen`** is synchronous. It marks the socket as passive and sets the connection backlog. The backlog parameter has an implementation-defined default. Binding and listening are distinct operations because some protocols require setting socket options between bind and listen (e.g. `reuse_address`).

**`accept`** is asynchronous. It suspends until a connection arrives. The result is a connected `tcp_socket` ready for I/O. The accepted socket inherits the execution context of the acceptor.

### 4.2 Why Not a Single Constructor

A constructor that binds, listens, and accepts in one call hides the failure mode. If bind fails, the caller does not know. If listen fails, the caller cannot distinguish it from a bind failure. Explicit steps give the caller explicit error points. The BSD interface has been explicit since 1983 for the same reason.

### 4.3 `accept` Returns `tcp_socket`

`accept` returns a `tcp_socket` by value (moved). Not a `unique_ptr<tcp_socket>`. Not a reference. The socket is a concrete object that the caller owns. Move semantics make the transfer zero-cost. The caller decides what to do with it: store it, wrap it in `any_stream`, or pass it to a handler coroutine.

---

## 5. IP Address Types

### 5.1 Why Dedicated Types, Not Integers

An IPv4 address is a 32-bit integer. An IPv6 address is a 128-bit integer. Why not `std::uint32_t` and `std::array<std::uint8_t, 16>`?

Because the type system exists to prevent exactly this class of error:

```cpp
// With integers:
void connect(uint32_t addr, uint16_t port);
connect(port, addr);   // compiles. Wrong.

// With types:
void connect(ipv4_address addr, uint16_t port);
connect(port, addr);   // ill-formed.
```

`ipv4_address` carries classifiers (`is_loopback`, `is_multicast`, `is_unspecified`), formatting (`to_string`), and parsing (`from_string`) that a bare integer does not. The classifiers are `constexpr` and carry zero runtime cost when unused.

Every language with a networking library provides dedicated address types: Go `net.IP`, Rust `std::net::Ipv4Addr` / `Ipv6Addr`, .NET `System.Net.IPAddress`, Python `ipaddress.IPv4Address` / `IPv6Address`, Java `java.net.Inet4Address` / `Inet6Address`. C++ is the outlier that does not.

### 5.2 Why a Variant for Dual-Stack

`ip_address` holds either an `ipv4_address` or an `ipv6_address`. The motivating use case is a dual-stack server that accepts connections from both protocol families:

```cpp
tcp_acceptor acceptor(ctx);
acceptor.bind(
    endpoint(ip_address(
        ipv6_address::any()), 443));
acceptor.listen();
```

With a `v6`-only acceptor on a dual-stack host, incoming IPv4 connections appear as IPv4-mapped IPv6 addresses. The `ip_address` variant represents both without forcing the caller to branch on protocol family at every point an address is stored, logged, or compared.

The alternative - two unrelated types with no common vocabulary - forces every function that stores or passes an address to be templated or overloaded. The variant captures the closed set of two families in one type.

### 5.3 `from_string` Returns a Result

```cpp
auto addr = ipv4_address::from_string("192.168.1.1");
if (!addr)
    handle_error(addr.error());
```

Parsing user-supplied address strings is a routine operation. It must not throw - invalid input is expected, not exceptional. `from_string` returns a result type. `to_string` is the inverse and does not fail.

---

## 6. Socket Options

Socket options are type-safe wrappers around `setsockopt` / `getsockopt`. Each option type encapsulates the SOL/SO level and name constants.

```cpp
sock.set_option(tcp_nodelay(true));
sock.set_option(reuse_address(true));
sock.set_option(
    receive_buffer_size(65536));

bool nodelay_val;
sock.get_option(tcp_nodelay(nodelay_val));
```

### 6.1 Minimum Option Set

The following options cover the needs that recur across networking codebases:

| Option | SOL/SO | Purpose |
|--------|--------|---------|
| `tcp_nodelay` | `IPPROTO_TCP` / `TCP_NODELAY` | Disable Nagle's algorithm for latency-sensitive protocols |
| `reuse_address` | `SOL_SOCKET` / `SO_REUSEADDR` | Allow binding to a recently closed address |
| `keep_alive` | `SOL_SOCKET` / `SO_KEEPALIVE` | Enable TCP keepalive probes |
| `receive_buffer_size` | `SOL_SOCKET` / `SO_RCVBUF` | Set the receive buffer size |
| `send_buffer_size` | `SOL_SOCKET` / `SO_SNDBUF` | Set the send buffer size |
| `linger` | `SOL_SOCKET` / `SO_LINGER` | Control close behaviour (linger on close, timeout) |

### 6.2 Extensibility

The option model is open. User-defined option types that provide the same interface (level, name, data pointer, data size) work with `set_option` / `get_option` without modifying the socket class. Platform-specific options are accessible through the same interface.

---

## 7. The Three Layers

The three-layer architecture from [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[6]</sup> Section 6 applies uniformly to TCP types.

### 7.1 Abstract: `io_stream`

`io_stream` provides protocol-agnostic byte I/O with virtual dispatch. A library that accepts `any_stream&` (the type-erased wrapper) compiles once and works with TCP, TLS, Unix domain sockets, or test mocks.

**Trade-off:** Virtual dispatch per read/write. The cost is bounded and constant - one pointer indirection, no allocation. For HTTP servers processing kilobytes of headers and megabytes of bodies, the vtable cost is immeasurable relative to the I/O latency.

### 7.2 Concrete: `tcp_socket`

The full protocol-specific API: `connect`, `shutdown`, endpoint queries, socket options. Still virtual dispatch for `read_some` / `write_some`. Separately compilable. The layer most application code uses.

### 7.3 Native: `native_tcp_socket<Backend>`

Templated on the platform backend (`epoll_backend`, `iocp_backend`, `kqueue_backend`). Member function shadowing eliminates the vtable. Full inlining. For hot paths where every nanosecond matters.

The three layers share a single inheritance chain. A `native_tcp_socket<Backend>` is-a `tcp_socket` is-a `io_stream`. The user chooses the abstraction level. Code written against a higher layer works unchanged when the concrete type is a lower layer.

---

## 8. Convergence

Six independently designed ecosystems provide the same TCP vocabulary. The shapes converge because the problem is the same: Wrap a file descriptor (or HANDLE), associate it with an address, read bytes, write bytes.

| Ecosystem | Socket type | Acceptor/Listener | Address types |
|-----------|-------------|-------------------|---------------|
| BSD (1983) | `int` (fd) | `accept()` | `struct sockaddr_in` / `sockaddr_in6` |
| Go (2009) | `net.TCPConn` | `net.TCPListener` | `net.IP`, `net.TCPAddr` |
| Rust / Tokio (2018) | `tokio::net::TcpStream` | `tokio::net::TcpListener` | `std::net::SocketAddr` |
| .NET (2002) | `TcpClient` / `NetworkStream` | `TcpListener` | `IPAddress`, `IPEndPoint` |
| Python asyncio (2014) | `asyncio.StreamReader` / `StreamWriter` | `asyncio.start_server` | implicit |
| Asio / This paper | `tcp_socket` | `tcp_acceptor` | `ipv4_address`, `ipv6_address`, `endpoint` |

**Six ecosystems. Same operations. Same shape.**

The naming varies - `TcpStream` vs `tcp_socket` vs `TCPConn` - but the operations are identical: connect, read, write, shutdown, close. The acceptor pattern is identical: bind, listen, accept returning a connected socket. The address model is identical: an IP address paired with a port number.

---

## 9. Anticipated Objections

### 9.1 "But the Networking TS Already Standardised TCP"

It specified TCP. The committee did not advance the Networking TS to the IS. The types it defined never shipped in a standard library. The shapes are the same; the completion model is different. The Networking TS used callback-based completion tokens. This paper uses the _IoAwaitable_ protocol. The operational semantics - connect, read_some, write_some, shutdown, close - are unchanged.

The Networking TS spent fourteen years in committee. The committee's consensus shifted to "networking should be built on sender/receiver" ([P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[10]</sup>). No sender-based TCP has shipped. The coroutine-native path has a shipping implementation.

### 9.2 "But Sockets Need More Flexibility"

The three-layer architecture provides three levels of abstraction. The abstract layer (`any_stream`) provides maximum flexibility - any transport plugs in. The concrete layer (`tcp_socket`) provides the full TCP API. The native layer (`native_tcp_socket<Backend>`) exposes the platform backend for zero-overhead access.

If a use case needs `setsockopt` with a platform-specific option not covered by the type-safe wrappers, `native_handle()` provides the raw file descriptor. The escape hatch exists ([P4035R1](https://isocpp.org/files/papers/P4035R1.pdf)<sup>[12]</sup>).

### 9.3 "But IP Addresses Should Use `std::string`"

Strings are not addresses. An IPv4 address is four bytes. Its string representation (`"192.168.1.1"`) is a serialization format. Comparison, hashing, and classification of addresses are O(1) on the integer representation and O(n) on the string. Every networking library in every language provides dedicated address types for this reason. Section 5.1 documents the convergence.

Parsing (`from_string`) returns a result type. Formatting (`to_string`) is available. The dedicated type provides both operations and is correct for storage, comparison, and protocol operations.

### 9.4 "But `accept` Should Return a `unique_ptr`"

`tcp_socket` is move-only. `accept` returns a `tcp_socket` by value (moved from internal storage). There is no heap allocation in the return path. The caller owns the socket and decides its lifetime.

`unique_ptr<tcp_socket>` would add a heap allocation for no benefit. The socket is already move-only. The object size is small (a file descriptor plus a pointer to the execution context). The move is cheaper than the allocation.

If the caller wants heap storage, it writes `auto p = std::make_unique<tcp_socket>(std::move(sock))`. The decision belongs to the caller.

---

## 10. Deferrals

Five features are out of scope for this paper. Each is named so the boundary is unambiguous.

### 10.1 Multipath TCP (MPTCP)

MPTCP ([RFC 8684](https://www.rfc-editor.org/rfc/rfc8684)<sup>[13]</sup>) allows a single TCP connection to use multiple network paths. Kernel support is available on Linux and macOS. The socket API extension is a socket option (`IPPROTO_MPTCP`). When the standard TCP vocabulary is in place, MPTCP can be added as a socket option without changing the socket type.

### 10.2 Socket Pairs

`socketpair()` creates a pair of connected Unix domain sockets. It is a Unix-specific facility with no Windows equivalent. It belongs in the Unix domain sockets paper, not in the TCP paper.

### 10.3 Raw Sockets

Raw sockets (`SOCK_RAW`) require elevated privileges and are used for protocol development, network monitoring, and ICMP. They operate below the transport layer. A separate paper is warranted if demand exists.

### 10.4 Unix Domain Sockets

`local_stream_socket` and `local_stream_acceptor` provide inter-process communication without the network stack. They satisfy `Stream` and share the acceptor pattern with TCP. They ship in Corosio on POSIX platforms. They are deferred to a separate paper because they do not use IP addresses or port numbers and have platform-specific behaviour (file-system paths, abstract names, credential passing).

### 10.5 SCTP

The Stream Control Transmission Protocol ([RFC 9260](https://www.rfc-editor.org/rfc/rfc9260)<sup>[14]</sup>) provides message-oriented, multi-stream transport with built-in multihoming. It does not share the `Stream` model (it is message-based, not byte-based). A separate paper is warranted if demand exists.

---

## 11. Why Now

The committee has deferred TCP for twenty-one years.

The deferral was not without reason. The executor model was unsettled. The completion model was unsettled. The relationship between networking and sender/receiver was unsettled. Each deferral waited for a prerequisite.

The prerequisites are now in place. Paper 1 ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[3]</sup>) defines the execution model. Paper 4 defines the buffer vocabulary. Paper 6 defines the stream concepts. Paper 11 defines TCP as a concrete instantiation of those abstractions.

The implementation ships. [Corosio](https://github.com/cppalliance/corosio)<sup>[4]</sup> provides `tcp_socket`, `tcp_acceptor`, `endpoint`, `ipv4_address`, and `ipv6_address` on Linux (epoll, io_uring), Windows (IOCP), and macOS (kqueue). [P4125R1](https://isocpp.org/files/papers/P4125R1.pdf)<sup>[5]</sup> reports a derivatives exchange porting from Asio callbacks to coroutine-native TCP. The types have been validated under production conditions.

Every year the committee does not have TCP in the standard is a year every C++ networking application depends on a third-party library for the most fundamental transport protocol on the internet.

---

## 12. Closing

We built this. It works. We are reporting what we found. Proposed wording for the vocabulary documented here lives in *TCP*<sup>[19]</sup>.

---

## Appendix A. `<std::io>` Synopsis (TCP)

```cpp
namespace std::io {

  // IP address types
  class ipv4_address
  {
  public:
    constexpr ipv4_address() noexcept;
    constexpr explicit ipv4_address(
        std::uint32_t addr) noexcept;
    constexpr ipv4_address(
        std::uint8_t a, std::uint8_t b,
        std::uint8_t c, std::uint8_t d) noexcept;

    constexpr std::uint32_t
        to_uint() const noexcept;
    std::string to_string() const;
    static result<ipv4_address>
        from_string(std::string_view s) noexcept;

    constexpr bool is_loopback() const noexcept;
    constexpr bool is_multicast() const noexcept;
    constexpr bool is_unspecified() const noexcept;

    friend constexpr bool operator==(
        ipv4_address const&,
        ipv4_address const&) noexcept = default;
    friend constexpr auto operator<=>(
        ipv4_address const&,
        ipv4_address const&) noexcept = default;

    static constexpr ipv4_address any() noexcept;
    static constexpr ipv4_address
        loopback() noexcept;
  };

  class ipv6_address
  {
  public:
    constexpr ipv6_address() noexcept;
    explicit ipv6_address(
        std::array<std::uint8_t, 16> const& bytes)
        noexcept;

    std::array<std::uint8_t, 16>
        to_bytes() const noexcept;
    std::string to_string() const;
    static result<ipv6_address>
        from_string(std::string_view s) noexcept;

    constexpr bool is_loopback() const noexcept;
    constexpr bool is_multicast() const noexcept;
    constexpr bool is_unspecified() const noexcept;
    constexpr bool
        is_link_local() const noexcept;
    constexpr bool is_v4_mapped() const noexcept;

    constexpr std::uint32_t
        scope_id() const noexcept;
    constexpr void set_scope_id(
        std::uint32_t id) noexcept;

    friend constexpr bool operator==(
        ipv6_address const&,
        ipv6_address const&) noexcept = default;
    friend constexpr auto operator<=>(
        ipv6_address const&,
        ipv6_address const&) noexcept = default;

    static constexpr ipv6_address any() noexcept;
    static constexpr ipv6_address
        loopback() noexcept;
  };

  class ip_address
  {
  public:
    constexpr ip_address() noexcept;
    constexpr ip_address(
        ipv4_address const& addr) noexcept;
    constexpr ip_address(
        ipv6_address const& addr) noexcept;

    constexpr bool is_v4() const noexcept;
    constexpr bool is_v6() const noexcept;
    constexpr ipv4_address to_v4() const;
    constexpr ipv6_address to_v6() const;

    std::string to_string() const;
    static result<ip_address>
        from_string(std::string_view s) noexcept;

    constexpr bool is_loopback() const noexcept;
    constexpr bool is_multicast() const noexcept;
    constexpr bool is_unspecified() const noexcept;

    friend constexpr bool operator==(
        ip_address const&,
        ip_address const&) noexcept = default;
    friend constexpr auto operator<=>(
        ip_address const&,
        ip_address const&) noexcept = default;
  };

  // Endpoint
  class endpoint
  {
  public:
    constexpr endpoint() noexcept;
    constexpr endpoint(
        ip_address addr,
        std::uint16_t port) noexcept;

    constexpr ip_address
        address() const noexcept;
    constexpr void set_address(
        ip_address addr) noexcept;
    constexpr std::uint16_t
        port() const noexcept;
    constexpr void set_port(
        std::uint16_t port) noexcept;

    std::string to_string() const;

    friend constexpr bool operator==(
        endpoint const&,
        endpoint const&) noexcept = default;
    friend constexpr auto operator<=>(
        endpoint const&,
        endpoint const&) noexcept = default;
  };

  // TCP socket - satisfies Stream
  class tcp_socket
  {
  public:
    explicit tcp_socket(
        execution_context& ctx);

    tcp_socket(tcp_socket&& other) noexcept;
    tcp_socket& operator=(
        tcp_socket&& other) noexcept;
    ~tcp_socket();

    IoAwaitable auto connect(
        endpoint const& ep);
    IoAwaitable auto read_some(
        MutableBufferSequence auto buffers);
    IoAwaitable auto write_some(
        ConstBufferSequence auto buffers);

    void shutdown(shutdown_type what);
    void close();

    bool is_open() const noexcept;
    endpoint local_endpoint() const;
    endpoint remote_endpoint() const;

    void set_option(/* socket option */);
    void get_option(/* socket option */) const;
    native_handle_type native_handle();
  };

  // TCP acceptor
  class tcp_acceptor
  {
  public:
    explicit tcp_acceptor(
        execution_context& ctx);

    tcp_acceptor(
        tcp_acceptor&& other) noexcept;
    tcp_acceptor& operator=(
        tcp_acceptor&& other) noexcept;
    ~tcp_acceptor();

    void bind(endpoint const& ep);
    void listen(
        int backlog
            = /* implementation-defined */);
    IoAwaitable auto accept();

    void close();
    bool is_open() const noexcept;
    endpoint local_endpoint() const;

    void set_option(/* socket option */);
    native_handle_type native_handle();
  };

}
```

---

## Appendix B. Corosio Headers

The vocabulary in this paper ships in the following Corosio headers:

| Header | Provides |
|--------|----------|
| `corosio/ip/address_v4.hpp` | `ipv4_address` |
| `corosio/ip/address_v6.hpp` | `ipv6_address` |
| `corosio/ip/address.hpp` | `ip_address` (variant) |
| `corosio/ip/endpoint.hpp` | `endpoint` |
| `corosio/ip/tcp.hpp` | `tcp_socket`, `tcp_acceptor` |
| `corosio/socket_options.hpp` | `tcp_nodelay`, `reuse_address`, `keep_alive`, etc. |

---

## Acknowledgments

Christopher Kohlhoff designed the Asio TCP socket, acceptor, endpoint, and IP address types. Twenty years of production deployment is the foundation this work builds on. The Networking TS authors codified the operational semantics. The shapes in this paper are the shapes they specified.

The integration partner reported in [P4125R1](https://isocpp.org/files/papers/P4125R1.pdf)<sup>[5]</sup> validated these types under production conditions at a derivatives exchange. Marcelo Zimbres Silva, Ruben Perez, and the Boost.Postgres team adopted the Corosio TCP types for their libraries.

The committee designed C++20 coroutines. Gor Nishanov, Lewis Baker, and their collaborators gave C++ the language mechanisms that make coroutine-native TCP possible.

---

## References

[1] [N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf) - "Networking proposal for TR2 (rev. 1)" (Gerhard Wesp, 2005).

[2] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).

[3] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[4] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[5] [P4125R1](https://isocpp.org/files/papers/P4125R1.pdf) - "Coroutine-Native I/O at a Derivatives Exchange" (Mungo Gill, 2026).

[6] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[7] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[8] [N1926](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1926.pdf) - "A Networking Library for TR2 (Revision 1)" (Christopher Kohlhoff, 2005).

[9] [N4242](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4242.html) - "Executors and Asynchronous Operations, Revision 1" (Christopher Kohlhoff, 2014).

[10] [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html) - "2021 October Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[11] [P2477R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2477r3.html) - "Allow programmers to control coroutine elision" (Xu, 2022).

[12] [P4035R1](https://isocpp.org/files/papers/P4035R1.pdf) - "The Need for Escape Hatches" (Vinnie Falco, 2026).

[13] [RFC 8684](https://www.rfc-editor.org/rfc/rfc8684) - "TCP Extensions for Multipath Operation with Multiple Addresses" (Alan Ford, Costin Raiciu, Mark Handley, Olivier Bonaventure, Christoph Paasch, 2020).

[14] [RFC 9260](https://www.rfc-editor.org/rfc/rfc9260) - "Stream Control Transmission Protocol" (Randall Stewart, Michael T&uuml;xen, Karen Nielsen, 2022).

[15] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - TCP socket, acceptor, and endpoint types (Christopher Kohlhoff, 2003-2026).

[16] [P4172R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r1.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[17] [P4099R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4099r0.pdf) - "History: The Twenty-One Year Networking Arc" (Vinnie Falco, 2026).

[18] [P4088R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r0.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[19] *TCP* (Vinnie Falco, 2026). Companion ask paper. D0021R0.
