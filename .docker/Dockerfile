# Docker image with Playwright and other convenient tools for agent based development
# docker run -it --rm --ipc=host --user pwuser --security-opt seccomp=seccomp_profile.json [this image] /bin/bash
# See https://playwright.dev/docs/docker for more info.
FROM mcr.microsoft.com/playwright:v1.45.1-noble

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV ENV_NAME="base"
ENV MAMBA_ROOT_PREFIX="/opt/conda"
ENV MAMBA_EXE="/usr/local/bin/micromamba"
ENV PATH=$MAMBA_ROOT_PREFIX/bin:$PATH
ARG VERSION=1.5.8

# For a non root user
ARG MAMBA_USER=mambauser
ARG MAMBA_USER_ID=57439
ARG MAMBA_USER_GID=57439
ENV MAMBA_USER=$MAMBA_USER
ENV MAMBA_USER_ID=$MAMBA_USER_ID
ENV MAMBA_USER_GID=$MAMBA_USER_GID

# Install necessary packages for micromamba installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    bzip2 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt /var/lib/dpkg /var/lib/cache /var/lib/log

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG TARGETARCH=amd64

# Create non-root user
RUN addgroup --gid $MAMBA_USER_GID $MAMBA_USER && \
    adduser --uid $MAMBA_USER_ID --gid $MAMBA_USER_GID --disabled-password --gecos "" $MAMBA_USER

RUN test "$TARGETARCH" = 'amd64' && export ARCH='64'; \
    test "$TARGETARCH" = 'arm64' && export ARCH='aarch64'; \
    test "$TARGETARCH" = 'ppc64le' && export ARCH='ppc64le'; \
    curl -L "https://micro.mamba.pm/api/micromamba/linux-${ARCH}/${VERSION}" | \
    tar -xj -C "/usr/local/bin" --strip-components=1 bin/micromamba && \
    chmod +x /usr/local/bin/micromamba

# Create MAMBA_ROOT_PREFIX directory
RUN mkdir -p $MAMBA_ROOT_PREFIX && \
    chmod -R 777 $MAMBA_ROOT_PREFIX && \
    chown -R $MAMBA_USER:$MAMBA_USER $MAMBA_ROOT_PREFIX

##### Switch to mamba user #####

USER $MAMBA_USER
WORKDIR /home/$MAMBA_USER

# Verify micromamba installation
RUN if [ ! -f /usr/local/bin/micromamba ]; then echo "micromamba installation failed"; exit 1; fi

# Create conda environment
COPY .docker/environment.yaml /tmp/environment.yaml
RUN mkdir -p $MAMBA_ROOT_PREFIX && \
    $MAMBA_EXE shell init --shell bash --prefix $MAMBA_ROOT_PREFIX && \
    $MAMBA_EXE create -y -f /tmp/environment.yaml -p $MAMBA_ROOT_PREFIX/env && \
    $MAMBA_EXE clean --all --yes && \
    chmod -R 777 $MAMBA_ROOT_PREFIX



### Set entrypoints and other things that execute quickly ###

# Script which launches commands passed to "docker run"
COPY .docker/_entrypoint.sh /usr/local/bin/_entrypoint.sh
COPY .docker/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]

# Default command for "docker run"
CMD ["/bin/bash"]

# Script which launches RUN commands in Dockerfile
COPY .docker/_dockerfile_shell.sh /usr/local/bin/_dockerfile_shell.sh
SHELL ["/usr/local/bin/_dockerfile_shell.sh"]
WORKDIR /mnt