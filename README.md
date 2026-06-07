# 🍕 Pizza REST API

A RESTful API built with FastAPI simulating a pizzeria order management system. It supports user authentication with JWT, order creation, item management, and role-based access control.

---

## Tech Stack

Python, FastAPI, SQLAlchemy, SQLite, Alembic, JWT (python-jose), Passlib (bcrypt), Pydantic, python-dotenv

---

## Features

User registration and login with JWT authentication, access token and refresh token support, order creation and management, add and remove items from orders, order cancellation and finalization, admin-only routes for listing all orders, user-specific order history and resume.

---

## Project Structure

```
RESTAPI_SCHEME/
├── alembic/              # Database migrations
├── venv/                 # Virtual environment (not committed)
├── .env                  # Environment variables (not committed)
├── alembic.ini           # Alembic configuration
├── main.py               # App entry point, config and router registration
├── models.py             # SQLAlchemy models (User, Order, ItemOrder)
├── schemas.py            # Pydantic schemas for request/response validation
├── dependencies.py       # Session factory and token verification
├── auth_routes.py        # Authentication routes
├── order_routes.py       # Order management routes
└── requirements.txt      # Project dependencies
```

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root of the project with the following content:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**5. Run database migrations**

```bash
alembic upgrade head
```

**6. Start the server**

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

### Auth — `/auth`

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/auth/` | Default auth route | No |
| POST | `/auth/create_account` | Register a new user | No |
| POST | `/auth/login` | Login with email and password | No |
| POST | `/auth/login-form` | Login via OAuth2 form (for Swagger UI) | No |
| POST | `/auth/refresh` | Generate a new access token using refresh token | Yes |

### Orders — `/orders`

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/orders/` | Default orders route | No |
| POST | `/orders/order` | Create a new order | Yes |
| POST | `/orders/order/add_item/{order_id}` | Add an item to an order | Yes |
| POST | `/orders/order/remove_item/{item_order_id}` | Remove an item from an order | Yes |
| POST | `/orders/order/cancel/{order_id}` | Cancel an order | Yes |
| POST | `/orders/order/finish/{order_id}` | Finalize an order | Yes |
| GET | `/orders/order/{order_id}` | View a specific order | Yes |
| GET | `/orders/list` | List all orders (admin only) | Yes (admin) |
| GET | `/orders/list/user-orders` | List orders of the authenticated user | Yes |
| GET | `/orders/list/user-order-resume` | List order resume of the authenticated user | Yes |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Secret key used to sign JWT tokens |
| `ALGORITHM` | Signing algorithm (e.g. `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration time in minutes |

---

## Notes

The `banco.db` SQLite file is not committed to the repository. Run `alembic upgrade head` to generate the database locally. The `venv/` folder and `.env` file are also excluded from version control.

---

## TODO

- Restrict `admin=True` assignment to existing admin users only
- Add pagination to order listing endpoints
