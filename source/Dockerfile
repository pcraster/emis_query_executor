FROM pcraster/emis_base:1.0.0

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

RUN set -x && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libhdf5-dev && \
    rm -fr /var/lib/apt/lists/* && \
    cd /opt && \
    wget --progress=bar:force https://cmake.org/files/v3.5/cmake-3.5.2-Linux-x86_64.tar.gz && \
    tar zxf cmake-3.5.2-Linux-x86_64.tar.gz && \
    ln -s cmake-3.5.2-Linux-x86_64 cmake && \
    export PATH="/opt/cmake/bin:$PATH" && \
    git clone --recursive https://github.com/geoneric/peacock.git /tmp/peacock && \
    mkdir /tmp/build && \
    cd /tmp/build && cmake \
        -Dpeacock_prefix=/usr/local \
        -Dbuild_boost=true -Dboost_version=1.57.0 \
            -Dboost_build_boost_test=TRUE \
        -Dbuild_pybind11=true -Dpybind11_version=1.8.1 \
        /tmp/peacock && \
    cmake --build /tmp/build --target all && \
    rm -fr /tmp/build

COPY requirements.txt /
RUN pip install -r requirements.txt

RUN pip install \
    --pre \
    --global-option=build_ext \
    --global-option="-I/usr/include/hdf5/serial:/usr/local/lib/python3.5/site-packages/numpy/core/include:/usr/local/linux/linux/gcc-4/x86_64/include" \
    --global-option="-L/usr/lib/x86_64-linux-gnu/hdf5/serial/lib:/usr/local/linux/linux/gcc-4/x86_64/lib" \
    "lue==0.0.0.dev3"

ENV LD_LIBRARY_PATH=/usr/local/linux/linux/gcc-4/x86_64/lib:$LD_LIBRARY_PATH

COPY cmd.sh server.py /
COPY emis_query_executor /emis_query_executor
COPY test /test
COPY emis /emis

CMD ["/cmd.sh"]
