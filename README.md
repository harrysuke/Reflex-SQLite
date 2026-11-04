# Reflex-SQLite Application

A full-stack web application built using **Reflex** (a pure-Python web framework) and integrated with an **SQLite** database for seamless backend data persistence.

## Features
* **Pure Python Full-Stack**: Built entirely in Python, utilizing Reflex for both the responsive frontend UI and reactive state handling.
* **SQLite Database Integration**: Local-first relational database persistence for standard CRUD workflows.
* **REST API Endpoints**: Raw SQL query processing for robust backend database operations without ORM overhead.
* **File Uploads System**: Dedicated storage handling for files through an automated uploads system.

## Project Structure
```text
├── data/               # SQLite database storage directory
├── reflexsqlite/       # Core application source code and Reflex components
├── uploads/            # Target folder for user file uploads
└── README.md           # Project documentation
```

## Getting Started

### Prerequisites
* Python 3.10 or higher
* pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/harrysuke/Reflex-SQLite.git
   cd Reflex-SQLite
   ```
2. Install Reflex and required dependencies:
   ```bash
   pip install reflex
   ```
3. Initialize the Reflex project:
   ```bash
   reflex init
   ```

### Running the Application
To launch both the frontend development server and the backend API server simultaneously, run:
```bash
reflex run
```
OR
```bach
uv run reflex run
```

The application will automatically initialize the local SQLite database and spin up the web interface, typically accessible at `http://localhost:3000`.

## API Usage
The backend processes data workflows using high-performance raw SQL queries rather than traditional heavy object-relational mapping (ORM) setups. Database interactions can be modified inside the core state handlers or routed through backend script configs.
