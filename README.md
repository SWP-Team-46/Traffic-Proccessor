# Traffic Processor
[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](CHANGELOG.md)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/github/license/SWP-Team-46/Traffic-Proccessor)](LICENSE)

**Traffic Processor** is a network visibility and control tool that captures live packet counters, per‑connection statistics, and traffic history, while supporting blocking, tunneling, and failover behaviours.

---

## Access the Product

The easiest way to try the current version is to run the fully containerised stack:

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on the target system.
- Ports **38080** (CNSS web dashboard).

### Deployment Steps

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

### Stopping the System

Stop the Traffic Processor:

```bash
make detach
```

Stop backend services:

```bash
make stop
```

## Documentation

All maintained documentation lives in the [`docs/`](docs) folder:

| Document | Purpose |
|----------|---------|
| **[Architecture Overview](docs/architecture)** | System components, static/dynamic/deployment views, and key architectural decisions (ADRs) |
| **[Testing & Quality](docs/testing.md)** | Test strategy, coverage expectations, and quality automation |
| **[Roadmap](docs/roadmap.md)** | Planned features and future direction |
| **[User Acceptance Tests](docs/user-acceptance-tests.md)** | UAT scenarios and sign‑off criteria |

---

## Handover Guidance

For the current product state, handover scope, and customer‑facing instructions, see the **[Customer Handover document](docs/customer-handover.md)**.

---

## Contributing & Agent Workflow

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Practical steps for setting up, branching, opening PRs, and meeting review requirements.
- **[AGENTS.md](AGENTS.md)** - Actionable setup, build, test, and safety instructions for coding agents.

---

## Repository Structure

.\
├── src/               # Application source code (TProc, CNSS, Gate, Error Server)\
├── docs/              # Maintained documentation (architecture, testing, handover, etc.)\
├── reports/           # Project reports and status updates\
├── .github/           # CI workflows and issue/PR templates\
├── AGENTS.md          # Agent‑focused setup and workflow guide\
├── CONTRIBUTING.md    # Contribution process and review expectations\
├── CHANGELOG.md       # Version history\
└── LICENSE            # Project license

---

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.

---

*For any questions or handover‑related inquiries, please refer to the [Customer Handover document](docs/customer-handover.md) or open an issue in this repository.*
