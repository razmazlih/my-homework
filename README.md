
# Project Name: File Processing System

This project is a system for uploading, processing, and tracking documents using Node.js, Python, and PostgreSQL. The system consists of three components:

1. **PostgreSQL Database**: Stores the uploaded documents and processed data.
2. **Node.js API**: Provides endpoints for uploading files and checking their processing status.
3. **Python Background Service**: Processes the uploaded documents by decoding and storing their data.

## Requirements

Before you begin, ensure that you have the following installed:

- Docker
- Docker Compose

## Setup

This project uses Docker and Docker Compose to manage the services. Follow the steps below to set up the environment.

### 1. Clone the repository

Clone the repository to your local machine.

```bash
git clone https://github.com/razmazlih/my-homework.git
cd my-homework
```

### 2. Configure Environment Variables

Create a `.env` file in the root of the project directory with the following content (make sure to replace the placeholder values):

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=db
DB_PORT=5432
```

### 3. Build and Run with Docker Compose

Run the following command to build and start the services:

```bash
docker-compose up --build
```

This will build the Docker images for the Node.js and Python services and start all the services defined in the `docker-compose.yml` file, including:

- `node_api`: Node.js API server running on port `3000`
- `python_service`: Python background service
- `db`: PostgreSQL database

### 4. Access the API

- The Node.js API will be accessible at `http://localhost:3000`.
- You can interact with the API using the following endpoints:

#### POST `/upload`
Uploads a file to the server and stores it in the `documents` table.

##### Request:
- Form data with the file to be uploaded under the key `file`.

##### Response:
- JSON with the `documentId` of the uploaded file.

#### GET `/status/:id`
Fetches the current processing status of a document.

##### Request:
- `id`: The ID of the document whose status you want to check.

##### Response:
- JSON with the `status` of the document (`uploaded`, `processing`, or `completed`).

### 5. Background Processing

The Python background service will automatically process uploaded documents. It periodically checks for documents with the status `uploaded`, decodes the document data, and inserts the processed data into the `processed_data` table.

The service is set to run continuously and can be stopped with `Ctrl+C`.

### 6. Stopping the Services

To stop the services, run:

```bash
docker-compose down
```

This will stop and remove all the containers but retain your data in the `db` volume.

## Database Schema

The database contains two tables:

1. **documents**:
    - `id`: The primary key for the document.
    - `filename`: The name of the uploaded file.
    - `upload_time`: Timestamp of when the file was uploaded.
    - `status`: The status of the document (`uploaded`, `processing`, `completed`).
    - `file_data`: The actual file data in binary format.

2. **processed_data**:
    - `id`: The primary key for processed data.
    - `document_id`: Foreign key referencing the `documents` table.
    - `column1`: The first data column from the document.
    - `column2`: The second data column from the document.
    - `created_at`: Timestamp of when the data was processed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
