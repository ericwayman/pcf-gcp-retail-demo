#!/bin/bash

source_jar="./time-source/target/time-source-0.0.1-SNAPSHOT.jar"
proc_jar="./transform-proc/target/transform-proc-0.0.1-SNAPSHOT.jar"
sink_jar="./log-sink/target/log-sink-0.0.1-SNAPSHOT.jar"
service="pubsub"

cf push time-source --no-start -p $source_jar -m 1024M
cf bs time-source $service -c '{ "role": "pubsub.admin" }'
cf set-env time-source SPRING_APPLICATION_JSON "{\"spring.cloud.stream.bindings.output.destination\":\"ticktock\"}"
cf set-env time-source SPRING_CLOUD_STREAM_PUBSUB_BINDER_PROJECT_NAME spring-cloud-dataflow-148214
cf start time-source

cf push processor --no-start -p $proc_jar -m 1024M
cf bs processor $service -c '{ "role": "pubsub.admin" }'
cf set-env processor SPRING_APPLICATION_JSON '{"spring.cloud.stream.bindings.input.destination": "ticktock", "spring.cloud.stream.bindings.output.destination": "postproc"}'
cf set-env processor SPRING_CLOUD_STREAM_PUBSUB_BINDER_PROJECT_NAME spring-cloud-dataflow-148214
cf start processor

cf push log-sink --no-start -p $sink_jar -m 1024M
cf bs log-sink $service -c '{ "role": "pubsub.admin" }'
cf set-env log-sink SPRING_APPLICATION_JSON "{\"spring.cloud.stream.bindings.input.destination\":\"postproc\"}"
cf set-env log-sink SPRING_CLOUD_STREAM_PUBSUB_BINDER_PROJECT_NAME spring-cloud-dataflow-148214
cf start log-sink

