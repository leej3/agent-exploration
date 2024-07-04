#!/bin/bash
eval "$(${MAMBA_EXE} shell hook --shell bash)"
micromamba activate ${MAMBA_ROOT_PREFIX}/env
exec "\$@"