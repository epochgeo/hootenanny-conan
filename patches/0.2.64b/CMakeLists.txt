cmake_minimum_required(VERSION 3.5)
project(hootenanny)

add_definitions("-std=c++11")
set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_program(CCACHE_FOUND ccache)
if(CCACHE_FOUND)
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
endif(CCACHE_FOUND)

# Remove me when it all works!
set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -w")
# We're linking statically and for some reason the version check fails in centos 8
#set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -DQT_NO_VERSION_TAGGING")

# This define is required for the precompiled headers to work properly
set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -DQT_CORE_LIB")
#set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -DVALIDATE_ON")
#set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -O0")

#set(CMAKE_CXX_COMPILER_LAUNCHER ccache)

#find_package(Boost)
#include_directories(${Boost_INCLUDE_DIRS})
#find_package(GDAL)
#include_directories(${GDAL_INCLUDE_DIRS})
#find_package(coinglpk MODULE REQUIRED)
#find_package(liboauthcpp)
#include_directories(${liboauthcpp_INCLUDE_DIRS})
#find_package(OpenCV)
#include_directories(${opencv_INCLUDE_DIRS})
#find_package(OpenSSL)
#include_directories(${OpenSSL_INCLUDE_DIRS})
#find_package(Protobuf)
#include_directories(${protobuf_INCLUDE_DIRS})
#find_package(Qt5)
#include_directories(${Qt5_INCLUDE_DIRS})
#find_package(libphonenumber REQUIRED)
#include_directories(${libphonenumber_INCLUDE_DIRS})
#link_directories(${libphonenumber_LIB_DIRS})

find_library(STXXL_LIBRARIES stxxl REQUIRED)
#find_library(libpostal_LIBRARIES postal REQUIRED)
find_package(JNI REQUIRED)

set(
    CONAN_LIBS
    ${Boost_LIBRARIES}
    ${GDAL_LIBRARIES}
    ${GLPK_LIBRARIES}
    ${liboauthcpp_LIBRARIES}
    #${libpostal_LIBRARIES}
    ${opencv_LIBRARIES}
    ${OpenSSL_LIBRARIES}
    ${protobuf_LIBRARIES}
    ${Qt5_LIBRARIES}
    ${STXXL_LIBRARIES}
    gssapi_krb5
)

set(
    CONAN_INCLUDE_DIRS
    ${Boost_INCLUDE_DIRS}
    ${GDAL_INCLUDE_DIRS}
    ${GLPK_INCLUDE_DIRS}
    ${liboauthcpp_INCLUDE_DIRS}
    ${opencv_INCLUDE_DIRS}
    ${OpenSSL_INCLUDE_DIRS}
    ${protobuf_INCLUDE_DIRS}
    ${Qt5_INCLUDE_DIRS}
    ${libphonenumber_INCLUDE_DIRS}
)

#
# v8
#
#find_path(V8_HEADER_PATH 
#    libplatform/libplatform.h
#    PATHS /usr/include/node/ /usr/include/nodejs/deps/v8/include/
#    REQUIRED
#)
#find_library(V8_LIBS
#    v8
#    HINTS /usr/lib/x86_64-linux-gnu/ /usr/lib64
#    REQUIRED
#)
#message(${V8_LIBS})

#
# node.js
#
#set(NODEJS_SEARCH_PATHS 
#    /usr/include/nodejs /usr/include/node /usr/include/nodejs/deps/uv/include)
#find_path(HOOT_HAVE_NODEJS_SRC_NODE_H 
#    NAMES nodejs/src/node.h
#    HINTS ${NODEJS_SEARCH_PATHS}
#)
#if (EXISTS ${HOOT_HAVE_NODEJS_SRC_NODE_H})
#    add_compile_definitions(HOOT_HAVE_NODEJS_SRC_NODE_H)
#endif()
#
#find_path(HOOT_HAVE_NODEJS_NODE_H 
#    NAMES nodejs/node.h
#    HINTS ${NODEJS_SEARCH_PATHS}
#)
#if (EXISTS ${HOOT_HAVE_NODEJS_NODE_H})
#    add_compile_definitions(HOOT_HAVE_NODEJS_NODE_H)
#endif()
#
##find_path(HOOT_HAVE_NODE_NODE_H 
#    NAMES node/node.h
#    HINTS ${NODEJS_SEARCH_PATHS}
#)
#if (EXISTS ${HOOT_HAVE_NODE_NODE_H})
#    add_compile_definitions(HOOT_HAVE_NODE_NODE_H)
#endif()
add_compile_definitions(HOOT_HAVE_NODE_NODE_H)

#find_library(NODEJS_LIBS
#    node
#    HINTS /usr/lib/x86_64-linux-gnu/ /usr/lib64
#    REQUIRED
#)
#set(NODEJS_LIBS "")

#include(${CMAKE_CURRENT_SOURCE_DIR}/../conanbuildinfo.txt)
#include(${CMAKE_CURRENT_LIST_DIR}/../conanbuildinfo.txt)
#include(${CMAKE_BINARY_DIR}/conan_toolchain.cmake)
#include("../conanbuildinfo.txt")
#message(${CMAKE_CURRENT_SOURCE_DIR})
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(Qt5 REQUIRED)
#set(CMAKE_AUTOMOC ON)

list(REMOVE_DUPLICATES CONAN_LIBS)

list(FILTER CONAN_LIBS EXCLUDE REGEX "^fontenc.*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^X.*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^xcb.*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^uuid.*")
#list(FILTER CONAN_LIBS EXCLUDE REGEX "^opencv.*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^ICE*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^SM*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^xkbfile*")
list(APPEND CONAN_LIBS opencv_core opencv_imgproc)
message(CONAN_LIBS)

# libphonenumber builds both static and dynamic, remove dynamic linking
list(REMOVE_ITEM CONAN_LIBS
    phonenumber
)

# Add libphonenumber static linking back in.
set(EXTRA_LIBS
    libphonenumber.a
    libgeocoding.a
    # Provided by libnode
    node
#    libv8_compiler.a
#    libv8_base_without_compiler.a
#    libv8_init.a
#    libv8_initializers.a
#    libv8_libbase.a
#    libv8_libplatform.a
#    libv8_libsampler.a
#    libv8_snapshot.a
#    libv8_zlib.a
#    libbrotli.a
#    libhistogram.a
#    libuvwasi.a
#    libuv.a
#    libcares.a
#    libllhttp.a
#    libnghttp2.a
#    libgtest.a
#    libgtest_main.a
#    libopenssl.a
#    libzlib.a
#    libicuucx.a
#    libicustubdata.a
#    libicui18n.a
#    libicudata.a
)

list(REMOVE_ITEM CONAN_LIBS ${EXTRA_LIBS})
list(PREPEND CONAN_LIBS ${EXTRA_LIBS})
#list(REMOVE_DUPLICATES CONAN_LIBS)

set(
    CONAN_INCLUDE_DIRS
    ${Boost_INCLUDE_DIRS}
    ${GDAL_INCLUDE_DIRS}
    ${GLPK_INCLUDE_DIRS}
    ${liboauthcpp_INCLUDE_DIRS}
)

set(HOOT_HOME ${PROJECT_SOURCE_DIR})
message(${HOOT_HOME})

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

add_library(Tbs
    STATIC
    ${TBS_FILES}
)
target_include_directories(Tbs PUBLIC ${TBS_SRC_PATH})
target_link_libraries(
    Tbs
    ${CONAN_LIBS}
)

#
# TGS
#

set(TGS_SRC_PATH ${HOOT_HOME}/tgs/src/main/cpp)

file(GLOB_RECURSE TGS_HEADER_FILES CONFIGURE_DEPENDS 
    ${TGS_SRC_PATH}/*.h
)

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

set(TGS_FILES 
    ${TGS_SRC_FILES}
    ${TGS_HEADER_FILES}
)
add_library(Tgs
    STATIC
    ${TGS_FILES}
)

target_include_directories(Tgs PUBLIC ${HOOT_HOME}/tgs/src/main/cpp/)
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

# Remove python translation -- not used much anymore
list(REMOVE_ITEM HOOT_CORE_FILES 
    ${HOOT_CORE_SRC_PATH}/hoot/core/schema/PythonSchemaTranslator.cpp
)

# Remove libpostal dependencies, we can add this back later.
list(REMOVE_ITEM HOOT_CORE_FILES
    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/address/LibPostalInit.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/address/AddressParser.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/address/AddressNormalizer.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/language/ToEnglishAddressTranslator.cpp
    ${HOOT_CORE_SRC_PATH}/hoot/core/schema/PythonSchemaTranslator.cpp
)

# Remove phonenumber dependencies, we can add this back later.
#list(REMOVE_ITEM HOOT_CORE_FILES 
#    ${HOOT_CORE_SRC_PATH}/hoot/core/algorithms/extractors/poi-polygon/PoiPolygonPhoneNumberScoreExtractor.cpp
#    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/phone/PhoneNumberLocator.cpp
#    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/phone/PhoneNumberNormalizer.cpp
#    ${HOOT_CORE_SRC_PATH}/hoot/core/conflate/phone/PhoneNumberParser.cpp
#    ${HOOT_CORE_SRC_PATH}/hoot/core/visitors/NormalizePhoneNumbersVisitor.cpp
#    ${HOOT_CORE_SRC_PATH}/hoot/core/visitors/PhoneNumberLocateVisitor.cpp
#)

# AUTOMOC doesn't work, probably due to our naming convention
set(HOOT_CORE_MOC_PATH 
    ${HOOT_CORE_SRC_PATH}/hoot/core/io/OgrWriterThread.h
    ${HOOT_CORE_SRC_PATH}/hoot/core/io/ElementTranslatorThread.h
)
qt5_wrap_cpp(HOOT_CORE_MOC_FILES ${HOOT_CORE_MOC_PATH})

add_library(HootCore
    ${HOOT_CORE_FILES}
    ${HOOT_CORE_MOC_FILES}
    ${HOOT_CORE_SRC_PATH}/hoot/core/info/VersionDefines.h
    ${HOOT_CORE_SRC_PATH}/hoot/core/util/ConfigOptions.h
    ${HOOT_CORE_SRC_PATH}/hoot/core/util/ConfigDefaults.h
    ${PROTO_OUTPUT_FILES}
)

message(${HOOT_CORE_SRC_PATH})
target_include_directories(
    HootCore
    PUBLIC
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
message(${CONAN_LIBS})
target_link_libraries(
    HootCore
    Tbs
    Tgs
    ${CONAN_LIBS}
)

#
# Hoot JS
#

file(GLOB_RECURSE HOOT_JS_FILES CONFIGURE_DEPENDS 
    ${HOOT_JS_SRC_PATH}/*.h
    ${HOOT_JS_SRC_PATH}/*.cpp
)

add_library(HootJs
    ${HOOT_JS_FILES}
)
target_include_directories(
    HootJs
    PUBLIC
    ${HOOT_CORE_SRC_PATH}
    ${TBS_SRC_PATH}
    ${TGS_SRC_PATH}
    ${HOOT_JS_SRC_PATH}
    ${NODEJS_HEADER_PATH}
    ${V8_HEADER_PATH}
    ${CONAN_INCLUDE_DIRS}
)
target_link_libraries(
    HootJs
    Tbs
    Tgs
    HootCore
    ${CONAN_LIBS}
)

#
# Hoot JOSM
#

set(HOOT_JOSM_SRC_PATH ${HOOT_HOME}/hoot-josm/src/main/cpp)
file(GLOB_RECURSE HOOT_JOSM_FILES CONFIGURE_DEPENDS 
    ${HOOT_JOSM_SRC_PATH}/*.h
    ${HOOT_JOSM_SRC_PATH}/*.cpp
)
message(${HOOT_JOSM_SRC_PATH})

#
# Hoot Core Test
#

set(HOOT_CORE_TEST_SRC_PATH ${HOOT_HOME}/hoot-core-test/src/test/cpp)
file(GLOB_RECURSE HOOT_CORE_TEST_FILES CONFIGURE_DEPENDS 
    ${HOOT_CORE_TEST_SRC_PATH}/*/TestUtils.h
    ${HOOT_CORE_TEST_SRC_PATH}/*/TestUtils.cpp
)
message(${HOOT_CORE_TEST_FILES})


#
# Hoot Test
#

set(HOOT_TEST_SRC_PATH ${HOOT_HOME}/hoot-test/src/main/cpp/)

file(GLOB_RECURSE HOOT_TEST_FILES CONFIGURE_DEPENDS 
    ${HOOT_TEST_SRC_PATH}/*.h
    ${HOOT_TEST_SRC_PATH}/*.cpp
)

set(HOOT_TEST_INCLUDES
    ${HOOT_TEST_SRC_PATH}
    ${HOOT_JOSM_SRC_PATH}
    ${HOOT_CORE_SRC_PATH}
    ${HOOT_CORE_TEST_SRC_PATH}
    ${TBS_SRC_PATH}
    ${TGS_SRC_PATH}
    ${HOOT_JS_SRC_PATH}
    ${V8_HEADER_PATH}
    ${JNI_INCLUDE_DIRS}
    ${CONAN_INCLUDE_DIRS}
) 

add_library(
    HootTestLib
    ${HOOT_TEST_FILES}
    ${HOOT_JOSM_FILES}
    ${HOOT_CORE_TEST_FILES}
)
set_target_properties(HootTestLib PROPERTIES OUTPUT_NAME HootTest)
set_property(TARGET HootTestLib PROPERTY POSITION_INDEPENDENT_CODE ON)
target_compile_options(HootTestLib PRIVATE -fPIC)
target_include_directories(
    HootTestLib
    PUBLIC
    ${HOOT_TEST_INCLUDES}
)
target_link_libraries(
    HootTestLib
    HootJs
    HootCore
    Tbs
    Tgs
    ${JNI_LIBRARIES}
    ${CONAN_LIBS}
)

add_executable(
    HootTest
    ${HOOT_TEST_FILES}
    # Lazy, no need to create a separate lib
    ${HOOT_JOSM_FILES}
    ${HOOT_CORE_TEST_FILES}
)
# This is required by Qt
set_property(TARGET HootTest PROPERTY POSITION_INDEPENDENT_CODE ON)
target_compile_options(HootTest PRIVATE -fPIC)
target_include_directories(
    HootTest
    PUBLIC
    ${HOOT_TEST_INCLUDES}
)
target_link_libraries(
    HootTest
    HootJs
    HootCore
    Tbs
    Tgs
    ${JNI_LIBRARIES}
    ${CONAN_LIBS}
)

#
# Hoot Cmd
#

set(HOOT_CMD_SRC_PATH ${HOOT_HOME}/hoot-cmd/src/main/cpp/)

file(GLOB_RECURSE HOOT_CMD_FILES CONFIGURE_DEPENDS 
    ${HOOT_CMD_SRC_PATH}/*.h
    ${HOOT_CMD_SRC_PATH}/*.cpp
)


add_executable(
    hoot.bin
    ${HOOT_CMD_FILES}
)
# This is required by Qt
set_property(TARGET hoot.bin PROPERTY POSITION_INDEPENDENT_CODE ON)
target_compile_options(hoot.bin PRIVATE -fPIC)
target_include_directories(
    hoot.bin
    PUBLIC
    ${HOOT_CORE_SRC_PATH}
    ${TBS_SRC_PATH}
    ${TGS_SRC_PATH}
    ${HOOT_JS_SRC_PATH}
    ${V8_HEADER_PATH}
    ${CONAN_INCLUDE_DIRS}
)
target_link_libraries(
    hoot.bin
    HootJs
    HootCore
    Tbs
    Tgs
    ${CONAN_LIBS}
)


install(TARGETS ${installable_libs}
    LIBRARY DESTINATION lib
    PUBLIC_HEADER DESTINATION include
)
install(FILES ${HOOT_HOME}/scripts/HootEnv.sh DESTINATION bin)
install(FILES ${HOOT_HOME}/scripts/RunHoot.sh DESTINATION bin RENAME hoot)
install(DIRECTORY ${HOOT_HOME}/conf DESTINATION .)
install(DIRECTORY ${CONAN_RES_DIRS_GDAL}/gdal DESTINATION .)
install(FILES ${CONAN_RES_DIRS_PROJ}/proj.db DESTINATION .)

