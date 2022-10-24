#!/bin/bash

SCRIPT_DIR=$(dirname ${0})

source ${SCRIPT_DIR}/helpers.sh

DEFAULT_MAX=5
DEFAULT_TESTS="hy li pa us"

prepare_tests() {
  argo_clean_workflows
  argo_clean
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