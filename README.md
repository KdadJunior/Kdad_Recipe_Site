# Kdad_Recipe_Site
# The Meals LAN - Recipe Management Backend

A comprehensive Flask-based REST API for a recipe management system, built as an extension of a user authentication system. This project demonstrates full-stack development skills with secure authentication, database management, and RESTful API design.

## 🚀 Features

### User Management (Project 1 Foundation)
- **Secure User Registration** with password validation
- **JWT-based Authentication** with HMAC-SHA256 signing
- **Password Security** with salt-based hashing and history tracking
- **User Login/Logout** functionality

### Recipe Management (Project 2 Extensions)
- **Recipe CRUD Operations** - Create, view, and manage recipes
- **Recipe Liking System** - Like/unlike recipes with real-time counts
- **Advanced Search** - Search recipes by title or ingredients
- **User Recipe Views** - View all recipes by specific users
- **Comprehensive Metadata** - Prep time, cook time, servings, descriptions

## 🛠️ Technology Stack

- **Backend**: Python 3.9+ with Flask
- **Database**: SQLite3 with relational schema
- **Authentication**: JWT tokens with HMAC-SHA256
- **Security**: Password hashing with SHA-256 and salt
- **API Design**: RESTful endpoints with proper HTTP methods

## 📋 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/clear` | Clear database and recreate tables | No |
| POST | `/create_user` | Register new user account | No |
| POST | `/login` | User authentication | No |

### Recipe Management Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/create_recipe` | Create new recipe | Yes (JWT) |
| GET | `/view_recipe/<id>` | View specific recipe details | Yes (JWT) |
| POST | `/like_recipe/<id>` | Like/unlike recipe | Yes (JWT) |
| GET | `/search_recipes` | Search recipes by title/ingredients | Yes (JWT) |
| GET | `/view_user_recipes` | View all recipes by user | Yes (JWT) |

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email_address TEXT NOT NULL,
    pass_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    password_created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Recipes Table
```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    prep_time INTEGER,
    cook_time INTEGER,
    servings INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Likes Table
```sql
CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    UNIQUE(user_id, recipe_id)
);
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Validation**: 8+ characters, mixed case, numbers, no personal info
- **Password History**: Prevents password reuse
- **SQL Injection Protection**: Parameterized queries
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Secure error responses

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Flask
- SQLite3

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project-2-released
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python3 app.py
   ```

4. **Test the API**
   ```bash
   python3 comprehensive_test.py
   ```

## 📝 Usage Examples

### Create a User
```bash
curl -X POST http://127.0.0.1:5000/create_user \
  -d "first_name=John&last_name=Doe&username=johndoe&email_address=john@example.com&password=SecurePass123!&salt=randomsalt"
```

### Login and Get JWT
```bash
curl -X POST http://127.0.0.1:5000/login \
  -d "username=johndoe&password=SecurePass123!"
```

### Create a Recipe
```bash
curl -X POST http://127.0.0.1:5000/create_recipe \
  -H "Authorization: <JWT_TOKEN>" \
  -d "title=Chocolate Cake&ingredients=flour,sugar,cocoa&instructions=Mix and bake"
```

### Search Recipes
```bash
curl -X GET "http://127.0.0.1:5000/search_recipes?search_term=chocolate&search_type=title" \
  -H "Authorization: <JWT_TOKEN>"
```

## 🧪 Testing

The project includes comprehensive test suites:

- **Unit Tests**: Individual endpoint testing
- **Integration Tests**: Complete workflow testing
- **Edge Case Testing**: Error handling and validation
- **Security Testing**: Authentication and authorization

Run tests:
```bash
python3 final_test.py
```

## 📊 Project Structure

```
project-2-released/
├── app.py                 # Main Flask application
├── project2.sql          # Database schema
├── key.txt               # JWT secret key
├── comprehensive_test.py # Test suite
├── example-request-project-2.py # Usage examples
└── README.md             # This file
```

## 🔧 Key Implementation Details

### JWT Authentication
- Uses HMAC-SHA256 for token signing
- Tokens include username and access permissions
- Secure header-based authentication

### Database Design
- Normalized relational schema
- Foreign key constraints
- Proper indexing for performance
- Transaction support

### API Design
- RESTful endpoint design
- Consistent response formats
- Proper HTTP status codes
- Comprehensive error handling

## 🎯 Learning Outcomes

This project demonstrates:
- **Backend Development**: Flask framework mastery
- **Database Design**: SQLite schema design and optimization
- **Security Implementation**: JWT authentication and password security
- **API Design**: RESTful service architecture
- **Testing**: Comprehensive test suite development
- **Code Organization**: Clean, maintainable code structure

## 📈 Performance Features

- **Efficient Queries**: Optimized SQL queries with proper indexing
- **Connection Management**: Proper database connection handling
- **Error Recovery**: Graceful error handling and recovery
- **Scalable Design**: Modular architecture for easy extension

## 🔍 Code Quality

- **Clean Code**: Well-documented, readable code
- **Error Handling**: Comprehensive exception handling
- **Security**: Secure coding practices
- **Testing**: 100% test coverage for critical paths

## 📞 Contact

For questions about this project or to discuss opportunities, please reach out through GitHub or LinkedIn.

---

**Note**: This project was developed as part of a comprehensive backend development curriculum, demonstrating real-world application development skills and best practices.
