#!/bin/bash

#realm/proc/control {"object_id":"c7ab078b-c832-43cc-8ad2-e68cfc910c75","action":"create","type":"arts_req","data":{"type":"module","uuid":"e5f4439e-5a02-4e5d-9d72-704d171d8949","name":"wiselab/configure_scene_room1","parent":"{}","filename":"ground-scale.py","fileid":"na","filetype":"PY","env":"SCENE=room1 MQTTH=arena.andrew.cmu.edu REALM=realm","args":"","channels":[{"path":"/ch/room1","type":"pubsub","mode":"rw","params":{"topic":"realm/s/room1"}}],"wait_state":"false"}}
#realm/proc/control {"object_id":"638eda2f-00a9-4a3d-b281-4ba10414db08","action":"create","type":"arts_req","data":{"type":"module","uuid":"aca2b0ba-429c-4186-ba7a-74dd7140bec7","name":"wiselab/robot-arm","parent":"{}","filename":"robot-arm.py","fileid":"na","filetype":"PY","env":"SCENE=room1 MQTTH=arena.andrew.cmu.edu REALM=realm","args":"","channels":[{"path":"/ch/room1","type":"pubsub","mode":"rw","params":{"topic":"realm/s/room1"}}],"wait_state":"false"}}
#realm/proc/control/370c9341-8094-412c-a9bc-c809075f4453 {"object_id": "486ef8a2-2a63-404b-b515-ec99b5b95e97", "action": "create", "type": "arts_req", "data": {"type": "module", "uuid": "e5f4439e-5a02-4e5d-9d72-704d171d8949", "name": "wiselab/configure_scene_room1", "parent": {"uuid": "370c9341-8094-412c-a9bc-c809075f4453"}, "filename": "ground-scale.py", "fileid": "na", "filetype": "PY", "apis": "python:python3", "args": "", "env": "SCENE=room1 MQTTH=arena.andrew.cmu.edu REALM=realm", "channels": "[{'path': '/ch/room1', 'type': 'pubsub', 'mode': 'rw', 'params': {'topic': 'realm/s/room1'}}]"}}

# load secrets
export $(grep -v '^#' secrets.env | xargs)

export __mqtt_srv="arena.andrew.cmu.edu"
export __mqtt_prt=8883
export __store_url="https://arena.andrew.cmu.edu/store"
export __name="wiselab/tmp/robot-arm"
export __filename="robot-arm.py"
export __fid=""
export __pipe_stdin_stdout="True"
export __sub_topic="realm/proc/debug/stdin/e5f4439e-5a02-4e5d-9d72-704d171d8949"
export __pub_topic="realm/proc/debug/stdout/e5f4439e-5a02-4e5d-9d72-704d171d8949"
export __args=""
export __done_topic="realm/proc/control/370c9341-8094-412c-a9bc-c809075f4453"
export __done_msg='{"object_id": "486ef8a2-2a63-404b-b515-ec99b5b95e97", "action": "delete", "type": "arts_req", "data": {"type": "module", "uuid": "e5f4439e-5a02-4e5d-9d72-704d171d8949"}}'

export SCENE="room1"
export MQTTH="arena.andrew.cmu.edu"
export REALM="realm"

export workdir="$(pwd)/tmp"
rm -fr ./tmp
mkdir ./tmp
echo $workdir

../../runtimemngr/py_run.sh
