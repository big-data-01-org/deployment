#!/bin/bash

# Ensure Helm is installed
if ! command -v helm &> /dev/null
then
    echo "Helm could not be found, please install Helm first."
    exit 1
fi

# Define variables
HELM_CHART="oci://registry-1.docker.io/bitnamicharts/kafka"
RELEASE_NAME="kafka"
VALUES_FILE="kafka-values.yaml"
CHART_VERSION="30.0.4"

# Install Kafka using Helm
helm install --values $VALUES_FILE $RELEASE_NAME $HELM_CHART --version $CHART_VERSION

# Check if the installation was successful
if [ $? -eq 0 ];  then
    echo "Kafka has been successfully installed."
    exit 0
else
    echo "Failed to install Kafka."
    exit 1
fi