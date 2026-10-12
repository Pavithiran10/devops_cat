# COIMBATORE INSTITUTE OF TECHNOLOGY
*(Government Aided Autonomous Institution Affiliated to Anna University)*  
**COIMBATORE – 641 014**

---

## 23IT723 – DEVOPS LABORATORY
### FINAL PROJECT REPORT

# FITTRACK – FITNESS TRACKER WEB APPLICATION WITH DEVOPS AUTOMATION

**OCTOBER 2026**

**Submitted by:**  
**PAVITHIRAN R**  
**Register No:** 2303717620522026  
**Department of Information Technology**  
**Coimbatore Institute of Technology**

---

## BONAFIDE CERTIFICATE

Certified that this project report titled **“FITTRACK – FITNESS TRACKER WEB APPLICATION WITH DEVOPS AUTOMATION”** is the bonafide work of **PAVITHIRAN R (Register No: 2303717620522026)** completed during the academic year 2025–2026 – Semester VII for the project presentation and laboratory evaluation of **23IT723 – DEVOPS LABORATORY** under our supervision.

Certified that the candidate was examined during the laboratory practical examination conducted on _________________.

**Review Members / Faculty Examiners:**
1. **Dr. M. SANGEETHA**, Associate Professor, Department of Information Technology
2. **Dr. E. ARUL**, Associate Professor, Department of Information Technology

---

## 23IT723 – DEVOPS LABORATORY: FINAL MINI PROJECT EVALUATION SCHEME

| S.No. | Evaluation Component | Key Verification Points | Marks |
|:---:|:---|:---|:---:|
| 1 | **Problem Definition & Project Planning** | Problem statement, objectives, requirements, module identification, technology selection, and workflow planning. | 10 |
| 2 | **Git Repository & Version Control** | Repository creation, meaningful commits, README, `.gitignore`, remote repository, push/pull/fetch operations, and commit history. | 15 |
| 3 | **Branching, Merging & Collaboration** | Feature branches, parallel development, merging, conflict handling, branch organization, and collaborative workflow. | 10 |
| 4 | **Application Development & Build** | Working full-stack application, project structure, dependency management, build configuration, and error-free execution. | 15 |
| 5 | **Jenkins Continuous Integration** | Jenkins pipeline configuration, SCM checkout, automated triggers (webhook/polling), build stages, and console logs. | 15 |
| 6 | **Docker Containerization** | Hardened Dockerfile, non-root user, multi-stage image, container execution, port mapping, and health check validation. | 10 |
| 7 | **Automation / Configuration Management** | Ansible playbook execution, idempotent container lifecycle management, volume mounting, and automated health checks. | 5 |
| 8 | **Testing & Verification** | 25 Pytest unit/integration test cases, boundary validation, test reporting, error identification, and corrective actions. | 5 |
| 9 | **Documentation & Presentation** | Architecture/workflow diagram, step-by-step commands, screenshots, troubleshooting guide, and conclusion. | 5 |
| 10 | **Final Demonstration & Viva-Voce** | Live demonstration, explanation of implementation, troubleshooting responses, and deep technical understanding. | 10 |
| **TOTAL** | **Comprehensive DevOps Evaluation** | **10 Core DevOps Competencies Integrated** | **100** |

---

## TABLE OF CONTENTS

| S.No. | Content | Page No. |
|:---:|:---|:---:|
| 1 | INTRODUCTION | 05 |
| 2 | OBJECTIVES | 05 |
| 3 | ABSTRACT | 06 |
| 4 | TECHNOLOGY STACK | 06 |
| 5 | SYSTEM ARCHITECTURE & CI/CD WORKFLOW | 07 |
| 6 | MODULE 1 — USER INTERFACE & WORKOUT LOGGING | 08 |
| 7 | MODULE 2 — FLASK RESTFUL BACKEND & API SERVICES | 09 |
| 8 | MODULE 3 — SQLITE DATABASE MANAGEMENT & SCHEMA | 10 |
| 9 | MODULE 4 — GIT & GITHUB SOURCE CONTROL | 11 |
| 10 | MODULE 5 — DOCKER CONTAINERIZATION & HARDENING | 12 |
| 11 | MODULE 6 — JENKINS CI/CD AUTOMATION PIPELINE | 14 |
| 12 | MODULE 7 — AUTOMATED TESTING (PYTEST SUITE) | 15 |
| 13 | MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION | 17 |
| 14 | MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME) | 18 |
| 15 | MODULE 10 — ANALYTICS ENGINE & GOAL MANAGEMENT | 19 |
| 16 | MODULE 11 — COMPLETE CI/CD INTEGRATION | 20 |
| 17 | MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION | 21 |
| 18 | RESULTS AND OUTPUT | 23 |
| 19 | COMMANDS USED (COMPREHENSIVE RUNBOOK) | 24 |
| 20 | ADVANTAGES | 28 |
| 21 | LIMITATIONS | 28 |
| 22 | FUTURE ENHANCEMENTS | 29 |
| 23 | CONCLUSION | 29 |

---

## 1. INTRODUCTION

**FitTrack** is a modern, responsive, full-stack fitness and wellness tracking web application coupled with end-to-end DevOps automation. In contemporary physical conditioning routines, individuals struggle to consistently record multi-discipline workouts (Running, Walking, Cycling, Strength Training, and Yoga), monitor daily metabolic expenditure, track hydration levels, and assess longitudinal health progress against predefined goals. Manual physical logs and disconnected spreadsheets lack instant caloric calculations, interactive KPI visualisations, and automated metric auditing.

To resolve these operational challenges, FitTrack couples a robust single-page application (HTML5, CSS3, ES6+ JavaScript, Chart.js) and a lightweight Python Flask REST backend with SQLite persistence. Beyond application logic, the project embodies modern software engineering by fully automating the software delivery lifecycle using DevOps industry best practices. Git and GitHub govern version control; Jenkins orchestrates a 10-stage Continuous Integration and Continuous Deployment (CI/CD) pipeline; Pytest executes 25 automated unit and regression tests; Docker containerizes the application into a hardened, non-root microservice; and Ansible provides idempotent configuration management and deployment. Persistent Docker Volumes ensure zero data loss during container upgrades.

---

## 2. OBJECTIVES

1. **Interactive Fitness Management**: Enable users to log, filter, edit, and audit multi-type workouts with real-time calorie and distance calculations.
2. **Visual KPI Analytics**: Provide an intuitive dashboard with daily step goal completion rings, 7-day caloric expenditure charts, and active-minute gauges.
3. **Version Control & Collaboration**: Implement Git source control on GitHub with structured branching, semantic commit conventions, and issue tracking.
4. **Continuous Integration Automation**: Automate code compilation, linting, and 25 Pytest validation tests using a declarative 10-stage Jenkins pipeline.
5. **Microservice Containerization**: Package the application into an optimized, multi-stage Python 3.11-slim Docker container operating under a non-root system user.
6. **Automated Deployment with Ansible**: Author an idempotent Ansible playbook to verify host Docker engines, prune legacy instances, bind volume mounts, and probe container health.
7. **Stateful Data Persistence**: Utilize dedicated Docker named volumes (`fittrack_sqlite_data`) mounted to `/app/data` to preserve SQLite database state across container updates.

---

## 3. ABSTRACT

FitTrack demonstrates the complete convergence of a full-stack web application with automated DevOps continuous delivery practices. The core application provides logging and analytics for daily physical activities, hydration, and goal setting, backed by a Flask API and SQLite database. Addressing the risks of manual deployment, human configuration errors, and inconsistent execution environments, this project establishes a resilient pipeline: **GitHub → Jenkins → Pytest → Docker Build → Ephemeral Health Check → Ansible Deployment → Production Docker Container**.

Every code push triggers automated compilation, regression testing across 25 assertions, and container image construction. Ephemeral testing validates endpoint health on port 5055 before release. Ansible guarantees repeatable, idempotent rollouts on target hosts, binding persistent Docker volumes to maintain uninterrupted fitness logs. The project proves that modern DevOps automation substantially accelerates delivery velocity while guaranteeing high application availability and data integrity.

---

## 4. TECHNOLOGY STACK

| Technology | Version / Tool | Role in DevOps Architecture |
|---|---|---|
| **HTML5 & CSS3** | Modern Web Standards | Semantic responsive structure, CSS variables, dark mode styling. |
| **JavaScript** | ES6+ Standards | Asynchronous Fetch API, DOM manipulation, Chart.js visual data rendering. |
| **Python** | 3.11 / 3.13 | Core programming language for backend RESTful services and test execution. |
| **Flask** | 3.0.0 | WSGI lightweight web framework, blueprint routing, application factory pattern. |
| **SQLite** | 3.x | Embedded relational database engine with foreign key constraints and ACID compliance. |
| **Gunicorn** | 21.2.0 | Production-grade WSGI HTTP server with multi-worker concurrency and signal handling. |
| **Git** | 2.51.0 | Distributed version control system tracking commit histories and branching. |
| **GitHub** | Cloud Repository | Centralized remote Git host, branch protection, and webhook integration (`Pavithiran10/devops_cat`). |
| **Jenkins** | 2.568.1 | Continuous Integration server orchestrating automated pipeline execution. |
| **Docker** | 29.1.3 | Containerization platform packaging runtime, dependencies, and OS layers. |
| **Pytest** | 8.3.5 | Automated testing framework executing 25 unit, integration, and validation tests. |
| **Ansible** | Core 2.10+ | Agentless configuration management engine deploying containers idempotently. |

---

## 5. SYSTEM ARCHITECTURE & CI/CD WORKFLOW

```
Developer Workspace (Local PC)
         │  git push origin main
         ▼
GitHub Remote Repository (Pavithiran10/devops_cat)
         │  Webhook / SCM Polling (2-min interval)
         ▼
Jenkins CI/CD Pipeline (localhost:8081)
 ├── 1. SCM Checkout
 ├── 2. Python Environment Setup
 ├── 3. Dependency Installation (pip)
 ├── 4. Pytest Automated Test Suite (25 Tests Passing)
 ├── 5. Bytecode Compilation Checks
 ├── 6. Docker Image Build (fittrack:latest)
 ├── 7. Ephemeral Container Health Probe (Port 5055)
 ├── 8. Image Tagging
 └── 9. Ansible Deployment Automation
         │
         ▼
Ansible Playbook Execution (ansible/playbook.yml)
 ├── Ensure Persistent Volume & Permissions (/app/data)
 ├── Stop and Prune Stale Containers
 └── Run Production Container (Port 5000:5000)
         │
         ▼
Production Docker Container (fittrack-app)
 ├── Gunicorn WSGI Server (3 Workers)
 ├── Flask Application Engine
 └── SQLite Persistent Database (/app/data/fittrack.db)
```

---

## 6. MODULE 1 — USER INTERFACE & WORKOUT LOGGING
- **Single Page Application (SPA)**: Ultra-fast rendering without page reloads using Vanilla CSS and modern DOM manipulation.
- **Workout Entry Modal**: Allows users to log discipline (Running, Walking, Cycling, Strength Training, Yoga), duration, calories burned, distance, and custom notes.
- **Dynamic KPI Rings**: Circular progress gauges displaying today's progress toward daily step goals and water intake targets.
- **Filtering & Search**: Instant client-side and server-side filtering of workout history with multi-column sorting.
- **Chart.js Analytics**: 7-day caloric expenditure bar graphs and interactive activity progress charts.

---

## 7. MODULE 2 — FLASK RESTFUL BACKEND & API SERVICES
- **Application Factory Pattern (`create_app`)**: Isolates configuration modes (development, testing, production) and manages database teardown hooks.
- **Modular Blueprints**:
  - `workouts_bp` (`/api/workouts`): Full CRUD operations with HTTP status codes (200, 201, 400, 404).
  - `activity_bp` (`/api/activity`): Daily metrics upserting and retrieval.
  - `goals_bp` (`/api/goals`): Fitness targets persistence.
  - `dashboard_bp` (`/api/dashboard`): Real-time KPI math aggregations.
- **Container Health Check Endpoint (`/api/health`)**: Returns `{"status":"healthy","database":"connected","version":"1.0.0"}` for automated probes.

---

## 8. MODULE 3 — SQLITE DATABASE MANAGEMENT & SCHEMA
- **Schema (`database/schema.sql`)**:
  - `workouts`: Tracks individual sessions, duration, distance, calories, and timestamps.
  - `daily_activity`: Tracks daily step count, active minutes, and water intake with date unique constraints.
  - `goals`: User target values.
- **Thread Safety & Transactions**: Managed via Flask context teardown (`g.db`), parameterized queries against SQL injection, and automatic rollbacks on exceptions.
- **Automated Seeding**: Idempotent table initialisation and sample record population on application startup.

---

## 9. MODULE 4 — GIT & GITHUB SOURCE CONTROL
- **Repository**: Hosted at `https://github.com/Pavithiran10/devops_cat.git`.
- **Default Branch**: `main`.
- **Ignore Rules (`.gitignore`)**: Strictly filters virtual environments (`.jenkins_venv`, `venv`), SQLite runtime files, and Python cache directories.
- **Semantic Commits**: Clean commit history documenting development, testing configuration (`pytest.ini`), and Jenkins cross-platform pipeline scripts.

---

## 10. MODULE 5 — DOCKER CONTAINERIZATION & HARDENING
- **Slim Base Image**: Built using `python:3.11-slim` to reduce image attack surface and decrease deployment footprint.
- **Non-Root System User**: Dedicated user `fittrack` (UID 1001) prevents privilege escalation attacks.
- **Production Server**: Employs `gunicorn` with 3 worker processes binding to `0.0.0.0:5000`.
- **Integrated Health Check**:
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
      CMD curl -f http://localhost:5000/api/health || exit 1
  ```
- **Volume Mount Point**: Volume `/app/data` declared for persistent storage.

---

## 11. MODULE 6 — JENKINS CI/CD AUTOMATION PIPELINE
- **Declarative Pipeline (`Jenkinsfile`)**: 10 sequential stages enforcing automated quality gates.
- **Automated Triggers**:
  - `githubPush()`: Immediate build execution on GitHub push events.
  - `pollSCM('H/2 * * * *')`: 2-minute polling fallback for local environments without public webhooks.
- **Cross-Platform Compatibility**: Uses `isUnix()` branching to execute Linux `sh` commands or native Windows `bat` commands with automatic Anaconda/Python PATH resolution.
- **Artifact Archiving**: Generates and archives `pytest-results.xml` for build trend reporting.

---

## 12. MODULE 7 — AUTOMATED TESTING (PYTEST SUITE)
- **25 Comprehensive Test Cases**:
  - `test_workouts.py` (13 tests): CRUD, 400 validations for negative numbers/bad dates, missing fields, 404 handling.
  - `test_activity.py` (5 tests): Date querying, upsert behaviors, error handling.
  - `test_goals.py` (3 tests): Fetching, boundary conditions, goal updates.
  - `test_dashboard.py` (3 tests): Calorie and distance calculations, weekly aggregations, demo reset.
  - `test_health.py` (1 test): Health check JSON contract verification.
- **Execution Speed**: 25 passed in **0.79 seconds**.
- **Pytest Configuration (`pytest.ini`)**: Configured with `pythonpath = .` to guarantee consistent test discovery.

---

## 13. MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION
- **Playbook (`ansible/playbook.yml`)**: Agentless deployment automation ensuring idempotence.
- **Tasks**:
  1. Verifies Docker runtime on target hosts.
  2. Creates application directories and persistent `/app/data` with 0777 permissions.
  3. Inspects images and prunes outdated containers.
  4. Launches production container with volume mapping `fittrack_sqlite_data:/app/data`.
  5. Probes `/api/health` with retry intervals until deployment success is confirmed.

---

## 14. MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)
- **Named Volume**: `fittrack_sqlite_data`.
- **Persistence Verification**: Deleting or upgrading the container preserves all recorded workouts and activity logs within the named Docker volume on the host.

---

## 15. MODULE 10 — ANALYTICS ENGINE & GOAL MANAGEMENT
- Dynamic metric engine in `services/analytics.py`.
- Aggregates workout burn with baseline daily activities.
- Calculates weekly consistency rates and step completion percentages.

---

## 16. MODULE 11 — COMPLETE CI/CD INTEGRATION
- Integrates GitHub, Jenkins, Docker, Pytest, and Ansible into an unbroken automated chain.
- Ensures zero manual intervention from code commit to verified production deployment.

---

## 17. MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION
- Full audit confirming:
  - Docker container running with status `Up (healthy)`.
  - HTTP 200 response on `http://localhost:5000`.
  - Zero database locks or internal server errors.
  - All 25 automated tests green.

---

## 18. RESULTS AND OUTPUT

The project achieved 100% compliance with laboratory guidelines:
- ✅ **Full-Stack Application**: Functional Single Page Application with Flask backend and SQLite database.
- ✅ **Automated Testing**: 25/25 Pytest test cases passing in 0.79s.
- ✅ **Hardened Container**: Docker container running under non-root security with active health checks.
- ✅ **CI/CD Pipeline**: 10-stage cross-platform Jenkins pipeline with automated triggers.
- ✅ **Ansible Automation**: Idempotent deployment playbook with health verification.
- ✅ **Data Persistence**: Docker Volume retaining database records across container recreations.

---

## 19. COMMANDS USED (COMPREHENSIVE RUNBOOK)

### 1. Git & Version Control
```bash
git init
git add .
git commit -m "feat: complete FitTrack with DevOps automation"
git branch -M main
git remote add origin https://github.com/Pavithiran10/devops_cat.git
git push -u origin main
```

### 2. Pytest Automated Testing
```bash
pytest -v
pytest -v --pdb               # Interactive debug mode on failure
pytest -v --junitxml=pytest-results.xml
```

### 3. Docker Container Management
```bash
docker compose up --build -d  # Build and launch in detached mode
docker ps                     # Verify container health status
docker logs -f fittrack-app   # Inspect live Gunicorn output
curl http://localhost:5000/api/health
docker volume ls              # Verify persistent volume
docker compose down           # Stop container
```

### 4. Ansible Automated Deployment
```bash
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml \
    --extra-vars "docker_image_tag=latest target_hosts=local"
```

---

## 20. ADVANTAGES
- **Environment Parity**: Docker eliminates "works on my machine" bugs.
- **Rapid Quality Feedback**: Pytest suite prevents regressions from reaching production.
- **Automated Delivery**: Code changes automatically trigger builds and deployments without human intervention.
- **Container Hardening**: Non-root execution reduces attack vectors.
- **High Availability**: Automated health checks and restart policies ensure resilient service uptime.

---

## 21. LIMITATIONS
- Single-node SQLite database (not designed for multi-region concurrent writes).
- Single-user design (multi-tenant authentication not included).
- Localhost deployment environment.

---

## 22. FUTURE ENHANCEMENTS
1. **PostgreSQL Migration**: Move to multi-instance PostgreSQL for enterprise concurrency.
2. **Kubernetes Deployment**: Author Helm charts and manifests with PersistentVolumeClaims.
3. **Prometheus & Grafana Monitoring**: Real-time request latency and error rate visualization.
4. **JWT Authentication**: Add user accounts with role-based access control.

---

## 23. CONCLUSION

FitTrack successfully integrates full-stack web application development with modern DevOps automation in accordance with the 23IT723 DevOps Laboratory curriculum. By connecting Flask and SQLite with Git, GitHub, Jenkins, Docker, Pytest, and Ansible, the project establishes a robust, enterprise-grade continuous delivery pipeline. The automated quality gates, hardened containerization, and persistent storage prove that DevOps automation significantly accelerates software delivery while maintaining strict reliability and data integrity.
