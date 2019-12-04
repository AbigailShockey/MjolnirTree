# base image
FROM ubuntu:bionic

# metadata
LABEL base.image="ubuntu:bionic"
LABEL version="1"
LABEL software="MjolnirTree"
LABEL description="Dependencies for MjolnirTree"
LABEL website="https://github.com/AbigailShockey/MjolnirTree"
LABEL license="https://github.com/AbigailShockey/MjolnirTree/blob/master/LICENSE"
LABEL maintainer="Abigail Shockey"
LABEL maintainer.email="abigail.shockey@slh.wisc.edu"

# install ubuntu dependencies
RUN apt-get update && apt-get install -y wget \
  python3 \
  python3-setuptools \
  python3-biopython \
  python3-pip


# RUN wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh && \
#  bash Anaconda3-2019.10-Linux-x86_64.sh -b -p ./anaconda

RUN python3 -m pip install -U dendropy pandas scipy numpy docker

RUN mkdir scripts

RUN wget https://github.com/AbigailShockey/MjolnirTree/blob/master/scripts/hammingDistanceTrees.py
RUN mv hammingDistanceTrees.py scripts/ && \
chmod +x scripts/hammingDistanceTrees.py

ENV PATH="${PATH}:/scripts"

RUN mkdir /data
WORKDIR /data
