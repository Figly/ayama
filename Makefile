POD_NAME := $(eval kb get pod -lapp=ayama -o=jsonpath="{.items[0].metadata.name}")

help:
	@echo "bootstrap - run environment setup installations"
	@echo "up - provision minikube and bring environment up"
	@echo "first - deploy everything from scratch"

bootstrap:
	./scripts/bootstrap.sh

up:
	./scripts/up.sh

db:
	kubectl --context=minikube apply -f services/postgres/kubernetes/dev
	./scripts/postgres.sh dev
	echo "waiting for DB availability"
	sleep 30

app:
	kubectl --context=minikube apply -f kubernetes/once-off/dev
	./scripts/_build.sh dev
	./scripts/deploy.sh dev

staging:
	./scripts/_build.sh staging
	./scripts/deploy.sh staging

collectstatic:
	@eval $$(minikube docker-env) ;\
	$(eval POD_NAME=$(shell sh -c "kubectl get pods | grep ayama-app | grep Running" | awk '{print $$1}'))
	kubectl --context=minikube exec $(POD_NAME) --stdin --tty -- ./manage.py collectstatic


migrate:
	@eval $$(minikube docker-env) ;\
	$(eval POD_NAME=$(shell sh -c "kubectl get pods | grep ayama-app | grep Running" | awk '{print $$1}'))
	kubectl --context=minikube exec $(POD_NAME) --stdin --tty -- ./manage.py migrate

scaleup:
	gcloud container clusters resize carignan --node-pool aragon --num-nodes 1 --zone europe-west1-d

scaledown:
	gcloud container clusters resize carignan --node-pool aragon --num-nodes 0 --zone europe-west1-d
