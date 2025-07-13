# KPA_ASSIGNEMENT
# KPA Assignment Backend (Dockerized)

This repository contains the backend service implementation for the **KPA Form Assignment**, built using Django and PostgreSQL. The application exposes APIs as specified in the provided Postman collection and Swagger documentation.

---

## 🚀 Setup Instructions (using Docker)

> Prerequisites: Make sure you have [Docker](https://www.docker.com/products/docker-desktop/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shubham-babaa/KPA_ASSIGNEMENT.git
   cd KPA_ASSIGNEMENT

Create .env File
Create a .env file in the root directory and include the following environment variables:


POSTGRES_USER=shubham
POSTGRES_PASSWORD=baba@321
POSTGRES_DB=kpa_db
DB_HOST=db

Build and Run the Containers

docker-compose up --build



Access the API

Backend running at: http://localhost:8000

Swagger docs (if added): http://localhost:8000/docs/ or /swagger/


⚙️ Key Features Implemented
✅ Two API endpoints implemented from the provided Postman collection.
✅ PostgreSQL integration using Docker.
✅ .env support for environment configuration.
✅ FastAPI backend with Pydantic models.
✅ Basic request validation and exception handling.
✅ Clean and modular FastAPI project structure.
✅ Auto-generated API documentation via Swagger UI and ReDoc.



⚠️ Limitations / Assumptions
❌ No frontend is included in this repository (only backend logic).
⚠️ Assumes Docker is available and used for running both app and database.
⚠️ Authentication is not implemented unless specifically required.

