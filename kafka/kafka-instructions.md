# Use Helm To Install Kafka

helm install --values kafka-values.yaml kafka oci://registry-1.docker.io/bitnamicharts/kafka --version 30.0.4

# Consumers

kafka.group-01.svc.cluster.local:9092

# Producers

kafka-controller-0.kafka-controller-headless.group-01.svc.cluster.local:9092
kafka-controller-1.kafka-controller-headless.group-01.svc.cluster.local:9092
kafka-controller-2.kafka-controller-headless.group-01.svc.cluster.local:9092

# Pod create

```
kubectl run kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.8.0-debian-12-r3  --command -- sleep infinity
```

## Connect into

kubectl exec --tty -i kafka-client --namespace group-01 -- bash
