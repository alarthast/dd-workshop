#!/bin/bash

docker pull --platform linux/amd64 remlapmot/r-docker:r-v2-for-will
docker tag remlapmot/r-docker:r-v2-for-will ghcr.io/opensafely-core/r:latest
docker pull --platform linux/amd64 remlapmot/r-docker:rstudio-v2-for-will
docker tag remlapmot/r-docker:rstudio-v2-for-will ghcr.io/opensafely-core/rstudio:latest

