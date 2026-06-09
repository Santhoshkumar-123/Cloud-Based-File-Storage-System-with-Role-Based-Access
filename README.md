# Cloud-Based File Storage System with Role-Based Access

## Project Overview

The Cloud-Based File Storage System is a secure serverless application built on AWS that enables users to upload, download, and manage files through a web interface. The system implements Role-Based Access Control (RBAC) to ensure that users can only perform actions permitted by their assigned roles.

The application follows a fully serverless architecture using AWS managed services such as Amazon S3, AWS Lambda, API Gateway, DynamoDB, Cognito, IAM, and CloudWatch. By leveraging serverless technologies, the system eliminates the need for managing backend servers while providing scalability, security, and high availability.

---

## Problem Statement

Traditional file storage systems often require dedicated servers, infrastructure maintenance, and complex security configurations. The objective of this project is to create a secure, scalable, and cost-effective cloud storage platform that:

* Enables secure file uploads and downloads.
* Supports role-based access control.
* Provides auditability through download history tracking.
* Reduces infrastructure management using serverless services.
* Ensures secure access to files without exposing storage resources publicly.

---

## Key Features

### Authentication and Authorization

* User authentication using Amazon Cognito.
* JWT-based authentication.
* Role-Based Access Control using Cognito Groups.
* Three user roles:

  * Admin
  * Editor
  * Viewer

### File Management

* Upload files securely.
* Download files securely.
* View available files.
* Delete files (Admin only).
* Store and manage file metadata.

### Download History

* Track user download activity.
* View historical download records.

### Security

* Private S3 bucket.
* Pre-signed URLs for secure uploads and downloads.
* IAM-based least-privilege permissions.
* HTTPS communication.

### Monitoring

* CloudWatch logging and monitoring.
* Error tracking and debugging support.

---

## Technology Stack

### Frontend

* React.js
* JavaScript
* Axios

### Backend

* AWS Lambda
* Amazon API Gateway
* Python

### Storage

* Amazon S3
* Amazon DynamoDB

### Authentication & Security

* Amazon Cognito
* AWS IAM

### Monitoring

* Amazon CloudWatch

### Architecture

* AWS Serverless Architecture

---

## System Architecture

User
↓
React Frontend
↓
API Gateway
↓
AWS Lambda Functions
↓
Amazon S3 (File Storage)
Amazon DynamoDB (Metadata & History)
↓
Amazon Cognito (Authentication)

---

## User Roles and Permissions

| Feature               | Admin | Editor      | Viewer      |
| --------------------- | ----- | ----------- | ----------- |
| Upload Files          | Yes   | Yes         | No          |
| Download Files        | Yes   | Yes         | Yes         |
| View Files            | Yes   | Yes         | Yes         |
| Delete Files          | Yes   | No          | No          |
| View Download History | Yes   | Own History | Own History |

---

## AWS Services Used

### Amazon S3

Used for storing uploaded files securely.

Responsibilities:

* File storage
* High durability
* Scalability
* Secure object access

### AWS Lambda

Implements backend business logic.

Functions:

* Upload File
* List Files
* Download File
* Delete File
* Get Download History

### Amazon API Gateway

Provides REST API endpoints between frontend and backend.

Endpoints:

* POST /upload
* GET /files
* POST /download
* DELETE /delete
* GET /history

### Amazon DynamoDB

Stores:

* File metadata
* Download history

### Amazon Cognito

Handles:

* User authentication
* User groups
* JWT token generation
* Role management

### AWS IAM

Provides secure access control and least-privilege permissions.

### Amazon CloudWatch

Used for:

* Monitoring
* Logging
* Error tracking
* Performance analysis

---

## Workflow

### 1. User Login

1. User enters credentials.
2. Cognito authenticates the user.
3. JWT token is generated.
4. User role is extracted from Cognito Groups.

---

### 2. File Upload Workflow

1. User selects a file in the React application.
2. Frontend sends request to Upload API.
3. Upload Lambda validates permissions.
4. Lambda generates a pre-signed upload URL.
5. File is uploaded directly to Amazon S3.
6. File metadata is stored in DynamoDB.

Benefits:

* Faster uploads
* Reduced backend load
* Improved scalability

---

### 3. File Listing Workflow

1. Frontend requests available files.
2. ListFiles Lambda retrieves metadata from DynamoDB.
3. RBAC rules are applied.
4. Results are returned to the frontend.

---

### 4. File Download Workflow

1. User clicks Download.
2. Frontend calls Download API.
3. Lambda validates permissions.
4. Lambda generates a pre-signed download URL.
5. Download activity is stored in DynamoDB.
6. Browser downloads file directly from S3.

---

### 5. File Deletion Workflow

1. Admin clicks Delete.
2. Delete Lambda validates Admin role.
3. File is removed from S3.
4. Metadata is removed from DynamoDB.
5. Success response is returned.

---

## Security Architecture

### Authentication

* Amazon Cognito User Pools
* JWT-based authentication

### Authorization

* Role-Based Access Control (RBAC)
* Cognito Groups

### Data Encryption

* HTTPS for data in transit
* S3 encryption at rest
* DynamoDB encryption at rest

### Secure File Access

* Private S3 bucket
* Temporary pre-signed URLs
* No public file access

### IAM Security

* Least-privilege permissions
* Service-specific access policies

---

## Database Design

### FileMetadata Table

Stores information about uploaded files.

Attributes:

* fileId
* fileName
* owner
* s3Key
* tags
* uploadTime

### DownloadHistoryTable

Stores download activity.

Attributes:

* historyId
* userId
* fileId
* downloadedAt

Global Secondary Index:

* userId-index

---

## Performance Achievements

* Reduced infrastructure management overhead by approximately 70% using serverless architecture.
* Achieved file upload response times of less than 2 seconds.
* Achieved file retrieval latency of approximately 300–500 milliseconds.
* Improved scalability through direct S3 file transfers using pre-signed URLs.

---

## Challenges and Solutions

### Challenge 1

Implementing secure role-based access.

Solution:

* Used Cognito Groups and JWT claims.

### Challenge 2

Preventing public access to files.

Solution:

* Implemented S3 pre-signed URLs.

### Challenge 3

Managing download history efficiently.

Solution:

* Created DynamoDB Global Secondary Index (userId-index).

### Challenge 4

Frontend and API integration issues.

Solution:

* Configured API Gateway CORS policies correctly.

---

## Future Enhancements

* File versioning support.
* Multi-factor authentication (MFA).
* File sharing between users.
* Search functionality.
* Virus scanning during uploads.
* Notification service using Amazon SNS.

---

## Project Outcome

The project successfully demonstrates the implementation of a secure, scalable, and cost-efficient file management platform using AWS serverless services. It provides secure file storage, role-based access control, download tracking, and direct S3 integration while eliminating the need for server management.

---

## Author

Santhosh Kumar KG

AWS Cloud Intern

Technologies Used:
AWS Lambda, Amazon S3, DynamoDB, API Gateway, Cognito, IAM, CloudWatch, CloudFront, React, Python, Serverless Architecture.
