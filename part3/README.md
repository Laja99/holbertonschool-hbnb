# Part 3: Enhanced Backend with Authentication and Database Integration

## Project Overview
Part 3 of the HBnB project extends the backend to introduce **user authentication, authorization, and persistent database storage**. This allows the application to scale from a prototype with in-memory storage to a production-ready backend using SQL databases.

---

**Key enhancements in this part include:**

- **JWT-based authentication** for secure login and session management.
- **Role-based access control** to restrict access based on user roles (`is_admin`).
- **Database integration** using SQLAlchemy ORM with SQLite for development and MySQL for production.
- **CRUD operations** refactored to persist data in a relational database.
- **Database design and visualization** using Mermaid.js ER diagrams.
- Ensuring **data consistency, validation, and security** in the backend.


## Task List

### 0. Modify the Application Factory to Include the Configuration
- **Objective:** Update `create_app()` in `app/__init__.py` to accept a configuration object.
- **Outcome:** Application Factory can handle different configurations (development, testing, production).

### 1. Modify the User Model to Include Password Hashing
- **Objective:** Store hashed passwords using bcrypt.
- **Outcome:** Passwords are hashed on registration and never returned in GET requests.

### 2. Implement JWT Authentication
- **Objective:** Use `flask-jwt-extended` to secure endpoints and manage sessions.
- **Outcome:** Login functionality issues JWT tokens; protected endpoints require a valid token.

### 3. Implement Authenticated User Access Endpoints
- **Objective:** Secure endpoints so authenticated users can create/update/delete resources they own.
- **Outcome:** Users can manage their own Places, Reviews, and User data securely.

### 4. Implement Administrator Access Endpoints
- **Objective:** Restrict access to admin-only endpoints for managing users, amenities, and bypass ownership restrictions.
- **Outcome:** Admins can perform privileged actions and manage resources globally.

### 5. Implement SQLAlchemy Repository
- **Objective:** Replace in-memory repository with SQLAlchemy-based repository.
- **Outcome:** All CRUD operations interact with SQLite for development and prepare for production databases.

### 6. Map the User Entity to SQLAlchemy Model
- **Objective:** Map `User` entity with proper attributes, relationships, and repository integration.
- **Outcome:** User data is stored persistently in the database with hashed passwords.

### 7. Map Place, Review, and Amenity Entities
- **Objective:** Map core attributes of Place, Review, and Amenity entities using SQLAlchemy.
- **Outcome:** Entities are persisted in the database, CRUD operations supported; relationships will be added later.

### 8. Map Relationships Between Entities Using SQLAlchemy
- **Objective:** Define one-to-many and many-to-many relationships between entities.
- **Outcome:** Structured relationships (User–Place, Place–Review, Place–Amenity) with constraints and foreign keys.

### 9. SQL Scripts for Table Generation and Initial Data
- **Objective:** Create SQL scripts to generate tables and insert initial data.
- **Outcome:** Database schema created with initial admin user, amenities, and tested CRUD operations.

### 10. Generate Database Diagrams
- **Objective:** Create ER diagrams using Mermaid.js.
- **Outcome:** Visual representation of tables, attributes, and relationships for documentation and review.

## Technologies & Resources

- **Flask** – Python web framework
- **SQLAlchemy & Flask-SQLAlchemy** – ORM for database management
- **SQLite / MySQL** – Relational databases
- **Flask-Bcrypt** – Password hashing
- **Flask-JWT-Extended** – JWT authentication
- **Mermaid.js** – ER diagram generation
- **cURL / Postman** – API testing
