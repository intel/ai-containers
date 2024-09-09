#!/bin/bash
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

set -ex

pt_package_name="pytorch_modules-v${PT_VERSION}_${VERSION}_${REVISION}.tgz"
os_string="ubuntu${OS_NUMBER}"
case "${BASE_NAME}" in
*rhel9.2*)
	os_string="rhel92"
	;;
*rhel9.4*)
	os_string="rhel94"
	;;
*rhel8*)
	os_string="rhel86"
	;;
*amzn2*)
	os_string="amzn2"
	;;
*tencentos*)
	os_string="tencentos31"
	;;
esac
pt_artifact_path="https://${ARTIFACTORY_URL}/artifactory/gaudi-pt-modules/${VERSION}/${REVISION}/pytorch/${os_string}"

tmp_path=$(mktemp --directory)
wget --no-verbose "${pt_artifact_path}/${pt_package_name}"
tar -xf "${pt_package_name}" -C "${tmp_path}"/.
pushd "${tmp_path}"
./install.sh "$VERSION" "$REVISION"
popd
# cleanup
rm -rf "${tmp_path}" "${pt_package_name}"
