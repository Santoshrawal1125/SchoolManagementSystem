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

---

### Tips

- Tokens are automatically refreshed using the **Refresh Token** request.  
- Use the **Register User** request to add new users if your role permits.  
- Feel free to explore and modify requests in the collection as needed.

---

