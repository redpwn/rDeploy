# RedpwnCTF Deployment

RedpwnCTF's automated deployment solution

## Problem Files

RedpwnCTF uses standardized YAML "challenge definition files" to specify deployment instructions to the automated deployment software. Also, the information stored in the file is generally useful information that the organizers use to put the challenges on CTFd.

The problem directory should be cloned into `data` and specified in `config/config.json`. 

The directory structure should look as so, which is how the current redpwnCTF challenge directories are setup.

```
root /
  pwn /
    chall1 / 
    chall2 /
    chall3 /
  web /
    chall1 /
    chall2 /
  crypto /
    ...
  ...
```

## Usage

```
python main.py
```
