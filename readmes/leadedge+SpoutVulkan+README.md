# Spout Vulkan C++ examples

Based on the the C++ examples for Vulkan by [Sascha Willems](https://github.com/SaschaWillems/Vulkan) and the [Khronos samples](https://github.com/KhronosGroup/Vulkan-Samples), with reference to the article by [Nvidia](https://developer.nvidia.com/getting-vulkan-ready-vr)

Search on "SPOUT" in the example source files. The SpoutVK class demonstrates the principles for interop between Vulkan and DirectX. The "LinkVulkanImage" function gives an overview of the process. Code comments provide more details.

Although the code may not be immediately suitable for a particular application, the examples can be examined for creating a Spout sender or receiver. The Willems examples may be the easiest to reproduce and working binaries can be tested. The Khronos example repository is more complex but the "hello_triangle" example has been successfully modified.

## Willems "triangle" sender/receiver example

The "triangle" example (Basic triangle using Vulkan 1.0) is modified for building as a sender or receiver.

First clone and build the complete Willems example project as described in the [repository readme](https://github.com/SaschaWillems/Vulkan/blob/master/README.md). The Spout examples are for Windows and have been built and tested with Visual Studio 2022 and not with any other environment.

Find the "triangle" example folder 

..\Vulkan\examples\triangle

Copy the following files to this folder, replacing "triangle.cpp".

Examples\triangle.cpp\
Examples\SpoutVK.cpp\
Examples\SpoutVK.h\
Examples\SpoutDX -> folder containing Spout SDK files\
  All ".cpp" and ".h" files

Find the "triangle" example in the main project solution and "Set as startup project".

"Source Files > Add existing item" - add SpoutVK.cpp and SpoutVK.h.\
"Project > Add new filter" - add a new "SpoutDX" filter to the project.\
"SpoutDX > Add existing item" and add all the files in the SpoutSDK folder.\

"File > Save All"\
"Build > Build triangle"

"Debug > Start without debugging" to create and run a Spout sender.

After build, you will find "triangle.exe" in\
..\Vulkan\build\windows\bin - Debug or Release
Rename it to "triangle-sender.exe"

For a receiver\
Edit the file "triangle.cpp" and find -

// SPOUT
<pre>
#include "SpoutVK.h"
// #define BUILDRECEIVER // Make a receiver rather than a sender
</pre>

Enable the line "#define BUILDRECEIVER", save and build to create a receiver.]
After build, rename "triangle.exe" to "triangle-receiver.exe".

## Other Willems examples

Other examples can be readily modified as senders. For each project add the "SpoutSDK" filter and files as for the triangle example.  Modified source code of "bloom" and "vulkanscene" can be found in the "Examples" folder. Search on "SPOUT" for additions. Pre-built binaries can be found in the "Binaries" folder.

## Khronos "hello_triangle" sender/receiver example

Follow the [readme](https://github.com/KhronosGroup/Vulkan-Samples/blob/main/README.adoc) to clone the repository and the [build guide](https://github.com/KhronosGroup/Vulkan-Samples/blob/main/docs/build.adoc#windows)

Find the "hello_triangle" example folder 

..\Vulkan_Samples\Samples\hello_triangle

Copy the following files to this folder, replacing "hello_triangle.cpp".

Examples\Khronos\hello_triangle.cpp\
Examples\Khronos\hello_triangle.h\
Examples\SpoutVK.h\
Examples\SpoutDX\
  all ".h" files
  
Right click on "hello_triangle" in the project explorer window and "Build".

Find the "apps" build folder 

"..\Vulkan-Samples\build\windows\app\apps"

Copy the following files to this folder.

Examples\SpoutVK.cpp\
Examples\SpoutVK.h\
Examples\SpoutDX\
  All ".cpp" and ".h" files

Find the "apps" project in the main project solution explorer.

"Vulkan-Samples\Samples\apps"

"Source Files > Add existing item" - add SpoutVK.cpp and SpoutVK.h.\
"Project > Add new filter" - add a new "SpoutDX" filter to the project.\
"SpoutDX > Add existing item" and add all the files in the SpoutSDK folder.

"File > Save All"\
Right click on "apps" in the project explorer window and "Build".

Find the "vulkan_samples" project in the main project solution explorer.\
Right click and "Set as startup project".\
Right click and "Debug > Start without debugging".

For a receiver\
Edit the file "hello_triangle.cpp" and find -

// SPOUT
<pre>
#include "SpoutVK.h"
// #define BUILDRECEIVER // Make a receiver rather than a sender
</pre>

Enable the line "#define BUILDRECEIVER" and "File > Save"\
Right click the "vulkan_samples" project and "Debug > Start without debugging".



