---
title: "Examining Six Observations on std::execution"
document: P4253R0
date: 2026-09-14
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

`std::execution` places three requirements on the completion of a byte transfer that the transfer cannot satisfy, and the cost lands on the user.

An operation must finish exactly once. Asio permits it never to finish, so the bridge detects abandonment and sends the completion itself. An operation must classify its ending. A read that returns `eof` after 47 bytes is a success or a failure according to the protocol above it, which the transport cannot see, so the mapping loses the byte count, or the channel discrimination, or the generic error algorithms, and a cancelled transfer's count has no parameter at all. An operation's results must not borrow from storage the model frees. P3373R4 frees the predecessor before the successor runs, and a read's buffer is exactly that storage. Each requirement is sound where the model fits; the committee adopted the fixes and moved on. At the I/O seam the same rigor produced a bridge, two tokens, an unwritten algorithm, and a dangling buffer. `std::execution` is a bridge to I/O, not a foundation for it. A coroutine-native design places none of the three requirements and pays none of the three costs.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## 1. Introduction

Robert Leahy has authored or co-authored thirty-one WG21 papers, most of them on `std::execution`, two completion tokens merged into NVIDIA's stdexec, and a review of an earlier attempt at the same adaptation. Seventeen of the papers, both tokens, the review, and a conference talk bear on I/O integration, and they carry what follows. The fourteen remaining range across core language changes, library defect fixes, naming, and committee process.

Three properties of the sender model deserve a name before the sections below examine its costs, because each one does work there. The receiver contract guarantees that a started operation delivers one completion signal and no more, so a consumer never reconciles two endings and never accounts for none. The three completion channels distinguish success, error, and cancellation in the completion itself, so a generic algorithm acts on the distinction without inspecting a value whose domain it may not know. And the operation state gives an asynchronous operation the stable storage a stack frame gives a synchronous one, for the whole of its lifetime. Each of the three is worth what it costs where an operation can supply it.

Leahy establishes the analogy in P3373R2. "In broad terms a regular (i.e. synchronous) function call has access to two forms of storage throughout its lifetime (note that the 'lifetime' of a regular function call is the time between the call thereto and the return therefrom)":<sup>[1]</sup>

> Stack storage (i.e. "variables with automatic storage duration")
>
> Heap storage (i.e. "variables with dynamic storage duration")

An asynchronous operation, he continues, has the same two: the contents of its operation state, and heap storage. The operation state is, in his words, "the asynchronous analog of a synchronous stack frame. Local stable storage the operation can rely on throughout its lifetime" (6:43).<sup>[2]</sup> He decomposes the call the same way: the sender "represents the function to call, and the arguments thereto", the operation state "represents the stack frame", and the receiver "represents the return".<sup>[3]</sup>

The analogy has one area, Leahy notes, "in which they lack predictive power: The lifetime of the operation state." One would expect that lifetime to end when a completion signal is invoked, "however this is not guaranteed to be the case in general and in fact `std::execution` appears to guarantee exactly the opposite."<sup>[1]</sup> Put differently: whereas the stack pointer for regular synchronous code moves both up and down, the analogue thereof for asynchronous code under the framework of `std::execution` moves in only one direction - such storage is only ever allocated.<sup>[1]</sup> Presenting the same observation to LEWG, Leahy put it as a consequence of the specification strategy: `std::execution` "has seemingly standardized the maximum possible lifetime, which means operation state lifetimes must persist for the full, containing asynchronous operation, perhaps even long after that part of the operation has ended".<sup>[3]</sup>

Leahy frames this not as an indictment but as an area requiring careful standardization. His P3373R2 proposes ending predecessor operation state lifetimes early for `let_value`, `let_error`, and `let_stopped` - a change which allows the storage occupied thereby to be reused for the operation state of the second operation,<sup>[1]</sup> standardizing existing practice in libunifex. His P3682R0<sup>[4]</sup> was adopted, removing `std::execution::split`. His P3887R1<sup>[5]</sup> was forwarded by SG1 (8-3-1-0-0) and LEWG (10-5-0-0-0) and adopted for C++26. His production code in NVIDIA's stdexec<sup>[6]</sup> is the Asio-to-sender bridge that the group reviewing the 2020 unified executors proposal sketched and did not build: "the actual asynchronous operation could use the completion token abstraction to plug into the sender/receiver protocol using the operation state," they wrote, and "such an implementation of the asynchronous operations isn't done, yet."<sup>[7]</sup>

Two assumptions bound what follows. The unit of analysis is one practitioner's corpus, which fixes the denominator but establishes no rate at which another practitioner would meet the same costs. And the comparison is drawn against two libraries the author maintains, a stake the Disclosure states; nothing is measured, and no claim depends on a measurement.

Which brings us to the question the six observations raise: what do they share?

## 2. The Simplest Bridge Compiles and Terminates

Let us consider the simplest formulation of bridging Asio and `std::execution`. A sender wraps an Asio initiating function. The sender's `connect` produces an operation state containing the initiation and the receiver. The operation state's `start` invokes the initiation with a completion handler that forwards all synthesized values through to the receiver, completing the operation thereby (8:30).<sup>[2]</sup>

Leahy demonstrates this formulation in his CppCon 2025 talk<sup>[2]</sup>: a sender that wraps an initiating function, a completion handler that sends values down the value channel to the receiver. The code compiles. The sender opts into the concepts machinery of `std::execution` by providing the needful nested type alias (8:54).<sup>[2]</sup> The sender curries the initiation, and `connect` propagates it into the operation state together with the receiver.

But then we look at this code further. We notice something curious. "I've declared this function `noexcept` but initiation is something I accept generically. I didn't establish any properties thereof. I didn't check to see if I could invoke it without throwing exceptions with my completion handler. This implementation can throw an exception and cause to terminate which is decidedly unergonomic" (10:06).<sup>[2]</sup>

And so we are confronted with a question: what does `std::execution` require of `start`?

## 3. The Noexcept Barrier Forces an Executor Wrapper

`start` is the point where the synchronous domain transitions to the asynchronous domain. Leahy states the rule in P3388R3: `std::execution` "permits the former to throw exceptions but does not allow the latter to throw exceptions", where the former is `connect` and the latter `start`.<sup>[8]</sup> Everything reached from a started operation therefore sits "behind the noexcept barrier of `std::execution::start`", and "an exception resulting from any of the aforementioned steps must be transmitted by `std::execution::set_error`."<sup>[8]</sup> It falls to the implementation of `start` to catch its own exceptions and direct them down the error channel to the receiver. Leahy gives the reason the boundary sits there. `std::execution` requires `start` and the completion functions to be `noexcept` despite their preconditions, because "there is no reasonable way for a caller to react to exceptions emitted by the above-mentioned APIs". He records that as among the rationales for splitting `submit` into `connect` and `start`.<sup>[9]</sup>

Leahy specifies this requirement in his review of the initial `use_sender` implementation<sup>[10]</sup>: the adaptor "needs to wrap the associated executor, use this wrapping to wrap all submitted intermediate completion handlers, catch all exceptions thrown thereby, and coalesce them to `set_error_t(std::exception_ptr)`."<sup>[10]</sup> And so Leahy wraps the executor. His `completion_token`<sup>[11]</sup> defines an executor wrapper whose `execute` member function wraps every submitted invocable in a `run_` method that creates a frame (as we shall see in the following section) and catches all exceptions:

```cpp
template <typename T>
void execute(T&& t) const noexcept
{
    self_.run_(
        [&]() { ex_.execute(
            wrap_(static_cast<T&&>(t))); });
}
```

Of course, the executor underlying the wrapper embodies whatever execution policy it embodies (24:40).<sup>[2]</sup> The work may be placed on a queue and later dequeued and invoked somewhere that is not underneath the wrapper on the call stack. And so it is insufficient to wrap on the outside; Leahy also wraps inside `execute` (24:56).<sup>[2]</sup> An `associated_executor` specialization<sup>[11]</sup> injects this wrapping into Asio, causing Asio to use Leahy's executor logic at every level of analysis (26:41).<sup>[2]</sup> A companion `associated_allocator` specialization<sup>[11]</sup> forwards the allocator from the receiver's environment into Asio; it performs no wrapping and has no part in the exception-safety obligation.

But if throwing an exception can cause Asio to stop making forward progress on an operation, why do we imagine that throwing an exception is the only way in which Asio can be induced to stop making forward progress on an operation (26:48)?<sup>[2]</sup>

## 4. The Bridge Synthesizes an Ending Asio May Never Send

Leahy identifies a second category of forward-progress failure beyond exceptions. Asio supports what Leahy terms "abandonment" - one can "simply walk away from a running operation, allow the lifetime of the completion handlers to end, and everything is fine."<sup>[10]</sup> `std::execution` does not tolerate this.<sup>[10]</sup> A started operation must send exactly one completion signal.<sup>[10]</sup>

Leahy describes the pattern from deployment experience: "the modal way that I have seen well-written working Asio applications effectuate shutdown is to simply stop calling run in the execution context. Let destructors run. Never make forward progress on the operations ever again. Gracefully clean up all of the resources and exit the scope" (27:06).<sup>[2]</sup> This formulation works perfectly in Asio applications (27:26).<sup>[2]</sup> It does not work under structured concurrency, whereunder it is incumbent upon the bridge to detect abandonment and coalesce it to a stopped completion - "to, for example `set_stopped_t()`", in Leahy's phrasing.<sup>[10]</sup>

And so Leahy builds the `frame_` class. His `operation_state_base`<sup>[11]</sup> in NVIDIA's stdexec reifies the above-described requirements as six members:

```cpp
Receiver                       r_;
asio_impl::cancellation_signal signal_;
std::recursive_mutex           m_;
frame_*                        frames_{nullptr};
std::exception_ptr             ex_;
bool                           abandoned_{false};
```

The six members are, in order: the receiver, a cancellation signal, a recursive mutex, an intrusive linked list of stack frames for lifetime tracking, an exception pointer, and an abandonment flag. The operation state stores a stop callback separately, as an optional. The `frame_` destructor<sup>[11]</sup> implements structured concurrency finalization. It acts when the current frame is the last frame on the linked list and the completion handler has been abandoned. It then releases the lock. It sends `set_error` to the receiver if the operation state holds an exception, and `set_stopped` if it does not. The `completion_handler` destructor<sup>[11]</sup> detects abandonment by creating a frame and setting the `abandoned_` flag to `true`.

Leahy's `frame_` destructor visits every branch of the state machine (33:59).<sup>[2]</sup> If the frame no longer holds the lock, the operation has already completed and there is no work to do. Otherwise: remove the frame from the intrusive linked list. Compute whether this frame should finalize the operation. If there are no frames remaining and the handler has been abandoned, finalize. The destructor enumerates every path. It leaves no branch unaddressed.

This machinery maintains every invariant of structured concurrency. What it costs becomes visible against a library that performs the same I/O without bridging a foreign completion model.

Corosio<sup>[12]</sup> is a coroutine-native I/O library maintained by the author, so the comparison below sets the author's own work against Leahy's. Corosio's per-operation state is `coro_op`, the envelope shared by every native backend - the readiness reactors, `io_uring`, and IOCP (Windows I/O completion ports) - with its constructors and comments elided:<sup>[12]</sup>

```cpp
struct coro_op : scheduler_op  // : intrusive_queue<scheduler_op>::node
{
    struct canceller { coro_op* op; void operator()() const noexcept; };

    std::coroutine_handle<>                      h;
    capy::continuation                           cont;
    capy::executor_ref                           ex;
    std::error_code*                             ec_out    = nullptr;
    std::size_t*                                 bytes_out = nullptr;
    bool                                         is_read      = false;
    bool                                         empty_buffer = false;
    std::atomic<bool>                            cancelled{false};
    std::optional<std::stop_callback<canceller>> stop_cb;
    std::shared_ptr<void>                        impl_ptr;

    void start(std::stop_token const&);
    void request_cancel() noexcept;
    virtual void on_cancel() noexcept;
};
```

This structure is not free, and it is not free of the mechanisms Leahy's uses. It is polymorphic, so it has a vtable pointer. Its base is an intrusive queue node, so every operation is a link in a list. It has an atomic flag and a stop callback for cancellation, and a `shared_ptr` keepalive because the kernel owns the submitted buffers until the operation completes. Leahy's `operation_state_base` has the cancellation cost too, through `signal_` and its separately stored stop callback.

The difference is not the presence of these mechanisms but what each is for. `coro_op`'s intrusive node links the operation into the scheduler's ready queue: one node, one list, and its purpose is to be run. Leahy's `frames_` is a per-operation list of nested executor frames whose purpose is to determine when the last frame unwinds, so that abandonment can be detected and a completion signal synthesized that Asio would not otherwise send. The `abandoned_` flag records the condition, the `frame_` destructor performs the synthesis, and the `completion_handler` destructor sets the flag that starts it when Asio destroys the handler.

Two of these mechanisms do more than one job. Each is counted for the job that brought it into being. The recursive mutex serializes cancellation against completion: `on_stop_request_` acquires it immediately before emitting the cancellation signal into Asio, and the completion path acquires it before releasing the frames.<sup>[11]</sup> A bridge needs that serialization whether or not it tracks frames, and `coro_op` performs it through the atomic flag and stop callback noted above, so the mutex is not counted. What the frames make necessary is only that it be recursive rather than plain, since frames nest and each holds the lock while user code runs beneath it.

Each frame holds the mutex itself, and `release()` walks the list to drop those locks on the completion path.<sup>[11]</sup> But that work exists only because the frames do, and the frames exist to detect abandonment. `coro_op` has no counterpart for that. So the list is counted and the mutex is not. Leahy has said that making thread safety a template parameter is among his remaining work items, and that for now the implementation "pessimizes and always creates it and always acquires it" (55:44),<sup>[2]</sup> so a single-threaded execution context would not pay for it; it is in the shipped code today.<sup>[11]</sup>

`coro_op` has no counterpart to the four, and the reason is not that coroutines are cheaper. A coroutine-native library can decline to deliver a completion too - Corosio's scheduler discards queued operations at shutdown through a `destroy()` documented as "Destroy without invoking the handler."<sup>[12]</sup> - but it is the party doing the discarding. It knows, because it decided. Leahy's bridge is on the other side of that decision: Asio's execution context destroys the completion handlers, and the bridge learns of it only from a destructor running under it. The frame list, the `abandoned_` flag, and the `completion_handler` destructor that sets it answer a question a library that owns both ends never has to ask: whether the other party has walked away. Once the answer is yes, the `frame_` destructor synthesizes the completion the receiver contract requires. That machinery is the cost of reconciling two models, not a cost of the sender model alone.

The bridge machinery is one place where the reconciliation shows. The values themselves are another.

## 5. Two Tokens Divide One Tradeoff

An Asio completion has a status and a payload together; the three channels admit them differently. The bridge must route the pair, and the two tokens Leahy shipped answer in opposite ways.

Asio operations complete by invoking their completion handler with a leading error code and trailing arguments. A call to `async_read` delivers `(boost::system::error_code, std::size_t)` - the status and the byte count. Both values are always present. A read that returns `eof` with 47 bytes means 47 bytes arrived before the peer closed the connection. The byte count is not redundant with the error code.

The sender model provides three completion channels: `set_value`, `set_error`, and `set_stopped`. Leahy must route compound Asio results into discrete channels. His `use_sender`<sup>[13]</sup> defines a receiver whose `set_value` overload, when the first argument satisfies `is_error_code`, dispatches along three paths:

```cpp
void set_value(T&& t, Args&&... args)
    && noexcept
{
    if (!t)
    {
        ::STDEXEC::set_value(
            static_cast<Receiver&&>(r_),
            static_cast<Args&&>(args)...);
        return;
    }
    if (/* cancellation check */)
    {
        ::STDEXEC::set_stopped(
            static_cast<Receiver&&>(r_));
        return;
    }
    ::STDEXEC::set_error(
        static_cast<Receiver&&>(r_),
        use_sender::to_exception_ptr(
            static_cast<T&&>(t)));
}
```

On the first path (no error), the error code is stripped and the remaining arguments - including the byte count - are forwarded through `set_value`. On the second path (cancellation), `set_stopped` is sent and all arguments are discarded. On the third path (error), the error code is converted to `std::exception_ptr` and sent through `set_error`. The remaining arguments - including the byte count - are not forwarded. They are discarded.

The pull request that merged these tokens ships a second mapping alongside the first.<sup>[14]</sup> `exec::asio::completion_token`<sup>[11]</sup> forwards every argument the completion handler receives, error code included, through `set_value`, and declares one `set_value_t(...)` completion signature per Asio completion signature:

```cpp
template <typename... Args>
struct signature<void(Args...)>
{
    using type = ::STDEXEC::set_value_t(Args...);
};
```

The two tokens divide the tradeoff between them. `completion_token` preserves the compound result and gives up channel discrimination: an I/O error arrives on the value channel, and `then`, `let_value`, and `when_all` cannot separate success from failure without inspecting the error code themselves. `use_sender` preserves channel discrimination and gives up the trailing arguments. The library ships both and requires the user to choose one.

A coroutine faces no such choice, and the reason is arity rather than channel count. The error and the byte count travel together in one returned object, so the return itself never separates them:

```cpp
auto [ec, n] =
    co_await stream.read_some(buf);
```

Capy - a coroutine-native I/O library maintained by the author, as Corosio is - makes this shape a requirement of its `ReadStream` concept:<sup>[15]</sup> `read_some` must await-return a result decomposing to `(error_code, std::size_t)`. The concept also specifies the partial-success case rather than leaving it to the caller - when `ec` is set, `n` is the number of bytes read before the I/O contingency arose.<sup>[15]</sup> Both values are present on every completion because there is one completion.

Two qualifications apply. Capy does adopt one transport-level convention: a completion that fills the buffer sequence counts as a success even where the operation also signals a contingency, which is deferred to the next read, so that "generic composition algorithms such as `when_all` and `when_any` distinguish a completed transfer from a failure."<sup>[15]</sup> That classifies the unambiguous case and leaves the ambiguous one alone - a short read still arrives as `(ec, n)`, with no verdict attached. And Capy's own range `when_all` discards: when its result has a set `ec`, "the payloads of the children that did succeed are discarded".<sup>[15]</sup> The data is lost there too, and it is the author doing the discarding.

`use_sender` discards the byte count on the error path. `completion_token` keeps it and gives up the discrimination the channels exist to provide. Each shipped token surrenders one of the two properties; what a third formulation would surrender instead comes in Section 5.1. A function that returns a pair is not asked to pick a half.

### 5.1. The Prescribed Algorithm

Each shipped token surrenders one property, and a third formulation would have to surrender something else. Each choice has its cost, and the affected class reaches beyond what the shipped test identifies.

Leahy raised the coalescing question himself, in the last paragraph of the same review, following three items he introduced as crucial. The sentence has its hedges:

> As a possible quality of life improvement `use_sender` should perhaps identify asynchronous operations which complete with `boost::system::error_code` as the first parameter to the completion handler and coalesce truthy completions to `set_error`, but perhaps that's best left as a separate algorithm to ensure that "partial success" has its context fully preserved.<sup>[10]</sup>

The hedges are Leahy's own and they should be read at face value. `use_sender` "should perhaps" identify such operations, but "perhaps that's" best left elsewhere; the remark follows three items he introduces as crucial and is offered as something outside them; and the coalescing shipped forty-six days later in `use_sender`<sup>[13]</sup>, written by Leahy himself. Nothing here is a commitment. What a hedge of that shape does record is that neither placement is comfortable: coalescing inside `use_sender` costs partial success its context, and not coalescing leaves every consumer to inspect the error code. Either way a choice is made on the caller's behalf. That concedes that a class of operation exists which the three channels do not accommodate.

What is not hedged is the reasoning Leahy recorded when the two tokens shipped. The merge commit states the design intent of `completion_token`. That invocations of the completion handler are "passed to the value channel untouched" reflects an intent that the token perform only "the most basic transformations necessary". The commit draws the consequence in the same paragraph: "the full context of partial success must be made available and since the error channel is unary this must be transmitted in the value channel."<sup>[14]</sup>

The separation he floated is part of what shipped. `use_sender` includes `completion_token` and initiates through it,<sup>[13]</sup> so the non-coalescing mapping is the primitive and the coalescing is an opt-in layer above it. What did not happen is the part the hedge was about. The coalescing test lives inside that layer rather than in an algorithm a caller composes. It identifies its operations by naming error-code types. Those types are the configured Asio `error_code`, which is `boost::system::error_code` in a Boost build and `std::error_code` standalone, or `std::error_code` in either.<sup>[13]</sup>

The suggestion is keyed on a type, and the shipped implementation applies a test of that shape, dispatching when the first argument satisfies `is_error_code`.<sup>[13]</sup> The concept admits the configured Asio `error_code` and `std::error_code`, and `to_exception_ptr` branches on which one it received to select the matching exception type.<sup>[13]</sup>

What the test reaches is error-code types. The class of operations that have a compound result is larger. An operation may report its contingency as a bare `errno` value, as an `io_uring` `res` and `cqe_flags` pair, or as a protocol status accompanied by however much of the message arrived. Corosio records three such pairings: `errn` with a byte count on the readiness reactors, a raw `res` with `cqe_flags` on `io_uring`, and `dwError` with a byte count on IOCP.<sup>[12]</sup> Each has a condition and a payload that remain meaningful together, and none presents an error-code type as its first parameter. A test that enumerates error-code types identifies the operations Asio spells that way, which is what `use_sender` needs and less than the class the suggestion names.

What such an algorithm would have to produce is a completion signature, and before any routing can be chosen, something has to be decided which the operation is not in a position to decide. The three channels ask a completing operation to classify itself: success, error, or stopped. A computation can answer. A reduction either produced a number or it did not, and the operation that ran it knows which.

A byte transfer cannot always answer, and one protocol is enough to show why: no transport-level rule classifies every ending correctly. A read which returns `eof` after delivering 47 bytes is a success or a failure according to the protocol layered above it, and the read does not know that protocol. HTTP/1.1 settles the question both ways depending on how the message was framed. A response with neither chunked transfer coding nor a `Content-Length` "is terminated by closure of the connection and, if the header section was received intact, is considered complete unless an error was indicated by the underlying connection".<sup>[16]</sup> The same close arriving mid-body under a declared length leaves the message truncated instead: a message using a valid `Content-Length` "is incomplete if the size of the message body received (in octets) is less than the value given by Content-Length."<sup>[16]</sup> Even the close-delimited verdict is conditioned on what the transport reports, so the transport supplies an input to the classification rather than the classification. The same syscall, the same bytes, opposite verdicts, and the difference is held by a layer the transport cannot see.

Leahy's talk reaches the same question from the other direction. The program he builds through it reads an HTTP response from Google and sometimes hangs, and he demonstrates why: the server does not close the socket, and the code does not consult the `Content-Length` header (45:47).<sup>[2]</sup> He sets an HTTP parser aside as outside the talk's scope and closes the example with `exec::when_any`, a stdexec extension rather than a working-draft algorithm, against a one-second timer, which ends the read without classifying it. The demonstration is of the algorithm, and it is a fair one. What stands in for the verdict, where the transport cannot supply one, is a timeout.

That is what makes a compound result awkward to route rather than only bulky. It is not a success with an extra field, nor a failure with a consolation value. It is the material from which a verdict will later be formed, by whatever knows the protocol. The channels require the verdict at the moment of completion, and for an ending short of the requested transfer a transport that does not parse the framing has no way to supply one. Read that way, Leahy's suggestion that the coalescing is "best left as a separate algorithm" locates the decision where the knowledge to make it lives.

The algorithm must nonetheless route the compound result - an error code together with a byte count - through the channels available to it, and so it must choose. Each of the three routes is an attempt to supply a verdict early, or to decline to. If the algorithm sends both values through `set_value` - that is, `set_value_t(error_code, size_t)` - then I/O errors travel the value channel, and the model's generic algorithms can no longer act on the distinction. `when_all` does not request that its siblings stop, `let_value` runs its continuation on a failed read, and `upon_error` never fires. Each behaves as though it received a success, because by channel it did.

The first route's second cost is the loss of what the channels exist to provide. Where completions are discriminated by channel, the happy path has nothing to inspect: a `set_value_t(size_t)` completion delivers a byte count already known to be good, and the consumer reads a value rather than a verdict. Routing a compound result through the value channel gives that up, and every consumer destructures and tests the error code on the success path as much as on the failure path.

That second cost is a loss against what the channels promised rather than a defect of the convention. A caller reads a coroutine's `(ec, n)` the same way on every path. To read the error on every path is a coherent choice. What the first route surrenders is the alternative to it, and that surrender is peculiar to this route. Coalescing to `set_error` keeps the happy path clean. It pays on the failure path instead, where the byte count does not travel.

The second route renders a verdict rather than deferring one, and renders it from information that does not determine it. Coalescing every truthy error code to `set_error` classifies the `eof` read above as a failure. That verdict is right for the message truncated under a declared length. It is wrong for the message the close itself framed. The consumer that knows the difference must then recover through `let_error` and reassemble what the channel discarded. The third route keeps the channel and changes the type. Routing through `set_error` with an aggregate of an error code and a byte count preserves both, because the byte count travels inside the single argument that channel admits.

Underneath the three routes lies a different triad. The channels themselves form an arity ladder, and a compound result meets a different rung on each. `set_value` is variadic. `set_error` takes a receiver and exactly one further argument. `set_stopped` takes a receiver and nothing at all - the working draft specifies the expression as `set_stopped(rcvr)`,<sup>[17]</sup> and Leahy states the constraint as a mandate while setting out why receivers must accept completion parameters by reference, noting that the question "doesn't apply to `set_stopped` because it must be nullary."<sup>[18]</sup>

The bottom rung is why a cancelled transfer is the hardest case. An operation cancelled after it has moved bytes has something to report and no parameter in which to report it. A caller that needs the count must therefore keep the operation off the stopped channel.

The specification constrains the middle rung by operation rather than by type. `set_error(rcvr, err)` names no particular error type.<sup>[17]</sup> Through `MANDATE-NOTHROW` it requires only that population of the parameter does not throw.<sup>[17]</sup><sup>[18]</sup> An aggregate of an error code and a byte count is nothrow-copyable, so a sender may complete with the two together. The aggregate reaches a composite intact, and the working draft confirms it: [exec.when.all] forms its `errors_variant` over the decayed error types of its children.<sup>[17]</sup> The data survives and the channel discrimination survives with it.

What does not survive is composition. The sender ecosystem's error type is `std::exception_ptr`: it is what `use_sender` coalesces to,<sup>[13]</sup> what generic `upon_error` and `let_error` chains are written against, and what `std::execution::task` handles. An aggregate error type is understood only by consumers written for it. Every intermediate algorithm that touches the operation must either be generic over the error domain or know this one, and a bespoke error domain does not compose with senders written against `std::exception_ptr`. The byte count is preserved at the cost of interoperating with the algorithms the model supplies.

Read as the loss of the byte count alone, the second route's cost would be recoverable. `std::exception_ptr` is type-erased, so an exception object with the count travels down the error channel as an ordinary `std::exception_ptr`: the data survives, the happy path keeps its bare `set_value_t(size_t)`, and every generic chain composes unchanged. What that recovers is the payload, not the classification. An operation which reaches `set_error` has been declared to have failed, and the generic algorithms act on the declaration rather than on its contents: `when_all` requests that its siblings stop, `let_error` runs, `then` does not. The `eof` read framed by the close itself is a success, and no arrangement of what travels inside the error argument makes it arrive as one.

And so the algorithm chooses among three routes, and none of them keeps everything. It can route through `set_value` and give up channel discrimination. It can coalesce to `std::exception_ptr` and declare a verdict the transport cannot reach. Or it can use an aggregate error and give up composition with the generic error algorithms. The difficulty is not that no formulation transmits both values. Each of the three can be made to. It is that transmitting them costs the channel discrimination, or a verdict the transport cannot support, or the consumers able to read the result.

Kohlhoff identified this problem in P2430R0 (2021)<sup>[19]</sup> and named the resolution the channels admit: "Due to the limitations of the set_error channel (which has a single 'error' argument) and set_done channel (which takes no arguments), partial results must be communicated down the set_value channel."<sup>[19]</sup> That is the first route, taken explicitly. P2300R10 reached R10 in 2024<sup>[20]</sup> and has not been revised since. Leahy's `completion_token` takes the same route; his `use_sender` takes the second.

The choice is between preserving the data, preserving what the channels are for, and composing with the model's own error algorithms. A coroutine returning a pair is not presented with it.

The channel mapping is one structural cost the published record documents. The algorithms are another.

## 6. Inside the Model, One Paper Reaches the Defect

Two algorithms with no foreign counterpart were both corrected on the same practitioner's motion through the committee's ordinary process, and their corrections give the model's self-correction a cost to set beside the costs at the seam.

`std::execution::split` forks a computation. Leahy records Eric Niebler's description of its purpose - to "represent[] a fork in the execution graph"<sup>[4]</sup> - and observes that P2300R10's own high-level description does not accurately describe the algorithm.<sup>[4]</sup> A `split` sender yields a multi-shot sender associated with a shared state. Connecting and starting it completes from a stored completion if one is present, otherwise waits on an operation already in flight, otherwise starts the underlying operation and stores its results for later consumers.<sup>[4]</sup>

P3682R0<sup>[4]</sup> identifies four deficiencies.

The first is dynamic allocation. `split` must allocate the state dynamically when it creates the sender, because that sender, every copy of it, and every operation state connected from either one share the state. The allocation also happens too early in the workflow, so the receiver's environment cannot supply an allocator for it at connect time.<sup>[4]</sup> The second is shared ownership. A shared state brings reference counting, which Leahy writes structured concurrency can usually avoid. It also keeps the operation state and its results alive until the last sender or operation state that refers to them is destroyed. For other operations the sender's lifetime has nothing to do with the operation state's.<sup>[4]</sup>

The third is conditional eagerness. P2300R10<sup>[20]</sup> records that eager execution was removed from earlier revisions because it "has a number of negative semantic and performance implications,"<sup>[20]</sup> yet the first consumer to connect and start finds `split` lazy and every subsequent consumer finds an operation already running.<sup>[4]</sup> The fourth is naming, and the name is too good for it: "'Split' is a very short (i.e. good) name. Reserving it for an operation which is so esoteric in the face of `std::execution`'s norms (see above) seems ill-advised."<sup>[4]</sup>

Leahy's alternative is `let_value` composed with `when_all`, shown here with two children where the source shows three:

```cpp
std::execution::sender auto shared =
    /* ... */;
(void)std::this_thread::sync_wait(
    std::move(shared)
    | std::execution::let_value(
        [](auto&&... values) {
            return std::execution::when_all(
                std::execution::just(
                    std::ref(values)...)
                | /* a */,
                std::execution::just(
                    std::ref(values)...)
                | /* b */);
        }));
```

The formulation needs no dynamic allocation, no shared ownership, and no conditional eagerness. For patterns this formulation does not reach, Leahy points to async scopes.<sup>[4]</sup> His proposal: "Remove `std::execution::split`. Replace it with nothing."<sup>[4]</sup>

The committee removed it. `split_t` no longer appears in [execution.syn] and the [exec.split] subclause is absent from the working draft.<sup>[17]</sup>

Two things followed the removal, and both bear on how much the removal settled.

The first is that the replacement is not free in the domain it serves. Proposing `std::execution::sequence` in 2026 - serial composition of a pack of senders, not the multi-item sequence senders of Section 4.1 - Leahy notes that without it "users who wish to serially compose senders must do so using `std::execution::let_value`", which "raises the concern of so-called 'dynamic asynchrony'".<sup>[21]</sup> The concern is Lelbach's, stated for NVIDIA's CUDA schedulers. `let_value` "is inherently dynamic, as we cannot know what the next sender will be until we connect and invoke the user-provided invocable", and in that implementation it "will block until the entire predecessor chain completes on the CPU side, introducing a substantial latency bubble that destroys performance." The position drawn there is that "the NVIDIA mindset on `let_value` has typically been that it is to be avoided or used sparingly, as it will have performance issues on our platform."<sup>[22]</sup> The same paragraph records that the position did not survive contact with the alternatives: a point-free style was pursued in the hope of limiting the need for `let_value`, but "we do not see a path for an elegant point-free-style design, so we are now resigned to using `let_value`, despite its performance pitfalls."<sup>[22]</sup> The composition that replaced `split` therefore has a documented cost on the hardware the model was designed to dispatch to, one NVIDIA has accepted rather than solved, expecting a newer CUDA model to reduce the overhead without removing it.

The second is that P3682R0's four deficiencies were not the whole list. In 2026 Leahy identified a fifth and located why it had gone unnoticed. `split` "completed with references", which made it "the asynchronous analogue of a function which returns a reference to a local variable, a detail which was masked by the fact asynchronous operations do not generally eagerly destroy their child operation states."<sup>[18]</sup> The property that masked it is the one Section 1 opens with. Removing `split` also left the working draft with no algorithm whose own completion signatures have references, a gap P4288R1 records while proposing that algorithms pass through their children's by-reference result datums rather than decay-copying them.<sup>[18]</sup>

The algorithm was removed and its four enumerated deficiencies went with it. A fifth was found afterwards, in a defect the model's own lifetime rule had hidden, and the composition offered in its place is one a P2300 co-author advises against on the platform it was written for. That is what removing `split` cost: a defect the committee reached cleanly, and a residue that surfaced after the vote.

## 7. The Ronseal Argument Reaches when_all

The second algorithm was not removed but corrected, and the corrections are still arriving. Four papers hold `std::execution::when_all` to the description the standard gives it; they belong together, because what they share is that standard rather than the defect each one found.

Leahy's P3887R1<sup>[5]</sup> identifies that `std::execution::when_all` does more than what it says on the tin - it is not, in Leahy's terminology, a "Ronseal algorithm."<sup>[5]</sup> P2300R10<sup>[20]</sup> describes the algorithm thusly: "when_all returns a sender that completes once all of the input senders have completed."<sup>[20]</sup> This articulation, and the single responsibility which springs therefrom, have nothing to do with eager checking for stop requests - functionality which can be provided by a separate algorithm.<sup>[5]</sup> Leahy supplied that algorithm eleven days before P3887R1: P3892R0<sup>[23]</sup> proposes `unless_stop_requested`, "an algorithm which neglects to start an asynchronous operation if at the time it would've been started a stop request therefor is already outstanding."<sup>[23]</sup>

Two consequences followed from the formulation Leahy examined. Even given a set of child senders none of which send `set_stopped_t()`, a `when_all` sender unconditionally reported that it can send `set_stopped_t()`.<sup>[5]</sup> And operations which the user reasonably believed would be started and allowed to run were skipped,<sup>[5]</sup> which is germane to async scopes and to generalized async RAII. The consequence for a scope is not only incorrect results: `simple_counting_scope`'s destructor "invokes `terminate`" unless the scope is "joined, unused, or unused-and-closed", so a join skipped by an eager stop check ends the program.<sup>[24]</sup> Leahy grounds the objection in one of P2300R10's own motivating principles, which he quotes: "Care about all reasonable use cases, domains and platforms."<sup>[20]</sup>

The committee agreed. SG1 forwarded to LEWG (8-3-1-0-0) and LEWG forwarded to LWG as a bug fix (10-5-0-0-0),<sup>[5]</sup> and P3887R1 was adopted for C++26.

The working draft<sup>[17]</sup> now starts every child unconditionally, and the stopped completion is guarded:

```cpp
if constexpr (sends-stopped) {
    on_stop.reset();
    set_stopped(std::move(rcvr));
}
```

where `sends-stopped` is true only if some child sender's completion signatures contain `set_stopped_t()`.<sup>[17]</sup> Leahy's argument was made, accepted, and shipped.

It did not finish the job, and Leahy filed again. P4269R0<sup>[25]</sup> proposes that `when_all` "not use a `std::inplace_stop_source` when it can be statically determined such a stop source would never be used."<sup>[25]</sup> The guard adopted above tests the children's completion signatures. But `when_all` creates a stop source unconditionally and injects its tokens into every child. A child connected in a stoppable environment advertises `set_stopped_t()`. The same child in an unstoppable environment does not. So the condition the guard tests is one `when_all` manufactures. Leahy's example is a child `s` advertising only `set_value_t()` under an unstoppable token, for which both `when_all(s)` and `when_all(s, s)` still advertise `set_stopped_t()`: "A bizarre outcome since the second completion signature will never be used."<sup>[25]</sup>

The unconditional `set_stopped_t()` advertisement P3887R1 objected to therefore survived P3887R1's adoption, in a second mechanism its wording did not reach.

Two further papers reach `when_all` the same way, and only one of them arrives by Leahy's route. P4217R1<sup>[26]</sup> takes up the zero-sender case, which the standard makes "ill-formed" by fiat and which "unnecessarily creates a special case when writing generic algorithms"; SG1 gave unanimous consent in Brno in 2026 to forwarding P4217R0 to LEWG for C++29.<sup>[26]</sup> It reaches that conclusion from the standard's own description of `when_all`, arguing that given zero senders "all input senders" have trivially completed. But it does not invoke the single-responsibility argument. It cites neither P3887R1 nor P3892R0, and credits a C++Now 2026 talk by Jonathan M&uuml;ller for making the author aware of the defect.<sup>[26]</sup> P4288R1<sup>[18]</sup> takes up decay-copying by applying P3887R1's own argument a second time: "Nothing about the quoted description of purpose has anything to do with decay-copying, and therefore `std::execution::when_all` shouldn't decay-copy anymore than it should randomly interact with stop requests". The extraction to a separate algorithm follows the precedent `unless_stop_requested` set.<sup>[18]</sup>

Each of the four holds `when_all` to what its own description says it does: complete when its children complete. Each removes something it had accrued past that. Extraction into algorithms that name them removes eager stop checking and decay-copying. Declining to create a stop source where it can be shown unused removes the manufactured one. And at zero senders, P4217R1 removes a prohibition the description does not warrant. One of the four shipped in C++26; P4269R0<sup>[25]</sup>, P4217R1<sup>[26]</sup> and P4288R1<sup>[18]</sup> are still pending. On that record the Ronseal case Leahy made in P3887R1 has not been rejected where it has been applied. P4217R1 reaches the same place without it. That is some evidence that the standard does the work rather than the argument's author.

Both algorithms tell the same story. Inside the model, correction reaches the defect. Four enumerated deficiencies removed `split` from the working draft, and one argument about `when_all` has met no rejection across four applications. The same practitioner whose I/O findings are reported here moved both. What that correction costs is elapsed revisions and a residue found afterwards, not a property nobody can recover.

But the algorithmic corrections address defects with no foreign party. The same method meets a different result when the defect is not inside the model.

## 8. let_value Frees the Buffer a Read Is Using

Section 1 opened on the one place Leahy's stack-frame analogy fails: the operation state's lifetime does not end when the completion fires. P3373R4<sup>[27]</sup> moves that lifetime back for `let_value`, `let_error`, and `let_stopped`, so the predecessor's storage can be reused for the successor. What happens when the freed storage is a buffer?

The dangling case is P3373R4's own example. Its Examples section pipes `just()` into a `then` callable that captures a `std::vector`, returns `std::cref(vec.front())`, and continues on a scheduler:

```cpp
auto op = std::execution::connect(
    std::execution::just()
    | std::execution::then([
        p = std::move(ptr),
        vec = std::vector<int>{1, 2, 3}]() noexcept
    {
        std::cout << &vec.front() << std::endl;
        return std::cref(vec.front());
    }) | std::execution::continue_on(scheduler),
    receiver{});
std::execution::start(op);
ctx.run();
```

P3373R4 then walks the synchronous analogue and reports the AddressSanitizer diagnostic that analogue produces.<sup>[27]</sup> Two substitutions follow. The result datum becomes `std::span<std::byte>` so that it is a buffer descriptor rather than a reference wrapper, which is what an I/O operation receives. The control is then added: a second predecessor with the same completion signature and the owner placed outside the sender. The matched pair is the contribution, not the dangling case, which P3373R4 established.

The adopted wording creates a specific destruction boundary inside `let_value`. Its state contains a variant named `ops`. That variant initially contains the predecessor operation state. On a matching value completion, [exec.let] performs six steps: store decayed copies of the predecessor's result datums in `args`; replace the active `ops` alternative with `monostate`; invoke the user-supplied factory with references to the stored copies; connect the returned sender to the downstream receiver; store the successor operation state in `ops`; start the successor.<sup>[17]</sup> The following excerpt is from the C++ draft source at commit `999d8ae0`, lines 4268-4277, with the exposition-only markup stripped and nothing else altered.<sup>[28]</sup> These ten lines are unchanged between N5046, N5054, and that commit.

```cpp
auto& tuple = args.template emplace<args_t>(std::forward<Ts>(ts)...);
ops.template emplace<monostate>();
auto&& sndr = apply(std::move(fn), tuple);
using op_t = connect_result_t<sender_type, receiver_type>;
auto mkop2 = [&] {
  return connect(std::forward<sender_type>(sndr),
  receiver_type{rcvr, env});
};
auto& op = ops.template emplace<op_t>(emplace-from{mkop2});
start(op);
```

`variant::emplace` destroys the active alternative before constructing its replacement.<sup>[17]</sup> The first `ops.emplace` therefore destroys the predecessor operation state after the result copies exist but before the factory is invoked.

The result datum persisted by `let_value` can be an owner or a non-owning descriptor. That distinction determines whether persisting the datum also preserves the objects reached through it. The standard defines `std::span` in [span.overview] as "a view over a contiguous sequence of objects, the storage of which is owned by some other object."<sup>[17]</sup> A span is trivially copyable. Copying it preserves a pointer and an extent; the copy does not copy the objects in the viewed sequence. P1179R1 uses the terms Owner and Pointer for this distinction. Its examples classify `string` and `vector` as Owners, while raw pointers, `string_view`, `span`, and `vector::iterator` are non-owning Pointers.<sup>[29]</sup>

The following constructed sender stores the vector in the predecessor operation state after connection.

```cpp
auto ephemeral =
    std::execution::just()
    | std::execution::then(
        [owner = std::vector<std::byte>(4096)]()
            mutable noexcept {
            return std::span<std::byte>(owner);
        });
```

The `then` callable returns a valid span while its vector capture is alive. `let_value` receives that span, copies it into `args`, and replaces the predecessor operation state with `monostate`. Replacement destroys the `then` callable and its vector. The persisted span remains alive and denotes storage whose lifetime has ended.

The control changes only the owner's location.

```cpp
std::vector<std::byte> owner(4096);

auto durable =
    std::execution::just()
    | std::execution::then([&owner]() noexcept {
        return std::span<std::byte>(owner);
    });
```

Destroying the second predecessor destroys a callable containing a reference. It does not destroy `owner`, so the persisted span remains usable while the external vector remains alive.

Both `noexcept` callables return the same type. Their value completion signatures are therefore equal:

```cpp
using ephemeral_sigs =
    std::execution::completion_signatures_of_t<
        decltype(ephemeral), std::execution::env<>>;
using durable_sigs =
    std::execution::completion_signatures_of_t<
        decltype(durable), std::execution::env<>>;

static_assert(std::same_as<ephemeral_sigs, durable_sigs>);
```

The assertion holds by the completion-signature rules, which do not depend on any implementation: both callables are `noexcept`, `just()` contributes `set_value_t()`, and decay-copying a `std::span` cannot throw, so both predecessors have `completion_signatures<set_value_t(std::span<std::byte>)>`. The assertion also compiles. Against stdexec at x86-64 gcc 16.2 with `-std=c++23 -Wall -Wextra`, the pair builds with no diagnostics and the `static_assert` passes.<sup>[30]</sup>

The matched pair becomes consequential when the successor is an asynchronous I/O operation. Boost.Asio 1.92.0 defines `mutable_buffer` as a copyable representation that "does not own the underlying data."<sup>[31]</sup> Its `basic_stream_socket::async_read_some` operation accepts one or more mutable buffers and returns immediately.<sup>[32]</sup> The parameter contract states:

> Although the buffers object may be copied as necessary, ownership of the underlying memory blocks is retained by the caller, which must guarantee that they remain valid until the completion handler is called.

The descriptor can therefore survive while its referent does not. The precondition applies from initiation through completion, the same interval for which the successor sender uses the buffer. Windows `ReadFileEx` independently requires its buffer to remain valid for the read duration.<sup>[33]</sup> Linux `io_uring(7)` states the same rule for pointers used by `IORING_OP_READ` and `IORING_OP_WRITE`.<sup>[34]</sup>

The adopted rule supports safe asynchronous I/O when the owner resides in state that remains alive through the successor. Four placements meet that condition: the owner sent into `let_value` as a persisted argument; the owner captured by the factory; the owner in external state that outlives the operation; and an owning completion datum, such as a `vector` or a `shared_ptr`, that makes ownership part of the result. Each is a placement the user chooses, and the completion signature does not record the choice.

Equal completion signatures, opposite validity, and nothing at the composition point can tell them apart.

## 9. What the Chain Reveals

The observations so far form an iterative chain, each arising from the published work of one practitioner. "And so maybe rather than iteratively discovering the whole problem domain, we take a step back and we look at the totality of it" (27:44).<sup>[2]</sup>

Six observations from Leahy's published work, four at the I/O seam and two inside the model:

1. A bridge<sup>[11]</sup> that requires a recursive mutex, an intrusive linked list, structured concurrency finalization in the `frame_` destructor, abandonment detection in the `completion_handler` destructor, two associator specializations, and a wrapped executor - where the equivalent awaitable integration requires a pre-allocated context structure, a continuation node, and a callback.

2. A channel mapping<sup>[13]</sup> that discards the byte count on the error path because the three-channel model affords no mapping which preserves both the error code and the remaining arguments without routing I/O errors through `set_value`.

3. A recommendation<sup>[10]</sup> that partial success should have its context fully preserved, followed by an implementation that cannot preserve it within the constraints of the available channels. The algorithm has not been written.

4. A lifetime rule<sup>[27]</sup> that frees the predecessor operation state before the successor runs, and with it a buffer a read is using. Equal completion signatures, opposite validity.

5. An algorithm removed<sup>[4]</sup> for dynamic allocation at sender creation time, shared ownership via reference counting, conditional eagerness, and a name too good for it. The committee agreed. A fifth deficiency surfaced afterward.

6. An algorithm corrected<sup>[5]</sup> for injecting stopped completions that no child is capable of sending, belying the reasonable expectations of the consumer. The committee agreed. Three further corrections are still in flight.

The first four sit at the seam where the model meets byte-oriented I/O. The last two are defects inside the model, with no foreign party, and they are the control. Inside the model, one paper reached each defect and the committee adopted the fix. At the seam the same rigor produced a bridge, two tokens, an unwritten algorithm, and a rule that frees a buffer under a read.

The three requirements named in the Introduction are what the seam cannot supply. Asio permits an operation never to finish, so the bridge synthesizes the completion. A transport cannot classify `eof`, so the mapping loses the data, the discrimination, or the generic algorithms. A buffer's owner is not the operation state, so the lifetime rule frees it. Each requirement is sound where the model fits. Each is a requirement a byte transfer cannot meet.

Four repairs at one seam, two inside the model, and only the two were finished.

## 10. Objections

Six objections remain after the preceding sections, stated in their strongest form.

### "The integration works; it was built."

It does, and it was. The bridge compiles, both tokens shipped, and the `frame_` destructor visits every branch. The obligation is the point: Section 4's four mechanisms exist because Asio permits an operation never to finish, and that obligation does not disappear because the machinery that meets it is correct.

### "Structured concurrency's guarantees are genuine."

They are. The receiver contract, the three channels, and the operation state are each worth what they cost where an operation can supply them, and Section 1 says so. A coroutine-native design achieves the same guarantees through scoped coroutine frames: the frame is destroyed when the scope exits, and the continuation is resumed by the executor that posted it. The guarantees are achieved differently, not absent.

### "`std::execution::task` gives you the same pair from one `co_await`."

It does. A `task` awaiting `completion_token`'s sender is resumed once, with `(ec, n)` in hand and no channel to select, which is the shape Section 5 describes. The model supplies a coroutine, and inside that coroutine the compound result is intact.

The cost appears when the value leaves the coroutine. `std::execution::task` is itself a sender, and a sender is consumed by the algorithms the model supplies. The moment that result is composed - handed to `when_all`, or produced by a task that a `let_value` continuation awaits - the completion it holds must be classified, and the three routes of Section 5.1 return unchanged.

The coroutine is not free of the third route's cost either. A task that reports its error as an aggregate rather than an `exception_ptr` does not compose with the generic error algorithms. Those algorithms are written against `exception_ptr`, and that is the same trade the third route names. `co_await` defers the classification to the boundary of the coroutine. It does not remove it.

Leahy's own work on `task` bears on both halves. P4282R1<sup>[35]</sup> records that `std::execution::task` "allows a coroutine to end in error without throwing an exception by yielding an instance of an instantiation of `std::execution::with_error`",<sup>[35]</sup> which is the non-exception error type the third route needs, and the reason that route's composition cost reaches a task as readily as a sender. The same paper records that while `task` "supports stopped completion signals the promise type has no bona fide manner in which the coroutine body can emit them", so authors of coroutine bodies "must use `co_await std::execution::just_stopped()`" instead.<sup>[35]</sup> Leahy proposes `co_return` overloads for both.

### "Leahy published the most on a young library, so he found the most."

The objection is correct that the unit of analysis is a person, and the denominator is public. As of August 2026 Leahy has thirty-one WG21 papers to his name, most of them on `std::execution`. Seventeen of them appear here, each cited where it is used. Sixteen are his own and one is a review report he co-authored.<sup>[7]</sup> Also cited: two merged completion tokens<sup>[11]</sup><sup>[13]</sup>, his review of an earlier adaptation attempt<sup>[10]</sup>, and a conference talk.<sup>[2]</sup>

The corpus's bounds follow from the denominator. The specification or the shipped code documents each cost, and a delegate can check each one there without reference to who found it. [exec.set.error] and [exec.set.stopped] give `set_error`'s arity and `set_stopped`'s absence of one.<sup>[17]</sup> `completion_token.hpp` holds the bridge machinery.<sup>[11]</sup> What one practitioner's corpus adds is that these were met together, in one integration, by someone who resolved each on its merits and proposed no alternative model. It does not establish how often another practitioner would meet them, and no rate follows.

### "The model's authors considered coroutines and rejected them for stated reasons."

They did, in P2300R10 section 1.9.2<sup>[20]</sup>:

> Although coroutines are lighter weight than futures, coroutines suffer many of the same problems. Since they typically start suspended, they can avoid synchronizing the chaining of dependent work. However in many cases, coroutine frames require an unavoidable dynamic allocation and indirect function calls. This is done to hide the layout of the coroutine frame from the C++ type system, which in turn makes possible the separate compilation of coroutines and certain compiler optimizations, such as optimization of the coroutine frame size.

The same section addresses HALO, the coroutine heap-allocation elision optimization that would remove the cost, and reports that it cannot be relied upon: "HALO requires a sophisiticated compiler, and a fair number of stars need to align for the optimization to kick in. In our experience, more often than not in real-world code today's compilers are not able to inline the coroutine, resulting in allocations and indirections in the generated code."<sup>[20]</sup>

Both statements hold, and nothing in the preceding sections contradicts them. `coro_op`<sup>[12]</sup> has an atomic flag, a stop callback, and a keepalive, which is that cost paid in one library rather than an argument that it does not exist. A frame that is not elided is allocated.

The scope of the preceding sections is I/O integration, and the Disclosure states the limitations on the coroutine side: it cannot express compile-time work graphs, and it cannot destroy asynchronously, because a destructor may not be a coroutine. Both models incur costs; the ones above are the ones with public sources.

### "The costs are not confined to I/O."

They are not. Two of Leahy's 2026 papers document structural costs of the sender model that have nothing to do with an I/O library. `std::execution`'s operation states are immovable and are created by being returned from `connect` under guaranteed copy elision, so users need a proxy to construct them in place. P4337R0 proposes standardizing that proxy, observing that "it is for this reason, in fact, that `std::execution` requires said functionality",<sup>[36]</sup> and its companion P4338R0 amends the deduction guides of `pair`, `tuple`, `optional`, `unexpected` and `array` to accommodate the proxy that results.<sup>[37]</sup> Separately, P3986R1 records that specifying `std::execution` "in terms of code" means "attempting to change components of `std::execution` presents the same kind of mechanical burden as refactoring actual code", and the inlinable-receiver optimization it sought reached the standard as `unspecified` and `implementation-defined` rather than as a guarantee.<sup>[38]</sup>

Both are costs the model imposes on everyone who uses it, in the compute domain and outside it. Neither is answered by anything in Sections 2 through 7, and neither enters here as evidence for a boundary. The four costs above are narrower, and narrow for a reason of evidence rather than of scope: they arise at one seam - one where a library may never finish, one where a transfer cannot classify its own ending, and one where a buffer's owner is freed under a read. Byte-oriented I/O is where they appear, because that is the domain whose record is public and whose details the author can check. Nothing here establishes that the seam is confined to that domain.

## 11. Falsification

The observations above would be discharged - that is, explained by causes other than the three requirements meeting a domain that cannot supply them - if any of the following were demonstrated:

- An Asio-to-sender bridge which satisfies the receiver contract when a completion handler is abandoned, without tracking nested executor frames to detect that abandonment - that is, a cheaper mechanism for the same guarantee than the one documented in Section 4.

- A channel mapping that preserves both the error code and the byte count, without routing I/O errors through `set_value`, without an error type that generic `upon_error` and `let_error` chains cannot consume, and without classifying an ending the transport is not in a position to classify - that is, an escape from all three routes of Section 5.1. Or a test that selects such operations without enumerating error-code types, and so reaches a compound result that presents none.

- A sender-based formulation in which an operation cancelled after moving bytes delivers the count to its caller while completing on the stopped channel - that is, a route past the bottom rung of the arity ladder set out in Section 5.1.

- A default `let_value` composition in which a predecessor-owned buffer remains valid through an asynchronous successor, without an owner in the persisted arguments, the factory's captures, external state, or the completion datum.

## 12. Conclusion

Leahy's bridge, tokens, and corrections hold the sender model's invariants under I/O integration. The bridge works. Both tokens work. The algorithmic corrections were adopted.

What the published record also shows is what each of those cost, and that the costs share a cause. Two requirements do the work: that an operation end once and only once, and that its ending be classified when it arrives. Both are useful, and in the compute graph both are available: an operation that computes a value knows it has finished and knows what the finishing meant. Asio does not guarantee the first. Its shutdown model permits a started operation to be abandoned. So the bridge has the four mechanisms Section 4 enumerates, among them a frame list and a destructor that sends an ending which would not otherwise arrive.

The second is not always available in byte-oriented I/O at all. A read that returns `eof` after 47 bytes has finished. Whether it succeeded is a fact about the protocol above it, which the transport cannot see. So the three channels ask for a verdict at the one moment it is not yet available, and the two shipped tokens answer differently because there is no answer that keeps everything. And a transfer cancelled mid-flight has a count the stopped channel has no parameter to hold, because that channel takes the receiver and nothing else. A third requirement, that an operation's results not borrow from storage the model frees, is the one P3373R4 trades away: the predecessor is destroyed before the successor runs, and a read's buffer is exactly that storage.

Both costs are individually addressable, and both tokens shipped. The coalescing algorithm remains unwritten. What the two raise is not whether each resolves in isolation. It is where they arise: both sit at a shared domain boundary, one where a library may never finish and one where a byte transfer cannot say what finishing meant.

Away from that boundary, on two algorithms of the model's own, the ordinary process reaches what it is aimed at. The committee removed `split` on four enumerated deficiencies. One argument about `when_all` has not been rejected where it has been applied, and a fourth paper reached the same conclusion without it. What those corrections left behind - a composition its own platform advises against and is resigned to using, a defect the model's lifetime rule had masked, three corrections to `when_all` still pending - is the ordinary residue of ordinary defects. The two costs at the seam were not settled that way. They were divided between two tokens, and the user was left to pick. The published record bounds the contrast: three of the four `when_all` corrections are still proposals, and the coalescing algorithm is not yet a proposal at all. Both sides of it are unfinished business.

`std::execution` is a bridge to I/O, not a foundation for it. A coroutine-native design places none of the three requirements and pays none of the three costs. The people best placed to test that are the ones who now build on the model: the author of the coalescing algorithm Leahy floated, and the authors of the sender algorithms still in flight.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy) and [Corosio](https://github.com/cppalliance/corosio) and believes coroutine-native I/O is a practical foundation for networking in C++.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

This paper uses AI.

The author has a stake in how C++ compares coroutine-native I/O with sender-based I/O. The comparison in Sections 4 and 5 sets the author's own libraries against Leahy's bridge, and the Disclosure names that stake so it can be weighed.

Coroutine-native I/O cannot express compile-time work graphs. This is a genuine limitation, and it is not the only one. C++ says in [class.dtor] that "A destructor shall not be a coroutine",<sup>[17]</sup> so asynchronous clean-up cannot be reached through RAII and needs a library facility instead. Leahy proposes one.<sup>[24]</sup>

This paper asks for nothing.

## Acknowledgments

Robert Leahy, whose published work supplied every observation above. Leahy's contributions to the sender model - production code in NVIDIA's stdexec, seventeen WG21 papers cited here, and CppCon talks whose constructive-proof methodology has informed the argumentation - constitute the most thorough published examination of `std::execution`'s integration with existing asynchronous ecosystems. His exemplary work let us build proofs by iterative refinement: construct the simplest version of a design, identify why it is wrong, fix it, discover what the fix breaks, and repeat until every path is covered and every invariant holds. Herb Sutter for the Owner and Pointer vocabulary in P1179R1. Christopher Kohlhoff for Boost.Asio's explicit asynchronous buffer-lifetime contract and for P2430R0, which named the partial-success problem in 2021. Mungo Gill for the editorial pass that attributed the dangling example to P3373R4 and for the compile check of the matched pair.

## References

[1] [P3373R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3373r2.pdf) - "Of Operation States and Their Lifetimes" (Robert Leahy, 2025).

[2] [std::execution in Asio Codebases: Adopting Senders Without a Rewrite](https://www.youtube.com/watch?v=S1FEuyD33yA) - CppCon 2025 (Robert Leahy, 2025).

[3] [P3389R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3389r0.pdf) - "Of Operation States and Their Lifetimes (LEWG Presentation 2024-09-10)" (Robert Leahy, 2024).

[4] [P3682R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3682r0.pdf) - "Remove std::execution::split" (Robert Leahy, 2025).

[5] [P3887R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3887r1.pdf) - "Make when_all a Ronseal Algorithm" (Robert Leahy, 2025).

[6] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec) - Reference implementation of `std::execution` (NVIDIA, 2024).

[7] [P2202R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2202r0.pdf) - "Executors review - Senders and Receivers" (Ga&scaron;per A&zcaron;man, Tony van Eerd, Thomas Rodgers, Tomasz Kami&nacute;ski, Corentin Jabot, Robert Leahy, Gordon Brown, Kirk Shoop, Eric Niebler, Dietmar K&uuml;hl, 2020).

[8] [P3388R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3388r3.pdf) - "When Do You Know connect Doesn't Throw?" (Robert Leahy, 2025).

[9] [P4254R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4254r0.pdf) - "Throwing Violation Handlers Are Post Hoc Library Design" (Robert Leahy, 2026).

[10] [NVIDIA/stdexec PR #1501](https://github.com/NVIDIA/stdexec/pull/1501) - "Adapt boost::asio to stdexec" (shyeyian, 2025); review comments by Robert Leahy.

[11] [exec/asio/completion_token.hpp](https://github.com/NVIDIA/stdexec/blob/main/include/exec/asio/completion_token.hpp) - AIO-to-sender bridge (Robert Leahy, 2025).

[12] [Corosio](https://github.com/cppalliance/corosio) (C++ Alliance, 2026).

[13] [exec/asio/use_sender.hpp](https://github.com/NVIDIA/stdexec/blob/main/include/exec/asio/use_sender.hpp) - Sender completion token (Robert Leahy, 2025).

[14] [NVIDIA/stdexec PR #1503](https://github.com/NVIDIA/stdexec/pull/1503) - "asioexec::completion_token & ::use_sender" (Robert Leahy, 2025).

[15] [Capy](https://github.com/cppalliance/capy) (C++ Alliance, 2026).

[16] [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html) - "HTTP/1.1" (Roy T. Fielding, Mark Nottingham, Julian Reschke, 2022).

[17] [N5054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5054.pdf) - "Working Draft, Programming Languages - C++" (Thomas K&ouml;ppe, 2026).

[18] [P4288R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4288r1.pdf) - "Stop the Decay" (Robert Leahy, 2026).

[19] [P2430R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2430r0.pdf) - "Partial success scenarios with P2300" (Christopher Kohlhoff, 2021).

[20] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[21] [P4320R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4320r0.pdf) - "std::execution::sequence" (Robert Leahy, 2026).

[22] [P3300R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3300r0.html) - "C++ Asynchronous Parallel Algorithms" (Bryce Adelstein Lelbach, 2024).

[23] [P3892R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3892r0.pdf) - "unless_stop_requested" (Robert Leahy, 2025).

[24] [P3955R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3955r1.pdf) - "It's Scopes All the Way Down" (Robert Leahy, 2026).

[25] [P4269R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4269r0.pdf) - "when_all Oughtn't Hallucinate set_stopped" (Robert Leahy, 2026).

[26] [P4217R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4217r1.pdf) - "when_all() is just just()" (Robert Leahy, 2026).

[27] [P3373R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3373r4.pdf) - "Of Operation States and Their Lifetimes" (Robert Leahy, 2026).

[28] [C++ draft source](https://github.com/cplusplus/draft/blob/999d8ae0d2d3d6e76d85d39819cf253caacf6af6/source/exec.tex#L4268-L4277) - "`let_value` code-equivalent wording at commit `999d8ae0`" (ISO C++ project, 2026).

[29] [P1179R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1179r1.pdf) - "Lifetime safety: Preventing common dangling" (Herb Sutter, 2019).

[30] [Compiler Explorer](https://godbolt.org/z/qhvq41116) - "Matched-predecessor completion signatures compiled against stdexec trunk, x86-64 gcc 16.2, `-std=c++23 -Wall -Wextra`" (Compiler Explorer, 2026).

[31] [Boost.Asio `mutable_buffer`](https://www.boost.org/doc/libs/1_92_0/doc/html/boost_asio/reference/mutable_buffer.html) - "A non-owning mutable buffer descriptor" (Christopher M. Kohlhoff, 2026).

[32] [Boost.Asio `async_read_some`](https://www.boost.org/doc/libs/1_92_0/doc/html/boost_asio/reference/basic_stream_socket/async_read_some.html) - "Asynchronous socket read and buffer-lifetime requirements" (Christopher M. Kohlhoff, 2026).

[33] [Microsoft `ReadFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfileex) - "Asynchronous file read and buffer-lifetime requirements" (Microsoft, accessed 2026-09-07).

[34] [`io_uring(7)`](https://man7.org/linux/man-pages/man7/io_uring.7.html) - "Linux asynchronous I/O interface" (Linux manual page, 2020).

[35] [P4282R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4282r1.pdf) - "Away From co_yield For std::execution::task" (Robert Leahy, 2026).

[36] [P4337R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4337r0.pdf) - "emplace_from" (Robert Leahy, 2026).

[37] [P4338R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4338r0.pdf) - "deduce" (Robert Leahy, 2026).

[38] [P3986R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3986r1.pdf) - "A Wording Strategy for Inlinable Receivers" (Robert Leahy, 2026).
