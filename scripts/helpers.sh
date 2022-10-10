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
    for sensor in $(kubectl -n metaflow-jobs get sensors | grep -v NAME | awk '{print $1}')
    do
        printf "Deleting %s sensor\n" ${sensor}
        kubectl -n metaflow-jobs delete sensor ${sensor}
    done
}

argo_clean_templates() {
    for template in $(kubectl -n metaflow-jobs get workflowtemplates | grep -v NAME | awk '{print $1}')
    do
        printf "Deleting %s workflow template\n" ${template}
        kubectl -n metaflow-jobs delete workflowtemplate ${template}
    done
}

argo_clean_workflows() {
    all_workflows="$(kubectl -n metaflow-jobs get workflows | grep -v NAME)"
    if [ $# -lt 1 ]; then
        for workflow in $(echo ${all_workflows} | awk '{print $1}')
        do
            printf "Deleting %s workflow\n" ${workflow}
            kubectl -n metaflow-jobs delete workflow ${workflow}
        done
    else
        while [ "${1}" != "" ]
        do
            for workflow in $(echo ${all_workflows} | grep "${1}" | awk '{print $1}')
            do
                printf "Deleting %s workflow\n" ${workflow}
                kubectl -n metaflow-jobs delete workflow ${workflow}
            done
            shift
        done
    fi
}

_argo_clean_short() {
    argo_clean_workflows 30s 31s 32s 33s 34s 35s 36s 38s 39s 40s 41s 42s 43s 44s 45s 46s 47s 48s 49s 50s 51s 52s 53s 54s 55s 56s 57s 58s 59s
}

_argo_clean_mid() {
    argo_clean_workflows 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 11m 12m 13m 14m 15m
}

argo_test() {
    python test_flows ${1}
}

alias acr="argo_create"
alias atr="argo_trigger"
alias ade="argo_delete"
alias argo_clean="argo_clean_sensors;argo_clean_templates;_argo_clean_short;_argo_clean_mid"
alias acl="argo_clean"