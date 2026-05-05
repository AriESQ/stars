# Miracle

[![Build & Test](https://github.com/McFlyboy/Miracle/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/McFlyboy/Miracle/actions/workflows/build-and-test.yml)

Miracle is a cross-platform, framework-style C++20 game engine, that is still early in its life cycle, for developing minimalistic 2D and 3D games on Windows, macOS and Linux. It uses the Vulkan SDK for rendering and relies on vcpkg to manage all other dependencies. Both must be installed to configure and build this project.

## Demos - Miracle in action
The following demonstrations were built from demo projects which come included as part of this repo.

### 2D demo
The source code for the 2D demo can be found [here](https://github.com/McFlyboy/Miracle/tree/main/Demos/Demo2).

![Miracle 2D demo](https://github.com/user-attachments/assets/1bfb9245-01a7-4c4e-8e37-153c404a6fb1)

### 3D demo
The source code for the 3D demo can be found [here](https://github.com/McFlyboy/Miracle/tree/main/Demos/Demo1).

![Miracle 3D demo](https://github.com/user-attachments/assets/acf093a7-0604-41fa-8350-d5f12a5d3c78)

## Setup
Miracle requires very little code to get started. Here is a minimal setup for an empty application:
```cpp
#include <Miracle/Miracle.hpp>

int main() {
	return Miracle::App("My app").run();
}
```

Let's break that down:
```cpp
#include <Miracle/Miracle.hpp>

using namespace Miracle;

int main() {
  // Step 1: Create the app
	auto app = App("My app");

  // Step 2: Run the app
	int exitCode = app.run();

  // Step 3 (optional): Return the app's exitcode
	return exitCode;
}
```
### Configure the app
In order to add content to your app and configure its behavior, we use an `AppConfig` during construction of the app, as shown below.
```cpp
auto app = App("My app", AppConfig{});
```

`AppConfig` is a struct containing several smaller structs that configure different parts of your app. Here's an example of an app with a resizable window and v-sync enabled:
```cpp
auto app = App(
  "My app",
  AppConfig{
	  .windowConfig = WindowConfig{
		  .size = WindowSize{
			  .width = 1280,
			  .height = 720
		  },
		  .resizable = true
	  },
	  .rendererConfig = RendererConfig{
		  .swapchainConfig = SwapchainConfig{
			  .useVsync = true
		  }
	  }
  }
);
```

### Adding content
#### Scenes
Miracle uses a scene system where content is split up into different scenes, and only a single scene is active and displayed to the user at a time. Right now, Miracle does not support creating multiple scenes, but this will change in the future. The content of a scene is made up of entities. Everything in a scene, except the solid color background of a scene, is an entity. A scene can be created by adding a `SceneConfig` to the app's `AppConfig`, while entities that belong to this scene can be created by adding `EntityConfig`s to the `SceneConfig`.
```cpp
AppConfig{
  // A scene containing three entities
  .sceneConfig = SceneConfig{
    .entityConfigs = std::vector{
      EntityConfig{},
      EntityConfig{},
      EntityConfig{}
    }
  }
}
```

#### Entities
An entity is an object that can represent anything in a 2D or 3D environment. For example, it can represent a controllable character, an enemy character, an inanimate object, a camera to view into the environment, a light source to light up the environment, or even the ground itself that all other entities stand on. Entities are made up of components which represents the different abilities that an entity possesses. An entity can only possess one of each component type. The Transform component is the only component that is mandatory for an entity to possess, and will be added even if not supplied by the developer in the `EntityConfig`. All other components are optional to include in an entity.
```cpp
SceneConfig{
	.entityConfigs = std::vector{
		// An entity containing two components
		EntityConfig{
			// A Transform component describing the position of the entity in 3D space
			.transformConfig = TransformConfig{
				.translation = Vector3{ .x = 2.0f, .y = 0.0f, .z = -1.0f }
			},
			// A Camera component describing the entity's ability to view the scene with a perspective lens
			.cameraConfig = PerspectiveCameraConfig{
				.fieldOfView = 80.0_deg
			}
		}
	}
}
```

#### Assets
Right now Miracle only supports one type of asset, which is 3D meshes, and the `AppConfig` does not provide a dedicated section to add assets yet, so for now, meshes are added directly into the `RendererConfig` instead.
```cpp
AppConfig{
	.rendererConfig = RendererConfig{
		.meshes = std::vector{
			// The mesh of a square
			Mesh{
				.vertices = std::vector{
					Vertex{ .position = Vector3{ .x = -0.5f, .y = -0.5f, .z = 0.0f } },
					Vertex{ .position = Vector3{ .x =  0.5f, .y = -0.5f, .z = 0.0f } },
					Vertex{ .position = Vector3{ .x =  0.5f, .y =  0.5f, .z = 0.0f } },
					Vertex{ .position = Vector3{ .x = -0.5f, .y =  0.5f, .z = 0.0f } }
				},
				.faces = std::vector{
					Face{ .indices = { 0, 1, 2 } },
					Face{ .indices = { 0, 2, 3 } }
				}
			}
		}
	}
}
```

Once your meshes have been added to the meshes section of the `RendererConfig` entities can use them by referring to the correct index in an Appearance component.
```cpp
EntityConfig{
	// An Appearance component describing an appearance that is using the first mesh in the RendererConfig's meshes colored as magenta
	.appearanceConfig = AppearanceConfig{
		.meshIndex = 0,
		.color     = ColorRgb::createFromNonlinearSrgbColorCode(0xFF00FF)
	}
}
```

#### Behavior
Behaviors are what powers entities to act on its own, or through user input. Miracle provides a polymorphic Behavior component which allows you to author any kinds of behavior that you want. To do so you have to create a class that extends `BehaviorBase`.
```cpp
class MySimpleBehavior : public BehaviorBase {
private:
	float m_movementSpeed;

public:
	// The behavior receives an entity context that lets it manipulate the state of the entity. The context must be the first parameter supplied to the constructor, and must be forwarded to the underlying BehaviorBase.
	// Following the context, any other parameters can be accepted by a behavior depending on your needs.
	MySimpleBehavior(const EntityContext& context, float movementSpeed) : BehaviorBase(context), m_movementSpeed(movementSpeed) {}

	// The act method acts out the behavior, and is called every update in the app
	virtual void act() override {
		// Moves the entity forward in the Z-axis when the W-key is held down on the keyboard
		if (Keyboard::isKeyHeld(KeyboardKey::keyW)) {
			m_context.getTransform().translate(Vector3s::forward * m_movementSpeed * DeltaTime::get());
		}
	}
};
```

Once a behavior class has been created the behavior can be assigned to an entity. Since the behavior needs to be instantiated *after* the entity has been instantiated as part of the scene, you need to describe in the `EntityConfig` both which behavior it should use and what parameters it should be instantiated with. This is done using a `BehaviorFactory`.
```cpp
EntityConfig{
	// A behavior component using our MySimpleBehavior class which will be instantiated by forwarding the factory's parameters to the class's constructor, in the supplied order
	.behaviorFactory = BehaviorFactory::createFactoryFor<MySimpleBehavior>(10.0f) // movementSpeed = 10.0f
}
```

### Global scripting
Miracle allows you to add scripts to the app that are not attatched to any entities. There are two types of scripts like this, the Start script and the Update script, both of which can be set in the app's `AppConfig`.

```cpp
AppConfig{
	.startScript = []() { Logger::info("Starting up..."); },
	.updateScript = []() { Logger::info("Running logic during update..."); }
}
```

The Start script will run once during startup of your app, and the Update script runs once every update, before the behaviors belonging to the current scene's entities run.

### Dynamic content
Miracle allows you to generate new entities during the app's runtime. This is helpful in games where you want to spawn in new content during runtime. In order to do so you can simply grab the current scene and provide it with an `EntityConfig` for your brand new entity.

```cpp
// Creates a new entity in the scene
CurrentScene::createEntity(EntityConfig{});

// Creates a new entity in the scene, and returns the context for it
EntityContext context = CurrentScene::createAndGetEntity(EntityConfig{});
```

Any entity can also be deleted during runtime from its `EntityContext`.
```cpp
context.destroyEntity();
```

## License
Miracle uses the MIT license.
