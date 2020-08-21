#!/bin/bash

# the env variables are given:
# ${__mqtt_srv}
# ${__store_url}
# ${__name}
# ${__filename}
# ${__fid}
# ${__pipe_stdin_stdout}
# ${__sub_topic}
# ${__pub_topic}
# ${__args}
# ${__done_topic}
# ${__done_msg}

wasmrt=/usr/local/bin/wasmer 
wget=/usr/local/bin/wget
mosquitto_pub=/usr/local/bin/mosquitto_pub
mosquitto_sub=/usr/local/bin/mosquitto_sub

workdir=`mktemp -d`

cd ${workdir}
${wget} ${wget_options} ${wget_credentials} ${__store_url}/users/${__name}/${__filename} > /dev/null
fn=$(basename -- "${__filename}")
ext="${fn##*.}"
fn="${fn%.*}"

if [ "${__pipe_stdin_stdout}" = "True" ]; then
    echo "Running: ${wasmrt} ${__filename} | ${__pub_topic}"
    ${wasmrt} ${__filename} | ${mosquitto_pub} -h ${__mqtt_srv} -t ${__pub_topic} -l
else
    echo "Running: ${wasmrt} ${__filename} "
    ${wasmrt} ${__filename}
fi

echo "Module done."
${mosquitto_pub} -h ${__mqtt_srv} -t ${__done_topic} -m ${__done_msg}