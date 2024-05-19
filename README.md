# k8s-webhook-python

Exploring kubernetes webhooks with python.

## Notes

Webhooks are in an audit mode and will not enforce any validations.

`response["response"]["allowed"] = True`

```
k8s-webhook 2024-05-19 14:40:52,396: INFO - AdmissionReview - admission.k8s.io/v1 | kind: ReplicaSet - operation: CREATE - namespace: test - name: test-000-648f879c8c
k8s-webhook 2024-05-19 14:40:52,396: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': '92d86b88-3c00-458d-b370-3c0ada71cee9', 'status': {'message': 'test-000-648f879c8c : 1 - Less then or equal to 2'}}}
k8s-webhook 2024-05-19 14:40:52,398: INFO - 172.19.0.3 - - [19/May/2024 14:40:52] "POST /validate-replicas?timeout=10s HTTP/1.1" 200 -

k8s-webhook 2024-05-19 14:40:52,422: INFO - AdmissionReview - admission.k8s.io/v1 | kind: Pod - operation: CREATE - namespace: test - name: test-000-648f879c8c-fffwh
k8s-webhook 2024-05-19 14:40:52,422: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': '8166f3a7-aa5d-4902-893f-dafd93903272', 'status': {'message': 'TOTAL CPU: 0.100 | TOTAL MEM:  524288000 B, 500.0 MB'}}}
k8s-webhook 2024-05-19 14:40:52,423: INFO - 172.19.0.3 - - [19/May/2024 14:40:52] "POST /validate-resources?timeout=10s HTTP/1.1" 200 -

k8s-webhook 2024-05-19 14:40:52,503: INFO - AdmissionReview - admission.k8s.io/v1 | kind: Pod - operation: CREATE - namespace: test - name: test-001-7bdb95bfd4-mdrfn
k8s-webhook 2024-05-19 14:40:52,504: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': '7483f7e1-ab47-44e5-bde5-fe92a921b2ff', 'status': {'message': 'TOTAL CPU: 0.400 | TOTAL MEM:  2149580800 B, 2.0 GB'}}}
k8s-webhook 2024-05-19 14:40:52,505: INFO - 172.19.0.3 - - [19/May/2024 14:40:52] "POST /validate-resources?timeout=10s HTTP/1.1" 200 -

k8s-webhook 2024-05-19 14:40:52,692: INFO - AdmissionReview - admission.k8s.io/v1 | kind: ServiceAccount - operation: CREATE - namespace: test - name: testsa-00
k8s-webhook 2024-05-19 14:40:52,692: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': 'a3baaa18-0ff6-461e-9ca9-6c9dadfec9d8', 'status': {'message': 'No annotations found'}}}
k8s-webhook 2024-05-19 14:40:52,693: INFO - 172.19.0.3 - - [19/May/2024 14:40:52] "POST /validate-service-accounts?timeout=10s HTTP/1.1" 200 -

k8s-webhook 2024-05-19 14:40:53,583: INFO - AdmissionReview - admission.k8s.io/v1 | kind: ReplicaSet - operation: UPDATE - namespace: test - name: test-000-874c78b6f
k8s-webhook 2024-05-19 14:40:53,583: INFO - {'apiVersion': 'admission.k8s.io/v1', 'kind': 'AdmissionReview', 'response': {'allowed': True, 'uid': 'fc00095b-1250-4a6c-892c-1772ac67dba1', 'status': {'message': 'test-000-874c78b6f : 0 - Less then or equal to 2'}}}
k8s-webhook 2024-05-19 14:40:53,583: INFO - 172.19.0.3 - - [19/May/2024 14:40:53] "POST /validate-replicas?timeout=10s HTTP/1.1" 200 -
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
