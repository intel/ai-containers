#!/bin/bash
set -e

_BASE_NAME=${1:-"ubuntu22.04"}
_SSL_LIB=""

# preinstall dependencies and define variables
case "${_BASE_NAME}" in
    *ubuntu22.04*)
        echo "Skip install Python3.10 from source on Ubuntu22.04"
        exit 0;
    ;;
    *debian* | *ubuntu*)
        apt update
        apt install -y libsqlite3-dev libreadline-dev
    ;;
    *rhel*)
        yum install -y sqlite-devel readline-devel xz-devel
    ;;
    *tencentos3.1*)
        dnf install -y sqlite-devel readline-devel zlib-devel xz-devel bzip2-devel libffi-devel
        wget -nv -O /opt/openssl-1.1.1w.tar.gz https://github.com/openssl/openssl/releases/download/OpenSSL_1_1_1w/openssl-1.1.1w.tar.gz && \
            cd /opt/ && \
            tar xzf openssl-1.1.1w.tar.gz && \
            rm -rf openssl-1.1.1w.tar.gz && \
            cd openssl-1.1.1w && \
            ./config --prefix=/usr/local/openssl-1.1.1w shared zlib && \
            make && make install
        ln -s /etc/pki/tls/cert.pem /usr/local/openssl-1.1.1w/ssl/cert.pem

        PATH=$PATH:/usr/local/protoc/bin:/usr/local/openssl-1.1.1w/bin
        LD_LIBRARY_PATH=/usr/local/openssl-1.1.1w/lib:$LD_LIBRARY_PATH
        _SSL_LIB="--with-openssl=/usr/local/openssl-1.1.1w"
    ;;
    *amzn2*)
        yum install -y sqlite-devel readline-devel
        wget -nv -O /opt/openssl-1.1.1w.tar.gz https://github.com/openssl/openssl/releases/download/OpenSSL_1_1_1w/openssl-1.1.1w.tar.gz && \
            cd /opt/ && \
            tar xzf openssl-1.1.1w.tar.gz && \
            rm -rf openssl-1.1.1w.tar.gz && \
            cd openssl-1.1.1w && \
            ./config --prefix=/usr/local/openssl-1.1.1w shared zlib && \
            make && make install
        ln -s /etc/pki/tls/cert.pem /usr/local/openssl-1.1.1w/ssl/cert.pem

        PATH=$PATH:/usr/local/protoc/bin:/usr/local/openssl-1.1.1w/bin
        LD_LIBRARY_PATH=/usr/local/openssl-1.1.1w/lib:$LD_LIBRARY_PATH
        _SSL_LIB="--with-openssl=/usr/local/openssl-1.1.1w"
    ;;
esac

# install Python
wget -nv -O /opt/Python-3.10.14.tgz https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
cd /opt/
tar xzf Python-3.10.14.tgz
rm -f Python-3.10.14.tgz
cd Python-3.10.14
./configure --enable-optimizations --enable-loadable-sqlite-extensions --enable-shared $_SSL_LIB
make -j && make altinstall

# post install
case "${_BASE_NAME}" in
    *rhel9*)
        alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.10 2 && \
        alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
        alternatives --set python3 /usr/local/bin/python3.10
        export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
    ;;
    *tencentos3.1*)
        alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.10 4 && \
        alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 3 && \
        alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2 && \
        alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 && \
        alternatives --set python3 /usr/local/bin/python3.10
        export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
    ;;
    *amzn2*)
        update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.10 3 && \
        update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2 && \
        update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
    ;;
    *debian*)
        update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.10 3
        update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.8 2
        update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
    ;;
esac

python3 -m pip install --upgrade pip setuptools

