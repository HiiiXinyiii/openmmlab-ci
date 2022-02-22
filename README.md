# OpenMMlab-ci

## 1. Introduction

openmmlab-ci is a quality assurance project for [OpenMMLab](https://openmmlab.com/) and [OpenMMlab Platform](https://platform.openmmlab.com/home/) project. It's designed to automatically test the current project codebase on server as DevOps suggests.

## 2. Getting Started

### 2.1 Guideline of Each Directory

- [Dockerfile README.md](Dockerfiles/README.md)

    It's used to create docker images for different codebases.

- [Windows README.md](Windows/README.md)
  
    + Install the necesssary environments for Windows OS
    + Generate precompiled package for mmcv on Windows OS

- [open README.md](./open.md)

    Test the automation of http api of [OpenMMlab Platform](https://platform.openmmlab.com/home/)

- [e2e READM.md](e2e/README.md)
  
    It's end-to-end tests for different codebases. 
