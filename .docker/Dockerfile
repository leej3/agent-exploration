# Use Playwright base image
FROM mcr.microsoft.com/playwright:v1.45.1-noble AS base

# Mutli-stage build to keep final image small. Otherwise end up with
# curl and openssl installed
FROM debian:bookworm-slim AS stage1
ARG VERSION=1.5.8

# Install necessary packages for micromamba installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    bzip2 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt /var/lib/dpkg /var/lib/cache /var/lib/log

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG TARGETARCH
RUN test "$TARGETARCH" = 'amd64' && export ARCH='64'; \
    test "$TARGETARCH" = 'arm64' && export ARCH='aarch64'; \
    test "$TARGETARCH" = 'ppc64le' && export ARCH='ppc64le'; \
    curl -L "https://micro.mamba.pm/api/micromamba/linux-${ARCH}/${VERSION}" | \
    tar -xj -C "/tmp" "bin/micromamba"

FROM base

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV ENV_NAME="base"
ENV MAMBA_ROOT_PREFIX="/opt/conda"
ENV MAMBA_EXE="/bin/micromamba"

COPY --from=stage1 /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=stage1 /tmp/bin/micromamba "$MAMBA_EXE"

# Create non-root user
ARG MAMBA_USER=mambauser
ARG MAMBA_USER_ID=57439
ARG MAMBA_USER_GID=57439
ENV MAMBA_USER=$MAMBA_USER
ENV MAMBA_USER_ID=$MAMBA_USER_ID
ENV MAMBA_USER_GID=$MAMBA_USER_GID

RUN addgroup --gid $MAMBA_USER_GID $MAMBA_USER && \
    adduser --uid $MAMBA_USER_ID --gid $MAMBA_USER_GID --disabled-password --gecos "" $MAMBA_USER


RUN mkdir -p $MAMBA_ROOT_PREFIX && \
    $MAMBA_EXE create -y -p $MAMBA_ROOT_PREFIX/env && \
    $MAMBA_EXE install -y -p $MAMBA_ROOT_PREFIX/env -c conda-forge python=3.9 && \
    $MAMBA_EXE clean --all --yes

USER $MAMBA_USER




ENV PATH=$MAMBA_ROOT_PREFIX/bin:$PATH

WORKDIR /home/$MAMBA_USER

# for use with 'apptainer shell --shell /usr/local/bin/_apptainer_shell.sh ...'
COPY .docker/_apptainer_shell.sh /usr/local/bin/_apptainer_shell.sh

# Script which launches commands passed to "docker run"
COPY .docker/_entrypoint.sh /usr/local/bin/_entrypoint.sh
COPY .docker/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]

# Default command for "docker run"
CMD ["/bin/bash"]

# Script which launches RUN commands in Dockerfile
COPY .docker/_dockerfile_shell.sh /usr/local/bin/_dockerfile_shell.sh
SHELL ["/usr/local/bin/_dockerfile_shell.sh"]