# EventFlow AI

An event registration and crowd management platform designed to handle high-concurrency registrations, automated waitlist management, and secure role-based access control.

## Key Features

### Authentication & Authorization

* JWT-based authentication
* Secure password hashing with bcrypt
* Role-based access control (Organizer / Student)

### Event Management

* Create and manage events
* Open/close registrations
* Cancel events
* Automatic event completion based on event date

### Registration System

* Capacity-aware registrations
* Automatic waitlist management
* Waitlist promotion on cancellation
* Re-registration support
* Duplicate registration prevention

### Concurrency-Safe Seat Allocation

Implemented transaction-safe registration using PostgreSQL row-level locking (`SELECT ... FOR UPDATE`) to prevent race conditions during simultaneous registrations.

### Database Design

* PostgreSQL
* SQLAlchemy ORM
* Foreign key relationships
* Unique constraints
* Transaction management

## System Design Concepts

### Concurrency

Prevents overbooking when multiple users attempt to register for the last available seats simultaneously.

### Synchronization

Ensures consistent seat allocation and waitlist promotion under concurrent requests.

### Reliability

Uses transactional updates to maintain database consistency during registrations, cancellations, and waitlist promotions.

## Tech Stack

### Backend

* FastAPI
* Python
* PostgreSQL
* SQLAlchemy

### Authentication

* JWT
* Passlib (bcrypt)

### Frontend (In Progress)

* Next.js
* TypeScript
* Tailwind CSS

## Future Enhancements

* Google OAuth Login
* QR-based ticket generation
* Organizer analytics dashboard
* Gemini-powered event description generation
* Attendance prediction models
* Event recommendation engine
* Redis + Celery background jobs
* Email notifications
* Deployment on cloud infrastructure
