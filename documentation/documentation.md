# Serverless File Storage System on AWS

## 1. Project Overview
The Serverless File Storage System is a cloud-based application built using AWS serverless services that enables users to securely upload, manage, download, and track files. The system implements Role-Based Access Control (RBAC) to enforce permissions for different user roles such as Admin, Editor, and Viewer.

The application leverages AWS managed services including Amazon API Gateway, AWS Lambda, Amazon S3, Amazon DynamoDB, and Amazon Cognito to build a scalable, secure, and cost-efficient file management solution.

Files are stored securely in Amazon S3 and accessed through temporary presigned URLs, ensuring that files cannot be accessed directly without proper authorization.

---

## 2. System Architecture
The system follows a serverless architecture where the frontend communicates with backend services through API Gateway.

Architecture Flow:

Frontend (React Application)  
↓  
Amazon API Gateway (REST API)  
↓  
AWS Lambda Functions (Business Logic)  
↓  
Amazon S3 (File Storage)  
Amazon DynamoDB (Metadata & Download History)  
↓  
Amazon Cognito (Authentication & Role Management)

---

## 3. Architecture Components

### 3.1 Frontend (React)
The frontend application provides the user interface for interacting with the file management system.

Features include:
- User login through Cognito
- File upload interface
- File listing and download functionality
- Download history viewing
- Admin file deletion

The frontend communicates with backend APIs using HTTP requests through API Gateway.

---

### 3.2 Amazon API Gateway
API Gateway acts as the entry point for all client requests.

Responsibilities:
- Exposes REST API endpoints
- Routes requests to AWS Lambda functions
- Integrates with Cognito for authentication
- Handles CORS configuration

Example API endpoints:

| Endpoint | Method | Description |
|---------|--------|-------------|
| /upload | POST | Generate upload URL |
| /files | GET | List available files |
| /download | POST | Generate download URL |
| /delete | DELETE | Delete file (Admin only) |
| /history | GET | Get download history |

---

### 3.3 AWS Lambda
Lambda functions implement the backend logic of the system.

Functions used in the project:

Upload Lambda
- Generates a presigned upload URL
- Stores file metadata in DynamoDB

List Files Lambda
- Retrieves file metadata from DynamoDB
- Applies RBAC filtering rules

Download Lambda
- Generates presigned download URLs
- Logs download activity in DynamoDB

Delete Lambda
- Deletes file from S3
- Removes metadata from DynamoDB
- Accessible only to Admin users

Get Download History Lambda
- Retrieves download history records for the logged-in user

---

### 3.4 Amazon S3
Amazon S3 is used to store uploaded files securely.

Key features:
- Files stored in private bucket
- Direct upload using presigned URLs
- Temporary access for downloads
- No public access allowed

Example file path structure:
users/{userId}/{filename}

---

### 3.5 Amazon DynamoDB

Two DynamoDB tables are used.

FileMetadata Table

| Attribute | Description |
|----------|-------------|
| fileId | Unique file identifier |
| fileName | Name of the uploaded file |
| owner | User who uploaded the file |
| s3Key | File path in S3 |
| tags | File tags |
| uploadTime | Upload timestamp |

DownloadHistoryTable

| Attribute | Description |
|----------|-------------|
| historyId | Unique record ID |
| userId | User who downloaded the file |
| fileId | File downloaded |
| downloadedAt | Download timestamp |

A Global Secondary Index (GSI) is created:

Index Name: userId-index  
Partition Key: userId  

This allows querying download history per user.

---

### 3.6 Amazon Cognito
Amazon Cognito is used for authentication and user management.

Features:
- User login and authentication
- JWT token generation
- User group management
- Integration with API Gateway

Three user roles are defined:

Admin  
Editor  
Viewer  

These roles are stored inside JWT tokens and used by Lambda functions to enforce access control.

---

## 4. Security Architecture

The system implements multiple security mechanisms to protect user data and resources.

### 4.1 Authentication
User authentication is handled by Amazon Cognito.

Users must log in before accessing any functionality.

After login, Cognito generates a JWT token which is sent in the Authorization header for all API requests.

---

### 4.2 Authorization (RBAC)

Role-Based Access Control ensures that each user only performs allowed actions.

| Role | Upload | Download | View Files | Delete | History |
|------|--------|----------|------------|--------|---------|
| Admin | Yes | Yes | All | Yes | All |
| Editor | Yes | Yes | All | No | Own |
| Viewer | No | Yes | All | No | Own |

RBAC rules are enforced inside Lambda functions using Cognito group claims.

---

### 4.3 Data Encryption

Encryption in Transit

All communications between the frontend and backend occur through HTTPS.

API Gateway ensures TLS encryption.

Encryption at Rest

Data stored in AWS services is encrypted:
- Amazon S3 uses Server-Side Encryption
- DynamoDB provides automatic encryption at rest

---

### 4.4 Secure File Access

Files are never publicly accessible.

Instead, access is granted through temporary presigned URLs.

These URLs:
- Are valid for a short duration (typically 5 minutes)
- Allow temporary access to specific files

This prevents unauthorized access to the S3 bucket.

---

### 4.5 IAM Role-Based Security

Each Lambda function is assigned an IAM role with minimal permissions.

Examples:

Upload Lambda permissions:
- s3:PutObject
- dynamodb:PutItem

Download Lambda permissions:
- s3:GetObject
- dynamodb:GetItem
- dynamodb:PutItem

Delete Lambda permissions:
- s3:DeleteObject
- dynamodb:DeleteItem

This follows the Principle of Least Privilege.

---

## 5. Deployment Guide

Step 1: Create Cognito User Pool
1. Open AWS Cognito
2. Create a new User Pool
3. Create user groups:
   - Admin
   - Editor
   - Viewer
4. Create an App Client

---

Step 2: Create DynamoDB Tables

FileMetadata  
Partition Key: fileId

DownloadHistoryTable  
Partition Key: historyId

Create Global Secondary Index:

Index Name: userId-index  
Partition Key: userId

---

Step 3: Create S3 Bucket

Create a bucket named:

cloud-file-storage-bucket-teamb

Enable:
- Block Public Access
- Server-side encryption

---

Step 4: Deploy Lambda Functions

Create the following Lambda functions:

UploadFile  
ListFiles  
DownloadFile  
DeleteFile  
GetDownloadHistory  

Attach proper IAM permissions.

---

Step 5: Configure API Gateway

Create REST API resources:

| Endpoint | Method |
|----------|--------|
| /upload | POST |
| /files | GET |
| /download | POST |
| /delete | DELETE |
| /history | GET |

Attach Cognito Authorizer.

Enable CORS for all resources.

Deploy the API.

---

Step 6: Run Frontend

Install dependencies:

npm install

Start the application:

npm start

Application runs at:

http://localhost:3000

---

## 6. Project Outcome

The system successfully provides a secure and scalable file storage platform using AWS serverless services.

Key achievements:
- Secure authentication with Amazon Cognito
- Role-Based Access Control implementation
- File upload and download using presigned URLs
- Download history logging
- Serverless architecture for scalability
- Secure file storage with Amazon S3

This architecture eliminates server management while maintaining security, scalability, and reliability.