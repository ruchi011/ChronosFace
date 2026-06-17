# ChronosFace AI
## Smart Face Recognition Attendance and Workforce Management System
### Project Description
ChronosFace AI is an intelligent face recognition-based attendance and workforce management system developed using Python, Artificial Intelligence, Computer Vision, and Machine Learning technologies.
The system automates attendance tracking by recognizing employees through facial biometrics instead of traditional methods such as manual registers, RFID cards, or fingerprint scanners.
ChronosFace AI not only marks attendance automatically but also provides advanced security through liveness detection, anti-spoofing mechanisms, visitor management, payroll management, employee management, attendance analytics, and email-based alert systems.
The project is designed to improve organizational productivity, reduce attendance fraud, and provide a secure and centralized workforce management solution.

# Problem Statement
Traditional attendance systems suffer from multiple problems:
* Proxy attendance
* Manual errors
* Time-consuming attendance marking
* Lack of security
* Poor employee tracking
* No real-time monitoring
ChronosFace AI solves these issues by using AI-powered facial recognition and liveness verification techniques.

# Objectives
The major objectives of ChronosFace AI are:
* Automate attendance marking.
* Eliminate proxy attendance.
* Improve organizational security.
* Maintain employee records digitally.
* Manage visitors effectively.
* Generate attendance reports automatically.
* Generate payroll and payslips.
* Provide role-based dashboards.
---
# Technology Stack
## Programming Language
* Python 3.x
Python is used as the primary development language because of its rich AI, Machine Learning, and Computer Vision ecosystem.
---
## Database
### SQLite
Used for:
* Employee Records
* Attendance Records
* Visitor Records
* Login Credentials
* Leave Management
* Payroll Information
Advantages:
* Lightweight
* Fast
* No separate server required
* Easy integration with Python
---
## GUI Framework
### CustomTkinter
Used for:
* Modern User Interface
* Dashboards
* Forms
* Attendance Screens
* Visitor Management
Provides a professional appearance compared to traditional Tkinter.

## Backend Framework

### Flask

Flask is used to implement a lightweight REST API layer that enables communication between client dashboards and the centralized attendance server.
---
# System Architecture

```text
+-------------------+
| Admin Dashboard   |
+-------------------+
          |
+-------------------+
| HR Dashboard      |
+-------------------+
          |
+-------------------+
| Employee Dashboard|
+-------------------+
          |
          v
+-------------------+
| Flask REST API    |
+-------------------+
          |
          v
+-------------------+
| SQLite Database   |
+-------------------+
          |
          v
+-------------------+
| Reports | Logs    |
| Payroll | Alerts  |
+-------------------+
```

# APIs and Libraries Used
ChronosFace follows a Client-Server Architecture using Flask REST APIs. The GUI dashboards communicate with the Flask server through HTTP requests, and all data is stored and retrieved from SQLite.
---

## 1. OpenCV API
Library:
```python
import cv2
```
Purpose:
* Webcam Access
* Image Capture
* Real-Time Video Streaming
* Image Processing
* Face Detection

Features Implemented:
* Employee Face Capture
* Visitor Face Capture
* Live Camera Feed
* Face Region Extraction

Workflow:
1. Camera captures live video.
2. Frames are processed continuously.
3. Face regions are extracted.
4. Images are stored for training.

---

## 2. InsightFace API
Library:
```python
from insightface.app import FaceAnalysis
```
Purpose:
* Face Detection
* Face Embedding Extraction
* Face Recognition

Why InsightFace?
Traditional face recognition compares images directly.
InsightFace converts each face into a 512-dimensional numerical vector called an embedding.
Example:
Employee Face:
[0.125, 0.847, 0.541, ...]
Live Face:
[0.124, 0.850, 0.537, ...]
The system compares these vectors and calculates similarity.

Advantages:
* High Accuracy
* Fast Recognition
* Robust Performance
---
## 3. MediaPipe Face Mesh API
Library:
```python
import mediapipe as mp
```
Purpose:
* Liveness Detection
* Eye Blink Detection
* Smile Detection
* Head Movement Verification
Features:
### Blink Detection

The system calculates Eye Aspect Ratio (EAR).

- Eyes Closed → EAR decreases
- Eyes Open → EAR increases

The system verifies real human presence.
---
### Smile Detection

The system measures mouth opening and facial expressions.

- Smile detected → Verification passed
- No smile detected → Verification failed

Purpose:
To ensure that the detected face belongs to a real person and not a static image.
---

### Head Movement Verification

The system generates a random movement challenge.

Possible challenges:

- Turn Left
- Turn Right
- Look Up
- Look Down

Verification Process:

1. Challenge is displayed.
2. User performs the requested movement.
3. System validates the movement.
4. Verification is completed.

Purpose:
Prevents spoofing attacks using printed photographs.
---
## 4. NumPy API
Library:
```python
import numpy as np
```
Purpose:
* Matrix Operations
* Numerical Computation
* Embedding Processing
Used in:
* Face Embedding Calculations
* FFT Analysis
* Similarity Calculations
---
## 5. SciPy API
Library:
```python
from scipy.spatial.distance import cosine
```
Purpose:
* Cosine Similarity Calculation
Formula:
Similarity = 1 - Cosine Distance
Used to compare:
Stored Employee Embedding
with
Live Camera Embedding
Higher similarity indicates a match.
---
## 6. SMTP Email API
Library:
```python
import smtplib
```
Purpose:
* Send Alert Emails
* Unknown Face Notifications
* Employee Registration Emails
Example:
When an unknown person appears:
1. Image is captured.
2. Stored in unknown_faces folder.
3. Email alert is sent automatically.
---
## 7. ReportLab API
Library:
```python
from reportlab.platypus import SimpleDocTemplate
```
Purpose:
* PDF Payslip Generation
Features:
* Employee Salary Details
* Attendance Information
* Deductions
* Overtime Calculations
Generated Output:
Employee_Payslip.pdf
---
# REST APIs

| Function | Endpoint |
|-----------|-----------|
| Employee Registration | POST /api/biometric/register |
| Employee Verification | POST /api/biometric/verify |
| Clock In | POST /api/attendance/clockin |
| Clock Out | POST /api/attendance/clockout |
| Start Break | POST /api/attendance/startbreak |
| End Break | POST /api/attendance/endbreak |
| Apply Leave | POST /api/leave/apply |
| View Logs | GET /api/logs |
| View Employees | GET /api/employees |
# Machine Learning Concepts Used
## Face Embeddings
Instead of storing raw images, the system stores embeddings.
Embedding:
Mathematical representation of a face.
Generated using:
InsightFace Model
Stored in:
face_embeddings.pkl
Advantages:
* Faster Recognition
* Lower Storage Requirements
* Better Accuracy.
---
## Cosine Similarity
Used to compare embeddings.
Range:
0 → Completely Different
1 → Exact Match
Threshold:0.70+
Recognition accepted.
---
# Security Features
## Liveness Detection
Prevents:
* Photo Attacks
* Mobile Screen Attacks
* Printed Image Attacks.
Techniques:
* Blink Verification
* Smile Verification
* Head Movement Verification
---
## Screen Spoof Detection

The system uses FFT (Fast Fourier Transform) analysis to identify digital screen artifacts.

Detects:

- Mobile Screens
- Laptop Screens
- Tablet Displays
- Printed Images

If spoofing is detected:

- Authentication is denied.
- Attendance is not recorded.

Purpose:
Prevents unauthorized access using images displayed on electronic devices.
---
## Replay Attack Detection

The system continuously monitors facial motion patterns.

Detection Logic:

- Natural face movements are expected.
- Unnaturally static faces are flagged.
- Replayed videos or screen recordings are detected.

If a replay attack is detected:

- Access is blocked.
- Attendance is not marked.
- Security alert can be generated.

Purpose:
Protects the system against video replay attacks and recorded face presentations.
---
# Project Modules
## Admin Module
Functions:
* Add Employee
* Modify Employee
* Delete Employee
* View Attendance
* Visitor Management
* Payroll Management
* Reports
---
## HR Module

Functions:

* Employee Monitoring
* Attendance Monitoring
* Leave Management
* Payroll Management

### Leave Management

* Apply Leave
* Approve Leave
* Reject Leave
* Leave Status Tracking
* Email Notification System
## Employee Module
Functions:
* Login
* View Attendance
* Clock In
* Start Break
* End Break
* Clock Out
* Apply Leave
* View Leave Status
* View Profile
* Change Password
---
## Visitor Management Module
Functions:
* Visitor Registration
* Visitor Check-In
* Visitor Check-Out
* Whitelist Management
* Blacklist Management
---
## Payroll Module
Functions:
* Salary Processing
* PDF Payslip Generation
---
# Attendance Workflow
1. Employee Registration
2. Face Dataset Capture
3. Embedding Generation
4. Live Camera Recognition
5. Liveness Verification
6. Cosine Similarity Matching
7. Attendance Marked Automatically
8. Break Tracking
9. Clock Out Processing
10. Working Hours Calculation
11. Attendance Log Generation
12. Attendance Report Generation
----
# Application Workflow and Functionalities

## ChronosFace AI Execution Flow

### Method 1: Attendance Marking System

The Face Recognition Attendance System can be started directly by executing:

```bash
python recognize.py
```

### Functionality

The system activates the webcam and continuously captures live video frames.
The following operations are performed:
1. Face Detection using InsightFace.
2. Liveness Detection using:
   * Blink Detection
   * Smile Detection
   * Head Movement Verification
3. Anti-Spoofing Verification:
   * Screen Spoof Detection
   * Replay Attack Detection
4. Face Embedding Extraction.
5. Cosine Similarity Matching with stored employee embeddings.
6. Employee Identification.
7. Automatic Attendance Marking.
8. Attendance Record Storage in SQLite Database.
9. Unknown Face Detection and Storage.
10. Email Alert Generation for unauthorized persons.
### Features
* Real-Time Face Recognition
* Automatic Attendance Marking
* Blink Verification
* Smile Verification
* Head Movement Challenge
* Anti-Spoofing Protection
* Unknown Face Monitoring
* Email Alerts
---
## Method 2: Complete Application Workflow
The complete application starts by running:
```bash
python login.py
```
### Login Window
The Login Window serves as the main entry point of the application.
The user is presented with three options:
1. Admin Login
2. HR Login
3. Employee Login
The user selects the appropriate role and enters credentials.
---
# Admin Module
### Access
Admin Login → Admin Dashboard
### Functionalities
The Admin Dashboard provides complete control over the system.
#### Employee Management
* Add Employees
* Modify Employee Details
* Delete Employees
* Search Employees
#### Face Recognition Management
* Capture Employee Dataset
* Generate Face Embeddings
* Train Recognition System
#### Attendance Management
* View Attendance Records
* Generate Attendance Reports
* Monitor Employee Activity
#### Visitor Management
* Visitor Registration
* Visitor Tracking
* Visitor Reports
* Visitor Whitelist
* Visitor Blacklist
#### Payroll Management
* Salary Management
* Payslip Generation
* Payroll Reports
#### Department Management
* Create Departments
* Manage Employee Groups
### Admin Features
* Complete System Control
* Attendance Monitoring
* Employee Monitoring
* Visitor Monitoring
* Payroll Processing
* Report Generation
---
# HR Module
### Access
HR Login → HR Dashboard
### Functionalities
The HR Dashboard focuses on employee administration and attendance monitoring.
#### Employee Operations
* View Employee Information
* Search Employee Records
* Update Employee Information
#### Attendance Operations
* View Attendance Reports
* Monitor Attendance Status
* Export Attendance Data
#### Payroll Operations
* Generate Payslips
* Process Salary Information
### HR Features
* Employee Monitoring
* Attendance Monitoring
* Payroll Support
* Report Generation
---
# Employee Module
### Access
Employee Login → Employee Dashboard
### Functionalities
Employees can access their personal information and attendance records.
#### Profile Management
* View Profile Information
* View Employee Details
#### Attendance Management
* View Attendance History
* Check Attendance Status
* Monitor Working Hours
#### Account Management
* Change Password
* Update Personal Information
### Employee Features
* Self-Service Dashboard
* Attendance Tracking
* Profile Management
* Password Management
---
# Face Recognition Workflow
Step 1:
Employee Face Images are captured using:
```bash
python capture_dataset.py
```
Step 2:
Face Embeddings are generated using:
```bash
python generate_embeddings.py
```
Step 3:
Embeddings are stored inside:
```text
embeddings/face_embeddings.pkl
```
Step 4:
Live Face Recognition starts through:
```bash
python recognize.py
```
Step 5:
Liveness Detection is performed.
Step 6:
Face Matching is performed using Cosine Similarity.
Step 7:
Attendance is marked automatically.
Step 8:
Attendance records are stored in SQLite Database.

# Database Storage
The application stores information in SQLite database:
```text
database/chronosface.db
```
Stored Data:
* Employee Information
* Attendance records 
* Visitor records
* Department Information
* Login Credentials
* Payroll Information

---
# Key Features of ChronosFace AI
* Face Recognition Attendance
* Employee Management
* Attendance Management
* Break Tracking System
* Leave Management
* Leave Approval/Rejection Workflow
* Visitor Management
* Visitor Check-In / Check-Out
* Whitelist / Blacklist Management
* Payroll Management
* PDF Payslip Generation
* Attendance Analytics
* Attendance Reports Export
* Employee Search
* API Logging System
* Email Notification System
* Liveness Detection
* Anti-Spoofing Protection
* Unknown Face Detection
* Role-Based Access Control
* Admin Dashboard
* HR Dashboard
* Employee Dashboard
* Flask REST API Integration
* SQLite Database Integration


# Data Storage, Reports and Generated Files

## Attendance Records

```text
attendance/attendance.csv
```

**Purpose**

Stores employee attendance records.

Information Stored:
Employee ID
Employee Name
Date
Login Time
Logout Time
Attendance Status
Working Hours

Usage:
Whenever an employee is successfully recognized and passes liveness verification, the attendance information is automatically recorded in attendance.csv.

**Benefits**

- Attendance Tracking
- Attendance History Management
- Report Generation
- Employee Activity Monitoring

## Attendance Reports: 
attendance/reports/

**Purpose**
This folder stores automatically generated attendance reports.

Generated Files:
Example:
attendance_report_20260521_200830.csv
attendance_report_20260522_130201.csv

Contents:
Employee Attendance Summary
Daily Attendance Statistics
Login/Logout Information
Working Hours Information

Usage:
Administrators and HR personnel can generate reports for attendance analysis and record keeping.

---
## Employee Database

```text
database/chronosface.db
```

**Purpose**
Main SQLite database used by the application.

**Stored Information**

- Employee ID
- Employee Name
- Department
- Email
- Password.

Attendance Table:
-Attendance Details,
-Login Time,
-Logout Time,
-Attendance Status.

Visitor Table:

-Visitor Information,
-Visitor Entry Details.

Department Table
-Department Names,
-Employee Group Information

Benefits:
Centralized Data Storage,
Fast Data Retrieval,
Secure Record Management.

---
## Employee Face Dataset

```text
dataset/
└── Employee_Name/
    ├── image1.jpg
    ├── image2.jpg
    └── image3.jpg
```

**Purpose**
Stores captured employee face images.

Workflow:
Employee Registration
Face Capture
Dataset Storage
Embedding Generation.

---
## Face Embeddings

```text
embeddings/face_embeddings.pkl
```

**Purpose**
Stores generated face embeddings.

Example:
Employee Face
512-Dimensional Embedding Vector
Stored in face_embeddings.pkl

Usage:
Used during recognition for matching live faces with registered employees.

Benefits:
Faster Recognition,
Better Accuracy,
Reduced Processing Time.

---
## Unknown Face Records

```text
unknown_faces/
```

**Purpose**
Stores images of unrecognized persons.

Example:
unknown_20260601_103322.jpg

Usage:
When a face is detected but not recognized:

Image is captured.
Stored in unknown_faces folder.
Email alert can be generated.
Admin can review suspicious activity.

Benefits:
Security Monitoring,
Unauthorized Access Detection,
Audit Trail Creation.

---
## Visitor Face Records

```text
visitor_faces/
```
**Purpose**
Stores visitor photographs.

Information:
Visitor Photos
Visitor Registration Images

Usage:
Used for visitor identification and visitor management.

Benefits:
Visitor Tracking,
Visitor Verification,
Entry Monitoring.

---
## Payslip Records

```text
payslips/
```

**Purpose**
Stores generated PDF payslips.

Generated File Example:1040_payslip.pdf
Contents:
Employee Details,
Salary Information,
Deductions,
Net Salary,
Payroll Summary.

Usage:Generated through Payroll Module.

Benefits:
Automated Salary Documentation,
Employee Salary Records.

---
# Future Enhancements
* Cloud Database Integration
* Mobile Application
* Web Dashboard
* Multi-Camera Recognition
* AI Attendance Analytics
* Face Mask Recognition
* GPS Integration

---

# Developer

Madichetty Sai Ruchitha

## Project Domain

- Artificial Intelligence (AI)
- Computer Vision
- Face Recognition
- Attendance Management
- Workforce Management System

## Repository

[ChronosFace Repository](https://github.com/ruchi011/ChronosFace)