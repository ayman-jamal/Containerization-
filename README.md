### Containerized Microservices Data Collection and Analytics System

[Watch the video on YouTube](https://youtu.be/6NIqXeBW9tc?si=26kTmOqhy3XHNaEw)

#### Overview
This project is a microservices-based system designed for data collection and analytics. It is built using Docker and Flask, with services containerized for scalability and ease of deployment. The system allows users to securely input data and view analytics, with a robust authentication mechanism. The data is stored in both MySQL and MongoDB databases, and analytics results are computed and displayed in real-time.

#### Features
- **Enter Data Service**: A web application where users can submit data after validating their credentials through the Authentication Service. Data is stored in a MySQL database.
- **Show Results Service**: A web application that displays analytics such as maximum, minimum, and average values. Data is retrieved from a MongoDB database after user authentication.
- **Authentication Service**: A microservice that validates user credentials and provides secure access to the system's features.
- **Analytics Service**: Retrieves data from the MySQL database, performs simple statistical analysis, and writes the results to MongoDB.

#### Technologies Used
- **Docker & Docker Compose**: For containerizing services and managing multi-container applications.
- **Flask**: Python web framework used to build the microservices.
- **MySQL**: Database for storing user credentials and data entries.
- **MongoDB**: Database for storing analytics results.
- **GitHub Actions**: CI/CD pipeline for building Docker images and pushing them to Docker Hub.

#### Project Structure
```
.
├── docker-compose.yml          # Compose file to define and run the multi-container Docker application
├── init.sql                    # SQL script for initializing MySQL database tables
├── Analytics                   # Microservice for performing data analysis
├── auth                        # Authentication service for validating users
├── enter_app                   # Web application for entering data
├── show_data                   # Web application for displaying results
└── README.md                   # Project documentation
```

#### CI/CD Pipeline
The project includes a CI/CD pipeline using GitHub Actions that automates:
- Building Docker images for each microservice
- Pushing the images to Docker Hub


4. Access the services:
   - Enter Data: `http://localhost:5000`
   - Show Results: `http://localhost:8000`

#### Future Improvements
- Implement role-based access control for enhanced security.
- Add more advanced analytics functionalities.
- Improve error handling and logging.
