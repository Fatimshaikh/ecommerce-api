# E-Commerce API 🚀

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.99.0-green)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)

---

## Project Overview
This project is a **complete E-Commerce API** built with **FastAPI**, designed to manage users, products, carts, and orders in a secure and efficient way.  

- **Authentication:** Users log in with email and password to receive a JWT token, which is used for accessing protected routes.
- **Roles:** Admins can manage all users, products, and orders, while normal users can only manage their profile, cart, and own orders.
- **Secure:** Passwords are hashed using **bcrypt**, and sensitive operations are protected with JWT token authentication.
- **Database:** PostgreSQL is used with **SQLAlchemy ORM** for database operations.

---

## Features
- ✅ User registration & login
- ✅ JWT-based authentication
- ✅ Role-based authorization (Admin/User)
- ✅ CRUD operations for products, carts, and orders
- ✅ Secure password hashing
- ✅ Protected routes for update/delete operations
- ✅ API documentation with Swagger UI

---

## Tech Stack
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Token)
- **Password Hashing:** bcrypt
- **Docs:** Swagger UI
