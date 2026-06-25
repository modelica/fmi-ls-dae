cmake_minimum_required(VERSION 3.17)

set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

project(FMI-LS-DAE-FMUs C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

set(FMI_ARCHITECTURE "" CACHE STRING "FMI Architecture")
set_property(CACHE FMI_ARCHITECTURE PROPERTY STRINGS "" "aarch64" "x86_64")

if (NOT FMI_ARCHITECTURE)
  if (${CMAKE_HOST_SYSTEM_PROCESSOR} MATCHES "AMD64|x86_64")
    set(FMI_ARCHITECTURE "x86_64")
  elseif (${CMAKE_HOST_SYSTEM_PROCESSOR} MATCHES "aarch64|arm64")
    set(FMI_ARCHITECTURE "aarch64")
  else ()
    message(FATAL_ERROR "Unknown system architecture: ${CMAKE_HOST_SYSTEM_PROCESSOR}")
  endif ()
endif ()

if (WIN32)
  set(FMI_PLATFORM "${FMI_ARCHITECTURE}-windows")
elseif (APPLE)
  set(FMI_PLATFORM "${FMI_ARCHITECTURE}-darwin")
else ()
  set(FMI_PLATFORM "${FMI_ARCHITECTURE}-linux")
endif ()

if (APPLE)
  if ("${FMI_ARCHITECTURE}" STREQUAL "x86_64")
    set(CMAKE_OSX_ARCHITECTURES "x86_64")
  elseif ("${FMI_ARCHITECTURE}" STREQUAL "aarch64")
    set(CMAKE_OSX_ARCHITECTURES "arm64")
  else ()
    message(FATAL_ERROR "Unsupported architecture for darwin: ${FMI_ARCHITECTURE}")
  endif ()
endif ()

if (MSVC)
  add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
endif ()

if (UNIX)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fvisibility=hidden")
endif ()

message(STATUS "FMI_PLATFORM: ${FMI_PLATFORM}")

set(MODEL_NAME SimpleDAE)

set(HEADERS
  ${MODEL_NAME}/config.h
  include/model.h
  include/fmi3Functions.h
  include/fmi3FunctionTypes.h
  include/fmi3PlatformTypes.h
)

set(SOURCES
  ${MODEL_NAME}/model.c
  src/fmi3Functions.c
  src/model_instance.c
)

add_library(${MODEL_NAME} SHARED
  ${HEADERS}
  ${SOURCES}
  ${MODEL_NAME}/modelDescription.xml
  ${MODEL_NAME}/buildDescription.xml
)

file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/fmus)

target_compile_definitions(${MODEL_NAME} PRIVATE
  FMI_VERSION=3
  DISABLE_PREFIX
)

if (MSVC)
  target_compile_options(${MODEL_NAME} PRIVATE /W4 /WX)
else ()
  target_compile_options(${MODEL_NAME} PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif ()

if (CMAKE_C_COMPILER_ID STREQUAL "GNU")
  target_link_options(${MODEL_NAME} PRIVATE "-static-libgcc")
endif ()

if (CMAKE_C_COMPILER_ID STREQUAL "Intel")
  target_link_options(${MODEL_NAME} PRIVATE "-static-intel" "-static-libgcc")
endif ()

target_include_directories(${MODEL_NAME} PRIVATE
  include
  ${MODEL_NAME}
)

set(FMU_BUILD_DIR temp/${MODEL_NAME})

set_target_properties(${MODEL_NAME} PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY         "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  RUNTIME_OUTPUT_DIRECTORY_DEBUG   "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  RUNTIME_OUTPUT_DIRECTORY_RELEASE "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  LIBRARY_OUTPUT_DIRECTORY         "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  LIBRARY_OUTPUT_DIRECTORY_DEBUG   "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  LIBRARY_OUTPUT_DIRECTORY_RELEASE "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  ARCHIVE_OUTPUT_DIRECTORY         "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  ARCHIVE_OUTPUT_DIRECTORY_DEBUG   "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  ARCHIVE_OUTPUT_DIRECTORY_RELEASE "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}"
  PREFIX ""
  OUTPUT_NAME ${MODEL_NAME}
)

# modelDescription.xml
add_custom_command(TARGET ${MODEL_NAME} POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_SOURCE_DIR}/${MODEL_NAME}/modelDescription.xml
    "${FMU_BUILD_DIR}/modelDescription.xml"
)

# model-specific sources
foreach (SOURCE_FILE config.h model.c)
  add_custom_command(TARGET ${MODEL_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
      "${CMAKE_CURRENT_SOURCE_DIR}/${MODEL_NAME}/${SOURCE_FILE}"
      "${FMU_BUILD_DIR}/sources/${SOURCE_FILE}"
  )
endforeach ()

# shared headers
foreach (SOURCE_FILE model.h)
  add_custom_command(TARGET ${MODEL_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
      "${CMAKE_CURRENT_SOURCE_DIR}/include/${SOURCE_FILE}"
      "${FMU_BUILD_DIR}/sources/${SOURCE_FILE}"
  )
endforeach ()

# shared sources
foreach (SOURCE_FILE fmi3Functions.c model_instance.c)
  add_custom_command(TARGET ${MODEL_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
      "${CMAKE_CURRENT_SOURCE_DIR}/src/${SOURCE_FILE}"
      "${FMU_BUILD_DIR}/sources/${SOURCE_FILE}"
  )
endforeach ()

# buildDescription.xml
add_custom_command(TARGET ${MODEL_NAME} POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy
    "${CMAKE_CURRENT_SOURCE_DIR}/${MODEL_NAME}/buildDescription.xml"
    "${FMU_BUILD_DIR}/sources/buildDescription.xml"
)

# fmi-ls-dae manifest (must live at extra/org.fmi-standard.fmi-ls-dae/ inside the FMU)
add_custom_command(TARGET ${MODEL_NAME} POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy
    "${CMAKE_CURRENT_SOURCE_DIR}/${MODEL_NAME}/fmi-ls-manifest.xml"
    "${FMU_BUILD_DIR}/extra/org.fmi-standard.fmi-ls-dae/fmi-ls-manifest.xml"
)

# remove MSVC import library artifacts (Release only)
if (MSVC)
  add_custom_command(TARGET ${MODEL_NAME} POST_BUILD
    COMMAND if $<CONFIG:Release> neq 0 (
      ${CMAKE_COMMAND} -E rm -f
        "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}/${MODEL_NAME}.exp"
        "${FMU_BUILD_DIR}/binaries/${FMI_PLATFORM}/${MODEL_NAME}.lib"
    )
  )
endif ()

# package as FMU (ZIP archive)
add_custom_command(TARGET ${MODEL_NAME} POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E tar cf
    ${CMAKE_CURRENT_BINARY_DIR}/fmus/${MODEL_NAME}.fmu --format=zip
    modelDescription.xml binaries sources extra
  WORKING_DIRECTORY ${FMU_BUILD_DIR}
  COMMENT "Creating ${MODEL_NAME}.fmu"
)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/fmus/${MODEL_NAME}.fmu
  DESTINATION ${CMAKE_INSTALL_PREFIX}
)
