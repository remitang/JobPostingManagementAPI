# Job Posting Management API

This repository contains a **Job Posting Management API** built with FastAPI. It is designed to manage job postings, users, and companies for a job board platform. The API implements role-based access control to ensure secure and reliable operations for different user roles, including Candidates, Recruiters, and Admins.  

---

## 🚀 Features  

### Core Functionality  
- **User Authentication & Authorization**:  
  - Secure password hashing and JWT-based authentication.  
  - Role-based access control for Candidates, Recruiters, and Admins.  
- **CRUD Operations**:  
  - Fully implemented CRUD endpoints for Users, Companies, and Job Postings.  
- **Company and Job Posting Management**:  
  - Only authorized users (Admins and Recruiters) can create, update, or delete companies and job postings.  
  - Role-specific access to sensitive operations.  

### Advanced Features  
- **User Dashboard**: `/me` endpoint for users to view their personal information.  
- **Database Integration**:  
  - Relational database setup with PostgreSQL for managing users, job postings, and companies.  
  - Optimized schema design with relations and constraints.  
- **Testing**:  
  - Comprehensive unit tests with Pytest.  
  - End-to-end testing with Postman collections.  

### Future Improvements  
- **Containerization**: Dockerizing the application for streamlined deployment and dependency management.  
- **Application Management**: Enabling candidates to apply for jobs and allowing recruiters to manage applications.  

---

## 📁 Project Architecture  

![Project Architecture](Project%20architecture.png)

This project is designed to manage job postings with a clear structure, making it easy to extend and maintain.  
The architecture follows a modular approach with distinct layers for models, routes, services, and database interactions.

---

## 📂 Project Structure  

```
JobPostingManagementAPI
├── app/
│   ├── main.py         # Application entry point
│   ├── models/         # Database models
│   │   ├── company.py  # Company model
│   │   ├── job_posting.py  # Job Posting model
│   │   └── user.py     # User model
│   ├── routers/        # API routes
│   │   ├── company.py  # Routes for managing companies
│   │   ├── job_posting.py  # Routes for managing job postings
│   │   └── user.py     # Routes for user authentication and management
│   ├── auth.py         # Authentication logic and JWT handling
│   ├── database.py     # Database connection and configuration
│   └── config.py       # App configuration
├── tests/              # Unit and integration tests
│   └── test_user.py    # Tests for user authentication and management
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🛠️ **Tech Stack**

- **Backend**: FastAPI (with Uvicorn server)
- **Database**: PostgreSQL (managed with PgAdmin)
- **Testing**: Pytest, Postman
- **Documentation**: Swagger / Redoc

---

## 🖥️ **Getting Started**

### Prerequisites

- Install Python 3.10+
- Install PostgreSQL and PgAdmin

### Installation

1. **Clone the repository:**

```
git clone https://github.com/remitang/JobPostingManagementAPI.git  
cd job-posting-api
```

2. **Install dependencies:**

```
pip install -r requirements.txt
```

3. **Set up the PostgreSQL database:**

   - Create a database and user in PostgreSQL.
   - Update the `DATABASE_URL` in the `config.py` file.

4. **Run the application:**

```
uvicorn app.main:app --reload
```

5. **Access the API documentation:**

   - Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

6. **Run tests:**

```
pytest tests/
```

---


🧪 **Testing**

- **Unit Testing**: Implemented with Pytest for validating endpoints and features.
- **Integration Testing**: Verified with Postman for end-to-end scenarios.
- **Test Coverage**: Covers authentication, CRUD operations, and role-based access control.

---


🛡️ **Security**

- **Authentication**: Secure JWT-based authentication for all API operations.
- **Authorization**: Strict role-based access control for sensitive actions.

---


🤝 **Contributing**

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

📧 **Contact**

For questions or suggestions, feel free to reach out at: `pro@remitang.com`.
