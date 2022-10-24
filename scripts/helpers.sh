#!/bin/bash

if [ -f env/config.json ]; then
    export METAFLOW_HOME=$(pwd)/env
fi

if [ -d ../metaflow ]; then
    export PYTHONPATH=$PYTHONPATH:$(cd .. && pwd)/metaflow
fi

flow() {
    if [ $# -lt 1 ]; then
        exit 3
    fi

    local flow_name="${1}"
    shift

    python test_flows/${flow_name}.py $@
}

argo_create() {
    local flow_name="${1}"
    shift

    if [ ! -f ./${flow_name} ]; then
      exit 3
    fi

    python ./${flow_name} argo-workflows create
}

argo_trigger() {
    local flow_name="${1}"
    shift
    
    if [ ! -f ./${flow_name} ]; then
        exit 3
    fi

    python ./${flow_name} argo-workflows trigger
}

argo_delete() {
    local flow_name="${1}"
    shift

    if [ ! -f ./${flow_name} ]; then
        exit 3
    fi

    python ./${flow_name} argo-workflows delete
}

argo_clean_sensors() {
    kubectl -n metaflow-jobs delete sensors --all=true
}

argo_clean_templates() {
    kubectl -n metaflow-jobs delete workflowtemplates --all=true
}

argo_clean_workflows() {
    if [ $# -lt 1 ]; then
        kubectl -n metaflow-jobs delete workflows --all=true
    else
        all_workflows="$(kubectl -n metaflow-jobs get workflows | grep -v NAME)"
        while [ "${1}" != "" ]
        do
            for workflow in $(echo ${all_workflows} | grep "${1}" | awk '{print $1}')
            do
                printf "Deleting %s workflow\n" ${workflow}
                kubectl -n metaflow-jobs delete --ignore-not-found=false workflow ${workflow}
            done
            shift
        done
    fi
}

argo_test() {
    python test_flows ${1}
}

alias acr="argo_create"
alias atr="argo_trigger"
alias ade="argo_delete"
alias argo_clean="argo_clean_sensors;argo_clean_templates;argo_clean_workflows"
alias acl="argo_clean"
alias burn_in="$(cd $(dirname ${0}) && pwd)/burn_in.sh $@"