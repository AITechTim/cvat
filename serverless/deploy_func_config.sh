#!/bin/bash
# Sample commands to deploy nuclio functions on GPU

set -eu

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
func_config=${1}

nuctl create project cvat --platform local

shopt -s globstar

func_root="$(dirname "$func_config")"
func_rel_path="$(realpath --relative-to="$SCRIPT_DIR" "$(dirname "$func_root")")"

echo "Deploying $func_rel_path function..."
nuctl deploy --project-name cvat --path "$func_root" \
    --file "$func_config" --platform local

nuctl get function --platform local
