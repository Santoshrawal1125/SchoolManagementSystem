# School Management Backend API

---

## Project Overview

This project is a backend API for managing schools, departments, classrooms, staff, and students with role-based authentication and authorization.  
It is built using Django and Django REST Framework (DRF) with JWT token authentication.

### Key Features

- User roles: SuperAdmin, SchoolAdmin, DepartmentHead, Staff, Student  
- Role-based access control on API endpoints  
- JWT authentication for secure API access  
- CRUD operations for schools, departments, classrooms, staff, and students  
- Seed command to pre-populate the database with sample data for easy testing  

---

## Application Flow

This describes how different users interact with the system and what APIs they typically use:

### SuperAdmin

- Logs in and obtains an access token.  
- Creates Schools and assigns SchoolAdmins to each school.  
- Has full control over schools (CRUD operations).  

### SchoolAdmin

- Logs in using their credentials.  
- Manages their assigned school only.  
- Creates Departments and Classrooms within their school.  
- Registers Staff and Students linked to their Departments and Classrooms.  
- Creates DepartmentHeads for each Department.  

### DepartmentHead

- Logs in and views only the Staff members within their own Department.  
- Cannot modify data but can view staff details relevant to their department.  

### Staff

- Logs in and views their own profile.  

### Student

- Logs in and views their own profile.  

---

## Installation & Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/Santoshrawal1125/SchoolManagementSystem.git
    cd SchoolManagementSystem
    ```

2. **Create and activate a virtual environment**

    ```bash
    python -m venv venv
    ```

    - On Linux/macOS:

      ```bash
      source venv/bin/activate
      ```

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Seed Initial Data**  
   (Creating every user, school, and department manually takes time — this command creates everything for you to test)

    ```bash
    python manage.py seed_data
    ```

    This will create:

    - 1 SuperAdmin (`username: superadmin`, `password: admin123`)  
    - 2 SchoolAdmins (`schooladmin1` and `schooladmin2`, both with password `admin123`)  
    - 2 Departments per school  
    - 2 Classrooms per school  
    - 2 Staff members per department  
    - 2 Students per classroom  

    This seeded data allows easy testing of all roles and features without manual setup.

6. **Run the development server**

    ```bash
    python manage.py runserver
    ```

---

## Testing with Postman

To make testing easier, this project includes:

- `SchoolManagement.postman_collection.json` — Pre-configured API requests  
- `SchoolManagement.postman_environment.json` — Environment variables with URLs and token placeholders  

### How to use Postman files
   The json file to import is inside the project.
1. **Import the Postman collection**

    - Open Postman and click **File > Import**  
    - Select the `SchoolManagement.postman_collection.json` file  
    - This loads all pre-made API requests into Postman.

2. **Import the Postman environment**

    - Again, click **File > Import**  
    - Select the `SchoolManagement.postman_environment.json` file  
    - This creates an environment named **SchoolManagement Env** with variables like `base_url` and token placeholders.

3. **Select the environment**

    - At the top-right in Postman, choose **SchoolManagement Env** from the environment dropdown.

4. **Use and test API endpoints**

    - You can now test endpoints like `/schools/`, `/departments/`, `/staff/` based on your logged-in user role.  
    - **Important:** Make sure to include the trailing slash (`/`) at the end of each endpoint URL in Postman (e.g., `/schools/`, `/register/`). Omitting the trailing slash may cause a "404 Not Found" or other errors because Django’s default URL patterns expect it.

---

### Tips

- Tokens are automatically refreshed using the **Refresh Token** request.  
- Use the **Register User** request to add new users if your role permits.  
- Feel free to explore and modify requests in the collection as needed.

---

## API Documentation (Swagger UI)

For the easiness of testing i have made short urls which are accesed from who is logged in like schooladmin if logged in can acess its schools data so they might not be clear soe please have a  good look.

This project also includes **Swagger UI** for interactive API documentation and testing.

- After running the development server (`python manage.py runserver`), open your browser and visit:
http://127.0.0.1:8000/swagger/

- The Swagger UI lists all available endpoints with detailed info on methods, request parameters, and response schemas.

- You can directly try out **GET** requests and some **POST** requests in Swagger.

- Note: Some POST endpoints might require additional setup or data in the request body because we are not using ModelViewSets for all views.

---


## 🔹 Note on API Endpoint Design

To simplify testing and enhance developer experience, this project uses **shortened, role-aware endpoints** that automatically return data scoped to the currently authenticated user.

### Examples:

- `/api/departments/` → returns departments **belonging to the logged-in SchoolAdmin's school (Make sure you are logged in with schooladmin)**
- `/api/staff/` → returns staff based on whether the user is a **SchoolAdmin** (school-level) or **DepartmentHead** (department-level)
- `/api/students/` → returns students associated with the **user's school**

This design reduces the need to pass user-specific filters or query parameters in most cases and allows **easy testing using tools like Postman**.

✅ These APIs can be extended into full **RESTful nested routes** (e.g., `/api/schools/{id}/departments/`) for production environments.  
However, this simplified structure was intentionally chosen to:

- Reduce complexity during testing or evaluation
- Support fast and context-aware data access
- Clearly demonstrate role-based authorization behavior

If you prefer REST-style nested routing, the project is modular and can be easily extended to support it.

Feel free to reach out if you need help with running or testing the project!


