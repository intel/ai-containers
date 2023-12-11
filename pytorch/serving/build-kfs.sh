cd ..
docker compose pull torchserve
docker tag $(docker images -q | head -n1) intel/torchserve:latest-kfs
git clone https://github.com/pytorch/serve
cd serve/kubernetes/kserve
git apply ../../../serving/kfs.patch
git submodule update --init --recursive
./build_image.sh
