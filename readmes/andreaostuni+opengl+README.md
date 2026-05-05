## Ubuntu 22.04

- [`base`, `base-ubuntu22.04` (*base/Dockerfile*)](https://gitlab.com/container-images/opengl/-/blob/ubuntu22.04/base/Dockerfile)
- [`1.0-glvnd-runtime`, `1.0-glvnd-runtime-ubuntu22.04` (*glvnd/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/opengl/-/blob/ubuntu22.04/glvnd/runtime/Dockerfile)
- [`1.0-glvnd-devel`, `1.0-glvnd-devel-ubuntu22.04` (*glvnd/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/opengl/-/blob/ubuntu22.04/glvnd/devel/Dockerfile)
- [`1.1-glvnd-runtime`, `1.1-glvnd-runtime-ubuntu22.04` (*glvnd/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/opengl/-/blob/ubuntu22.04/glvnd/runtime/Dockerfile)
- [`1.1-glvnd-devel`, `1.1-glvnd-devel-ubuntu22.04` (*glvnd/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/opengl/-/blob/ubuntu22.04/glvnd/devel/Dockerfile)
- [`1.2-glvnd-runtime`, `1.2-glvnd-runtime-ubuntu22.04` (*glvnd/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/opengl/-/blob/ubuntu22.04/glvnd/runtime/Dockerfile)
- [`1.2-glvnd-devel`, `1.2-glvnd-devel-ubuntu22.04` (*glvnd/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/opengl/-/blob/ubuntu22.04/glvnd/devel/Dockerfile)

## HOW TO BUILD CUSTOM IMAGES USING THE DOCKER SCRIPTS

Procedure is similar to the [CUDA Container Images](https://gitlab.com/nvidia/container-images/cuda#building-from-source).

Run this script from the cloned opengl repo parent path (making changes where necessary):

```
#/bin/bash

export IMAGE_NAME="my/nvidia/opengl"
export LIBGLVND_VERSION="1.2"

export FROM="${OS}:${OS_VERSION}"
export OS="ubuntu"
export OS_VERSION="22.04"

# Example for building unsupported debian images:
# export FROM="debian:10"
# export OS="debian"
# export OS_VERSION="10"

cp NGC-DL-CONTAINER-LICENSE base/

echo -e ">>> Building BASE Image\n"

docker build -t "${IMAGE_NAME}:base-${OS}${OS_VERSION}" --build-arg "from=${FROM}" "base/"

echo -e "\n>>> Building RUNTIME Image\n"

docker build -t "${IMAGE_NAME}:${LIBGLVND_VERSION}-runtime-${OS}${OS_VERSION}" \
             --build-arg "from=${IMAGE_NAME}:base-${OS}${OS_VERSION}" \
             --build-arg "LIBGLVND_VERSION=${LIBGLVND_VERSION}" \
             "glvnd/runtime"

echo -e "\n>>> Building DEVEL Image\n"

docker build -t "${IMAGE_NAME}:${LIBGLVND_VERSION}-devel-${OS}${OS_VERSION}" \
             --build-arg "from=${IMAGE_NAME}:${LIBGLVND_VERSION}-runtime-${OS}${OS_VERSION}" \
             "glvnd/devel"
```
