#!/bin/bash

if [ -f env/config.json ]; then
    export METAFLOW_HOME=$(pwd)/env
fi

flow() {
    if [ $# -lt 1 ]; then
        exit 3
    fi

    local flow_name="${1}"
    shift

    python test_flows/${flow_name}.py $@
}

load_test_flows() {
    for f in $(ls test_flows/{foo,bar,baz,goodbye,hello,rip,three_way}.py)
    do
        python ${f} argo-workflows create
    done
}