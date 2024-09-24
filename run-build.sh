#!/bin/bash
# This script is used tackle a some specifics of the GitHub action used with a docker container. 
# It copies the cached node-modules from the container to the runner workspace and then triggers the build using npm

cp -r /usr/src/repo/. /github/workspace/.
cd repo
export NODE_OPTIONS="--max-old-space-size=8192"
exec antora --stacktrace --fetch --clean antora-playbook.yml
