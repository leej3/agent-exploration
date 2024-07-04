#!/bin/bash
source /opt/conda/etc/profile.d/mamba.sh
micromamba activate /opt/conda/env
exec "$@"