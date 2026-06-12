# 🚜 Farm Pilot API

Farm Pilot API is the backend service powering the [Farm Pilot](https://github.com/tamilarasu18/farm-pilot) application. Built with FastAPI and an async SQLAlchemy stack, it provides a robust, high-performance RESTful API for managing agricultural data — users, lands, sections, crops, daily logs, soil tests, finances, and analytics.

> This is the backend repository. The frontend lives at [farm-pilot](https://github.com/tamilarasu18/farm-pilot) — live demo: [farm-pilot-blue.vercel.app](https://farm-pilot-blue.vercel.app/).

## 🌟 Features

- **Authentication & Authorization**: Secure JWT-based authentication with bcrypt password hashing.
- **Entity Management**: Full CRUD operations for Lands, Sections, and Crops (with a seeded default crop catalog).
- **Comprehensive Logging**: Track daily farming activities, weather conditions, crop health, and associated income & expenses.
- **Soil Health Tracking**: Record and manage soil test results.
- **Financial Analytics**: Aggregate revenue, expenses, net profit, monthly trends, and category-wise expense breakdowns.
- **Asynchronous by Design**: Fully async database interactions for high performance and scalability.
- **Auto-generated Docs**: Interactive Swagger UI and ReDoc out of the box.

## 🚀 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.10+
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async)
- **Database**: SQLite (`aiosqlite`) for development, PostgreSQL (`asyncpg`) ready for production
- **Data Validation**: [Pydantic V2](https://docs.pydantic.dev/latest/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Authentication**: `python-jose`, `bcrypt`
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Containerization**: Docker

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tamilarasu18/farmPilot-backend-api.git
   cd farmPilot-backend-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   DATABASE_URL=sqlite+aiosqlite:///./farmpilot.db
   ```

   > For PostgreSQL, use a connection string like:
   > `postgresql+asyncpg://user:password@host:5432/farmpilot`

## 🛠️ Running the API

To start the local development server with live reload:
```bash
uvicorn main:app --reload
```
The API will be accessible at [http://localhost:8000](http://localhost:8000).

- **Interactive API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative API Documentation (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

## 🐳 Running with Docker

Build and run the containerized API:
```bash
docker build -t farmpilot-api .
docker run -p 8000:8000 --env-file .env farmpilot-api
```

## 📚 API Modules

| Router | Prefix | Description |
| :--- | :--- | :--- |
| Auth | `/api/auth` | Registration & login (JWT) |
| Users | `/api/users` | User profile management |
| Lands | `/api/lands` | Lands & sections CRUD |
| Crops | `/api/crops` | Crop catalog & assignments |
| Daily Logs | `/api/logs`, `/api/sections/{id}/logs` | Activity logs, expenses & income |
| Soil Tests | `/api/soil-tests` | Soil health records |
| Analytics | `/api/analytics` | Financial aggregates & trends |

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📄 License

This project is licensed under the MIT License.
