FROM ubuntu:latest
LABEL authors="nenyt"

ENTRYPOINT ["top", "-b"]