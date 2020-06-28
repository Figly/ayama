POD_NAME := $(eval kb get pod -lapp=ayama -o=jsonpath="{.items[0].metadata.name}")

help:
	@echo "bootstrap - run environment setup installations"
	@echo "up - provision minikube and bring environment up"
	@echo "first - deploy everything from scratch"

bootstrap:
	./scripts/src/bootstrap.sh

up:
	./scripts/src/up.sh

db:
	kubectl --context=minikube apply -f services/postgres/kubernetes/dev
	./scripts/src/postgres.sh dev
	echo "waiting for DB availability"
	sleep 30

app:
	kubectl --context=minikube apply -f kubernetes/once-off/dev
	./scripts/src/_build.sh dev
	./scripts/src/migrate.sh dev
	./scripts/sr/cdeploy.sh dev

staging:
	./scripts/src/_build.sh staging
	./scripts/src/migrate.sh staging
	./scripts/src/deploy.sh staging
	./scripts/src/collectstatic.sh staging

first:
	$(MAKE) db
	$(MAKE) app

scaleup:
	gcloud container clusters resize carignan --node-pool aragon --num-nodes 1 --zone europe-west1-d

scaledown:
	gcloud container clusters resize carignan --node-pool aragon --num-nodes 0 --zone europe-west1-d
