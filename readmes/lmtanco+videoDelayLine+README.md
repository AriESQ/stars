videoDelayLine
==============

Simple Video Delay Line using openFrameworks library and boost circular buffer. 

Requires boost/circular_buffer. Repository includes Visual Studio 2012 project files and XCode 8.2.1 project files

This software was used in Molina-Tanco, L., García-Berdonés, C., Reyes-Lecuona, A., 'The Delay Mirror: a Technological Innovation Specific to the Dance Studio'. Proceedings of the 4th International Conference on Movement Computing (MOCO'17). https://doi.org/10.1145/3077981.3078033 


OSX
---

* Check out https://github.com/danoli3/ofxOSXBoost to your openFrameworks addon directory.
* Change the following line in your CoreOF.xconfig file:

`//HEADER_BOOST = "$(OF_PATH)/libs/boost/include"`

`HEADER_BOOST = "$(OF_PATH)/addons/ofxOSXBoost/libs/boost/include"`
