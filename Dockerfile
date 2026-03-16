FROM ubuntu:22.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install core system utilities and diagnostic packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    can-utils \
    minicom \
    screen \
    usbutils \
    net-tools \
    iproute2 \
    kmod \
    git \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install Python OBD libraries
RUN pip3 install --no-cache-dir \
    obd \
    pyserial \
    python-can \
    cantools \
    udsoncan

# Create a directory for your diagnostic scripts
WORKDIR /diagnostics
COPY . /diagnostics

# Set the entrypoint to a bash shell so you can run the tools interactively
CMD ["/bin/bash"]