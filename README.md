# HBnB Project

## Table of Contents
- [Overview](#overview)
- [Project Stages](#project-stages)
- [Authors](#authors)

---

## Overview
Simplified AirBnB-like backend application focused on system design and architecture. While the initial phase emphasized creating UML-based technical documentation to define core entities and business rules, the project has now evolved into a fully functional modular implementation. 
The current phase bridges the gap between theoretical design and practical application, ensuring that the software remains maintainable, scalable, and robust.

---

## Project Stages  
### **1. UML**
- **High-Level Package Diagram:** 

create a high-level package diagram that illustrates the three-layer architecture of the HBnB application and shows how these layers interact using the Facade Pattern.

- **Class Diagram for Business Logic Layer:**

Show the main business entities, the data they contain, and how they relate to each other.

- **Sequence Diagrams:**  

Visualize how core API requests flow through the Presentation, Business Logic, and Persistence layers in the HBnB application. The diagrams clarify component interactions and data flow for key use cases, serving as a blueprint for implementation.

---

### **2. BL and API**
- **Business Logic Layer:**

Implemented OOP-based models (User, Place, Review, Amenity) inheriting from a unified BaseModel for UUID and timestamp management.

- **Facade Pattern Integration:**

Integrated a Facade Pattern to decouple the API from business logic, ensuring a single entry point for all operations.

- **In-Memory Persistence:**

Deployed an In-Memory Repository to manage data storage and entity relationships without database overhead.

- **RESTful API Development:**

Developed RESTful endpoints via Flask-RESTx, supporting full CRUD operations and complex entity linking.

- **Validation & Data Integrity:**

Applied strict validation rules (e.g., email formats, rating scales) across models and API layers.

---

### **3. Authentication and Database Integration**

- **Authentication & Authorization**

Implement JWT-based authentication using Flask-JWT-Extended.

Enforce role-based access control with is_admin attribute for specific endpoints.

- **Database Integration**

Use SQLAlchemy ORM for database management.

Integrate SQLite for development and prepare MySQL for production environments.

- **CRUD Operations**

Refactor all CRUD operations to interact with the persistent database.

- **Database Design & Visualization**

Design the database schema and visualize it using mermaid.js.

Map relationships between entities: Users, Places, Reviews, Amenities.

- **Data Consistency & Validation**

Ensure proper data validation and constraints in models.

---

### **4. Simple Web Client**

- **Design & Structure**

Login Page: Form for user credentials.

List of Places: Grid or list view of available properties.

Place Details: Detailed view of a specific property.

Add Review: Interactive form for feedback.

- **Authentication (Login)**

Implement the login logic by sending a POST request to your back-end.

Upon successful login, capture the JWT token.

Store the token in a cookie to manage the user session efficiently.

- **List of Places (Main Page)**

Fetch all places from the API and display them dynamically.

Client-side Filtering: Implement a filter to sort places by country.

Auth Guard: Ensure that unauthenticated users are redirected to the login page.

- **Place Details**

Retrieve specific place information using the place_id from the URL.

Display amenities, descriptions, and existing reviews.

Conditionally display the "Add Review" button only if the user is logged in.

- **Add Review**

Develop the submission form for reviews.

Strictly restrict access to authenticated users; unauthorized attempts should redirect back to the index page.

---

## Authors

**Fai AlSharekh** - [GitHub](https://github.com/Fai-Web-Lab)  
**Layla Alshehri** - [GitHub](https://github.com/Laja99)  
**Mohammed Aloufi** - [GitHub](https://github.com/MohammedError)
