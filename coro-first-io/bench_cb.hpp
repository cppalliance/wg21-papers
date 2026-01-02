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

#include <cstddef>
#include <utility>

namespace cb {

//----------------------------------------------------------
// Thread-local cache for operation recycling

struct op_cache
{
    static void* allocate(std::size_t n)
    {
        auto& c = get();
        if(c.ptr_ && c.size_ >= n)
        {
            void* p = c.ptr_;
            c.ptr_ = nullptr;
            return p;
        }
        return ::operator new(n);
    }

    static void deallocate(void* p, std::size_t n)
    {
        auto& c = get();
        if(!c.ptr_ || n >= c.size_)
        {
            ::operator delete(c.ptr_);
            c.ptr_ = p;
            c.size_ = n;
        }
        else
        {
            ::operator delete(p);
        }
    }

private:
    void* ptr_ = nullptr;
    std::size_t size_ = 0;

    static op_cache& get()
    {
        static thread_local op_cache c;
        return c;
    }
};

//----------------------------------------------------------
// Native callback operations

template<class Executor, class Handler>
struct io_op : work
{
    Executor ex_;
    Handler handler_;

    io_op(Executor ex, Handler h)
        : ex_(ex), handler_(std::move(h)) {}

    static void* operator new(std::size_t n)
    {
        return op_cache::allocate(n);
    }

    static void operator delete(void* p, std::size_t n)
    {
        op_cache::deallocate(p, n);
    }

    void operator()() override
    {
        auto h = std::move(handler_);
        auto ex = ex_;
        delete this;
        ex.dispatch(std::move(h));
    }
};

//----------------------------------------------------------

template<class Executor>
struct socket
{
    Executor ex_;

    explicit socket(Executor ex)
        : ex_(ex) {}

    Executor get_executor() const { return ex_; }

    template<class Handler>
    void async_io(Handler&& handler)
    {
        using op_t = io_op<Executor, std::decay_t<Handler>>;
        ex_.post(new op_t(ex_, std::forward<Handler>(handler)));
    }
};

//----------------------------------------------------------

template<class Executor, class Handler>
void async_read_some(socket<Executor>& sock, Handler&& handler)
{
    sock.async_io(std::forward<Handler>(handler));
}

//----------------------------------------------------------

template<class Executor, class Handler>
struct read_op
{
    socket<Executor>* sock_;
    Handler handler_;
    int count_ = 0;

    read_op(socket<Executor>& sock, Handler h)
        : sock_(&sock), handler_(std::move(h)) {}

    void operator()()
    {
        // async_read calls async_read_some 10 times
        if(count_++ < 10)
        {
            async_read_some(*sock_, std::move(*this));
            return;
        }
        sock_->get_executor().dispatch(std::move(handler_));
    }
};

template<class Executor, class Handler>
void async_read(socket<Executor>& sock, Handler&& handler)
{
    read_op<Executor, std::decay_t<Handler>>(sock, std::forward<Handler>(handler))();
}

//----------------------------------------------------------

template<class Executor, class Handler>
struct request_op
{
    socket<Executor>* sock_;
    Handler handler_;
    int count_ = 0;

    request_op(socket<Executor>& sock, Handler h)
        : sock_(&sock), handler_(std::move(h)) {}

    void operator()()
    {
        // async_request calls async_read 10 times
        if(count_++ < 10)
        {
            async_read(*sock_, std::move(*this));
            return;
        }
        sock_->get_executor().dispatch(std::move(handler_));
    }
};

template<class Executor, class Handler>
void async_request(socket<Executor>& sock, Handler&& handler)
{
    request_op<Executor, std::decay_t<Handler>>(sock, std::forward<Handler>(handler))();
}

} // cb

#endif
