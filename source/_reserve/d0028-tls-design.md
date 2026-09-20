---
title: "TLS: Design Rationale"
document: D0028R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Every language has a TLS wrapper except C++.

Go has `crypto/tls` since 2012. Rust has `rustls` and `native-tls`. Python has `ssl` since 2004. .NET has `SslStream` since 2005. Java has `SSLSocket` since 1999. Each wraps TLS the same way: A configuration object holds certificates and policy, an encrypted stream wraps a transport. The shape has been stable since SSLv3 in 1996. Thirty years of convergence across seven ecosystems produced the same two-object design every time.

This paper documents the design rationale for `tls_context` and `tls_stream` as proposed in the companion ask paper *TLS*<sup>[1]</sup>. The configuration object is `tls_context`. The encrypted stream is `tls_stream`. The cryptographic engine is implementation-defined. The interface is portable. This paper is Paper 14 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[2]</sup>. It depends on Paper 1 (the IoAwaitable Protocol, [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[3]</sup> and [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[4]</sup>) and Paper 6 (Stream Concepts, D0011/D0012). Stage Two paper. Final paper in the series.

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author develops and maintains [Capy](https://github.com/cppalliance/capy)<sup>[5]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[6]</sup>. TLS ships in Corosio today with OpenSSL and WolfSSL backends. Both engines use the same abstract `tls_context` API. The author maintains [Boost.Beast](https://github.com/boostorg/beast)<sup>[7]</sup>, which has used Asio's `ssl::context` and `ssl::stream`<sup>[8]</sup> for HTTPS and secure WebSocket since 2017. The body of work creates a bias toward a portable TLS wrapper.

This paper documents the design rationale for the TLS vocabulary proposed in the companion *TLS*<sup>[1]</sup>. The stream concepts that `tls_stream` satisfies are proposed in *Stream Concepts*<sup>[14]</sup> and *Stream Concepts: Design Rationale*<sup>[15]</sup>.

This paper asks for nothing.

---

## 2. Why TLS in the Standard

### 2.1 The Missing Row

| Language   | TLS Wrapper                  | Year Introduced |
| ---------- | ---------------------------- | --------------- |
| Java       | `SSLSocket` / `SSLContext`   | 1999            |
| Python     | `ssl.SSLContext` / `ssl.SSLSocket` | 2004      |
| .NET       | `SslStream`                  | 2005            |
| Go         | `crypto/tls`                 | 2012            |
| Rust       | `rustls` / `native-tls`     | 2016            |
| C++        | (none)                       | -               |

Every row but the last has a TLS wrapper in its standard library or de facto standard ecosystem. Every row but the last allows a developer to write `connect -> handshake -> read/write` without dropping to a C library.

C++ developers drop to OpenSSL, WolfSSL, BoringSSL, SChannel, or Secure Transport directly. Each has a different API. Each has different memory management conventions. Each has different error reporting. A portable C++ program that needs TLS must either depend on a third-party wrapper (Asio SSL, Poco NetSSL, Qt SSL) or maintain engine-specific code paths.

The standard library can eliminate that fragmentation the same way `std::filesystem` eliminated path-manipulation fragmentation: Specify the interface, let the implementation provide the platform integration.

### 2.2 Every Server Needs TLS

TLS is not optional infrastructure. It is baseline infrastructure. HTTP/2 requires TLS in practice (all major browsers require it). HTTP/3 requires TLS 1.3 by specification. gRPC requires TLS. Cloud provider APIs require TLS. Database connections increasingly require TLS. Internal service meshes require mutual TLS.

A C++ networking facility without TLS is a networking facility that cannot connect to the modern internet without a third-party dependency the standard does not define.

### 2.3 The Risk Profile

The risk profile is lopsided.

**The interface carries no risk.** The context-plus-stream shape has been stable since SSLv3 in 1996. No language has redesigned its TLS wrapper API. Configuration, handshake, read, write, shutdown - the operations have not changed in thirty years. They will not change for C++.

**The implementation carries all the risk.** TLS vulnerabilities are discovered regularly. Heartbleed (2014), POODLE (2014), ROBOT (2017), Raccoon (2020). Each was a bug in a specific engine, not in the wrapper API. Each was patched in the engine, not in the language standard. The implementation-defined engine model means the fix ships as an OS or library update. The standard library binary links against the patched engine. No recompilation of user code.

**Standardise the riskless part. Offload the risky implementation to the OS and ecosystem.**

---

## 3. The Shape

### 3.1 Context Plus Stream

Every TLS wrapper, in every language, in every era, consists of two objects:

1. **A configuration object** that holds certificates, keys, trust anchors, protocol version constraints, and verification policy. Created once. Shared across connections. Thread-safe for reads.
2. **An encrypted stream** that wraps a transport and performs the handshake, encryption, and decryption. One per connection. Not thread-safe. Owned by the coroutine or thread that drives the connection.

This is not a design choice. It is a convergence result. The two objects exist because TLS has two concerns that have different lifetimes: Configuration outlives any single connection; the encrypted channel dies with the connection.

### 3.2 Stable Since SSLv3

The SSLv3 specification (1996)<sup>[9]</sup> established the handshake, record, and alert protocols. Every subsequent version - TLS 1.0, 1.1, 1.2, 1.3 - changed the cryptographic details inside those protocols. None changed the wrapper API. `handshake`, `read`, `write`, `shutdown` have been the four operations since the beginning. The configuration object grew new options (ALPN in TLS 1.2 extensions, 0-RTT in TLS 1.3), but the shape - set certificates, set trust, set policy, create context, pass to stream - has not changed.

Thirty years of stability in a security protocol's wrapper API is not an accident. It reflects the fundamental decomposition: The wrapper is a byte transformer. Bytes go in encrypted, come out decrypted. The transformer's interface is trivial. The transformer's internals are not.

### 3.3 Asio's Two Decades

[Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[8]</sup> has shipped `ssl::context` and `ssl::stream` since 2005. The API has been source-stable for twenty years. The internal implementation has been rewritten multiple times - from blocking BIO to async BIO, from OpenSSL 0.9.x to 3.x - without changing the user-facing interface. This is the empirical proof that the wrapper API is decoupled from the engine.

Corosio's `tls_context` and `tls_stream` are the coroutine-native successors. Same shape. Different engine integration. The interface survived the transition from callbacks to coroutines without change.

---

## 4. Implementation-Defined Engine

### 4.1 Why Not Mandate OpenSSL

OpenSSL is the most widely deployed TLS library. It is not the only one. Mandating OpenSSL would create three problems:

**Platform conflict.** Windows has SChannel. macOS has Secure Transport. Both are maintained by the OS vendor, integrated with the OS certificate store, and updated through the OS update mechanism. Mandating OpenSSL would force implementations on these platforms to ship, maintain, and update a second TLS stack alongside the native one. Users on those platforms would get worse integration, not better.

**Licensing.** OpenSSL's license changed from a BSD-style license to Apache 2.0 in version 3.0. Not every C++ implementation vendor is willing or able to ship Apache-2.0-licensed code as part of the standard library. The standard should not create a licensing dependency.

**Update cadence.** OpenSSL CVEs are published irregularly. The interval between disclosure and patch varies from days to weeks. A standard library that ships a mandated engine must track that cadence. A standard library that delegates to the platform engine inherits the platform's update cadence, which is already managed by the OS vendor.

### 4.2 The `std::filesystem` Model

`std::filesystem` specifies effects, not mechanisms. `std::filesystem::remove()` does not specify whether it calls `unlink()`, `DeleteFileW()`, or `NtSetInformationFile()`. It specifies that the file is removed. The mechanism is the platform's responsibility.

`tls_context` and `tls_stream` follow the same model. `tls_context::set_default_verify_paths()` specifies that the system trust store is loaded. It does not specify whether that trust store is `/etc/ssl/certs`, the macOS Keychain, or the Windows certificate store. `tls_stream::handshake()` specifies that a TLS handshake is performed. It does not specify whether the handshake uses OpenSSL, WolfSSL, BoringSSL, SChannel, or Secure Transport.

### 4.3 Patchability

A TLS vulnerability disclosed on Monday must be patchable by Tuesday.

With an implementation-defined engine, the patch is an OS or library update. The shared library that implements `tls_stream` links against the engine. The engine is updated. The next program launch picks up the fix. No recompilation. No redistribution. No standard library release.

With a mandated engine, the patch requires the standard library vendor to update the bundled engine, rebuild, test, and release. The interval is weeks, not hours. Every deployed binary must be rebuilt or the old engine remains in use.

The implementation-defined model is not a compromise. It is the security-correct choice.

---

## 5. `tls_stream` as `Stream`

### 5.1 Satisfies `Stream`

`tls_stream<NextLayer>` provides `read_some()` and `write_some()` with the same signatures as `tcp_socket`, `stream_file`, and every other type that satisfies `Stream` (Paper 6). This means:

```cpp
static_assert(Stream<tls_stream<tcp_socket>>);
```

Any algorithm written against `Stream` works on `tls_stream`. Any function that accepts `any_stream&` handles encrypted and unencrypted connections without branching.

### 5.2 Composes with `any_stream`

Type erasure is the integration point. A library compiled once against `any_stream&` handles TCP, TLS, UNIX domain sockets, and test mocks without recompilation:

```cpp
std::io::tcp_socket raw_sock(ctx, ep);
co_await raw_sock.connect(ep);

std::io::tls_stream<std::io::tcp_socket> tls_sock(
    std::move(raw_sock), tls_ctx);
co_await tls_sock.handshake(handshake_type::client);

// Type-erase for the library.
std::io::any_stream stream(std::move(tls_sock));
co_await http::read(stream, buffer, request);
```

The HTTP library never sees `tls_stream`. It sees `any_stream`. The encryption is invisible. The same library handles HTTP and HTTPS with one code path.

### 5.3 Layered on Any Transport

`tls_stream` is a template parameterised on `NextLayer`. The `NextLayer` is any `Stream`. The most common case is `tcp_socket`, but the design does not restrict it:

| `NextLayer`             | Use Case                                |
| ----------------------- | --------------------------------------- |
| `tcp_socket`            | Standard internet TLS                   |
| `any_stream`            | Type-erased transport                   |
| `local_stream_socket`   | TLS over UNIX domain sockets            |
| `tls_stream<tcp_socket>`| Nested TLS (tunnelling)                 |
| User-defined `Stream`   | Testing, simulation, proxying           |

The layering is structural. The `tls_stream` does not know what it wraps. It reads bytes from the next layer, decrypts them, and presents them to the application. It takes bytes from the application, encrypts them, and writes them to the next layer. The next layer's identity is irrelevant.

---

## 6. Certificate Management Design

### 6.1 File-Based Loading

Certificates and keys are loaded from files. This is the universal convention. Every TLS engine supports PEM and DER file loading. Every deployment pipeline generates certificate files. The file-based API is the lowest common denominator that works everywhere.

The alternative - loading from memory buffers - is a useful extension but not the primary interface. Memory-buffer loading requires the application to manage the buffer lifetime, handle encoding, and deal with engine-specific parsing. File-based loading delegates all of that to the engine.

### 6.2 System Trust Store

`set_default_verify_paths()` loads the operating system's trust store. This is the function a TLS client calls to verify server certificates against the system's root CAs.

The system trust store is managed by the OS vendor. It is updated when CAs are added, revoked, or distrusted. The application does not manage the trust store. It delegates to the platform.

This is the correct default for client applications. A custom trust store is needed only for certificate pinning, private CAs, or testing. Those cases are served by loading explicit certificate files, not by bypassing the system trust store.

### 6.3 Verification Policy

The `verify_mode` enumeration controls what happens during the handshake:

- **Client connecting to a server:** Set `verify_mode::peer`. The client verifies the server's certificate against the trust store. This is the minimum for secure communication.
- **Server not requiring client certificates:** Leave `verify_mode::none` (the default). The server presents its certificate; the client does not.
- **Server requiring mutual TLS:** Set `verify_mode::peer | verify_mode::fail_if_no_peer_cert`. Both sides present and verify certificates.

The policy is simple because the common cases are simple. Custom verification callbacks, hostname override, and certificate pinning are extensions that the companion *TLS*<sup>[1]</sup> Section 10 lists as deferrals.

---

## 7. Convergence

Seven ecosystems. Same shape. Same operations. Same decomposition.

| Ecosystem      | Context Type               | Stream Type                | Handshake | Read     | Write    | Shutdown |
| -------------- | -------------------------- | -------------------------- | --------- | -------- | -------- | -------- |
| Asio (2005)    | `ssl::context`<sup>[8]</sup> | `ssl::stream<T>`         | yes       | yes      | yes      | yes      |
| Java (1999)    | `SSLContext`<sup>[10]</sup>  | `SSLSocket`              | yes       | yes      | yes      | yes      |
| Python (2004)  | `ssl.SSLContext`<sup>[11]</sup> | `ssl.SSLSocket`       | yes       | yes      | yes      | yes      |
| .NET (2005)    | `SslClientAuthenticationOptions` | `SslStream`<sup>[12]</sup> | yes | yes | yes      | yes      |
| Go (2012)      | `tls.Config`<sup>[13]</sup>  | `tls.Conn`               | yes       | yes      | yes      | yes      |
| Rust (2016)    | `TlsConnector` / `TlsAcceptor` | `TlsStream<S>`       | yes       | yes      | yes      | yes      |
| This paper     | `tls_context`              | `tls_stream<NextLayer>`    | yes       | yes      | yes      | yes      |

The column headers are the four operations. Every row has "yes" in every column. The shape is universal.

### 7.1 Go `crypto/tls`

Go's `tls.Config`<sup>[13]</sup> holds certificates, root CAs, and verification policy. `tls.Dial()` creates a `tls.Conn` that wraps a `net.Conn`. The `tls.Conn` satisfies `net.Conn` itself - encrypted and unencrypted connections are interchangeable. This is the same property that `tls_stream` satisfying `Stream` provides for C++.

### 7.2 Rust `rustls` / `native-tls`

Rust has two TLS ecosystems. `rustls` is a pure-Rust implementation. `native-tls` delegates to the platform engine (SChannel, Secure Transport, OpenSSL). Both expose the same shape: a connector/acceptor configuration object and a `TlsStream<S>` that wraps a transport stream. The generic parameter `S` is Rust's equivalent of `NextLayer`. The two ecosystems are interchangeable at the API level.

### 7.3 .NET `SslStream`

.NET's `SslStream`<sup>[12]</sup> wraps any `System.IO.Stream`. Configuration is passed through `SslClientAuthenticationOptions` or `SslServerAuthenticationOptions`. The wrapped stream satisfies `Stream` - the same layering property as every other ecosystem.

### 7.4 Python `ssl`

Python's `ssl` module<sup>[11]</sup> provides `SSLContext` for configuration and `SSLSocket` for the encrypted channel. `SSLContext.wrap_socket()` takes a plain socket and returns an `SSLSocket`. The wrapped socket satisfies the same interface as the plain socket. Same shape. Same layering.

### 7.5 Java `SSLSocket` / `SSLContext`

Java's `javax.net.ssl`<sup>[10]</sup> provides `SSLContext` for configuration and `SSLSocketFactory` for creating `SSLSocket` instances. `SSLSocket` extends `Socket` - the encrypted socket is substitutable for the plain socket. The factory pattern differs from the direct constructor in other languages, but the context-plus-stream decomposition is the same.

---

## 8. Risk Profile

### 8.1 Interface Risk: None

The wrapper API has four operations: handshake, read, write, shutdown. These operations have existed in every TLS wrapper since SSLv3 (1996). No TLS version transition - SSLv3 to TLS 1.0, TLS 1.0 to 1.1, 1.1 to 1.2, 1.2 to 1.3 - has changed the wrapper API. The next version of TLS will not change the wrapper API.

The configuration API has grown incrementally. TLS 1.2 added ALPN. TLS 1.3 added 0-RTT and simplified the cipher suite model. Each addition was a new option on the configuration object, not a redesign of the configuration object.

The interface is the stable part.

### 8.2 Implementation Risk: Managed

TLS implementations have bugs. Heartbleed was a buffer over-read in OpenSSL's heartbeat extension. POODLE was a padding oracle in SSLv3 CBC mode. Each was a bug in the cryptographic implementation, not in the wrapper API.

The implementation-defined engine model means:

- **The vendor chooses the engine.** On Windows, SChannel. On macOS, Secure Transport. On Linux, OpenSSL or WolfSSL. The choice is the vendor's, informed by platform integration, licensing, and security posture.
- **The vendor patches the engine.** An OpenSSL CVE triggers an OpenSSL update. The standard library vendor rebuilds against the patched OpenSSL. Or, on platforms where the engine is an OS component, the OS vendor patches the engine directly.
- **The user relinks.** No source changes. No recompilation. The dynamic library picks up the patched engine.

The implementation is the risky part. The implementation-defined model manages that risk by placing it where it belongs: with the platform and the engine vendor, not with the standard.

---

## 9. Anticipated Objections

### 9.1 "But TLS Is Too Complex for the Standard"

TLS the protocol is complex. The TLS wrapper API is not. The wrapper has four operations: handshake, read, write, shutdown. The configuration object has five to ten functions. The total API surface is smaller than `std::regex`.

The complexity of the cryptographic implementation is the engine's problem. The standard does not specify the implementation. It specifies the interface. The interface is small.

`std::filesystem` is a precedent. Filesystems are complex. Journaling, permissions, symbolic links, race conditions, platform-specific behaviour. The standard specifies the interface. The implementation handles the complexity. The same separation applies to TLS.

### 9.2 "But Mandating an Engine Creates Vendor Lock-In"

This paper does not mandate an engine. The engine is implementation-defined. Implementations are free to use OpenSSL, WolfSSL, BoringSSL, SChannel, Secure Transport, or any engine that satisfies the interface requirements. Platform vendors use the platform engine. Linux distributions use the distribution's OpenSSL. Embedded vendors use the engine their hardware supports.

No lock-in. The interface is the contract. The engine is the implementation detail.

### 9.3 "But Certificate Management Is OS-Specific"

It is. That is why `set_default_verify_paths()` exists and why it is implementation-defined. The function means "load the system trust store." What "the system trust store" is depends on the system. On Linux, it is a directory of PEM files. On macOS, it is the Keychain. On Windows, it is the certificate store. The implementation knows which platform it runs on. The application does not need to.

The file-based certificate loading functions (`use_certificate_file`, `use_private_key_file`, `use_certificate_chain_file`) are portable. PEM and DER are platform-independent formats. The system trust store integration is platform-specific and implementation-defined. The split is deliberate.

### 9.4 "But Post-Quantum Cryptography Will Change Everything"

Post-quantum cryptography will change the algorithms inside the handshake and the record protocol. It will not change the wrapper API. The handshake will still be initiated by calling `handshake()`. Encrypted bytes will still be read by calling `read_some()`. The configuration object will gain new options for post-quantum cipher suites and hybrid key exchange. The four operations will remain the same.

TLS 1.3 already demonstrates this. The cipher suite model changed fundamentally between TLS 1.2 and TLS 1.3. The wrapper API did not change. Post-quantum TLS will follow the same pattern: new algorithms, same wrapper.

The NIST post-quantum standards (ML-KEM, ML-DSA, SLH-DSA) are engine-level changes. They are precisely the kind of change that the implementation-defined engine model is designed to absorb. The engine is updated. The standard library binary picks up the update. No change to the interface. No change to user code.

---

## 10. Deferrals

Five features are deferred from this paper. Each is named so the scope is unambiguous.

### 10.1 DTLS

Datagram Transport Layer Security provides TLS semantics over UDP. The wrapper API shape is similar but not identical - DTLS must handle packet reordering, retransmission, and MTU discovery. A `dtls_stream` is a natural future addition once the datagram socket vocabulary (Paper 13, UDP) is established.

### 10.2 Custom Cipher Suites

Selecting specific cipher suites is a deployment concern, not a specification concern. The implementation-defined engine provides the available cipher suites. The application selects from among them. A future revision may add `set_cipher_list()` or an equivalent; this paper does not.

### 10.3 Certificate Pinning

Certificate pinning restricts which certificates are accepted for a given host beyond what the trust store provides. It is a defence-in-depth mechanism used by mobile applications and high-security services. The mechanism is orthogonal to the core TLS wrapper and is deferred.

### 10.4 OCSP Stapling

Online Certificate Status Protocol stapling allows the server to include a signed certificate status response in the handshake, eliminating the client's need to contact the CA's OCSP responder. It is an optimization and a privacy improvement. The mechanism is implementation-defined in practice (the engine handles it), and explicit API support is deferred.

### 10.5 Post-Quantum Algorithm Selection

Explicit API for selecting post-quantum key exchange algorithms (ML-KEM, X-Wing) and signature algorithms (ML-DSA, SLH-DSA) is deferred until the NIST standards are finalised and deployed in production engines. The implementation-defined engine model means implementations can support post-quantum algorithms without API changes - the engine negotiates the algorithms during the handshake.

---

## 11. Why Now

### 11.1 The Timeline

| Year | Event                                                                              |
| ---- | ---------------------------------------------------------------------------------- |
| 1996 | SSLv3 establishes the context-plus-stream wrapper shape<sup>[9]</sup>              |
| 1999 | Java ships `SSLSocket`<sup>[10]</sup>                                              |
| 2004 | Python ships `ssl`<sup>[11]</sup>                                                  |
| 2005 | .NET ships `SslStream`<sup>[12]</sup>; Asio ships `ssl::stream`<sup>[8]</sup>      |
| 2012 | Go ships `crypto/tls`<sup>[13]</sup>                                               |
| 2016 | Rust `rustls` first release                                                        |
| 2018 | TLS 1.3 published (RFC 8446); wrapper APIs unchanged                               |
| 2024 | NIST post-quantum standards finalised; wrapper APIs unchanged                      |
| 2026 | C++ still has no TLS wrapper in the standard library                               |

Thirty years of convergence. Seven ecosystems. Zero API instability. The standard is not early. The standard is late.

### 11.2 The Series Context

This paper is Paper 14 - the final paper in the Network Endeavor series. The series builds from the bottom: execution model (Paper 1), buffer vocabulary (Papers 4-5), stream concepts (Paper 6), platform I/O (Papers 8-14). TLS sits at the top of the stack because it depends on streams and because it is the last piece needed for a complete networking facility.

A C++ networking library without TLS is a networking library that cannot connect to the modern internet. Papers 1-13 deliver the vocabulary, the transports, and the protocols. Paper 14 delivers the security layer that makes them usable in production.

---

## 12. Closing

The shape is thirty years old. Every language has it. C++ does not. The interface is stable. The implementation is the engine's problem. We built this. It ships in Corosio with two engines today. We are reporting what we found.

Proposed wording for the vocabulary documented here lives in the companion *TLS*<sup>[1]</sup>.

---

## Appendix A. `<std::io>` Synopsis (TLS)

```cpp
namespace std::io {

  enum class tls_method { tlsv12, tlsv13 };
  enum class handshake_type { client, server };
  enum class verify_mode : unsigned {
    none                 = 0,
    peer                 = 1,
    fail_if_no_peer_cert = 2
  };
  enum class file_format { pem, asn1 };

  constexpr verify_mode operator|(
      verify_mode, verify_mode);
  constexpr verify_mode operator&(
      verify_mode, verify_mode);

  class tls_context
  {
  public:
    explicit tls_context(tls_method method);

    tls_context(tls_context&&) noexcept;
    tls_context& operator=(tls_context&&) noexcept;
    ~tls_context();

    tls_context(tls_context const&) = delete;
    tls_context& operator=(
        tls_context const&) = delete;

    void use_certificate_file(
        std::filesystem::path const& p,
        file_format fmt);
    void use_private_key_file(
        std::filesystem::path const& p,
        file_format fmt);
    void use_certificate_chain_file(
        std::filesystem::path const& p);

    void set_default_verify_paths();
    void set_verify_mode(verify_mode mode);
  };

  template<Stream NextLayer>
  class tls_stream
  {
  public:
    tls_stream(NextLayer&& next, tls_context& ctx);

    tls_stream(tls_stream&&) noexcept;
    tls_stream& operator=(tls_stream&&) noexcept;
    ~tls_stream();

    tls_stream(tls_stream const&) = delete;
    tls_stream& operator=(
        tls_stream const&) = delete;

    IoAwaitable auto handshake(handshake_type type);

    IoAwaitable auto read_some(
        MutableBufferSequence auto const& buffers);
    IoAwaitable auto write_some(
        ConstBufferSequence auto const& buffers);

    IoAwaitable auto shutdown();

    NextLayer& next_layer() noexcept;
    NextLayer const& next_layer() const noexcept;
  };

}
```

---

## Appendix B. Corosio Headers

The TLS vocabulary ships in the following headers in [Corosio](https://github.com/cppalliance/corosio)<sup>[6]</sup>. The list is a pointer to the implementation for the reader who wants to inspect it.

| Header                                  | Provides                                      |
| --------------------------------------- | --------------------------------------------- |
| `corosio/ssl/context.hpp`              | `tls_context`, `tls_method`, `verify_mode`, `file_format` |
| `corosio/ssl/stream.hpp`              | `tls_stream<NextLayer>`, `handshake_type`     |

Both headers are backend-agnostic. The backend selection (OpenSSL or WolfSSL) is a build-time configuration. User code includes the same headers regardless of backend.

---

## Acknowledgments

Christopher Kohlhoff designed Asio's `ssl::context` and `ssl::stream` - the production TLS wrapper that this proposal builds on. Twenty years of deployment in [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[8]</sup> established the context-plus-stream shape as the C++ TLS API.

Mohammad Nejati implemented the Corosio TLS backend across OpenSSL and WolfSSL, proving that one wrapper API spans multiple engines without source changes.

The OpenSSL project, the WolfSSL project, and the platform TLS teams at Microsoft, Apple, and Google maintain the engines that make the implementation-defined model viable.

---

## References

[1] *TLS* (Vinnie Falco, 2026). Companion ask paper. D0027R0.

[2] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[3] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[4] [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[5] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[6] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[7] [Boost.Beast](https://github.com/boostorg/beast) - HTTP and WebSocket built on Boost.Asio (Vinnie Falco, 2017-2026).

[8] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - ssl::context and ssl::stream (Christopher Kohlhoff, 2003-2026).

[9] [SSL 3.0 Specification](https://datatracker.ietf.org/doc/html/rfc6101) - "The Secure Sockets Layer (SSL) Protocol Version 3.0" (Alan Freier, Philip Karlton, Paul Kocher, 1996).

[10] [Java SSLSocket](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/net/ssl/SSLSocket.html) - `javax.net.ssl.SSLSocket` (Oracle, 1999-2026).

[11] [Python ssl module](https://docs.python.org/3/library/ssl.html) - `ssl.SSLContext`, `ssl.SSLSocket` (Python Software Foundation, 2004-2026).

[12] [.NET SslStream](https://learn.microsoft.com/en-us/dotnet/api/system.net.security.sslstream) - `System.Net.Security.SslStream` (Microsoft, 2005-2026).

[13] [Go crypto/tls](https://pkg.go.dev/crypto/tls) - `tls.Config`, `tls.Conn` (The Go Authors, 2012-2026).

[14] *Stream Concepts* (Vinnie Falco, 2026). Ask paper for coroutine stream concepts. D0011R0.

[15] *Stream Concepts: Design Rationale* (Vinnie Falco, 2026). Design paper for coroutine stream concepts. D0012R0.
