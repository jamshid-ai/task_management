# Project Name

Task Management API.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

Instructions on how to install and set up the project.

1. Clone the repository:
    ```bash
    git clone git@github.com:jamshid-ai/task_management.git
    ```
2. Change to the project directory:
    ```bash
    cd task_management
    ```
3. Create a new virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
    - On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```
5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Create a `.env` file with the following variables:
    ```bash
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ELASTIC_URL=http://localhost:9200
    ELASTIC_USERNAME=elastic
    ELASTIC_PASSWORD=changeme
    ```
7. Run the project:
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

Instructions on how to use the project.

## Features

List of features and functionalities of your project.

## Contributing

Guidelines for contributing to your project.

## License

Information about the license under which your project is released.
