"""
FastAPI Backend Application for Seller Dashboard
Connects to Firebase Firestore and provides REST API endpoints for product data.
"""

import os
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Seller Dashboard API",
    description="REST API for retrieving product data from Firebase Firestore",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase Admin SDK
try:
    # Check if Firebase app is already initialized
    if not firebase_admin._apps:
        # Try to load from environment variable first (for production)
        import json
        creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
        
        if creds_json:
            # Production: Load from environment variable
            cred_dict = json.loads(creds_json)
            cred = credentials.Certificate(cred_dict)
            logger.info("Loading Firebase credentials from environment variable")
        else:
            # Development: Load from file
            cred = credentials.Certificate("serviceAccountKey.json")
            logger.info("Loading Firebase credentials from file")
        
        firebase_admin.initialize_app(cred)
    
    # Initialize Firestore client
    db = firestore.client()
    logger.info("Firebase Admin SDK initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Firebase: {str(e)}")
    db = None

# Pydantic Models for Request/Response Validation

class Product(BaseModel):
    """Product model representing the Firestore document structure"""
    id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Product description")
    imageUrl: str = Field(..., description="Product image URL")
    vendorId: str = Field(..., description="Vendor identifier")
    email: str = Field(..., description="Vendor email")
    createdAt: str = Field(..., description="Product creation timestamp (ISO format)")

class APIResponse(BaseModel):
    """Standard API response format"""
    success: bool = Field(..., description="Request success status")
    data: Any = Field(..., description="Response data")
    message: Optional[str] = Field(None, description="Optional message")

class ErrorResponse(BaseModel):
    """Error response format"""
    success: bool = Field(False, description="Request success status")
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")

# Helper Functions

def convert_firestore_timestamp(timestamp) -> str:
    """Convert Firestore timestamp to ISO format string"""
    if hasattr(timestamp, 'timestamp'):
        return datetime.fromtimestamp(timestamp.timestamp()).isoformat()
    elif isinstance(timestamp, datetime):
        return timestamp.isoformat()
    else:
        return str(timestamp)

def format_product_data(doc) -> Dict[str, Any]:
    """Format Firestore document to Product format"""
    data = doc.to_dict()
    data['id'] = doc.id
    
    # Convert timestamp to ISO format
    if 'createdAt' in data:
        data['createdAt'] = convert_firestore_timestamp(data['createdAt'])
    
    # Handle missing fields gracefully
    required_fields = ['name', 'price', 'description', 'imageUrl', 'vendorId', 'email']
    for field in required_fields:
        if field not in data:
            data[field] = ""
    
    # Ensure price is a number
    if 'price' in data:
        try:
            data['price'] = float(data['price'])
        except (ValueError, TypeError):
            data['price'] = 0.0
    
    return data

# API Endpoints

@app.get("/", response_model=APIResponse)
async def root():
    """
    Root endpoint - Returns API information and available endpoints
    """
    api_info = {
        "api_name": "Seller Dashboard API",
        "version": "1.0.0",
        "description": "REST API for retrieving product data from Firebase Firestore",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /products": "Get all products",
            "GET /products/{product_id}": "Get product by ID",
            "GET /products/vendor/{vendor_id}": "Get products by vendor",
            "GET /docs": "Interactive API documentation",
            "GET /redoc": "ReDoc API documentation"
        },
        "query_parameters": {
            "/products": {
                "limit": "Limit number of results (default: 100)",
                "sort_by": "Sort by field (name, price, createdAt)",
                "order": "Sort order (asc, desc)"
            }
        }
    }
    
    return APIResponse(success=True, data=api_info, message="Welcome to Seller Dashboard API")

@app.get("/health", response_model=APIResponse)
async def health_check():
    """
    Health check endpoint - Returns service status
    """
    firestore_status = "connected" if db is not None else "disconnected"
    
    health_data = {
        "status": "healthy" if db is not None else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "fastapi": "running",
            "firestore": firestore_status
        }
    }
    
    return APIResponse(success=True, data=health_data)

@app.get("/products", response_model=APIResponse)
async def get_all_products(
    limit: int = Query(100, ge=1, le=1000, description="Limit number of results"),
    sort_by: str = Query("createdAt", description="Sort by field (name, price, createdAt)"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order")
):
    """
    Get all products from Firestore
    
    Query parameters:
    - limit: Maximum number of products to return (1-1000)
    - sort_by: Field to sort by (name, price, createdAt)
    - order: Sort order (asc, desc)
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Firebase connection not available")
    
    try:
        # Build query with sorting
        products_ref = db.collection('products')
        
        # Apply sorting
        direction = firestore.Query.ASCENDING if order == "asc" else firestore.Query.DESCENDING
        query = products_ref.order_by(sort_by, direction=direction).limit(limit)
        
        # Execute query
        docs = query.stream()
        
        # Format products data
        products = []
        for doc in docs:
            try:
                product_data = format_product_data(doc)
                products.append(product_data)
            except Exception as e:
                logger.warning(f"Failed to format product {doc.id}: {str(e)}")
                continue
        
        logger.info(f"Retrieved {len(products)} products")
        return APIResponse(
            success=True, 
            data=products, 
            message=f"Retrieved {len(products)} products"
        )
        
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve products: {str(e)}")

@app.get("/products/{product_id}", response_model=APIResponse)
async def get_product_by_id(product_id: str):
    """
    Get a single product by ID
    
    Parameters:
    - product_id: Unique product identifier
    
    Returns:
    - Product details if found
    - 404 error if product not found
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Firebase connection not available")
    
    try:
        # Get product document
        doc_ref = db.collection('products').document(product_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Product with ID '{product_id}' not found")
        
        # Format product data
        product_data = format_product_data(doc)
        
        logger.info(f"Retrieved product: {product_id}")
        return APIResponse(
            success=True, 
            data=product_data, 
            message=f"Product {product_id} retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve product: {str(e)}")

@app.get("/products/vendor/{vendor_id}", response_model=APIResponse)
async def get_products_by_vendor(
    vendor_id: str,
    limit: int = Query(100, ge=1, le=1000, description="Limit number of results"),
    sort_by: str = Query("createdAt", description="Sort by field (name, price, createdAt)"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order")
):
    """
    Get all products for a specific vendor
    
    Parameters:
    - vendor_id: Vendor identifier to filter by
    
    Query parameters:
    - limit: Maximum number of products to return (1-1000)
    - sort_by: Field to sort by (name, price, createdAt)
    - order: Sort order (asc, desc)
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Firebase connection not available")
    
    try:
        # Build query for vendor products
        products_ref = db.collection('products')
        
        # Filter by vendorId only (no sorting to avoid index requirement)
        query = products_ref.where('vendorId', '==', vendor_id).limit(limit)
        
        # Execute query
        docs = query.stream()
        
        # Format products data and sort in memory
        products = []
        for doc in docs:
            try:
                product_data = format_product_data(doc)
                products.append(product_data)
            except Exception as e:
                logger.warning(f"Failed to format product {doc.id}: {str(e)}")
                continue
        
        # Sort in memory based on the requested field
        reverse = (order == "desc")
        if sort_by == "price":
            products.sort(key=lambda x: x.get('price', 0), reverse=reverse)
        elif sort_by == "name":
            products.sort(key=lambda x: x.get('name', ''), reverse=reverse)
        else:  # createdAt
            products.sort(key=lambda x: x.get('createdAt', ''), reverse=reverse)
        
        logger.info(f"Retrieved {len(products)} products for vendor: {vendor_id}")
        return APIResponse(
            success=True, 
            data=products, 
            message=f"Retrieved {len(products)} products for vendor {vendor_id}"
        )
        
    except Exception as e:
        logger.error(f"Error retrieving products for vendor {vendor_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve vendor products: {str(e)}")

# Exception Handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return {
        "success": False,
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "success": False,
        "error": "Internal server error",
        "status_code": 500
    }

# Application startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Seller Dashboard API starting up...")
    if db is None:
        logger.warning("Firebase connection not available - some endpoints may not work")
    else:
        logger.info("Firebase connection established")

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Seller Dashboard API shutting down...")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )