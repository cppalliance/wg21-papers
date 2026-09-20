---
title: "UDP: Design Rationale"
document: D0026R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper documents the design rationale for `std::io::udp_socket`.

D0025R0<sup>[1]</sup> proposes the normative vocabulary - `udp_socket`, `send_to`, `receive_from`, `bind`, multicast group management, and connected-mode operations. This paper is the companion record: why datagrams require a separate type, what alternatives were considered, how UDP relates to TCP streams, where connected mode matters, and what the convergence evidence shows. Read D0025R0<sup>[1]</sup> first for the proposal; read this paper when you need the design audit trail.

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

This paper is part of the [Network Endeavor](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) ([P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[2]</sup>), a project to bring coroutine-native I/O to C++.

The author develops and maintains [Capy](https://github.com/cppalliance/capy)<sup>[3]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[4]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

This paper asks for nothing.

---

## 2. Why UDP

UDP is the second transport protocol in the Internet Protocol Suite. It carries roughly 40% of Internet traffic by volume<sup>[5]</sup>. Five domains depend on it directly.

**DNS.** Every name resolution on the Internet begins with a UDP datagram. DNS stub resolvers send queries as single UDP messages and receive responses the same way. TCP is the fallback for responses exceeding 512 bytes (or 4096 with EDNS0), but the common path is UDP. A standard library that provides TCP without UDP cannot perform name resolution at the transport level.

**QUIC/HTTP/3.** QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000)<sup>[6]</sup>) is the transport beneath HTTP/3 ([RFC 9114](https://www.rfc-editor.org/rfc/rfc9114)<sup>[7]</sup>). QUIC runs over UDP. Chrome, Firefox, Safari, and Edge use QUIC for the majority of their HTTP traffic. A standard library that ships TCP sockets but not UDP sockets cannot host a QUIC implementation. The QUIC layer needs raw UDP - `send_to`, `receive_from`, and `bind` - not a stream abstraction.

**Game networking.** Real-time multiplayer games send player state updates at 20-60 Hz. Each update is a datagram. Lost packets are acceptable - the next update supersedes the lost one. TCP's retransmission and head-of-line blocking are actively harmful. Game networking protocols (ENet, GameNetworkingSockets, Photon) are built on UDP.

**Media streaming.** RTP ([RFC 3550](https://www.rfc-editor.org/rfc/rfc3550)<sup>[8]</sup>) carries audio and video over UDP. WebRTC, VoIP, and live broadcast systems use RTP. A dropped audio frame is better than a delayed one. UDP's tolerance for packet loss is a feature, not a deficiency.

**IoT protocols.** CoAP ([RFC 7252](https://www.rfc-editor.org/rfc/rfc7252)<sup>[9]</sup>) is the constrained-device alternative to HTTP. It runs over UDP. Constrained devices cannot afford TCP's three-way handshake and connection state. mDNS and DNS-SD use UDP multicast for zero-configuration service discovery.

The standard library already provides TCP through Paper 11. Without UDP, the standard covers one of two transport protocols. The gap is not theoretical - it blocks DNS, QUIC, games, media, and IoT.

---

## 3. Datagram vs Stream

TCP delivers a byte stream. The kernel may coalesce multiple `write` calls into one segment, split one `write` across multiple segments, or deliver a partial read. The caller must frame messages and reassemble fragments. Stream concepts (`ReadStream`, `WriteStream`) model this behaviour.

UDP delivers discrete datagrams. Each `sendto` produces exactly one datagram. Each `recvfrom` delivers exactly one datagram. The kernel does not coalesce, split, or reorder within a single operation. Message boundaries are part of the protocol.

This difference is structural, not incidental. It determines the API shape.

### 3.1 Why `udp_socket` Does Not Satisfy `Stream`

The `Stream` concepts from Paper 6 assume byte-oriented, potentially infinite sequences. `read_some` may return fewer bytes than requested - the caller retries until the full message arrives. `write_some` may accept fewer bytes than offered - the caller retries with the remainder. These partial-result semantics are correct for TCP and wrong for UDP.

A `receive_from` that returns fewer bytes than the datagram has discarded the rest. There is no "retry for the remainder." A `send_to` that accepts fewer bytes than the message has sent a truncated datagram - a protocol violation in every datagram-based protocol.

Forcing UDP through a stream interface would require one of two compromises:

1. **Silently change semantics.** Define `read_some` on a UDP socket to mean "receive one datagram" and suppress the partial-read retry pattern. Generic algorithms that call `read_some` in a loop would break - they would treat each datagram as a fragment of a larger stream.

2. **Buffer and reassemble.** Add an internal buffer that accumulates datagrams and presents them as a byte stream. This destroys message boundaries - the property that makes UDP useful. The receiver can no longer tell where one datagram ends and the next begins.

Neither compromise is acceptable. `udp_socket` has `send_to`/`receive_from` and `send`/`receive`. It does not have `read_some` or `write_some`. It does not satisfy `Stream`. The naming makes the semantic difference visible at the API level.

### 3.2 Buffer Sizing

UDP datagrams have a maximum size determined by the IP layer: 65,535 bytes for IPv4 (minus headers), effectively limited to the path MTU in practice (typically 1,472 bytes for Ethernet with IPv4). If the receive buffer is smaller than the incoming datagram, the excess is discarded silently on most platforms. The application is responsible for providing a sufficiently large buffer.

This is a fundamental difference from TCP, where the kernel buffers incoming bytes and delivers them incrementally. With UDP, the entire datagram must fit in the buffer provided to `receive_from`, or data is lost. The API does not hide this property - it is inherent to the protocol.

---

## 4. Connected vs Unconnected

UDP supports two modes of operation. The default is unconnected: Each `send_to` specifies a destination, each `receive_from` reports a source. The alternative is connected: `connect` associates the socket with a single remote endpoint, after which `send` and `receive` operate without per-call endpoint arguments.

### 4.1 What `connect` Does on a UDP Socket

On a TCP socket, `connect` initiates a three-way handshake and establishes a connection. On a UDP socket, `connect` is a local kernel operation. No packets are sent. The kernel records the remote address and applies two filters:

1. **Outbound filter.** `send` transmits to the recorded address without requiring the caller to specify it.
2. **Inbound filter.** `receive` delivers only datagrams from the recorded address. Datagrams from other sources are silently discarded by the kernel.

The operation is fast, local, and reversible (by connecting to `AF_UNSPEC` on POSIX, or by calling `connect` with a different address).

### 4.2 When Connected Mode Is Appropriate

**DNS stub resolvers.** A resolver sends a query to a specific server and expects a response from that server. Connected mode provides implicit source filtering - a spoofed response from a different address is discarded by the kernel before it reaches the application.

**QUIC connections.** Each QUIC connection is a logical session over UDP. After the initial handshake, all traffic flows between two endpoints. Connected mode matches this pattern.

**Game client sessions.** A game client communicates with a single game server for the duration of a session. Connected mode eliminates per-send address specification and provides implicit source filtering.

### 4.3 When Unconnected Mode Is Appropriate

**Servers.** A UDP server receives datagrams from many clients. It must know the source of each datagram to send responses. `receive_from` provides this. Connected mode, which filters to a single source, would prevent the server from hearing other clients.

**Multicast.** Multicast datagrams arrive from many sources. Connected mode's source filtering is incompatible with the multicast model.

**Protocol multiplexing.** A single socket that handles multiple protocols or peers (common in IoT gateways) needs per-datagram source information.

### 4.4 Design Decision

Both modes are exposed because both are needed. The unconnected API (`send_to`/`receive_from`) is the general case. The connected API (`connect` + `send`/`receive`) is the optimised specialisation for single-peer communication. Neither subsumes the other.

The `connect` method is an `IoAwaitable` for consistency with the rest of the I/O surface, even though the underlying kernel operation is synchronous on all major platforms. This keeps the API uniform and allows future platforms that might perform asynchronous address resolution during connect.

---

## 5. Multicast Design

### 5.1 The Multicast Model

IP multicast allows a single datagram to be delivered to multiple recipients. The sender transmits to a multicast group address (224.0.0.0/4 for IPv4, ff00::/8 for IPv6). Routers and switches replicate the datagram to all hosts that have joined the group. The sender does not know or care how many receivers exist.

### 5.2 API Surface

D0025R0<sup>[1]</sup> proposes two operations:

```cpp
void join_group(ip_address const& multicast_addr);
void leave_group(ip_address const& multicast_addr);
```

This is the minimal surface. Every multicast use case begins with joining a group and ends with leaving it. The socket must be bound before joining - the bind address determines which network interface receives the multicast traffic.

### 5.3 What Is Deferred

Advanced multicast features are deferred to a future paper or to socket options (Section 9):

- **Source-specific multicast (SSM).** `IP_ADD_SOURCE_MEMBERSHIP` / `IPV6_JOIN_SOURCE_GROUP`. SSM restricts reception to datagrams from a specific source within the group. Used in IPTV and financial market data feeds. Important but not universal.
- **Multicast TTL.** `IP_MULTICAST_TTL` / `IPV6_MULTICAST_HOPS`. Controls how far multicast packets propagate through routers. Default is 1 (link-local). Adjustable for site-local or wider distribution.
- **Loopback control.** `IP_MULTICAST_LOOP` / `IPV6_MULTICAST_LOOP`. Controls whether multicast packets sent from a socket are looped back to receivers on the same host. Default varies by platform.
- **Interface selection.** `IP_MULTICAST_IF` / `IPV6_MULTICAST_IF`. Specifies which network interface to use for outgoing multicast traffic. Relevant on multi-homed hosts.

Each deferred feature maps to a socket option. The join/leave surface is sufficient for the initial proposal. Socket options can be added without changing the core API.

---

## 6. Platform Implementation

### 6.1 POSIX (Linux, macOS, BSD)

| Operation        | System call    | Notes                              |
| ---------------- | -------------- | ---------------------------------- |
| `bind`           | `bind(2)`      | Same as TCP                        |
| `send_to`        | `sendto(2)`    | Scatter via `sendmsg(2)`           |
| `receive_from`   | `recvfrom(2)`  | Gather via `recvmsg(2)`            |
| `connect`        | `connect(2)`   | Local operation, no network traffic |
| `send`           | `send(2)`      | Connected mode                     |
| `receive`        | `recv(2)`      | Connected mode                     |
| `join_group`     | `setsockopt`   | `IP_ADD_MEMBERSHIP` / `IPV6_JOIN_GROUP` |
| `leave_group`    | `setsockopt`   | `IP_DROP_MEMBERSHIP` / `IPV6_LEAVE_GROUP` |
| `close`          | `close(2)`     | Implicitly drops all group memberships |

The Corosio implementation on Linux uses `epoll` with `EPOLLIN`/`EPOLLOUT` for readiness notification. On macOS and FreeBSD, `kqueue` with `EVFILT_READ`/`EVFILT_WRITE` serves the same purpose.

### 6.2 Windows (IOCP)

| Operation        | API                | Notes                              |
| ---------------- | ------------------ | ---------------------------------- |
| `bind`           | `bind()`           | Winsock2                           |
| `send_to`        | `WSASendTo()`      | Overlapped I/O for IOCP            |
| `receive_from`   | `WSARecvFrom()`    | Overlapped I/O for IOCP            |
| `connect`        | `WSAConnect()`     | Local operation                    |
| `send`           | `WSASend()`        | Connected mode, overlapped         |
| `receive`        | `WSARecv()`        | Connected mode, overlapped         |
| `join_group`     | `setsockopt`       | `IP_ADD_MEMBERSHIP`                |
| `leave_group`    | `setsockopt`       | `IP_DROP_MEMBERSHIP`               |
| `close`          | `closesocket()`    | Winsock2                           |

Windows requires `WSARecvFrom`/`WSASendTo` for overlapped (IOCP-driven) datagram I/O. The non-overlapped `recvfrom`/`sendto` from BSD sockets do not integrate with I/O completion ports.

### 6.3 io_uring (Linux)

`io_uring` supports `IORING_OP_SENDTO` and `IORING_OP_RECVFROM` (added in Linux 6.0). These operations submit datagram I/O directly to the kernel ring buffer, eliminating the system call overhead of `sendto`/`recvfrom`. The Corosio io_uring backend uses these operations when available. The `epoll` backend provides the fallback for older kernels.

### 6.4 Cross-Platform Consistency

The `udp_socket` API maps directly to platform primitives on all three major platforms. No emulation layer is required. The variation is in the completion notification mechanism (epoll, kqueue, IOCP, io_uring), not in the datagram operations themselves. The same `sendto`/`recvfrom` system call family has been available on every platform since BSD 4.2 (1983).

---

## 7. Convergence

Six ecosystems provide datagram socket APIs. The shapes converge.

| Ecosystem   | Type                            | Send              | Receive              | Bind       | Multicast              |
| ----------- | ------------------------------- | ----------------- | -------------------- | ---------- | ---------------------- |
| BSD (1983)  | `int` (socket fd)               | `sendto(2)`       | `recvfrom(2)`        | `bind(2)`  | `setsockopt`           |
| Go          | `net.UDPConn`                   | `WriteTo`         | `ReadFromUDP`        | `ListenUDP`| `JoinGroup`            |
| Rust (Tokio)| `tokio::net::UdpSocket`         | `send_to`         | `recv_from`          | `bind`     | `join_multicast_v4`    |
| .NET        | `System.Net.Sockets.UdpClient`  | `SendAsync`       | `ReceiveAsync`       | Constructor| `JoinMulticastGroup`   |
| Python      | `asyncio.DatagramProtocol`      | `sendto`          | `datagram_received`  | `bind`     | `setsockopt`           |
| Asio        | `udp::socket`                   | `async_send_to`   | `async_receive_from` | `bind`     | `join_group` (option)  |

### 7.1 Universal Operations

Every ecosystem provides the same four primitives:

1. **Bind** to a local address and port.
2. **Send** a datagram to a destination endpoint.
3. **Receive** a datagram with the sender's address.
4. **Close** the socket.

The naming varies. The semantics do not.

### 7.2 Connected Mode

Every ecosystem supports connected UDP: Go's `net.UDPConn` returned by `DialUDP`, Rust's `UdpSocket::connect`, .NET's `UdpClient.Connect`, Asio's `udp::socket::connect`. The pattern is universal because the kernel feature is universal - it has existed since BSD 4.2.

### 7.3 Multicast

Every ecosystem provides multicast group management. Go and .NET expose dedicated methods (`JoinGroup`, `JoinMulticastGroup`). Rust and Asio expose it through socket options (`join_multicast_v4`, `multicast::join_group`). The proposed `join_group`/`leave_group` interface follows the Go/.NET approach: dedicated methods on the socket type rather than generic socket option setters.

### 7.4 What Our Design Recovers

The proposed `udp_socket` recovers the universal shape - `bind`, `send_to`/`receive_from`, `connect` + `send`/`receive`, `join_group`/`leave_group` - and wraps it in the IoAwaitable protocol. The API is new to C++. The shape is forty years old.

---

## 8. Anticipated Objections

### 8.1 "UDP is unreliable and should not be standardised"

UDP is unreliable by design. Packets may be lost, duplicated, or reordered. The protocol does not guarantee delivery.

This is not a defect. It is the feature. Every protocol built on UDP - DNS, QUIC, RTP, game networking, CoAP - handles reliability at the application layer, where the reliability requirements are domain-specific. DNS retransmits after a timeout. QUIC implements its own loss detection and congestion control. RTP tolerates loss. Game networking supersedes lost state with newer state. CoAP provides confirmable messages for operations that need acknowledgement.

The standard library provides `std::vector` even though it does not sort its elements. It provides `std::atomic` even though misuse causes data races. The standard provides tools. The programmer provides the discipline. UDP is a tool.

The alternative - omitting UDP and forcing every C++ programmer to drop to raw sockets or platform APIs for datagram I/O - is worse than standardising the tool.

### 8.2 "QUIC makes raw UDP obsolete"

QUIC uses UDP as its transport. QUIC does not eliminate the need for `sendto` and `recvfrom` - it requires them. A QUIC implementation is built on UDP sockets. Without standard UDP sockets, a standard QUIC implementation is impossible.

QUIC also does not replace every use of UDP. DNS query/response is simpler than a full QUIC handshake. Game state updates at 60 Hz do not need QUIC's congestion control. Multicast has no QUIC equivalent. IoT devices that cannot afford QUIC's connection state use CoAP over UDP directly.

QUIC is a user of UDP, not a replacement for it.

### 8.3 "Multicast is rarely used"

Multicast is rarely used on the public Internet because most ISPs do not enable multicast routing. On local networks, multicast is pervasive:

- **mDNS/DNS-SD** (Bonjour, Avahi): Every Apple device, every Linux desktop with Avahi, every Chromecast and smart speaker uses multicast for service discovery.
- **SSDP/UPnP**: every consumer router, every media server (Plex, DLNA), every smart TV.
- **PTP (IEEE 1588)**: precision time synchronisation in financial trading, broadcast studios, and industrial automation.
- **VXLAN**: data centre overlay networking.
- **IPTV**: commercial television distribution.

The mDNS multicast group 224.0.0.251 is one of the most active multicast addresses on any local network segment. Omitting multicast from a UDP standard would make the standard incapable of expressing the most common UDP use case on local networks.

### 8.4 "Datagram sockets need scatter/gather"

The proposed API accepts `ConstBufferSequence` and `MutableBufferSequence` - the same scatter/gather vocabulary used by TCP sockets in Paper 11. A single `send_to` call can gather data from multiple non-contiguous buffers into one datagram. A single `receive_from` can scatter one datagram into multiple buffers.

The scatter/gather capability is present in the API through the buffer sequence concepts. The `sendmsg`/`recvmsg` system calls (POSIX) and `WSASendTo`/`WSARecvFrom` (Windows) provide the kernel-level scatter/gather. No additional API surface is needed.

---

## 9. Deferrals

The following features are acknowledged as valuable but deferred from this initial proposal.

### 9.1 QUIC Integration

A QUIC transport layer would sit above `udp_socket` and provide connection management, stream multiplexing, loss detection, congestion control, and encryption. QUIC is a large, complex protocol ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000)<sup>[6]</sup> alone is 151 pages). Standardising QUIC transport is a separate multi-paper effort. The `udp_socket` proposed here provides the foundation it would build on.

### 9.2 Raw Sockets

Raw sockets (`SOCK_RAW`) allow sending and receiving IP packets without transport-layer framing. They are used for ICMP (ping, traceroute), custom protocols, and network diagnostics. Raw sockets require elevated privileges on most platforms and have significantly different security implications. They are deferred to a future paper.

### 9.3 Socket Options Fine-Tuning

The initial proposal exposes `join_group`/`leave_group` as dedicated member functions. Other socket options - `SO_REUSEADDR`, `SO_REUSEPORT`, `SO_BROADCAST`, `IP_MULTICAST_TTL`, `IP_MULTICAST_LOOP`, `IP_MULTICAST_IF`, `IP_PKTINFO`, receive buffer sizes - are deferred to a general socket options mechanism that would apply to both TCP and UDP sockets. The companion TCP paper (Paper 11) faces the same deferral.

### 9.4 Batch Operations (`recvmmsg`/`sendmmsg`)

Linux provides `recvmmsg(2)` and `sendmmsg(2)` for receiving and sending multiple datagrams in a single system call. These are performance-critical for high-throughput UDP servers (DNS servers, game servers, media relays). The batch operations reduce system call overhead by amortising the kernel transition across multiple datagrams.

The initial proposal does not expose batch operations. The single-datagram `send_to`/`receive_from` interface is sufficient for correctness and covers the common case. Batch operations can be added as overloads or separate functions in a future revision without changing the core API. The io_uring backend (Section 6.3) achieves similar amortisation through submission batching at the ring level.

### 9.5 `recvmsg` Ancillary Data

`recvmsg(2)` can deliver ancillary data (control messages) alongside the datagram payload - destination address (`IP_PKTINFO`), timestamp (`SO_TIMESTAMP`), TTL (`IP_RECVTTL`), traffic class. These are valuable for advanced applications (DNS servers that need to know the destination address, PTP requiring hardware timestamps). The initial proposal does not expose ancillary data. Adding it later through an extended receive interface is straightforward.

---

## 10. Why Now

UDP is Paper 13 in a 14-paper series. The timing reflects dependency order, not priority.

Papers 1-7 (Stage One) establish the protocol, task type, buffer concepts, stream concepts, and combinators. Papers 8-10 prove the protocol against kernel interactions (timers, signals, files). Paper 11 (TCP) establishes the socket, endpoint, and address types. Paper 12 (DNS) provides name resolution. UDP builds on the endpoint and address types from Paper 11 and provides the datagram transport that DNS (Paper 12) uses at the wire level.

The dependency chain is: IoAwaitable (Paper 1) -> endpoint/address types (Paper 11) -> UDP (Paper 13).

QUIC standardisation efforts in the IETF are mature. HTTP/3 deployment is widespread. C++ QUIC implementations exist (MsQuic, ngtcp2, quiche). All of them build on UDP sockets. The standard library should provide the transport layer these implementations need.

The Corosio implementation ships UDP on three platforms today. The API has been stable through production use. The convergence evidence spans forty years and six ecosystems. The design is ready.

---

## 11. Closing

UDP is the simplest network socket type. Bind, send, receive, close. No connection state. No handshake. No flow control. No reassembly. The kernel delivers datagrams. The application decides what they mean.

The standard library should provide this tool. Five domains need it. Six ecosystems converge on the same shape. The implementation ships today.

---

\newpage

## Appendix A: Synopsis

```cpp
namespace std::io {

  class udp_socket {
  public:
    // Construction and destruction
    explicit udp_socket(execution_context& ctx);

    udp_socket(udp_socket const&) = delete;
    udp_socket& operator=(
        udp_socket const&) = delete;
    udp_socket(udp_socket&&) noexcept;
    udp_socket& operator=(
        udp_socket&&) noexcept;

    ~udp_socket();

    // Binding and lifetime
    void bind(endpoint const& ep);
    void close();

    // Unconnected datagram I/O
    IoAwaitable auto send_to(
        ConstBufferSequence auto const& buffers,
        endpoint const& dest);
    IoAwaitable auto receive_from(
        MutableBufferSequence auto const& buffers,
        endpoint& sender);

    // Connected UDP
    IoAwaitable auto connect(
        endpoint const& ep);
    IoAwaitable auto send(
        ConstBufferSequence auto const& buffers);
    IoAwaitable auto receive(
        MutableBufferSequence auto const& buffers);

    // Multicast
    void join_group(
        ip_address const& multicast_addr);
    void leave_group(
        ip_address const& multicast_addr);
  };

}
```

---

\newpage

## Appendix B: Corosio Headers

The Corosio implementation of `udp_socket` is available at:

- [`corosio/include/corosio/udp_socket.hpp`](https://github.com/cppalliance/corosio)

The implementation covers Linux (epoll, io_uring), macOS (kqueue), and Windows (IOCP). The test suite exercises unconnected I/O, connected mode, multicast join/leave, cancellation via stop token, and cross-platform endpoint handling.

---

## Acknowledgments

Christopher Kohlhoff designed the Asio `udp::socket` that this proposal recovers for a coroutine-native model. The Asio UDP interface has been stable for over fifteen years and has been deployed in every Asio-based application that requires datagram I/O.

Mohammad Nejati implemented the Corosio UDP socket on three platforms (IOCP, epoll, kqueue) and the io_uring datagram path.

The authors of ngtcp2, MsQuic, and quiche demonstrated that production QUIC implementations require raw UDP sockets as their foundation.

---

## References

[1] D0025R0 - "UDP" (Vinnie Falco, 2026). Companion ask paper.

[2] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[3] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[4] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[5] Sandvine, Global Internet Phenomena Report (2024). UDP share of Internet traffic.

[6] [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000) - "QUIC: A UDP-Based Multiplexed and Secure Transport" (Jana Iyengar, Martin Thomson, 2021).

[7] [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114) - "HTTP/3" (Mike Bishop, 2022).

[8] [RFC 3550](https://www.rfc-editor.org/rfc/rfc3550) - "RTP: A Transport Protocol for Real-Time Applications" (Henning Schulzrinne, Stephen Casner, Ron Frederick, Van Jacobson, 2003).

[9] [RFC 7252](https://www.rfc-editor.org/rfc/rfc7252) - "The Constrained Application Protocol (CoAP)" (Zach Shelby, Klaus Hartke, Carsten Bormann, 2014).

[10] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - UDP socket and datagram services (Christopher Kohlhoff, 2003-2026).

[11] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "The IoAwaitable Protocol" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[12] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).
