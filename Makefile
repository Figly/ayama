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
