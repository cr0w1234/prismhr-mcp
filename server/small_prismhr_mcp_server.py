import asyncio
import logging
import os
from fastmcp import FastMCP 
import json
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("PrismHR MCP Server", stateless_http=True)

load_dotenv(override=True)

def authenticate_prismhr(username, password, peo_id, base_url="https://salesdemoapi.prismhr.com/prismhr-api"):
    """
    Authenticate with PrismHR API and return session ID
    
    Args:
        username: PrismHR web service username
        password: PrismHR web service password
        peo_id: PEO identifier
        base_url: Base URL for PrismHR API
        
    Returns:
        str: Session ID if successful, None if failed
    """
    auth_url = f"{base_url}/services/rest/login/v1/createPeoSession"
    auth_data = urllib.parse.urlencode({
        "username": username,
        "password": password,
        "peoId": peo_id
    }).encode('utf-8')
    
    auth_request = urllib.request.Request(
        auth_url,
        data=auth_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(auth_request, timeout=30) as response:
            auth_result = json.loads(response.read().decode('utf-8'))
        
        if auth_result.get("errorCode") == "0":
            return auth_result.get("sessionId")
        else:
            logger.error(f"Authentication failed: {auth_result.get('errorMessage', 'Unknown error')}")
            return None
            
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        return None

'''
@mcp.tool()
def request_pto(
    client_id: str,
    employee_id: str, 
    absence_code: str,
    start_date: str,
    end_date: str,
    leave_details: List[Dict[str, Any]],
    comment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Request PTO (Paid Time Off) for an employee using the PrismHR API
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier  
        absence_code: PTO register type code for the leave request
        start_date: Date on which the PTO begins (YYYY-MM-DD format)
        end_date: Date on which the PTO ends (YYYY-MM-DD format)
        leave_details: List of leave detail objects with "leaveDate" and "leaveHours"
        comment: Optional employee comments regarding the PTO request
        
    Returns:
        Dictionary containing the result of the operation with success status and response data
    """
    try:
        # Get credentials from environment variables
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {
                "success": False,
                "error": "Missing PrismHR credentials. Please set PRISMHR_USERNAME, PRISMHR_PASSWORD, and PRISMHR_PEO_ID environment variables."
            }
        
        # Authenticate
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {
                "success": False,
                "error": "Authentication failed"
            }
        
        # Make PTO request
        url = f"{base_url}/services/rest/employee/v1/requestPTO"
        
        request_body = {
            "sessionId": session_id,
            "clientId": client_id,
            "employeeId": employee_id,
            "absenceCode": absence_code,
            "startDate": start_date,
            "endDate": end_date,
            "leaveDetails": leave_details
        }
        
        if comment:
            request_body["comment"] = comment
        
        json_data = json.dumps(request_body).encode('utf-8')
        request = urllib.request.Request(
            url,
            data=json_data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        if result.get("errorCode") == "0":
            return {
                "success": True,
                "response": result,
                "message": "PTO request submitted successfully"
            }
        else:
            error_message = result.get("errorMessage", "Failed to request PTO")
            return {
                "success": False,
                "error": error_message,
                "response": result
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_result = json.loads(error_body)
            error_message = error_result.get("errorMessage", "HTTP Error")
            return {
                "success": False,
                "error": error_message,
                "response": error_result
            }
        except:
            return {
                "success": False,
                "error": f"HTTP Error {e.code}: {e.reason}"
            }
            
    except Exception as e:
        logger.error(f"PTO request failed: {e}")
        return {
            "success": False,
            "error": f"PTO request failed: {e}"
        }
'''

@mcp.tool()
def get_employee_list(client_id: str, status_class: Optional[str] = None, type_class: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a list of employees for a client using the actual PrismHR API
    
    Args:
        client_id: Client identifier
        status_class: Optional filter by employee status (A=Active, L=Leave, T=Terminated)
        type_class: Optional filter by employee type (F=Full-time, P=Part-time)
        
    Returns:
        Dictionary containing the list of employees
    """
    try:
        # Get credentials from environment variables
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getEmployeeList"
        params = {
            "clientId": client_id
        }
        
        if status_class:
            params["statusClass"] = status_class
        if type_class:
            params["typeClass"] = type_class
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        request = urllib.request.Request(
            full_url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
            
    except Exception as e:
        logger.error(f"Get employee list failed: {e}")
        return {"error": f"Get employee list failed: {e}"}

@mcp.tool()
def get_employee(client_id: str, employee_id: str, options: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed information for a specific employee using the actual PrismHR API
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier (can be a single ID or comma-separated list)
        options: Optional data options (Person, Client, Compensation, etc.)
        
    Returns:
        Dictionary containing detailed employee information
    """
    try:
        # Get credentials from environment variables
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getEmployee"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if options:
            params["options"] = options
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        request = urllib.request.Request(
            full_url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
            
    except Exception as e:
        logger.error(f"Get employee failed: {e}")
        return {"error": f"Get employee failed: {e}"}

@mcp.tool()
def test_connection() -> Dict[str, Any]:
    """
    Test the connection to PrismHR API by attempting authentication
    
    Returns:
        Dictionary containing connection test results
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD")
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {
                "success": False,
                "error": "Missing PrismHR credentials. Please set PRISMHR_USERNAME, PRISMHR_PASSWORD, and PRISMHR_PEO_ID environment variables.",
                "credentials_status": {
                    "username": bool(username),
                    "password": bool(password),
                    "peo_id": bool(peo_id)
                }
            }
        
        # Test authentication
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        
        if session_id:
            return {
                "success": True,
                "message": "Connection test successful",
                "session_id": session_id,
                "base_url": base_url
            }
        else:
            return {
                "success": False,
                "error": "Authentication failed - check credentials",
                "base_url": base_url
            }
            
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return {
            "success": False,
            "error": f"Connection test failed: {e}"
        }

if __name__ == "__main__":
    logger.info(f"🚀 PrismHR MCP server starting on port {os.getenv('PORT', 8080)}")
    
    try:
        # Run the MCP server
        asyncio.run(
            mcp.run_async(
                transport="streamable-http",
                host="0.0.0.0",
                port=int(os.getenv("PORT", "8080")),
            )
        )
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        raise
