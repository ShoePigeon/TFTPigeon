# API Documentation

## User Login and Registration

### 1. User Registration

#### Endpoint

```
POST /register
```

#### Input Example

```json
{
  "user_name": "john_doe",
  "password": "secure_password123",
  "DOB": "1995-06-15",
  "email": "abc@gmail.com"
}
```

#### Response Example

```json
{
  "status": 200,
  "message": "Registration successful",
  "user_id": 1,
  "user_name": "john_doe",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.abc123token"
}
```

#### Description

##### Purpose

Registers a new user in the system.

##### Input Fields

- `user_name`: The username of the new user (string, required)
- `password`: The password for the new user (string, required)
- `DOB`: The date of birth of the new user (date, optional)
- `email`: The email address of the new user (string, required)

##### Output

- `status`: HTTP status code (200 for success)
- `message`: A message indicating the result of the operation
- `user_id`: Unique identifier for the newly registered user
- `user_name`: Username of the newly registered user
- `token`: A JWT token for authentication purposes

### 2. User Login

#### Endpoint

```
POST /login
```

#### Input Example

```json
{
  "user_name": "john_doe",
  "password": "secure_password123"
}
```

#### Response Example

```json
{
  "status": 200,
  "message": "Login successful",
  "user_id": 1,
  "user_name": "john_doe",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.abc123token"
}
```

#### Description

##### Purpose

Authenticates an existing user.

##### Input Fields

- `user_name`: The username of the user (string, required)
- `password`: The password for the user (string, required)

##### Output

- `status`: HTTP status code (200 for success)
- `message`: A message indicating the result of the operation
- `user_id`: Unique identifier of the authenticated user
- `user_name`: Username of the authenticated user
- `token`: A JWT token for authentication purposes
