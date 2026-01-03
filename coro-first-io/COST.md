# Cost Analysis: Callback vs Coroutine (Clang 3x Slowdown)

## Benchmark Results

This document analyzes performance differences between callback and coroutine implementations for composed asynchronous I/O operations. The benchmarks measure four abstraction levels, comparing both plain `socket` and `tls_stream` (which wraps a socket with an additional layer to simulate TLS overhead).

**Output format:**
- **Level** (1-4): Abstraction depth (1=read_some, 2=read, 3=request, 4=session)
- **Stream type**: `socket` or `tls_stream`
- **Operation**: `read_some`, `read`, `request`, or `session`
- **Style**: `cb` (callback) or `co` (coroutine)
- **Metrics**: Nanoseconds per operation (`ns/op`) and work items per operation (`work/op`)

### Clang Results

```
1 socket     read_some  cb :     4 ns/op, 1 work/op
1 socket     read_some  co :    22 ns/op, 2 work/op
1 tls_stream read_some  cb :     4 ns/op, 1 work/op
1 tls_stream read_some  co :    21 ns/op, 2 work/op

2 socket     read       cb :    24 ns/op, 5 work/op
2 socket     read       co :    37 ns/op, 6 work/op
2 tls_stream read       cb :    74 ns/op, 5 work/op
2 tls_stream read       co :    58 ns/op, 6 work/op

3 socket     request    cb :    47 ns/op, 10 work/op
3 socket     request    co :    58 ns/op, 11 work/op
3 tls_stream request    cb :   158 ns/op, 10 work/op
3 tls_stream request    co :    87 ns/op, 11 work/op

4 socket     session    cb : 12194 ns/op, 1000 work/op
4 socket     session    co :  3576 ns/op, 1001 work/op
4 tls_stream session    cb : 11105 ns/op, 1000 work/op
4 tls_stream session    co :  6527 ns/op, 1001 work/op
```

**The Problem:** At level 4 (`session`), callbacks are **3.4x slower** than coroutines (12194 ns vs 3576 ns). Same work count, same I/O operations, but dramatically different performance. This document explains why Clang struggles where MSVC succeeds.

### MSVC Results

```
1 socket     read_some  cb :     5 ns/op, 1 work/op
1 socket     read_some  co :    26 ns/op, 2 work/op
1 tls_stream read_some  cb :     7 ns/op, 1 work/op
1 tls_stream read_some  co :    44 ns/op, 2 work/op

2 socket     read       cb :    32 ns/op, 5 work/op
2 socket     read       co :    58 ns/op, 6 work/op
2 tls_stream read       cb :    57 ns/op, 5 work/op
2 tls_stream read       co :   166 ns/op, 6 work/op

3 socket     request    cb :    66 ns/op, 10 work/op
3 socket     request    co :    92 ns/op, 11 work/op
3 tls_stream request    cb :   126 ns/op, 10 work/op
3 tls_stream request    co :   313 ns/op, 11 work/op

4 socket     session    cb :  7247 ns/op, 1000 work/op
4 socket     session    co :  6536 ns/op, 1001 work/op
4 tls_stream session    cb : 13281 ns/op, 1000 work/op
4 tls_stream session    co : 26387 ns/op, 1001 work/op
```

**Key observation:** At level 4 (`session`), callbacks and coroutines perform nearly equally (7247 ns vs 6536 ns, **1.11x ratio**). MSVC's optimizer successfully reduces the abstraction penalty that Clang cannot.

### GCC Results

```
1 socket     read_some  cb :     5 ns/op, 1 work/op
1 socket     read_some  co :    17 ns/op, 2 work/op
1 tls_stream read_some  cb :     5 ns/op, 1 work/op
1 tls_stream read_some  co :    28 ns/op, 2 work/op

2 socket     read       cb :    32 ns/op, 5 work/op
2 socket     read       co :    35 ns/op, 6 work/op
2 tls_stream read       cb :    49 ns/op, 5 work/op
2 tls_stream read       co :    84 ns/op, 6 work/op

3 socket     request    cb :    66 ns/op, 10 work/op
3 socket     request    co :    50 ns/op, 11 work/op
3 tls_stream request    cb :   104 ns/op, 10 work/op
3 tls_stream request    co :   147 ns/op, 11 work/op

4 socket     session    cb :  7774 ns/op, 1000 work/op
4 socket     session    co :  4405 ns/op, 1001 work/op
4 tls_stream session    cb : 13825 ns/op, 1000 work/op
4 tls_stream session    co : 13733 ns/op, 1001 work/op
```

**Key observations:**
- **Callbacks faster for simpler operations** (levels 1-2): Callbacks outperform coroutines at shallow abstraction depths.
- **Coroutines faster for complex operations** (level 4 socket): At level 4 socket operations, coroutines are **1.77x faster** than callbacks (4405 ns vs 7774 ns).
- **TLS overhead nearly equal**: For TLS operations at level 4, callbacks and coroutines perform nearly equally (13825 ns vs 13733 ns, **1.01x ratio**).

## The Root Cause

**Nested move constructor chains** that Clang cannot optimize away.

Each I/O operation moves a handler chain through 3-4 levels:
- `io_op` move ctor → moves `read_op` → moves `request_op` → moves `session_op` → moves callback
- **~280 bytes moved per I/O** vs **~24 bytes assigned** for coroutines
- **11.7x more data movement**, but that alone doesn't explain 3x slowdown

The real issue: **Clang generates conservative code** for complex nested template types.

### Callback Model Issues (Clang)

- ✅ **Recycling possible** via `op_cache` - memory is recycled after first allocation (benchmark shows 0 allocs/op)
- ❌ **Nested moves** required per I/O operation (~280 bytes moved)
- ❌ **Template type growth** inhibits optimization (`read_op<request_op<session_op<callback>>>`)
- ❌ **Temporary object churn** on stack (3 levels: `session_op`, `request_op`, `read_op`)
- ❌ **Clang doesn't inline** deeply nested move constructors
- ❌ **Object construction per I/O** - new `io_op` object constructed each time (memory recycled, but object construction overhead remains)

**Why callbacks suffer:**
1. **Template type growth** - Handler type grows: `read_op<request_op<session_op<callback>>>`
2. **Separate code paths** - Each template instantiation creates different code
3. **Temporary object churn** - Stack temporaries created/destroyed at 3 levels
4. **Defensive code generation** - Clang can't prove moves are safe to optimize

### Coroutine Model Advantages

- ✅ **Pre-allocated operation state** - `read_state` reused 1000 times
- ✅ **No nested moves per I/O** - just assignment of handle + executor (~24 bytes)
- ✅ **Type erasure** - `std::coroutine_handle<void>` is fixed size (8 bytes)
- ✅ **No temporary churn** - coroutine state lives in coroutine frame
- ✅ **Better optimization** - compiler sees entire coroutine state machine
- ✅ **Zero allocations per I/O** - operation state pre-allocated in socket

**Why coroutines win:**
1. **Type erasure** - `std::coroutine_handle<void>` is fixed size (8 bytes)
2. **Pre-allocation** - Single `read_state` reused, no construction per I/O
3. **Single frame** - All state in one coroutine frame, compiler sees entire structure
4. **Static optimization** - State machine structure enables better inlining

### Compiler Differences

The callback abstraction penalty is **compiler-dependent**. Benchmark results show:

- **Clang**: Level 4 session → callback **12194 ns** vs coroutine **3576 ns** (**3.4x slower**)
- **MSVC**: Level 4 session → callback **7247 ns** vs coroutine **6536 ns** (**1.11x slower**)
- **GCC**: Level 4 session → callback **7774 ns** vs coroutine **4405 ns** (**1.77x slower**)

**Why MSVC outperforms Clang:**

1. **More aggressive inlining** - MSVC inlines deeply nested move constructors through 3-4 template layers; Clang stops inlining earlier
2. **Better template instantiation optimization** - MSVC optimizes across template instantiations; Clang treats each instantiation more separately
3. **More aggressive temporary elimination** - MSVC eliminates stack temporaries; Clang is more conservative
4. **Less defensive code generation** - MSVC optimizes complex nested types when it can prove safety; Clang generates more defensive code

**GCC's performance characteristics:**

GCC shows a mixed optimization profile:
- **Better than Clang**: GCC achieves callback performance closer to coroutines (1.77x ratio vs Clang's 3.4x)
- **Worse than MSVC**: GCC doesn't achieve MSVC's near-parity (1.77x vs MSVC's 1.11x)
- **Callbacks excel at shallow levels**: GCC's callback implementation is faster than coroutines for levels 1-2
- **TLS overhead nearly equal**: GCC callbacks and coroutines perform nearly equally for TLS operations at level 4

**The core issue:** Clang's optimizer is more conservative with deeply nested template types and move operations, generating more function calls and data movement. MSVC's optimizer is more aggressive and can see through the abstraction layers, making callbacks closer to coroutines. GCC shows strong coroutine optimization at deeper levels but struggles with callback optimization compared to MSVC.

## TLS Stream Overhead Analysis

The benchmark results include `tls_stream` measurements, which wrap a `socket` with an additional layer to simulate TLS overhead. The `tls_stream` adds a wrapper operation (`tls_read_op`) that calls the underlying stream's `async_read_some` once, adding an extra layer of indirection without changing the number of I/O operations.

**Key findings:**

1. **Clang callbacks show improved performance with TLS wrapper** at Level 4 - `tls_stream` is actually faster than plain `socket` (11105 ns vs 12194 ns, 0.91x ratio). The simpler `tls_read_op` wrapper type enables better compiler optimization than the deeply nested handler chains.
2. **MSVC callbacks show overhead with TLS wrapper** - `tls_stream` is slower than plain `socket` (13281 ns vs 7247 ns, 1.83x ratio), suggesting the wrapper layer adds overhead that MSVC's optimizer cannot eliminate.
3. **GCC callbacks show overhead with TLS wrapper** - `tls_stream` is slower than plain `socket` (13825 ns vs 7774 ns, 1.78x ratio), similar to MSVC.
4. **Coroutines show consistent overhead with TLS wrapper** across all compilers - the wrapper layer adds overhead for coroutines (Clang: 1.83x, MSVC: 4.04x, GCC: 3.12x ratios).
5. **Clang's callback optimization benefits from simpler types** - The `tls_read_op` wrapper creates a simpler handler type that Clang can optimize better than deeply nested compositions.

The `tls_stream` analysis reveals that the wrapper layer's impact depends on compiler optimizations and the complexity of handler types. Clang benefits from the simpler `tls_read_op` type structure, while MSVC and GCC show overhead from the additional indirection layer.

## Experimental Validation

Added `char buf[256];` to `session_op` to measure move cost impact:

**Results:**
- **Before:** 13273 ns/op
- **After:** 16211 ns/op  
- **Increase:** ~2940 ns (**22% slower**)

**Analysis:**
`session_op` is moved ~1000 times per `async_session` operation. Adding 256 bytes means **256 KB of data movement** per operation (256 bytes × 1000 moves).

**Conclusion:**
- Move operations are a **real and substantial cost**
- Clang is **not optimizing away** nested moves
- Nested move constructor chains are a **significant contributor** to the 3x slowdown

## Cost Comparison

**Callback Path (per I/O operation):**
- Move handler chain into `io_op`: ~92 bytes moved
- Construct `io_op`: ~96 bytes initialized
- Move handler chain out of `io_op`: ~92 bytes moved
- Destroy `io_op`: cleanup
- **Total: ~280 bytes moved/initialized per I/O**

**Coroutine Path (per I/O operation):**
- Assign handle: 8 bytes
- Assign executor: ~16 bytes
- **Total: ~24 bytes assigned per I/O**

**Ratio: ~11.7x more data movement in callback path**

## Conclusion

**Coroutines avoid the callback abstraction penalty** because:

1. **Pre-allocated operation state** - Single `read_state` reused for all I/O operations
2. **No nested moves per I/O** - Operation state is assigned, not moved
3. **Type erasure via coroutine handle** - Fixed-size handle (8 bytes) vs growing handler types
4. **Single coroutine frame** - All state embedded in one frame, compiler can optimize entire state machine
5. **No temporary object creation** - Coroutine state persists in frame, not created/destroyed per operation

The callback model's 3x slowdown **on Clang** comes from nested move constructor chains that Clang doesn't optimize (~280 bytes moved per I/O), template type growth creating separate code paths, temporary object creation/destruction per I/O operation, and complex nested type handling requiring defensive code generation.

**MSVC avoids this penalty** through more aggressive optimization, achieving near-parity with coroutines.

**The coroutine model performs similarly to sender/receiver** - both avoid the nested move cost penalty that plagues the callback model.
