#
# Copyright (c) 2025 Vinnie Falco (vinnie dot falco at gmail dot com)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
# Official repository: https://github.com/cppalliance/wg21-papers/coro-first-io
#

cmake_minimum_required(VERSION 3.16)
project(capy-bench LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(SOURCES
    bench.cpp
    bench.hpp
    bench_cb.hpp
    bench_co.hpp
)

add_executable(bench ${SOURCES})

source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})

target_include_directories(bench PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Platform-specific settings
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(bench PRIVATE -fcoroutines -Wall -Wextra -Wpedantic)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(bench PRIVATE -stdlib=libc++ -Wall -Wextra -Wpedantic)
    target_link_options(bench PRIVATE -stdlib=libc++)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(bench PRIVATE /W4 /permissive-)
endif()

# Threading support
find_package(Threads REQUIRED)
target_link_libraries(bench PRIVATE Threads::Threads)
