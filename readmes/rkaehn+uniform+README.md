*This document was written by hand. No part of it was generated or modified by AI.*

# Introduction
Uniform provides tools for building responsive and beautiful user interfaces. 

Despite implementing a full replacement for native UI tools, including text, layout, and rendering, a complete web application using Uniform is less than 280 KB (compressed).

Uniform does not have a visual identity. Instead, it makes it as easy as possible to express _any_ visual identity. Its goal is to allow designers to implement their ideas precisely: pixel-perfect layout, smooth animations, and the flexibility to customize the tools when necessary. By taking low-level control, it behaves consistently across all supported platforms.

Uniform is easy to use, and has different APIs for different needs.  
A JavaScript API is optimized to enable the fastest possible iteration speeds. With no build step, changes are visible immediately. It calls directly into the C core of the library, which compiles to WASM on the web, and native code on all other platforms.

There is also a simple, clean C API. It provides greater performance, but is just as usable as the JavaScript API. The library can be statically linked, or compiled from source together with the rest of the application. Compilation from source, including shaders, takes less than 1 second.

Uniform is currently in Preview, which means the API may change, and not all features are done. It supports iOS and macOS, where it renders via Metal, and the web, where it renders via WebGPU. Native support for Windows, Linux, and Android, where it will render via Vulkan, is planned.

[Demo](https://raffk.com/hn-demo)

## Main Features
**Powerful Layout.** Uniform combines the best parts of constraint-based layout with an auto-layout system using stacks. Constraints are defined between parent and child, and work by pinning an anchor from the child to an anchor of the parent, plus an optional offset.
Stacks support spacing between items, padding around the stack content, alignment, and distribution. Each item can define how it behaves as part of a stack: it either fills the available space, fits tightly around its content, or has a fixed size.

Layout is performed in fixed-point arithmetic, edges are snapped to pixel boundaries, and consistent spacing ensured. For text, Uniform supports text layout with character-level information accessible to the user, making custom text selection and visual effects possible.
Custom fonts are supported and can be set, along with size, weight, and color, for specific ranges within a string.

**Built for Custom Design.** Most applications require exact control over visual design and behavior. Shipping pre-built components and providing selected customization points does not fulfill this requirement. Simple components like buttons are defined from scratch. Custom visuals, gestures, and behaviors take only a few lines of code. For more complex components like scrolling lists or text fields, the library provides the core functionality like event handling, gestures, physics, and animations. The user just reads the calculated result of what should be drawn in what location, and creates the visual elements with the appearance they want.

**Shapes and Effects.** Uniform uses SDF shapes as a central concept. SDF is short for Signed Distance Field. It means that every pixel has information about its distance to the closest edge, as well as the corresponding normal. This information can be used to enable advanced visual effects. Glass uses it to add refraction effects near the edge, vary the blur radius across the shape, and render realistic shadows. It also allows shapes to blend together.

**Continuous Curves.** The library renders perfectly smooth curves: continuous position, continuous slope, continuous curvature, and continuous curvature slope. These curves are used by default for rounded rectangles, which transition smoothly down to pills and circles. They can also be used for arbitrary polylines or polygons.

**Low-Latency Input Processing.** There is a platform-independent interface for touch, pencil, keyboard, and mouse input. For full control, raw events can be received on each interface element, hit-tested against the node hierarchy. For touch input, there is a powerful gesture system. Gestures enable negotiations between components to resolve what actions are performed. Common gestures like tap, long-press, pan, or pinch come with the library. These bundled gestures are implemented using the public API, so custom gestures have exactly the same level of control and interoperate seamlessly.

**Advanced Display Technologies.** Uniform supports extended dynamic range rendering with a simple interface. Solid colors, gradients, images, and more can just use values above 1.0 and will be rendered brighter on capable displays. The compositor can render with high bit depth, or apply dithering for improved color transitions on standard bit depth targets. High refresh rates are supported, too.

**Simple API.** Interface elements are created with a single function call. The result is an immutable node. Nodes can be organized into a hierarchy. Layout and rendering operate on such hierarchies and behave like pure functions. Creating and laying out nodes is a cheap operation that can be performed as often as needed. While most layouts can be realized with the built-in constraint and stack based tools, Uniform is designed to support *any* layout. The ability to perform layout on individual nodes and hierarchies, potentially repeatedly or with complex dependencies, makes this possible.

**Native Integration.** Uniform does not compete with platform-provided UI frameworks. It does not include copies of native controls. Instead, it provides tools to build controls that should eventually *exceed* native or browser quality. Because the library is shipped directly with the application, improvements can be delivered to all users immediately. At the platform boundaries, Uniform strives for perfect integration. Windows resize artifact-free and rendering happens with no additional latency compared to native UI.

**Fast Iteration Speeds.** For creative work, iteration times are highest priority. Uniform embraces this at every level. For rapid prototyping, the JavaScript API eliminates any build steps. C headers are minimal, and compiling the library from scratch takes less than a second. At runtime, every language calls into the common C core. For most use cases, choosing an interface is a matter of preference, not performance.

**Light and Efficient.** Uniform’s core is written in C, and its shaders in the Slang Shading Language. It makes minimal use of third-party libraries. Eventually, all core technologies should be controlled by the project. Through this approach, binary sizes are small and runtime resource consumption low. The library works great for games and professional apps with high performance requirements, and just as much for simple apps and prototypes.

**Easy Integration.** A JavaScript application can be written in a single file. The file is processed by the Uniform runtime. The runtime uses JavaScriptCore to execute JIT-compiled code on desktop, and interpreted code on mobile. In both cases, JavaScript functions are forwarded to native functions. For deployment to desktop and mobile platforms, the runtime executable and the user file can be bundled and shipped, including to app stores. For deployment on the web, no additional runtime is needed, and the library code is included directly.

For C, or languages with a C FFI, the library provides header files, plus a binary archive per target platform. When building for the web, the application and server can be bundled into a single executable, with no external dependencies. Updating production reduces to copying a file.

## Examples
The following code launches the application, opens a window, and draws a gradient background. It runs on macOS, iOS, and the web.

```javascript
function onUpdate(window) {
    const targetDesc = app.windowGetTargetDesc(window);

    const root = ui.frame({
        size: ui.sizeFix(targetDesc.pxSize[0], targetDesc.pxSize[1]),
        fill: ui.fillGradient('down', ui.gray10, ui.gray40),
    });

    ui.layout(root);

    const commandBuffer = gpu.commandBufferCreate(app.getDevice(app.windowGetApp(window)), '');
    const target = app.windowAcquireTarget(window);

    ui.render(root, commandBuffer, target);
    ui.release(root);

    app.windowPresent(window, commandBuffer, target);
}

function onStart(a) {
    ui.init(app.getDevice(a));

    app.windowCreate(a, {
        onUpdate: onUpdate,
    });
}

app.run({
    onStart: onStart,
});
```

```c
void on_update(struct app_window* window) {
    struct app_target_desc target_desc = app_window_get_target_desc(window);

    struct ui_node root = ui_frame(&(struct ui_frame) {
        .size = ui_size_fix(target_desc.px_size.x, target_desc.px_size.y),
        .fill = ui_fill_gradient(ui_gradient_direction_down, ui_gray10, ui_gray40),
    });

    ui_layout(root);

    struct gpu_command_buffer* command_buffer = gpu_command_buffer_create(app_get_device(app_window_get_app(window)), "");
    struct gpu_texture* target = app_window_acquire_target(window);

    ui_render(root, command_buffer, target, (struct ui_render_desc) {});
    ui_release(root);

    app_window_present(window, command_buffer, target);
}

void on_start(struct app* app) {
    ui_init(app_get_device(app));

    app_window_create(app, &(struct app_window_desc) {
        .on_update = on_update,
    });
}

int main(void) {
    app_run(&(struct app_desc) {
        .on_start = on_start,
    });
}
```

`app_run` initializes long-lived application state. It is called once before any of the other `app_` functions. Once its work is completed, it calls the user-provided `on_start` function.

In `on_start`, the GPU device is available via `app_get_device`. The UI context is created and set as the default, so UI functions do not need to provide it explicitly.
Then, a window is opened via `app_window_create`. On macOS, it creates a window and positions and sizes it according to the user-provided parameters. On iOS, it uses the default scene and window, which fills the screen. On the web, it creates a canvas element in the DOM. The function returns a handle to the window. Using that, the user can render content into the window. 

Most commonly, drawing is performed at the refresh rate of the display. To be notified of display refreshes, a callback `on_update` can be provided when creating the window. `on_update` is called once per display refresh, commonly 60 or 120 times per second. 

The user can request information about the current state of the app or window by calling `app_` or `app_window_` functions. For instance, the properties of the drawing surface are accessible via `app_window_get_target_desc()`. Using that, the root node of the user interface is created.

Next, the root node is laid out. `ui_layout` takes the requested position, size, and layout of each node and calculates the layout result for a specific target resolution. In this case, the size of the root node was specified as exactly the size of the target, so it fills it completely.

For rendering, a GPU command buffer and the current drawing surface of the window are acquired. Both are given as parameters to `ui_render`, which writes commands into the command buffer. It returns immediately after the work is enqueued and does not wait for rendering to complete. The root node is no longer needed and gets released. If it had children, they would get released as well.

Finally, `app_window_present` enqueues a command to present the drawing surface and commits the command buffer for asynchronous execution on the GPU.

Note that the code as written here is not optimally energy-efficient. `on_update` is called on every display refresh, and each time, we layout and render exactly the same content. For an app that mostly draws static content, it might be ideal to only render when any part of it changed. In this instance, the window size is the only thing that influences the rendered result. If it stayed constant, the function could return early and the previous render would simply stay on screen.

Next, the code above is extended to draw a slightly more complicated interface.

```javascript
    const isDark = app.windowGetIsDark(window);

    const root = ui.frame({
        size: ui.sizeFix(targetDesc.pxSize[0], targetDesc.pxSize[1]),
        fill: ui.fillGradient('down', isDark ? ui.gray10 : ui.white, isDark ? ui.gray40 : ui.gray80),
    });

    const background = ui.frame({
        parent: root,
        pos: ui.posCenter(),
        layout: ui.layoutStackX('center', 'center', 0, ui.padXy(24, 12)),
        fill: ui.fillSolid(isDark ? ui.white : ui.black),
        corners: ui.corners(16),
    });

    ui.text({
        parent: background,
        str: ui.str('Uniform', isDark ? ui.black : ui.white, 26),
    });
```

```c
    bool is_dark = app_window_get_is_dark(window);

    struct ui_node root = ui_frame(&(struct ui_frame) {
        .size = ui_size_fix(target_desc.px_size.x, target_desc.px_size.y),
        .fill = ui_fill_gradient(ui_gradient_direction_down, is_dark ? ui_gray10 : ui_white, is_dark ? ui_gray40 : ui_gray80),
    });

    struct ui_node background = ui_frame(&(struct ui_frame) {
        .parent = root,
        .pos = ui_pos_center(),
        .layout = ui_layout_stack_x(ui_dist_center, ui_align_center, 0, ui_pad_xy(24, 12)),
        .fill = ui_fill_solid(is_dark ? ui_white : ui_black),
        .corners = ui_corners(16),
    });

    ui_text(&(struct ui_text) {
        .parent = background,
        .str = ui_str("Uniform", is_dark ? ui_black : ui_white, 26),
    });
```

The code is now reading the current theme from the window and using it to customize the appearance of the content. A background node is added as a child of the root node and positioned at its center. It has a `layout` argument, which specifies the position and size of its children. A stack layout has parameters for `distribution` (positions along the stack axis), `alignment` (positions on the cross-axis), `spacing` (space between the items), and `padding` (space around the whole content). In this case, the content is centered, and since there is only a single child, the stack direction and spacing have no visual impact.

The background node does not specify a size. By default, the size of a stack is determined automatically based on the size of its content.

The nodes are drawn in order of their hierarchy. The gradient is drawn first, then the solid background behind the text, and then the text itself.

Next, gestures are added.

```javascript
function onTap(gesture) {
    if (ui.tapGestureGetPhase(gesture) === 'recognized') {
        console.log('tap');
    }
}
```

```javascript
    const background = ui.node(root, ui.keyAuto);

    const tap = ui.tap({
        node: background,
        onChange: onTap,
    });

    const hover = ui.hover({
        node: background,
    });

    let fillColor = isDark ? ui.white : ui.black;
    if (ui.tapGestureHasTouch(tap)) {
        fillColor = ui.red;
    } else if (ui.hoverGestureHasHover(hover)) {
        fillColor = ui.gray50;
    }

    ui.frame({
        node: background,
        pos: ui.posCenter(),
        layout: ui.layoutStackX('center', 'center', 0, ui.padXy(24, 12)),
        fill: ui.fillSolid(fillColor),
        corners: ui.corners(16),
    });
```

```c
void on_tap(struct ui_tap_gesture gesture, void* user) {
    if (ui_tap_gesture_get_phase(gesture) == ui_gesture_phase_recognized) {
        printf("tap\n");
    }
}
```

```c
    struct ui_node background = ui_node(root, ui_key_auto);

    struct ui_tap_gesture tap = ui_tap(&(struct ui_tap) {
        .node = background,
        .on_change = on_tap,
    });

    struct ui_hover_gesture hover = ui_hover(&(struct ui_hover) {
        .node = background,
    });

    struct ui_color fill_color = is_dark ? ui_white : ui_black;
    if (ui_tap_gesture_has_touch(tap)) {
        fill_color = ui_red;
    } else if (ui_hover_gesture_has_hover(hover)) {
        fill_color = ui_gray50;
    }

    ui_frame(&(struct ui_frame) {
        .node = background,
        .pos = ui_pos_center(),
        .layout = ui_layout_stack_x(ui_dist_center, ui_align_center, 0, ui_pad_xy(24, 12)),
        .fill = ui_fill_solid(fill_color),
        .corners = ui_corners(16),
    });
```

`ui_node` is used to separate the creation of a node from setting its visual content. This separation allows the fill color to be set based on gesture data. In `ui_frame`, the node is specified via `.node = background`, and the parent node is not needed in that call anymore.

A tap and a hover gesture are attached to the node. Each can set an optional callback `on_change`, which is called whenever the state of the gesture changes. The state can change with input events, or based on time. The properties of the gesture can be read directly via the resulting handle. This is used inside the callback to read the current phase, and also as part of building the UI.

Gestures rely on the input system. It processes events and executes the user callbacks on nodes and gestures. It is set up as follows.

```javascript
let prevRoot = ui.nodeNull;

function onStart(a) {
    ui.init(app.getDevice(a));
    ui.inputSet(ui.inputCreate());

    app.windowCreate(a, {
        onUpdate: onUpdate,
    });
}
```

```javascript
    const events = app.windowTakeEvents(window);

    ui.inputDispatch(prevRoot, app.windowGetTimestamp(window), events, 1 / targetDesc.toPxFromPt);

    const root = ui.frame({ ... });

    ui.layout(root);

    ui.release(prevRoot);
    prevRoot = root;
```

```c
struct ui_node prev_root;

void on_start(struct app* app) {
    ui_init(app_get_device(app));
    ui_input_set(ui_input_create());

    app_window_create(app, &(struct app_window_desc) {
        .on_update = on_update,
    });
}
```

```c
    const struct app_event* events;
    uint32_t event_count;
    app_window_take_events(window, &events, &event_count);

    ui_input_dispatch(prev_root, app_window_get_timestamp(window), events, event_count, 1.0 / target_desc.to_px_from_pt);

    struct ui_node root = ui_frame(&(struct ui_frame) { ... });

    ui_layout(root);

    ui_release(prev_root);
    prev_root = root;
```

`app_window_take_events` provides the new events since the last time the function was called. These events are given to the input system via `ui_input_dispatch`. Explicit control over events can be useful for testing, where they may be created synthetically, or recorded and replayed. 

Note that the input system is called with `prev_root`. Structuring the code like this means that input is handled early, before the interface is built. When a gesture changes user state, that change will be reflected when building the new `root`.

The Uniform API is made of plain structures and functions. This means that typical programming paradigms _just work_. To make a component reusable, wrap it in a function. To create many nodes, write a loop. For optional nodes, use conditionals.

```javascript
function button(parent, key, label, onTap) {
    const background = ui.node(parent, key);

    const tap = ui.tap({ ... });

    const hover = ui.hover({ ... });

    ui.frame({ ... });

    ui.text({ ... });

    return background;
}
```

```javascript
    const root = ui.frame({
        size: ui.sizeFix(targetDesc.pxSize[0], targetDesc.pxSize[1]),
        layout: ui.layoutStackX('center', 'center', 12, 0),
        fill: ui.fillGradient('down', isDark ? ui.gray10 : ui.white, isDark ? ui.gray40 : ui.gray80),
    });

    for (let i = 0; i < 3; i++) {
        button(root, ui.keyAuto, buttons[i].label, buttons[i].onTap);
    }
```

```c
struct ui_node button(struct ui_node parent, struct ui_key key, const char* label, void (*on_tap)(struct ui_tap_gesture gesture, void* user), void* user) {
    struct ui_node background = ui_node(parent, key);

    struct ui_tap_gesture tap = ui_tap(&(struct ui_tap) { ... });

    struct ui_hover_gesture hover = ui_hover(&(struct ui_hover) { ... });

    ui_frame(&(struct ui_frame) { ... });

    ui_text(&(struct ui_text) { ... });

    return background;
}
```

```c
    struct ui_node root = ui_frame(&(struct ui_frame) {
        .size = ui_size_fix(target_desc.px_size.x, target_desc.px_size.y),
        .layout = ui_layout_stack_x(ui_dist_center, ui_align_center, 12, 0),
        .fill = ui_fill_gradient(ui_gradient_direction_down, is_dark ? ui_gray10 : ui_white, is_dark ? ui_gray40 : ui_gray80),
    });

    for (int i = 0; i < 3; i++) {
        button(root, ui_key_auto, buttons[i].label, buttons[i].on_tap, NULL);
    }
```

The `checkmark` function below is another example of a reusable component. It uses shape nodes, custom paths, and manual layout. 

```javascript
function checkmark(parent, color) {
    const icon = ui.frame({
        parent: parent,
        size: ui.sizeFix(16, 16),
    });

    ui.ellipse({
        parent: icon,
        pos: ui.posCenter(),
        size: ui.sizeFix(14, 14),
        outline: ui.outlineSolid('center', 1.5, color),
    });

    const path = ui.pathCreate();

    ui.pathMoveTo(path, [4.5, 8.5]);
    ui.pathLineTo(path, [7.0, 11.0]);
    ui.pathLineTo(path, [11.5, 5.5]);

    ui.shape({
        parent: icon,
        size: ui.sizeFix(16, 16),
        mode: 'stroke',
        thickness: 1.5,
        path: path,
        fill: ui.fillSolid(color),
    });

    ui.pathDestroy(path);

    return icon;
}
```

```javascript
    const background = ui.frame({ ... });

    checkmark(background, ui.white);

    ui.text({
        parent: background,
        str: ui.str(label, ui.white, 26),
    });
```

```c
struct ui_node checkmark(struct ui_node parent, struct ui_color color) {
    struct ui_node icon = ui_frame(&(struct ui_frame) {
        .parent = parent,
        .size = ui_size_fix(16, 16),
    });

    ui_ellipse(&(struct ui_ellipse) {
        .parent = icon,
        .pos = ui_pos_center(),
        .size = ui_size_fix(14, 14),
        .outline = ui_outline_solid(ui_outline_align_center, 1.5, color),
    });

    struct ui_path* path = ui_path_create();

    ui_path_move_to(path, make_double2(4.5, 8.5));
    ui_path_line_to(path, make_double2(7.0, 11.0));
    ui_path_line_to(path, make_double2(11.5, 5.5));

    ui_shape(&(struct ui_shape) {
        .parent = icon,
        .size = ui_size_fix(16, 16),
        .mode = ui_shape_mode_stroke,
        .thickness = 1.5,
        .path = path,
        .fill = ui_fill_solid(color),
    });

    ui_path_destroy(path);

    return icon;
}
```

```c
    struct ui_node background = ui_frame(&(struct ui_frame) { ... });

    checkmark(background, ui_white);

    ui_text(&(struct ui_text) {
        .parent = background,
        .str = ui_str(label, ui_white, 26),
    });
```

The shape API includes `ui_rect`, `ui_ellipse`, `ui_line`, and `ui_shape`. `ui_shape` defines a shape by filling or stroking a path. Building a path is just `move_to`, `line_to`, `cubic_to`, and more on the path. 

Like other nodes, shapes have fill, outline, shadow, blur, and effect options. Shapes can be smoothly combined within a given radius by setting `.shape_group = ui_shape_group(radius)` on their parent.

Lastly, there are some examples for rendering to a texture and writing it to disk, using external textures, and working alongside other renderers.

```javascript
    const texture = gpu.textureCreate(device, {
        label: 'export',
        format: 'bgra8',
        size: [width, height],
        usage: gpu.textureUsageRenderTarget | gpu.textureUsageSample | gpu.textureUsageRead,
    });

    const pixels = uniform.alloc(width * height * 4);

    const commandBuffer = gpu.commandBufferCreate(device, '');
    ui.render(root, commandBuffer, texture, {});
    gpu.commandBufferReadTexture(commandBuffer, texture, pixels, width * 4);
    gpu.deviceWait(device, gpu.commandBufferCommit(commandBuffer));

    writePng(path, uniform.read(pixels, width * height * 4), width, height, width * 4);
    uniform.free(pixels);
```

```c
    struct gpu_texture* texture = gpu_texture_create(device, &(struct gpu_texture_desc) {
        .label = "export",
        .format = gpu_format_bgra8,
        .size = make_uint2(width, height),
        .usage = gpu_texture_usage_render_target | gpu_texture_usage_sample | gpu_texture_usage_read,
    });

    uint8_t pixels[width * height * 4];

    struct gpu_command_buffer* command_buffer = gpu_command_buffer_create(device, "");
    ui_render(root, command_buffer, texture, (struct ui_render_desc) {});
    gpu_command_buffer_read_texture(command_buffer, texture, pixels, width * 4);
    gpu_device_wait(device, gpu_command_buffer_commit(command_buffer));

    write_png(path, pixels, width, height, width * 4);
```

`ui_render` just renders to a texture. The texture can come from the drawing surface of the window, or be created ad-hoc. The code above also works in a command line app. 

In the other direction, external textures can be used as source data for graphics. The user can write into the texture from their own renderer, and combine the result with the rest of the interface. The texture data is not copied, the texture is used directly as the backing storage.

In the following example, `render_scene` could encode its own commands into the command buffer, including rendering to `texture`. A game might use this to add a HUD on top of its main content.

```javascript
    const texture = gpu.textureCreate(device, {
        label: 'texture',
        format: 'bgra8',
        size: [512, 512],
        usage: gpu.textureUsageRenderTarget | gpu.textureUsageSample,
    });

    const graphic = ui.graphicCreateTexture(texture);
```

```javascript
function onUpdate(window) {
    const targetDesc = app.windowGetTargetDesc(window);

    const root = ui.frame({
        size: ui.sizeFix(targetDesc.pxSize[0], targetDesc.pxSize[1]),
        fill: ui.fillGradient('down', ui.gray10, ui.gray40),
    });

    ui.frame({
        parent: root,
        pos: ui.posCenter(),
        size: ui.sizeFix(512, 512),
        fill: ui.fillGraphic(graphic, 'fill', ui.white),
    });

    ui.layout(root);

    const commandBuffer = gpu.commandBufferCreate(app.getDevice(app.windowGetApp(window)), '');
    const target = app.windowAcquireTarget(window);

    renderScene(commandBuffer, texture);
    ui.render(root, commandBuffer, target);
    ui.release(root);

    app.windowPresent(window, commandBuffer, target);
}
```

```c
    struct gpu_texture* texture = gpu_texture_create(device, &(struct gpu_texture_desc) {
        .label = "texture",
        .format = gpu_format_bgra8,
        .size = make_uint2(512, 512),
        .usage = gpu_texture_usage_render_target | gpu_texture_usage_sample,
    });

    struct ui_graphic* graphic = ui_graphic_create_texture(texture);
```

```c
void on_update(struct app_window* window) {
    struct app_target_desc target_desc = app_window_get_target_desc(window);

    struct ui_node root = ui_frame(&(struct ui_frame) {
        .size = ui_size_fix(target_desc.px_size.x, target_desc.px_size.y),
        .fill = ui_fill_gradient(ui_gradient_direction_down, ui_gray10, ui_gray40),
    });

    ui_frame(&(struct ui_frame) {
        .parent = root,
        .pos = ui_pos_center(),
        .size = ui_size_fix(512, 512),
        .fill = ui_fill_graphic(graphic, ui_address_mode_fill, ui_white),
    });

    ui_layout(root);

    struct gpu_command_buffer* command_buffer = gpu_command_buffer_create(app_get_device(app_window_get_app(window)), "");
    struct gpu_texture* target = app_window_acquire_target(window);

    render_scene(command_buffer, texture);
    ui_render(root, command_buffer, target, (struct ui_render_desc) {});
    ui_release(root);

    app_window_present(window, command_buffer, target);
}
```

## Quick Start
To get started, download `uniform.zip` from the releases page. `bin` contains the runtime executable, which is used to run JavaScript code. `include` and `lib` contain headers and static libraries for using Uniform from C. You can either add the directory of the runtime executable to your `PATH`, or replace all following occurrences of `uniform` with the correct path.

The download also contains examples. To see a simple JavaScript example, navigate to `examples/simple-js` and execute the following command.

```sh
uniform main.js
```

A window with a button will open.

Behind the scenes, the runtime executable runs _native_ code to open windows, process input, draw graphics, and more. Uniform does *not* use web views for rendering, it renders its content directly with the GPU.

This simple example also includes a function (near the end of the file) to enable hot reload whenever its source code changes. Open `main.js` in an editor and change for instance the background color. The change will be reflected immediately. It is worth noting that hot reload is not a feature of the runtime. It can be implemented by the user in whatever way is best for a given use case.

The simple example can also be executed on the web and on iOS devices. All targets support hot reload. On iOS, the source code can be changed directly on the device. No connection to a computer is required. This allows a coding agent on the device, even running via a local model and no internet connection, to update an app.

To start a server for the example, first generate a certificate for HTTPS via `uniform --certificate`. You may also want to install this certificate on your iOS device, via `uniform --certificate --device="My iPad"`. This allows an iOS device to access pages served by the runtime, even over WiFi.
Start the server as follows. By listing arguments *before* the source file, they are provided to the runtime.

```sh
uniform --serve main.js
```

To install a native app for this example, execute the following command. The source code is accessible on the device under `On My iPad/simple-js`.

```sh
uniform --device="My iPad" main.js
```

To distribute a JavaScript app to users, the Uniform runtime executable and the JavaScript files need to be bundled. The bundle may also include additional files, like an app icon, and it must be signed. To make this as easy as possible, the runtime executable has an additional feature: it can package itself.

Copy the code below into a file and execute it in the usual way, by providing it as an argument to the Uniform runtime executable.

```javascript
const build = bd.create();

const config = bd.configCreateDefault(build);
bd.configSetString(config, bd.all, 'uniformPath', 'path/to/uniform');
bd.configSetString(config, bd.all, 'appleBundleIdentifier', 'com.example.simple');
bd.configSetString(config, bd.platformMacos, 'appleNotaryProfile', 'notary');

const simple = bd.targetCreate(build, 'simple', 'app');
bd.targetSetConfig(simple, config);
bd.targetAddInput(simple, 'main.js');
bd.targetAddInput(simple, 'JetBrainsMono.ttf');
bd.targetAddUniform(simple);

uniform.exit(bd.run(build, uniform.args));
```

To provide arguments to the application and not the runtime, they are listed *after* the input file.

```sh
uniform build.js --target=simple --platform=macos --profile=release --export
```

A `simple.app` bundle will be created in `build/products/simple-macos-release/`. It is ready to be published for download.

There is also a simple example for using Uniform from C. Navigate to `examples/simple` and execute `sh run.sh macos`. The script uses Clang to compile the `main.c` and link it with the static library.

```sh
clang -Iuniform/include main.c uniform/lib/macos-release/libuniform.a -framework AppKit -framework Metal -framework QuartzCore -o simple
```

```sh
./simple
```

You can also run the example on the web, by starting a server via `sh run.sh wasm` or on iOS via `DEVICE="My iPad" sh run.sh ios`.

In this case, `run.sh` calls Clang directly. It is also possible to use the `build.js` from above to compile and publish C applications, by just changing the input file to `main.c`. Alternatively, the build file can be written in C. This is shown in `examples/triangle`. This is particularly useful when sharing code between the application and the build file.

The following code is equivalent to the JavaScript version above. It will also produce packaged apps for all supported platforms, ready for publishing.

```c
int main(int argc, char** argv) {
    struct bd* build = bd_create();

    struct bd_config* config = bd_config_create_default(build);
    bd_config_set_string(config, bd_all, bd_config_uniform_path, "path/to/uniform");
    bd_config_set_string(config, bd_all, bd_config_apple_bundle_identifier, "com.example.simple");
    bd_config_set_string(config, bd_platform_macos, bd_config_apple_notary_profile, "notary");

    struct bd_target* simple = bd_target_create(build, "simple", bd_target_type_app);
    bd_target_set_config(simple, config);
    bd_target_add_input(simple, "main.c");
    bd_target_add_uniform(simple);

    return bd_run(build, argc, argv);
}
```

```sh
mkdir build
clang -Iuniform/include build.c uniform/lib/macos-release/libuniform.a -o build/bd
```

```sh
./build/bd --target=simple --platform=macos --profile=release
```

With the C version of Uniform, the packaged app only includes native code, no JavaScript. Both versions are small and efficient, but the C version will be slightly better in both regards, as expected.

Uniform also provides tools to build a custom web server. The following code builds the WASM version of the application, and embeds it into the server executable. The server can be compiled for macOS or Linux. To update an application, only a single, small executable needs to be copied to the server.

```c
extern const char* const simple_site_names[];
extern const unsigned char* const simple_site_data[];
extern const unsigned long long simple_site_sizes[];
extern const unsigned long long simple_site_count;

static struct cl_site site;

static void on_conn_update(struct cl_server_conn_update* update, void* args) {
    if (update->type == cl_server_conn_update_type_http_request) {
        cl_site_respond(&site, update);
    }
}

int main(int argc, char** argv) {
    struct cr_str* certificate = cr_str_create_with_contents_of_file(cr_str_create(argv[1]));
    struct cr_str* private_key = cr_str_create_with_contents_of_file(cr_str_create(argv[2]));

    cl_site_add_embed(&site, "", simple_site_names, simple_site_data, simple_site_sizes, simple_site_count);

    struct cl* server = cl_server_create(&(struct cl_server_params) {
        .certificate_pem = cr_str_get_data(certificate),
        .certificate_pem_size = cr_str_get_count(certificate),
        .private_key_pem = cr_str_get_data(private_key),
        .private_key_pem_size = cr_str_get_count(private_key),
        .port = 9443,
        .on_conn_update = on_conn_update,
    });

    return cl_server_run(server);
}
```

```c
    struct bd_target* site = bd_target_create(build, "simple_site", bd_target_type_embed);
    bd_target_set_config(site, config);
    bd_target_add_input_ex(site, &(struct bd_input_desc) { .target = simple, .overrides.platform = bd_platform_wasm });

    struct bd_target* server = bd_target_create(build, "simple_server", bd_target_type_executable);
    bd_target_set_config(server, config);
    bd_target_add_input(server, "server.c");
    bd_target_add_input_ex(server, &(struct bd_input_desc) { .target = site, .filter = bd_platform_macos | bd_platform_linux });
    bd_target_add_uniform(server);
```

Since the WASM code of the application is embedded into the server executable, the server target depends on the application target. This is specified via `bd_target_add_input_ex`.

The site is served via HTTPS, and the certificate and private key are provided as arguments to the server.

```sh
./build/bd --target=simple_server --platform=macos --profile=release
./build/products/simple_server-macos-release/simple_server certificate.pem private_key.pem
```

# Motivation
**Abstract.** Developers have a strong desire to make their software available on a wide range of platforms. Current solutions ask for significant compromises. By analyzing these compromises, opportunities for improvement can be found.

**Conceptual Problems.** Platform-provided UI tools require developers to implement the same interface several times. If the interface paradigms are fundamentally different, differences in the tools might be justified. Often though, the differences extend down to basic primitives. These primitives might produce the exact same visual or behavioral result. Logically, there is no reason why even a simple rectangle is expressed one way in the browser, and another way in a native app. 

A standard approach when interacting with platform-specific code in other domains, for instance with graphics APIs, is to introduce a level of abstraction. Unfortunately, all major platform UI frameworks are written in high-level programming languages, take high-level control of the rendering and interaction loop, and enforce high-level architecture constraints. High-level code can never be abstracted to low-level code, so many use cases are immediately excluded.

Furthermore, the constraints that the various platform tools enforce are not just high-level, they are also all _different_. Designing an architecture around a framework with very specific requirements is already a significant effort. When multiple platforms are targeted, individual problems accumulate, and the interactions between paradigms cause an exponential number of new problems.

Besides the architectural issues, the platform-provided tools also have a number of practical issues. Most frameworks provide ready-to-use components like buttons, sliders, and text fields. 
Some of them also handle more abstract concepts like navigation or focus. They are advertised to automatically support accessibility, various languages, and adapt to user preferences. At the start of a project, these features are helpful, and progress is fast.

Inevitably, first issues appear. A designer might want to customize an attribute that the framework does not allow to customize. A feature that was assumed to be standard turns out not to be available on the targeted platform version. A bug in the implementation of the framework cannot be worked around. What seemed like progress turns out to be an illusion.

At a fundamental level, the paradigms of most UI frameworks do not match the actual user requirements.

**Conceptual solutions.** Most importantly, a UI framework must work on all major platforms, and must do so consistently. The popularity of existing cross-platform tools is a strong indicator for the need of developers to avoid duplicated work. When platforms require specialized interfaces, only the parts that are actually different should have separate implementations.

Next, the tools must be implemented at a low level of abstraction. Developers can build and distribute high-level components. Different ideas can compete, and over time, ideal solutions emerge. Hardware compatibility should be handled by the framework, so developers can focus on the user experience. Ideally, this approach extends down to the platform. Low-level access to the hardware raises the performance ceiling and allows abstractions to evolve.

High-level components need to be open and customizable at the level of source code. They should serve as starting points, and the tools must be powerful enough to reimplement these components from scratch. By definition, the UI is the contact point between users and application. It is the part of a project where developers should be least willing to accept compromises. The tools must respect this from the start.

Finally, UI tools should not be coupled to the platform version. Bugs need to be fixed quickly, and the user interface needs to look the same across all versions. If a new feature is added, developers should be able to use it immediately, without having to split the userbase. Engineers and designers need to be sure that their interface does not change without their explicit approval. Tools should be bundled with the application, and updated only by choice.

**API.** Most modern UI frameworks take full control over the execution of an application. The user can only customize the behavior in predefined ways, and otherwise surrenders responsibility. The design ideas of those frameworks are often highly opinionated and unreasonably strongly enforced. The result is an inefficient and difficult-to-use API.

Frameworks with a declarative API might insist on making every part of the UI code declarative. For some use cases, like parameter lists or stateless descriptions, declarative code might be ideal. In other cases, like processes over time or conditional execution, declarative code can be unintuitive or unable to be written altogether. Instead of handling these cases with the native tools of the language, API-level constructs have to be invented. In extreme cases, modifications to the language are made.

In the other direction, imperative frameworks might insist on making everything imperative. To change properties of UI elements, the user interacts with the framework by changing state. To avoid UI state being the source of truth, a state layer controlled by the user might be introduced. Multiple copies of state means they have to be kept in sync, which can ultimately lead to cases where data and visualization diverge. At that point, other frameworks are introduced to solve the problem of state management. 

Sometimes, one framework might be used as a layer above another framework. An example is a cross-platform layer above a native toolkit. In those cases, updated state might need to be diffed, and only the changed parts of the state are forwarded to the layer below. Updating each of the layers might already be expensive, but diffing now requires additional computation on top. Again, more frameworks are built to solve these problems. More frameworks lead to higher complexity, and higher complexity means worse understanding, more bugs, and slower performance.

Selecting a paradigm and applying it everywhere is unlikely to lead to a good design. Instead, first-principles solutions to individual problems need to be found. A collection of visual elements does not inherently require state. Defining them via simple descriptors is sufficient. When state is needed, it is defined by the user, and the interface is derived from it. In contrast, a custom layout procedure should not be expressed declaratively. Rather, existing control flow constructs of the language should be used. 

The result is a dramatic reduction of complexity in both library and user code. The saved complexity can be used by the developer to improve the quality of the application itself. It also makes the tools more approachable, even to other disciplines. 

At the moment, design is widely seen as a separate process from implementation. In the handoff from one to another, details can get lost. This may happen in the form of animations or interactions that cannot be accurately designed or transferred. Or changes that are made to a prototype, but not applied to the actual product. Especially when multiple people are involved, problems like these are inevitable.

A simple, clear API allows designers to build, understand, and change components directly. Translation errors between disciplines or tools can be avoided. Ideas can be prototyped with the full capabilities of the target from the beginning. Experimentation can clarify plans, and show new directions. Consequentially, product quality improves.

**Implementation.** The implementation has to respect that different users have different preferences and needs regarding their programming language. It must therefore not rely on features of any specific language, and instead use constructs that are expressible in *all* languages. This produces an interface that naturally serves as a foundation, and can be adapted to idiomatic code if needed. 

The tools need to work on many platforms, and as much of their implementation as possible should be shared between them. Further, by targeting the web, binary size becomes one of the most important metrics to optimize. Finally, allocation cost has to be considered, in terms of size, count, and execution time. Full control to build and specify memory allocators everywhere is required. Standard libraries of many languages are not designed for these goals. Thus, the ability to write systems code directly is required, and relevant functionality is implemented from scratch.

For better or worse, the only language options satisfying these constraints are C and C++. Strictly, even the use of C++ constructs in the public API is not possible, as those can not be imported into most other languages. The door to a future use of C++ in private code is kept open, but for now, all CPU-side code is written in C.

For GPU code, again, the lowest-level control is required. On Apple platforms, recent versions of Metal give user applications essentially the same capabilities as native applications. Performance and energy efficiency at or exceeding the level of platform UI tools are possible, and can be verified via tests.

On the web, WebGPU has recently become standard, and is starting to be widely available. The addition of compute shaders makes advanced visual effects possible. It is also architecturally closer to native GPU APIs, which brings it closer in performance, and enables building a single abstraction that covers all platforms. With that, new platforms can be added without changing the abstraction or rendering code. 

While WebGPU is a significant step towards parity of web and native code in terms of capability and performance, they are not yet equal. Most importantly, mobile GPUs are built around a technique called tile-based rendering, and only native APIs provide tools to optimize for this paradigm. In practice, this means that blending, for instance by using transparency or special blend modes, can be slower than what the native implementation would achieve. Fortunately, proposals to add these missing features exist already, and are likely to become standard in the near future.

A consequence of low-level control is that applications become essentially universal. More platform versions are supported, and the usual problems of external dependencies can be avoided. Behavior is completely consistent, and a deeper understanding allows to reduce complexity. A simple, predictable, and efficient solution emerges. 

*Contact via uniform@raffk.com.*
