#!/bin/bash
eval "$(/usr/local/bin/micromamba shell hook --shell bash)"
micromamba activate /opt/conda/env
exec "$@"