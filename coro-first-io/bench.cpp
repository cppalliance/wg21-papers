//
// Copyright (c) 2025 Vinnie Falco (vinnie dot falco at gmail dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
// Official repository: https://github.com/cppalliance/wg21-papers/coro-first-io
//

#include "bench_cb.hpp"
#include "bench_co.hpp"

#include <chrono>
#include <iostream>
#include <cstdlib>
#include <new>

static std::size_t g_alloc_count = 0;
std::size_t g_io_count = 0;
std::size_t g_work_count = 0;

void* operator new(std::size_t size)
{
    ++g_alloc_count;
    void* p = std::malloc(size);
    if(!p) throw std::bad_alloc();
    return p;
}

void operator delete(void* p) noexcept
{
    std::free(p);
}

void operator delete(void* p, std::size_t) noexcept
{
    std::free(p);
}

struct bench_result
{
    long long ns;
    std::size_t allocs;
    std::size_t ios;
    std::size_t works;
};

struct bench_test
{
    static constexpr int N = 100000;

    template<class Socket, class AsyncOp>
    static bench_result bench(Socket& sock, AsyncOp op)
    {
        using clock = std::chrono::high_resolution_clock;
        auto& ioc = *sock.get_executor().ctx_;
        int count = 0;

        g_alloc_count = 0;
        g_io_count = 0;
        g_work_count = 0;
        auto t0 = clock::now();
        for (int i = 0; i < N; ++i)
        {
            op(sock, [&count]{ ++count; });
            ioc.run();
        }
        auto t1 = clock::now();

        auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
        return { ns / N, g_alloc_count / N, g_io_count / N, g_work_count / N };
    }

    template<class MakeTask>
    static bench_result bench_co(io_context& ioc, MakeTask make_task)
    {
        using clock = std::chrono::high_resolution_clock;
        int count = 0;

        g_alloc_count = 0;
        g_io_count = 0;
        g_work_count = 0;
        auto t0 = clock::now();
        for (int i = 0; i < N; ++i)
        {
            co::async_run(ioc.get_executor(), make_task(count));
            ioc.run();
        }
        auto t1 = clock::now();

        auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
        return { ns / N, g_alloc_count / N, g_io_count / N, g_work_count / N };
    }

    static void print_line(char const* name, char const* type, bench_result const& r, bench_result const& other)
    {
        std::cout << name << type << r.ns << " ns/op";
        if (r.allocs != 0)
            std::cout << ", " << r.allocs << " allocs/op";
        if (r.ios != other.ios)
            std::cout << ", " << r.ios << " io/op";
        if (r.works != other.works)
            std::cout << ", " << r.works << " work/op";
        std::cout << "\n";
    }

    static void print_results(char const* name, bench_result const& cb, bench_result const& co)
    {
        print_line(name, "callback: ", cb, co);
        print_line(name, "coro:     ", co, cb);
    }

    void
    run()
    {
        std::cout << "\n";

        io_context ioc;
        cb::socket cb_sock(ioc.get_executor());
        co::socket co_sock;

        bench_result cb, co;

        // 1 call
        cb = bench(cb_sock, [](auto& sock, auto h){ sock.async_read_some(std::move(h)); });
        co = bench_co(ioc, [&](int& count) -> co::task { co_await co_sock.async_read_some(); ++count; });
        print_results("read_some        ", cb, co);

        std::cout << "\n";

        // 10 calls
        cb = bench(cb_sock, [](auto& sock, auto h){ cb::async_read(sock, std::move(h)); });
        co = bench_co(ioc, [&](int& count) -> co::task { co_await co::async_read(co_sock); ++count; });
        print_results("async_read       ", cb, co);

        std::cout << "\n";

        // 100 calls
        cb = bench(cb_sock, [](auto& sock, auto h){ cb::async_request(sock, std::move(h)); });
        co = bench_co(ioc, [&](int& count) -> co::task { co_await co::async_request(co_sock); ++count; });
        print_results("async_request    ", cb, co);

        std::cout << "\n";

        // 1000 calls
        cb = bench(cb_sock, [](auto& sock, auto h){ cb::async_session(sock, std::move(h)); });
        co = bench_co(ioc, [&](int& count) -> co::task { co_await co::async_session(co_sock); ++count; });
        print_results("async_session    ", cb, co);
    }
};

int main()
{
    bench_test t;
    t.run();
    return 0;
}
