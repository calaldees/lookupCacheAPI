DOCKER_IMAGE:=lookup_cache_api

run:
	uv run litestar run --debug --pdb

doc:
	open http://localhost:8000/schema


docker:
	docker build --tag ${DOCKER_IMAGE} .
	docker run --rm --publish 8000:8000 ${DOCKER_IMAGE}
