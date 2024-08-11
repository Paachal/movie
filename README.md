Movie Listing API
Overview
The Movie Listing API is a FastAPI-based web service that allows users to register, log in, and manage movie listings. Users can add, view, update, delete movies, and add/view nested comments. The API uses JWT authentication to secure endpoints.

Features
User Registration & Login: Secure authentication with JWT.
CRUD Operations on Movies: Add, view, update, and delete movies.
Nested Comments: Users can add and view comments on movies.
API Documentation: Auto-generated documentation using Swagger.
Technologies
FastAPI: For building the web API.
MongoDB: NoSQL database for storing data.
JWT: For securing the API endpoints.
Vercel: Deployment platform.
Setup and Installation
Prerequisites
Python 3.8+
MongoDB Atlas (or a local MongoDB instance)
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/movie-assignment.git
cd movie-assignment
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory and add your MongoDB URI and a secret key for JWT:

bash
Copy code
MONGO_URL=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
SECRET_KEY=your_secret_key
Run the application:

bash
Copy code
uvicorn main:app --reload
API Endpoints
POST /token: Obtain JWT token.
GET /users/me: Get current logged-in user info.
POST /movies/: Create a new movie (authentication required).
GET /movies/: List all movies.
GET /movies/{movie_id}: Get details of a specific movie.
PUT /movies/{movie_id}: Update a movie (authentication required).
DELETE /movies/{movie_id}: Delete a movie (authentication required).
Testing the API
Swagger UI: Visit http://127.0.0.1:8000/docs to interact with the API.
ReDoc: Visit http://127.0.0.1:8000/redoc for alternative API documentation.
Deployment
To deploy the application on Vercel:

Push your code to GitHub.
Link your repository to Vercel.
Set environment variables on Vercel (MONGO_URL, SECRET_KEY).
Deploy!
Contributing
Feel free to open issues or submit pull requests with improvements.

License
This project is licensed under the MIT License