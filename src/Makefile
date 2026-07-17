# ============================================================
# Traffic Processor Deployment Makefile
#
# For backend
#   make backend
#
# For TP
#   make attach TARGET=<container-name>
#
# Optional:
#   make attach TARGET=my-service \
#        CNSS_URL=http://10.0.0.5:38080/load
#
#   make attach TARGET=my-service \
#        INTERFACE=docker0
# ============================================================

IMAGE := ghcr.io/swp-team-46/traffic-processor:latest
COMPOSE := docker compose

TARGET ?=
CNSS_URL ?= http://host.docker.internal:38080/load
INTERFACE ?= eth0

.DEFAULT_GOAL := help

.PHONY: help backend attach stop logs pull

help:
	@echo ""
	@echo Traffic Processor
	@echo "Targets:"
	@echo "  make backend                     Start backend services"
	@echo "  make pull                        Pulls TP image"
	@echo "  make attach TARGET=<container>   Attach TP to container"
	@echo "  make detach                      Remove TP"
	@echo "  make logs                        Backend logs"
	@echo "  make stop                        Stop backend"
	@echo "
	@echo "Variables:"
	@echo "  TARGET      Container to monitor (required)"
	@echo "  CNSS_URL    $(CNSS_URL)"
	@echo "  INTERFACE   $(INTERFACE)"
	@echo Note: If you want to run TP on the external machine, copy Makefile from the repository to the target system and run: 
	@echo " make attach TARGET=<container> \ CNSS_URL=http://<backend-IP>:38080/load "
	@echo ""

backend:
	$(COMPOSE) up -d

pull:
	docker pull $(IMAGE)

logs:
	$(COMPOSE) logs -f

stop:
	$(COMPOSE) down

detach:
	-docker stop traffic-processor

attach:
ifndef TARGET
	$(error TARGET is required. Example: make attach TARGET=my-service)
endif
	@echo "Searching for running container '$(TARGET)'..."
	@MATCHES=$$(docker ps --filter "name=$(TARGET)" --format "{{.ID}} {{.Names}}"); \
	COUNT=$$(printf "%s\n" "$$MATCHES" | grep -c .); \
	if [ $$COUNT -eq 0 ]; then \
		echo ""; \
		echo "ERROR: No running container matches '$(TARGET)'."; \
		exit 1; \
	fi; \
	if [ $$COUNT -gt 1 ]; then \
		echo ""; \
		echo "ERROR: Multiple running containers match '$(TARGET)':"; \
		echo ""; \
		printf "%s\n" "$$MATCHES" | awk '{print "   - " $$2}'; \
		echo ""; \
		echo "Please specify a more specific container name."; \
		exit 1; \
	fi; \
	CID=$$(printf "%s\n" "$$MATCHES" | awk '{print $$1}'); \
	NAME=$$(printf "%s\n" "$$MATCHES" | awk '{print $$2}'); \
	echo ""; \
	echo "Container : $$NAME"; \
	echo "CNSS      : $(CNSS_URL)"; \
	echo "Interface : $(INTERFACE)"; \
	echo "Image      : $(IMAGE)"; \
	echo ""; \
	echo "Starting Traffic Processor..."; \
	docker run \
    	--name traffic-processor \
    	--pull=always \
    	--rm \
		--network container:$$CID \
		--cap-add=NET_ADMIN \
		--cap-add=NET_RAW \
		-e CNSS_URL="$(CNSS_URL)" \
		-e INTERFACE="$(INTERFACE)" \
		-e TARGET_HOSTNAME="$$NAME" \
		$(IMAGE)
