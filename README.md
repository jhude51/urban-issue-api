# Urban Issue Reporting API

[![Django CI Pipeline](https://github.com/jhude51/urban-issue-api/actions/workflows/ci.yml/badge.svg)](https://github.com/jhude51/urban-issue-api/actions/workflows/ci.yml)

A production-oriented REST API for reporting and managing urban infrastructure issues.

The project is built with Django REST Framework, PostgreSQL, Docker, Gunicorn, and GitHub Actions. It serves as a practical backend and DevOps portfolio project focused on building, containerising, testing, securing, and eventually deploying a real-world API.

---

## Project Status

**Active development**

The API foundation, issue-management functionality, documentation, and automated quality baseline are complete. The current version supports full CRUD operations, issue categorisation and prioritisation, lifecycle management, filtering, search, ordering, pagination, and interactive OpenAPI documentation.

The project also includes automated API and edge-case testing, Ruff linting and formatting, application coverage measurement, OpenAPI schema validation, and Docker image validation through GitHub Actions.

The project has not yet been deployed to Azure. Cloud deployment, managed PostgreSQL, infrastructure automation, observability, and alerting remain planned.

---

## Problem Statement

Urban infrastructure issues such as potholes, broken traffic lights, damaged roads, drainage problems, and faulty public facilities are often reported through informal or fragmented channels.

This can make it difficult to:

- Store reports in a consistent format
- Validate the information being submitted
- Track when issues were reported
- Organise reports for further action
- Build automated workflows around issue resolution
- Analyse infrastructure problems over time

The Urban Issue Reporting API provides the backend foundation for a system where citizens, vendors, and other stakeholders can submit structured issue reports.

The long-term goal is to evolve the project into a cloud-hosted platform that supports issue tracking, categorisation, prioritisation, resolution workflows, automation, and operational reporting.

---

## Why I Built This Project

I started this project as part of my transition from IT support and infrastructure operations into DevOps and cloud engineering.

My professional experience has largely involved troubleshooting endpoints, infrastructure, identity platforms, operating systems, networks, and production support issues. I wanted a project that would help me move beyond maintaining existing systems and gain practical experience building and operating an application across its full lifecycle.

This project allows me to apply:

- Python and Django backend development
- Linux and command-line troubleshooting
- PostgreSQL administration
- Docker containerisation
- CI pipeline development
- Environment and secret management
- Application server configuration
- Deployment security assessment
- Root-cause analysis
- Technical documentation

Rather than treating the API as a one-time coding exercise, I am developing it as an evolving production-oriented system.

---

## Current Features

### API and Issue management

- Create, retrieve, update, partially update, and delete urban issue reports
- Categorise issues by infrastructure type
- Assign operational priority levels
- Track issues through a controlled lifecycle
- Enforce valid lifecycle transitions
- Filter by reporter, category, priority, and status
- Search across title, description, and location
- Order issue collections
- Paginate API responses
- Validate submitted data using Django REST Framework serializers
- Store issue data in PostgreSQL
- Manage records through the Django admin interface

Each issue contains:

- `id`
- `title`
- `description`
- `location`
- `reporter`
- `category`
- `priority`
- `status`
- `created_at`
- `updated_at`

Supported reporter types are citizen and vendor.

### Application and DevOps foundation

- Environment-based Django configuration
- PostgreSQL database service
- Multi-stage Docker image
- Docker Compose orchestration
- PostgreSQL health checks
- Gunicorn production application server
- Automated database migrations during container startup
- GitHub Actions CI pipeline
- Automated Django system checks
- Automated tests
- Automated Docker image build validation
- Configurable HTTPS, cookie, and HSTS settings

### Quality engineering

- Automated API and edge-case test coverage
- Ruff linting and formatting enforcement
- Application coverage measurement with Coverage.py
- Minimum 95% coverage enforced in CI
- OpenAPI schema validation with warnings treated as failures
- Development and runtime dependencies separated
- Docker image build validation in CI

### Container hardening

- Non-root application runtime
- Reduced runtime image size using a dedicated virtual environment
- Minimal runtime image contents
- Graceful Gunicorn process handling with a dedicated entrypoint
- Application and database health endpoint
- Docker-native container health checks
- OCI image metadata for source and version traceability
- Commit-specific Docker image tags in CI

### CI/CD and artifact delivery

- Quality-gated pull request workflow
- Automated container publishing after successful merges to `main`
- GitHub Container Registry integration
- Commit-specific image tags
- `latest` image tag for the newest successful `main` build
- OCI version and Git revision metadata
- Immutable SHA-256 deployment references
- Registry artifact verification after publishing

---

## Architecture

### Application request flow

```text
Client
  |
  | HTTP request
  v
Django REST Framework API
  |
  | Serializer validation
  v
Django ORM
  |
  | SQL queries
  v
PostgreSQL
```

### Container architecture

```text
Docker Compose
  |
  +-- django_app
  |     |
  |     +-- Non-root app user
  |     +-- Entrypoint applies migrations
  |     +-- Gunicorn runs as PID 1
  |     +-- /health/ checks Django + PostgreSQL
  |     +-- Docker HEALTHCHECK monitors /health/
  |
  +-- postgres_db
        |
        +-- PostgreSQL 15
        +-- Persistent named volume
        +-- Database health check
```

The Django container waits until PostgreSQL reports a healthy state before migrations and Gunicorn are started.

### CI workflow

```text
Pull request
    |
    v
Build / quality job
    |
    +-- Ruff linting and formatting
    +-- PostgreSQL
    +-- Django checks
    +-- OpenAPI validation
    +-- Tests and coverage
    +-- Docker build validation

Merge to main
    |
    v
Build / quality job
    |
    v
Publish container image
    |
    +-- Authenticate to GHCR
    +-- Build release image
    +-- Tag with commit SHA
    +-- Tag as latest
    +-- Push to GHCR
    +-- Capture registry digest
    +-- Pull and verify immutable image
    +-- Publish release summary```

---

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | Django |
| API framework | Django REST Framework |
| Database | PostgreSQL 15 |
| ORM | Django ORM |
| Configuration | python-decouple |
| Application server | Gunicorn |
| Containerisation | Docker |
| Local orchestration | Docker Compose |
| Continuous integration | GitHub Actions |
| Version control | Git and GitHub |
| Container registry | GitHub Container Registry |

---

## Project Structure

```text
urban-issue-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── issues/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
|   │   ├── pagination.py
│   │   └── views.py
│   └── manage.py
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── .coveragerc
├── pyproject.toml
└── README.md
```

---

## Quick Start with Docker

Docker Compose is the recommended way to run the complete application locally.

### 1. Clone the repository

```bash
git clone https://github.com/jhude51/urban-issue-api.git
cd urban-issue-api
```

### 2. Create your environment file

```bash
cp .env.example .env
```

Replace the placeholder values in `.env`.

For Docker Compose, ensure the database host is set to the Compose service name:

```env
DB_HOST=db
```

Generate a local Django secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated value into:

```env
SECRET_KEY=your_generated_secret_key
```

A development Docker configuration should contain values similar to:

```env
SECRET_KEY=your_generated_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=urban_issue_db
DB_USER=dayo
DB_PASSWORD=replace_with_a_database_password
DB_HOST=db
DB_PORT=5432

POSTGRES_DB=urban_issue_db
POSTGRES_USER=dayo
POSTGRES_PASSWORD=replace_with_a_database_password

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
```

The Django `DB_*` values and PostgreSQL `POSTGRES_*` values must describe the same database credentials.

### 3. Build and start the services

```bash
docker compose up --build
```

Docker Compose will:

1. Start PostgreSQL
2. Wait until PostgreSQL reports a healthy state
3. Start the Django container
4. Apply database migrations
5. Start Gunicorn on port `8000`

### 4. Test the API

```bash
curl -i http://localhost:8000/issues/
```

A new database should return an empty list:

```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

### 5. Check container status

```bash
docker compose ps
```

The PostgreSQL service should be healthy and the Django service should be running.

### 6. Stop the services

```bash
docker compose down
```

The PostgreSQL data is stored in a named Docker volume and will remain available after the containers are stopped.

To also delete the development database volume:

```bash
docker compose down -v
```

> This permanently removes the PostgreSQL data stored by the Compose project.

---

## Local Development Without Docker

A local PostgreSQL server is required when running the Django application outside Docker.

### 1. Create a virtual environment

Linux, macOS, or WSL:

```bash
python -m venv venv
source venv/bin/activate
```

Windows Command Prompt:

```bat
python -m venv venv
venv\Scripts\activate
```

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure the environment

Copy the example file:

```bash
cp .env.example .env
```

For a PostgreSQL server running directly on your machine, use:

```env
DB_HOST=localhost
```

Create the database and database user using values that match the environment file.

### 4. Apply migrations

```bash
python app/manage.py migrate
```

### 5. Run the development server

```bash
python app/manage.py runserver
```

The API will be available at:

```text
http://localhost:8000/issues/
```

---

## Environment Variables

### Django and database configuration

| Variable | Purpose | Local example |
|---|---|---|
| `SECRET_KEY` | Django cryptographic signing secret | Generated private value |
| `DEBUG` | Enables or disables Django debugging | `True` |
| `ALLOWED_HOSTS` | Comma-separated accepted hostnames | `localhost,127.0.0.1` |
| `DB_NAME` | Database used by Django | `urban_issue_db` |
| `DB_USER` | Database user used by Django | `dayo` |
| `DB_PASSWORD` | Database password used by Django | Private value |
| `DB_HOST` | PostgreSQL hostname | `db` in Compose, `localhost` outside Docker |
| `DB_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | Database created by the PostgreSQL image | `urban_issue_db` |
| `POSTGRES_USER` | User created by the PostgreSQL image | `dayo` |
| `POSTGRES_PASSWORD` | Password assigned by the PostgreSQL image | Private value |

### HTTPS and production security

| Variable | Development default | Purpose |
|---|---:|---|
| `SECURE_SSL_REDIRECT` | `False` | Redirects HTTP requests to HTTPS |
| `SESSION_COOKIE_SECURE` | `False` | Sends session cookies only over HTTPS |
| `CSRF_COOKIE_SECURE` | `False` | Sends CSRF cookies only over HTTPS |
| `SECURE_HSTS_SECONDS` | `0` | Sets the browser HSTS duration |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | `False` | Applies HSTS to all subdomains |
| `SECURE_HSTS_PRELOAD` | `False` | Enables the HSTS preload directive |

The HTTPS values remain disabled during local HTTP development.

They should only be enabled after HTTPS, the production domain, reverse-proxy behaviour, and subdomain strategy have been verified.

---

## API Endpoints

The API supports full CRUD operations, issue lifecycle management, filtering, search, ordering, and pagination.

Base URL during local development:

```text
http://localhost:8000
```

### Endpoint Summary

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/issues/` | List issues |
| `POST` | `/issues/` | Create an issue |
| `GET` | `/issues/{id}/` | Retrieve an issue |
| `PUT` | `/issues/{id}/` | Replace an issue |
| `PATCH` | `/issues/{id}/` | Partially update an issue |
| `DELETE` | `/issues/{id}/` | Delete an issue |

### Create an Issue

```bash
curl -X POST http://localhost:8000/issues/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Large pothole on major road",
    "description": "A large pothole is affecting traffic.",
    "location": "Ring Road, Ibadan",
    "reporter": "citizen",
    "category": "road",
    "priority": "high"
  }'
```

New issues default to:

```text
category = other
priority = medium
status   = reported
```

### Issue Lifecycle

```text
reported → acknowledged → in_progress → resolved → closed
                                      ↑
                                      └── resolved issues may be reopened
```

Invalid lifecycle transitions are rejected with `400 Bad Request`.

### Filtering, Search and Ordering

Filter by reporter, category, priority, or status:

```bash
curl "http://localhost:8000/issues/?category=road&priority=high&status=reported"
```

Search across title, description, and location:

```bash
curl "http://localhost:8000/issues/?search=Bodija"
```

Order results:

```bash
curl "http://localhost:8000/issues/?ordering=-updated_at"
```

### Pagination

Results are paginated with a default page size of `5` and a maximum configurable page size of `50`.

```bash
curl "http://localhost:8000/issues/?page=2&page_size=10"
```

### API Documentation

| Endpoint | Purpose |
|---|---|
| `/api/schema/` | OpenAPI schema |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc documentation |

Swagger and ReDoc provide the complete request/response schemas, field descriptions, validation rules, query parameters, and examples.

---

## Testing and Quality Checks

The project uses automated tests and static quality checks to protect API behaviour and prevent regressions.

### Run the test suite

From the `app` directory:

```bash
DB_HOST=localhost python manage.py test -v 2
```

The current suite covers:
- CRUD operations
- Issue lifecycle transitions
- Category, priority, and reporter validation
- Required fields and field-length limits
- Filtering, searching, and ordering
- Pagination and pagination limits
- PUT and PATCH behaviour
- Read-only server-managed fields
- OpenAPI, Swagger, and ReDoc availability
- Invalid and edge-case API requests

### Code Quality

Run linting:
```bash
ruff check app
```

Check formatting:
```bash
ruff format --check app
```

To format the code locally:
```bash
ruff format app
```

### Test Coverage

Run tests with coverage:
```bash
cd app

DB_HOST=localhost coverage run \
  --rcfile=../.coveragerc \
  manage.py test

coverage report \
  --rcfile=../.coveragerc \
  -m

cd ..
```

The project currently achieves 100% coverage across the measured application code.

CI requires a minimum coverage threshold of 95%.

Test files, migrations, and framework entrypoints are excluded from the application coverage calculation.

### Run Django system checks

```bash
python app/manage.py check
```

### Check installed dependency compatibility

```bash
python -m pip check
```

### Build the Docker image

```bash
docker build --tag urban-issue-api:local .
```

### Validate the complete Compose environment

```bash
docker compose up --build -d
docker compose ps
curl -i http://localhost:8000/issues/
```

### Run Django's deployment assessment

```bash
DEBUG=False python app/manage.py check --deploy
```

A production simulation can be performed using:

```bash
DEBUG=False \
SECURE_SSL_REDIRECT=True \
SESSION_COOKIE_SECURE=True \
CSRF_COOKIE_SECURE=True \
SECURE_HSTS_SECONDS=3600 \
SECURE_HSTS_INCLUDE_SUBDOMAINS=False \
SECURE_HSTS_PRELOAD=False \
python app/manage.py check --deploy
```

Warnings relating to HSTS subdomains and browser preload are currently intentional. Those settings will remain disabled until the final production domain and HTTPS architecture are established.

---

## Continuous Integration

The GitHub Actions workflow runs:

- On every pull request
- On every push to `main`

### CI quality gates

Every pull request is validated through GitHub Actions.

The pipeline performs:

1. Dependency installation
2. Ruff linting
3. Ruff formatting validation
4. PostgreSQL service health checks
5. Django migrations
6. Django system checks
7. OpenAPI schema validation
8. Automated tests
9. Minimum 95% application coverage enforcement
10. Docker image build validation

A pull request is not considered ready to merge until the pipeline completes successfully.

---

## Production Readiness

The project currently includes a production-oriented foundation, but it should not yet be described as a fully production-ready or production-deployed service.

### Implemented controls

- Sensitive Django settings are loaded from environment variables
- The secret key is no longer hardcoded
- Debug mode is environment controlled
- Allowed hosts are environment controlled
- HTTPS redirect behaviour is configurable
- Secure session and CSRF cookies are configurable
- HSTS duration is configurable
- HSTS subdomain and preload policies are configurable
- Gunicorn is used instead of Django's development server
- Dependencies are pinned
- Docker uses separate builder and runtime stages
- PostgreSQL readiness is checked before application startup
- CI validates migrations, checks, tests, and the Docker build
- Application container runs as a non-root user
- Runtime image excludes development-only files and dependencies
- Gunicorn receives container termination signals directly
- Application health checks verify database connectivity
- Docker monitors application health at runtime
- Built images include OCI source, version, and revision metadata

### Deferred deployment decisions

The following will be finalised during cloud deployment:

- Azure hosting service
- Production PostgreSQL service
- Production domain
- TLS certificate configuration
- Reverse-proxy HTTPS headers
- Trusted proxy configuration
- HSTS duration
- HSTS subdomain coverage
- HSTS preload eligibility
- Static file strategy
- Production logging
- Monitoring and alerting

---

## Container Registry

Successful merges to `main` publish the application image to GitHub Container Registry:

```text
ghcr.io/jhude51/urban-issue-api
```

Published images receive:

- a commit-specific tag, such as 1ba42be
- the mutable latest tag
- an immutable registry digest

Pull a specific version:

```bash
docker pull ghcr.io/jhude51/urban-issue-api:1ba42be
```

For production deployment, the immutable digest is preferred:

```text
ghcr.io/jhude51/urban-issue-api@sha256:<digest>
```

This ensures the deployed container refers to the exact artifact produced and verified by CI/CD.

---

## Key Engineering Decisions

### PostgreSQL instead of SQLite

PostgreSQL provides an environment closer to a real production system. It also introduces practical experience with database users, permissions, service readiness, credentials, networking, persistence, and CI database services.

### Environment-based configuration

Configuration varies between local development, Docker, CI, and production. Externalising the configuration prevents sensitive values from being committed and allows the same application code to run in different environments.

### Gunicorn instead of `runserver`

Django's development server is intended for development. Gunicorn provides the production WSGI runtime used by the container.

### Multi-stage Docker build

Dependencies are installed in a builder stage and copied into a separate runtime stage. This separates dependency installation from application execution and provides a cleaner production foundation.

### Database health checks

Opening port `5432` does not necessarily mean the configured PostgreSQL database is ready for application traffic. The Compose health check uses `pg_isready` and delays the Django service until PostgreSQL is healthy.

### Disposable CI credentials

The CI database is temporary and isolated. Visible non-production test credentials make the pipeline reproducible for pull requests without exposing or depending on production secrets.

### Deliberate HSTS adoption

HSTS can have long-lasting effects on a domain and its subdomains. The application supports HSTS configuration, but advanced options remain disabled until the deployed domain and HTTPS architecture are verified.

---

## Project Experience

Through this project, I have gained hands-on experience in the following areas:

### Backend development

- Creating Django models
- Working with Django migrations
- Building Django REST Framework serializers
- Implementing serializer-level validation
- Creating list and create API operations
- Using the Django ORM with PostgreSQL
- Returning structured API responses and validation errors

### Containerisation

- Writing a multi-stage Dockerfile
- Containerising Django and Gunicorn
- Running Django and PostgreSQL as separate services
- Configuring service-to-service networking
- Persisting PostgreSQL data with named volumes
- Adding database health-aware startup behaviour
- Debugging container logs and worker startup failures

### Continuous integration

- Creating a GitHub Actions workflow
- Running PostgreSQL as a CI service
- Supplying isolated CI environment variables
- Automating migrations
- Automating Django system checks
- Automating test execution
- Validating that the Docker image builds on a clean runner
- Using pull requests and green pipelines as merge gates

### Configuration and security

- Removing hardcoded secrets
- Managing environment-specific configuration
- Parsing Boolean and list values from environment variables
- Assessing deployment security with `check --deploy`
- Making HTTPS, cookie, and HSTS settings environment controlled
- Separating local development settings from production decisions

### Troubleshooting

- Reading Python tracebacks
- Identifying the first meaningful exception
- Diagnosing Python import-path problems
- Troubleshooting PostgreSQL permissions and readiness
- Distinguishing network failures from code failures
- Comparing behaviour across local, Docker, and CI environments
- Applying fixes through small branches and pull requests

---

## Challenges and Lessons Learned

### 1. PostgreSQL permissions and ownership

**Problem**

The application initially encountered PostgreSQL permission errors while attempting to create or access database objects.

**Diagnosis**

A successful connection to PostgreSQL did not automatically mean the application user had the correct database and schema permissions.

**Resolution**

The PostgreSQL role, database ownership, and required permissions were reviewed and corrected.

**Lesson**

Database connectivity, authentication, database ownership, and schema permissions are separate concerns. A database connection can succeed while migrations still fail.

---

### 2. Conflicting `decouple` packages

**Problem**

Django failed with:

```text
ImportError: cannot import name 'config' from 'decouple'
```

**Diagnosis**

The environment had previously contained the unrelated `decouple` package instead of, or alongside, the required `python-decouple` package.

Both packages use the same Python import name:

```python
from decouple import config
```

**Resolution**

The conflicting packages were removed and the pinned project requirements were reinstalled.

**Lesson**

The import name used in Python code is not always the same as the package name installed by pip. Dependency conflicts can remain in a virtual environment even after a requirements file has been corrected.

---

### 3. Inconsistent Django import paths

**Problem**

Local execution and CI produced errors such as:

```text
ModuleNotFoundError: No module named 'app'
```

**Diagnosis**

The project mixed two different Python package conventions:

```text
app.core
app.issues
```

and:

```text
core
issues
```

Running:

```bash
python app/manage.py
```

adds the inner `app/` directory to Python's import path. From that execution context, the correct top-level packages are `core` and `issues`.

**Resolution**

The project was standardised to use:

```text
core.settings
core.urls
core.wsgi
issues.apps.IssuesConfig
issues.views
```

**Lesson**

Python imports depend on the working directory and the entries in `sys.path`. A module path that works from one execution location may fail from another.

---

### 4. Gunicorn working-directory failure

**Problem**

Gunicorn found the WSGI file but the worker failed while loading Django settings:

```text
ModuleNotFoundError: No module named 'core'
```

**Diagnosis**

Gunicorn was launched from the repository root, while the `core` package was inside the nested `app/` directory.

**Resolution**

Gunicorn was configured to change into the Django application directory before loading the WSGI module:

```bash
gunicorn --chdir app core.wsgi:application --bind 0.0.0.0:8000
```

**Lesson**

Finding a WSGI file and successfully booting the Django application are separate stages. The application server's working directory must match the project's Python import layout.

---

### 5. Port availability versus database readiness

**Problem**

The Django container originally waited for PostgreSQL by checking whether port `5432` was open.

**Diagnosis**

An open TCP port only indicates that a process is listening. It does not confirm that PostgreSQL has completed initialisation or that the configured database is ready.

**Resolution**

The manual Netcat loop was replaced with a Docker health check using:

```bash
pg_isready
```

The Django service now depends on the PostgreSQL service reaching a healthy state.

**Lesson**

Service availability should be measured with an application-aware health check rather than a basic network-port test.

---

### 6. Generated Python files committed to Git

**Problem**

Compiled `.pyc` files and `__pycache__` directories were accidentally tracked in the repository.

**Diagnosis**

Adding a pattern to `.gitignore` does not automatically remove files that Git already tracks.

**Resolution**

The files were removed from Git's index and the ignore rules were expanded:

```gitignore
__pycache__/
*.py[cod]
*$py.class
```

**Lesson**

`.gitignore` prevents new untracked files from being added. Previously tracked generated files must be explicitly removed from the index.

---

### 7. Docker dependency download timeout

**Problem**

A clean Docker build failed while downloading Django from PyPI:

```text
ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org')
```

**Diagnosis**

The download had started successfully but the network connection was extremely slow and timed out. The error was unrelated to the application code or dependency compatibility.

**Resolution**

The build was retried without unnecessarily discarding all reusable Docker layers. Pip timeout and retry settings were also considered for unreliable connections.

**Lesson**

Not every build failure is a source-code failure. Download rate, timeout location, and the final exception should be examined before changing application dependencies.

---

### 8. Differences between local, Docker, and CI environments

**Problem**

Configuration that worked locally did not always work in Docker or GitHub Actions.

Examples included:

- `DB_HOST=localhost` locally versus `DB_HOST=db` in Compose
- Required `SECRET_KEY` missing in CI
- Different Python working directories
- PostgreSQL service credentials not matching Django credentials

**Diagnosis**

Each environment has a different network and process context even though it runs the same application code.

**Resolution**

Configuration was made explicit for each environment:

- `.env` for local and Compose execution
- Disposable job-level values for CI
- Service names for container networking
- Consistent commands for migrations, checks, tests, and Gunicorn

**Lesson**

A reliable application requires configuration parity, not identical configuration values. Every environment must supply the same categories of configuration in a way appropriate to that environment.

---

### 9. CI success did not initially validate the container

**Problem**

The first passing pipeline proved that Django migrations, checks, and tests worked, but it did not prove that the Dockerfile could build.

**Diagnosis**

The workflow ended after the test stage.

**Resolution**

A Docker build stage was added:

```bash
docker build --tag urban-issue-api:ci .
```

**Lesson**

A green pipeline only validates the steps it actually runs. CI coverage must be compared with the artefacts intended for deployment.

---

## What I Learned

The most important lesson from this project is that application development and DevOps cannot be separated cleanly.

A backend API may work in a local Python process but still fail because of:

- Package conflicts
- Import paths
- Incorrect working directories
- Missing environment variables
- Database permissions
- Service startup order
- Container networking
- CI configuration
- Production security requirements

I also learned to use a more structured troubleshooting process:

1. Reproduce the problem
2. Read the full error output
3. Locate the first meaningful exception
4. Identify the failing layer
5. Change one relevant variable at a time
6. Run the smallest useful verification command
7. Test locally
8. Test in Docker
9. Test in CI
10. Document the final decision

This project has helped me move from simply following tutorials toward understanding why application, container, database, and CI configurations behave the way they do.

---

## Roadmap

### Completed

- [x] Django REST API foundation
- [x] PostgreSQL integration
- [x] Environment-based database configuration
- [x] Issue creation endpoint
- [x] Issue list endpoint
- [x] Serializer-level validation
- [x] Initial automated model test
- [x] Multi-stage Docker image
- [x] Docker Compose environment
- [x] Gunicorn runtime
- [x] PostgreSQL health check
- [x] Environment-based security settings
- [x] GitHub Actions CI
- [x] Automated migrations and system checks
- [x] Automated Docker build validation
- [x] Production deployment assessment

### Planned API development

- [x] Retrieve a single issue
- [x] Update an issue
- [x] Delete an issue
- [x] Issue status lifecycle
- [x] Issue categories
- [x] Priority levels
- [ ] Assignment and ownership
- [x] Filtering and search
- [x] Pagination
- [ ] Authentication and authorisation
- [x] Expanded validation
- [x] OpenAPI and Swagger documentation

### Planned quality improvements

- [x] Serializer tests
- [x] API endpoint tests
- [x] Validation tests
- [ ] Permission tests
- [x] Test coverage reporting
- [x] Linting and formatting checks
- [x] Container runtime health endpoint

### Planned DevOps development

- [x] Build versioned Docker images
- [x] Publish versioned Docker images
- [ ] Deploy the API to Azure
- [ ] Configure a managed PostgreSQL database
- [ ] Add deployment automation
- [ ] Provision infrastructure with Terraform
- [ ] Add structured production logging
- [ ] Add monitoring and observability
- [ ] Add alerting
- [ ] Evaluate Kubernetes deployment after the initial cloud deployment

---

## Author

**Dayo Jude Adeyemi**

IT Workspace Specialist transitioning into DevOps and cloud engineering, with a focus on Linux, Azure, AWS, Docker, Kubernetes, CI/CD, automation, and production troubleshooting.

- GitHub: [jhude51](https://github.com/jhude51)
- LinkedIn: [dayo-jude-adeyemi](https://www.linkedin.com/in/dayo-jude-adeyemi)

This project is part of my practical journey toward building and operating reliable cloud-native applications rather than relying only on certifications and tutorial-based learning.