"""
API middleware for the Robot Arm Control System.

This module provides middleware for request/response handling,
including error handling and logging.
"""

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging API requests and responses."""
    
    def __init__(self, app: ASGIApp):
        """Initialize the middleware."""
        super().__init__(app)
        self.logger = logging.getLogger(__name__)
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process the request and log relevant information."""
        start_time = time.time()
        
        # Log request
        self.logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'Unknown'}"
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            self.logger.info(
                f"Response: {response.status_code} "
                f"Process Time: {process_time:.3f}s"
            )
            
            # Add processing time header
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log error
            self.logger.error(f"Error processing request: {str(e)}")
            raise 