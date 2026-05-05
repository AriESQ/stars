# videobeats

## how to compile???

as described here: https://github.com/astellato/ofxSyphon/issues/50#issuecomment-1241697342

1. download ofx nightly 20220908
2. download https://github.com/ofTheo/ofxSyphon/tree/feature-arc and add it to addons folder
3. apply fix mentioned here: ofTheo/ofxSyphon@feature-arc...sloev:ofxSyphon:patch-1
4. use project generator to update examples/video/videoplayer with
    a. addons: ofxsyphon
    b. template: visual studio code
5. open vscode workspace folder
6. compile debug release
7. copy Syphon.Framework from /addons/ofxSyphon/libs/Syphon/lib/osx/Syphon.framework to examples/video/videoPlayerExample/bin/videoPlayerExample_debug.app/Contents/Frameworks/Syphon.framework
8. run debug start debugging

## DEMO 

video:

[![Final video of fixing issues in your code in VS Code](https://img.youtube.com/vi/K9DTGbNg_cg/maxresdefault.jpg)](https://www.youtube.com/watch?v=K9DTGbNg_cg)
