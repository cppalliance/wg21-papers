---
title: "Stream Concepts"
document: D0011R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper asks the committee to advance coroutine stream concepts and type-erasing wrappers - `ReadStream`, `WriteStream`, `Stream`, `ReadSource`, `WriteSink`, `BufferSource`, `BufferSink`, and seven `any_*` wrappers - as standard library vocabulary for byte-oriented I/O.

The concepts are the coroutine-native successors to the [Networking TS](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[2]</sup> stream requirements, deployed in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup>, consumed by [Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup>'s `tcp_socket`, `tls_stream`, and `io_stream`, and used by [Boost.Http](https://github.com/cppalliance/http)<sup>[4]</sup> for ABI-stable HTTP processing compiled once against `any_stream`.

The companion paper *Stream Concepts: Design Rationale*<sup>[11]</sup> provides the design rationale, the convergence record across six ecosystems, anticipated objections, and the implementation inventory. Read this paper for the proposal; read the companion when you need the audit trail.

This paper is Paper 6 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[5]</sup>. It depends on Paper 1 (the IoAwaitable protocol, [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[6]</sup>), Paper 4 (buffer-ranges concepts, *I/O Buffer Ranges*<sup>[12]</sup>), and Paper 5 (dynamic-buffer concept, *Dynamic Buffer*<sup>[13]</sup>).

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial Version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author maintains [Boost.Beast](https://github.com/boostorg/beast)<sup>[7]</sup> and develops [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup>, plus three further Boost libraries built on them. Each defines or consumes stream abstractions. The body of work creates a bias toward dedicated stream concepts.

This paper is the proposal-only ask paper for the coroutine stream concepts and type-erasing wrappers. The design rationale lives in the companion *Stream Concepts: Design Rationale*<sup>[11]</sup>. The buffer-ranges vocabulary that stream operations accept lives in *I/O Buffer Ranges*<sup>[12]</sup> and *I/O Buffer Ranges: Design Rationale*<sup>[14]</sup>. The dynamic-buffer concept that `ReadSource` reads into lives in *Dynamic Buffer*<sup>[13]</sup> and *Dynamic Buffer: Design Rationale*<sup>[15]</sup>.

This paper asks for nothing.

---

## 2. What This Paper Asks

The committee is asked to advance the following vocabulary for the standard library:

```cpp
namespace std::io {

  // Caller-owned-buffer concepts
  template<class T> concept ReadStream   = /* Section 3.1 */;
  template<class T> concept WriteStream  = /* Section 3.2 */;
  template<class T> concept Stream       = /* Section 3.3 */;

  // Refinements
  template<class T> concept ReadSource   = /* Section 4.1 */;
  template<class T> concept WriteSink    = /* Section 4.2 */;

  // Callee-owned-buffer concepts
  template<class T> concept BufferSource = /* Section 4.3 */;
  template<class T> concept BufferSink   = /* Section 4.4 */;

  // Type-erasing wrappers
  class any_stream;
  class any_read_stream;
  class any_write_stream;
  class any_read_source;
  class any_write_sink;
  class any_buffer_source;
  class any_buffer_sink;

}
```

Seven concepts. Two families. Seven type-erasing wrappers. Zero per-operation allocation.

---

## 3. The Concepts

### 3.1 `ReadStream`

A type whose `read_some` accepts a caller-owned mutable buffer sequence and returns an IoAwaitable that completes with the number of bytes transferred.

```cpp
template<class T>
concept ReadStream =
    requires(T& t, mutable_buffer buf) {
        { t.read_some(buf) } -> IoAwaitable;
    };
```

`read_some` transfers at least one byte and at most `buffer_size(buf)` bytes into the caller's buffer. Completion with zero bytes indicates end-of-stream. The operation is partial: The caller must loop to read a complete message.

```cpp
std::io::task<std::size_t>
read_header(ReadStream auto& stream, mutable_buffer buf)
{
    std::size_t total = 0;
    while (total < buf.size())
    {
        auto [ec, n] = co_await stream.read_some(buf);
        if (ec || n == 0) break;
        buf += n;
        total += n;
    }
    co_return total;
}
```

### 3.2 `WriteStream`

A type whose `write_some` accepts a caller-owned const buffer sequence and returns an IoAwaitable that completes with the number of bytes transferred.

```cpp
template<class T>
concept WriteStream =
    requires(T& t, const_buffer buf) {
        { t.write_some(buf) } -> IoAwaitable;
    };
```

`write_some` transfers at least one byte and at most `buffer_size(buf)` bytes from the caller's buffer. The operation is partial: The caller must loop to write a complete message.

### 3.3 `Stream`

A type that is both a `ReadStream` and a `WriteStream`.

```cpp
template<class T>
concept Stream = ReadStream<T> && WriteStream<T>;
```

A TCP socket satisfies `Stream`. A TLS stream wrapping a TCP socket satisfies `Stream`. A pipe with separate read and write ends does not - each end satisfies one half.

---

## 4. Refinements

Two refinements of the caller-owned-buffer family add complete-transfer semantics. Two callee-owned-buffer concepts provide zero-copy paths.

### 4.1 `ReadSource`

A `ReadStream` that also provides complete reads into a `DynamicBuffer`.

```cpp
template<class T>
concept ReadSource =
    ReadStream<T> &&
    requires(T& t, flat_dynamic_buffer& db, std::size_t limit) {
        { t.read(db, limit) } -> IoAwaitable;
    };
```

`read(db, limit)` loops internally until the dynamic buffer contains `limit` bytes, the stream reports end-of-stream, or an error occurs. The caller does not write the loop. The implementation writes it once.

### 4.2 `WriteSink`

A `WriteStream` that also provides complete writes and end-of-stream signalling.

```cpp
template<class T>
concept WriteSink =
    WriteStream<T> &&
    requires(T& t, const_buffer buf) {
        { t.write(buf) }    -> IoAwaitable;
        { t.write_eof() }   -> IoAwaitable;
    };
```

`write(buf)` loops internally until every byte is transferred or an error occurs. `write_eof()` signals that no further data will be sent - the HTTP half-close, the TLS `close_notify`, the TCP `shutdown(SHUT_WR)`.

### 4.3 `BufferSource`

A type that owns the read buffer. The caller pulls data and then consumes it.

```cpp
template<class T>
concept BufferSource =
    requires(T& t, std::size_t n) {
        { t.pull() }    -> IoAwaitable;
        { t.data() }    -> ConstBufferSequence;
        { t.consume(n) };
    };
```

`pull()` fills the internal buffer from the underlying transport. `data()` returns a read-only view of the buffered bytes. `consume(n)` discards `n` bytes from the front. The caller never allocates a read buffer. The `BufferSource` owns it.

Zero-copy decompression, base64 decoding, and TLS record processing are natural `BufferSource` implementations: The internal buffer holds the decoded output; the caller inspects and consumes without copying.

### 4.4 `BufferSink`

A type that owns the write buffer. The caller prepares space and then commits data.

```cpp
template<class T>
concept BufferSink =
    requires(T& t, std::size_t n) {
        { t.prepare(n) } -> MutableBufferSequence;
        { t.commit(n) };
        { t.flush() }    -> IoAwaitable;
    };
```

`prepare(n)` returns at least `n` bytes of writable space from the internal buffer. `commit(n)` marks `n` written bytes as ready for transmission. `flush()` pushes committed bytes to the underlying transport.

---

## 5. Type-Erasing Wrappers

Seven wrappers type-erase any type satisfying the corresponding concept behind a pointer-and-vtable pair. One pointer. One vtable. Zero per-operation allocation.

```cpp
class any_stream
{
    io_stream* impl_;   // points to derived concrete type
public:
    any_stream() = default;
    any_stream(any_stream&&) noexcept;
    any_stream& operator=(any_stream&&) noexcept;
    ~any_stream();

    template<class S>
        requires Stream<S>
    explicit any_stream(S& s);

    /* IoAwaitable */ read_some(mutable_buffer buf);
    /* IoAwaitable */ write_some(const_buffer buf);
};
```

The coroutine frame subsidizes the type erasure. When a coroutine calls `co_await stream.read_some(buf)`, the operation state lives in the caller's frame. The frame is already allocated. The virtual dispatch adds one indirection per operation. There is no per-operation heap allocation.

`any_read_stream`, `any_write_stream`, `any_read_source`, `any_write_sink`, `any_buffer_source`, and `any_buffer_sink` follow the same pattern, each wrapping the corresponding concept.

### 5.1 Usage

```cpp
std::io::task<>
serve(any_stream stream)
{
    flat_dynamic_buffer buf(storage, sizeof(storage));
    auto [ec, n] = co_await stream.read_some(buf.prepare(4096));
    buf.commit(n);
    // parse, respond...
    co_return {};
}
```

`serve` compiles once. It links once. It works with `tcp_socket`, `tls_stream`, `unix_socket`, a test mock, or any future transport that satisfies `Stream`. The caller passes the concrete type through the wrapper at the boundary. The business logic never names the concrete type.

[Boost.Http](https://github.com/cppalliance/http)<sup>[4]</sup> uses `any_stream` throughout. The HTTP library is compiled once and shipped as a binary. New transports plug in without recompilation.

---

## 6. The Three-Layer Architecture

Every I/O object in the series exposes three API layers. The stream concepts are the vocabulary that the abstract layer speaks.

```
         io_stream                    abstract (Layer 3)
             |
        tcp_socket                    concrete (Layer 2)
             |
native_tcp_socket<Backend>            native   (Layer 1)
```

| Property             | Abstract                   | Concrete                   | Native                                  |
| -------------------- | -------------------------- | -------------------------- | --------------------------------------- |
| Compilation speed    | Fastest                    | Fast                       | Slowest (platform headers + templates)  |
| Separate compilation | Yes                        | Yes                        | No                                      |
| Call overhead        | Virtual dispatch           | Virtual dispatch           | None (direct / inlined)                 |
| API surface          | `read_some` / `write_some` | Full protocol-specific API | Same as concrete, fully inlined         |
| Use case             | Libraries, generic algos   | Application code           | Hot paths, benchmarks                   |

`any_stream` wraps the abstract layer. A library that accepts `any_stream&` compiles against `io_stream`'s vtable. The concrete type behind the wrapper is invisible. New backends - io_uring-native, IOCP-optimized, embedded - plug in without recompilation.

**The user chooses the layer. The stream concepts define what every layer must provide.**

---

## 7. Suggested Straw Poll

> LEWG agrees that the stream concepts `ReadStream`, `WriteStream`, `Stream`, `ReadSource`, `WriteSink`, `BufferSource`, `BufferSink`, and the type-erasing wrappers `any_stream`, `any_read_stream`, `any_write_stream`, `any_read_source`, `any_write_sink`, `any_buffer_source`, `any_buffer_sink` documented in this paper and its companion *Stream Concepts: Design Rationale* should be advanced as standard library vocabulary for byte-oriented I/O.

---

## Acknowledgments

Christopher Kohlhoff designed the Asio stream requirements - `AsyncReadStream`, `AsyncWriteStream`, and the composed-operation model - that this paper recovers as C++20 concepts with coroutine-native semantics. Twenty years of production deployment in [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[8]</sup> is the foundation this work builds on.

The Networking TS authors codified the stream operational semantics in [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[2]</sup>. The shapes in this paper are the coroutine-native successors to the shapes they specified.

---

## References

[1] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[2] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).

[3] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[4] [Boost.Http](https://github.com/cppalliance/http) - HTTP/1.1 server built on Capy's stream concepts (Vinnie Falco, 2025-2026).

[5] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[6] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[7] [Boost.Beast](https://github.com/boostorg/beast) - HTTP and WebSocket built on Boost.Asio (Vinnie Falco, 2017-2026).

[8] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - Stream requirements and composed operations (Christopher Kohlhoff, 2003-2026).

[9] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[10] [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[11] *Stream Concepts: Design Rationale* (Vinnie Falco, 2026). Companion design paper. D0012R0.

[12] *I/O Buffer Ranges* (Vinnie Falco, 2026). Companion ask paper for the byte-region vocabulary. D0007R0.

[13] *Dynamic Buffer* (Vinnie Falco, 2026). Companion ask paper for the growable buffer concept. D0009R0.

[14] *I/O Buffer Ranges: Design Rationale* (Vinnie Falco, 2026). Companion design paper for the byte-region vocabulary. D0008R0.

[15] *Dynamic Buffer: Design Rationale* (Vinnie Falco, 2026). Companion design paper for the growable buffer concept. D0010R0.
