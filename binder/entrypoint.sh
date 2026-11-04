#!/bin/bash

set -e

source "${ROS_PATH}/setup.bash"

if [[ -f /workspace/ros/install/setup.bash ]]; then
    source /workspace/ros/install/setup.bash
fi

log_startup_context() {
    local log_file="/tmp/binder-startup.log"
    {
        echo "=== Binder entrypoint startup context ==="
        echo "date=$(date -Iseconds)"
        echo "pwd=$(pwd)"
        printf 'argv='
        printf '%q ' "$@"
        printf '\n'
        echo "--- selected environment ---"
        env | sort | grep -E '^(BINDER|JUPYTER|JUPYTERHUB|NB|REPO|URL|PATH|QUERY|ROBOT|TASK|ENVIRONMENT)=' || true
        echo "=== end startup context ==="
    } | tee "${log_file}" >&2
}

log_startup_context "$@"

exec "$@"
