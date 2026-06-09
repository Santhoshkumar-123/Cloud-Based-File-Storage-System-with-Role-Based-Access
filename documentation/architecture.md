# System Architecture

## Overview

The Serverless File Storage System is built using AWS serverless services.  
It allows users to upload, download, and manage files securely using role-based access control.

## Architecture Components

### Frontend
- Built using **React**
- Provides user interface for file upload, download, and history tracking
- Communicates with backend through **API Gateway**

### API Gateway
- Acts as the entry point for all client requests
- Routes requests to appropriate AWS Lambda functions
- Secured using **Amazon Cognito Authorizer**

### AWS Lambda
Implements backend logic for the application.

Lambda functions used:
- Upload File
- List Files
- Download File
- Delete File
- Get Download History

### Amazon S3
- Stores uploaded files
- Files are uploaded using **presigned URLs**
- Prevents direct public access to the bucket

### Amazon DynamoDB
Stores metadata and logs.

Tables used:
- **FileMetadata**
- **DownloadHistoryTable**

### Amazon Cognito
- Handles authentication
- Implements **Role-Based Access Control (RBAC)**

User Roles:
- Admin
- Editor
- Viewer

## Security Architecture

### Authentication
Users authenticate using Amazon Cognito.

### Authorization
Role-based access control enforced through Lambda functions.

| Role | Upload | Download | Delete | History |
|-----|------|------|------|------|
| Admin | Yes | Yes | Yes | Yes |
| Editor | Yes | Yes | No | Own |
| Viewer | No | Yes | No | Own |

### Data Protection
- HTTPS used for secure communication
- Files accessed using temporary presigned URLs
- S3 bucket access restricted through IAM policies