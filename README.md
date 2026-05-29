# ChronosFace AI
## Smart Face Recognition Attendance and Workforce Management System
### Project Description
ChronosFace AI is an intelligent face recognition-based attendance and workforce management system developed using Python, Artificial Intelligence, Computer Vision, and Machine Learning technologies.
The system automates attendance tracking by recognizing employees through facial biometrics instead of traditional methods such as manual registers, RFID cards, or fingerprint scanners.
ChronosFace AI not only marks attendance automatically but also provides advanced security through liveness detection, anti-spoofing mechanisms, visitor management, payroll management, employee management, attendance analytics, and email-based alert systems.
The project is designed to improve organizational productivity, reduce attendance fraud, and provide a secure and centralized workforce management solution.
---
# Problem Statement
Traditional attendance systems suffer from multiple problems:
* Proxy attendance
* Manual errors
* Time-consuming attendance marking
* Lack of security
* Poor employee tracking
* No real-time monitoring
ChronosFace AI solves these issues by using AI-powered facial recognition and liveness verification techniques.
---
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
---
# APIs and Libraries Used
Although ChronosFace is a desktop application and does not use REST APIs such as GET, POST, PUT, DELETE, it utilizes several powerful APIs and libraries.
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
When eyes close:
EAR decreases.
When eyes open:
EAR increases.
The system verifies real human presence.
---
### Smile Detection
The system measures mouth opening.
If the smile threshold is reached:
User passes the smile challenge.
---

### Head Movement Verification
Random challenge:
* Turn Left
* Turn Right
User must perform the movement.
This prevents photo-based spoofing.
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
* Better Accuracy
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
* Printed Image Attacks
Techniques:
* Blink Verification
* Smile Verification
* Head Movement Verification
---
## Screen Spoof Detection
Uses FFT (Fast Fourier Transform).
Detects:
* Phone Screens
* Laptop Screens
* Printed Photos
---
## Replay Attack Detection
Monitors:
Face Area Stability
If the face remains unnaturally static:
Replay Attack Detected
Access Blocked
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
---
## Employee Module
Functions:
* Login
* View Attendance
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
Step 1:
Employee Registration

Step 2:
Face Dataset Capture

Step 3:
Embedding Generation

Step 4:
Live Camera Recognition

Step 5:
Liveness Verification

Step 6:
Cosine Similarity Matching

Step 7:
Attendance Marked Automatically

Step 8:
Attendance Report Generated

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
Madichetty Sairuchitha
## Project Domain
Artificial Intelligence (AI)
Computer Vision
Face Recognition
Attendance Management
Workforce Management System
## Repository
https://github.com/ruchi011/ChronosFace
