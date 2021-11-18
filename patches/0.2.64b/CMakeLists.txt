cmake_minimum_required(VERSION 2.8.12)
project(hootenanny)

add_definitions("-std=c++11")

# Remove me when it all works!
set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -w")

# v8
find_path(V8_HEADER_PATH v8.h
    /usr/include/node/
    /usr/include/nodejs/deps/v8/include/
)

# Python Includes
find_path(PYTHON_HEADER_PATH Python.h
    /usr/include/python3.8/
)

#include(${CMAKE_CURRENT_LIST_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()

option(BUILD_SHARED_LIBS "Build using shared libraries" OFF)

set(HOOT_HOME ${PROJECT_SOURCE_DIR})
message(${HOOT_HOME})

# This avoids linker errors w/ older versions of glibc
# https://github.com/AppImage/AppImageKit/tree/stable/v1.0/LibcWrapGenerator
set(CMAKE_CXX_FLAGS  "-include ${HOOT_HOME}/libcwrap.h ${CMAKE_CXX_FLAGS} -w")

#
# valac - this is used to avoid glibc errors
#

# wget https://raw.githubusercontent.com/AppImage/AppImageKit/stable/v1.0/LibcWrapGenerator/LibcWrapGenerator.vala
# valac --pkg gee-0.8 --pkg posix --pkg glib-2.0 --pkg gio-2.0 LibcWrapGenerator.vala
#  ./LibcWrapGenerator --target 2.10 --libdir /lib --output libcwrap.h

#
# TBS
#

set(TBS_SRC_PATH ${HOOT_HOME}/tbs/src/main/cpp)

file(GLOB TBS_FILES CONFIGURE_DEPENDS 
    ${TBS_SRC_PATH}/tbs/stats/*.h
    ${TBS_SRC_PATH}/tbs/stats/*.cpp
    ${TBS_SRC_PATH}/tbs/optimization/*.h
    ${TBS_SRC_PATH}/tbs/optimization/*.cpp
)

add_library(Tbs ${TBS_FILES})

target_include_directories(
    Tbs PRIVATE ${TBS_SRC_PATH})
target_link_libraries(Tbs ${CONAN_LIBS})

#
# TGS
#

set(TGS_SRC_PATH ${HOOT_HOME}/tgs/src/main/cpp)

file(GLOB_RECURSE TGS_HEADER_FILES CONFIGURE_DEPENDS 
    ${TGS_SRC_PATH}/*.h)

# We're specifying specific files b/c not all files are actively maintained anymore.
file(GLOB TGS_SRC_FILES CONFIGURE_DEPENDS
    ${TGS_SRC_PATH}/tgs/*.cpp
    ${TGS_SRC_PATH}/tgs/DelaunayTriangulation/*.cpp
    ${TGS_SRC_PATH}/tgs/Interpolation/*.cpp
    ${TGS_SRC_PATH}/tgs/Optimization/*.cpp
    ${TGS_SRC_PATH}/tgs/ProbablePath/*.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/DataFrame.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/InfoGainCalculator.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/BaseRandomForest.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/RandomForest.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/BaseRandomForestManager.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/RandomForestManager.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/RandomTree.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/MissingDataHandler.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/MultithreadedRandomForest.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/MultithreadedRandomForestManager.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/RandomForestThread.cpp
    ${TGS_SRC_PATH}/tgs/RandomForest/RandomForestUtilities.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/Box.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/HilbertRTree.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/IntersectionIterator.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/KnnIterator.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/KnnIteratorNd.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/MemoryPageStore.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/Page.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/RStarTree.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/RStarTreePrinter.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/RTreeNode.cpp
    ${TGS_SRC_PATH}/tgs/RStarTree/RTreeNodeStore.cpp
    ${TGS_SRC_PATH}/tgs/Statistics/*.cpp
    ${TGS_SRC_PATH}/tgs/System/*.cpp
)

set(TGS_FILES ${TGS_SRC_FILES} ${TGS_HEADER_FILES})
add_library(Tgs ${TGS_FILES})

target_include_directories(
    Tgs PRIVATE ${HOOT_HOME}/tgs/src/main/cpp/)
target_link_libraries(Tgs ${CONAN_LIBS})

set(HOOT_CORE_SRC_PATH ${HOOT_HOME}/hoot-core/src/main/cpp/)
set(HOOT_JS_SRC_PATH ${HOOT_HOME}/hoot-js/src/main/cpp/)

#
# Hoot Config Options
#

add_custom_command(
    OUTPUT
        ${HOOT_CORE_SRC_PATH}/hoot/core/util/ConfigOptions.h
        ${HOOT_CORE_SRC_PATH}/hoot/core/util/ConfigDefaults.h
    COMMAND 
        python ${HOOT_HOME}/scripts/core/CreateConfigCode.py 
        ${HOOT_HOME}/conf/core/ConfigOptions.asciidoc 
        ${HOOT_CORE_SRC_PATH}/hoot/core/util/ConfigOptions.h
        ${HOOT_CORE_SRC_PATH}/hoot/core/util/ConfigDefaults.h
)

#
# Protobuf
#

set(PROTO_PATH ${HOOT_CORE_SRC_PATH}/hoot/core/proto)

set(PROTO_OUTPUT_FILES
    ${PROTO_PATH}/OsmFormat.pb.cc
    ${PROTO_PATH}/OsmFormat.pb.h
    ${PROTO_PATH}/FileFormat.pb.cc
    ${PROTO_PATH}/FileFormat.pb.h
)

add_custom_command(
    OUTPUT ${PROTO_OUTPUT_FILES}
    COMMAND 
        protoc --cpp_out=${PROTO_PATH} -I${PROTO_PATH}
            ${PROTO_PATH}/OsmFormat.proto
            ${PROTO_PATH}/FileFormat.proto
)

#
# Hoot Core
#

add_custom_command(
    OUTPUT
        ${HOOT_CORE_SRC_PATH}/hoot/core/info/VersionDefines.h
    COMMAND 
        cd ${HOOT_HOME} ";" ./HOOT_VERSION_GEN
)

file(GLOB_RECURSE HOOT_CORE_FILES CONFIGURE_DEPENDS 
    ${HOOT_CORE_SRC_PATH}/*.h
    ${HOOT_CORE_SRC_PATH}/*.cpp
)

# Remove libpostal dependencies, we can add this back later.
list(REMOVE_ITEM HOOT_CORE_FILES 
    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/address/LegacyVertexMatcher.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/address/LibPostalInit.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/address/AddressParser.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/address/AddressNormalizer.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/language/ToEnglishAddressTranslator.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/schema/PythonSchemaTranslator.cpp
)


add_library(HootCore
    ${HOOT_CORE_FILES}
    ${HOOT_CORE_SRC_PATH}/hoot/core/info/VersionDefines.h
    ${HOOT_CORE_SRC_PATH}/hoot/core/util/ConfigOptions.h
    ${HOOT_CORE_SRC_PATH}/hoot/core/util/ConfigDefaults.h
    ${PROTO_OUTPUT_FILES}
)
message(${HOOT_CORE_SRC_PATH})
target_include_directories(
    HootCore PRIVATE 
    ${HOOT_CORE_SRC_PATH}
    ${TBS_SRC_PATH}
    ${TGS_SRC_PATH}
    ${HOOT_JS_SRC_PATH}
    ${V8_HEADER_PATH}
)
target_precompile_headers(
    HootCore PUBLIC 
    ${HOOT_CORE_SRC_PATH}/hoot/core/HootCoreStable.h
)
target_link_libraries(HootCore ${CONAN_LIBS} Tbs Tgs)

install(TARGETS ${installable_libs} DESTINATION lib)
