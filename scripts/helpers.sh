#!/bin/bash

if [ -f env/config.json ]; then
    export METAFLOW_HOME=$(pwd)/env
fi

if [ -d ../metaflow ]; then
    if [ "" != "${FORCE_LOCAL_METAFLOW}" ]; then
        export PYTHONPATH=$PYTHONPATH:$(cd .. && pwd)/metaflow
    else
        export PYTHONPATH=
        echo "Not forcing use of $(cd .. && pwd)/metaflow"
    fi
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
    if [ ! -f FLOW_NAMES ]; then
        kubectl -n metaflow-jobs delete sensors --all=true
    else
        for name in $(cat FLOW_NAMES)
        do
            sensor_name=$(echo ${name} | tr -u "." "-")
            echo "Deleting ${sensor_name}"
            kubectl -n metaflow-jobs delete sensor ${sensor_name}
        done
    fi
}

argo_clean_templates() {
    if [ ! -f FLOW_NAMES ]; then
        kubectl -n metaflow-jobs delete workflowtemplates --all=true
    else 
        for name in $(cat FLOW_NAMES)
        do
            printf "Deleting %s workflow template\n" ${name}
            kubectl -n metaflow-jobs delete workflowtemplate ${name}
        done
    fi
}

_is_known_name() {
    workflow=${1}
    names=${2}
    for name in ${names}
    do
        result=$(expr ${workflow} : ${name})
        if [ ${result} -gt 0 ]; then
            echo "${workflow} : ${name} == yes" 1>&2
            echo "yes"
            return
        else
            echo "${workflow} : ${name} == no" 1>&2
        fi
    done
    echo "no"
}

argo_clean_workflows() {
    if [ -f FLOW_NAMES ]; then
        all_names=$(cat FLOW_NAMES)
        all_workflows="$(kubectl -n metaflow-jobs get workflows | grep -v NAME)"
        for workflow in $(echo ${all_workflows} | grep "${1}" | awk '{print $1}')
        do
            result=$(_is_known_name "${workflow}" "${all_names}")
            if [ "${result}" = "yes" ]; then
                printf "Deleting %s workflow\n" ${workflow}
                #kubectl -n metaflow-jobs delete --ignore-not-found=false workflow ${workflow}
            fi
        done
    fi
}

argo_test() {
    python test_flows $@
}

burn_in() {
    if [ -d ./scripts ]; then
        scripts/burn_in.sh $@
    elif [ -f burn_in.sh ]; then
        ./burn_in.sh $@
    else
        echo "Can't locate burn_in.sh!" 1>&2
        exit 1
    fi
}

alias acr="argo_create"
alias atr="argo_trigger"
alias ade="argo_delete"
alias argo_clean="argo_clean_sensors;argo_clean_templates;argo_clean_workflows"
alias acl="argo_clean"
