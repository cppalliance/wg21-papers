---
title: "Files: Design Rationale"
document: D0020R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper documents the design rationale for async file I/O in the Network Endeavor.

[D0019R0]<sup>[1]</sup> proposes the normative vocabulary (`stream_file`, `random_access_file`, `file_flags`). This paper is the companion record: why async files belong in a coroutine-native I/O library, why two types instead of one, how the design maps to platform capabilities, and where the convergence evidence lives. Read [D0019R0]<sup>[1]</sup> for the proposal; read this paper when you need the audit trail.

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial version.

---

## 1. Disclosure

This paper asks for nothing.

The author develops and maintains [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup>. File I/O ships in Corosio today. The experience informs this rationale.

This paper is part of the [Network Endeavor](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) ([P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[4]</sup>).

---

## 2. Why Async Files

### 2.1 The Problem

Synchronous file I/O blocks the calling thread. In a coroutine-native server, a single blocking `read()` call stalls the entire event loop - every socket, every timer, every pending operation waits for the disk. The obvious workaround (thread pools for blocking file I/O) introduces context switches, synchronization overhead, and cancellation complexity that the coroutine model was designed to eliminate.

### 2.2 Platform Support

**Windows IOCP.** Windows provides true async file I/O through `FILE_FLAG_OVERLAPPED`. The file handle registers with an I/O completion port. `ReadFile` and `WriteFile` with an `OVERLAPPED` structure complete asynchronously. The completion notification arrives on the IOCP thread pool - the same mechanism that handles socket I/O. No separate thread pool. No blocking. File I/O and socket I/O share the same completion infrastructure.

**Linux io_uring.** `io_uring` (kernel 5.1+) provides true async file I/O through submission and completion queues. `IORING_OP_READ` and `IORING_OP_WRITE` submit file operations that complete without blocking the submitting thread. `io_uring` handles files, sockets, timers, and signals through one interface. It is the Linux equivalent of IOCP for unified async I/O.

**POSIX fallback.** On platforms without `io_uring` or IOCP, POSIX file I/O (`read()`, `write()`, `pread()`, `pwrite()`) is synchronous. The implementation dispatches these calls to a dedicated I/O thread pool. The coroutine suspends at `co_await`, the thread pool executes the blocking call, and the coroutine resumes on completion. The async interface is preserved. The coroutine body is identical regardless of backend.

### 2.3 One Interface, Three Backends

```cpp
// This code is identical on Windows, Linux, and POSIX
std::io::stream_file log(ctx);
auto [ec] = co_await log.open(path, flags);
if (ec) co_return ec;
auto [ec2, n] = co_await log.write_some(
    std::io::buffer(data));
```

The application developer does not know or care which backend runs underneath. On Windows, this goes through IOCP. On modern Linux, this can go through `io_uring`. On older Linux or BSD, this goes through the thread pool fallback. The coroutine body does not change.

---

## 3. Two File Types

### 3.1 Why Not One Type

A single `file` type with both sequential and positional access creates problems:

1. **Hidden mutable state.** A `file` with an internal position and `read_some(buffers)` has a cursor that advances implicitly. Two coroutines reading the same file concurrently race on the cursor. The race is invisible in the source code.

2. **API surface confusion.** A single type with both `read_some(buffers)` and `read_some_at(offset, buffers)` invites mistakes. Which advances the position? Does `read_some_at` move the cursor? The answer depends on the platform (`pread()` does not move the cursor on POSIX; `ReadFile` with explicit offset does not advance the internal pointer on Windows). A single type hides this.

3. **Concept satisfaction.** `Stream` requires `read_some(buffers)` without an offset. A type that satisfies `Stream` must have sequential semantics. A type that takes an offset parameter is a different concept.

Two types make the access pattern explicit in the type system:

| Type | Access Pattern | Concept | Internal State |
|------|---------------|---------|----------------|
| `stream_file` | Sequential | Satisfies `Stream` | File position |
| `random_access_file` | Positional | Does not satisfy `Stream` | No position |

### 3.2 `stream_file`: The Sequential Case

`stream_file` is the right choice for:

- **Log files.** Append-only. Never seek. `write_some()` appends.
- **Config file reads.** Read from beginning to end. Never seek.
- **Streaming output.** Pipe-like semantics. Sequential write.
- **Generic algorithms.** Any algorithm that accepts `Stream` or `any_stream&` works with `stream_file`.

The sequential file has one internal state: the current position. Each `read_some()` or `write_some()` advances it. This is the same model as a socket - bytes flow in order.

### 3.3 `random_access_file`: The Positional Case

`random_access_file` is the right choice for:

- **Database page files.** Read page N at offset `N * page_size`. Write page M at offset `M * page_size`. No sequential relationship between operations.
- **Memory-mapped file alternatives.** When `mmap()` is not available or not desirable, explicit offset-based access provides the same capability.
- **Concurrent readers.** Multiple coroutines reading different regions. No cursor contention.
- **Write-ahead logs.** Random reads for recovery. Sequential writes to the tail (with explicit offset tracking by the caller).

The positional file has no internal state. The caller provides the offset with every operation. This makes concurrent access safe without synchronization.

### 3.4 Precedent

Asio provides both `basic_stream_file` and `basic_random_access_file` as separate types. Boost.Beast consumers use both. The separation has been stable since introduction.

---

## 4. Relationship to Stream Concepts

### 4.1 `stream_file` Satisfies `Stream`

`stream_file` satisfies the `ReadStream`, `WriteStream`, and `Stream` concepts defined in Paper 6 (D0011/D0012). This means:

- `stream_file` works with `any_stream`.
- Algorithms written against `Stream` work with files.
- A function that copies from one `Stream` to another copies from file to socket, socket to file, or file to file without specialization.

```cpp
std::io::task<> pipe(
    std::io::any_stream& src,
    std::io::any_stream& dst)
{
    std::array<std::byte, 8192> buf;
    for (;;)
    {
        auto [ec, n] = co_await src.read_some(
            std::io::buffer(buf));
        if (ec) break;
        co_await dst.write_some(
            std::io::buffer(buf, n));
    }
}
```

This function does not know whether `src` is a file, a socket, a TLS stream, or a zlib decompressor. The `Stream` concept abstracts them all.

### 4.2 `random_access_file` Does Not Satisfy `Stream`

The `Stream` concept requires `read_some(MutableBufferSequence)` - no offset parameter. `random_access_file` provides `read_some_at(offset, MutableBufferSequence)`. The signatures are incompatible because the semantics are incompatible.

Forcing `random_access_file` to satisfy `Stream` would require one of:

1. **Hidden position.** Add an internal cursor and implement `read_some(buffers)` by reading at the cursor. This defeats the purpose of a positional type.
2. **Separate concept.** Define `PositionalStream` with `read_some_at`. This is what the design already does by giving `random_access_file` its own interface.

The types are deliberately separate. Sequential I/O and positional I/O are different access patterns. The type system makes the distinction visible.

---

## 5. Open Modes and Flags Design

### 5.1 Why an Enum, Not Strings

POSIX `fopen()` uses mode strings (`"r"`, `"w"`, `"a"`, `"r+"`, etc.). This proposal uses a bitmask enum. Reasons:

1. **Combinability.** `file_flags::write | file_flags::create | file_flags::truncate` is self-documenting. `"w"` is not - you must know that `"w"` implies create and truncate.
2. **Type safety.** The compiler rejects `file_flags::read | 42`. It cannot reject `"r" + "w"`.
3. **Extensibility.** New flags (`exclusive`, future `direct`, `sync`) add orthogonally. String modes require defining new magic strings.
4. **Platform mapping.** The bitfield maps directly to both POSIX `open()` flags and Windows `CreateFileW` parameters. No parsing step.

### 5.2 Why Not `std::ios_base::openmode`

`std::ios_base::openmode` exists. It is not reused here because:

1. **It conflates formatting with access.** `std::ios_base::binary` controls text translation, not access mode. Async file I/O is always binary.
2. **Missing modes.** `std::ios_base::openmode` has no `exclusive` equivalent.
3. **Historical baggage.** The interaction between `ios_base::in`, `ios_base::out`, `ios_base::trunc`, and `ios_base::app` is specified as a table of non-obvious combinations. The mapping from intent to flags is not intuitive.

`file_flags` is a clean slate. Each flag has one meaning. Combinations are additive.

### 5.3 `append` Semantics

When `file_flags::append` is set, every `write_some()` operation atomically positions the write at the end of the file before writing. This is the POSIX `O_APPEND` semantic. On Windows, it maps to `FILE_APPEND_DATA`. The guarantee is important for concurrent log writers: Multiple processes appending to the same file do not interleave within a single write operation.

`append` is only meaningful for `stream_file`. For `random_access_file`, the caller provides the offset explicitly - there is no implicit "end of file" positioning.

---

## 6. Relationship to `std::filesystem`

### 6.1 Complementary, Not Competing

`std::filesystem` provides:

- Path manipulation (`path`, `relative()`, `canonical()`)
- Directory operations (`create_directories()`, `directory_iterator`)
- File status (`exists()`, `file_size()`, `last_write_time()`)
- Synchronous file operations (`copy_file()`, `rename()`, `remove()`)

`std::io` file types provide:

- Async byte-level I/O (`read_some()`, `write_some()`)
- Platform-native async open (`open()` with IOCP/io_uring integration)
- Stream concept satisfaction (interoperability with sockets)

There is no overlap. `std::filesystem::path` is the input to `std::io::stream_file::open()`. The two facilities compose:

```cpp
namespace fs = std::filesystem;

auto temp = fs::temp_directory_path() / "upload.tmp";
std::io::stream_file f(ctx);
co_await f.open(temp, file_flags::write | file_flags::create);
// ... write bytes ...
f.close();
fs::rename(temp, final_path);  // atomic on most platforms
```

### 6.2 Why Not Extend `std::filesystem`

`std::filesystem` is synchronous. Adding async operations to it would require:

1. An execution context parameter on every async operation.
2. A coroutine return type for the async overloads.
3. Cancellation support.
4. Buffer sequence parameters.

This is the entire `std::io` file interface. Rather than retrofitting async semantics onto a synchronous API, the design provides a separate type purpose-built for async I/O. The synchronous API remains simple. The async API remains clean.

---

## 7. Convergence

Six ecosystems provide async file I/O. All arrive at the same structural decisions.

### 7.1 Go: `os.File`

Go combines both access patterns in one type (`Read` vs `ReadAt`). The goroutine scheduler handles blocking transparently. Go does not need two types because goroutines are cheap and scheduling is implicit. C++ coroutines are different - the type system must distinguish access patterns.

### 7.2 Rust: `tokio::fs::File`

Tokio's `File` wraps blocking I/O in a thread pool. It implements `AsyncRead` and `AsyncWrite` (sequential). Positional access is available through OS-specific extensions (`read_at` on Unix). The sequential/positional distinction exists but is handled through traits rather than separate types.

### 7.3 .NET: `FileStream`

.NET combines both patterns in `FileStream` with an explicit `Position` property and `ReadAsync`. Async is opt-in via the constructor. One type, mutable position state, explicit seeking.

### 7.4 Python: `aiofiles`

Python wraps blocking I/O in a thread pool executor. Sequential by default. Positional access through explicit `seek()`. One type.

### 7.5 Asio: `stream_file` / `random_access_file`

Asio separates the two access patterns into distinct types. `stream_file` satisfies `AsyncReadStream` and `AsyncWriteStream`. `random_access_file` has a different interface with explicit offset parameters. This proposal follows Asio's structural decision.

### 7.6 libuv: `uv_fs_t`

libuv provides a single low-level API with an explicit offset parameter. Offset `-1` means "use current position" (sequential). Any non-negative offset means positional. One API surface, mode selected by parameter.

### 7.7 Summary

| Ecosystem | Types | Sequential | Positional | Async Mechanism |
|-----------|-------|------------|------------|-----------------|
| Go | 1 | `Read` | `ReadAt` | Goroutine scheduler |
| Rust/Tokio | 1 | `AsyncRead` trait | OS extension | Thread pool |
| .NET | 1 | `ReadAsync` | `Position` + `ReadAsync` | IOCP native |
| Python | 1 | `read()` | `seek()` + `read()` | Thread pool |
| Asio | 2 | `stream_file` | `random_access_file` | IOCP/io_uring/thread pool |
| libuv | 1 | offset = -1 | offset >= 0 | Thread pool |

Every ecosystem distinguishes sequential from positional access. Some distinguish through types (Asio). Some distinguish through API parameters (libuv, Go). Some distinguish through mutable state (Python, .NET). This proposal uses types because:

1. The type system catches misuse at compile time.
2. Concept satisfaction (`Stream`) is type-level.
3. The distinction is semantic, not parametric.

---

## 8. Anticipated Objections

### 8.1 "But `std::fstream` already exists"

`std::fstream` is synchronous. It blocks the calling thread on every read and write. In a coroutine-native event loop, a blocking read stalls every pending operation. `std::fstream` cannot be made async without fundamental redesign - it has no execution context, no completion notification mechanism, no cancellation.

`std::fstream` also carries decades of design decisions that do not serve modern I/O: locale-dependent character conversion, `sync_with_stdio`, virtual function overhead on every character, `sentry` objects. These are not defects - they serve `iostream`'s original domain. But they are not appropriate for byte-level async I/O.

`stream_file` and `random_access_file` do not replace `std::fstream`. They serve a different domain. Code that formats text with locale support continues to use `std::fstream`. Code that moves bytes asynchronously uses `std::io`.

### 8.2 "But async file I/O is platform-specific"

Every async I/O mechanism is platform-specific in implementation. IOCP is Windows. `io_uring` is Linux. `kqueue` is BSD. The standard does not mandate a specific implementation - it mandates behavior. `std::thread` is implemented with pthreads on POSIX and Windows threads on Windows. `std::filesystem` is implemented with OS-specific syscalls. `std::io::stream_file` follows the same pattern.

The interface is portable. The implementation is platform-specific. This is the universal pattern for system-adjacent standard library facilities.

### 8.3 "But `io_uring` changes the file I/O model"

`io_uring` provides true kernel-level async file I/O - no thread pool needed. Some argue that standardizing file I/O now locks in a thread-pool-based model that `io_uring` supersedes.

This objection misunderstands the proposal. The interface (`read_some()`, `write_some()`, `read_some_at()`, `write_some_at()`) is backend-agnostic. An implementation on modern Linux uses `io_uring` natively. An implementation on older Linux uses a thread pool. An implementation on Windows uses IOCP. The coroutine body is identical in all cases. The standard specifies the interface and its behavioral guarantees, not the kernel mechanisms.

`io_uring` does not change the file I/O model for users. It changes the implementation. The interface proposed here accommodates both thread-pool and native-async backends without modification.

### 8.4 "But files should use memory-mapped I/O"

Memory-mapped I/O (`mmap()`, `CreateFileMapping`) maps file contents directly into process address space. It is the fastest path for random access to large files on many platforms. Why not standardize `mmap()` instead?

1. **Different abstraction level.** `mmap()` provides a memory region, not a stream. It does not compose with `Stream` concepts or buffer sequences. It is a different facility serving a different pattern.
2. **Portability concerns.** `mmap()` behavior varies across platforms in ways that are difficult to abstract: truncation behavior, coherency guarantees, signal handling on access errors (SIGBUS on Linux vs. structured exceptions on Windows).
3. **Not always appropriate.** `mmap()` requires the entire file (or a region) to be addressable. For files larger than available virtual address space (32-bit systems), for streaming access patterns, or for files on network filesystems where `mmap()` has poor performance, explicit read/write is necessary.
4. **Complementary.** A future paper can propose memory-mapped file facilities. They do not compete with explicit async I/O - they serve different access patterns.

Memory-mapped files are deferred (Section 9). This proposal addresses the explicit I/O case.

---

## 9. Deferrals

The following facilities are intentionally deferred from this proposal:

### 9.1 Memory-Mapped Files

Memory mapping (`mmap()` / `CreateFileMapping`) provides zero-copy access to file contents through virtual memory. It is a different abstraction - a memory region rather than an I/O stream. A future paper may propose `mapped_file` or `memory_mapped_region`. It does not block this proposal.

### 9.2 Directory Watching

File system change notifications (`inotify`, `ReadDirectoryChangesW`, `kqueue` `EVFILT_VNODE`) enable reactive programming based on filesystem events. They are useful but orthogonal to byte-level file I/O. A future paper may propose `directory_watcher`. It does not block this proposal.

### 9.3 `io_uring`-Native File Operations

`io_uring` supports operations beyond simple read/write: `splice`, `tee`, `fallocate`, `statx`, `renameat2`. These are powerful but Linux-specific. A future paper may propose platform extensions or a broader operation set. The current proposal covers the portable core.

### 9.4 File Locking

Advisory and mandatory file locking (`flock`, `fcntl`, `LockFileEx`) provides inter-process coordination. It is useful for databases and log rotation. It is orthogonal to the byte I/O interface and can be added independently.

---

## 10. Why Now

### 10.1 Stage Two Dependencies

This paper is a Stage Two paper. It depends on:

- **Paper 1 (IoAwaitable Protocol).** `stream_file` and `random_access_file` return `IoAwaitable` awaitables. Their `open()`, `read_some()`, `write_some()`, `read_some_at()`, and `write_some_at()` operations all participate in the IoAwaitable protocol for execution context propagation, cancellation, and frame allocation.
- **Paper 6 (Stream Concepts).** `stream_file` satisfies `Stream`. The concept taxonomy from Paper 6 gives `stream_file` its composition power.

### 10.2 Completing the I/O Story

Papers 1-7 (Stage One) provide the execution model, task types, buffers, streams, and combinators. Papers 8-9 (Timers, Signals) provide the simplest kernel interactions. Paper 10 (Files) provides the first heavy I/O primitive. Together, Papers 8-10 prove that the IoAwaitable protocol scales from simple notifications (timers) through signal handling to sustained byte transfer (files).

After Paper 10, a user can write a complete application that:

- Reads configuration from files
- Writes structured logs asynchronously
- Handles signals for graceful shutdown
- Uses timers for periodic tasks
- Composes all of the above with `when_all`/`when_any`

All without a single blocking call. All with one `task<T>` type. All with the same error model.

### 10.3 Implementation Maturity

File I/O ships in [Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup> today. Both `stream_file` and `random_access_file` are implemented and tested. The Windows implementation uses IOCP with `FILE_FLAG_OVERLAPPED`. The Linux implementation uses POSIX I/O with a thread pool backend. `io_uring` support is on the roadmap. The proposal reflects deployed, tested code.

---

## 11. Closing

Files are not exotic. Every program reads or writes files. The question is not whether C++ needs async file I/O - it is whether the standard should provide it or leave every project to reinvent it against raw platform APIs.

`stream_file` satisfies `Stream`. It composes with sockets, TLS, compression, and every other stream-shaped abstraction. `random_access_file` provides safe concurrent positional access without hidden state. Both integrate with the IoAwaitable protocol for cancellation, execution context propagation, and frame allocation.

Two types. One flag enum. The same buffer sequences, error model, and cancellation mechanism as every other I/O primitive in the series. The generic algorithms that work on sockets work on files. The ecosystem benefits compound.

---

## Appendix A: Synopsis

```cpp
namespace std::io {

  enum class file_flags : unsigned {
    read       = 1,
    write      = 2,
    read_write = 3,
    create     = 4,
    truncate   = 8,
    append     = 16,
    exclusive  = 32
  };

  constexpr file_flags operator|(
      file_flags lhs, file_flags rhs) noexcept;
  constexpr file_flags operator&(
      file_flags lhs, file_flags rhs) noexcept;
  constexpr file_flags operator^(
      file_flags lhs, file_flags rhs) noexcept;
  constexpr file_flags operator~(
      file_flags f) noexcept;

  class stream_file {
  public:
    explicit stream_file(execution_context& ctx);

    stream_file(stream_file&&) noexcept;
    stream_file& operator=(stream_file&&) noexcept;
    ~stream_file();

    stream_file(stream_file const&) = delete;
    stream_file& operator=(
        stream_file const&) = delete;

    IoAwaitable auto open(
        std::filesystem::path const& p,
        file_flags flags);
    void close();
    bool is_open() const noexcept;

    IoAwaitable auto read_some(
        MutableBufferSequence auto const& buffers);
    IoAwaitable auto write_some(
        ConstBufferSequence auto const& buffers);
  };

  class random_access_file {
  public:
    explicit random_access_file(
        execution_context& ctx);

    random_access_file(
        random_access_file&&) noexcept;
    random_access_file& operator=(
        random_access_file&&) noexcept;
    ~random_access_file();

    random_access_file(
        random_access_file const&) = delete;
    random_access_file& operator=(
        random_access_file const&) = delete;

    IoAwaitable auto open(
        std::filesystem::path const& p,
        file_flags flags);
    void close();
    bool is_open() const noexcept;

    IoAwaitable auto read_some_at(
        std::uint64_t offset,
        MutableBufferSequence auto const& buffers);
    IoAwaitable auto write_some_at(
        std::uint64_t offset,
        ConstBufferSequence auto const& buffers);

    std::uint64_t size() const;
  };

}
```

---

## Appendix B: Corosio Headers

The following headers implement the proposed facilities in [Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup>:

| Header | Contents |
|--------|----------|
| `corosio/stream_file.hpp` | `stream_file` class |
| `corosio/random_access_file.hpp` | `random_access_file` class |
| `corosio/file_flags.hpp` | `file_flags` enum and operators |

Implementation status:

| Platform | Backend | Status |
|----------|---------|--------|
| Windows | IOCP (`FILE_FLAG_OVERLAPPED`) | Shipping |
| Linux | POSIX thread pool | Shipping |
| Linux | `io_uring` | Roadmap |
| macOS/BSD | POSIX thread pool | Shipping |

---

## Acknowledgments

Christopher Kohlhoff designed Asio's `basic_stream_file` and `basic_random_access_file`. Their separation into distinct types with distinct concept satisfaction is the structural precedent for this proposal.

Jens Axboe created `io_uring`, which makes true async file I/O possible on Linux without thread pool overhead.

---

## References

[1] *Files* (Vinnie Falco, 2026). Companion ask paper. D0019R0.

[2] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[3] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[4] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[5] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[6] [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[7] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).

[8] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - Async I/O including stream_file and random_access_file (Christopher Kohlhoff, 2003-2026).

[9] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[10] [Tokio](https://docs.rs/tokio/latest/tokio/fs/struct.File.html) - Async runtime for Rust (Tokio Contributors, 2016-2026).

[11] [libuv](https://docs.libuv.org/en/v1.x/fs.html) - Cross-platform async I/O library (libuv Contributors, 2011-2026).
