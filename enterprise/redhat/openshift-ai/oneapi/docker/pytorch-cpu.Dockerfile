ARG BASE_IMAGE
ARG BASE_TAG
FROM ${BASE_IMAGE}:${BASE_TAG} AS python-base

USER root

RUN echo "[BaseOS]" > /etc/yum.repos.d/CentOS-Linux-BaseOS.repo && \
    echo "name=CentOS Linux 9 - BaseOS" >> /etc/yum.repos.d/CentOS-Linux-BaseOS.repo && \
    echo "baseurl=https://mirror.stream.centos.org/9-stream/BaseOS/x86_64/os" >> /etc/yum.repos.d/CentOS-Linux-BaseOS.repo && \
    echo "gpgkey=https://www.centos.org/keys/RPM-GPG-KEY-CentOS-Official-SHA256" >> /etc/yum.repos.d/CentOS-Linux-BaseOS.repo && \
    echo "gpgcheck=1" >> /etc/yum.repos.d/CentOS-Linux-BaseOS.repo

RUN echo "[centos9]" > /etc/yum.repos.d/CentOS-Linux-AppStream.repo && \
    echo "name=CentOS Linux 9 - AppStream" >> /etc/yum.repos.d/CentOS-Linux-AppStream.repo && \
    echo "baseurl=https://mirror.stream.centos.org/9-stream/AppStream/x86_64/os" >> /etc/yum.repos.d/CentOS-Linux-AppStream.repo && \
    echo "gpgkey=https://www.centos.org/keys/RPM-GPG-KEY-CentOS-Official-SHA256" >> /etc/yum.repos.d/CentOS-Linux-AppStream.repo && \
    echo "gpgcheck=1" >> /etc/yum.repos.d/CentOS-Linux-AppStream.repo

RUN dnf install -y \
        python3-dnf-plugin-versionlock && \ 
    dnf versionlock add redhat-release* && \
    dnf update -y && \
    dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
    dnf install -y \
        git \
        gperftools \
        python3.11 \
        python3.11-pip \
        python3.11-devel \
        rsync \
        unzip \
        wget && \
    dnf clean all && rm -rf /var/cache/yum

RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2 && \
    alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
    alternatives --set python3 /usr/bin/python3.11 && \
    alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.11 2 && \
    alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.9 1 && \
    alternatives --set pip3 /usr/bin/pip3.11

ENV APP_ROOT=/opt/app-root \
    HOME=/opt/app-root/src

WORKDIR ${APP_ROOT}

RUN python3.11 -m venv ${APP_ROOT} && \
    wget -O ${APP_ROOT}/bin/fix-permissions \
        https://raw.githubusercontent.com/sclorg/s2i-python-container/master/3.9-minimal/root/usr/bin/fix-permissions && \
    chown -R 1001:0 ${APP_ROOT} && \
    chmod +x ${APP_ROOT}/bin/fix-permissions && \
    ${APP_ROOT}/bin/fix-permissions ${APP_ROOT} -P && \
    echo "unset BASH_ENV PROMPT_COMMAND ENV" >> ${APP_ROOT}/bin/activate

ENV BASH_ENV="${APP_ROOT}/bin/activate"
ENV ENV="${APP_ROOT}/bin/activate"
ENV PROMPT_COMMAND=". ${APP_ROOT}/bin/activate"

SHELL ["/bin/bash", "-c"]

FROM python-base AS pytorch-notebook

#requirements.txt conflicts with the codeflare-sdk's requirements.txt. Hence the tmp- prefix
#Codeflare-sdk creates a dir called requirements.txt/requirements.txt and fails.
COPY --chown=1001:0 pytorch-requirements.txt tmp-requirements.txt

USER 1001

RUN python -m pip install --no-cache-dir -r tmp-requirements.txt && \
    rm -rf tmp-requirements.txt

RUN python -m ipykernel install --prefix=${APP_ROOT} --name 'pytorch-cpu' --display-name='pytorch-cpu' && \
    jupyter labextension disable "@jupyterlab/apputils-extension:announcements" && \
    chmod -R g+w ${APP_ROOT}/lib/python3.11/site-packages && \
    mkdir -p ${APP_ROOT}/src && \
    chmod -R g+w ${APP_ROOT}/src && \
    fix-permissions ${APP_ROOT} -P


#Replacing kernel manually with oneapi variable setting script
COPY --chown=1001:0 start-notebook.sh /opt/app-root/bin
COPY --chown=1001:0 builder /opt/app-root/builder
COPY --chown=1001:0 utils /opt/app-root/bin/utils

WORKDIR ${APP_ROOT}/src

ENV JUPYTER_PRELOAD_REPOS="https://github.com/IntelAI/oneAPI-samples"
ENV REPO_BRANCH="main"

ENTRYPOINT ["bash", "-c", "/opt/app-root/builder/run"]
