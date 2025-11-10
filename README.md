
# El Rincón del Gordo

"El Rincón del Gordo" is a complete and functional web application for a fictitious restaurant. This project includes user management, product administration, and a clean and organized structure that separates responsibilities.

## Features

-   **User Authentication**: Secure system for registration, login, and logout using password hashing.
-   **User Roles**: Two types of roles:
    -   **Administrator**: Has access to a control panel to manage users and products.
    -   **Client**: Can browse the application, view products, and manage their profile.
-   **Product Management (CRUD)**: Administrators can create, read, update, and delete restaurant products.
-   **User Management (CRUD)**: Administrators can create, read, update, and delete users.
-   **Administrator Dashboard**: A dashboard for administrators that displays statistics, such as the total number of users and products.
-   **Product Graphics**: A section that displays a bar chart with product prices.
-   **Contact Form**: A form for users to send messages.

## Project Structure

The project follows a modular structure that separates logic into different components:

```
/
├── app.py # Main application file
├── config.py # Application configuration (e.g., database)
├── Dockerfile # Docker configuration for deployment
├── requirements.txt # Project dependencies
├── src/ # Source code
│ ├── __init__.py # Application factory
│ ├── controllers/ # Route handlers
│ │ ├── AdminController.py # Admin routes
│ │ ├── homeController.py # Home routes
│ │ ├── LoginController.py # Authentication routes
│ │ ├── ProductosController.py # Product routes
│ │ └── UserController.py # User routes
│ ├── data/ # Database connection logic
│ │ └── mysqlConexion.py
│ ├── models/ # Data models
│ │ └── Users.py
│ └── Services/ # Business logic services
│ ├── CryptoService.py # Password hashing
│ └── UserServices.py # User-related logic
├── static/ # Static files (CSS, JS, images)
└── templates/ # HTML templates
```

## Technologies

-   **Backend**:
    -   **Framework**: Flask
    -   **Database**: MySQL
    -   **ORM**: Flask-MySQLdb
    -   **Password Hashing**: Werkzeug Security
-   **Frontend**:
    -   **Templating**: Jinja2
    -   **Styling**: CSS
    -   **JavaScript**: For interactive functionalities like modals and tooltips.
-   **Deployment**:
    -   **Containerization**: Docker

## Database

The application uses a MySQL database to store information about users and products. The connection is managed through `src/data/mysqlConexion.py`, which uses a connection pool to handle multiple requests efficiently.

The application uses stored procedures to interact with the database. The main procedures are:

-   `CrearUsuario`: Creates a new user.
-   `ActualizarUsuario`: Updates an existing user.
-   `EliminarUsuario`: Deletes a user.
-   `insertarProductos`: Adds a new product.
-   `actualizar_producto`: Updates an existing product.

## Installation and Usage

To run the project locally, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/tu-usuario/El-ricon-del-gordo.git
    cd El-ricon-del-gordo
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the database**:
    -   Make sure you have a MySQL server running.
    -   Create a database for the project.
    -   Set the database credentials in `config.py`.

5.  **Run the application**:
    ```bash
    python app.py
    ```

The application will be available at `http://localhost:8000`.

## Deployment

The project is configured to be deployed using Docker. To create a Docker image and run a container, follow these steps:

1.  **Build the Docker image**:
    ```bash
    docker build -t el-rincon-del-gordo .
    ```

2.  **Run the Docker container**:
    ```bash
    docker run -p 8000:8000 el-rincon-del-gordo
    ```

The application will be accessible at `http://localhost:8000`.

## Contributing

If you wish to contribute to the project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/new-feature`).
3.  Make your changes and commit them (`git commit -m 'Add new feature'`).
4.  Push your changes to the branch (`git push origin feature/new-feature`).
5.  Open a Pull Request.

## License

This project is under the MIT License. See the `LICENSE` file for more details.
