# Customer Handover – Traffic Processor (TP)

**Date:** 17 July 2026
**Product Baseline:** Traffic Processor (TP) – a network visibility and control tool that captures live packet counters, per-connection statistics, traffic history, and supports blocking, tunneling, and failover behaviours. This document provides a snapshot of the current product state to support the *future* handover process.

---

## 1. Current Product Status and Handover Scope

The Traffic Processor system is a **containerised** network visibility and control solution designed to monitor the network activity of existing Docker containers. The product consists of the following components:

| Component | Description | Technology |
|-----------|-------------|------------|
| **Traffic Processor (TP)** | Captures live network traffic from a target container, computes traffic statistics, and forwards them to CNSS. | Python, Scapy |
| **CNSS** | Control and Status Server – receives statistics from TP, stores historical data, and serves the web dashboard and API. | FastAPI |
| **PostgreSQL** | Persistent storage for CNSS statistics and historical data. | PostgreSQL 14 |

The backend services (CNSS and PostgreSQL) are deployed using Docker Compose, while the Traffic Processor runs as a separate container attached to the network namespace of the container being monitored. This allows the monitored application to remain unchanged while traffic is captured independently.

The product has completed its planned feature implementation and provides:

- Live packet and bandwidth statistics
- Per-IP traffic statistics
- Historical traffic storage
- Web dashboard for monitoring
- REST API for programmatic access
- Remote deployment where backend and monitored containers may run on different hosts

**Handover status:** The product is **Ready for independent use**. The customer has received deployment instructions, source code, and supporting documentation required for independent.

---

## 2. How the Customer Accesses and Uses the Product

### 2.1 Access Methods

| Access Point | URL / Endpoint | Purpose |
|--------------|----------------|---------|
| **Web Dashboard** | `http://<host-ip>:8080/static/index.html` | View live traffic statistics (packets, bytes, rates, protocol breakdowns, per‑IP stats) |
| **CNSS API** | `POST /load`, `GET /packets`, `POST /reset` | Programmatic access to statistics and control |

### 2.2 Usage Workflow

1. Deploy the backend services using the provided deployment commands.
2. Pull the latest Traffic Processor container image.
3. Attach the Traffic Processor to the Docker container that should be monitored.
4. Open the web dashboard at `http://<backend-ip>:38080/static/index.html`.
5. Monitor live and historical traffic statistics.
6. Stop or reattach the Traffic Processor whenever monitoring another container is required.

---

## 3. Installation / Deployment Instructions

### 3.1 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on the target system.
- Ports **38080** (CNSS web dashboard).

### 3.2 Deployment Steps

Backend host:

```bash
# Clone the repository
git clone https://github.com/SWP-Team-46/Traffic-Proccessor.git
cd Traffic-Proccessor/src

# Start backend services
make backend
```

Target host (host running the container to monitor):

```bash
# Attach Traffic Processor to the target container
make attach TARGET=<container-name> \
CNSS_URL=http://<backend-ip>:38080/load
```

Verify deployment:

```bash
docker ps
curl http://<backend-ip>:38080/root
```

Open the dashboard:

```
http://<backend-ip>:38080/static/index.html
```

### 3.3 Stopping the System

Stop the Traffic Processor:

```bash
make detach
```

Stop backend services:

```bash
make stop
```

## 4. Required Configuration and Secrets‑Handling Expectations

### 4.1 Environment Variables

The following variables may be configured before deployment.

| Variable | Purpose | Example |
|----------|---------|---------|
| `TARGET` | Docker container that will be monitored | `nginx` |
| `CNSS_URL` | URL of the CNSS `/load` endpoint | `http://192.168.1.10:38080/load` |
| `INTERFACE` | Network interface used for packet capture | `eth0` |

### 4.2 Secrets‑Handling Expectations

- **Never commit secrets** to the repository. Credentials, tokens, or private keys must never appear in version control.
- Use `.env` files for local development - they are listed in `.gitignore` and are not pushed.
- For production, use Docker secrets or a secure vault to manage sensitive variables.
- The system does not currently require API keys or external service credentials for core functionality.

---

## 5. Operational Notes for Normal Use

### 5.1 Data Persistence

- Statistics are stored in **PostgreSQL**.
- The PostgreSQL container uses a persistent volume; data survives container restarts unless the volume is explicitly removed.

### 5.2 Performance Considerations

- TProc uses **Scapy** for packet capture – this may require elevated privileges (`CAP_NET_RAW`) in production environments.
- The system is designed for **moderate** network loads; for high‑throughput environments, consider scaling resources (CPU/memory) allocated to containers.
- The Makefile utilite is set to work in bash and wouldn't work in Powershell. On Windows, consider running commands through git-bash.

### 5.3 Monitoring

- Use `docker stats` to monitor container resource usage.
- Check container logs: `docker logs <container-name>` (e.g., `docker logs tproc`).

### 5.4 Backup

- Backup the PostgreSQL volume regularly if historical statistics are critical.
- The volume location can be inspected via `docker volume ls` and `docker volume inspect`.

### 5.5 Deployment Notes

- The Traffic Processor runs independently from the backend services.
- The backend and monitored container may be deployed on different hosts provided the Traffic Processor can reach the configured CNSS endpoint.
- The Traffic Processor shares the network namespace of the monitored container and therefore requires Docker networking capabilities (`NET_ADMIN` and `NET_RAW`).
- Reattaching the Traffic Processor to another container requires stopping the current attachment before starting a new one.

---

## 6. Troubleshooting and Support Guidance

### 6.1 Common Issues and Resolutions

| Issue | Likely Cause | Resolution |
|-------|--------------|------------|
| Dashboard not loading | CNSS container not running or port 38080 unavailable | Check `docker ps`; ensure port 38080 is free; view logs: `docker logs cnss` |
| No traffic data appearing | TProc not capturing or network interface misconfigured | Verify TProc is running; check logs: `docker logs tproc` |
| PostgreSQL connection errors | Database not initialised or credentials mismatch | Check PostgreSQL logs: `docker logs postgres`; ensure migrations have run |
| Permission errors (TProc) | Missing `CAP_NET_RAW` or Scapy cannot access network interface | Run with elevated privileges or adjust Docker capabilities in `docker-compose.yml` |
| Target container not found | Incorrect container name | Confirm the container is running and use the exact Docker container name |
| Multiple matching containers | Container name is ambiguous | Specify a more specific container name |

### 6.2 Getting Support

- **Internal team support:** Contact the development team.
- **Issue reporting:** Open a GitHub Issue at [https://github.com/SWP-Team-46/Traffic-Proccessor/issues](https://github.com/SWP-Team-46/Traffic-Proccessor/issues).
- **Documentation:** Refer to the maintained docs in the repository (see Section 9).

---

## 7. Known Limitations, Unfinished Areas, and Important Risks

### 7.1 Known Limitations

| Area | Limitation | Impact |
|------|------------|--------|
| **Scalability** | Designed for moderate network loads; not tested at enterprise scale | May not handle high‑throughput production environments without tuning |
| **IPv6** | Not explicitly tested; Scapy supports IPv6 but filtering and statistics may not fully account for IPv6 traffic | IPv6 traffic may be partially captured but not fully classified |
| **Authentication** | No user authentication on the web dashboard or API | Dashboard and API are publicly accessible if exposed; should be deployed behind a VPN or reverse proxy with authentication in production |
| **High Availability** | No built‑in clustering or failover | Single point of failure; not suitable for mission‑critical deployments without additional orchestration |

### 7.2 Unfinished Areas
Feature, which will allow to distinguish different TPs connected to one CNSS by their ID in database, so the frontend could sort displayed data by concrete module, is not yet implemented.

### 7.3 Important Risks

- **Privacy / GDPR:** The tool captures live network traffic and per‑connection data. Ensure appropriate consent and data protection measures are in place before deploying in environments with personal or sensitive data.
- **Security:** Exposing the dashboard or API to the public internet without authentication is a security risk. Use in LAN environments.
- **Container Security:** Regularly update base images and apply security patches.

---

## 8. Handover Status

> **Current Handover Level:** Ready for independent use
>
> The product is considered **Ready for independent use**. The vast majority of planned functionality has been implemented, documented, and made available to the customer together with deployment instructions and source code.

The customer is able to deploy, configure, operate, and troubleshoot the system independently using the provided documentation.

The product has not yet progressed to stronger handover levels because the repository and deployment workflow were delivered only at the end of the last implementation sprint. As a result, the customer has not yet had sufficient operational time to independently use the product and provide long-term operational feedback.

**Remaining actions:**

| Action | Status | Blocking? |
|--------|--------|-----------|
| Customer operational evaluation over an extended period | Pending | No |
| Customer feedback and improvement requests | Ongoing | No |
| Long-term production experience | Pending | No |

The remaining activities are part of the normal post-handover adoption process and **do not prevent independent customer use**. There are currently no outstanding development-side blockers preventing transition of ownership or day-to-day operation.

---

## 9. Links to Related Customer‑Relevant Documentation

| Document | Description |
|----------|-------------|
| [README.md](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/main/README.md) | Project overview and quick start |
| [docs/architecture/](https://github.com/SWP-Team-46/Traffic-Proccessor/tree/main/docs/architecture) | System architecture (static, dynamic, deployment views) |
| [docs/user-acceptance-tests.md](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/main/docs/user-acceptance-tests.md) | End‑user acceptance test scenarios |
| [docs/development-process.md](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/main/docs/development-process.md) | Development workflow (for reference) |
| [docs/roadmap.md](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/main/docs/roadmap.md) | Project roadmap and upcoming milestones |
| [docs/quality-requirements.md](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/main/docs/quality-requirements.md) | Quality standards and non‑functional requirements |
| [CHANGELOG.md](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/main/CHANGELOG.md) | Release notes and version history |

---

*This document is maintained alongside the repository and updated whenever customer‑facing instructions, deployment steps, limitations, or handover status change.*
