# Student Record Management API

## Description
Build an API for managing student records.

## Entities
- **Students**

## Endpoints
- **GET /students**: Fetch all student records.
- **GET /students/{id}**: Fetch a student by their ID.
- **POST /students**: Add a new student.
- **PATCH /students/{id}**: Update some details about a student (e.g., contact info).
- **PUT /students/{id}**: Completely update a student's information.
- **DELETE /students/{id}**: Remove a student record.

## Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the application**:
    ```sh
    uvicorn main:app --reload
    ```

6. **Access the API documentation**:
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation.