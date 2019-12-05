# base image
FROM ubuntu:bionic

# metadata
LABEL base.image="ubuntu:bionic"
LABEL version="1"
LABEL software="MjolnirTree"
LABEL description="MjolnirTree dependencies"
LABEL website="https://github.com/AbigailShockey/MjolnirTree/"
LABEL license="https://github.com/AbigailShockey/MjolnirTree/blob/master/LICENSE"
LABEL maintainer="Abigail Shockey"
LABEL maintainer.email="abigail.shockey@slh.wisc.edu"

# install ubuntu dependencies
RUN apt-get update && apt-get install -y wget \
  python3 \
  python3-setuptools \
  python3-biopython \
  python3-pip

RUN python3 -m pip install -U dendropy pandas scipy numpy docker

RUN mkdir scripts

RUN wget https://raw.githubusercontent.com/AbigailShockey/MjolnirTree/master/scripts/hammingDistanceNJTrees.py && \
  mv hammingDistanceNJTrees.py scripts/ && \
  chmod +x scripts/hammingDistanceNJTrees.py

ENV PATH="${PATH}:/scripts"

RUN mkdir /data
WORKDIR /data
