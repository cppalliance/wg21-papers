---
title: "What C++20 Coroutines Already Buy The Standard"
document: P4088R2
date: 2026-07-01
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
  - "C++ Alliance Proposal Team"
---

## Abstract

C++20 shipped coroutines as a language-level asynchronous model.

C++26 also ships senders. Each model provides properties the other cannot replicate at zero per-operation cost. Two of those properties matter specifically for serial stream I/O: zero-cost iteration in stream loops, and the immediately-ready fast path that skips suspension when data is already buffered. This paper documents both properties, traces their structural origin to the coroutine frame, states the price coroutines pay, and places the evidence beside the sender model's corresponding path.

---

## Revision History

### R2: July 2026 (post-Brno mailing)

- Restructured around two focal arguments: stream-loop iteration efficiency and the immediately-ready fast path.
- Added full-pipeline composition comparison (coroutine loop vs sender `repeat_effect`).
- Added `await_ready` trade-off analysis, acknowledging initial-suspension-by-design as a sender strength.
- Acknowledged sequence senders as future work; documented current status.
- Fixed tutorial oversimplification in Section 2.1.
- Fixed `std::regex` ABI claim in Section 9.5.
- Expanded compound result claim to trilemma framing in Section 9.7.
- Added compilation cost discussion for sender template depth in Section 5.
- Moved Design Fork earlier in the paper (Section 5, was Section 10).
- Condensed history sections into Section 6.
- Disclosure reordered to canonical slot sequence.

### R1: May 2026 (pre-Brno mailing)

- Corrected N1925 attribution (Gerhard Wesp, not Kohlhoff).
- Corrected `when_all` description (concurrent joins, not sequential statements).
- Corrected St. Louis meeting date (July 2024).
- Formatting corrections.

### R0: April 2026 (post-Croydon mailing)

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup>, a coroutine I/O primitives library, and [Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup>, a coroutine-native networking library, both under the C++ Alliance.

This paper is part of the [Network Endeavor](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf) ([P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf)<sup>[1]</sup>), a project to bring coroutine-native I/O to C++. Thirteen papers document the technical case, the retrospective record, and the bridge to `std::execution`.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

Coroutine-native I/O cannot express compile-time work graphs. The coroutine frame is an optimization barrier that prevents full pipeline visibility. These are genuine limitations the sender model does not share.

This paper asks for nothing.

---

## 2. Two Models Already Ship

C++26 ships two async models: coroutines and senders. Both are in the standard. Both address asynchronous programming. Each makes a different trade-off at the point where the caller meets the operation.

### 2.1 Three Keywords

Coroutine I/O is not a new programming model. It is `for`, `if`, `while`, `break`, `return`, structured bindings - the language the programmer already writes. Three keywords are new: `co_await`, `co_return`, `co_yield`.

The coroutine "tutorial" is: Write regular code, put `co_await` before async operations. Two caveats apply. The function must return a type whose `promise_type` supports the awaitable protocol - `task<T>`, `io_task<T>`, or another coroutine return type. Non-coroutine callers cannot use `co_await` and must manage the coroutine's lifetime through the returned object.

### 2.2 Thirty Algorithms

The sender model provides library equivalents for these constructs: `let_value` for local variables, `then` for function calls, `upon_error` for `catch`, `when_all` for concurrent joins, `repeat_effect_until` for `for`. [P4014R2](https://isocpp.org/files/papers/P4014R2.pdf)<sup>[4]</sup>, a progressive tutorial of all thirty sender algorithms in C++26, documents the equivalences.

| Model      | New vocabulary |
| ---------- | -------------- |
| Coroutines | `co_await`, `co_return`, `co_yield` |
| Senders    | `just`, `just_error`, `just_stopped`, `sync_wait`, `then`, `upon_error`, `upon_stopped`, `let_value`, `let_error`, `let_stopped`, `schedule`, `starts_on`, `continues_on`, `on`, `affine`, `schedule_from`, `read_env`, `write_env`, `unstoppable`, `when_all`, `when_all_with_variant`, `into_variant`, `stopped_as_optional`, `stopped_as_error`, `bulk`, `bulk_chunked`, `bulk_unchunked`, `associate`, `spawn_future` |

### 2.3 The Standard Ships Both

[P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[5]</sup> "Add a Coroutine Task Type" Section 9.4.1 [task.overview] defines the result:

> "The `task` class template represents a sender that can be used as the return type of coroutines."

`std::execution::task` is a coroutine that is also a sender.

On September 28, 2021, the Executors telecon polled ([P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[6]</sup> "2021 October Library Evolution Poll Outcomes"):

> "We believe we need one grand unified model for asynchronous execution in the C++ Standard Library, that covers structured concurrency, event based programming, active patterns, etc."
>
> SF:4 / WF:9 / N:5 / WA:5 / SA:1 - No consensus (leaning in favor).

The poll did not reach consensus. The working draft ships both models.

### 2.4 The Chronology

C++20 was ratified in 2020 with coroutines as a language feature. Every major compiler implements them. Production codebases have used them for six years. `std::execution` was adopted into the working draft at St. Louis in July 2024<sup>[7]</sup> and ships in C++26. Networking has been proposed since [N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf)<sup>[8]</sup> (2005) and is not in the standard.

### 2.5 The Incumbent

Three execution models complement each other in C++26: parallel algorithms with execution policies, `std::execution` with sender/receiver composition, and coroutines with `co_await`. Execution policies annotate synchronous calls with parallelism. Senders compose asynchronous work graphs. Coroutines suspend and resume sequential code. The committee accepted complementary execution models when it shipped all three.

`std::sort(std::execution::par, first, last)` does not use senders. [P2500R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2500r2.html)<sup>[10]</sup> "C++ parallel algorithms and P2300", the only paper that attempts a bridge between execution policies and senders, has not been revised since October 2023, was never adopted, and leaves the customization mechanism unspecified.

Coroutine-native I/O does not introduce a fourth model. It completes the third. C++20 gave the committee `co_await`, `coroutine_handle<>`, and `promise_type`. It did not give the committee standard I/O operations that use them. The question is what happens when you build I/O on the model the language already provides.

---

## 3. What Senders Buy

The sender/receiver model is an achievement.

Eric Niebler described the philosophical foundation in 2020<sup>[11]</sup>:

> "It brings the Modern C++ style to our async programs by making async lifetimes correspond to ordinary C++ lexical scopes, eliminating the need for reference counting to manage object lifetime."

Child operations complete before their parents. Lexical scopes govern async lifetimes. The same discipline that makes synchronous C++ safe - RAII, deterministic destruction, nested scopes - extends to asynchronous code.

The practical motivation is equally clear. Niebler wrote in 2024<sup>[12]</sup>:

> "There's nothing wrong with the callback API. What's wrong is that every library that exposes asynchrony uses a slightly different callback API. If you want to chain two async operations from two different libraries, you're going to need to write a bunch of glue code to map this async abstraction to that async abstraction. It's the Tower of Babel problem."

One standard async abstraction solves the interoperability problem. Senders provide the common vocabulary.

Senders and coroutines are not either/or. Niebler framed this directly<sup>[12]</sup>:

> "If your library exposes asynchrony, then returning a sender is a great choice: your users can await the sender in a coroutine if they like, or they can avoid the coroutine frame allocation and use the sender with a generic algorithm like `then()` or `when_all()`. The lack of allocations makes senders an especially good choice for embedded developers."

The sender model provides zero-allocation pipelines through a specific design choice: `connect(sender, receiver)` produces an operation state that aggregates all data before `start()` is called. Niebler described the consequence<sup>[12]</sup>:

> "That means we can launch lots of async work with complex dependencies with only a single dynamic allocation or, in some cases, no allocations at all."

Separating construction from launch lets the pipeline aggregate all state before any work starts. The optimizer sees the full pipeline. The operation state is parameterized on the receiver type, so the compiler knows the complete type at every stage.

Senders also provide completion signatures as type-level contracts. A type mismatch between pipeline stages is a compile error. The three-channel model - `set_value`, `set_error`, `set_stopped` - routes results by channel, and generic algorithms like `retry`, `when_all`, and `upon_error` dispatch on the channel without knowing the concrete sender type.

These are deployed at scale. [P2470R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2470r0.pdf)<sup>[13]</sup> "Slides for presentation of P2300R2" documented the deployments: Facebook ("monthly users number in the billions"), NVIDIA ("fully invested in P2300... we plan to ship in production"), and Bloomberg (experimentation). GPU dispatch, infrastructure, HPC - the domains where compile-time work graphs, zero-allocation pipelines, and heterogeneous composition deliver their full value.

---

## 4. What Coroutines Pay

Coroutines are not free. Three costs are irreducible.

**Frame allocation.** When a function becomes a coroutine, the compiler moves everything that would normally live on the stack - local variables, function parameters, suspension point, awaitable machinery - into a heap-allocated coroutine frame. Every coroutine that suspends allocates this frame through `operator new`. The caller cannot `sizeof` it, cannot stack-allocate it, cannot embed it in a struct. HALO ([P0981R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0981r0.html)<sup>[14]</sup> "Halo: coroutine Heap Allocation eLision Optimization") can elide the allocation when the compiler proves the frame's lifetime is bounded by the caller's scope, but no compiler guarantees HALO. The recycling allocator ([recycling_memory_resource](https://github.com/cppalliance/capy/blob/p4088r0/include/boost/capy/ex/recycling_memory_resource.hpp)<sup>[2]</sup>) amortizes the cost to a thread-local pool lookup - nanoseconds instead of microseconds - but the allocation still happens. Senders do not pay this cost. Sender operation states can be stack-allocated or embedded in the parent's operation state.

**Opaque resume.** The compiler cannot see through `std::coroutine_handle<>::resume()`. Every suspension point is an optimization barrier. The optimizer cannot inline across it. In tight inner loops this is measurable. Senders do not pay this cost. Sender operation states are fully visible to the optimizer within a pipeline.

**Reference lifetime hazard.** Coroutine parameters are copied into the frame at the call site, but references are copied as references, not as values. A `const std::string&` parameter stores the reference in the frame. If the caller's string goes out of scope before the first suspension point, the reference dangles. Google built `Co<T>` as immovable and prvalue-only specifically to prevent it ([P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html)<sup>[15]</sup> "Concerns about the design of `std::execution::task`"). Senders do not share this hazard in the same way - the operation state owns copies of everything passed through `connect`.

At the baseline, the price does not make coroutines slower. A [benchmark](https://github.com/sgerbino/capy/tree/pr/beman-bench/bench/beman)<sup>[16]</sup> of 100,000,000 `read_some` calls on concrete streams measures both models at ~30-31 ns/op with zero allocations. The frame allocation is a cost that buys something. It is not a cost that slows you down.

A coroutine that does fifty reads pays one frame allocation and fifty zero-cost resumptions. The frame the compiler already built holds the operation state, the local variables, and the result. The type erasure that blocks inlining is the same type erasure that gives you `any_stream`, `task<T>` with one parameter, and non-template operation states. Sections 7, 8, and 9 document what the frame buys.

---

## 5. The Design Fork

Six objections to the coroutine-native model are well-known. Every one is conceded.

1. Every coroutine that suspends pays a heap allocation. Senders do not.
2. `coroutine_handle<>::resume()` is an optimization barrier. Senders give the optimizer full pipeline visibility.
3. References captured in the coroutine frame can dangle. Sender operation states own copies.
4. Coroutines do not provide compile-time work graphs, static completion signature checking, or heterogeneous child composition.
5. Coroutines do not provide the generic sender composition algebra - `retry`, `upon_error`, `let_value` as reusable channel-routing adapters.
6. Two async models in the standard library are harder to teach and maintain than one.

These are real costs. Each model provides something in return. The fork is one design choice:

<table>
<tr><th>Awaitable</th><th>Sender</th></tr>
<tr>
<td><pre><code>struct read_awaitable
{
    bool await_ready();
    void await_suspend(
        std::coroutine_handle&lt;&gt; h);
        // caller erased
    io_result&lt;size_t&gt;
        await_resume();
};</code></pre></td>
<td><pre><code>template&lt;class Receiver&gt;
struct read_operation
{
    Receiver rcvr_;
        // caller stamped in
    void start() noexcept;
};</code></pre></td>
</tr>
</table>

`coroutine_handle<>` erases the caller. `connect(sender, receiver)` stamps the caller into the operation state. The `<>` is the fork. Everything that follows in Sections 7 through 9 traces from this difference.

When a coroutine `co_await`s an awaitable, the awaitable's `await_suspend` receives `std::coroutine_handle<>` - a type-erased handle. The awaitable does not know the caller's return type, promise type, local variables, or resumption point. The caller's entire identity is behind an opaque pointer. The I/O operation's state does not depend on who is waiting for it. A `read_op` struct is the same whether the caller is `task<int>`, `task<void>`, or any other coroutine type.

`std::function` erases a callable. `coroutine_handle<>` erases a resumable. One is a library convention that allocates its own storage. The other is a language primitive that points to a frame the compiler already built.

In the sender model, `connect(sender, receiver)` stamps the receiver's type into the operation state. The optimizer sees the full pipeline - it can inline across operation boundaries, eliminate dead code, and propagate constants through the entire chain. That visibility is the strength for GPU pipelines (Section 3). The cost is that the I/O operation's state depends on who is waiting for it. The same `async_read` connected to two different receivers produces two different operation state types.

Each choice unlocks a different set of strengths:

| Senders | Coroutines |
| ------- | ---------- |
| Full pipeline visibility to optimizer | Type-erased streams at zero per-op cost |
| Zero-allocation composition | Concrete, non-template operation states |
| Compile-time work graphs | Operation state lives in the I/O object |
| Static completion signature checking | Separate compilation of I/O algorithms |
| Heterogeneous child composition | ABI stability across transport changes |
| Generic composition algebra | Compound result preservation (ec + n) |

Both companions provide structured concurrency (`when_all`, `when_any`), stop token propagation, non-exception error channels, and production deployment at scale. The bridge crossing cost is ~10-14 ns with zero allocations ([P4092R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r0.pdf)<sup>[25]</sup>, [P4093R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r0.pdf)<sup>[26]</sup>).

At zero per-operation cost, the two property sets are mutually exclusive consequences of the design fork. Senders can achieve type erasure by heap-allocating the operation state. Coroutines can achieve partial pipeline visibility when HALO fires. Neither achieves both property sets without cost. The sender strengths cluster around parallel and heterogeneous dispatch. The coroutine strengths cluster around serial stream I/O. The complementary specializations follow from the design fork the committee already shipped.

The receiver-parameterized operation state carries a compilation cost. The stdexec reference implementation requires template instantiation depth 150-229 for a hello-world sender pipeline (Clang 17, [stdexec issue #1276](https://github.com/NVIDIA/stdexec/issues/1276)). Sean Baxter (Circle) reported that swapping one constraint in the `sender` concept produced a 5,500-line Clang error diagnostic and an internal compiler error ([stdexec issue #856](https://github.com/NVIDIA/stdexec/issues/856)). Chuanqi Xu (Alibaba) observed that every `then` in a chain creates a new symbol, producing symbol table and code size growth that declined after switching to coroutines. No wall-clock compile-time benchmark comparing coroutine and sender pipelines exists. The template depth numbers are structural - they follow from the receiver parameterization that gives the optimizer full pipeline visibility. The visibility is the benefit that the depth purchases.

---

## 6. The Contract

The committee has been trying to standardize networking since [N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf)<sup>[8]</sup> (2005). The contract that every attempt has been built on comes from Asio. This section traces the contract from its original form to its C++20 concept and identifies what changed.

The [Boost.Asio documentation](https://www.boost.org/doc/libs/1_87_0/doc/html/boost_asio/reference/AsyncReadStream.html)<sup>[17]</sup> defines `AsyncReadStream` as a named requirement with two operations: `get_executor()` and `async_read_some(mb, t)`, where `t` is a completion token determining the async model and the result has completion signature `void(error_code ec, size_t n)`. Two operations. Twenty years. The contract has not changed.

[ReadStream](https://github.com/cppalliance/capy/blob/p4088r0/include/boost/capy/concept/read_stream.hpp)<sup>[2]</sup> formalizes the same contract as a C++20 concept:

```cpp
template<typename T>
concept ReadStream =
    requires(T& stream,
             mutable_buffer_archetype buffers)
    {
        { stream.read_some(buffers) }
            -> IoAwaitable;
        requires awaitable_decomposes_to<
            decltype(stream.read_some(buffers)),
            std::error_code, std::size_t>;
    };
```

`read_some` takes a buffer. The result satisfies `IoAwaitable`. The result decomposes to `(error_code, size_t)` via structured bindings. Nine lines. Twenty years of contract, nine lines of concept.

Two things vanished. The completion token disappeared - in the coroutine model, the coroutine is the completion mechanism, so the token that selects among callbacks, futures, and use_awaitable serves no purpose. `get_executor()` disappeared entirely - I/O objects do not carry executors, and the caller provides the executor through `io_env` at `await_suspend` time, resolving Asio's long-standing confusion where the I/O object has one executor and the completion token has another.

What stayed: `read_some` takes a buffer, returns `(error_code, size_t)`. The named requirement became a concept. The language caught up to the contract.

Networking stalled because networking is not the hard problem. Asynchrony is the hard problem, and asynchrony has three domains: bulk-parallel execution, heterogeneous work-graph composition, and serial stream I/O. C++17 standardized the first. C++26 standardized the second. The serial I/O domain - networking, files, pipes, TLS - has no standard facility. C++26 ships three execution models.

---

## 7. The Stream Loop

Stream I/O is inherently iterative. TLS decrypts by looping encrypted reads. HTTP sequences header parsing with body reads. Protocol implementations - SMTP, DNS, WebSocket, QUIC - are loops over `read_some`. The cost model of that loop determines I/O throughput at scale. The two protocols produce different per-iteration cost structures.

### 7.1 The Mechanism

A stream read loop in a coroutine:

```cpp
// Coroutine loop (Capy, ReadStream concept)
for (;;) {
    auto [ec, n] = co_await stream.read_some(buf);
    if (ec)
        break;
    process(buf, n);
}
```

The coroutine frame is allocated once, before the first iteration. Every subsequent `co_await` reuses the same frame. The awaitable returned by `read_some` stores its state inside the socket (Section 9.2) - not allocated per call. The loop has the cost structure of a `while` loop with a function call.

Under the sender model, a stream read loop requires `repeat_effect` or equivalent iteration. Each iteration calls `connect(sender, receiver)`, constructing an operation state whose type depends on both the sender and the receiver. `start` launches the work. When the work completes, `set_value` fires on the receiver, and the next iteration begins. Each iteration independently executes the connect/start/complete protocol sequence.

| Per iteration | Coroutine loop | Sender loop |
| ------------- | -------------- | ----------- |
| Frame allocations | 0 | 0 (shared with outer task) |
| Operation state constructions | 0 | 1 |
| Receiver instantiations | 0 | 1 |
| `connect` calls | 0 | 1 |
| `start` calls | 0 | 1 |

The asymmetry is structural. The coroutine frame persists across iterations because the language defines it that way - a coroutine's locals survive across suspension points. The sender model constructs a fresh operation state per iteration because the operation state's type depends on the receiver, and each iteration is a new `connect`.

### 7.2 The Full Pipeline

Real I/O is layered. A network read passes through tcp -> tls -> decompress -> parse. Each layer is a coroutine composing the layer below through `co_await`. The pipeline shares one frame per layer.

[P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[32]</sup> "Awaitables And Senders For Synchronous I/O" Section 11 quantifies the composed I/O cost. A 64 KB read with a 4 KB kernel buffer produces sixteen iterations of `read_some`. Under the awaitable model, when the buffer already contains decrypted data, `await_ready()` returns `true` and no suspension occurs. The loop runs with the same cost as a hand-written `while` loop calling `memcpy`. Under the sender model, each of those sixteen iterations executes the seven-step protocol sequence documented in [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[32]</sup> Section 6: Construct operation state, instantiate receiver, suspend coroutine, call `start`, fire `set_value`, emplace into `variant`, resume coroutine.

TLS is the canonical amplifier. One network read fills a 16 KB TLS record. A 4 KB application buffer reads four times from that record. Three of those four reads are synchronous - the data is already decrypted in memory. Under awaitables, three of four reads pay zero protocol cost. Under senders, all four execute the full protocol sequence. The multiplier compounds across protocol layers: HTTP over TLS over TCP is three layers of composed coroutines, each with its own `read_some` loop.

### 7.3 Honest Limits

A sender can handle multiple iterations within a single functor. A `then` handler that processes all buffered data before returning concedes zero per-iteration cost to the coroutine model. Hybrid code at that boundary shares the coroutine's cost structure.

When the compiler has full type visibility - no type erasure, concrete sender and receiver types - the per-iteration protocol steps (operation state construction, receiver instantiation, connect, start) may compile to near-zero overhead. The irreducible cost appears under type erasure (Section 9.3) and at the `await_ready` boundary (Section 8), where the structural gap persists regardless of optimization.

Sequence senders - an extension to the sender model for multi-shot, streaming operations - would address the iteration problem directly. Kirk Shoop proposed the abstraction in an August 2019 reflector post. Seven years later, no P-number paper exists. A prototype lives on the `kirkshoop/libunifex` branch `sequenceconnect`, not on stdexec. An experimental API under the `exec::` namespace exists in stdexec, using `subscribe`/`set_next` semantics, with a known bug: Stop token propagation fails for type-erased sequence senders ([stdexec issue #1668](https://github.com/NVIDIA/stdexec/issues/1668)). `split`, the sender model's only multi-shot mechanism in the C++26 standard, was removed at Croydon (P3682R0<sup>[34]</sup>). The coroutine loop is available today.

The coroutine frame persists across all iterations. The sender protocol constructs a fresh operation state for each one.

---

## 8. The Fast Path

The second property coroutines provide for serial I/O is the immediately-ready fast path. When I/O data is already in memory, the awaitable protocol skips suspension entirely. The sender protocol does not. The difference is structural and precisely measurable.

### 8.1 The Mechanism

The awaitable protocol begins every `co_await` with a question: Is the result already available?

```cpp
struct immediate
{
    bool await_ready() const noexcept
    {
        return true;
    }
    void await_suspend(
        std::coroutine_handle<>,
        io_env const*) noexcept {}
    void await_resume() noexcept {}
};
```

When `await_ready()` returns `true`, the coroutine does not suspend. No register spill. No coroutine handle manipulation. No atomic exchange. The value is extracted directly through `await_resume()`. Three protocol steps total: `await_ready`, `await_resume`, done. [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[32]</sup> Section 7 traces the full protocol path.

A memory buffer, a test mock, a zlib decompressor reading from an already-decrypted TLS record, a base64 decoder operating on in-memory data - each satisfies `ReadStream` by returning immediately-ready awaitables. The same `dump` function from Section 9.4 works whether the stream suspends for kernel I/O or returns instantly from a buffer. The algorithm does not know the difference. No `is_async` flag. No separate sync API. One abstraction covers both.

### 8.2 The Trade-Off

The sender model's initial-suspension-by-design is a genuine architectural strength. No work runs until `start()` is called. The pipeline is fully constructed before any computation begins. Niebler described the consequence in 2024<sup>[12]</sup>:

> "separating the launch of the work from the construction of the operation state lets us aggregate lots of operation states into one"

Piecewise graph construction, compile-time work aggregation, and zero-allocation composition all depend on this property. GPU dispatch (Section 3) builds entire work graphs before launching any kernel. Domain customization via `transform_sender` retargets the same graph to CPU or GPU by swapping the scheduler. The separation between construction and launch is what makes senders the right choice for heterogeneous composition.

The cost appears at I/O boundaries. When the data is already buffered and the operation completes synchronously, the sender protocol still constructs an operation state, wires a receiver, calls `start`, routes through `set_value`, and resumes through the coroutine handle. [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[32]</sup> Section 6 documents the full sequence: seven protocol steps for an operation that completes synchronously.

### 8.3 Why I/O Benefits

Network I/O frequently has data already buffered. TLS decryption reads an entire record (up to 16 KB) from the network in one syscall. Application-level reads from the decrypted buffer are synchronous until the buffer drains. HTTP header parsing reads buffered bytes until a delimiter. DNS cache lookups return cached results with no network transition.

[P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[32]</sup> Section 11 quantifies the pattern for composed I/O. A 64 KB read with a 4 KB buffer produces sixteen iterations. On a buffered stream where most completions are synchronous, each synchronous completion executes the seven-step protocol sequence under senders. Under awaitables with `await_ready() == true`, the generic algorithm has the same cost as a hand-written `while` loop calling `memcpy`.

Stepanov's iterator concepts do not impose indirection when dereferencing a pointer. A `T*` satisfies `random_access_iterator` and dereferences in one instruction - the concept does not require constructing an intermediate state object, wiring a callback, or performing a two-phase access protocol. The awaitable protocol has this property. `await_ready() == true` is the pointer dereference: The value is there, take it. `await_ready() == false` is the disk-backed iterator: The value requires work, suspend, resume when ready. The cost tracks the operation, not the protocol.

### 8.4 The Structural Gap

The difference between the two paths is not one context switch. The difference is structural: register spill/reload cycle plus atomic CAS.

When `await_ready()` returns `true`, the coroutine continues inline. The [benchmark](https://github.com/sgerbino/capy/tree/pr/beman-bench/bench/beman)<sup>[16]</sup> measures 1.0 ns per operation on a no-op synchronous stream (20,000,000 operations).

When a sender completes synchronously inside a coroutine consuming it through the `sender-awaitable` path, the coroutine suspends (register spill), `connect` and `start` execute inline, `set_value` fires on the receiver, the receiver stores the result and calls `.resume()` on the coroutine handle (atomic CAS, register reload). The same benchmark measures 2.6 ns per operation with a trampoline scheduler, 5.1 ns with the sender-to-awaitable bridge.

Both stdexec and libunifex unconditionally return `false` from `await_ready` when wrapping senders. The specification requires it: `sender-awaitable::await_ready()` returns `false` ([P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[27]</sup> `[exec.as.awaitable]`). A sender whose `start` calls `set_value` synchronously still triggers suspension and resumption. Repeated inline completions cause unbounded stack growth. The `trampoline_scheduler` is a runtime mitigation. [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf)<sup>[33]</sup> "Symmetric Transfer and Sender Composition" characterizes the overhead:

> "the runtime overhead in the completion path that P0913R1 was specifically adopted to eliminate"

[P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[32]</sup> Section 14 states three falsification criteria - testable conditions that would discharge these observations. No implementation has satisfied any of them.

The awaitable protocol reaches the zero-cost path through `await_ready()`. The sender protocol has no equivalent conditional path.

---

## 9. What The Frame Buys

The coroutine frame paid for in Section 4 is the storage the awaitable protocol reuses. Sections 7 and 8 documented the two focal properties - zero-cost iteration and the immediately-ready fast path. The properties below are the supporting links in the causal chain from frame to library. Each follows from the design fork in Section 5: The caller is erased, so the operation state is concrete. The operation state is concrete, so it lives in the socket. The socket owns the state, so there is no per-operation allocation. No per-operation allocation, so the stream can be type-erased. The type-erased stream compiles once. The compiled stream is ABI-stable. Remove any link and the rest collapse.

### 9.1 The Operation State Is Concrete

Windows (IOCP). [overlapped_op](https://github.com/cppalliance/corosio/blob/p4088r0/include/boost/corosio/native/detail/iocp/win_overlapped_op.hpp)<sup>[3]</sup> and [read_op](https://github.com/cppalliance/corosio/blob/p4088r0/include/boost/corosio/native/detail/iocp/win_socket.hpp)<sup>[3]</sup>:

```cpp
struct overlapped_op : OVERLAPPED
{
    std::coroutine_handle<> h;
    capy::executor_ref      ex;
    std::error_code*        ec_out;
    std::size_t*            bytes_out;
    DWORD                   bytes_transferred;
};

struct read_op : overlapped_op
{
    WSABUF wsabufs[16];
    DWORD  wsabuf_count;
    DWORD  flags;
    win_socket_internal& internal;
};
```

Linux (epoll). [epoll_op.hpp](https://github.com/cppalliance/corosio/blob/p4088r0/include/boost/corosio/native/detail/epoll/epoll_op.hpp)<sup>[3]</sup>:

```cpp
struct epoll_read_op final
    : reactor_read_op<epoll_op> {};

struct epoll_write_op final
    : reactor_write_op<
        epoll_op, epoll_write_policy> {};
```

Not templates. Not parameterized on the caller. Known at library-build time. The same `read_op` serves every coroutine that reads from the socket.

### 9.2 The Operation State Lives in the Socket

[win_socket_internal](https://github.com/cppalliance/corosio/blob/p4088r0/include/boost/corosio/native/detail/iocp/win_socket.hpp)<sup>[3]</sup>:

```cpp
class win_socket_internal
{
    connect_op conn_;
    read_op    rd_;
    write_op   wr_;
    SOCKET     socket_ = INVALID_SOCKET;
    int        family_  = AF_UNSPEC;
};
```

Three operation states. Members of the socket. Pre-allocated when the socket is created. 10,000 sockets means 10,000 `read_op` instances of one known type, allocated once, reused for every read.

### 9.3 Zero Per-Operation Allocation

[any_read_stream](https://github.com/cppalliance/capy/blob/p4088r0/include/boost/capy/io/any_read_stream.hpp)<sup>[2]</sup> type-erases any `ReadStream`. The erasure is on the awaitable, not the stream. The [vtable](https://github.com/cppalliance/capy/blob/p4088r0/include/boost/capy/io/any_read_stream.hpp)<sup>[2]</sup> dispatches `await_ready`, `await_suspend`, `await_resume` through function pointers:

```cpp
struct vtable
{
    void (*construct_awaitable)(
        void*, void*,
        std::span<mutable_buffer const>);
    bool (*await_ready)(void*);
    std::coroutine_handle<> (*await_suspend)(
        void*, std::coroutine_handle<>,
        io_env const*);
    io_result<std::size_t> (*await_resume)(void*);
    void (*destroy_awaitable)(void*) noexcept;
    std::size_t awaitable_size;
    std::size_t awaitable_align;
    void (*destroy)(void*) noexcept;
};
```

The awaitable storage is pre-allocated at construction time and reused for every `read_some` call. One allocation at construction. Zero per-operation.

The [benchmark](https://github.com/sgerbino/capy/tree/pr/beman-bench/bench/beman)<sup>[16]</sup> measures the cost. 100,000,000 `read_some` calls on a single thread, no-op stream, five runs per configuration:

| Stream type  | capy IoAwaitable |       | P2300 sender |       |
| ------------ | ---------------: | ----: | -----------: | ----: |
|              | ns/op            | al/op | ns/op        | al/op |
| Native       | 31.4             | 0     | 30.0         | 0     |
| Abstract     | 32.1             | 0     | 53.5         | 1     |
| Type-erased  | 36.4             | 0     | 53.4         | 1     |

At the native level, both models are equivalent. Under type erasure, awaitables add +5 ns and zero allocations. Senders add +23 ns and one allocation per operation. The cost is structural: `await_suspend` takes a type-erased `coroutine_handle<>`, so the awaitable's size is known at construction time. `connect(receiver)` produces an operation state whose type depends on both the sender and the receiver. When either side is type-erased, the operation state is heap-allocated per operation.

For any individual I/O operation, the +23 ns dispatch difference is negligible - a `read()` syscall costs 1-10 us, and network round-trips cost orders of magnitude more. The difference is infrastructure burden. To eliminate the per-operation allocation, senders need per-connection pools sized for the operation state, threaded through the API, and managed across 10,000 concurrent connections. Coroutines need nothing - the frame is the storage the awaitable already uses. At scale, 10,000 connections at 100 operations per second is 1,000,000 allocations per second that senders must pool or accept.

### 9.4 Compile Once

Because `any_read_stream` has a fixed layout, a function accepting `any_read_stream&` goes in a `.cpp` file:

```cpp
// dump.hpp
#include <boost/capy/task.hpp>
#include <boost/capy/io/any_read_stream.hpp>

capy::task<> dump(capy::any_read_stream& in);
```

```cpp
// dump.cpp
#include "dump.hpp"
#include <boost/capy/buffers.hpp>
#include <iostream>

capy::task<> dump(capy::any_read_stream& in)
{
    char buf[1024];
    for(;;)
    {
        auto [ec, n] = co_await in.read_some(
            capy::mutable_buffer(buf, sizeof buf));
        if(ec)
            break;
        std::cout.write(buf, n);
    }
}
```

The header includes only [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup>. No platform headers. No sockets. The `.cpp` compiles once. Consumers include the header and link. The stream behind `any_read_stream` could be a TCP socket, a TLS session, a file, or a test mock. Nothing recompiles.

The architecture also enables the [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup>/[Corosio](https://github.com/cppalliance/corosio)<sup>[3]</sup> split. Capy delivers the abstract layer: `task<T>`, `any_read_stream`, `any_write_stream`, buffer concepts, stream concepts. Pure C++20. No platform dependency. Corosio delivers the platform layer: `tcp_socket`, `tls_stream`, timers, DNS, signals. One frame. Two libraries. Zero recompilation.

### 9.5 Forty Years of ABI

The vtable layout of `any_read_stream` does not change. Libraries compiled today work with new transports tomorrow. A `tls_stream` implementation compiled against OpenSSL 3.0 satisfies `ReadStream`. A future implementation compiled against a post-quantum TLS library satisfies the same concept, plugs into the same `any_read_stream`, and works with every library compiled against the old transport.

ABI commitments are permanent. The question is whether this vtable will need to change.

The contract behind it:

```
read_some(buffer) -> (error_code, size_t)
```

This is the POSIX `read()` contract with a C++ interface. Six change vectors exist. None breaks it.

- **New buffer types.** The `ReadStream` concept is already generic over buffer type. New buffer representations satisfy the existing concept. The vtable is unaffected.
- **New error conditions.** `std::error_code` is extensible via error categories. QUIC errors, post-quantum TLS errors, io_uring-specific errors - each registers a new category. The return type does not change.
- **New return values.** A read operation takes a buffer and reports how many bytes were transferred and whether an error occurred. No I/O model in any language returns anything else.
- **Cancellation.** Stop tokens propagate through `io_env`, not through the return type. Cancellation does not touch the contract.
- **New I/O patterns.** `read_some` is the primitive. Scatter/gather, vectored I/O, and read-until are composed from `read_some` by algorithms. The primitive does not change because the compositions do.
- **Environment evolution.** `io_env const*` is part of the `await_suspend` signature. If the environment needs new capabilities, the type evolves. The mitigation is pointer indirection: New fields append to the structure without changing the vtable's function signatures. The same evolution model as `OVERLAPPED` on Windows and `iocb` on Linux.

The contract has survived POSIX, BSD sockets, IOCP, Asio, the Networking TS, io_uring, and every transport from TCP to QUIC.

### 9.6 The User Chooses

The user chooses the trade-off. [io_stream](https://github.com/cppalliance/corosio/blob/p4088r0/include/boost/corosio/io/io_stream.hpp)<sup>[3]</sup>, [tcp_socket](https://github.com/cppalliance/corosio/blob/p4088r0/include/boost/corosio/tcp_socket.hpp)<sup>[3]</sup>, [native_tcp_socket](https://github.com/cppalliance/corosio/blob/p4088r0/include/boost/corosio/native/native_tcp_socket.hpp)<sup>[3]</sup>:

```
io_stream                        // abstract (Layer 3)
    |
tcp_socket                       // concrete (Layer 2)
    |
native_tcp_socket<Backend>       // native   (Layer 1)
```

**Abstract** (`io_stream`): virtual dispatch, ABI-stable, separately compiled. Business logic accepts `any_stream&` and never sees a platform header. Maximum compilation speed. The cost is virtual dispatch per I/O operation - nanoseconds against a microsecond syscall.

**Concrete** (`tcp_socket`): protocol-specific API - bind, connect, shutdown - still virtual dispatch, still separately compiled. Application code lives here.

**Native** (`native_tcp_socket<Backend>`): templated on the platform backend. Member function shadowing eliminates the vtable. Full inlining. Zero overhead. Hot paths and benchmarks live here.

Different layers coexist. A library accepts `any_stream&`. An application creates `tcp_socket`. A benchmark uses `native_tcp_socket<epoll>`. All three interoperate through the inheritance chain.

### 9.7 The Frame Subsidizes Everything

The coroutine frame paid for in Section 4 holds the local variables, the suspension point, and the result. `any_read_stream` works without per-operation allocation because the caller's frame already exists. The frame allocation you cannot avoid subsidizes the type erasure you want.

Per-operation allocations by execution model and stream type:

| Stream type  | `capy::task` | `beman::task` | sender pipeline |
| ------------ | -----------: | ------------: | --------------: |
| Native       |            0 |             0 |               0 |
| Abstract     |            0 |             1 |               1 |
| Type-erased  |            0 |             1 |               1 |

Additional properties riding on the same frame:

- **Compile-time domain gate.** The two-argument `await_suspend(coroutine_handle<>, io_env const*)` is a deliberate trade-off. The pointer is the cost. The domain gate is the benefit: Any awaitable that does not accept `io_env const*` is a type error inside an I/O task. Foreign awaitables that do not speak the I/O protocol are rejected by the compiler. [IoAwaitable](https://github.com/cppalliance/capy/blob/p4088r0/include/boost/capy/concept/io_awaitable.hpp)<sup>[2]</sup>.

- **Compound result preservation.** `auto [ec, n] = co_await sock.read_some(buf)`. Both values visible. No channel split. No data loss. The sender model's three-channel completion model routes results by channel. [P4090R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4090r0.pdf)<sup>[20]</sup> "Sender I/O: A Constructed Comparison" and [P4091R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4091r0.pdf)<sup>[21]</sup> "Two Error Models" document a trilemma: Pick two of {preserve all data, use composition algebra, stay generic}. Sending `tuple<error_code, size_t>` through the value channel works physically but bypasses the composition algebra entirely - `when_all` does not cancel siblings on I/O failure, `upon_error` is unreachable, `retry` does not fire. P4090R0 Section 13 issues an open challenge: Construct an echo server that uses the composition algebra for I/O errors while preserving compound results. No such construction exists.

- **Symmetric transfer.** `await_suspend` returns `coroutine_handle<>`. O(1) stack depth regardless of chain length.

- **One-parameter `task<T>`.** [task.hpp](https://github.com/cppalliance/capy/blob/p4088r0/include/boost/capy/task.hpp)<sup>[2]</sup>: `template<typename T = void> struct task`. One parameter. No Environment. The promise carries the environment. [P4089R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4089r0.pdf)<sup>[22]</sup> "On the Diversity of Coroutine Task Types" documents why coroutine task type diversity is both inevitable and desirable.

---

## 10. One Allocation Per Operation

Senders can achieve type-erased I/O. They can get ABI stability. The benchmark in Section 9.3 documents the cost: one allocation per operation, +23 ns. One allocation per read. Completely reasonable.

A custom allocator can pool the operation states. The pool must know each operation state's size at construction time - the size depends on both the sender and the receiver, so the pool is parameterized on the pipeline shape. The pool must be threaded through the API - the I/O object, the connect call, or the execution context must carry it. The pool must be managed per-connection - 10,000 connections means 10,000 pools, each sized for the operation states that connection's pipeline produces.

Small buffer optimization (SBO) is another mitigation. SBO works for `std::function` because callable objects are often small. Sender operation states are not small: The state includes captured data from the sender, the receiver's continuation and environment, and intermediate storage. Under type erasure, the size depends on both the sender and receiver types, neither of which is known at compile time. A fixed SBO buffer must be sized for the worst case or fall back to heap allocation.

The allocation purchased something. The receiver-parameterized operation state gives the optimizer full pipeline visibility - the strength documented in Section 3. That visibility is what makes senders the right choice for GPU dispatch, HPC, and compile-time work graphs. The allocation is the price of stamping the receiver into the operation state when the receiver is type-erased.

The coroutine model provides zero-allocation type erasure as a language consequence. The frame the compiler already built is the storage the awaitable already uses. No pool. No size calculation. No API threading. No per-connection management.

---

## 11. Anticipated Objections

**Q: Why not type-erase senders with `any_sender`?**

A: `any_sender` type-erases the sender, not the receiver. `connect(any_sender, receiver)` still stamps the receiver type into the operation state. The operation state remains a template. `any_sender` erases the sender's identity from the caller. The coroutine model erases the caller's identity from the I/O operation. Section 5 documents the distinction. Section 10 documents the cost.

**Q: Does `std::execution::task` not already bridge both models?**

A: It does. `task` is a coroutine that is also a sender. But serving both models in one type is where the friction originates - two template parameters, open issues documented in [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[23]</sup> "Open Issues in `std::execution::task`", constraints that neither model alone requires. The companion approach accepts the design fork: Each model does what it does best, and bridges connect them at ~10-14 ns with zero allocations. The question is whether the coroutine side carries I/O facilities that exploit the properties `coroutine_handle<>` provides. `task` bridges the models. It does not provide I/O.

**Q: Two async models are harder to teach.**

A: C++ already teaches three execution models: parallel algorithms with execution policies, `std::execution` with sender algorithms, and coroutines with `co_await`. The teachability cost was paid when the committee shipped all three. Coroutine-native I/O does not add a fourth model. It completes the third.

The teachability gap extends beyond the committee. On the `stdexec` issue tracker, a user [reported](https://github.com/NVIDIA/stdexec/issues/1564)<sup>[28]</sup> that `let_error([](int) { ... })` does not compile when the upstream sender can also complete with `std::exception_ptr`. The response: *"This is the design of stdexec."* Jonathan M&uuml;ller [wrote](https://www.think-cell.com/en/career/devblog/trip-report-summer-iso-cpp-meeting-in-st-louis-usa)<sup>[29]</sup>: *"One particular complexity I don't like is the idea of environments."* The derivatives exchange described in [P4125R1](https://isocpp.org/files/papers/P4125R1.pdf)<sup>[31]</sup> reported that the sender/receiver expression syntax caused many mental "trips" when reasoning about behaviour, and did not scale beyond simple examples.

**Q: Sequence senders will solve the stream-loop problem.**

A: Sequence senders, an extension for multi-shot streaming operations, have been forthcoming since Kirk Shoop's August 2019 reflector post. Seven years later, no P-number paper exists. The prototype lives on a libunifex branch, not stdexec. An experimental API under `exec::` exists in stdexec with known bugs. `split`, the sender model's only multi-shot mechanism in C++26, was removed at Croydon (P3682R0<sup>[34]</sup>). The coroutine loop is available today.

**Q: Senders complete synchronously too.**

A: `sender-awaitable::await_ready()` returns `false` unconditionally per the normative specification ([P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[27]</sup> `[exec.as.awaitable]`). Confirmed across implementations: Both stdexec and libunifex return `false`. Repeated inline completions cause unbounded stack growth requiring `trampoline_scheduler` as runtime mitigation (+2.6 ns/op). [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[32]</sup> Section 14 states three falsification criteria that would discharge the observation. None has been met.

**Q: The full-pipeline comparison favors senders because the entire pipeline is one allocation.**

A: A sender pipeline launched on a scope pays one allocation for the pipeline. Each iteration of `repeat_effect` within that pipeline independently pays connect/start/complete. [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[32]</sup> Section 11 documents the per-iteration protocol sequence for a 64 KB read with 4 KB buffer: sixteen iterations, each executing seven protocol steps. The pipeline allocation is shared. The per-iteration protocol cost is not.

**Q: A sender can provide member `as_awaitable` to skip the protocol sequence.**

A: True. `[exec.as.awaitable]` uses a sender's own `as_awaitable` in preference to the generic `sender-awaitable` path. A sender whose `as_awaitable` returns a synchronous awaitable takes the three-step path of Section 8.1 rather than the seven-step path. Two costs remain. The `as_awaitable` member is manual and per-sender - a sender that omits it inherits the seven-step path. And the member is lost under type erasure: `any_sender` erases the concrete sender and the `as_awaitable` member with it.

**Q: Coroutines were not designed for I/O.**

A: Correct. The five mechanisms were designed for generality - async patterns, lazy evaluation, generators. Sections 7 through 9 document what they produce when applied to I/O. The substrate is emergent.

**Q: The domain split is artificial. Senders compose across domains.**

A: C++26 ships three complementary execution models. [P2500R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2500r2.html)<sup>[10]</sup> "C++ parallel algorithms and P2300" has not been revised since October 2023, was never adopted, and leaves the customization mechanism unspecified. `std::sort(std::execution::par, first, last)` does not use senders. The design fork (Section 5) is structural: `coroutine_handle<>` erases the caller, `connect(sender, receiver)` stamps the caller in. The resulting property sets are mutually exclusive at zero per-operation cost. The bridges ([P4092R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r0.pdf)<sup>[25]</sup>, [P4093R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r0.pdf)<sup>[26]</sup>) are how the companions connect.

**Q: If the domains are separate, why do you need bridges?**

A: Different computation models interact at boundaries. C and C++ interact through `extern "C"`. CPU and GPU interact through memory copies. The bridges are evidence of a clean interface between models. The crossing has a cost, and it is the right trade-off.

**Q: P2300 was designed to serve I/O too. Its motivating example is a TCP server.**

A: The motivating example illustrates the trade-off. [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[27]</sup> Section 1.4.1.3 is analyzed in [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[23]</sup> Section 3 and [P4090R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4090r0.pdf)<sup>[20]</sup>. The three-channel completion model routes the byte count and the error code to separate channels. Type erasure requires per-operation allocation because the operation state depends on the receiver. The design properties that produce these characteristics are the same properties that serve parallel and heterogeneous dispatch.

**Q: io_uring's batch submission model favors senders.**

A: The coroutine model does not submit one syscall per `co_await`. The event loop batches submissions from multiple suspended coroutines between `io_uring_enter` calls. The coroutine suspends into the submission queue; the event loop flushes the queue in bulk when it re-enters the kernel. Batching is an event loop implementation detail, invisible to the coroutine.

**Q: This is too much scope for C++29.**

A: [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[24]</sup> "A Minimal Coroutine Execution Model" is two concepts, one executor, and a frame allocator cache. Six pages. The Network Endeavor ([P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf)<sup>[1]</sup>) is modular - each paper stands independently. The team's target is pencils down by December 2028: reviewed, stable proposals with implementation experience.

---

## 12. Conclusion

Two properties of C++20 coroutines matter for serial stream I/O, and neither can be replicated by the sender model at zero per-operation cost.

The first is zero-cost iteration. A coroutine stream loop allocates one frame and reuses it across every iteration. The sender model constructs a fresh operation state per iteration because the receiver is stamped into the type. For a 64 KB buffered TLS read at 4 KB per application read, that is sixteen iterations. The coroutine allocates one frame; the sender protocol constructs sixteen operation states.

The second is the immediately-ready fast path. When data is already in memory, `await_ready()` returns `true` and the coroutine continues without suspension - 1.0 ns per operation. The sender protocol suspends unconditionally - `sender-awaitable::await_ready()` returns `false` per the normative specification - incurring register spill, atomic CAS, and resumption overhead at 2.6-5.1 ns per operation. Both stdexec and libunifex confirm this behavior.

Both properties originate in the same design choice: `coroutine_handle<>` erases the caller. The sender model stamps the caller in. At zero per-operation cost, the two property sets are mutually exclusive. The sender strengths - full pipeline visibility, zero-allocation composition, compile-time work graphs - serve parallel and heterogeneous dispatch. The coroutine strengths - zero-cost iteration, synchronous fast paths, type-erased streams, separate compilation, ABI stability - serve serial stream I/O.

Three independent executor designs - P0443R14's `execute`, P3941R4's infallible scheduler, and P4003R3's coroutine executor - converge on the same continuation-framed shape because the caller is suspended in all three ([P4286R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4286r0.pdf)<sup>[35]</sup> "The Return of Networking TS Executors in P3552"). Convergence from unrelated starting points eliminates the explanation that the shape is an artifact of any one model.

C++20 shipped the language. C++26 shipped `std::execution`. The serial I/O domain has no standard facility. If coroutine-native I/O ships, C++ arrives at three companions - each contributing what the others cannot.

---

## Acknowledgments

The author thanks Chris Kohlhoff for Asio's stream model, buffer sequences, and executor architecture - twenty years of production deployment is the foundation this work builds on; Eric Niebler, Kirk Shoop, Lewis Baker, and their collaborators for `std::execution`; Gor Nishanov for the coroutine model's explicit support for task type diversity; Dietmar K&uuml;hl for `beman::execution` and [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html); Ian Petersen for identifying an asymmetry in an earlier draft and for confirming the equivalence between sender and coroutine dispatch; Ville Voutilainen for the structural feedback that drove this revision - identifying stream-loop iteration efficiency and the immediately-ready fast path as the two strongest arguments, and surfacing the counter-arguments that sharpened both; Jens Maurer for framing the design spectrum; Herb Sutter for identifying the need for tutorials and documentation; Jonathan M&uuml;ller for confirming the symmetric transfer gap in [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html); Peter Dimov for the refined channel mapping; Robert Leahy for the symmetric transfer analysis; Mungo Gill for co-authoring [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf) on symmetric transfer and sender composition; Klemens Morgenstern for Boost.Cobalt and the cross-library bridges; Steve Gerbino for co-developing the constructed comparison, bridge implementations, and Corosio; and Mungo Gill, Mohammad Nejati, and Michael Vandeberg for feedback.

---

## References

[1] [P4100](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf) - "The Network Endeavor: Coroutine-Native I/O for C++29" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[2] [cppalliance/capy](https://github.com/cppalliance/capy) - Coroutine I/O primitives library.

[3] [cppalliance/corosio](https://github.com/cppalliance/corosio) - Coroutine-native networking library.

[4] [P4014R2](https://isocpp.org/files/papers/P4014R2.pdf) - "The Sender Sub-Language For Beginners" (Vinnie Falco, Mungo Gill, 2026).

[5] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[6] [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html) - "2021 October Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[7] [Herb Sutter, "Trip report: Summer ISO C++ standards meeting (St Louis, MO, USA)," 2024](https://herbsutter.com/2024/07/02/trip-report-summer-iso-c-standards-meeting-st-louis-mo-usa/)

[8] [N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf) - "Networking proposal for TR2 (rev. 1)" (Gerhard Wesp, 2005).

[9] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, Michael Wong, 2020).

[10] [P2500R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2500r2.html) - "C++ parallel algorithms and P2300" (Ruslan Arutyunyan, Alexey Kukanov, 2023).

[11] [Eric Niebler, "Structured Concurrency," 2020](https://ericniebler.com/2020/11/08/structured-concurrency/)

[12] [Eric Niebler, "What are Senders Good For, Anyway?" 2024](https://ericniebler.com/2024/02/04/what-are-senders-good-for-anyway/)

[13] [P2470R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2470r0.pdf) - "Slides for presentation of P2300R2" (Eric Niebler, 2021).

[14] [P0981R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0981r0.html) - "Halo: coroutine Heap Allocation eLision Optimization" (Gor Nishanov, 2018).

[15] [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html) - "Concerns about the design of `std::execution::task`" (Jonathan M&uuml;ller, 2025).

[16] [I/O Read Stream Benchmark](https://github.com/sgerbino/capy/tree/pr/beman-bench/bench/beman) - 100M and 20M operation benchmarks on type-erased no-op read streams (Steve Gerbino, 2026).

[17] [Boost.Asio AsyncReadStream requirements](https://www.boost.org/doc/libs/1_87_0/doc/html/boost_asio/reference/AsyncReadStream.html)

[18] [P4094](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r0.pdf) - "Retrospective: The Unification of Executors and P0443" (Vinnie Falco, 2026).

[19] [P4099](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4099r0.pdf) - "Twenty-One Years: The Arc of Networking in C++" (Vinnie Falco, 2026).

[20] [P4090](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4090r0.pdf) - "Sender I/O: A Constructed Comparison" (Vinnie Falco, Steve Gerbino, 2026).

[21] [P4091](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4091r0.pdf) - "Two Error Models" (Vinnie Falco, 2026).

[22] [P4089](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4089r0.pdf) - "On the Diversity of Coroutine Task Types" (Vinnie Falco, 2026).

[23] [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf) - "Open Issues in `std::execution::task`" (Vinnie Falco, Mungo Gill, 2026).

[24] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[25] [P4092](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r0.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[26] [P4093](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r0.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[27] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Eric Niebler, Micha&lstrok; Dominiak, Lewis Baker, Kirk Shoop, Lucian Radu Teodorescu, Lee Howes, 2024).

[28] [NVIDIA/stdexec issue #1564: type issue of let_error](https://github.com/NVIDIA/stdexec/issues/1564) - @taooceros, @BartolomeyKant, July 2025 / March 2026.

[29] [Trip Report: Summer ISO C++ Meeting in St. Louis, USA](https://www.think-cell.com/en/career/devblog/trip-report-summer-iso-cpp-meeting-in-st-louis-usa) - Jonathan M&uuml;ller, July 2024.

[30] [r/cpp: C++ committee polling results for asynchronous programming](https://old.reddit.com/r/cpp/comments/q6tgod/c_committee_polling_results_for_asynchronous/) - Oct 2021.

[31] [P4125R1](https://isocpp.org/files/papers/P4125R1.pdf) - "Coroutine-Native I/O at a Derivatives Exchange" (Mungo Gill, 2026).

[32] [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf) - "Awaitables And Senders For Synchronous I/O" (Vinnie Falco, 2026). Documents the 3-step awaitable vs 7-step sender protocol for synchronous I/O and provides falsification criteria.

[33] [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf) - "Symmetric Transfer and Sender Composition" (Mungo Gill, Vinnie Falco, 2026). Analyzes the trampoline overhead in sender completion paths and documents the runtime cost P0913R1 was adopted to eliminate.

[34] [P3682R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3682r0.pdf) - "Remove std::execution::split" (Robert Leahy, 2025). Adopted at Croydon (March 2026). The sender model's only multi-shot mechanism in the standard was withdrawn.

[35] [P4286R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4286r0.pdf) - "The Return of Networking TS Executors in P3552" (Vinnie Falco, 2026). Documents convergence of three independent executor designs onto the same infallible continuation-framed shape.
