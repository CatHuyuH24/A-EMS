"""
API Gateway routing configuration.
"""

from fastapi import FastAPI, Request, Response, HTTPException
import httpx
from typing import Dict, Any
import json

from shared.logging.logger import get_logger

logger = get_logger(__name__)

# Service endpoints configuration
SERVICE_ENDPOINTS = {
    "auth": "http://auth-service:8000",
    "sales": "http://sales-service:8001",
    "finance": "http://finance-service:8002",
    "hr": "http://hr-service:8003",
    "products": "http://products-service:8004",
    "risk": "http://risk-service:8005",
    "reports": "http://reports-service:8006",
    "ai": "http://ai-service:8007"
}


async def proxy_request(
    request: Request,
    service_url: str,
    path: str = ""
) -> Response:
    """Proxy HTTP request to microservice."""
    http_client = request.app.state.http_client
    
    # Build target URL
    target_url = f"{service_url}{path}"
    
    # Prepare headers (exclude hop-by-hop headers)
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    try:
        # Read request body
        body = await request.body()
        
        # Make request to microservice
        response = await http_client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=dict(request.query_params)
        )
        
        # Create response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )
        
    except httpx.TimeoutException:
        logger.error(f"Timeout calling service: {target_url}")
        raise HTTPException(
            status_code=504,
            detail={
                "error": "Service timeout",
                "message": "The request took too long to process"
            }
        )
    
    except httpx.ConnectError:
        logger.error(f"Failed to connect to service: {target_url}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Service unavailable",
                "message": "The service is currently unavailable"
            }
        )
    
    except Exception as e:
        logger.error(f"Error proxying request to {target_url}: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail={
                "error": "Gateway error",
                "message": "An error occurred while processing the request"
            }
        )


def setup_routes(app: FastAPI):
    """Setup API Gateway routes."""
    
    # Authentication service routes
    @app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def auth_service_proxy(request: Request, path: str):
        return await proxy_request(
            request, 
            SERVICE_ENDPOINTS["auth"], 
            f"/api/auth/{path}"
        )
    
    # Sales service routes
    @app.api_route("/api/sales/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def sales_service_proxy(request: Request, path: str):
        return await proxy_request(
            request,
            SERVICE_ENDPOINTS["sales"],
            f"/api/sales/{path}"
        )
    
    # Finance service routes
    @app.api_route("/api/finance/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def finance_service_proxy(request: Request, path: str):
        return await proxy_request(
            request,
            SERVICE_ENDPOINTS["finance"],
            f"/api/finance/{path}"
        )
    
    # HR service routes
    @app.api_route("/api/hr/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def hr_service_proxy(request: Request, path: str):
        return await proxy_request(
            request,
            SERVICE_ENDPOINTS["hr"],
            f"/api/hr/{path}"
        )
    
    # Products service routes
    @app.api_route("/api/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def products_service_proxy(request: Request, path: str):
        return await proxy_request(
            request,
            SERVICE_ENDPOINTS["products"],
            f"/api/products/{path}"
        )
    
    # Risk service routes
    @app.api_route("/api/risk/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def risk_service_proxy(request: Request, path: str):
        return await proxy_request(
            request,
            SERVICE_ENDPOINTS["risk"],
            f"/api/risk/{path}"
        )
    
    # Reports service routes
    @app.api_route("/api/reports/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def reports_service_proxy(request: Request, path: str):
        return await proxy_request(
            request,
            SERVICE_ENDPOINTS["reports"],
            f"/api/reports/{path}"
        )
    
    # AI service routes
    @app.api_route("/api/ai/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def ai_service_proxy(request: Request, path: str):
        return await proxy_request(
            request,
            SERVICE_ENDPOINTS["ai"],
            f"/api/ai/{path}"
        )
    
    # Service discovery endpoint
    @app.get("/api/services")
    async def list_services():
        """List available services and their health status."""
        services = []
        
        for service_name, service_url in SERVICE_ENDPOINTS.items():
            try:
                # Simple health check
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{service_url}/health", timeout=5.0)
                    status = "healthy" if response.status_code == 200 else "unhealthy"
            except:
                status = "unreachable"
            
            services.append({
                "name": service_name,
                "url": service_url,
                "status": status
            })
        
        return {"services": services}