Assessing Colocalization - Malene E. Lindholm
==================================

### Mono- and biallelic protein truncating variants in alpha-actinin 2 cause cardiomyopathy through distinct mechanisms



## Setup
1 - Download [Anaconda](https://www.anaconda.com/download/), a free installer that includes Python and all the common scientific packages.
Be sure to download Anaconda for Python 3.6 or 3.7 for the appropriate operating system.
Follow the on-screen instructions for installation. When prompted, be sure to "Install for me only."
You may be prompted for optional installations, like PyCharm. You will not need it.

2- Clone (or download) the repository

(On Window, you may need to install [Git](https://hackernoon.com/install-git-on-windows-9acf2a1944f0))

```
git clone https://github.com/bioimage-analysis/colocalization-malene
```

3- Go into the directory using the command line

```
$ cd /../colocalization-malene/
```

4- Create a conda environment with the dependency:

```
$ conda env create -f environment.yml
```

(To install python / conda on a Window environment you can follow this [LINK](https://medium.com/@GalarnykMichael/install-python-on-windows-anaconda-c63c7c3d1444))

```
$ conda env create -f environment.yml
```

5- Activate your conda environment:

```
$ conda activate malene
```

6- To go back to your master environment:

```
$ conda deactivate
```

(The installation of python-bioformats / javabridge might fail, if so, download Java Dev. kit, [here](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html))

## Usage

from the command line cd to the notebook directory and lunch jupyter notebook:

```
jupyter notebook
```
You will find a basic introduction on how to use the Jupyter Notebook [HERE](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Notebook%20Basics.html)

## Note about Notebook in github

If it doesn't load try using this [link](https://nbviewer.jupyter.org/).

## Contact
Cedric Espenel  
E-mail: espenel@stanford.edu
