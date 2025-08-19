# Camping with Friends - Full Stack Web Application

A social camping application where users can log camping trips, search for campgrounds, view their friends' camping adventures in a feed, and interact socially around shared outdoor activities.

## Tech Stack

- **Backend**: Python + FastAPI
- **Database**: PostgreSQL + SQLAlchemy
- **Authentication**: JWT-based login/signup
- **External APIs**: RapidAPI Outdoor Activities (for campground data)
- **Frontend**: React + TypeScript (coming soon)

## Project Structure

```
app/
├── api/              # API routes
│   ├── auth.py       # Authentication endpoints
│   ├── users.py      # User endpoints
│   ├── campgrounds.py # Campground search endpoints
│   └── camping_trips.py # Camping trip endpoints
├── core/             # Core functionality
│   ├── config.py     # Configuration settings
│   ├── database.py   # Database connection
│   ├── security.py   # Security utilities
│   ├── auth.py       # Authentication dependencies
│   └── api_service.py # External API service
├── crud/             # Database operations
│   ├── user.py       # User CRUD operations
│   ├── campground.py # Campground CRUD operations
│   └── camping_trip.py # Camping trip CRUD operations
├── models/           # SQLAlchemy models
│   ├── user.py       # User model
│   ├── campground.py # Campground model
│   ├── camping_trip.py # Camping trip model
│   └── friend.py     # Friend model
├── schemas/          # Pydantic schemas
│   ├── user.py       # User schemas
│   ├── campground.py # Campground schemas
│   ├── camping_trip.py # Camping trip schemas
│   └── token.py      # Token schemas
└── main.py           # FastAPI application
```

## Features

### Authentication
- User registration with email and username
- JWT-based login system
- Password hashing with bcrypt
- Protected routes requiring authentication

### Camping Features
- Search for campgrounds using external API
- Log camping trips with details (title, dates, weather, group size)
- View personal camping history
- View friend feed (camping trips from other users)
- Update and delete camping trips (only own trips)

### User Management
- Get current user information
- User profile management (coming soon)

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user information

### Campgrounds
- `GET /api/v1/campgrounds/search` - Search for campgrounds
- `GET /api/v1/campgrounds/{campground_id}` - Get specific campground

### Camping Trips
- `POST /api/v1/camping-trips/` - Log a new camping trip
- `GET /api/v1/camping-trips/my-trips` - Get current user's camping trips
- `GET /api/v1/camping-trips/feed` - Get friend feed
- `GET /api/v1/camping-trips/{trip_id}` - Get specific camping trip
- `PUT /api/v1/camping-trips/{trip_id}` - Update a camping trip
- `DELETE /api/v1/camping-trips/{trip_id}` - Delete a camping trip

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL database

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd camping-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**
   - Create a new database named `hiking_app` (legacy name, will be updated)
   - Update the `DATABASE_URL` in `app/core/config.py` if needed

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**
   - API documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `username` (Unique)
- `hashed_password`
- `full_name`
- `is_active`
- `created_at`
- `updated_at`

### Campgrounds Table
- `id` (Primary Key)
- `name`
- `location`
- `description`
- `latitude`
- `longitude`
- `amenities` (JSON)
- `max_capacity`
- `has_electricity`
- `has_water`
- `has_showers`
- `has_wifi`
- `pet_friendly`
- `rv_friendly`
- `tent_friendly`
- `external_id`
- `source_api`
- `created_at`

### Camping Trips Table
- `id` (Primary Key)
- `title`
- `description`
- `start_date`
- `end_date`
- `notes`
- `weather_conditions`
- `group_size`
- `user_id` (Foreign Key to Users)
- `campground_id` (Foreign Key to Campgrounds)
- `created_at`
- `updated_at`

### Friends Table
- `id` (Primary Key)
- `user_id` (Foreign Key to Users)
- `friend_id` (Foreign Key to Users)
- `is_accepted`
- `created_at`

## Development Notes

This is a learning project focused on teaching software engineering fundamentals:

- **Separation of Concerns**: Each module has a specific responsibility
- **Dependency Injection**: FastAPI's dependency system for clean code
- **Data Validation**: Pydantic schemas ensure data integrity
- **Security**: JWT tokens, password hashing, and proper authentication
- **Database Design**: Proper relationships and constraints
- **API Design**: RESTful endpoints with proper HTTP methods
- **External API Integration**: Mock data fallback for development

## Next Steps

1. Implement friend system (send/accept friend requests)
2. Add image upload for camping trips
3. Create React frontend
4. Add real-time notifications
5. Implement advanced search and filtering
6. Add camping recommendations
7. Integrate with real campground APIs
