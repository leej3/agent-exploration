#!/bin/bash
eval "$(/bin/micromamba shell hook --shell bash)"
micromamba activate /opt/conda/env
exec "$@"