#pragma once

#ifdef _WIN32
  #define libmemcached_EXPORT __declspec(dllexport)
#else
  #define libmemcached_EXPORT
#endif

libmemcached_EXPORT void libmemcached();
