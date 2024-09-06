#!/bin/bash -ex

# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DEFAULT_EFA_INSTALLER_VER=1.29.0
efa_installer_version=${1:-$DEFAULT_EFA_INSTALLER_VER}

tmp_dir=$(mktemp -d)
wget -nv https://efa-installer.amazonaws.com/aws-efa-installer-$efa_installer_version.tar.gz -P $tmp_dir
tar -xf $tmp_dir/aws-efa-installer-$efa_installer_version.tar.gz -C $tmp_dir
pushd $tmp_dir/aws-efa-installer
case $(. /etc/os-release ; echo -n $ID) in
    rhel)
        # we cannot install dkms packages on RHEL images due to OCP rules
        rm -f RPMS/RHEL8/x86_64/dkms*.rpm
    ;;
    tencentos)
        dnf install -y RPMS/ROCKYLINUX8/x86_64/rdma-core/libibverbs-46.0-1.el8.x86_64.rpm RPMS/ROCKYLINUX8/x86_64/rdma-core/libibverbs-utils-46.0-1.el8.x86_64.rpm
        patch -f -p1 -i /tmp/tencentos_efa_patch.txt --reject-file=tencentos_efa_patch.rej --no-backup-if-mismatch
    ;;
esac
./efa_installer.sh -y --skip-kmod --skip-limit-conf --no-verify
popd
rm -rf $tmp_dir
