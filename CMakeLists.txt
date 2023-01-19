cmake_minimum_required(VERSION 3.15)
project(libmemcached CXX)

add_library(libmemcached src/libmemcached.cpp)
target_include_directories(libmemcached PUBLIC include)

set_target_properties(libmemcached PROPERTIES PUBLIC_HEADER "include/libmemcached.h")
install(TARGETS libmemcached)
