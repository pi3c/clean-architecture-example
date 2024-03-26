# Python RESTful Blog API

I wrote this project to explore clean architecture and put some of its principles into practice. Since I had no ideas for the project, I chose to develop a REST API for a classic blog

## Installation

To install the dependencies, run the following command:

```bash
pip install -e .
```

## Setting Environment Variables

Before running the project, make sure you have an `.env` file in the `env/` directory, containing the following variables:

```.env
# JWT settings
JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
JWT_EXPIRES_IN=2

# PostgreSQL settings
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=5432

# Server settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## Running

To run the project, execute:

```bash
bash scripts/start.sh
```

## API Routes
![API Routes](api_routes.png)

### posts
- `GET /posts` - Get all posts
- `POST /posts` - Create a new post
- `GET /posts/{id}` - Get post by ID
- `PATCH /posts{id}` - Update a post by post ID
- `DELETE /posts/{id}` - Delete a post by post ID

### comments
- `POST /comments` - Create comment
- `GET /comments/{id}` - Get comment by ID
- `PATCH /comments/{id}` - Update comment by ID
- `DELETE /comments/{id}` - Delete comment by ID
- `GET /comments?post_id=` - Get comments by post ID

### authentication
- `POST /auth/register` - Register user
- `POST /auth/login` - Login user

### users
- `GET /users/me` - Get current user

## Contribution

If you have any suggestions for improving the project, please create an Issue or Pull Request.
