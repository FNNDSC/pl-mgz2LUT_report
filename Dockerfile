# Docker file for mgz2lut_report ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-mgz2LUT_report .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-mgz2LUT_report .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-mgz2LUT_report
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-mgz2LUT_report
#

FROM python:3.9.1-slim-buster
LABEL maintainer="Sandip Samal <sandip.samal@childrens.harvard.edu>"
RUN apt-get update \
    && apt-get install -y libsm6 libxext6 libxrender-dev wkhtmltopdf xvfb \
    && rm -rf /var/lib/apt/lists/*
    
ENV XDG_RUNTIME_DIR=/usr/local/src
ENV RUNLEVEL=3

WORKDIR /usr/local/src

COPY requirements.txt .
COPY mgz2lut_report/FreeSurferColorLUT.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install .

CMD ["mgz2lut_report", "--help"]
