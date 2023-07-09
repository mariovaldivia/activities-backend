.PHONY: help

help: ## Print this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
build: ## Build a dockerimage
	docker compose build
up: ## Build a dockerimage
	docker compose up
install: ## install dependencies with pip install
	docker run –-rm activities-backend-django_app-1 sh -c 'pip install -r requirements.txt'
shell: ## shell inside docker container
	docker exec -ti activities-backend-django_app-1 sh