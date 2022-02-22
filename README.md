# Openmmlab-ci

## 1. Introduction

Openmmlab-ci is a quality assurance project for [OpenMMLab](https://openmmlab.com/) and [Openmmlab Platform](https://platform.openmmlab.com/home/) project. It's designed to automatically test the current project codebase on server as DevOps suggests.

## 2. Getting Started

### 2.1 Guideline of Each Directory

- [Dockerfile README.md](Dockerfiles/Dockerfile.md)

    It's used to create images for different codebase.

- [Windows README.md](Windows/Windows.md)
  
    + Install the necesssary environments for Windows OS
    + Download some precompiled package for Windows OS

- [open README.md](./open.md)

    Test the automation of http api of [Openmmlab Platform](https://platform.openmmlab.com/home/)

- [e2e READM.md](e2e/e2e.md)
  
    It's end-to-end tests for different codebases. 
