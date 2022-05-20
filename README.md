# docker-compose

To build an specific container (like Jupyter for example) try:
- `$ make jupyter`
and then check:
`$ docker images | grep -i 'tf-base' | grep -i 'jupyter'`
and you should have something like the following:
`tf-base                                                                2.8.0-jupyter-ubuntu-20.04                                   561dd9bc65ba   33 minutes ago   1.36GB`

To build all the containers try:
- `$ make all`
- and then check:
`$ docker images | grep -i 'tf-base'
and you should have something like the following:
```
tf-base                                                                2.8.0-mpich-horovod-ubuntu-20.04                             df35fd668828   25 minutes ago   2.57GB
tf-base                                                                2.8.0-mpich-horovod-dev-ubuntu-20.04                         5b7a064b8138   25 minutes ago   1.75GB
tf-base                                                                2.8.0-mpich-ubuntu-20.04                                     067c719e3ea4   29 minutes ago   1.46GB
tf-base                                                                2.8.0-openmpi-horovod-ubuntu-20.04                           69d282e505c0   30 minutes ago   2.62GB
tf-base                                                                2.8.0-openmpi-horovod-dev-ubuntu-20.04                       4a4385b3271b   30 minutes ago   1.83GB
tf-base                                                                2.8.0-openmpi-ubuntu-20.04                                   62d68cba4fa4   35 minutes ago   1.51GB
tf-base                                                                2.8.0-jupyter-ubuntu-20.04                                   561dd9bc65ba   35 minutes ago   1.36GB
tf-base                                                                2.8.0-ubuntu-20.04                                           42ea6177d9da   36 minutes ago   1.19GB
```

To build `debian` image you can try:
`$ BASE_IMAGE_NAME=debian BASE_IMAGE_TAG=11 make all`
