#!/bin/bash

# Create the service instances required for SCDF server on Cloud Foundry

cf cs p-redis shared-vm redis
cf cs p-rabbitmq standard rabbit
cf cs p-mysql 100mb mysql

