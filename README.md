# Cowry: A Secure FTP System

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8290e2c0bc824966948f26cfbbf6eb23)](https://www.codacy.com/app/yxwzaxns/cowry?utm_source=github.com&utm_medium=referral&utm_content=yxwzaxns/cowry&utm_campaign=badger)
[![Code Climate](https://codeclimate.com/github/yxwzaxns/cowry/badges/gpa.svg)](https://codeclimate.com/github/yxwzaxns/cowry)

![](docs/cowry.png)

## Introduction

Cowry is an open source project to transfer files security.

## Features
* Encryption base on TLS
* Encrypt local files in a variety of ways
* Do not need to leave a password to share files securely
* Friendly interface


## Install Cowry Server

```

git clone https://github.com/yxwzaxns/cowry.git

cd cowry/server

pip3 install -r requirements.txt

python3 server.py -n

python3 server.py -s

```

## Usage
```
git clone https://github.com/yxwzaxns/cowry.git

cd cowry/client

pip3 install -r requirements.txt

python3 client.py
```
