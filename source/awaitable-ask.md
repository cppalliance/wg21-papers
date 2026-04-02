# What We Want for I/O in C++

## 1. The Ask

Two things.

**First**, we want standard I/O operations to return IoAwaitable, the protocol defined in [P4003R0](https://isocpp.org/files/papers/P4003R0.pdf) "Coroutines for I/O."

**Second**, we want [P4126R0](https://isocpp.org/files/papers/P4126R0.pdf) "A Universal Continuation Model" - a mechanism that lets a struct produce a `coroutine_handle` without allocating a coroutine frame. This gives sender/receiver pipelines zero-allocation access to every awaitable ever written.

Together, these two changes make coroutines and senders both first-class citizens of the I/O stack.

## 2. The Numbers

20,000,000 `read_some` calls per cell, single thread, no-op stream. Mean +/- stddev over 5 runs (warmup excluded). **Bold** = native execution model. Col A = awaitable I/O, Col B = sender I/O. al/op counts allocation calls per operation, including recycled allocations. Benchmark source: [github.com/cppalliance/capy/.../bench/beman](https://github.com/cppalliance/capy/tree/develop/bench/beman) [14].

#### Table 1: sender/receiver pipeline

|                | A: awaitable (bridge) |          | B: sender (native)    |          |
|----------------|----------------------:|---------:|----------------------:|---------:|
|                | ns/op                 | al/op    | ns/op                 | al/op    |
| Native         | 46.0 +/- 0.1         | 1        | **32.8 +/- 0.2**     | **0**    |
| Abstract       | 46.0 +/- 0.1         | 1        | **45.1 +/- 0.2**     | **1**    |
| Type-erased    | 55.7 +/- 0.2         | 1        | **57.1 +/- 0.3**     | **1**    |
| Synchronous    | N/A                   |          | N/A                   |          |

#### Table 2: `capy::task`

|                | A: awaitable (native)  |          | B: sender (bridge) |          |
|----------------|-----------------------:|---------:|--------------------:|---------:|
|                | ns/op                  | al/op    | ns/op               | al/op    |
| Native         | **31.4 +/- 0.0**      | **0**    | 48.3 +/- 0.5       | 0        |
| Abstract       | **32.4 +/- 0.4**      | **0**    | 72.1 +/- 0.1       | 1        |
| Type-erased    | **36.3 +/- 0.0**      | **0**    | 72.3 +/- 0.1       | 1        |
| Synchronous    | **1.0 +/- 0.1**       | **0**    | 19.7 +/- 0.2       | 0        |

#### Table 3: `beman::execution::task`

|                | A: awaitable (bridge) |          | B: sender (native)    |          |
|----------------|----------------------:|---------:|----------------------:|---------:|
|                | ns/op                 | al/op    | ns/op                 | al/op    |
| Native         | 43.5 +/- 0.2         | 1        | **32.2 +/- 0.2**     | **0**    |
| Abstract       | 43.3 +/- 0.3         | 1        | **55.3 +/- 0.2**     | **1**    |
| Type-erased    | 48.8 +/- 0.1         | 1        | **55.3 +/- 0.2**     | **1**    |
| Synchronous    | 2.7 +/- 0.3          | 0        | **1.1 +/- 0.3**      | **0**    |

#### Per-operation allocations (native column)

| Stream type           | pipeline | capy::task | bex::task |
|-----------------------|---------:|-----------:|----------:|
| Native                | 0        | 0          | 0         |
| Abstract              | 1        | 0          | 1         |
| Type-erased           | 1        | 0          | 1         |

`capy::task` is the only execution model with zero allocations at every abstraction level.

#### Trade-off summary

| Property                          | IoAwaitable (Col A)                   | sender/receiver (Col B)                       |
|-----------------------------------|---------------------------------------|-----------------------------------------------|
| Native concrete performance       | ~31 ns/op, 0 al/op                   | ~32 ns/op, 0 al/op                           |
| Type erasure cost (with recycler) | +5 ns/op, 0 al/op                    | +23-24 ns/op, 1 al/op                        |
| Type erasure mechanism            | Preallocated awaitable                | Recycled op_state (factory + virtual dispatch)|
| Why the gap persists              | No allocator path, no allocation call | Allocator fast path + factory + unique_ptr [3]|
| Synchronous completion            | ~1 ns/op (symmetric transfer)         | N/A (stack overflow without trampoline)       |
| Inline completion (await_ready)   | I/O in `await_ready`, no suspend      | No equivalent; `start()` is post-suspend      |
| Looping                           | Native `for` loop                     | Requires `repeat_effect_until`                |
| Bridge to other model (native)    | ~10-11 ns/op, 1 al/op                | ~17 ns/op, 0 al/op                           |
| Bridge to other model (erased)    | Faster in bex::task, equal in pipeline| ~36 ns/op, 1 al/op                           |
| `as_awaitable` bypass             | N/A (native protocol)                 | Only leaf senders with explicit member [7]    |
| Compile-time env safety           | Structural (in function signature)    | Opt-in (per-sender constraint) [11, 12]       |
| Composability                     | Coroutine chains                      | Sender algorithm pipelines                    |

#### Gaps in the sender model for I/O

- **No synchronous completion path.** `start()` is void - it cannot signal that the operation completed inline. Without a trampoline, synchronous completions cause stack overflow.
- **Per-operation allocation under type erasure.** `connect` produces a type-dependent `op_state` that must be heap-allocated when either side is erased. A recycling allocator reduces the cost but cannot eliminate the allocation call.
- **No looping primitive.** There is no standard sender algorithm for a read loop. The benchmark uses `repeat_effect_until` adapted from an example implementation.
- **No awaitable-to-sender customization point.** `as_awaitable` lets senders optimize for coroutines, but there is no equivalent for awaitables entering the sender model. `connect-awaitable` allocates a bridge coroutine frame [3].
- **`as_awaitable` is leaf-only.** Only senders that explicitly provide an `as_awaitable` member bypass `connect`/`start`. Composed senders (`let_value`, `then`, `when_all`) go through the full protocol.

## 3. Why This Matters

`std::execution` provides compile-time sender composition, structured concurrency, and heterogeneous dispatch. Coroutines serve a different domain: serial byte-oriented I/O - reads, writes, timers, DNS lookups, TLS handshakes.

`await_suspend` takes a type-erased `coroutine_handle<>`. An awaitable's size is known when the stream is constructed - preallocated once, reused across every operation. Zero per-operation allocation.

Sender/receiver's `connect(receiver)` produces an `op_state` whose type depends on both the sender and the receiver. Under type erasure, the size is unknown at construction time. It must be heap-allocated per operation. The cost is structural [3].

Coroutines already pay for the frame allocation. If I/O returns senders, coroutines pay the frame allocation and the sender overhead on every call. If I/O returns awaitables, coroutines consume them natively and senders consume them through the P4126 bridge. Both models pay for what they use.

## 4. What Happens If We Do Not Do This

Without IoAwaitable, standard I/O returns senders. Three consequences follow.

**Coroutines pay a compounding tax.** Every `co_await` of a sender inside a P2300 task goes through `connect`/`start`/`state<Rcvr>` on top of the frame allocation. The cost is in the tables.

**The teachable model carries a penalty.** A `for` loop reading from a socket is something a student can follow. The sender equivalent - `repeat_effect_until` composed with `let_value` - works, but most developers will not write or maintain it. If the model developers can learn is slower, new users conclude C++ async is slow.

**The domain partition goes unserved.** Senders excel at compile-time work graphs and heterogeneous dispatch. Coroutines excel at serial byte-oriented I/O and type-erased streams. The current path optimizes one side and taxes the other.

## 5. Detail

### The Prize

The C++ Alliance has built the libraries, written the papers, and found the adopters.

- [P4100R0](https://isocpp.org/files/papers/P4100R0.pdf) "The Network Endeavor: Coroutine-Native I/O for C++29" - thirteen papers, two libraries, three independent adopters, and a timeline through 2028.
- [P4125R0](https://isocpp.org/files/papers/P4125R0.pdf) "Field Experience: Porting a Derivatives Exchange to Coroutine-Native I/O" - a commercial derivatives exchange porting from Asio callbacks to coroutine-native I/O.
- [P4048R0](https://isocpp.org/files/papers/P4048R0.pdf) "Networking for C++29: A Call to Action" - a production pipeline, a continuous workflow, and an open invitation.

Twenty-one years is long enough.

### Supporting Papers

- [P4126R0](https://isocpp.org/files/papers/P4126R0.pdf) "A Universal Continuation Model" - purely additive; gives senders zero-allocation access to every awaitable ever written
- [P4092R0](https://isocpp.org/files/papers/P4092R0.pdf) "Consuming Senders from Coroutine-Native Code" - the sender-to-awaitable bridge, working implementation
- [P4093R0](https://isocpp.org/files/papers/P4093R0.pdf) "Producing Senders from Coroutine-Native Code" - the awaitable-to-sender bridge, working implementation
- [P4123R0](https://isocpp.org/files/papers/P4123R0.pdf) "The Cost of Senders for Coroutine I/O" - structural cost analysis, every concession granted
- [P4088R0](https://isocpp.org/files/papers/P4088R0.pdf) "The Case for Coroutines" - five properties that make coroutines the right substrate for I/O
- [P4003R0](https://isocpp.org/files/papers/P4003R0.pdf) "Coroutines for I/O" - defines the IoAwaitable protocol
- [P4127R0](https://isocpp.org/files/papers/P4127R0.pdf) "The Coroutine Frame Allocator Timing Problem" - the frame allocator must arrive before the frame exists

### Benchmark Methodology

**Execution models** (one per table):

- **sender/receiver pipeline** - Pure sender pipeline using `repeat_effect_until` + `let_value`. Driven by `sender_thread_pool` via `sync_wait`.
- **capy::task** - Capy's coroutine task, driven by `capy::thread_pool`. Natively consumes IoAwaitables.
- **beman::execution::task** - Beman's P2300 coroutine task [1], driven by `sender_thread_pool`. Natively consumes senders. `bex::task`'s `await_transform` checks `as_awaitable` on the sender (first-priority dispatch per [exec.as.awaitable]). When the sender provides an `as_awaitable` member, the task calls it directly, bypassing `connect`/`start` entirely. Table 3's native sender column therefore measures the `as_awaitable` path, not the full sender protocol.

**Stream abstraction levels** (one per row):

- **Native** - Concrete stream type, fully visible to the compiler.
- **Abstract** - Virtual base class.
- **Type-erased** - Value-type erasure. `capy::any_read_stream` for awaitables (preallocated awaitable storage); `sndr_any_read_stream` for senders (heap-allocated stream, SBO).

**I/O return types** (one per column):

- **Column A** - Awaitable I/O type.
- **Column B** - Sender I/O type.

Each execution model natively consumes one I/O type and bridges the other.

**Thread pools:** Both inherit from `boost::capy::execution_context`, providing the same recycling memory resource for coroutine frame allocation. Both use intrusive work queues and mutex + condition variable synchronization. `capy::thread_pool` posts `continuation&` objects intrusively (zero allocation). `sender_thread_pool` posts `work_item*` intrusively when the operation state inherits `work_item` (zero allocation). It has no `post(coroutine_handle<>)` - P2300 execution contexts only expose `schedule()`, which returns a sender. To resume a coroutine on the scheduler, the caller must go through `schedule()`, `connect()`, `start()`, heap-allocating the operation state (one allocation per post).

**Operation state recycling:** Type-erased senders allocate their operation state (`concrete_op`) via `op_base::operator new`, overridden to use the same recycling memory resource used for coroutine frames. After warmup, these allocations are served from a thread-local free list in O(1). Both models are shown at their best. The al/op counts reflect allocation *calls* (including recycled), not global heap hits, so the structural allocation demand is visible even when the recycler eliminates the malloc cost. The recycling allocator is functionally equivalent to what P3433R1 [9] proposes.

**Allocation tracking:** All allocation paths go through a single counter. Global `operator new` and the recycling memory resource wrapper both increment `g_alloc_count`. al/op reflects allocation calls per operation regardless of whether they hit the global heap or the recycler's free list.

**Warmup:** The first complete pass is discarded. The 5 measured runs begin from a thermally stable state.

**Compiler optimization:** Each `co_await` suspends the coroutine and posts to the thread pool's work queue, acquiring a mutex, pushing to the intrusive queue, and signaling a condition variable. These are observable side effects that prevent the compiler from eliminating the benchmark loops.

### Bridge Implementations

#### `await_sender` (sender to IoAwaitable)

Used in Table 2 Col B. Placement-constructs the sender's operation state on the coroutine frame. A `bridge_receiver` stores the completion result in a `std::variant`. An `std::atomic<bool>` exchange protocol handles synchronous completion safely [5] - whichever side (suspend or completion) arrives second resumes the coroutine. Zero bridge allocations; the 1 al/op on abstract/type-erased rows comes from the sender's own type-erased `connect`.

#### `as_sender` (IoAwaitable to sender)

Used in Tables 1 and 3 Col A. Constructs a synthetic coroutine frame (`frame_cb`) - a 24-byte struct matching the coroutine frame ABI layout. `coroutine_handle<>::from_address(&cb_)` produces a valid handle whose `.resume()` calls the bridge's completion callback. This avoids the heap-allocated bridge coroutine that P2300's `connect-awaitable` requires [3]. P4126R0 [10] proposes standardizing this technique.

For `beman::execution::task` (Table 3), the bridge provides an `as_awaitable(Promise&)` member - first-priority dispatch in `[exec.as.awaitable]` [2] - which calls the IoAwaitable directly, bypassing beman's `sender_awaitable` wrapping.

The 1 al/op in all Col A cells comes from the `scheduled_resume` operation state required by P2300's `schedule()`, `connect()`, `start()` protocol - a cross-protocol adaptation cost, not a bridge cost.

### Analysis

#### Baseline

Both models achieve ~31-33 ns/op with zero allocations on concrete streams. The baseline is equivalent.

#### Type erasure

Under type erasure, costs diverge. `capy::any_read_stream` adds ~5 ns and zero allocations - the awaitable is preallocated at stream construction because `coroutine_handle<>` is already type-erased. `sndr_any_read_stream` adds ~23-24 ns and one allocation per operation - `connect`'s template-dependent `op_state` must be heap-allocated when either side is erased, even with a recycling allocator. This asymmetry is structural [3].

#### Synchronous completions

In real networking, many operations complete without waiting: reads from a socket with data in the receive buffer, writes to a non-full send buffer, DNS cache hits. The Synchronous row measures this. Both coroutine models achieve ~1 ns/op through symmetric transfer. The sender pipeline cannot run this benchmark - `start()` is void and cannot signal synchronous completion; the only delivery path recurses through the receiver, causing stack overflow without a trampoline.

Coroutines handle this through `await_ready` (complete inline, never suspend) and `await_suspend` return value (symmetric transfer). Neither has a sender equivalent.

#### Bridges

Both bridges are competitive. `await_sender` adds ~17 ns with zero bridge allocations. `as_sender` adds ~10-11 ns with zero bridge allocations. Allocations in bridged columns come from the target model's own machinery.

In Table 3, the bridged awaitable (Col A) is faster than the native sender (Col B) for abstract and type-erased streams - 43.3 ns vs 55.3 ns at 1 al/op each. The bridge cost is constant across abstraction levels while sender machinery scales with abstraction.

#### Table 3 and `as_awaitable`

Table 3's native sender column benefits from `bex::task`'s `as_awaitable` dispatch - the sender's `connect` and `start` are never invoked. This is why Table 3 native sender (32.2 ns) matches Table 2 native awaitable (31.4 ns) - both measure the awaitable path.

The existing P2300 networking implementation in beman::net [13] does not use `bex::task`. Its `demo::task` always creates a `sender_awaiter` that calls `connect` + `start` with no `as_awaitable` check. For beman::net users, Table 1 is more representative. Senders produced by P2300 algorithms (`let_value`, `then`, `when_all`, etc.) also go through the full path - the `as_awaitable` optimization is only available to leaf senders that implement it explicitly.

#### P2300 bridge asymmetry

**Sender to Awaitable:** `as_awaitable` [2, 7] lets senders provide optimized awaitable representations, completely bypassing `connect`/`start`.

**Awaitable to Sender:** No equivalent customization. `connect-awaitable` creates a bridge coroutine whose frame is "not generally eligible for HALO" [3]. Capy's `as_sender` avoids this with a synthetic `frame_cb`. P4126R0 [10] proposes standardizing the technique.

#### Compile-time safety

IoAwaitable's 2-argument `await_suspend(coroutine_handle<>, io_env const*)` structurally enforces that the execution environment is provided at suspension time. In sender/receiver, environment availability is checked when a sender queries the receiver's environment inside `start()` - compile-time but opt-in. P3164R4 [11] and P3557R2 [12] are addressing diagnostic quality for these errors.

#### Scope and limitations

This benchmark measures per-operation overhead for sequential I/O in a tight loop. It does not measure concurrent composition, real I/O latency, multi-threaded work distribution, or compile-time diagnostics.

---

This benchmark is the subject of ongoing optimization. Absolute numbers will change. The fundamental cost asymmetry - per-operation allocation for senders under type erasure, zero for awaitables - is structural and will not change. The architects of P2300 are especially welcome to inspect the code and suggest improvements.

### References

[1] Beman Project. *execution26: Beman.Execution*. https://github.com/bemanproject/execution

[2] P2300R10. *std::execution*. Niebler, Baker, Hollman, et al. https://wg21.link/P2300

[3] P2006R1. *Eliminating heap-allocations in sender/receiver with connect()/start() as basis operations*. Baker, Niebler, et al. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2006r1.pdf

[4] P3187R1. *Remove ensure_started and start_detached from P2300*. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3187r1.pdf

[5] P3552R3. *Add a Coroutine Task Type*. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html

[6] NVIDIA. *stdexec: NVIDIA's reference implementation of P2300*. https://github.com/NVIDIA/stdexec

[7] C++ Working Draft. *[exec.as.awaitable]*. https://eel.is/c++draft/exec.as.awaitable

[8] P2079R6. *System execution context*. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2079r6.html

[9] P3433R1. *Allocator Support for Operation States*. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3433r1.pdf

[10] P4126R0. *A Universal Continuation Model*. https://isocpp.org/files/papers/P4126R0.pdf

[11] P3164R4. *Early Diagnostics for Sender Expressions*. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3164r4.html

[12] P3557R2. *High-Quality Sender Diagnostics with Constexpr Exceptions*. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3557r2.html

[13] Beman Project. *net: Beman.Net - P2300-based networking*. https://github.com/bemanproject/net

[14] Gerbino, S. *I/O Read Stream Benchmark source*. https://github.com/cppalliance/capy/tree/develop/bench/beman
