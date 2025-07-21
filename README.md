# FastAPI Ecommerce Backend

A FastAPI-based ecommerce backend application with MongoDB integration, built for the HROne Backend Intern Hiring Task.

## Features

- **Product Management**: Create and list products with filtering and pagination
- **Order Management**: Create orders and retrieve user orders
- **MongoDB Integration**: Uses MongoDB for data persistence
- **Input Validation**: Comprehensive request/response validation using Pydantic
- **Error Handling**: Proper HTTP status codes and error messages
- **Documentation**: Auto-generated API documentation with FastAPI

## Tech Stack

- **FastAPI**: Modern Python web framework
- **MongoDB**: NoSQL database for data storage
- **Pydantic**: Data validation and serialization
- **Pymongo**: MongoDB driver for Python
- **Uvicorn**: ASGI server for FastAPI

## API Endpoints

### Products

#### Create Product
- **POST** `/products`
- Creates a new product
- **Request Body**: `{"name": "Product Name", "price": 25.99, "quantity": 100}`
- **Response**: `{"id": "product_id"}` (Status: 201)

#### List Products
- **GET** `/products`
- Lists products with optional filtering and pagination
- **Query Parameters**:
  - `name`: Filter by product name (partial search supported)
  - `size`: Filter by size (searches within product name)
  - `limit`: Number of products to return (default: 10)
  - `offset`: Number of products to skip (default: 0)
- **Response**: Paginated list of products with metadata

### Orders

#### Create Order
- **POST** `/orders`
- Creates a new order and updates product quantities
- **Request Body**:
  ```json
  {
    "items": [{"productId": "product_id", "boughtQuantity": 2}],
    "totalAmount": 51.98,
    "userAddress": {"City": "New York", "Country": "USA", "ZipCode": "10001"}
  }
  ```
- **Response**: `{"id": "order_id"}` (Status: 201)

#### Get User Orders
- **GET** `/orders/{user_id}`
- Retrieves orders for a specific user
- **Query Parameters**:
  - `limit`: Number of orders to return (default: 10)
  - `offset`: Number of orders to skip (default: 0)
- **Response**: Paginated list of orders

## Database Schema

### Products Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "price": "number",
  "quantity": "number"
}
```

### Orders Collection
```json
{
  "_id": "ObjectId",
  "items": [{"productId": "string", "boughtQuantity": "number"}],
  "totalAmount": "number",
  "userAddress": {"City": "string", "Country": "string", "ZipCode": "string"},
  "createdOn": "datetime",
  "user_id": "string"
}
```

## Setup and Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone [<repository_url>](https://github.com/AnkitaGupta1003/HROne-Backend)
   cd fastapi-ecommerce
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**
   - Install MongoDB locally or use MongoDB Atlas (free M0 cluster)
   - Set the `MONGODB_URL` environment variable:
     ```bash
     export MONGODB_URL="mongodb://localhost:27017"
     # or for MongoDB Atlas:
     export MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net/ecommerce"
     ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - API: `http://localhost:8000`
   - Documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`



### Cloud Deployment (Render/Railway)

1. **Environment Variables**
   - Set `MONGODB_URL` to your MongoDB Atlas connection string

2. **Deploy**
   - Push to GitHub (public repository)
   - Connect to Render/Railway
   - Deploy using the provided Dockerfile

## Project Structure

```
fastapi-ecommerce/
├── main.py              # Main FastAPI application
├── database.py          # Database configuration and connection
├── schemas.py           # Pydantic models and schemas
├── utils.py             # Utility functions
├── routers/             # API route handlers
│   ├── __init__.py
│   ├── products.py      # Product-related endpoints
│   └── orders.py        # Order-related endpoints
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## Key Implementation Details

### Data Validation
- Uses Pydantic models for request/response validation
- Custom ObjectId handling for MongoDB integration
- Proper error handling with meaningful messages

### Database Operations
- Efficient queries with proper indexing considerations
- Transaction-like behavior for order creation (validates inventory before committing)
- Pagination support for large datasets

### Search and Filtering
- Regex-based partial search for product names
- Case-insensitive filtering
- Flexible query parameter handling

### Error Handling
- Proper HTTP status codes
- Detailed error messages
- Input validation with clear feedback

## Testing

You can test the API using the auto-generated documentation at `/docs` or use tools like curl, Postman, or any HTTP client.

### Example API Calls

```bash
# Create a product
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Large T-Shirt", "price": 25.99, "quantity": 100}'

# List products
curl "http://localhost:8000/products?limit=10&offset=0"

# Create an order
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"productId": "product_id_here", "boughtQuantity": 2}],
    "totalAmount": 51.98,
    "userAddress": {"City": "New York", "Country": "USA", "ZipCode": "10001"}
  }'
```

## Performance Considerations

- Database indexes on frequently queried fields
- Pagination to handle large datasets
- Efficient MongoDB queries
- Proper connection pooling with PyMongo

## Future Enhancements

- User authentication and authorization
- Product categories and better search
- Order status tracking
- Inventory management webhooks
- Rate limiting and API security
- Comprehensive test suite

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is created for the HROne Backend Intern Hiring Task.
