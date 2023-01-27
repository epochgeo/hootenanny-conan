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

find_library(STXXL_LIBRARIES stxxl REQUIRED)
find_library(libpostal_LIBRARIES postal REQUIRED)
find_package(JNI REQUIRED)

set(
    CONAN_LIBS
    ${Boost_LIBRARIES}
    ${GDAL_LIBRARIES}
    ${GLPK_LIBRARIES}
    ${liboauthcpp_LIBRARIES}
    ${libpostal_LIBRARIES}
    ${opencv_LIBRARIES}
    ${OpenSSL_LIBRARIES}
    ${protobuf_LIBRARIES}
    ${Qt5_LIBRARIES}
    ${STXXL_LIBRARIES}
    gssapi_krb5
    /home/vagrant/.pyenv/versions/3.7.14/lib/libpython3.7m.so
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

add_compile_definitions(HOOT_HAVE_NODE_NODE_H)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(Qt5 REQUIRED)
#set(CMAKE_AUTOMOC ON)

list(REMOVE_DUPLICATES CONAN_LIBS)

list(FILTER CONAN_LIBS EXCLUDE REGEX "^fontenc.*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^X.*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^xcb.*")
list(FILTER CONAN_LIBS EXCLUDE REGEX "^uuid.*")
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
    # link to node as a shared lib
#   node
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
    /home/vagrant/.pyenv/versions/3.7.14/include/python3.7m
        
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

