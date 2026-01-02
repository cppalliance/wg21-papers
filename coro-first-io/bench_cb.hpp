//
// Copyright (c) 2025 Vinnie Falco (vinnie dot falco at gmail dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
// Official repository: https://github.com/cppalliance/wg21-papers/coro-first-io
//

#ifndef BENCH_CB_HPP
#define BENCH_CB_HPP

#include "bench.hpp"
#include "bench_cb_detail.hpp"

#include <utility>

namespace cb {

//----------------------------------------------------------

/** A simulated asynchronous socket for benchmarking callback-based I/O.

    This class models an asynchronous socket that provides I/O operations
    accepting completion handlers. It demonstrates the traditional callback
    pattern where async operations accept a handler that is invoked upon
    completion.

    The socket stores an executor which is used to post I/O completion
    work items and to dispatch completion handlers.

    @tparam Executor The executor type used for completion dispatch.

    @note This is a simulation for benchmarking purposes. Real implementations
    would integrate with OS-level async I/O facilities.
*/
template<class Executor>
struct socket
{
    Executor ex_;

    explicit socket(Executor ex)
        : ex_(ex) {}

    Executor get_executor() const { return ex_; }

    template<class Handler>
    void async_read_some(Handler&& handler)
    {
        using op_t = detail::io_op<Executor, std::decay_t<Handler>>;
        ex_.post(new op_t(ex_, std::forward<Handler>(handler)));
    }
};

//----------------------------------------------------------

/** Performs a composed read operation on a stream.

    This function performs 10 sequential read_some operations on the
    stream, simulating a composed read that continues until a complete
    message or buffer has been received.

    This demonstrates a 2-level composed operation: async_read calls
    the stream's async_read_some member function 10 times.

    @param stream The stream to read from.
    @param handler The completion handler to invoke when done.
*/
template<class Stream, class Handler>
void async_read(Stream& stream, Handler&& handler)
{
    detail::read_op<Stream, std::decay_t<Handler>>(stream, std::forward<Handler>(handler))();
}

//----------------------------------------------------------

/** Performs a composed request operation on a stream.

    This function performs 10 sequential async_read operations,
    simulating a higher-level protocol operation such as reading
    an HTTP request with headers and body.

    This demonstrates a 3-level composed operation: async_request
    calls async_read 10 times, each of which performs 10 read_some
    operations, for a total of 100 I/O operations.

    @param stream The stream to read from.
    @param handler The completion handler to invoke when done.
*/
template<class Stream, class Handler>
void async_request(Stream& stream, Handler&& handler)
{
    detail::request_op<Stream, std::decay_t<Handler>>(stream, std::forward<Handler>(handler))();
}

//----------------------------------------------------------

/** Performs a composed session operation on a stream.

    This function performs 10 sequential async_request operations,
    simulating a complete session that handles multiple requests
    over a persistent connection.

    This demonstrates a 4-level composed operation: async_session
    calls async_request 10 times, each of which performs 100 I/O
    operations, for a total of 1000 I/O operations.

    @param stream The stream to use for the session.
    @param handler The completion handler to invoke when done.
*/
template<class Stream, class Handler>
void async_session(Stream& stream, Handler&& handler)
{
    detail::session_op<Stream, std::decay_t<Handler>>(stream, std::forward<Handler>(handler))();
}

//----------------------------------------------------------
// Deferred definitions for detail ops that call free functions

template<class Stream, class Handler>
void detail::request_op<Stream, Handler>::operator()()
{
    if(count_++ < 10)
    {
        async_read(*stream_, std::move(*this));
        return;
    }
    stream_->get_executor().dispatch(std::move(handler_));
}

template<class Stream, class Handler>
void detail::session_op<Stream, Handler>::operator()()
{
    if(count_++ < 10)
    {
        async_request(*stream_, std::move(*this));
        return;
    }
    stream_->get_executor().dispatch(std::move(handler_));
}

} // cb

#endif
