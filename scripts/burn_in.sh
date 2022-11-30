#!/bin/bash

DEFAULT_MAX=5
DEFAULT_TESTS=$(echo "hy li pa us" | shuffle)

argo_test() {
    python test_flows ${1}
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

prepare_tests() {
  argo_clean_workflows
  argo_clean_sensors
  argo_clean_templates
}

MAX=${DEFAULT_MAX}
TESTS=""

while [ $# -gt 0 ];
do
  case ${1} in
    --max)
      MAX=${2}
      shift;;
    -m)
      MAX=${2}
      shift;;
    *)
      if [ "${TESTS}" == "" ]; then
        TESTS="${1}"
      else
        TESTS="${TESTS} ${1}"
      fi
  esac
  shift
done

if [ "${MAX}" == "" ]; then
  exit 1
fi

if [ "${TESTS}" == "" ]; then
  TESTS=${DEFAULT_TESTS}
fi

prepare_tests
clear

i=0

echo "Burning in suites ${TESTS} for ${MAX} iterations"
while [ ${i} -lt ${MAX} ]
do
  echo "Burn in pass # $(expr ${i} + 1)"
  echo ""
  for suite in $(echo ${TESTS} | shuffle)
  do
    argo_test ${suite}
  done
  i=$(expr ${i} + 1)
done