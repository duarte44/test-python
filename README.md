<<<<<<< HEAD
# alura-python-testes
=======
# alura-python-testes

# Burguer App - Class-Based Architecture

## Overview
This project has been refactored to use a class-based architecture across all microservices. The refactoring maintains backward compatibility by keeping the original functions while adding new class-based implementations.

## Architecture

### Microservices Structure
- **Auth Service** (Port 5000) - Authentication and authorization
- **User Service** (Port 5001) - User management
- **Product Service** (Port 5003) - Product catalog management
- **Order Service** (Port 5002) - Order processing

### Class-Based Components

#### 1. Database Configuration
All services now use `DatabaseConfig` class:

#### 2. Models
Each service has class-based models:

**UserModel**
- Handles user data serialization and validation
- Methods: `serialize()`, `to_dict()`, `validate()`

**ProductModel**  
- Manages product data and validation
- Methods: `serialize()`, `to_dict()`, `validate()`

**OrderModel**
- Handles order data and status management
- Methods: `serialize()`, `to_dict()`, `validate()`, `update_status()`

#### 3. Services
Business logic is encapsulated in service classes:

**AuthService**
- `login_user()` - User authentication
- `verify_user_exists()` - User verification

**UserService**
- `create_user()` - User creation with validation
- `get_user_by_email()` - User retrieval
- `update_user()` - User data updates
- `delete_user()` - User removal

**ProductService**
- `create_product()` - Product creation with validation
- `get_all_products()` - Product listing
- `get_available_products()` - Available products only
- `update_product()` - Product updates
- `delete_product()` - Product removal
- `initialize_products()` - Default product creation

**OrderService**
- `create_order()` - Order creation with validation
- `get_order_by_id()` - Order retrieval
- `update_order_status()` - Status management
- `delete_order()` - Order removal

#### 4. Controllers
Request handling is managed by controller classes:

**AuthController**
- `login_page()` - Login form display
- `login()` - Authentication processing
- `dashboard()` - User dashboard
- `logout()` - Session termination

**UserController**
- `create()` - User registration
- `profile()` - Profile display
- `edit()` - Profile editing
- `delete()` - User deletion

**ProductController**
- `list_products()` - Product catalog
- `admin_products()` - Admin product management
- `create_product()` - Product creation
- `edit_product()` - Product editing
- `delete_product()` - Product deletion
- `api_products()` - API endpoint for products

**OrderController**
- `create_order()` - Order creation
- `list_all_orders()` - Order listing
- `get_order_details()` - Order details
- `update_order_status()` - Status updates
- `delete_order()` - Order deletion

#### 5. Applications
Main application classes:

**AuthApp**, **UserApp**, **ProductApp**, **OrderApp**
- Encapsulate Flask application configuration
- Handle routing setup
- Manage application lifecycle

## Key Benefits

### 1. **Maintainability**
- Clear separation of concerns
- Easier to test individual components
- Better code organization

### 2. **Scalability**
- Easy to extend functionality
- Better dependency management
- Reusable components

### 3. **Backward Compatibility**
- Original functions preserved
- Gradual migration possible
- No breaking changes

### 4. **Data Validation**
- Built-in validation in models
- Consistent error handling
- Better data integrity

### 5. **Testing**
- Easier to mock dependencies
- Unit testing friendly
- Better isolation

## Running the Application
Each service can be run independently:

```bash
# Auth Service
cd auth-service
python app.py

# User Service  
cd user-service
python app.py

# Product Service
cd product-service
python app.py

# Order Service
cd order-service
python app.py
```

## Environment Setup

Make sure to have a `.env` file in each service directory:

```
MONGO_URI

## Dependencies

Each service requires:
- Flask
- PyMongo
- python-dotenv
- Werkzeug

Install with:
```bash
pip install -r requirements.txt
```

## Future Enhancements

The class-based architecture enables:
- Easy addition of new features
- Better error handling
- Improved logging
- Enhanced security
- API versioning
- Caching implementation
- Database connection pooling

## Migration Guide

To fully migrate to class-based approach:

1. Replace function calls with class method calls
2. Update imports to use new classes
3. Leverage validation methods in models
4. Use service classes for business logic
5. Implement proper error handling

The refactored codebase maintains full backward compatibility while providing a solid foundation for future development.
>>>>>>> 14f1c5638fc5d459c596b1b8c06251699ec690ca
