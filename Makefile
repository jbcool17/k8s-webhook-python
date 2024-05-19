LOCAL_TEST_ENV = "tests"

# LOCAL TEST ENV
create-local-test-env: create-kind cert-manager docker-build-push deploy-webhook test-deployment

delete-local-test-env:
	kind delete clusters k8s-webhook

create-kind:
	kind get clusters | grep "k8s-webhook" || kind create cluster --config $(LOCAL_TEST_ENV)/kind-config.yaml

cert-manager:
	helm upgrade --install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.9.1 --set installCRDs=true

deploy-webhook:
	kubectl apply -f $(LOCAL_TEST_ENV)/webhook-configs && kubectl apply -f $(LOCAL_TEST_ENV)/deployment

deploy-webhook-pcln:
	kubectl apply -f $(LOCAL_TEST_ENV)/webhook-configs && kubectl apply -f $(LOCAL_TEST_ENV)/deployment-pcln

test-deployment:
	kubectl apply -f $(LOCAL_TEST_ENV)/test-deployment.yaml

# TEST
# Build and restart
test: docker-build-push restart-webhook restart-test-deploy

restart-webhook:
	sleep 2 && kubectl rollout restart -n k8s-webhook deployment k8s-webhook

restart-test-deploy:
	sleep 10 \
		&& kubectl rollout restart -n test deployment test-000 \
		&& kubectl rollout restart -n test deployment test-001

# BUILD
docker-build-push:
	export DOCKER_DEFAULT_PLATFORM=linux/amd64 && docker-compose build && docker-compose push
