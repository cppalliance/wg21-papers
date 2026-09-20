---
title: "Stream Concepts: Design Rationale"
document: D0012R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Every C++ project that does I/O invents its own stream abstraction.

Six other ecosystems do not. Each provides a vocabulary for the same pair of operations: Read bytes from a transport, write bytes to a transport. BSD gave them to us in 1983. POSIX standardised `readv`/`writev`. Asio shipped `async_read_some`/`async_write_some`. Go has `io.Reader`/`io.Writer`. Rust has `AsyncRead`/`AsyncWrite`. .NET has `Stream.ReadAsync`/`Stream.WriteAsync`. The C++ standard has none of them. This paper documents the stream concepts that ship in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> today - the coroutine-native successors to the [Networking TS](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[2]</sup> stream requirements - and the type-erasing wrappers that give C++ ABI-stable I/O for the first time.

This paper is the design-rationale companion to *Stream Concepts*<sup>[21]</sup>, which contains the proposal-only specification and the straw poll. It is part of the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup>, in which Stream Concepts is Paper 6. It depends on Paper 1 (IoAwaitable protocol, [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[4]</sup>), Paper 4 (buffer-ranges concepts, *I/O Buffer Ranges: Design Rationale*<sup>[22]</sup>), and Paper 5 (dynamic-buffer concept, *Dynamic Buffer: Design Rationale*<sup>[23]</sup>).

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial Version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author maintains [Boost.Beast](https://github.com/boostorg/beast)<sup>[5]</sup>, a published HTTP and WebSocket library built on Asio's stream model, and develops [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[6]</sup>, plus three further Boost libraries built on them: Boost.Http, Boost.Beast2, and Boost.Burl. Each defines or consumes stream abstractions. The body of work creates a bias toward dedicated stream concepts.

This paper documents the stream concepts and type-erasing wrappers that ship in Capy. The proposal-only ask paper is *Stream Concepts*<sup>[21]</sup>. The buffer-ranges vocabulary that stream operations accept is documented in *I/O Buffer Ranges: Design Rationale*<sup>[22]</sup>. The dynamic-buffer concept that `ReadSource` reads into is documented in *Dynamic Buffer: Design Rationale*<sup>[23]</sup>.

The [Networking TS](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[2]</sup> defined `AsyncReadStream` and `AsyncWriteStream` as named requirements. The shapes in this paper are coroutine-native successors to the same shapes, recovered as C++20 concepts on a parallel track to the Network Endeavor.

The companion papers are *Stream Concepts*<sup>[21]</sup> (proposal-only ask paper for the concepts in this paper), *I/O Buffer Ranges*<sup>[24]</sup> and *I/O Buffer Ranges: Design Rationale*<sup>[22]</sup> (buffer-ranges pair), *Dynamic Buffer*<sup>[25]</sup> and *Dynamic Buffer: Design Rationale*<sup>[23]</sup> (dynamic-buffer pair), and [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup> (the umbrella paper that places this work in series).

Every concept and wrapper documented in this paper ships in Capy. Every I/O type in Corosio satisfies the stream concepts. Appendix B is the inventory.

This paper asks for nothing.

---

## 2. Why Streams

The question a stream concept answers is: Given a transport, how does generic code read bytes from it and write bytes to it?

The question is forty years old. BSD answered it in 1983 with `read()` and `write()`. The shape has not changed since. What has changed is the delivery mechanism - blocking calls became callbacks, callbacks became futures, futures became coroutine awaitables. The two operations at the core are the same.

### 2.1 What C++ Does Not Have

The standard library provides `std::basic_istream` and `std::basic_ostream`. They operate on formatted characters, not on raw bytes. They carry locale state. They do not accept buffer sequences. They do not compose with platform scatter/gather syscalls. They are synchronous. They are not the operations that I/O libraries need.

The standard library provides `std::filesystem::read` (since C++17) for file contents. It returns a string. It does not accept a caller-owned buffer. It is synchronous. It does not compose with sockets, pipes, TLS, or decompression layers.

The standard library does not provide a concept for "a type that reads bytes asynchronously into a caller-owned buffer." Every library that does I/O invents one.

### 2.2 What Every I/O Library Invents

Every C++ networking library defines the same pair of operations:

```cpp
// Asio (2003)
template<class MBS, class Token>
auto async_read_some(MBS const& buffers, Token&& token);

// Capy (2024)
auto read_some(MutableBufferSequence auto buffers)
    -> IoAwaitable auto;

// Beast (2017) - delegates to the underlying stream
template<class MBS, class Token>
auto async_read_some(MBS const& buffers, Token&& token);
```

The names vary. The shape does not. Read bytes into a buffer. Write bytes from a buffer. Return a byte count. Signal errors. Signal end-of-stream with zero bytes.

The stream concepts in this paper name that shape so that generic algorithms can be written against it once.

**The standard library is the dictionary that does not have the word.**

---

## 3. Caller-Owned vs Callee-Owned

The stream concepts divide into two families. The division is not an accident. It reflects two fundamentally different ownership models for the bytes in transit.

### 3.1 Caller-Owned Buffers

`ReadStream`, `WriteStream`, `Stream`, `ReadSource`, `WriteSink`. The caller allocates the buffer and passes it to the stream. The stream fills (or drains) the buffer and returns a byte count.

```cpp
char storage[4096];
mutable_buffer buf(storage, sizeof(storage));
auto [ec, n] = co_await stream.read_some(buf);
```

The caller controls the buffer's lifetime, location, and size. The stream does not allocate. This is the simple path. It is sufficient for the majority of I/O operations.

### 3.2 Callee-Owned Buffers

`BufferSource`, `BufferSink`. The stream owns the buffer. The caller asks for data (`pull`) or space (`prepare`) and the stream provides a view into its internal storage.

```cpp
co_await source.pull();
auto data = source.data();   // view into internal buffer
process(data);
source.consume(data.size()); // release processed bytes
```

The stream controls the buffer's lifetime, location, and size. The caller operates on a view. No copy occurs between the stream's buffer and the caller's buffer.

### 3.3 When Each Family Applies

| Scenario                        | Family               | Reason                                                    |
| ------------------------------- | -------------------- | --------------------------------------------------------- |
| Simple socket read/write        | Caller-owned         | Caller has a stack buffer; no reason to add another       |
| HTTP body streaming             | Caller-owned         | Application provides the destination buffer               |
| TLS record decryption           | Callee-owned         | TLS layer must buffer ciphertext; caller reads plaintext  |
| Decompression (zlib, zstd)      | Callee-owned         | Decompressor owns the decode buffer                       |
| Base64 decoding                 | Callee-owned         | Decoder owns the output buffer                            |
| Protocol framing (WebSocket)    | Callee-owned         | Framer buffers partial frames; caller reads complete ones |

The two families are not redundant. A pipeline of `tcp_socket` (caller-owned) to `tls_stream` (callee-owned internally, caller-owned externally) to `decompression_stream` (callee-owned) to HTTP parser is the shape of a real server. Each layer uses the ownership model that fits.

**Two families. Caller-owned for the simple path. Callee-owned for zero-copy.**

---

## 4. Type Erasure

Type erasure is the feature that gives C++ ABI-stable I/O. Without it, every library that accepts a stream is a template - separately compiled against each concrete transport, recompiled when a new transport appears, unable to ship as a stable binary. With it, a library accepts `any_stream&` and compiles once.

### 4.1 The Shape

```cpp
class io_stream
{
public:
    virtual ~io_stream() = default;

    virtual /* IoAwaitable */
    read_some(mutable_buffer buf) = 0;

    virtual /* IoAwaitable */
    write_some(const_buffer buf) = 0;
};

class any_stream
{
    io_stream* impl_;
public:
    template<Stream S>
    explicit any_stream(S& s);

    /* IoAwaitable */ read_some(mutable_buffer buf)
    { return impl_->read_some(buf); }

    /* IoAwaitable */ write_some(const_buffer buf)
    { return impl_->write_some(buf); }
};
```

One pointer to the abstract base. Two virtual calls per read/write. The concrete type is invisible behind the vtable. The ABI is the vtable layout. It does not change when a new transport is added.

### 4.2 Zero Per-Operation Allocation

The critical claim is zero per-operation allocation. Here is why it holds.

When a coroutine calls `co_await stream.read_some(buf)`, the compiler generates a coroutine frame that holds:

- The local variables of the calling coroutine (including `buf`).
- The awaitable returned by `read_some`.
- The suspension point state.

The frame is allocated once, at coroutine creation. Each `co_await` reuses the frame. The virtual dispatch in `any_stream` returns an awaitable whose state lives in the coroutine frame of the caller. No heap allocation occurs per read or per write.

Contrast this with callback-based type erasure. Each `async_read_some` creates a completion handler. The handler must be type-erased and heap-allocated (or placed in a small-buffer-optimized storage) because the callback's type depends on the caller's continuation. The per-operation allocation is structural.

Coroutine-native type erasure eliminates it. The coroutine frame - which already exists, which the caller already paid for - subsidizes the type erasure. The frame allocation the program cannot avoid pays for the type erasure it wants.

**The frame is the allocation. The type erasure is free.**

### 4.3 Buffer Sequences Across the Virtual Boundary

A virtual function cannot be a template. `read_some` must accept a concrete type, not a concept. The buffer-ranges vocabulary solves this: The virtual function accepts `mutable_buffer` (a single buffer) or `std::span<mutable_buffer>` (a materialized sequence). The caller-side template captures the user's arbitrary `MutableBufferSequence`, materializes it into a span, and passes the span across the virtual boundary.

Capy's `buffer_param<BS>` adapter (documented in *I/O Buffer Ranges: Design Rationale*<sup>[22]</sup> Section 5.4) handles the materialization. It slides a fixed-capacity window of buffer descriptors over the user's sequence, passing each window as a span. No heap allocation. The windowing is transparent to both sides of the virtual boundary.

---

## 5. The Three-Layer Architecture

Every I/O object exposes three API layers. The stream concepts define what the abstract layer provides. The concrete and native layers add protocol-specific operations.

```
         io_stream                    abstract (Layer 3)
             |
        tcp_socket                    concrete (Layer 2)
             |
native_tcp_socket<Backend>            native   (Layer 1)
```

### 5.1 The Inheritance Chain

`io_stream` defines `read_some` and `write_some` as pure virtuals. `tcp_socket` inherits from `io_stream` and adds `connect`, `bind`, `listen`, `local_endpoint`, `remote_endpoint`, `set_option`. `native_tcp_socket<Backend>` inherits from `tcp_socket` and shadows the virtual functions with non-virtual, fully inlined implementations.

The shadowing is the native layer's zero-overhead mechanism. When the user holds a `native_tcp_socket<epoll_backend>&`, the compiler sees the non-virtual `read_some` and inlines the platform syscall. When the user holds an `io_stream&`, the compiler dispatches through the vtable. The same object supports both paths.

### 5.2 `any_stream` as the Abstract Gateway

`any_stream` wraps any `io_stream*`. A library that declares `task<> process(any_stream& s)` compiles against the abstract layer. It does not include platform headers. It does not depend on the backend. It ships as a binary.

```cpp
// http_server.cpp - compiled once, shipped as .so/.dll
std::io::task<>
handle_request(any_stream& stream)
{
    flat_dynamic_buffer buf(storage, sizeof(storage));
    auto [ec, req] = co_await http::read_request(stream, buf);
    if (ec) co_return {};
    auto res = route(req);
    co_await http::write_response(stream, res);
}

// main.cpp - includes platform headers
auto sock = co_await acceptor.accept();
any_stream stream(sock);
co_await handle_request(stream);
```

`handle_request` does not know what transport it is talking to. It does not care. `tcp_socket`, `tls_stream`, `unix_socket`, `test_mock` - any `Stream` works.

**One compilation. One binary. Any transport.**

---

## 6. Synchronous Streams

A stream concept that requires suspension would exclude synchronous implementations. The design avoids this through the `await_ready()` mechanism that C++20 coroutines already provide.

When a coroutine evaluates `co_await expr`, it calls `await_ready()` on the awaitable. If `await_ready()` returns `true`, no suspension occurs. The coroutine continues synchronously. The awaitable delivers its result immediately.

A memory buffer, a test mock, a zlib decompressor, a base64 decoder - each can implement `read_some` by returning an awaitable whose `await_ready()` returns `true`. The bytes are already available. No I/O occurs. No suspension occurs. The operation completes in the caller's execution context.

```cpp
class memory_read_stream
{
    const_buffer remaining_;
public:
    memory_read_stream(const_buffer data)
        : remaining_(data) {}

    auto read_some(mutable_buffer buf)
    {
        std::size_t n = buffer_copy(buf, remaining_);
        remaining_ += n;
        return immediate_awaitable{n};  // await_ready() == true
    }
};
```

`memory_read_stream` satisfies `ReadStream`. A generic algorithm that reads from any `ReadStream` works with it. No suspension, no thread switch, no system call. The algorithm does not know the difference.

A pipeline of `tcp_socket` to `tls_stream` to `decompression_stream` to HTTP parser works regardless of which layers suspend. The TCP socket suspends on the kernel. The decompression stream returns immediately. The algorithm calls `co_await` uniformly. The awaitable decides.

**Synchronous streams are not a separate abstraction. They are streams whose awaitables are always ready.**

---

## 7. Convergence

Six I/O ecosystems, designed independently, all arrived at the same pair of operations.

| Ecosystem         | Read                                            | Write                                           | Type erasure                    |
| ----------------- | ----------------------------------------------- | ----------------------------------------------- | ------------------------------- |
| BSD (1983)        | `read(fd, buf, len)`<sup>[7]</sup>              | `write(fd, buf, len)`<sup>[7]</sup>             | File descriptor                 |
| POSIX             | `readv(fd, iov, iovcnt)`<sup>[8]</sup>          | `writev(fd, iov, iovcnt)`<sup>[8]</sup>         | File descriptor                 |
| Asio (2003)       | `async_read_some(bufs, token)`<sup>[9]</sup>    | `async_write_some(bufs, token)`<sup>[9]</sup>   | Template (no erasure)           |
| Go (2012)         | `io.Reader.Read(p []byte)`<sup>[10]</sup>       | `io.Writer.Write(p []byte)`<sup>[10]</sup>      | Interface                       |
| Rust (2019)       | `AsyncRead::poll_read`<sup>[11]</sup>           | `AsyncWrite::poll_write`<sup>[11]</sup>         | Trait object (`dyn`)            |
| .NET (2012)       | `Stream.ReadAsync(buf)`<sup>[12]</sup>          | `Stream.WriteAsync(buf)`<sup>[12]</sup>         | Virtual dispatch                |
| Capy (2024)       | `ReadStream::read_some(bufs)`<sup>[1]</sup>     | `WriteStream::write_some(bufs)`<sup>[1]</sup>   | `any_stream` (vtable)           |
| C++ standard      | (none)                                          | (none)                                          | (none)                          |

Every row except the last provides both the pair of operations and a type-erasure mechanism. The C++ standard provides neither.

Asio provides the operations but not the type erasure - every consumer is a template. Capy provides both. The stream concepts in this paper name the operations as concepts. The `any_*` wrappers provide the type erasure. Together they close both gaps.

**Six ecosystems. Same operations. Same type erasure. The C++ row is empty.**

---

## 8. Anticipated Objections

### 8.1 "But `std::execution` Handles Async I/O"

[P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[13]</sup> is a sender-and-receiver framework for composing asynchronous operations. It does not define byte-oriented stream concepts. It does not define `read_some` or `write_some`. It does not provide type-erasing wrappers for streams.

A sender-based I/O library needs the same stream vocabulary. A `sender_read_some` that returns a sender instead of an awaitable still needs to name the operation "read bytes into a buffer and return a count." The concepts in this paper name that operation. They are agnostic to the async model behind the awaitable. A sender-based stream could satisfy `ReadStream` by returning a sender-backed awaitable.

The stream concepts impose no async-model dependency. They enrich `std::execution`-based I/O; they do not compete with it.

### 8.2 "But Virtual Dispatch Adds Overhead"

It does. One indirect call per `read_some` or `write_some`. The question is whether the overhead matters relative to the I/O operation itself.

A TCP read involves a context switch to the kernel, a trip through the network stack, a memory copy from kernel buffer to user buffer, and a return to user space. The virtual-dispatch overhead - one indirect branch, one instruction-cache miss in the worst case - is noise against that background. The overhead is measurable in microbenchmarks and unmeasurable in production I/O workloads.

For the user who needs zero overhead, the native layer exists. `native_tcp_socket<Backend>` shadows the virtual functions with inlined implementations. The three-layer architecture exists precisely so that zero-overhead and ABI-stability are both available, and neither forces a choice on the other.

### 8.3 "But Two Families of Concepts Is Too Complex"

Two families exist because two ownership models exist. The caller-owned family (`ReadStream`, `WriteStream`, `Stream`) covers the common case: The application has a buffer and wants bytes in it. The callee-owned family (`BufferSource`, `BufferSink`) covers the zero-copy case: The stream owns the buffer because it must (TLS decryption, decompression, protocol framing).

A single family would either force every stream to own a buffer (wasting memory when the caller already has one) or force every caller to provide a buffer (forcing a copy when the stream already has the data). Two families is the minimum that avoids both wastes.

The user who does not need zero-copy uses `ReadStream` and `WriteStream`. The user who does need it uses `BufferSource` and `BufferSink`. Neither user encounters the other family unless they choose to.

### 8.4 "But the Networking TS Already Defined Streams"

It did. The committee did not advance the Networking TS. The stream requirements never reached the IS. The shapes are the same; the delivery mechanism is different. The Networking TS streams used completion tokens (callbacks, futures, `use_awaitable`). These streams use coroutine awaitables directly. The Networking TS streams were not type-erasable without per-operation allocation. These streams are - because the coroutine frame subsidizes the erasure.

The concepts in this paper are the coroutine-native successors to the Networking TS stream requirements. The operational semantics are unchanged. The implementation model is new.

---

## 9. Deferrals

Five deferrals. Each is named so the scope is unambiguous.

### 9.1 Datagram Concepts

`ReadStream` and `WriteStream` model byte streams - ordered, reliable, connection-oriented. Datagrams (UDP, Unix datagram sockets) are unordered, unreliable, message-oriented. A `DatagramSource` / `DatagramSink` concept pair is a natural extension. This paper does not include it. Paper 13 (UDP) may define it.

### 9.2 Seekable Streams

File I/O requires positioning: `seek`, `tell`, `read_at`, `write_at`. A `SeekableStream` refinement that adds positioning operations is a natural extension. This paper does not include it. Paper 10 (Files) may define it.

### 9.3 Allocator-Aware Type-Erasing Wrappers

The `any_*` wrappers in this paper do not accept an allocator parameter. They wrap a reference to an existing stream; they do not own the stream's storage. An owning `any_stream` that allocates the wrapped object on a user-provided allocator is a possible extension. This paper does not include it.

### 9.4 Cancellation Semantics

The IoAwaitable protocol ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[4]</sup>) propagates `std::stop_token` through the coroutine environment. Each stream operation observes the stop token and may complete early with an operation-cancelled error. This paper documents the stream concepts. The cancellation mechanism is defined in the IoAwaitable protocol paper and inherited by every stream operation.

### 9.5 Concrete Standard Implementations

This paper proposes the concepts and the type-erasing wrappers. It does not propose `std::io::tcp_socket`, `std::io::tls_stream`, or any concrete stream type. Those are the subject of Stage Two papers (Papers 8-14).

---

## 10. Why Now

The committee has had stream requirements in front of it before.

| Year | Paper                                                                                                  | Outcome                                                     |
| ---- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| 2005 | [N1925](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf)<sup>[14]</sup>             | First networking proposal for TR2                           |
| 2018 | [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[2]</sup>              | Networking TS draft with `AsyncReadStream` / `AsyncWriteStream` |
| 2024 | [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[13]</sup>     | `std::execution` adopted; no stream concepts                |
| 2026 | [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup>         | Network Endeavor frames Stream Concepts as Paper 6          |

The stream vocabulary has been deployed for over twenty years in [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[9]</sup>. It is in the Networking TS<sup>[2]</sup>. It is in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> today, with coroutine-native semantics and type-erasing wrappers that deliver ABI-stable I/O.

Paper 6 completes the bridge to existing I/O ecosystems. After Papers 1-6, an `asio::ip::tcp::socket` becomes an `any_stream` through one adapter in one `.cpp` file. Business logic compiles against the standard. The Asio socket is behind the wrapper. The bulk of a networking application's code compiles against `std::io`.

**The standard library is the place that does not have it.**

---

## 11. Closing

```cpp
std::io::task<>
echo(any_stream stream)
{
    char storage[4096];
    for (;;)
    {
        mutable_buffer buf(storage, sizeof(storage));
        auto [ec, n] = co_await stream.read_some(buf);
        if (ec || n == 0) break;
        auto [wec] = co_await stream.write_some(
            const_buffer(storage, n));
        if (wec) break;
    }
}
```

We built this. It works. We are reporting what we found. Proposed wording for the stream concepts lives in *Stream Concepts*<sup>[21]</sup>.

---

## Appendix A. `<std::io>` Synopsis (Informative)

Stream-concepts-only synopsis. Buffer types and dynamic-buffer concepts live in companion papers.

```cpp
namespace std::io {

  // Caller-owned-buffer concepts
  template<class T>
  concept ReadStream =
      requires(T& t, mutable_buffer buf) {
          { t.read_some(buf) } -> IoAwaitable;
      };

  template<class T>
  concept WriteStream =
      requires(T& t, const_buffer buf) {
          { t.write_some(buf) } -> IoAwaitable;
      };

  template<class T>
  concept Stream = ReadStream<T> && WriteStream<T>;

  // Refinements
  template<class T>
  concept ReadSource =
      ReadStream<T> &&
      requires(T& t, /* DynamicBuffer */ auto& db,
               std::size_t limit) {
          { t.read(db, limit) } -> IoAwaitable;
      };

  template<class T>
  concept WriteSink =
      WriteStream<T> &&
      requires(T& t, const_buffer buf) {
          { t.write(buf) }  -> IoAwaitable;
          { t.write_eof() } -> IoAwaitable;
      };

  // Callee-owned-buffer concepts
  template<class T>
  concept BufferSource =
      requires(T& t, std::size_t n) {
          { t.pull() }    -> IoAwaitable;
          { t.data() }    -> ConstBufferSequence;
          { t.consume(n) };
      };

  template<class T>
  concept BufferSink =
      requires(T& t, std::size_t n) {
          { t.prepare(n) } -> MutableBufferSequence;
          { t.commit(n) };
          { t.flush() }    -> IoAwaitable;
      };

  // Type-erasing wrappers
  class any_stream;
  class any_read_stream;
  class any_write_stream;
  class any_read_source;
  class any_write_sink;
  class any_buffer_source;
  class any_buffer_sink;

  // Abstract base classes (used by any_* wrappers)
  class io_stream;
  class io_read_stream;
  class io_write_stream;

}
```

---

## Appendix B. Capy Header Inventory

The stream concepts and type-erasing wrappers ship in the following [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> headers. Buffer-ranges and dynamic-buffer headers are listed in the companion papers.

| Header                                            | Provides                                                        |
| ------------------------------------------------- | --------------------------------------------------------------- |
| `boost/capy/concept/read_stream.hpp`              | `ReadStream` concept                                            |
| `boost/capy/concept/write_stream.hpp`             | `WriteStream` concept                                           |
| `boost/capy/concept/stream.hpp`                   | `Stream` concept                                                |
| `boost/capy/concept/read_source.hpp`              | `ReadSource` concept                                            |
| `boost/capy/concept/write_sink.hpp`               | `WriteSink` concept                                             |
| `boost/capy/concept/buffer_source.hpp`            | `BufferSource` concept                                          |
| `boost/capy/concept/buffer_sink.hpp`              | `BufferSink` concept                                            |
| `boost/capy/io/io_stream.hpp`                     | `io_stream` abstract base, `any_stream`                         |
| `boost/capy/io/io_read_stream.hpp`                | `io_read_stream` abstract base, `any_read_stream`               |
| `boost/capy/io/io_write_stream.hpp`               | `io_write_stream` abstract base, `any_write_stream`             |
| `boost/capy/io/any_read_source.hpp`               | `any_read_source`                                               |
| `boost/capy/io/any_write_sink.hpp`                | `any_write_sink`                                                |
| `boost/capy/io/any_buffer_source.hpp`             | `any_buffer_source`                                             |
| `boost/capy/io/any_buffer_sink.hpp`               | `any_buffer_sink`                                               |

---

## Acknowledgments

Christopher Kohlhoff designed the Asio stream requirements - `AsyncReadStream`, `AsyncWriteStream`, and the composed-operation model - that this paper recovers as C++20 concepts with coroutine-native semantics. Twenty years of production deployment in [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[9]</sup> is the foundation this work builds on.

The Networking TS authors codified the stream operational semantics in [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[2]</sup>. The shapes in this paper are the coroutine-native successors to the shapes they specified.

The Go standard library's `io.Reader` and `io.Writer` interfaces<sup>[10]</sup> demonstrated that two methods and an interface are sufficient to build an entire I/O ecosystem. The Rust async ecosystem's `AsyncRead` and `AsyncWrite` traits<sup>[11]</sup> demonstrated that the same pair of operations works in a zero-overhead, ownership-aware language. The .NET runtime's `Stream` class<sup>[12]</sup> demonstrated that virtual dispatch and async/await compose without per-operation allocation. This paper applies the same lessons to C++ coroutines.

Peter Dimov's review of the Capy stream code surfaced the design questions about buffer materialization across virtual boundaries that informed Section 4.3.

---

## References

[1] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[2] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).

[3] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[4] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[5] [Boost.Beast](https://github.com/boostorg/beast) - HTTP and WebSocket built on Boost.Asio (Vinnie Falco, 2017-2026).

[6] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[7] [The Single UNIX Specification, Version 4](https://pubs.opengroup.org/onlinepubs/9699919799/) - `read`, `write` (The Open Group, 2018).

[8] [POSIX `<sys/uio.h>`](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/sys_uio.h.html) - `readv`, `writev` (The Open Group, 2018).

[9] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - Stream requirements and composed operations (Christopher Kohlhoff, 2003-2026).

[10] [Go standard library: `io` package](https://pkg.go.dev/io) - `Reader`, `Writer` interfaces (The Go Authors, 2012-2026).

[11] [Rust `tokio::io`](https://docs.rs/tokio/latest/tokio/io/index.html) - `AsyncRead`, `AsyncWrite` traits (Tokio contributors, 2019-2026).

[12] [.NET API: System.IO.Stream](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream) - `ReadAsync`, `WriteAsync` virtual methods (Microsoft, 2012-2026).

[13] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[14] [N1925](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf) - "Networking proposal for TR2 (rev. 1)" (Gerhard Wesp, 2005).

[15] [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[16] [Boost.Http](https://github.com/cppalliance/http) - HTTP/1.1 server built on Capy's stream concepts (Vinnie Falco, 2025-2026).

[17] [P4088R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r0.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[18] [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf) - "Senders and Coroutines" (Vinnie Falco, Mungo Gill, 2026).

[19] [P4125R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4125r0.pdf) - "Field Report: Coroutine-Native I/O at a Derivatives Exchange" (Vinnie Falco, 2026).

[20] [C++ Working Draft](https://eel.is/c++draft/) - `<coroutine>`.

[21] *Stream Concepts* (Vinnie Falco, 2026). Companion ask paper. D0011R0.

[22] *I/O Buffer Ranges: Design Rationale* (Vinnie Falco, 2026). Companion design paper for the byte-region descriptors and sequence concepts. D0008R0.

[23] *Dynamic Buffer: Design Rationale* (Vinnie Falco, 2026). Companion design paper for the growable buffer concept. D0010R0.

[24] *I/O Buffer Ranges* (Vinnie Falco, 2026). Companion ask paper for the byte-region vocabulary. D0007R0.

[25] *Dynamic Buffer* (Vinnie Falco, 2026). Companion ask paper for the growable buffer concept. D0009R0.
