# Customer Handover – Traffic Processor (TP)

**Date:** 17 July 2026
**Product Baseline:** Traffic Processor (TP) – a network visibility and control tool that captures live packet counters, per-connection statistics, traffic history, and supports blocking, tunneling, and failover behaviours. This document provides a snapshot of the current product state to support the *future* handover process.

---

## 1. Current Product Status and Handover Scope

The Traffic Processor system is a **fully containerised** network visibility and control solution. It consists of six services orchestrated via Docker Compose:

| Component | Description | Technology |
|-----------|-------------|------------|
| **TProc** | Packet sniffer that captures traffic, classifies packets, computes per-IP statistics, and sends data to CNSS. | Python, Scapy |
| **CNSS** | Control and Status Server – receives statistics, serves the web dashboard, and supports reset functionality. | FastAPI, PostgreSQL |
| **PostgreSQL** | Persistent storage for CNSS data. | PostgreSQL 14.8 |

**Sprint 3 (completed 5 July 2026)** introduced major upgrades:

- PostgreSQL for persistent storage (with Alembic migrations)
- Gate reverse proxy with IP‑based filtering (`BLOCKED_IPS`)
- Dedicated Error Server for 403 responses
- Per‑IP statistics collection and display
- Block traffic based on a blacklist

All documented User Acceptance Tests (UATs) for Sprint 2 and Sprint 3 have passed.

**Handover status:** Formal handover to the customer has **not yet been initiated** (see Section 8 for details).

---

## 2. How the Customer Accesses and Uses the Product

### 2.1 Access Methods

| Access Point | URL / Endpoint | Purpose |
|--------------|----------------|---------|
| **Web Dashboard** | `http://<host-ip>:8080/static/index.html` | View live traffic statistics (packets, bytes, rates, protocol breakdowns, per‑IP stats) |
| **CNSS API** | `POST /load`, `GET /packets`, `POST /reset` | Programmatic access to statistics and control |

### 2.2 Usage Workflow

1. **Deploy** the system using Docker Compose (see Section 3).
2. **Monitor** network traffic via the web dashboard at `http://localhost:8080/static/index.html`.
3. **Block** unwanted IPs by adding them to the `BLOCKED_IPS` environment variable (see Section 4).
4. **Query** statistics programmatically via the CNSS API endpoints.
5. **Reset** statistics using the `POST /reset` endpoint if needed.

---

## 3. Installation / Deployment Instructions

### 3.1 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on the target system.
- Ports **38080** (CNSS web dashboard).

### 3.2 Deployment Steps

```bash
# 1. Clone the repository
git clone https://github.com/SWP-Team-46/Traffic-Proccessor.git
cd Traffic-Proccessor/src

# 2. (Optional) Configure environment variables – see Section 4 below

# 3. Start all services
docker compose up --build -d

# 4. Verify all containers are running
docker ps

# 6. Verify CNSS web server is responding
curl http://localhost:38080/root

# 8. Open the web dashboard in a browser
# http://localhost:38080/static/index.html
```

### 3.3 Stopping the System

```bash
docker compose down
```

## 4. Required Configuration and Secrets‑Handling Expectations

### 4.1 Environment Variables

The following environment variables can be configured via a `.env` file in the `src` directory or by setting them directly in `docker-compose.yml`:

| Variable | Purpose | Example |
|----------|---------|---------|
| `DEV_MODE` | Enables development‑mode responses (e.g., `/root` endpoint returns `{"message": "DEV_MODE is true"}`) | `true` or `false` |
| PostgreSQL credentials | Set via `docker-compose.yml` environment section for the `postgres` service | (defaults are set internally) |

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

### 5.3 Monitoring

- Use `docker stats` to monitor container resource usage.
- Check container logs: `docker logs <container-name>` (e.g., `docker logs tproc`).

### 5.4 Backup

- Backup the PostgreSQL volume regularly if historical statistics are critical.
- The volume location can be inspected via `docker volume ls` and `docker volume inspect`.

---

## 6. Troubleshooting and Support Guidance

### 6.1 Common Issues and Resolutions

| Issue | Likely Cause | Resolution |
|-------|--------------|------------|
| Dashboard not loading | CNSS container not running or port 38080 unavailable | Check `docker ps`; ensure port 38080 is free; view logs: `docker logs cnss` |
| No traffic data appearing | TProc not capturing or network interface misconfigured | Verify TProc is running; check logs: `docker logs tproc` |
| PostgreSQL connection errors | Database not initialised or credentials mismatch | Check PostgreSQL logs: `docker logs postgres`; ensure migrations have run |
| Permission errors (TProc) | Missing `CAP_NET_RAW` or Scapy cannot access network interface | Run with elevated privileges or adjust Docker capabilities in `docker-compose.yml` |

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
 <!--Add smth there-->

### 7.3 Important Risks

- **Privacy / GDPR:** The tool captures live network traffic and per‑connection data. Ensure appropriate consent and data protection measures are in place before deploying in environments with personal or sensitive data.
- **Security:** Exposing the dashboard or API to the public internet without authentication is a security risk. Use in LAN environments.
- **Container Security:** Regularly update base images and apply security patches.

---

## 8. Handover Status

> **Current Handover Level:** Blocked
>
> Formal customer handover is **Blocked**. The product is currently in active development, with the team focusing on completing the planned feature set and hardening the system for production use.

The product is functionally complete for the features delivered in Sprint 3 (as of 5 July 2026), and all documented UATs have passed. However, handover activities (such as formal acceptance testing, customer documentation walkthroughs, or production deployment planning) have not yet commenced.

**Prerequisites and blockers that must be resolved before handover can be initiated:**

| Action | Status | Blocking? |
|--------|--------|-----------|
| Security hardening (authentication for dashboard/API, TLS) | Not addressed | No - optional |
| Formal customer acceptance criteria / sign‑off process | Not defined | Yes – must be established with the customer |
| Final documentation review and walkthrough | Pending | Yes – required before handover |

**To initiate and complete a full handover (customer‑deployed/operated), the following steps are required:**

1. Complete all planned sprints and remaining backlog items.
2. Set up production monitoring, logging, and alerting in collaboration with the customer's operations team.
3. Conduct a formal handover meeting and walk the customer through deployment, configuration, and troubleshooting.
4. Complete formal UAT sign‑off by the customer.

Until these actions are completed, the product remains under active development and is not yet ready for independent customer use or production deployment.

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
