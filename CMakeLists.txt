cmake_minimum_required(VERSION 3.15...4.0)

if(CMAKE_HOST_APPLE OR CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(CMAKE_OSX_DEPLOYMENT_TARGET "13.3" CACHE STRING
      "Minimum macOS deployment version" FORCE)
endif()

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(nanobind CONFIG REQUIRED)
nanobind_add_module(_core
  src/main.cpp
  src/cuts.cpp
  src/grids.cpp
  src/swe.cpp
  src/text_cursor.cpp
)
target_compile_features(_core PRIVATE cxx_std_20)

include(cmake/CPM.cmake)

CPMAddPackage(
  NAME fast_float
  GITHUB_REPOSITORY "fastfloat/fast_float"
  GIT_TAG v8.2.10)
target_link_libraries(_core PUBLIC fast_float)

install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})
