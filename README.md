# Seller Dashboard FastAPI Backend

A complete FastAPI backend application that connects to Firebase Firestore and exposes REST API endpoints to retrieve product data. This API is designed to work seamlessly with Android app databases using the same Firestore structure.

## 🚀 Features

- **FastAPI Framework**: High-performance, modern Python web framework
- **Firebase Firestore Integration**: Direct connection to your Android app's database
- **CORS Enabled**: Browser-accessible API endpoints
- **Comprehensive Error Handling**: Proper HTTP status codes and error messages
- **Auto-Generated Documentation**: Interactive API docs at `/docs`
- **Query Parameters**: Filtering, sorting, and pagination support
- **Type Safety**: Pydantic models for request/response validation
- **Production Ready**: Logging, health checks, and proper error handling

## 📋 Prerequisites

- Python 3.8 or higher
- Firebase project with Firestore database
- Firebase service account credentials

## 🛠️ Installation & Setup

### 1. Clone or Create Project Directory

```bash
mkdir seller-dashboard
cd seller-dashboard
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Firebase Configuration

#### Option A: Service Account Key File (Recommended for Development)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to Project Settings → Service Accounts
4. Click "Generate New Private Key"
5. Download the JSON file
6. Rename it to `serviceAccountKey.json`
7. Place it in the project root directory

#### Option B: Environment Variables (Recommended for Production)

1. Copy `.env.example` to `.env`
2. Update the values with your Firebase credentials

### 5. Verify Firestore Database Structure

Ensure your Firestore has a `products` collection with documents containing:

```json
{
  "id": "string",
  "name": "string", 
  "price": number,
  "description": "string",
  "imageUrl": "string",
  "vendorId": "string",
  "email": "string",
  "createdAt": timestamp
}
```

## 🚀 Running the Application

### Development Mode

```bash
uvicorn main:app --reload --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Using Python Directly

```bash
python main.py
```

## 📊 API Endpoints

### Base URL
- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

### Available Endpoints

#### 🏠 Root & Utility

- **GET /** - API information and available endpoints
- **GET /health** - Health check and service status

#### 📦 Products

- **GET /products** - Get all products
  - Query parameters:
    - `limit`: Limit results (1-1000, default: 100)
    - `sort_by`: Sort field (name, price, createdAt)
    - `order`: Sort order (asc, desc)

- **GET /products/{product_id}** - Get product by ID
  - Returns 404 if product not found

- **GET /products/vendor/{vendor_id}** - Get products by vendor
  - Same query parameters as `/products`

#### 📚 Documentation

- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /redoc** - ReDoc API documentation

## 🔧 Example API Calls

### Get All Products

```bash
curl -X GET "http://localhost:8000/products?limit=10&sort_by=price&order=asc"
```

### Get Product by ID

```bash
curl -X GET "http://localhost:8000/products/your-product-id"
```

### Get Products by Vendor

```bash
curl -X GET "http://localhost:8000/products/vendor/vendor123?limit=5"
```

### Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

## 📤 Response Format

### Success Response

```json
{
  "success": true,
  "data": {...},
  "message": "Optional message"
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message",
  "status_code": 400
}
```

### Product Data Structure

```json
{
  "id": "product123",
  "name": "Product Name",
  "price": 29.99,
  "description": "Product description",
  "imageUrl": "https://example.com/image.jpg",
  "vendorId": "vendor123",
  "email": "vendor@example.com",
  "createdAt": "2024-01-01T12:00:00"
}
```

## 🔒 Security & Production Deployment

### Security Considerations

1. **Never commit credentials to version control**
2. **Use environment variables in production**
3. **Configure CORS properly for production**
4. **Use HTTPS in production**
5. **Implement rate limiting if needed**

### Production Configuration

1. Update CORS origins in `main.py`:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

2. Use environment variables instead of service account file

3. Deploy with proper production ASGI server:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## 🧪 Testing the API

### Using Interactive Documentation

1. Start the server: `uvicorn main:app --reload --port 8000`
2. Open browser: `http://localhost:8000/docs`
3. Try out the endpoints directly in the browser

### Using curl

```bash
# Test API status
curl -X GET "http://localhost:8000/"

# Test health check
curl -X GET "http://localhost:8000/health"

# Test products endpoint
curl -X GET "http://localhost:8000/products"
```

### Using Postman or HTTP Client

Import the OpenAPI schema from `http://localhost:8000/openapi.json`

## 🐛 Troubleshooting

### Common Issues

1. **Firebase Connection Error**
   - Verify `serviceAccountKey.json` is valid
   - Check Firebase project ID
   - Ensure Firestore is enabled

2. **Port Already in Use**
   - Change port: `uvicorn main:app --port 8001`
   - Kill existing process

3. **CORS Issues**
   - Check browser console for CORS errors
   - Verify CORS configuration in `main.py`

4. **Missing Dependencies**
   - Reinstall: `pip install -r requirements.txt`

### Logging

The application includes comprehensive logging. Check console output for detailed error information.

### Debug Mode

Set `DEBUG=True` in environment variables for detailed error responses.

## 📁 Project Structure

```
seller-dashboard/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── serviceAccountKey.json  # Firebase credentials (do not commit)
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Test with the interactive documentation at `/docs`
4. Verify Firebase configuration and permissions

---

**Happy coding! 🚀**