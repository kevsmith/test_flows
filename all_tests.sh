#!/bin/bash

homes="$(pwd)/env_nats $(pwd)/env_webhook"
tests="li hy ty pa us"

FORCE_LOCAL_METAFLOW=1
source scripts/helpers.sh

for home in ${homes}
do
    echo "METAFLOW_HOME: ${home}"
    tests="$(echo ${tests} | shuffle)"
    for t in ${tests}
    do
        METAFLOW_HOME=${home} argo_test ${t}
    done
    echo ""
done