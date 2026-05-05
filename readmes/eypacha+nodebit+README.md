# Overview

**Nodebit** is a web app for creating Bytebeat music using an interactive, node-based interface inspired by Pure Data. It allows you to connect and control nodes to explore and generate sound creatively.

![Screenshot](public/screenshot.png)

Nodebit is built on top of the html5bytebeat library by Greggman, which provides the `ByteBeatNode` a [`AudioNode`](https://developer.mozilla.org/en-US/docs/Web/API/AudioNode) for generating and controlling audio. The app is developed using Vue 3 and is designed to offer an intuitive way to create music with minimal coding.

## Features

- Interactive Node System: Add, connect, and control various types of nodes on a canvas to build audio synthesis chains.
- Node Editing: Each node represents a specific operation or value that contributes to the sound generation. You can edit, resize, and move nodes freely.
- Export and Import: Save your work as JSON or image files and reload it at any time.
- Visualizer: Some nodes include visualizations to help understand the sound output.
- Keyboard Shortcuts: Control the flow and structure of your Bytebeat creations with convenient keyboard shortcuts.

## Nodebit Controls

- Ctrl + Click: Create a new empty node.
- Click: Select a node.
- Double Click: Edit the selected node.
- Shift + Enter: Insert a new line in the node editor.
- Enter: Evaluate the selected node.
- Delete / Backspace: Delete the selected path or node.
- 1, 2, 3, 4...: Change paths in the selected switch node.

## Node Types and Expressions

Nodebit supports a variety of node types and mathematical expressions, automatically detected when the node is evaluated:

- **Time** (t): Represents the time variable.
- **Numbers**: Supported formats include decimal, floating-point, hexadecimal, and binary (e.g., 14, .5, 0xFF, 0b1010).
- **Operators**: Standard operators like +, -, *, /, %.
- **Logic & Bitwise Operators**: Includes !, &, |, ^, >>, <<.
- **Array Operators**: Includes +[], &[], |[], etc.
- **Math Functions**: Most [JavaScript Math Methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math#static_methods) such as sin, cos, tan, sqrt, etc., are available for node calculations.
- **Switch**: Use it to select between multiple inputs.

## Special Nodes

- **Play**: Starts or pauses audio playback.
- **Stop**: Stops the audio playback and reset the t variable.
- **Reset**: Reset the t variable.
- **Visualizer** Nodes: Use visualizer or visual nodes to get visual feedback of the sound output.
- **Export**: Export your work as JSON or image.
- **Import**: Load your saved JSON or image file.
- **Mouse**: Get the current mouse (X, Y) position for interaction.
- **Help**: Displays help for a specific node.
- **Manual**: Displays this help message.

## Project Setup

```sh
yarn
```

### Compile and Hot-Reload for Development

```sh
yarn dev
```

### Compile and Minify for Production

```sh
yarn build
```