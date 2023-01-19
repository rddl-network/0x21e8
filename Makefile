TAG ?= latest
DOCKER_IMAGE_REGISTRY ?= index.docker.io
IMAGE ?= $(DOCKER_IMAGE_REGISTRY)/riddleandcode/dockerized-0x21e8:$(TAG)

# Build docker image of service
build:
	DOCKER_BUILDKIT=1 docker build --network host -t $(IMAGE) -f docker/Dockerfile ./

# Run image
run:
	docker run $(IMAGE)

# Publish image to DockerHub
publish:
	docker push $(IMAGE)
