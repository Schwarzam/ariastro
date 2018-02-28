# `ariastro - being updated`

## Installation



### Set the path to GalFit executable

Next we will show you how to create a link named ```galfitm```that will be invoked by ```ariastro``` when needed. This link, in turn, must point to an existing GalFit executable, and it has to be in your system path. Below there is an example to be done if you have sudo access on your machine.

```shell
cd /usr/local/bin  # or other directory that is already in your path
sudo ln -s <path-to-galfit-executable> galfitm
```

#### no-sudo Alternative

If you don't have sudo access, you may try some of the following:

```shell
cd  # chances to home directory
mkdir bin
cd bin
ln -s <path-to-galfit-executable> galfitm
```
Then add the following line to your file ```~/.bashrc```:

```shell
export PATH="${PATH}:~/bin"
```

### Install `ariastro` package and scripts

```shell
cd CALIFA/github
sudo python setup.py develop
cd scripts
chmod +x *.py
```



## How to setup GitHub project

### On GitHub

Create project `ariastro`

### Local machine

#### Setup git 

```shell
git init
git remote add origin ssh://git@github.com/aricorte/ariastro.git
```

:notes: It is necessary to setup SSH key: please check https://github.com/trevisanj/oblivion/blob/master/github-ssh.md

#### Create commits 

```
git add . --all
git commit -m "first commit"
git push
```
git status
git add .--all
git commit -m "blah blah"
git push

## PyCharm shortcuts

  - rename file: Shift+F6
  - find file by name: Ctrl+Shift+N

## Astroenv
  
   source activate astroenv
