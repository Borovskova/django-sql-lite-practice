# Django SQL-Lite Practice

A hands-on project built with Django, Python, and WebSockets, designed to demonstrate and educate on real-time web communication.

## 🌟 Goal: Education

This project serves as an educational resource to provide a practical example and playground for learning:

*   Integrating **WebSockets** into a Django application using Django Channels.
*   Handling real-time data flow between server and client.
*   Understanding core **Django** concepts and structure.
*   Exploring asynchronous programming patterns in a web context.
*   Utilizing **SQLite** as the default database backend for simplicity.

## ✨ Features

This project demonstrates the following key functionalities:

*   Basic Django web application setup with views and templates.
*   Establishment and management of WebSocket connections using Django Channels.
*   Receiving messages/data from the client via WebSocket.
*   Broadcasting messages/data from the server to all connected clients in real-time.


## 🚀 Technologies Used

*   **Python:** The core programming language.
*   **Django:** The high-level Python web framework.
*   **Django Channels:** Extends Django to handle WebSockets and other asynchronous protocols.
*   **WebSockets:** Enables two-way real-time communication.
*   **SQLite:** The default, file-based database.
*   HTML, CSS, JavaScript: For the user interface and client-side logic.

### Prerequisites

Make sure you have the following installed:

*   Python (3.6+)
*   pip
*   venv or virtualenv

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Borovskova/django-api.git
    cd django_api_education
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply Database Migrations:**

    ```bash
    python manage.py migrate
    ```

### Running the Application

1.  **Make sure your virtual environment is activated.**
2.  **Start the Django development server:**

    ```bash
    python manage.py runserver
    ```

3.  **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000/` to see the standard Django welcome page`.


## 📚 Learning Resources

*   Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
*   Django Channels Documentation: [https://channels.readthedocs.io/](https://channels.readthedocs.io/)
*   MDN Web Docs - WebSockets: [https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
