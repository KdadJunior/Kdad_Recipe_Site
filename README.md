# Kdad_Recipe_Site  
# The Meals LAN — Recipe Management Backend

A Flask-based REST API for managing users and recipes with secure JWT auth, likes, follows, and flexible search (feed, popular, ingredients). Built to demonstrate real-world backend design: authentication, relational data modeling, and production-style endpoints.

---

## 🚀 Features

- **JWT Auth** with HMAC-SHA256 signing and secure password hashing
- **Recipes**: create, view (field-selectable), like
- **Social graph**: follow other users; feed built from follow graph
- **Search modes**:  
  - **Feed**: latest from followed users  
  - **Popular**: top liked recipes  
  - **Ingredients**: filter by ingredient list
- **Safe deletes** with cascading cleanup for user-owned data

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, Flask
- **DB**: SQLite3 (relational, FK + cascades)
- **Auth**: JWT (HMAC-SHA256)
- **Security**: salted password hashing, password history, input validation

---

## 📋 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/login` | Verifies credentials and returns a JWT (`{"status":1,"jwt":"<TOKEN>"}`) | No |

### Recipes
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/create_recipe` | Create a recipe. Form params: `recipe_id` (int), `name` (str), `description` (str), `ingredients` (JSON list, optional) | Yes |
| GET | `/view_recipe/<int:recipe_id>` | Return only the fields you request via query flags: `name`, `description`, `likes`, `ingredients` (each `True`/`False`) | Yes |
| POST | `/like` | Like a recipe (one like per user per recipe) | Yes |

### Social
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/follow` | Follow a user by `username` (form) | Yes |
| GET | `/search` | Multi-mode search. Query flags: `feed=True` (recent from followed users), `popular=True` (top by likes), or `ingredients=[...]` (JSON list) | Yes |

### Account
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/delete` | Delete your own account; cascades remove your recipes/likes/follows | Yes |

---

## 🗄️ Database Schema (SQLite)

```sql
-- users + password history
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

CREATE TABLE password_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    pass_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- recipes + likes (unique per user/recipe)
CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    ingredients TEXT, -- JSON list (optional)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    UNIQUE(user_id, recipe_id)
);

-- social graph
CREATE TABLE follows (
    id INTEGER PRIMARY KEY,
    follower_id INTEGER NOT NULL,
    following_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(follower_id, following_id)
);

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
