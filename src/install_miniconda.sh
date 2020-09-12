#!/bin/bash

# install anaconda
sudo apt-get update --fix-missing && sudo apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh && \
    rm ~/miniconda.sh

# reload bash
source ~/.bashrc

# deactivate base
conda config --set auto_activate_base false
conda deactivate
conda update -y --name base conda \
    && conda clean --all -y
