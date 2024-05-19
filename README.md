# k8s-webhook-python

Exploring kubernetes webhooks with python.

## Notes

Webhooks are in an audit mode and will not enforce any validations.

`response["response"]["allowed"] = True`

```
k8s-webhook 2024-05-18 14:37:15,834: INFO - Kind: AdmissionReview, apiVersion: admission.k8s.io/v1 - ReplicaSet - CREATE - test - test-000-746d9bcdbf
k8s-webhook 2024-05-18 14:37:15,835: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': '176c1e41-fe7b-4ffc-ae90-26781c378c5f', 'status': {'message': 'test-000-746d9bcdbf - Less then or equal to 2'}}}
k8s-webhook 2024-05-18 14:37:15,838: INFO - 172.18.0.3 - - [18/May/2024 14:37:15] "POST /validate-replicas?timeout=10s HTTP/1.1" 200 -
k8s-webhook 2024-05-18 14:37:15,864: INFO - Kind: AdmissionReview, apiVersion: admission.k8s.io/v1 - Pod - CREATE - test - test-000-746d9bcdbf-g7mnc
k8s-webhook 2024-05-18 14:37:15,869: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': 'fb674fd6-a40d-4da2-a2e0-223477db7776', 'status': {'message': 'TOTAL CPU: 0.100 | TOTAL MEM:  524288000 B, 500.0 MB'}}}
k8s-webhook 2024-05-18 14:37:15,870: INFO - 172.18.0.3 - - [18/May/2024 14:37:15] "POST /validate-resources?timeout=10s HTTP/1.1" 200 -
k8s-webhook 2024-05-18 14:37:15,882: INFO - Kind: AdmissionReview, apiVersion: admission.k8s.io/v1 - ReplicaSet - CREATE - test - test-001-6cffdc76b
k8s-webhook 2024-05-18 14:37:15,882: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': '530d356b-3be7-4187-9e92-3b29504f3fbb', 'status': {'message': 'test-001-6cffdc76b - Less then or equal to 2'}}}
k8s-webhook 2024-05-18 14:37:15,884: INFO - 172.18.0.3 - - [18/May/2024 14:37:15] "POST /validate-replicas?timeout=10s HTTP/1.1" 200 -
k8s-webhook 2024-05-18 14:37:15,902: INFO - Kind: AdmissionReview, apiVersion: admission.k8s.io/v1 - Pod - CREATE - test - test-001-6cffdc76b-q4d8m
k8s-webhook 2024-05-18 14:37:15,904: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': 'fdf8fdf2-7616-4a98-a2a7-7545c639380e', 'status': {'message': 'TOTAL CPU: 0.400 | TOTAL MEM:  2149580800 B, 2.0 GB'}}}
k8s-webhook 2024-05-18 14:37:15,905: INFO - 172.18.0.3 - - [18/May/2024 14:37:15] "POST /validate-resources?timeout=10s HTTP/1.1" 200 -
```

## Requirements

- flask
- kubernetes client libraries

### Testing Locally

- kind
- helm
- cert-manager : https://artifacthub.io/packages/helm/cert-manager/cert-manager

## Usage

- update `docker-compose.yaml` to use your own image registry

```
# Set up test environment
make create-local-test-env

# Rebuild and run restart workloads
make test

```

## TODO

- work in progress...
- add config for enfore / audit
