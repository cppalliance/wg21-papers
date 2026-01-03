#
# Copyright (c) 2025 Vinnie Falco (vinnie dot falco at gmail dot com)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
# Official repository: https://github.com/cppalliance/wg21-papers/coro-first-io
#

cmake_minimum_required(VERSION 3.16)
project(bench LANGUAGES CXX)

# Ensure GCC builds go in build-gcc directory
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    get_filename_component(BUILD_DIR_NAME ${CMAKE_BINARY_DIR} NAME)
    if(NOT BUILD_DIR_NAME STREQUAL "build-gcc")
        message(FATAL_ERROR "GCC builds must be configured in the 'build-gcc' directory.\n"
            "Current build directory: ${CMAKE_BINARY_DIR}\n"
            "Please run: cmake -B build-gcc -S .")
    endif()
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(SOURCES
    bench.cpp
    bench.hpp
    bench_cb.hpp
    bench_cb_detail.hpp
    bench_co.hpp
    bench_co_detail.hpp
)

add_executable(bench ${SOURCES})

source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})

target_include_directories(bench PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Platform-specific settings
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(bench PRIVATE -fcoroutines -Wall -Wextra -Wpedantic -O3 -march=native -flto -funroll-loops -DNDEBUG -ffast-math -fno-stack-protector -fno-unwind-tables -fno-asynchronous-unwind-tables)
    target_link_options(bench PRIVATE -flto -s -Wl,--as-needed)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(bench PRIVATE -stdlib=libc++ -Wall -Wextra -Wpedantic -O3 -march=native -flto -DNDEBUG)
    target_link_options(bench PRIVATE -stdlib=libc++ -flto)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(bench PRIVATE /W4 /permissive-)
    # Optimization flags for Release and RelWithDebInfo builds
    target_compile_options(bench PRIVATE 
        $<$<OR:$<CONFIG:Release>,$<CONFIG:RelWithDebInfo>>:/O2 /Ob2 /GL>
    )
    target_link_options(bench PRIVATE 
        $<$<OR:$<CONFIG:Release>,$<CONFIG:RelWithDebInfo>>:/LTCG>
    )
endif()

# Threading support
find_package(Threads REQUIRED)
target_link_libraries(bench PRIVATE Threads::Threads)

# Register as test for ctest
enable_testing()
add_test(NAME bench COMMAND bench)
