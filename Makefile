#include .mk/bumpversion.mk

MAKEFLAGS += --warn-undefined-variables --no-print-directory
.SHELLFLAGS := -eu -o pipefail -c

all: help
.PHONY: all

# Use bash for inline if-statements
SHELL:=bash

APP_NAME:=pygame-template
APP_DESCRIPTION:=Ein Template-Projekt für Pygame-basierte Spiele


##@ Hilfe
help: ## Zeige diese Hilfe an
	@echo "$(APP_NAME)"
	@echo "================================================="
	@echo "$(APP_DESCRIPTION)"
	@awk 'BEGIN {FS = ":.*##"; printf "\033[36m\033[0m"} /^[a-zA-Z0-9_%\/-]+:.*?##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@printf "\n"

##@ Codespace
start/%:
start/%: ## Starte eine Codespace-Umgebung für eine App. Gib den Namen des App-Verzeichnissesn mit 'start/<app-name>' an.
	@./start $(notdir $@)

##@ Docker
build: DARGS?=
build: ## Docker Image bauen
	docker compose build $(DARGS)

run/%:
run/%: ## Starte einen Docker Container für eine App. Gib den Namen des App-Verzeichnissesn mit 'run/<app-name>' an.
	APP_DIR=$(notdir $@) docker compose up