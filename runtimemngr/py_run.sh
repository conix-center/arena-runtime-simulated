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

python3=`which python3`
pip=`which pip3`
wget=`which wget`
mosquitto_pub=`which mosquitto_pub`
mosquitto_sub=`which mosquitto_sub`
if [ -z "$workdir" ]
then
      workdir=`mktemp -d`
fi
virtualenv=`which virtualenv`

wget_options='-q -r -nH --cut-dirs=4 --no-parent --reject="index.html*"'
wget_credentials='--user=devtest --password=dev#test20'

cd ${workdir}

${wget} ${wget_options} ${wget_credentials} ${__store_url}/users/${__name}/ > /dev/null
fn=$(basename -- "${__filename}")
ext="${fn##*.}"
fn="${fn%.*}"

test -d venv || ${virtualenv} -p ${python3} venv
. venv/bin/activate

if [ "$ext" = "zip" ]; then
    unzip ${workdir}/${__filename}
fi

${pip} install -Ur requirements.txt

if [ "${__pipe_stdin_stdout}" = "True" ]; then
     echo "Running: ${mosquitto_sub} -h ${__mqtt_srv} -t ${__sub_topic} | { exec ${python3} -u ${__filename} ${__args}; pkill -g 0; } |& ${mosquitto_pub} -h ${__mqtt_srv} -t ${__pub_topic} -l"
     ${mosquitto_sub} -h ${__mqtt_srv} -t ${__sub_topic} | { exec ${python3} -u ${__filename} ${__args}; echo "Module exited."; ${mosquitto_pub} -h ${__mqtt_srv} -t ${__done_topic} -m "${__done_msg}"; sleep 1; pkill -g 0; } |& ${mosquitto_pub} -h ${__mqtt_srv} -t ${__pub_topic} -l
else
    echo "Running: ${python3} ${__filename}"
    ${python3} ${__filename} ${__args}

    echo "Module exited. -t ${__done_topic} -m ${__done_msg}" |& ${mosquitto_pub} -h ${__mqtt_srv} -t ${__pub_topic} -l

    ${mosquitto_pub} -h ${__mqtt_srv} -t ${__done_topic} -m "${__done_msg}"
fi


touch venv/bin/activate
