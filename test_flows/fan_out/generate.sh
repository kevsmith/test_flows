#!/bin/bash

i=1
max_flows=${1}
base_path=$(dirname ${0})

while [ $i -lt ${max_flows} ] || [ $i -eq ${max_flows} ]
do
    e="s/FlowNameFlow/Flow${i}/g"
    cp ${base_path}/template.pyt "${base_path}/flow${i}.py"
    sed -i "" -e ${e} ${base_path}/flow${i}.py
    i=$(expr ${i} + 1)
done