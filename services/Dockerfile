FROM ubuntu:20.04

RUN apt-get update

RUN apt-get install tzdata
RUN echo Europe/Berlin > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

ENV USERNAME=p2w
RUN useradd $USERNAME && mkdir /home/$USERNAME && chown -R $USERNAME:users /home/$USERNAME
WORKDIR /home/$USERNAME

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    python3-distutils \
    python3-setuptools

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN apt-get install -y --no-install-recommends \
        libegl1-mesa \
        libgl1-mesa-dri \
        x11-xserver-utils \
        libxkbcommon-x11-0 \
        x11-utils \
        xvfb \
        x11vnc \
        libnss3 \
        libasound2 \
        gcc \
        g++ \
        libglib2.0-0 \
        libfontconfig1 \
        libxrender1 \
        libsm6 \
        libxext6 \
        build-essential \
        cmake \
        libxml2 \
        libxslt1.1 \
        qt5-default  # change if scanner switch to pyside6

ENV DISPLAY=:99
ENV SCREEN=0
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null
ENV XDG_RUNTIME_DIR=/run/user/1000

RUN mkdir -p -m 0700 $XDG_RUNTIME_DIR && chown -R $USERNAME:users $XDG_RUNTIME_DIR

USER $USERNAME

ENV QT_DEBUG_PLUGINS=0
ENV QT_VERBOSE false
ENV QT_TESTING false

COPY . /home/$USERNAME

CMD ["python3", "run.py"]