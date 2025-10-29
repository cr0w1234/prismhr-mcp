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

# Batch 1: First 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_job_applicant_list(
    client_id: str, 
    applicant_id: Optional[str] = None, 
    apply_date: Optional[str] = None, 
    last_name: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of job applicants
    
    Args:
        client_id: Client identifier (up to 20 IDs can be passed, separated by commas)
        applicant_id: Applicant ID (optional)
        apply_date: Application date in YYYY-MM-DD format (optional)
        last_name: Applicant last name (optional)
        count: Number of records returned per page (optional)
        startpage: Pagination start location, first page = '0' (optional)
        
    Returns:
        Dictionary containing list of job applicants
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/applicant/v1/getJobApplicantList"
        params = {"clientId": client_id}
        
        if applicant_id:
            params["applicantId"] = applicant_id
        if apply_date:
            params["applyDate"] = apply_date
        if last_name:
            params["lastName"] = last_name
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get job applicant list failed: {e}")
        return {"error": f"Get job applicant list failed: {e}"}

@mcp.tool()
def get_job_applicants(client_id: str, applicant_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Get job applicants
    
    Args:
        client_id: Client identifier
        applicant_id: Applicant identifier (optional)
        
    Returns:
        Dictionary containing job applicant information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/applicant/v1/getJobApplicants"
        params = {"clientId": client_id}
        
        if applicant_id:
            params["id"] = applicant_id
        
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
        logger.error(f"Get job applicants failed: {e}")
        return {"error": f"Get job applicants failed: {e}"}

@mcp.tool()
def get_benefit_enrollment_status(
    client_id: str, 
    employee_id: Optional[str] = None, 
    enrollment_type: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get benefit enrollment status
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier (optional)
        enrollment_type: Enrollment type (optional)
        count: Number of records returned per page (optional)
        startpage: Pagination start location (optional)
        
    Returns:
        Dictionary containing benefit enrollment status
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/benefitEnrollmentStatus"
        params = {"clientId": client_id}
        
        if employee_id:
            params["employeeId"] = employee_id
        if enrollment_type:
            params["enrollmentType"] = enrollment_type
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get benefit enrollment status failed: {e}")
        return {"error": f"Get benefit enrollment status failed: {e}"}

@mcp.tool()
def get_401k_match_rules(
    client_id: str, 
    benefit_group_id: str, 
    retirement_plan_id: str
) -> Dict[str, Any]:
    """
    Get client's 401(k) match rules
    
    Args:
        client_id: Client identifier
        benefit_group_id: Benefit group identifier
        retirement_plan_id: Retirement plan identifier
        
    Returns:
        Dictionary containing 401(k) match rules
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/get401KMatchRules"
        params = {
            "clientId": client_id,
            "benefitGroupId": benefit_group_id,
            "retirementPlanId": retirement_plan_id
        }
        
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
        logger.error(f"Get 401k match rules failed: {e}")
        return {"error": f"Get 401k match rules failed: {e}"}

@mcp.tool()
def get_aca_offered_employees(
    client_id: str, 
    employee_id: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get ACA offered employees
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier (optional)
        count: Number of employees returned per page (optional)
        startpage: Pagination start location (optional)
        
    Returns:
        Dictionary containing ACA offered employees information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getACAOfferedEmployees"
        params = {"clientId": client_id}
        
        if employee_id:
            params["employeeId"] = employee_id
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get ACA offered employees failed: {e}")
        return {"error": f"Get ACA offered employees failed: {e}"}

# Batch 2: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_absence_journal(
    client_id: str, 
    journal_id: List[str]
) -> Dict[str, Any]:
    """
    Get absence journals
    
    Args:
        client_id: Client identifier
        journal_id: Absence journal identifier(s) - up to 20 journals
        
    Returns:
        Dictionary containing absence journal information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getAbsenceJournal"
        params = {
            "clientId": client_id,
            "journalId": journal_id
        }
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get absence journal failed: {e}")
        return {"error": f"Get absence journal failed: {e}"}

@mcp.tool()
def get_absence_journal_by_date(
    client_id: str, 
    journal_date_start: str, 
    journal_date_end: str, 
    employee_id: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get absence journals by date range
    
    Args:
        client_id: Client identifier
        journal_date_start: Absence journals date range starting date (YYYY-MM-DD format)
        journal_date_end: Absence journals date range ending date (YYYY-MM-DD format)
        employee_id: Return only records for the specified employee (optional)
        count: Number of absence journal records returned per page (optional)
        startpage: Pagination start location, first page = '0' (optional)
        
    Returns:
        Dictionary containing absence journal information by date
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getAbsenceJournalByDate"
        params = {
            "clientId": client_id,
            "journalDateStart": journal_date_start,
            "journalDateEnd": journal_date_end
        }
        
        if employee_id:
            params["employeeId"] = employee_id
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get absence journal by date failed: {e}")
        return {"error": f"Get absence journal by date failed: {e}"}

@mcp.tool()
def get_active_benefit_plans(
    client_id: str, 
    employee_id: str, 
    plan_id: Optional[List[str]] = None, 
    effective_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get active benefit plans for an employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        plan_id: List of benefit plan IDs (optional)
        effective_date: YYYY-MM-DD formatted string (optional)
        
    Returns:
        Dictionary containing active benefit plans information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getActiveBenefitPlans"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if plan_id:
            params["planId"] = plan_id
        if effective_date:
            params["effectiveDate"] = effective_date
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get active benefit plans failed: {e}")
        return {"error": f"Get active benefit plans failed: {e}"}

@mcp.tool()
def get_available_benefit_plans(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get available benefit plans for the specified employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing available benefit plans information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getAvailableBenefitPlans"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get available benefit plans failed: {e}")
        return {"error": f"Get available benefit plans failed: {e}"}

@mcp.tool()
def get_benefit_adjustments(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get benefit adjustment information for a specified employee
    
    Args:
        client_id: Client identifier associated with the employee
        employee_id: Employee whose benefits adjustments should be retrieved
        
    Returns:
        Dictionary containing benefit adjustment information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getBenefitAdjustments"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get benefit adjustments failed: {e}")
        return {"error": f"Get benefit adjustments failed: {e}"}

# Batch 3: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_benefit_confirmation_data(
    client_id: str, 
    employee_id: str, 
    confirm_num: str, 
    download_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Download benefits confirmation statement
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        confirm_num: Benefits confirmation code
        download_id: Identifier used to check status of / download data (optional)
        
    Returns:
        Dictionary containing benefit confirmation data
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getBenefitConfirmationData"
        params = {
            "clientId": client_id,
            "employeeId": employee_id,
            "confirmNum": confirm_num
        }
        
        if download_id:
            params["downloadId"] = download_id
        
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
        logger.error(f"Get benefit confirmation data failed: {e}")
        return {"error": f"Get benefit confirmation data failed: {e}"}

@mcp.tool()
def get_benefit_confirmation_list(
    client_id: str, 
    employee_id: str, 
    year: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of benefit confirmation
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        year: Specify a year (in YYYY format) to only return confirmations from that year (optional)
        
    Returns:
        Dictionary containing benefit confirmation list
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getBenefitConfirmationList"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if year:
            params["year"] = year
        
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
        logger.error(f"Get benefit confirmation list failed: {e}")
        return {"error": f"Get benefit confirmation list failed: {e}"}

@mcp.tool()
def get_benefit_plan_list() -> Dict[str, Any]:
    """
    Get a list of group benefit plans
    
    Returns:
        Dictionary containing list of system level benefit plans
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getBenefitPlanList"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get benefit plan list failed: {e}")
        return {"error": f"Get benefit plan list failed: {e}"}

@mcp.tool()
def get_benefit_plans(
    client_id: str, 
    employee_id: str, 
    plan_id: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get benefit plans for the specified employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        plan_id: List of benefit plan IDs (optional)
        
    Returns:
        Dictionary containing benefit plans information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getBenefitPlans"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if plan_id:
            params["planId"] = plan_id
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get benefit plans failed: {e}")
        return {"error": f"Get benefit plans failed: {e}"}

@mcp.tool()
def get_benefit_rule(
    client_id: str, 
    group_plan_id: Optional[str] = None, 
    plan_id: Optional[str] = None, 
    effective_date: Optional[str] = None, 
    use_actual_effective_date: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get benefit rule
    
    Args:
        client_id: Client identifier
        group_plan_id: Identifier for client's benefit group, or employee ID if the rule is an employee-specific override (optional)
        plan_id: Identifier for the group benefit plan (optional)
        effective_date: Format YYYY-MM-DD (optional)
        use_actual_effective_date: When calculating contributions, whether to use the current effective date (false, default behavior) or the effective date of each individual benefit rule (true) (optional)
        
    Returns:
        Dictionary containing benefit rule information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getBenefitRule"
        params = {"clientId": client_id}
        
        if group_plan_id:
            params["groupPlanId"] = group_plan_id
        if plan_id:
            params["planId"] = plan_id
        if effective_date:
            params["effectiveDate"] = effective_date
        if use_actual_effective_date is not None:
            params["useActualEffectiveDate"] = str(use_actual_effective_date).lower()
        
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
        logger.error(f"Get benefit rule failed: {e}")
        return {"error": f"Get benefit rule failed: {e}"}

# Batch 4: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_benefit_workflow_grid(
    client_id: Optional[str] = None, 
    download_id: Optional[str] = None, 
    workflow_eff_date: Optional[str] = None, 
    workflow_level: Optional[str] = None, 
    oe_start_date: Optional[str] = None, 
    oe_end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get client benefit workflow grid
    
    Args:
        client_id: Client identifier (optional)
        download_id: Identifier used to check status of / download data (optional)
        workflow_eff_date: YYYY-MM-DD formatted string (optional)
        workflow_level: Workflow level: system-level (S), client-level (C), or both (B) (optional)
        oe_start_date: YYYY-MM-DD formatted string (optional)
        oe_end_date: YYYY-MM-DD formatted string (optional)
        
    Returns:
        Dictionary containing benefit workflow grid data
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getBenefitWorkflowGrid"
        params = {}
        
        if client_id:
            params["clientId"] = client_id
        if download_id:
            params["downloadId"] = download_id
        if workflow_eff_date:
            params["workflowEffDate"] = workflow_eff_date
        if workflow_level:
            params["workflowLevel"] = workflow_level
        if oe_start_date:
            params["oeStartDate"] = oe_start_date
        if oe_end_date:
            params["oeEndDate"] = oe_end_date
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}" if query_string else url
        
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
        logger.error(f"Get benefit workflow grid failed: {e}")
        return {"error": f"Get benefit workflow grid failed: {e}"}

@mcp.tool()
def get_benefits_enrollment_trace(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get employee's benefit enrollment workflow
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing benefit enrollment workflow trace data
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getBenefitsEnrollmentTrace"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get benefits enrollment trace failed: {e}")
        return {"error": f"Get benefits enrollment trace failed: {e}"}

@mcp.tool()
def get_client_benefit_plan_setup_details(
    client_id: str, 
    plan_id: str, 
    plan_class: str
) -> Dict[str, Any]:
    """
    Get client benefit plan setup details
    
    Args:
        client_id: Client identifier
        plan_id: Plan identifier
        plan_class: Plan classification must be one of: 'G' (Group Benefits), 'R' (Retirement), 'F' (Flex Spending), 'M' (Employer Match), or 'H' (HSA)
        
    Returns:
        Dictionary containing client benefit plan setup details
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getClientBenefitPlanSetupDetails"
        params = {
            "clientId": client_id,
            "planId": plan_id,
            "planClass": plan_class
        }
        
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
        logger.error(f"Get client benefit plan setup details failed: {e}")
        return {"error": f"Get client benefit plan setup details failed: {e}"}

@mcp.tool()
def get_client_benefit_plans(
    client_id: str
) -> Dict[str, Any]:
    """
    Get client benefit plans
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing all benefit plans available to a client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getClientBenefitPlans"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get client benefit plans failed: {e}")
        return {"error": f"Get client benefit plans failed: {e}"}

@mcp.tool()
def get_cobra_codes() -> Dict[str, Any]:
    """
    Get Cobra Codes
    
    Returns:
        Dictionary containing list of qualifying events and termination reasons found in the Cobra processing parameters
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getCobraCodes"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get cobra codes failed: {e}")
        return {"error": f"Get cobra codes failed: {e}"}

# Batch 5: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_cobra_employee(
    employee_id: str
) -> Dict[str, Any]:
    """
    Get Cobra Employee
    
    Args:
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing COBRA benefit plan enrollment information about qualified employees
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getCobraEmployee"
        params = {"employeeId": employee_id}
        
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
        logger.error(f"Get cobra employee failed: {e}")
        return {"error": f"Get cobra employee failed: {e}"}

@mcp.tool()
def get_dependents(
    client_id: str, 
    employee_id: str, 
    dependent_id: Optional[str] = None, 
    only_active: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get dependent information for an employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        dependent_id: Dependent identifier (optional)
        only_active: Indicates whether the operation should return only active dependents. Valid values are true, false, or empty (optional)
        
    Returns:
        Dictionary containing information about the specified employee's dependents
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getDependents"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if dependent_id:
            params["dependentId"] = dependent_id
        if only_active:
            params["onlyActive"] = only_active
        
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
        logger.error(f"Get dependents failed: {e}")
        return {"error": f"Get dependents failed: {e}"}

@mcp.tool()
def get_disability_plan_enrollment_details(
    group_benefit_plan_id: str, 
    effective_date: Optional[str] = None, 
    from_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get benefit enrollment plan details for disability plans
    
    Args:
        group_benefit_plan_id: Benefit plan ID; must be a disability plan, with offerType="LTD" or "STD"
        effective_date: Specify a plan effective date (format: YYYY-MM-DD) to return only plans for that date (optional)
        from_date: Specify a date (format: YYYY-MM-DD) to return benefit plan enrollment records with effective dates on or after this date (optional)
        
    Returns:
        Dictionary containing coverage amounts and other enrollment details for disability plans
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getDisabilityPlanEnrollmentDetails"
        params = {"groupBenefitPlanId": group_benefit_plan_id}
        
        if effective_date:
            params["effectiveDate"] = effective_date
        if from_date:
            params["fromDate"] = from_date
        
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
        logger.error(f"Get disability plan enrollment details failed: {e}")
        return {"error": f"Get disability plan enrollment details failed: {e}"}

@mcp.tool()
def get_eligible_flex_spending_plans(
    client_id: str, 
    employee_id: str, 
    as_of_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get eligible flex spending plans for an employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        as_of_date: Date to use when calculating an employee's eligibility. Defaults to today's date (optional)
        
    Returns:
        Dictionary containing list of FSA and HSA plans for which an employee is eligible
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getEligibleFlexSpendingPlans"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if as_of_date:
            params["asOfDate"] = as_of_date
        
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
        logger.error(f"Get eligible flex spending plans failed: {e}")
        return {"error": f"Get eligible flex spending plans failed: {e}"}

@mcp.tool()
def get_eligible_zip_codes(
    plan_id: str
) -> Dict[str, Any]:
    """
    Get eligible zip codes
    
    Args:
        plan_id: Group benefit plan identifier
        
    Returns:
        Dictionary containing list of eligible zip codes for a Group Benefit Plan
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getEligibleZipCodes"
        params = {"planId": plan_id}
        
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
        logger.error(f"Get eligible zip codes failed: {e}")
        return {"error": f"Get eligible zip codes failed: {e}"}

# Batch 6: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_employee_premium(
    client_id: str, 
    employee_id: str, 
    effective_date: str, 
    plan_id: str, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate an employee's premium rates
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        effective_date: Date to use when calculating the employee's premium
        plan_id: Benefit plan identifier
        options: A string containing zero or more of the keywords: PremiumRates, ContributionRates (optional)
        
    Returns:
        Dictionary containing calculated billing rates and optionally premium and contribution rates
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getEmployeePremium"
        params = {
            "clientId": client_id,
            "employeeId": employee_id,
            "effectiveDate": effective_date,
            "planId": plan_id
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
        logger.error(f"Get employee premium failed: {e}")
        return {"error": f"Get employee premium failed: {e}"}

@mcp.tool()
def get_employee_retirement_summary(
    client_id: str, 
    employee_id: str, 
    plan_id: str, 
    plan_year: str
) -> Dict[str, Any]:
    """
    Get employee retirement summary
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        plan_id: Plan identifier
        plan_year: Plan year
        
    Returns:
        Dictionary containing details of the retirement benefits for an employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getEmployeeRetirementSummary"
        params = {
            "clientId": client_id,
            "employeeId": employee_id,
            "planId": plan_id,
            "planYear": plan_year
        }
        
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
        logger.error(f"Get employee retirement summary failed: {e}")
        return {"error": f"Get employee retirement summary failed: {e}"}

@mcp.tool()
def get_enroll_input_list(
    client_id: str, 
    employee_id: str, 
    plan_id: str
) -> Dict[str, Any]:
    """
    Get required input elements to enroll specified employee in benefit plan
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        plan_id: Group benefit plan identifier
        
    Returns:
        Dictionary containing elements that are required to enroll the employee in the specified group benefit plan
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getEnrollInputList"
        params = {
            "clientId": client_id,
            "employeeId": employee_id,
            "planId": plan_id
        }
        
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
        logger.error(f"Get enroll input list failed: {e}")
        return {"error": f"Get enroll input list failed: {e}"}

@mcp.tool()
def get_enrollment_plan_details(
    plan_id: str, 
    offer_type: str, 
    effective_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get benefit enrollment plan details
    
    Args:
        plan_id: Benefit plan identifier
        offer_type: Group benefit plan offer type (Examples: MED, DEN, VIS, LIF)
        effective_date: Enter a date to return only plans associated with that effective date or dates following it (optional)
        
    Returns:
        Dictionary containing benefit plan information from the benefit carrier, including deductibles, copay amounts, and visit types
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getEnrollmentPlanDetails"
        params = {
            "planId": plan_id,
            "offerType": offer_type
        }
        
        if effective_date:
            params["effectiveDate"] = effective_date
        
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
        logger.error(f"Get enrollment plan details failed: {e}")
        return {"error": f"Get enrollment plan details failed: {e}"}

@mcp.tool()
def get_fsa_reimbursements(
    client_id: str, 
    employee_id: str, 
    plan_year: Optional[str] = None, 
    account_type: Optional[str] = None, 
    ref_number: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get flexible spending account (FSA) reimbursement for an employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        plan_year: Enter an FSA plan year to only return data associated with that plan year (optional)
        account_type: Enter a flexible spending account type to only return data associated with accounts of that type (optional)
        ref_number: Enter a reference number to only return information about the reimbursement associated with that number (optional)
        
    Returns:
        Dictionary containing information about FSA plan reimbursements for specific employees and clients
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getFSAReimbursements"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if plan_year:
            params["planYear"] = plan_year
        if account_type:
            params["accountType"] = account_type
        if ref_number:
            params["refNumber"] = ref_number
        
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
        logger.error(f"Get FSA reimbursements failed: {e}")
        return {"error": f"Get FSA reimbursements failed: {e}"}

# Batch 7: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_flex_plans(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get flexible spending plan enrollment for the specified employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing flexible spending plan enrollment information for the specified employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getFlexPlans"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get flex plans failed: {e}")
        return {"error": f"Get flex plans failed: {e}"}

@mcp.tool()
def get_group_benefit_plan(
    plan_id: str
) -> Dict[str, Any]:
    """
    Get group benefit plan details
    
    Args:
        plan_id: Plan identifier
        
    Returns:
        Dictionary containing details of the specified group benefit plan
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getGroupBenefitPlan"
        params = {"planId": plan_id}
        
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
        logger.error(f"Get group benefit plan failed: {e}")
        return {"error": f"Get group benefit plan failed: {e}"}

@mcp.tool()
def get_group_benefit_rates(
    plan_id: str, 
    date: Optional[str] = None, 
    rate_group: Optional[str] = None, 
    network_id: Optional[str] = None, 
    plan_type: Optional[str] = None, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get premium and billing rates for a benefit plan
    
    Args:
        plan_id: Group benefit plan id
        date: Effective date (optional)
        rate_group: Rate group (optional)
        network_id: Network id (optional)
        plan_type: Plan type (optional)
        options: A string containing zero or more of the keywords: BILLING, PREMIUM (optional)
        
    Returns:
        Dictionary containing premium and billing rates for a specific benefit plan
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getGroupBenefitRates"
        params = {"planId": plan_id}
        
        if date:
            params["date"] = date
        if rate_group:
            params["rateGroup"] = rate_group
        if network_id:
            params["networkId"] = network_id
        if plan_type:
            params["planType"] = plan_type
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
        logger.error(f"Get group benefit rates failed: {e}")
        return {"error": f"Get group benefit rates failed: {e}"}

@mcp.tool()
def get_group_benefit_types(
    type_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get group benefit type(s)
    
    Args:
        type_code: Group benefit plan type code (optional)
        
    Returns:
        Dictionary containing list of system-level group benefit plan type codes and their associated data
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getGroupBenefitTypes"
        params = {}
        
        if type_code:
            params["typeCode"] = type_code
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}" if query_string else url
        
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
        logger.error(f"Get group benefit types failed: {e}")
        return {"error": f"Get group benefit types failed: {e}"}

@mcp.tool()
def get_life_event_code_details(
    client_id: str, 
    life_event_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get life event code(s) information for a client
    
    Args:
        client_id: Client identifier
        life_event_code: Enter a life event code if you want to return information about only that code (optional)
        
    Returns:
        Dictionary containing information about life event codes or a specified life event code
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getLifeEventCodeDetails"
        params = {"clientId": client_id}
        
        if life_event_code:
            params["lifeEventCode"] = life_event_code
        
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
        logger.error(f"Get life event code details failed: {e}")
        return {"error": f"Get life event code details failed: {e}"}

# Batch 8: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_monthly_aca_info(
    client_id: str, 
    employee_id: List[str]
) -> Dict[str, Any]:
    """
    Get monthly employee ACA data
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier or identifiers (array)
        
    Returns:
        Dictionary containing monthly employee ACA data as calculated by the system for the current year
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getMonthlyACAInfo"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get monthly ACA info failed: {e}")
        return {"error": f"Get monthly ACA info failed: {e}"}

@mcp.tool()
def get_pto_requests_list(
    client_id: str, 
    employee_id: Optional[List[str]] = None, 
    statuses: Optional[str] = None, 
    leave_type: Optional[str] = None, 
    pto_starts_after_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get PTO Request List
    
    Args:
        client_id: Client identifier
        employee_id: List of employee IDs (optional)
        statuses: Optional. Filter by PTO request status. Enter one or more of: N (Pending), A (Approved), C (Cancelled), P (Paid), D (Denied) (optional)
        leave_type: Optional. Filter by this PTO type code (optional)
        pto_starts_after_date: Optional. Filter by PTO date range. Include only time off that starts after this date, in YYYY-MM-DD format (optional)
        
    Returns:
        Dictionary containing listing of all employee's leave requests for a client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPTORequestsList"
        params = {"clientId": client_id}
        
        if employee_id:
            params["employeeId"] = employee_id
        if statuses:
            params["statuses"] = statuses
        if leave_type:
            params["leaveType"] = leave_type
        if pto_starts_after_date:
            params["ptoStartsAfterDate"] = pto_starts_after_date
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get PTO requests list failed: {e}")
        return {"error": f"Get PTO requests list failed: {e}"}

@mcp.tool()
def get_paid_time_off(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get paid time off information
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing paid time off register information for the current year and basic summary information for prior years
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPaidTimeOff"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get paid time off failed: {e}")
        return {"error": f"Get paid time off failed: {e}"}

@mcp.tool()
def get_paid_time_off_plans(
    client_id: str
) -> Dict[str, Any]:
    """
    Get paid time off plans for the specified client
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing array of all available paid time off plans for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPaidTimeOffPlans"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get paid time off plans failed: {e}")
        return {"error": f"Get paid time off plans failed: {e}"}

@mcp.tool()
def get_plan_year_info(
    plan_type: Optional[str] = None, 
    plan_year: Optional[str] = None, 
    plan_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get benefit plan year data
    
    Args:
        plan_type: Provide a plan type to return only information for that type of plan. Valid types are F (retirement), H (HSA), and C (Section 125) (optional)
        plan_year: Provide a four-digit year to return only information for that year (optional)
        plan_id: Provide a plan ID to return only information for that benefit plan (optional)
        
    Returns:
        Dictionary containing benefit plan year data for retirement, HSA, and Section 125 plans
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPlanYearInfo"
        params = {}
        
        if plan_type:
            params["planType"] = plan_type
        if plan_year:
            params["planYear"] = plan_year
        if plan_id:
            params["planId"] = plan_id
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}" if query_string else url
        
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
        logger.error(f"Get plan year info failed: {e}")
        return {"error": f"Get plan year info failed: {e}"}

# Batch 9: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_pto_absence_codes(
    client_id: str, 
    absence_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get PTO absence codes for a client
    
    Args:
        client_id: Client identifier
        absence_code: Absence code identifier to get a single absence code (optional)
        
    Returns:
        Dictionary containing all PTO absence codes for a client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPtoAbsenceCodes"
        params = {"clientId": client_id}
        
        if absence_code:
            params["absenceCode"] = absence_code
        
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
        logger.error(f"Get PTO absence codes failed: {e}")
        return {"error": f"Get PTO absence codes failed: {e}"}

@mcp.tool()
def get_pto_auto_enroll_rules(
    client_id: str
) -> Dict[str, Any]:
    """
    Get PTO auto enroll rules for a client
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of PTO auto enroll rules for a client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPtoAutoEnrollRules"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get PTO auto enroll rules failed: {e}")
        return {"error": f"Get PTO auto enroll rules failed: {e}"}

@mcp.tool()
def get_pto_classes(
    client_id: str
) -> Dict[str, Any]:
    """
    Get paid time off classes for the specified client
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing all PTO classes for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPtoClasses"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get PTO classes failed: {e}")
        return {"error": f"Get PTO classes failed: {e}"}

@mcp.tool()
def get_pto_plan_details(
    client_id: str, 
    pto_plan_id: str
) -> Dict[str, Any]:
    """
    Get PTO plan details
    
    Args:
        client_id: Client identifier
        pto_plan_id: PTO plan identifier
        
    Returns:
        Dictionary containing information about a single PTO Benefit Plan
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPtoPlanDetails"
        params = {
            "clientId": client_id,
            "ptoPlanId": pto_plan_id
        }
        
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
        logger.error(f"Get PTO plan details failed: {e}")
        return {"error": f"Get PTO plan details failed: {e}"}

@mcp.tool()
def get_pto_register_types(
    client_id: str, 
    pto_type_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get PTO register types for a client
    
    Args:
        client_id: Client identifier
        pto_type_code: Single PTO type code to return (optional)
        
    Returns:
        Dictionary containing list of PTO register types for a client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getPtoRegisterTypes"
        params = {"clientId": client_id}
        
        if pto_type_code:
            params["ptoTypeCode"] = pto_type_code
        
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
        logger.error(f"Get PTO register types failed: {e}")
        return {"error": f"Get PTO register types failed: {e}"}

# Batch 10: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_retirement_loans(
    client_id: str, 
    employee_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get retirement loans for the specified employee or a client
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier to retrieve loans for that employee (optional)
        
    Returns:
        Dictionary containing retirement loan information for the specified employee or client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getRetirementLoans"
        params = {"clientId": client_id}
        
        if employee_id:
            params["employeeId"] = employee_id
        
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
        logger.error(f"Get retirement loans failed: {e}")
        return {"error": f"Get retirement loans failed: {e}"}

@mcp.tool()
def get_retirement_plan(
    client_id: str, 
    employee_id: str, 
    effective_date: Optional[str] = None, 
    is_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get active retirement plans for an employee
    
    Args:
        client_id: Client identifier
        employee_id: PrismHR employee id
        effective_date: YYYY-MM-DD formatted string (optional)
        is_active: If isActive is set to true, we will only return retirement plan details that are active from today's date or the effective date entered. Default is false which will return all detail information (optional)
        
    Returns:
        Dictionary containing retirement plan(s) that are currently active for the specified employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getRetirementPlan"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if effective_date:
            params["effectiveDate"] = effective_date
        if is_active is not None:
            params["isActive"] = str(is_active).lower()
        
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
        logger.error(f"Get retirement plan failed: {e}")
        return {"error": f"Get retirement plan failed: {e}"}

@mcp.tool()
def get_section125_plans(
    plan_type: str, 
    plan_id: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get HSA/Section 125 plan details
    
    Args:
        plan_type: Type of plan to return; valid values are H (HSA) and C (Section 125)
        plan_id: Specify a plan ID to return only data about that plan (optional)
        count: Number of plans returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing data about Health Savings Account (HSA) benefit plans and Section 125 plans
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/getSection125Plans"
        params = {"planType": plan_type}
        
        if plan_id:
            params["planId"] = plan_id
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get section 125 plans failed: {e}")
        return {"error": f"Get section 125 plans failed: {e}"}

@mcp.tool()
def get_retirement_census_export(
    report_format: str, 
    plan_id: str, 
    client_id: Optional[str] = None, 
    download_id: Optional[str] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Download retirement census report
    
    Args:
        report_format: Report format: Census, Participants, or Eligibility
        plan_id: Retirement plan identifier; enter a single retirement plan ID or ALL for all plans
        client_id: Client identifier (optional)
        download_id: Identifier used to check status of / download data (optional)
        start_date: Start date for the report (optional)
        end_date: End date for the report (optional)
        count: Number of records per page (optional)
        startpage: Pagination start location (optional)
        
    Returns:
        Dictionary containing retirement census report data or download status
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/benefits/v1/retirementCensusExport"
        params = {
            "reportFormat": report_format,
            "planId": plan_id
        }
        
        if client_id:
            params["clientId"] = client_id
        if download_id:
            params["downloadId"] = download_id
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get retirement census export failed: {e}")
        return {"error": f"Get retirement census export failed: {e}"}

@mcp.tool()
def get_aca_large_employer(
    client_id: str, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get ACA large Employer
    
    Args:
        client_id: Client identifier; if the web service user has no client restrictions, enter "ALL" to return this information for all clients
        count: Number of records per page (optional)
        startpage: Pagination start location (optional)
        
    Returns:
        Dictionary containing information about ACA Large Employer status for one client or all clients
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getACALargeEmployer"
        params = {"clientId": client_id}
        
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get ACA large employer failed: {e}")
        return {"error": f"Get ACA large employer failed: {e}"}

# Batch 11: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_active_employee_count_by_entity(
    client_id: str, 
    entity_type: str, 
    include_obsolete: Optional[bool] = None, 
    download_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get active employee count by entity
    
    Args:
        client_id: List of up to ten client identifiers
        entity_type: Type of entity. Pass only one value. Allowed values: benefitGroup, department, division, location, position, project, shift, skill, workGroup
        include_obsolete: Whether to include obsolete entities (optional)
        download_id: Identifier used to check status of / download data (optional)
        
    Returns:
        Dictionary containing count of active employees, broken down by entityId, for one or more clients
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getActiveEmployeeCountByEntity"
        params = {
            "clientId": client_id,
            "entityType": entity_type
        }
        
        if include_obsolete is not None:
            params["includeObsolete"] = str(include_obsolete).lower()
        if download_id:
            params["downloadId"] = download_id
        
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
        logger.error(f"Get active employee count by entity failed: {e}")
        return {"error": f"Get active employee count by entity failed: {e}"}

@mcp.tool()
def get_all_prism_client_contacts(
    client_id: str
) -> Dict[str, Any]:
    """
    Get all Prism client contacts
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing information of all contacts for a specific client managed in the PrismHR product
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getAllPrismClientContacts"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get all Prism client contacts failed: {e}")
        return {"error": f"Get all Prism client contacts failed: {e}"}

@mcp.tool()
def get_backup_assignments(
    client_id: str
) -> Dict[str, Any]:
    """
    Get Backup Assignments
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of backup users for the various Account Assignment roles for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getBackupAssignments"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get backup assignments failed: {e}")
        return {"error": f"Get backup assignments failed: {e}"}

@mcp.tool()
def get_benefit_group(
    client_id: str, 
    group_id: List[str]
) -> Dict[str, Any]:
    """
    Get a benefit group
    
    Args:
        client_id: Client identifier
        group_id: Benefit group identifier(s) of the groups currently defined for the client
        
    Returns:
        Dictionary containing up to 20 of the specified client company's benefit groups, including the groups' basic definitions, as well as associated group benefit plans and cafeteria plan contributions
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getBenefitGroup"
        params = {
            "clientId": client_id,
            "groupId": group_id
        }
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get benefit group failed: {e}")
        return {"error": f"Get benefit group failed: {e}"}

@mcp.tool()
def get_bill_pending(
    client_id: str, 
    status: Optional[str] = None, 
    start_bill_date: Optional[str] = None, 
    end_bill_date: Optional[str] = None, 
    event: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get bill pending record
    
    Args:
        client_id: Client identifier
        status: Only return bill pending items in a particular status. Options are Pending, Complete, or All (default) (optional)
        start_bill_date: Enter a date to only return bill pending items created on or after that date (optional)
        end_bill_date: Enter a date to only return bill pending items created on or before that date (optional)
        event: Enter an event to only return bill pending items associated with that event code (optional)
        
    Returns:
        Dictionary containing data associated with line items in the Client Bill Pending record
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getBillPending"
        params = {"clientId": client_id}
        
        if status:
            params["status"] = status
        if start_bill_date:
            params["startBillDate"] = start_bill_date
        if end_bill_date:
            params["endBillDate"] = end_bill_date
        if event:
            params["event"] = event
        
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
        logger.error(f"Get bill pending failed: {e}")
        return {"error": f"Get bill pending failed: {e}"}

# Batch 12: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_bundled_billing_rule(
    client_id: str, 
    billing_rule: Optional[str] = None, 
    wc_code: Optional[str] = None, 
    state: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get bundled billing rule(s)
    
    Args:
        client_id: Client identifier
        billing_rule: Enter a billing rule id to return a specific bundled billing rule (optional)
        wc_code: Only return bundled billing rules for the workers' compensation code (optional)
        state: Only return bundled billing rules for the associate state in the workers' compensation code (optional)
        
    Returns:
        Dictionary containing bundled billing rules information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getBundledBillingRule"
        params = {"clientId": client_id}
        
        if billing_rule:
            params["billingRule"] = billing_rule
        if wc_code:
            params["wcCode"] = wc_code
        if state:
            params["state"] = state
        
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
        logger.error(f"Get bundled billing rule failed: {e}")
        return {"error": f"Get bundled billing rule failed: {e}"}

@mcp.tool()
def get_client_billing_bank_account(
    client_id: str
) -> Dict[str, Any]:
    """
    Get client billing bank account
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing client billing bank account information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getClientBillingBankAccount"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get client billing bank account failed: {e}")
        return {"error": f"Get client billing bank account failed: {e}"}

@mcp.tool()
def get_client_codes(
    client_id: str, 
    options: str, 
    exclude_obsolete: Optional[bool] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get code tables for the specified client
    
    Args:
        client_id: Client identifier
        options: Single string containing one or more of the options mentioned in notes section (e.g., "BenefitGroup,Department,Pay")
        exclude_obsolete: Use to exclude obsolete codes. Flag only applies for BenefitGroup, Deduction, Department, Division, Job, Location, Pay, Project, Reason, Relation, Status, Type, Workgroup options (optional)
        count: Number of codes returned per page (currently only available for Project option) (optional)
        startpage: Pagination start location (first page = '0') (currently only applies for Project option) (optional)
        
    Returns:
        Dictionary containing one or more code tables as arrays (lists) for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getClientCodes"
        params = {
            "clientId": client_id,
            "options": options
        }
        
        if exclude_obsolete is not None:
            params["excludeObsolete"] = str(exclude_obsolete).lower()
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get client codes failed: {e}")
        return {"error": f"Get client codes failed: {e}"}

@mcp.tool()
def get_client_events(
    client_id: str, 
    organizer: Optional[str] = None, 
    from_date: Optional[str] = None, 
    thru_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get client specific events
    
    Args:
        client_id: Client whose events you want to retrieve
        organizer: Enter an organizer if you want to only return events associated with them (optional)
        from_date: Enter a date if you want to only return events that occur from this date (optional)
        thru_date: Enter a date if you want to only return events that occur through this date (optional)
        
    Returns:
        Dictionary containing client events and the data associated with those events
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getClientEvents"
        params = {"clientId": client_id}
        
        if organizer:
            params["organizer"] = organizer
        if from_date:
            params["fromDate"] = from_date
        if thru_date:
            params["thruDate"] = thru_date
        
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
        logger.error(f"Get client events failed: {e}")
        return {"error": f"Get client events failed: {e}"}

@mcp.tool()
def get_client_list(
    in_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get clients list
    
    Args:
        in_active: Use to indicate whether the operation should retrieve inactive clients instead of active clients (which is the default behavior) (optional)
        
    Returns:
        Dictionary containing an array of clients with clientId, clientName, legalName and status properties
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getClientList"
        params = {}
        
        if in_active is not None:
            params["inActive"] = str(in_active).lower()
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}" if query_string else url
        
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
        logger.error(f"Get client list failed: {e}")
        return {"error": f"Get client list failed: {e}"}

# Batch 13: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_client_location_details(
    client_id: str, 
    location_id: str
) -> Dict[str, Any]:
    """
    Get client location detail
    
    Args:
        client_id: Client identifier
        location_id: ID of the client's worksite location to retrieve
        
    Returns:
        Dictionary containing information about the specified client's worksite location
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getClientLocationDetails"
        params = {
            "clientId": client_id,
            "locationId": location_id
        }
        
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
        logger.error(f"Get client location details failed: {e}")
        return {"error": f"Get client location details failed: {e}"}

@mcp.tool()
def get_client_master(
    client_id: str
) -> Dict[str, Any]:
    """
    Get client master data
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing the entire Client Master data object for the specified client, as well as a checksum
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getClientMaster"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get client master failed: {e}")
        return {"error": f"Get client master failed: {e}"}

@mcp.tool()
def get_client_ownership(
    client_id: str
) -> Dict[str, Any]:
    """
    Get client ownership details
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing client ownership information as configured on the Client Details > Benefits tab
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getClientOwnership"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get client ownership failed: {e}")
        return {"error": f"Get client ownership failed: {e}"}

@mcp.tool()
def get_doc_expirations(
    client_id: str, 
    doc_types: str, 
    days_out: str, 
    employee_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Return docs that will expire within 'daysOut' days from current date
    
    Args:
        client_id: Client identifier
        doc_types: Type of document: 'I9' (Form I-9 documents) or 'SKILL' (skills from Employee Details)
        days_out: Number of days (for example, 42 to retrieve documents that have expired or will expire six weeks from today)
        employee_id: Employee identifier (optional)
        
    Returns:
        Dictionary containing a list of employees' documents with an expiration date on or before the specified numbers of days from the current date
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getDocExpirations"
        params = {
            "clientId": client_id,
            "docTypes": doc_types,
            "daysOut": days_out
        }
        
        if employee_id:
            params["employeeId"] = employee_id
        
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
        logger.error(f"Get doc expirations failed: {e}")
        return {"error": f"Get doc expirations failed: {e}"}

@mcp.tool()
def get_employee_list_by_entity(
    client_id: str, 
    entity_type: str, 
    entity_id: str, 
    status_class: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get employee list by entity
    
    Args:
        client_id: Client identifier
        entity_type: The type of entity specified by the entityId (location, division, workGroup, position, skill, shift, benefitGroup, project or department)
        entity_id: Entity identifier
        status_class: Specify a value to only return employees within that status class. Valid values are A (active), L (on leave), T (terminated), or a combination of these. If no value is specified, the method returns employees of all status classes (optional)
        
    Returns:
        Dictionary containing a list of employees associated with a particular client entity
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getEmployeeListByEntity"
        params = {
            "clientId": client_id,
            "entityType": entity_type,
            "entityId": entity_id
        }
        
        if status_class:
            params["statusClass"] = status_class
        
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
        logger.error(f"Get employee list by entity failed: {e}")
        return {"error": f"Get employee list by entity failed: {e}"}

# Batch 14: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_employees_in_pay_group(
    client_id: str, 
    pay_group: str
) -> Dict[str, Any]:
    """
    Get employees by pay group
    
    Args:
        client_id: Client identifier
        pay_group: Pay group identifier
        
    Returns:
        Dictionary containing a list of employees who are assigned to the specified pay group
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getEmployeesInPayGroup"
        params = {
            "clientId": client_id,
            "payGroup": pay_group
        }
        
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
        logger.error(f"Get employees in pay group failed: {e}")
        return {"error": f"Get employees in pay group failed: {e}"}

@mcp.tool()
def get_gl_cutback_check_post(
    gl_company: str, 
    tran_date: str
) -> Dict[str, Any]:
    """
    Get GLCutbackCheckPost
    
    Args:
        gl_company: Employer ID (GL company identifier)
        tran_date: Transaction date (date of the payroll), MM/DD/YY format
        
    Returns:
        Dictionary containing general ledger cutback check posting information for the specified employer
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getGLCutbackCheckPost"
        params = {
            "glCompany": gl_company,
            "tranDate": tran_date
        }
        
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
        logger.error(f"Get GL cutback check post failed: {e}")
        return {"error": f"Get GL cutback check post failed: {e}"}

@mcp.tool()
def get_gl_data(
    type: str
) -> Dict[str, Any]:
    """
    Get GL data
    
    Args:
        type: Type must be one of: 'Journal' (data available for journal posting), 'Invoice' (data available for invoice posting), or 'Cutback' (data available for check posting)
        
    Returns:
        Dictionary containing not-yet-posted transaction dates, employer IDs, and amounts associated with the specified type
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getGLData"
        params = {"type": type}
        
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
        logger.error(f"Get GL data failed: {e}")
        return {"error": f"Get GL data failed: {e}"}

@mcp.tool()
def get_gl_invoice_post(
    gl_company: str, 
    inv_date: str
) -> Dict[str, Any]:
    """
    Get GL invoice post
    
    Args:
        gl_company: Employer ID (GL company identifier)
        inv_date: Invoice date (date of the payroll), MM/DD/YY format
        
    Returns:
        Dictionary containing an employer's G/L invoice posting information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getGLInvoicePost"
        params = {
            "glCompany": gl_company,
            "invDate": inv_date
        }
        
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
        logger.error(f"Get GL invoice post failed: {e}")
        return {"error": f"Get GL invoice post failed: {e}"}

@mcp.tool()
def get_gl_journal_post(
    gl_company: str, 
    tran_date: str
) -> Dict[str, Any]:
    """
    Get GL journal post
    
    Args:
        gl_company: Employer ID (GL company identifier)
        tran_date: Transaction date (date of the payroll), MM/DD/YY format
        
    Returns:
        Dictionary containing external general ledger journal posting information for the specified employer
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getGLJournalPost"
        params = {
            "glCompany": gl_company,
            "tranDate": tran_date
        }
        
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
        logger.error(f"Get GL journal post failed: {e}")
        return {"error": f"Get GL journal post failed: {e}"}

# Batch 15: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_geo_locations(
    zip_code: str
) -> Dict[str, Any]:
    """
    Get GeoLocations matching for the ZIP code
    
    Args:
        zip_code: The five-digit ZIP code used to match GeoLocations
        
    Returns:
        Dictionary containing an array of all Vertex GeoLocations matching the specified ZIP code
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getGeoLocations"
        params = {"zipCode": zip_code}
        
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
        logger.error(f"Get geo locations failed: {e}")
        return {"error": f"Get geo locations failed: {e}"}

@mcp.tool()
def get_labor_allocations(
    client_id: str, 
    template_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of labor allocation templates
    
    Args:
        client_id: Client identifier
        template_id: Template identifier (optional)
        
    Returns:
        Dictionary containing a list of labor allocation templates
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getLaborAllocations"
        params = {"clientId": client_id}
        
        if template_id:
            params["templateId"] = template_id
        
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
        logger.error(f"Get labor allocations failed: {e}")
        return {"error": f"Get labor allocations failed: {e}"}

@mcp.tool()
def get_labor_union_details(
    client_id: str, 
    union_code: str
) -> Dict[str, Any]:
    """
    Get Labor Union Details
    
    Args:
        client_id: Client identifier
        union_code: Union code
        
    Returns:
        Dictionary containing details for a specific labor union configured in PrismHR
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getLaborUnionDetails"
        params = {
            "clientId": client_id,
            "unionCode": union_code
        }
        
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
        logger.error(f"Get labor union details failed: {e}")
        return {"error": f"Get labor union details failed: {e}"}

@mcp.tool()
def get_message_list(
    user_id: str, 
    from_date: Optional[str] = None, 
    to_date: Optional[str] = None, 
    un_read_only: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get message list
    
    Args:
        user_id: User identifier
        from_date: First date to retrieve, inclusive (format YYYY-MM-DD) (optional)
        to_date: Last date to retrieve, inclusive (format YYYY-MM-DD) (optional)
        un_read_only: Whether to return only unread messages (optional)
        
    Returns:
        Dictionary containing a list of messages without the body
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getMessageList"
        params = {"userId": user_id}
        
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        if un_read_only is not None:
            params["unReadOnly"] = str(un_read_only).lower()
        
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
        logger.error(f"Get message list failed: {e}")
        return {"error": f"Get message list failed: {e}"}

@mcp.tool()
def get_messages(
    user_id: str, 
    message_id: List[str]
) -> Dict[str, Any]:
    """
    Get messages
    
    Args:
        user_id: User identifier
        message_id: List of message IDs
        
    Returns:
        Dictionary containing an array of messages, including the body of the message (maximum 20 messages)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getMessages"
        params = {
            "userId": user_id,
            "messageId": message_id
        }
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get messages failed: {e}")
        return {"error": f"Get messages failed: {e}"}

# Batch 16: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_osha_300a_stats(
    client_id: str, 
    report_year: str, 
    location_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get OSHA 300A stats
    
    Args:
        client_id: Client identifier
        report_year: Report year
        location_code: Location code for report (optional)
        
    Returns:
        Dictionary containing OSHA 300A statistics for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getOSHA300Astats"
        params = {
            "clientId": client_id,
            "reportYear": report_year
        }
        
        if location_code:
            params["locationCode"] = location_code
        
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
        logger.error(f"Get OSHA 300A stats failed: {e}")
        return {"error": f"Get OSHA 300A stats failed: {e}"}

@mcp.tool()
def get_pay_day_rules(
    client_id: str
) -> Dict[str, Any]:
    """
    Return pay day rules for the client
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing pay day rules for the client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getPayDayRules"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get pay day rules failed: {e}")
        return {"error": f"Get pay day rules failed: {e}"}

@mcp.tool()
def get_pay_group_details(
    client_id: str, 
    pay_group_code: str
) -> Dict[str, Any]:
    """
    Get pay group details by pay group ID
    
    Args:
        client_id: Client identifier
        pay_group_code: Pay group identifier
        
    Returns:
        Dictionary containing the details of the specified pay group
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getPayGroupDetails"
        params = {
            "clientId": client_id,
            "payGroupCode": pay_group_code
        }
        
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
        logger.error(f"Get pay group details failed: {e}")
        return {"error": f"Get pay group details failed: {e}"}

@mcp.tool()
def get_payroll_schedule(
    client_id: str
) -> Dict[str, Any]:
    """
    Get pay group and pay schedule for the specified client
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing pay group and pay schedule information for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getPayrollSchedule"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get payroll schedule failed: {e}")
        return {"error": f"Get payroll schedule failed: {e}"}

@mcp.tool()
def get_prism_client_contact(
    client_id: str, 
    contact_id: str
) -> Dict[str, Any]:
    """
    Get a Prism client contact
    
    Args:
        client_id: Client identifier
        contact_id: ID of the contact at the specified client to retrieve
        
    Returns:
        Dictionary containing information for a particular contact at a specific client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getPrismClientContact"
        params = {
            "clientId": client_id,
            "contactId": contact_id
        }
        
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
        logger.error(f"Get prism client contact failed: {e}")
        return {"error": f"Get prism client contact failed: {e}"}

# Batch 17: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_retirement_plan_list(
    client_id: str, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Retirement Plan List
    
    Args:
        client_id: Client identifier; if the web service user has no client restrictions, enter "ALL" to return this information for all clients
        count: Number of records per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing a list of all retirement benefit plans set up under the Benefits tab
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getRetirementPlanList"
        params = {"clientId": client_id}
        
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get retirement plan list failed: {e}")
        return {"error": f"Get retirement plan list failed: {e}"}

@mcp.tool()
def get_suta_billing_rates(
    client_id: str, 
    state_code: str, 
    effective_date: str, 
    location_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get SUTA billing rates
    
    Args:
        client_id: Client identifier
        state_code: State identifier
        effective_date: Date when the SUTA billing rate goes into effect, in YYYY-MM-DD format
        location_code: Identifier for a location within the state (optional)
        
    Returns:
        Dictionary containing client SUTA billing rate information for a given state, effective date, and optional location
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getSutaBillingRates"
        params = {
            "clientId": client_id,
            "stateCode": state_code,
            "effectiveDate": effective_date
        }
        
        if location_code:
            params["locationCode"] = location_code
        
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
        logger.error(f"Get SUTA billing rates failed: {e}")
        return {"error": f"Get SUTA billing rates failed: {e}"}

@mcp.tool()
def get_suta_rates(
    state: str, 
    client_id: Optional[str] = None, 
    employer_id: Optional[str] = None, 
    effective_date: Optional[str] = None, 
    from_date: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get SUTA rates
    
    Args:
        state: Enter a state code to return SUTA rate information for that state, or enter "ALLSTATES"
        client_id: Client identifier; required if employer_id is empty; enter a client ID or enter "ALLCLIENTS" to return SUTA rates for all clients (optional)
        employer_id: Employer identifier; web service user's client access must include clients of this employer; enter an employer ID or enter "ALLEMPLOYERS" to return SUTA rates for all employers (optional)
        effective_date: Enter a date (format: YYYY-MM-DD) to return only SUTA rates with that effective date (optional)
        from_date: Required if effective_date is empty; enter a date (format: YYYY-MM-DD) to return SUTA rates that are effective on or after that date (optional)
        count: Number of SUTA rates returned per page (optional)
        startpage: Pagination startpage location (first page = '0') (optional)
        
    Returns:
        Dictionary containing information about client-level and employer-level state unemployment tax rates
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getSutaRates"
        params = {"state": state}
        
        if client_id:
            params["clientId"] = client_id
        if employer_id:
            params["employerId"] = employer_id
        if effective_date:
            params["effectiveDate"] = effective_date
        if from_date:
            params["fromDate"] = from_date
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get SUTA rates failed: {e}")
        return {"error": f"Get SUTA rates failed: {e}"}

@mcp.tool()
def get_unbundled_billing_rules(
    client_id: str, 
    rule_id: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get unbundled billing rules
    
    Args:
        client_id: Client identifier
        rule_id: Identifier for a specific billing rule to return (optional)
        count: Number of billing rules returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing a list of unbundled billing rules for the specified client, or information about a specific billing rule
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getUnbundledBillingRules"
        params = {"clientId": client_id}
        
        if rule_id:
            params["ruleId"] = rule_id
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get unbundled billing rules failed: {e}")
        return {"error": f"Get unbundled billing rules failed: {e}"}

@mcp.tool()
def get_wc_accrual_modifiers(
    client_id: str, 
    state_code: Optional[str] = None, 
    effective_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get client W/C accrual modifiers
    
    Args:
        client_id: Client identifier
        state_code: Enter a two-character state code to only include W/C modifiers for that state (optional)
        effective_date: Enter a date to only return W/C modifiers effective on or after that date (optional)
        
    Returns:
        Dictionary containing all client-level Workers' Compensation accrual modifiers associated with a specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getWCAccrualModifiers"
        params = {"clientId": client_id}
        
        if state_code:
            params["stateCode"] = state_code
        if effective_date:
            params["effectiveDate"] = effective_date
        
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
        logger.error(f"Get WC accrual modifiers failed: {e}")
        return {"error": f"Get WC accrual modifiers failed: {e}"}

# Batch 18: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_wc_billing_modifiers(
    client_id: str, 
    state_code: str, 
    location_code: Optional[str] = None, 
    existing_effective_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get client W/C billing modifiers
    
    Args:
        client_id: Client identifier
        state_code: Two-character Workers' Compensation state code
        location_code: Worksite location associated with the modifier (optional)
        existing_effective_date: Date on which the modifier takes effect (optional)
        
    Returns:
        Dictionary containing information about client-level Workers' Compensation billing modifiers
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v1/getWCBillingModifiers"
        params = {
            "clientId": client_id,
            "stateCode": state_code
        }
        
        if location_code:
            params["locationCode"] = location_code
        if existing_effective_date:
            params["existingEffectiveDate"] = existing_effective_date
        
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
        logger.error(f"Get WC billing modifiers failed: {e}")
        return {"error": f"Get WC billing modifiers failed: {e}"}

@mcp.tool()
def get_client_location_details_v2(
    client_id: str, 
    location_id: str
) -> Dict[str, Any]:
    """
    Get client location detail V2 version
    
    Args:
        client_id: Client identifier
        location_id: ID of the client's worksite location to retrieve
        
    Returns:
        Dictionary containing details for a specific client worksite location (V2 version with PII masking)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v2/getClientLocationDetails"
        params = {
            "clientId": client_id,
            "locationId": location_id
        }
        
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
        logger.error(f"Get client location details V2 failed: {e}")
        return {"error": f"Get client location details V2 failed: {e}"}

@mcp.tool()
def get_suta_billing_rates_v2(
    client_id: str, 
    state_code: str, 
    location_code: Optional[str] = None, 
    effective_date: Optional[str] = None, 
    from_date: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get SUTA billing rates (v2)
    
    Args:
        client_id: Client identifier
        state_code: Two-character state identifier; enter "ALLSTATES" to return billing rates for all states
        location_code: Optional identifier for a specific location within the state; enter "ALL" to return billing rates for all locations (optional)
        effective_date: Specify a date when the SUTA billing rate goes into effect (format: YYYY-MM-DD) to return only billing rates for that date; to use this field, from_date must be empty (optional)
        from_date: Specify a date in YYYY-MM-DD format to return all billing rates from that date onward; to use this field, effective_date must be empty (optional)
        count: Number of billing rates returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing client state unemployment tax (SUTA) billing rate information (V2 version with pagination)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/clientMaster/v2/getSutaBillingRates"
        params = {
            "clientId": client_id,
            "stateCode": state_code
        }
        
        if location_code:
            params["locationCode"] = location_code
        if effective_date:
            params["effectiveDate"] = effective_date
        if from_date:
            params["fromDate"] = from_date
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get SUTA billing rates V2 failed: {e}")
        return {"error": f"Get SUTA billing rates V2 failed: {e}"}

@mcp.tool()
def get_billing_code(
    billing_code: Optional[str] = None, 
    only_active: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Billing codes
    
    Args:
        billing_code: Enter a billing code to only retrieve information about that code (optional)
        only_active: If true, the response only includes non-obsolete billing codes (optional)
        count: Number of billing codes returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing a list of client billing codes and their setup information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getBillingCode"
        params = {}
        
        if billing_code:
            params["billingCode"] = billing_code
        if only_active:
            params["onlyActive"] = only_active
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get billing code failed: {e}")
        return {"error": f"Get billing code failed: {e}"}

@mcp.tool()
def get_client_category_list(
    client_category_id: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get client category list
    
    Args:
        client_category_id: Enter a client category ID to only retrieve information about that client category ID (optional)
        count: Number of client category records to return per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing the list of client categories
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getClientCategoryList"
        params = {}
        
        if client_category_id:
            params["clientCategoryId"] = client_category_id
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get client category list failed: {e}")
        return {"error": f"Get client category list failed: {e}"}

# Batch 19: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_contact_type_list() -> Dict[str, Any]:
    """
    Get Contact Type List
    
    Args:
        None
        
    Returns:
        Dictionary containing a list of contact types
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getContactTypeList"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get contact type list failed: {e}")
        return {"error": f"Get contact type list failed: {e}"}

@mcp.tool()
def get_course_codes_list(
    client_id: str, 
    course_code_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get all courses associated with a particular client
    
    Args:
        client_id: Client identifier
        course_code_id: Single course code to return (optional)
        
    Returns:
        Dictionary containing all courses associated with a client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getCourseCodesList"
        params = {"clientId": client_id}
        
        if course_code_id:
            params["courseCodeId"] = course_code_id
        
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
        logger.error(f"Get course codes list failed: {e}")
        return {"error": f"Get course codes list failed: {e}"}

@mcp.tool()
def get_deduction_code_details(
    deduction_code: str
) -> Dict[str, Any]:
    """
    Get Deduction code details
    
    Args:
        deduction_code: Deduction code ID
        
    Returns:
        Dictionary containing the configuration details for a specified deduction code
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getDeductionCodeDetails"
        params = {"deductionCode": deduction_code}
        
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
        logger.error(f"Get deduction code details failed: {e}")
        return {"error": f"Get deduction code details failed: {e}"}

@mcp.tool()
def get_department_code(
    client_id: str, 
    department_code: str
) -> Dict[str, Any]:
    """
    Get specified department code file for a particular client
    
    Args:
        client_id: Client identifier
        department_code: Department code
        
    Returns:
        Dictionary containing information about a department code for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getDepartmentCode"
        params = {
            "clientId": client_id,
            "departmentCode": department_code
        }
        
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
        logger.error(f"Get department code failed: {e}")
        return {"error": f"Get department code failed: {e}"}

@mcp.tool()
def get_division_code(
    client_id: str, 
    division_code: str
) -> Dict[str, Any]:
    """
    Get specified division code file for a particular client
    
    Args:
        client_id: Client identifier
        division_code: Division code
        
    Returns:
        Dictionary containing information about a division code for the specified client (with PII masking)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getDivisionCode"
        params = {
            "clientId": client_id,
            "divisionCode": division_code
        }
        
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
        logger.error(f"Get division code failed: {e}")
        return {"error": f"Get division code failed: {e}"}

# Batch 20: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_eeo_codes(
    eeo_code_type: str, 
    eeo_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get EEO setup codes
    
    Args:
        eeo_code_type: Type of EEO-1 setup code to return; allowed values are 'Class', 'Group', and 'Ethnic'
        eeo_code: Enter a setup code to only return information about that code, or leave blank to return all codes for the specified type (optional)
        
    Returns:
        Dictionary containing information about codes used during setup of EEO-1 reporting in PrismHR
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getEeoCodes"
        params = {"eeoCodeType": eeo_code_type}
        
        if eeo_code:
            params["eeoCode"] = eeo_code
        
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
        logger.error(f"Get EEO codes failed: {e}")
        return {"error": f"Get EEO codes failed: {e}"}

@mcp.tool()
def get_event_codes(
    client_id: str
) -> Dict[str, Any]:
    """
    Returns event codes file for the specified client
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing a list of event codes and their descriptions
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getEventCodes"
        params = {"clientId": client_id}
        
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
        logger.error(f"Get event codes failed: {e}")
        return {"error": f"Get event codes failed: {e}"}

@mcp.tool()
def get_holiday_code_list(
    year: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get global holiday code list for this PEO
    
    Args:
        year: Year filter (format: YYYY) (optional)
        
    Returns:
        Dictionary containing the system level list of Holidays with dates and description for this PEO
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getHolidayCodeList"
        params = {}
        
        if year:
            params["year"] = year
        
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
        logger.error(f"Get holiday code list failed: {e}")
        return {"error": f"Get holiday code list failed: {e}"}

@mcp.tool()
def get_naics_code_list(
    naics_code: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get NAICS Code List
    
    Args:
        naics_code: A six-digit NAICS identifier that identifies the industry, for example, 311221. To retrieve the details of a particular NAICS code, enter it here. Leave it blank to retrieve the details of all NAICS codes in PrismHR (optional)
        count: Number of NAICS code records returned per page (default: 5000) (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing the details of one or all North American Industry Classification System (NAICS) codes
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getNAICSCodeList"
        params = {}
        
        if naics_code:
            params["naicsCode"] = naics_code
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get NAICS code list failed: {e}")
        return {"error": f"Get NAICS code list failed: {e}"}

@mcp.tool()
def get_pay_grades(
    client_id: str, 
    pay_grade_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Client Pay Grades
    
    Args:
        client_id: Client identifier
        pay_grade_code: Enter a pay grade code to only return information about that code, or leave blank to return all codes (optional)
        
    Returns:
        Dictionary containing information about one or more pay grade codes for a specific client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getPayGrades"
        params = {"clientId": client_id}
        
        if pay_grade_code:
            params["payGradeCode"] = pay_grade_code
        
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
        logger.error(f"Get pay grades failed: {e}")
        return {"error": f"Get pay grades failed: {e}"}

# Batch 21: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_paycode_details(
    paycode_id: str
) -> Dict[str, Any]:
    """
    Get Pay Code details
    
    Args:
        paycode_id: Pay code identifier
        
    Returns:
        Dictionary containing pay code setup details
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getPaycodeDetails"
        params = {"paycodeId": paycode_id}
        
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
        logger.error(f"Get paycode details failed: {e}")
        return {"error": f"Get paycode details failed: {e}"}

@mcp.tool()
def get_position_classifications(
    position_class: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns position classifications
    
    Args:
        position_class: Position class (optional)
        
    Returns:
        Dictionary containing information about position classification codes for a client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getPositionClassifications"
        params = {}
        
        if position_class:
            params["positionClass"] = position_class
        
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
        logger.error(f"Get position classifications failed: {e}")
        return {"error": f"Get position classifications failed: {e}"}

@mcp.tool()
def get_position_code(
    client_id: str, 
    position_code: str
) -> Dict[str, Any]:
    """
    Returns position code for the specified client
    
    Args:
        client_id: Client identifier
        position_code: Position code
        
    Returns:
        Dictionary containing information about position codes
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getPositionCode"
        params = {
            "clientId": client_id,
            "positionCode": position_code
        }
        
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
        logger.error(f"Get position code failed: {e}")
        return {"error": f"Get position code failed: {e}"}

@mcp.tool()
def get_project_code(
    client_id: str, 
    project_code: str
) -> Dict[str, Any]:
    """
    Returns project code for the specified client
    
    Args:
        client_id: Client identifier
        project_code: Project code
        
    Returns:
        Dictionary containing details about a single project code including certified payroll details information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getProjectCode"
        params = {
            "clientId": client_id,
            "projectCode": project_code
        }
        
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
        logger.error(f"Get project code failed: {e}")
        return {"error": f"Get project code failed: {e}"}

@mcp.tool()
def get_project_phase(
    client_id: str, 
    class_code: Optional[str] = None, 
    project_phase_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns project phases for the specified client
    
    Args:
        client_id: Client identifier
        class_code: Project class code (optional)
        project_phase_code: Project phase code (optional)
        
    Returns:
        Dictionary containing information about project phases
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getProjectPhase"
        params = {"clientId": client_id}
        
        if class_code:
            params["classCode"] = class_code
        if project_phase_code:
            params["projectPhaseCode"] = project_phase_code
        
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
        logger.error(f"Get project phase failed: {e}")
        return {"error": f"Get project phase failed: {e}"}

# Batch 22: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_rating_code(
    client_id: str, 
    rating_code_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get rating codes for specific client
    
    Args:
        client_id: Client whose rating codes you want to retrieve
        rating_code_id: Enter a valid rating code ID to return information about only that rating code (optional)
        
    Returns:
        Dictionary containing a list of rating codes for employee performance reviews
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getRatingCode"
        params = {"clientId": client_id}
        
        if rating_code_id:
            params["ratingCodeId"] = rating_code_id
        
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
        logger.error(f"Get rating code failed: {e}")
        return {"error": f"Get rating code failed: {e}"}

@mcp.tool()
def get_shift_code(
    client_id: str, 
    shift_code: str
) -> Dict[str, Any]:
    """
    Get specified shift code file for a particular client
    
    Args:
        client_id: Client identifier
        shift_code: Shift code
        
    Returns:
        Dictionary containing information about a shift code for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getShiftCode"
        params = {
            "clientId": client_id,
            "shiftCode": shift_code
        }
        
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
        logger.error(f"Get shift code failed: {e}")
        return {"error": f"Get shift code failed: {e}"}

@mcp.tool()
def get_skill_code(
    client_id: str, 
    skill_code: str
) -> Dict[str, Any]:
    """
    Returns skill code for the specified client
    
    Args:
        client_id: Client identifier
        skill_code: Skill code
        
    Returns:
        Dictionary containing the details of a single skill code
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getSkillCode"
        params = {
            "clientId": client_id,
            "skillCode": skill_code
        }
        
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
        logger.error(f"Get skill code failed: {e}")
        return {"error": f"Get skill code failed: {e}"}

@mcp.tool()
def get_user_defined_fields(
    client_id: str, 
    field_type: str, 
    type_id: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get user-defined fields for the specified field type
    
    Args:
        client_id: Client identifier
        field_type: Type of user-defined fields you want to return (e.g., GroupBenefitPlans, ClientDetails, DeliveryMethods, EmployeeDependents, Departments, Divisions, RetirementPlanEnrollment, EmployeeBenefitsEnrollment, EmployeeDetails, Positions, WorksiteLocations, OshaCases, Projects, PayGrades, Shifts, LaborUnions, WorkersCompensationCases)
        type_id: List of type identifiers associated with the fieldType (max 20 values, except ClientDetails which only allows one) (optional)
        
    Returns:
        Dictionary containing user-defined fields from any part of the system where they exist
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/codeFiles/v1/getUserDefinedFields"
        params = {
            "clientId": client_id,
            "fieldType": field_type
        }
        
        if type_id:
            for tid in type_id:
                params["typeId"] = tid
        
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
        logger.error(f"Get user defined fields failed: {e}")
        return {"error": f"Get user defined fields failed: {e}"}

@mcp.tool()
def get_deduction_arrears(
    client_id: str, 
    employee_id: str, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get payroll deductions arrear information
    
    Args:
        client_id: Client identifier
        employee_id: The employee ID used to retrieve the deductions
        options: Reserved for future use; send empty String (optional)
        
    Returns:
        Dictionary containing information about payroll deductions in arrears for a particular employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/deductions/v1/getDeductionArrears"
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
        logger.error(f"Get deduction arrears failed: {e}")
        return {"error": f"Get deduction arrears failed: {e}"}

# Batch 23: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_deductions(
    client_id: str, 
    employee_id: str, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get payroll deductions information
    
    Args:
        client_id: Client identifier
        employee_id: The employee ID used to retrieve the deductions
        options: Reserved for future use; send empty String (optional)
        
    Returns:
        Dictionary containing payroll deduction rules for employee (voluntary, non-voluntary, and benefit plan deductions)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/deductions/v1/getDeductions"
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
        logger.error(f"Get deductions failed: {e}")
        return {"error": f"Get deductions failed: {e}"}

@mcp.tool()
def get_employee_loans(
    client_id: str, 
    employee_id: str, 
    loan_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get employee loans information
    
    Args:
        client_id: Client identifier
        employee_id: The employee ID used to retrieve the loans
        loan_id: The loan ID. Optional parameter that allows to extract loan by Id (optional)
        
    Returns:
        Dictionary containing all loan information for a specific employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/deductions/v1/getEmployeeLoans"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if loan_id:
            params["loanId"] = loan_id
        
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
        logger.error(f"Get employee loans failed: {e}")
        return {"error": f"Get employee loans failed: {e}"}

@mcp.tool()
def get_garnishment_details(
    client_id: str, 
    employee_id: str, 
    docket_number: Optional[str] = None, 
    garnishment_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Garnishment Details for the employee
    
    Args:
        client_id: Client Identifier
        employee_id: Employee Identifier
        docket_number: Garnishment Docket Number (optional)
        garnishment_type: Garnishment Type (C- Child Support, SP- Spousal Support, I- IRS Tax Levy, B- Bankruptcy Order, S- State Tax Levy, FTB- Franchise Tax Board, O- Creditor Wage Garnishment, SL- Student Loan) (optional)
        
    Returns:
        Dictionary containing garnishment details for a particular employee and client (with PII masking)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/deductions/v1/getGarnishmentDetails"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if docket_number:
            params["docketNumber"] = docket_number
        if garnishment_type:
            params["garnishmentType"] = garnishment_type
        
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
        logger.error(f"Get garnishment details failed: {e}")
        return {"error": f"Get garnishment details failed: {e}"}

@mcp.tool()
def get_garnishment_payment_history(
    client_id: str, 
    employee_id: str, 
    docket_number: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get garnishment payment history
    
    Args:
        client_id: Client identifier
        employee_id: The employee ID used to retrieve the loans
        docket_number: Docket number assigned to this garnishment (optional)
        
    Returns:
        Dictionary containing an employee's garnishment payment history
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/deductions/v1/getGarnishmentPaymentHistory"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if docket_number:
            params["docketNumber"] = docket_number
        
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
        logger.error(f"Get garnishment payment history failed: {e}")
        return {"error": f"Get garnishment payment history failed: {e}"}

@mcp.tool()
def get_voluntary_recurring_deductions(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get voluntary recurring deductions list
    
    Args:
        client_id: Client identifier
        employee_id: The employee ID used to retrieve the voluntary deductions
        
    Returns:
        Dictionary containing all voluntary recurring deductions for an employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/deductions/v1/getVoluntaryRecurringDeductions"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get voluntary recurring deductions failed: {e}")
        return {"error": f"Get voluntary recurring deductions failed: {e}"}

# Batch 24: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_document_types(
    document_type_id: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get document types
    
    Args:
        document_type_id: Document type ID(s) (optional)
        
    Returns:
        Dictionary containing information about document types related to PrismHR Document Management
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/documentService/v1/getDocumentTypes"
        params = {}
        
        if document_type_id:
            for dtid in document_type_id:
                params["documentTypeId"] = dtid
        
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
        logger.error(f"Get document types failed: {e}")
        return {"error": f"Get document types failed: {e}"}

@mcp.tool()
def get_ruleset(
    user_id: str, 
    client_id: str, 
    user_type: str, 
    context: str
) -> Dict[str, Any]:
    """
    Get document management ruleset
    
    Args:
        user_id: Username
        client_id: Client identifier
        user_type: User type: 'I' (Internal User (service provider)), 'C' (Worksite Manager), 'A' (Worksite Trusted Advisor), or 'E' (Employee)
        context: Name of the ruleset
        
    Returns:
        Dictionary containing document management ruleset (for internal use only)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/documentService/v1/getRuleset"
        params = {
            "userId": user_id,
            "clientId": client_id,
            "userType": user_type,
            "context": context
        }
        
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
        logger.error(f"Get ruleset failed: {e}")
        return {"error": f"Get ruleset failed: {e}"}

@mcp.tool()
def check_for_garnishments(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Check for garnishments for employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing whether an employee has active garnishments (does not return garnishment details)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/checkForGarnishments"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Check for garnishments failed: {e}")
        return {"error": f"Check for garnishments failed: {e}"}

@mcp.tool()
def download_1095c(
    client_id: str, 
    employee_id: List[str], 
    year: str
) -> Dict[str, Any]:
    """
    Download an employee's 1095C
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier(s); provide only one employee ID to download 1095C for a single employee, provide two employee IDs to download 1095Cs for all employees of the provided client within the given range
        year: 1095C year
        
    Returns:
        Dictionary containing 1095C form data (limit of 200 1095Cs per batch)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/download1095C"
        params = {
            "clientId": client_id,
            "year": year
        }
        
        for eid in employee_id:
            params["employeeId"] = eid
        
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
        logger.error(f"Download 1095C failed: {e}")
        return {"error": f"Download 1095C failed: {e}"}

@mcp.tool()
def download_w2(
    client_id: str, 
    employee_id: List[str], 
    year: str
) -> Dict[str, Any]:
    """
    Download an employee's W2
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier(s); provide only one employee ID to download W2 for a single employee, provide two employee IDs to download W2s for all employees of the provided client within the given range
        year: W2 year
        
    Returns:
        Dictionary containing W2 form data (limit of 200 W2s per batch)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/downloadW2"
        params = {
            "clientId": client_id,
            "year": year
        }
        
        for eid in employee_id:
            params["employeeId"] = eid
        
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
        logger.error(f"Download W2 failed: {e}")
        return {"error": f"Download W2 failed: {e}"}

# Batch 25: Next 4 endpoints from all_get_endpoints.txt (skipping getEmployee as it already exists)

@mcp.tool()
def get_1095c_years(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get a list of available Form 1095-C years
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing list of Form 1095-C years for the specified employee (only years where Show In ESS is set to Yes)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/get1095CYears"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get 1095C years failed: {e}")
        return {"error": f"Get 1095C years failed: {e}"}

@mcp.tool()
def get_1099_years(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get a list of available 1099 years
    
    Args:
        client_id: Client identifier
        employee_id: ID of the Form 1099 contractor
        
    Returns:
        Dictionary containing list of existing Form 1099 years for the specific independent contractor (only years employer allows to display online)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/get1099Years"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get 1099 years failed: {e}")
        return {"error": f"Get 1099 years failed: {e}"}

@mcp.tool()
def get_ach_deductions(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get Employee ACH Deductions
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing voluntary employee ACH deduction setup (where accountType = "DED1", "DED2", or "DED3")
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getACHDeductions"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get ACH deductions failed: {e}")
        return {"error": f"Get ACH deductions failed: {e}"}

@mcp.tool()
def get_address_info(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get employee address information
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing addresses for the particular employee including residential address, address for Forms W-2, and mailing (alternate) address
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getAddressInfo"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get address info failed: {e}")
        return {"error": f"Get address info failed: {e}"}

# Batch 26: Next 4 endpoints from all_get_endpoints.txt (skipping getEmployeeList as it already exists)

@mcp.tool()
def get_employee_events(
    employee_id: str, 
    client_id: str
) -> Dict[str, Any]:
    """
    Get events for an employee
    
    Args:
        employee_id: Employee ID
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of employee events for a single employee (includes checksum for updates)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getEmployeeEvents"
        params = {
            "employeeId": employee_id,
            "clientId": client_id
        }
        
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
        logger.error(f"Get employee events failed: {e}")
        return {"error": f"Get employee events failed: {e}"}

@mcp.tool()
def get_employee_ssn_list(
    client_id: str
) -> Dict[str, Any]:
    """
    Get list of employees with their SSN
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of employees including their employee IDs and Social Security numbers
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getEmployeeSSNList"
        params = {
            "clientId": client_id
        }
        
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
        logger.error(f"Get employee SSN list failed: {e}")
        return {"error": f"Get employee SSN list failed: {e}"}

@mcp.tool()
def get_employees_ready_for_everify() -> Dict[str, Any]:
    """
    Get employees who have E-Verify Requested status
    
    Returns:
        Dictionary containing list of employees from clients that have the status E-Verify Requested
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getEmployeesReadyForEverify"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get employees ready for everify failed: {e}")
        return {"error": f"Get employees ready for everify failed: {e}"}

@mcp.tool()
def get_employers_info(
    employee_id: str, 
    client_id: str
) -> Dict[str, Any]:
    """
    Get current employer and list of possible employers
    
    Args:
        employee_id: Employee ID
        client_id: Client identifier
        
    Returns:
        Dictionary containing employee's current employer and all potential employers associated with the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getEmployersInfo"
        params = {
            "employeeId": employee_id,
            "clientId": client_id
        }
        
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
        logger.error(f"Get employers info failed: {e}")
        return {"error": f"Get employers info failed: {e}"}

# Batch 27: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_everify_status(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get employee's E-Verify data
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing employee's E-Verify data including status and case number
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getEverifyStatus"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get everify status failed: {e}")
        return {"error": f"Get everify status failed: {e}"}

@mcp.tool()
def get_future_ee_change(
    event_object_id: str
) -> Dict[str, Any]:
    """
    Get employee future event change
    
    Args:
        event_object_id: Event object identifier (returned by SubscriptionService.getEvents or getNewEvents for subscription Schema Employee and Class FutureEEChanges)
        
    Returns:
        Dictionary containing future-scheduled changes to an employee job/position, pay rate, or status
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getFutureEeChange"
        params = {
            "eventObjectId": event_object_id
        }
        
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
        logger.error(f"Get future ee change failed: {e}")
        return {"error": f"Get future ee change failed: {e}"}

@mcp.tool()
def get_garnishment_employee(
    client_id: str, 
    garnishment_id: str
) -> Dict[str, Any]:
    """
    Get employee Id for garnishment
    
    Args:
        client_id: Client identifier
        garnishment_id: Garnishment identifier (docket number)
        
    Returns:
        Dictionary containing employee ID associated with the specific client ID and garnishment ID/docket number
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getGarnishmentEmployee"
        params = {
            "clientId": client_id,
            "garnishmentId": garnishment_id
        }
        
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
        logger.error(f"Get garnishment employee failed: {e}")
        return {"error": f"Get garnishment employee failed: {e}"}

@mcp.tool()
def get_history(
    client_id: str, 
    employee_id: str, 
    type: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get historical events
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        type: History types (specify B for benefit groups, C for locations, D for departments, J for jobs/positions, P for pay, S for status, V for divisions, W for wellness status, or leave blank to retrieve all history types)
        
    Returns:
        Dictionary containing array of historical events for an employee including pay rate changes, job/position changes, leave of absence, status changes, and employment termination
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getHistory"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if type:
            for t in type:
                params["type"] = t
        
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
        logger.error(f"Get history failed: {e}")
        return {"error": f"Get history failed: {e}"}

@mcp.tool()
def get_i9_data(
    client_id: str, 
    employee_id: str, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get employee I9 data
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        options: A string containing zero or more of the keywords in the options table (e.g., AdditionalMetadata)
        
    Returns:
        Dictionary containing Form I-9 data for the particular employee including all data pertinent to the USCIS Form I-9
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getI9Data"
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
        logger.error(f"Get I9 data failed: {e}")
        return {"error": f"Get I9 data failed: {e}"}

# Batch 28: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_leave_requests(
    client_id: str, 
    leave_id: str
) -> Dict[str, Any]:
    """
    Get leave requests by clientId and leaveId
    
    Args:
        client_id: Client identifier
        leave_id: PTO (leave request) identifier
        
    Returns:
        Dictionary containing employee PTO request information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getLeaveRequests"
        params = {
            "clientId": client_id,
            "leaveId": leave_id
        }
        
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
        logger.error(f"Get leave requests failed: {e}")
        return {"error": f"Get leave requests failed: {e}"}

@mcp.tool()
def get_life_event(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Retrieve an employee life event
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing a single employee life event for the provided client and employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getLifeEvent"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get life event failed: {e}")
        return {"error": f"Get life event failed: {e}"}

@mcp.tool()
def get_osha(
    client_id: str, 
    case_number: str
) -> Dict[str, Any]:
    """
    Get OSHA case
    
    Args:
        client_id: Client identifier
        case_number: OSHA case file number
        
    Returns:
        Dictionary containing OSHA case file from PrismHR
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getOSHA"
        params = {
            "clientId": client_id,
            "caseNumber": case_number
        }
        
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
        logger.error(f"Get OSHA failed: {e}")
        return {"error": f"Get OSHA failed: {e}"}

@mcp.tool()
def get_pay_card_employees(
    client_id: str, 
    transit_number: str
) -> Dict[str, Any]:
    """
    Get list of employees associated with a specified direct deposit transit/routing number
    
    Args:
        client_id: Client identifier
        transit_number: Direct deposit routing number
        
    Returns:
        Dictionary containing list of employees associated with the specified direct deposit transit/routing number
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getPayCardEmployees"
        params = {
            "clientId": client_id,
            "transitNumber": transit_number
        }
        
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
        logger.error(f"Get pay card employees failed: {e}")
        return {"error": f"Get pay card employees failed: {e}"}

@mcp.tool()
def get_pay_rate_history(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get historical pay rate attributes
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing array (list) of historical pay rate attributes
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getPayRateHistory"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get pay rate history failed: {e}")
        return {"error": f"Get pay rate history failed: {e}"}

# Batch 29: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_pending_approval(
    client_id: str, 
    type: Optional[str] = None, 
    employee_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of pending approvals by employeeID
    
    Args:
        client_id: Client identifier
        type: Pending approval type (specify 'T' for terminated, 'A' for Active, or leave blank to retrieve both status change types)
        employee_id: Employee identifier (optional)
        
    Returns:
        Dictionary containing array (list) of employeeIDs with pending approvals for status/type changes or terminations
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getPendingApproval"
        params = {
            "clientId": client_id
        }
        
        if type:
            params["type"] = type
        if employee_id:
            params["employeeId"] = employee_id
        
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
        logger.error(f"Get pending approval failed: {e}")
        return {"error": f"Get pending approval failed: {e}"}

@mcp.tool()
def get_position_rate(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get list of position rates
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing array (list) of position rate objects that contain standard rate, pay code, and billing rate attributes
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getPositionRate"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get position rate failed: {e}")
        return {"error": f"Get position rate failed: {e}"}

@mcp.tool()
def get_scheduled_deductions(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get an employee's scheduled deductions
    
    Args:
        client_id: Client ID
        employee_id: Employee ID
        
    Returns:
        Dictionary containing list of an employee's scheduled deductions (one-time or temporary deductions, not including standard deductions or garnishments)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getScheduledDeductions"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get scheduled deductions failed: {e}")
        return {"error": f"Get scheduled deductions failed: {e}"}

@mcp.tool()
def get_status_history_for_adjustment(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Retrieve status history for employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing all information necessary to make a status/type history date adjustment for an employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getStatusHistoryForAdjustment"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get status history for adjustment failed: {e}")
        return {"error": f"Get status history for adjustment failed: {e}"}

@mcp.tool()
def get_termination_date_range(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get termination date range for employees
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing valid date range for employee terminations
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getTerminationDateRange"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get termination date range failed: {e}")
        return {"error": f"Get termination date range failed: {e}"}

# Batch 30: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_w2_years(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get a list of available W2 years
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing list of Form W-2 years available for a specified employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/getW2Years"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get W2 years failed: {e}")
        return {"error": f"Get W2 years failed: {e}"}

@mcp.tool()
def reprint_1099(
    client_id: str, 
    employee_id: List[str], 
    year: str
) -> Dict[str, Any]:
    """
    Download an employee's 1099
    
    Args:
        client_id: Client identifier
        employee_id: ID of the independent contractor (array)
        year: Form 1099 year, returned by get1099Years
        
    Returns:
        Dictionary containing independent contractor's Form 1099 for the specified year
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/reprint1099"
        params = {
            "clientId": client_id,
            "year": year
        }
        
        # Handle array parameter for employee_id
        for i, emp_id in enumerate(employee_id):
            params[f"employeeId[{i}]"] = emp_id
        
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
        logger.error(f"Reprint 1099 failed: {e}")
        return {"error": f"Reprint 1099 failed: {e}"}

@mcp.tool()
def reprint_w2c(
    client_id: str, 
    employee_id: str, 
    year: str
) -> Dict[str, Any]:
    """
    Download an employee's W2C
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        year: W2C year
        
    Returns:
        Dictionary containing employee's W2C form for the provided year
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/employee/v1/reprintW2C"
        params = {
            "clientId": client_id,
            "employeeId": employee_id,
            "year": year
        }
        
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
        logger.error(f"Reprint W2C failed: {e}")
        return {"error": f"Reprint W2C failed: {e}"}

@mcp.tool()
def get_bulk_outstanding_invoices(
    client_id: Optional[str] = None, 
    download_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve list of client invoices
    
    Args:
        client_id: List of client identifiers (optional, required if user has client restrictions)
        download_id: Identifier used to check status of / download data (optional)
        
    Returns:
        Dictionary containing list of outstanding invoices across multiple clients
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getBulkOutstandingInvoices"
        params = {}
        
        if client_id:
            params["clientId"] = client_id
        if download_id:
            params["downloadId"] = download_id
        
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
        logger.error(f"Get bulk outstanding invoices failed: {e}")
        return {"error": f"Get bulk outstanding invoices failed: {e}"}

@mcp.tool()
def get_client_accounting_template(
    client_id: str
) -> Dict[str, Any]:
    """
    Retrieve client and global PEO accounting templates
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing details about the accounting template assigned to a particular client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getClientAccountingTemplate"
        params = {
            "clientId": client_id
        }
        
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
        logger.error(f"Get client accounting template failed: {e}")
        return {"error": f"Get client accounting template failed: {e}"}

# Batch 31: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_client_gl_data(
    client_id: str, 
    download_id: Optional[str] = None, 
    pay_date_start: Optional[str] = None, 
    pay_date_end: Optional[str] = None, 
    post_date_start: Optional[str] = None, 
    post_date_end: Optional[str] = None, 
    batch_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get PEO client accounting data
    
    Args:
        client_id: Client identifier
        download_id: Identifier used to check status of / download data (optional)
        pay_date_start: Pay date range starting date (optional; formatted YYYY-MM-DD)
        pay_date_end: Pay date range ending date (optional; formatted YYYY-MM-DD)
        post_date_start: Post date range starting date (optional; formatted YYYY-MM-DD)
        post_date_end: Post date range ending date (optional; formatted YYYY-MM-DD)
        batch_id: Payroll batch ID to return journal IDs for that specific batch (optional)
        
    Returns:
        Dictionary containing PEO client accounting data from PrismHR for use by external programs
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getClientGLData"
        params = {
            "clientId": client_id
        }
        
        if download_id:
            params["downloadId"] = download_id
        if pay_date_start:
            params["payDateStart"] = pay_date_start
        if pay_date_end:
            params["payDateEnd"] = pay_date_end
        if post_date_start:
            params["postDateStart"] = post_date_start
        if post_date_end:
            params["postDateEnd"] = post_date_end
        if batch_id:
            params["batchId"] = batch_id
        
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
        logger.error(f"Get client GL data failed: {e}")
        return {"error": f"Get client GL data failed: {e}"}

@mcp.tool()
def get_gl_codes(
    gl_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of General Ledger account codes and their descriptions
    
    Args:
        gl_code: Optional GL code parameter to get the information just for that code
        
    Returns:
        Dictionary containing General Ledger account codes and their descriptions
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getGLCodes"
        params = {}
        
        if gl_code:
            params["glCode"] = gl_code
        
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
        logger.error(f"Get GL codes failed: {e}")
        return {"error": f"Get GL codes failed: {e}"}

@mcp.tool()
def get_gl_detail_download(
    download_id: Optional[str] = None, 
    batch_id: Optional[str] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    client_id: Optional[List[str]] = None, 
    employer_id: Optional[List[str]] = None, 
    gl_account: Optional[List[str]] = None, 
    gl_cost_center: Optional[List[str]] = None, 
    gl_detail_code_type: Optional[List[str]] = None, 
    gl_detail_code: Optional[List[str]] = None, 
    voucher_id: Optional[List[str]] = None, 
    check_number: Optional[List[str]] = None, 
    employee_id: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Download accounting G/L detail report
    
    Args:
        download_id: Identifier used to check status of / download data (optional)
        batch_id: Payroll batch identifier (either batchId or date range is required)
        start_date: Pay date range starting date (either batchId or date range is required; formatted YYYY-MM-DD)
        end_date: Pay date range ending date (either batchId or date range is required; formatted YYYY-MM-DD)
        client_id: Client identifier(s) (either one or many clientId(s) or employerId(s) or neither; cannot include both)
        employer_id: Employer identifier(s) (either one or many clientId(s) or employerId(s) or neither; cannot include both)
        gl_account: G/L account report filter
        gl_cost_center: G/L cost center report filter
        gl_detail_code_type: G/L detail code type report filter; valid values are (B)enefits, (BI)lling, (C)hecks, (D)eductions, (DD) direct deposit, (FSA) flexible savings accounts, (HSA) health savings accounts, (P)ay, (R)etirement, (T)axes, and (W)orkers comp
        gl_detail_code: G/L detail code report filter
        voucher_id: Voucher ID report filter
        check_number: Check number report filter
        employee_id: Employee ID report filter
        
    Returns:
        Dictionary containing accounting G/L detail report data
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getGLDetailDownload"
        params = {}
        
        if download_id:
            params["downloadId"] = download_id
        if batch_id:
            params["batchId"] = batch_id
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        # Handle array parameters
        if client_id:
            for i, cid in enumerate(client_id):
                params[f"clientId[{i}]"] = cid
        if employer_id:
            for i, eid in enumerate(employer_id):
                params[f"employerId[{i}]"] = eid
        if gl_account:
            for i, account in enumerate(gl_account):
                params[f"glAccount[{i}]"] = account
        if gl_cost_center:
            for i, center in enumerate(gl_cost_center):
                params[f"glCostCenter[{i}]"] = center
        if gl_detail_code_type:
            for i, code_type in enumerate(gl_detail_code_type):
                params[f"glDetailCodeType[{i}]"] = code_type
        if gl_detail_code:
            for i, code in enumerate(gl_detail_code):
                params[f"glDetailCode[{i}]"] = code
        if voucher_id:
            for i, vid in enumerate(voucher_id):
                params[f"voucherId[{i}]"] = vid
        if check_number:
            for i, check in enumerate(check_number):
                params[f"checkNumber[{i}]"] = check
        if employee_id:
            for i, eid in enumerate(employee_id):
                params[f"employeeId[{i}]"] = eid
        
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
        logger.error(f"Get GL detail download failed: {e}")
        return {"error": f"Get GL detail download failed: {e}"}

@mcp.tool()
def get_gl_invoice_detail(
    gl_company: str, 
    inv_date: str, 
    include_posted: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get posted and unposted invoice detail
    
    Args:
        gl_company: Employer identifier associated with the G/L invoices
        inv_date: Invoice date (format: MM/DD/YY)
        include_posted: Whether to include posted invoices in the response (optional)
        
    Returns:
        Dictionary containing detail data about items on the PrismHR External Invoice Post form
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getGLInvoiceDetail"
        params = {
            "glCompany": gl_company,
            "invDate": inv_date
        }
        
        if include_posted:
            params["includePosted"] = include_posted
        
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
        logger.error(f"Get GL invoice detail failed: {e}")
        return {"error": f"Get GL invoice detail failed: {e}"}

@mcp.tool()
def get_gl_setup(
    gl_template: str, 
    gl_type: str, 
    gl_object_id: Optional[str] = None, 
    state: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of general ledger accounts
    
    Args:
        gl_template: ID of the general ledger template you want to access
        gl_type: Type of G/L data to retrieve (B, L, C, D, M, P, R, FSA, HSA, T, W, WP)
        gl_object_id: GL object identifier if you want to retrieve G/L setup information related to a specific gl type (optional)
        state: Two-character state code; only required for Tax G/L type (optional)
        
    Returns:
        Dictionary containing G/L setup information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getGLSetup"
        params = {
            "glTemplate": gl_template,
            "glType": gl_type
        }
        
        if gl_object_id:
            params["glObjectId"] = gl_object_id
        if state:
            params["state"] = state
        
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
        logger.error(f"Get GL setup failed: {e}")
        return {"error": f"Get GL setup failed: {e}"}

# Batch 32: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_outstanding_invoices(
    client_id: str, 
    show_only_deposit_match: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve list of client invoices
    
    Args:
        client_id: Client identifier
        show_only_deposit_match: Enter a deposit value for the system to match; the endpoint returns the invoice with a balance that matches this value, if it exists (optional)
        
    Returns:
        Dictionary containing list of client invoices that are outstanding from an accounting perspective (not overdue and not yet paid)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getOutstandingInvoices"
        params = {
            "clientId": client_id
        }
        
        if show_only_deposit_match:
            params["showOnlyDepositMatch"] = show_only_deposit_match
        
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
        logger.error(f"Get outstanding invoices failed: {e}")
        return {"error": f"Get outstanding invoices failed: {e}"}

@mcp.tool()
def get_pending_cash_receipts(
    cash_receipt_batch_id: str, 
    include_post_type: Optional[str] = None, 
    include_deposit_type: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a paginated list of cash receipts and, optionally, any associated G/L deposit and post information
    
    Args:
        cash_receipt_batch_id: ID of the cash receipts batch to retrieve; enter "ALL" to return all
        include_post_type: Set value to true to include a list of G/L posting options in the response (optional)
        include_deposit_type: Set value to true to include a list of G/L deposit options in the response (optional)
        count: Number of vouchers returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing G/L data about cash receipts that are still pending (not yet paid)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v1/getPendingCashReceipts"
        params = {
            "cashReceiptBatchId": cash_receipt_batch_id
        }
        
        if include_post_type:
            params["includePostType"] = include_post_type
        if include_deposit_type:
            params["includeDepositType"] = include_deposit_type
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get pending cash receipts failed: {e}")
        return {"error": f"Get pending cash receipts failed: {e}"}

@mcp.tool()
def get_client_gl_data_v2(
    client_id: str, 
    pay_date_start: Optional[str] = None, 
    pay_date_end: Optional[str] = None, 
    post_date_start: Optional[str] = None, 
    post_date_end: Optional[str] = None, 
    batch_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get PEO client accounting data (v2 - non-asynchronous version)
    
    Args:
        client_id: Client identifier
        pay_date_start: Pay date range starting date (optional; formatted YYYY-MM-DD)
        pay_date_end: Pay date range ending date (optional; formatted YYYY-MM-DD)
        post_date_start: Post date range starting date (optional; formatted YYYY-MM-DD)
        post_date_end: Post date range ending date (optional; formatted YYYY-MM-DD)
        batch_id: Payroll batch ID to return journal IDs for that specific batch (optional)
        
    Returns:
        Dictionary containing PEO client accounting data from PrismHR for use by external programs (up to 5000 records)
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/generalLedger/v2/getClientGLData"
        params = {
            "clientId": client_id
        }
        
        if pay_date_start:
            params["payDateStart"] = pay_date_start
        if pay_date_end:
            params["payDateEnd"] = pay_date_end
        if post_date_start:
            params["postDateStart"] = post_date_start
        if post_date_end:
            params["postDateEnd"] = post_date_end
        if batch_id:
            params["batchId"] = batch_id
        
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
        logger.error(f"Get client GL data v2 failed: {e}")
        return {"error": f"Get client GL data v2 failed: {e}"}

@mcp.tool()
def get_assigned_pending_approvals(
    prism_user_id: str, 
    client_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of pending approvals
    
    Args:
        prism_user_id: The PrismHR username for which assigned pending approvals should be returned
        client_id: Client identifier (optional)
        
    Returns:
        Dictionary containing list of pending approvals assigned to a specified PrismHR user
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/humanResources/v1/getAssignedPendingApprovals"
        params = {
            "prismUserId": prism_user_id
        }
        
        if client_id:
            params["clientId"] = client_id
        
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
        logger.error(f"Get assigned pending approvals failed: {e}")
        return {"error": f"Get assigned pending approvals failed: {e}"}

@mcp.tool()
def get_onboard_tasks(
    download_id: Optional[str] = None, 
    client_list: Optional[str] = None, 
    from_date: Optional[str] = None, 
    task: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get onboarding tasks
    
    Args:
        download_id: Used to check status of and eventually download the onboard tasks data (optional)
        client_list: Comma separated list of client ids (optional)
        from_date: Only return tasks from the date entered to the current date (optional)
        task: Only return tasks for the task id. Valid task ids are 1 -> I9 section 1, 2 -> Employee information, 3 -> I9 Section 2 or 4 -> All other forms (optional)
        
    Returns:
        Dictionary containing JSON object summary of onboarding tasks for clients
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/humanResources/v1/getOnboardTasks"
        params = {}
        
        if download_id:
            params["downloadId"] = download_id
        if client_list:
            params["clientList"] = client_list
        if from_date:
            params["fromDate"] = from_date
        if task:
            params["task"] = task
        
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
        logger.error(f"Get onboard tasks failed: {e}")
        return {"error": f"Get onboard tasks failed: {e}"}

# Batch 33: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_staffing_placement(
    vendor_id: str, 
    staffing_client: str, 
    placement_id: str
) -> Dict[str, Any]:
    """
    Get staffing placement record
    
    Args:
        vendor_id: Vendor identifier
        staffing_client: Client identifier under the vendor
        placement_id: Staffing placement identifier
        
    Returns:
        Dictionary containing information about a specific staffing placement
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/humanResources/v1/getStaffingPlacement"
        params = {
            "vendorId": vendor_id,
            "staffingClient": staffing_client,
            "placementId": placement_id
        }
        
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
        logger.error(f"Get staffing placement failed: {e}")
        return {"error": f"Get staffing placement failed: {e}"}

@mcp.tool()
def get_staffing_placement_list(
    employee_id: str, 
    client_id: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get staffing placement IDs
    
    Args:
        employee_id: Employee identifier
        client_id: Client identifier (optional)
        count: Number of placement IDs to return per page (optional)
        startpage: Starting position in the placement ID list (optional)
        
    Returns:
        Dictionary containing list of staffing placement IDs associated with a specified employee
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/humanResources/v1/getStaffingPlacementList"
        params = {
            "employeeId": employee_id
        }
        
        if client_id:
            params["clientId"] = client_id
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get staffing placement list failed: {e}")
        return {"error": f"Get staffing placement list failed: {e}"}

@mcp.tool()
def check_permissions_request_status(
    web_service_user: str
) -> Dict[str, Any]:
    """
    Get status for API permissions request
    
    Args:
        web_service_user: The web service user ID
        
    Returns:
        Dictionary containing status for the API permissions request
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/login/v1/checkPermissionsRequestStatus"
        params = {
            "webServiceUser": web_service_user
        }
        
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
        logger.error(f"Check permissions request status failed: {e}")
        return {"error": f"Check permissions request status failed: {e}"}

@mcp.tool()
def get_api_permissions() -> Dict[str, Any]:
    """
    Get current API permissions
    
    Returns:
        Dictionary containing current API permissions for the logged in web service user
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/login/v1/getAPIPermissions"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get API permissions failed: {e}")
        return {"error": f"Get API permissions failed: {e}"}

@mcp.tool()
def get_new_hire_questions(
    state_code: str
) -> Dict[str, Any]:
    """
    Get new hire questions associated with state code
    
    Args:
        state_code: Enter a two-character state code to return new hire questions for that state
        
    Returns:
        Dictionary containing new hire and state default questions associated with a particular state code
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/newHire/v1/getNewHireQuestions"
        params = {
            "stateCode": state_code
        }
        
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
        logger.error(f"Get new hire questions failed: {e}")
        return {"error": f"Get new hire questions failed: {e}"}

# Batch 34: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_new_hire_required_fields(
    client_id: str
) -> Dict[str, Any]:
    """
    Get list of required fields for new hires
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of required fields for a new hire for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/newHire/v1/getNewHireRequiredFields"
        params = {
            "clientId": client_id
        }
        
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
        logger.error(f"Get new hire required fields failed: {e}")
        return {"error": f"Get new hire required fields failed: {e}"}

@mcp.tool()
def check_initialization_status(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Check payroll batch initialization status
    
    Args:
        client_id: Client identifier
        batch_id: Batch identifier
        
    Returns:
        Dictionary containing current status of a payroll batch initialization
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/checkInitializationStatus"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Check initialization status failed: {e}")
        return {"error": f"Check initialization status failed: {e}"}

@mcp.tool()
def get_approval_summary(
    client_id: str, 
    batch_id: str, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get payroll batch summary for approval
    
    Args:
        client_id: Client identifier
        batch_id: Batch identifier
        options: A string containing zero or more of the keywords in the options table (optional)
        
    Returns:
        Dictionary containing summary of an initialized payroll batch that is pending approval
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getApprovalSummary"
        params = {
            "clientId": client_id,
            "batchId": batch_id
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
        logger.error(f"Get approval summary failed: {e}")
        return {"error": f"Get approval summary failed: {e}"}

@mcp.tool()
def get_batch_info(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Get payroll batch information
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch identifier
        
    Returns:
        Dictionary containing payroll control information for the specified payroll batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBatchInfo"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Get batch info failed: {e}")
        return {"error": f"Get batch info failed: {e}"}

@mcp.tool()
def get_batch_list_by_date(
    client_id: str, 
    start_date: str, 
    end_date: str, 
    date_type: str, 
    pay_group: Optional[str] = None
) -> Dict[str, Any]:
    """
    Return Payroll Batches Within a Date Range
    
    Args:
        client_id: Client identifier
        start_date: Starting date for the payroll batch range
        end_date: Ending date for the payroll batch range
        date_type: Whether to use pay periods, pay dates, or post dates when returning batches in the specified date range; valid values are PAY, PERIOD, and POST
        pay_group: Enter a pay group if you want to only return batches associated with that group (optional)
        
    Returns:
        Dictionary containing list of all payroll batches within a specified date range
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBatchListByDate"
        params = {
            "clientId": client_id,
            "startDate": start_date,
            "endDate": end_date,
            "dateType": date_type
        }
        
        if pay_group:
            params["payGroup"] = pay_group
        
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
        logger.error(f"Get batch list by date failed: {e}")
        return {"error": f"Get batch list by date failed: {e}"}

# Batch 35: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_batch_list_for_approval(
    client_id: str
) -> Dict[str, Any]:
    """
    Get a list of batchids available for approval for client
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of batches for a specific client that are ready for client approval
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBatchListForApproval"
        params = {
            "clientId": client_id
        }
        
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
        logger.error(f"Get batch list for approval failed: {e}")
        return {"error": f"Get batch list for approval failed: {e}"}

@mcp.tool()
def get_batch_list_for_initialization(
    client_id: str
) -> Dict[str, Any]:
    """
    Get a list of batch IDs available for initialization for specified client
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of batches for a specific client that are ready for initialization
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBatchListForInitialization"
        params = {
            "clientId": client_id
        }
        
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
        logger.error(f"Get batch list for initialization failed: {e}")
        return {"error": f"Get batch list for initialization failed: {e}"}

@mcp.tool()
def get_batch_payments(
    client_id: str, 
    payroll_number: str
) -> Dict[str, Any]:
    """
    Get batch payments information for an employee
    
    Args:
        client_id: Client identifier
        payroll_number: Payroll identifier
        
    Returns:
        Dictionary containing all pre-calculated payments to be paid during a specific payroll batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBatchPayments"
        params = {
            "clientId": client_id,
            "payrollNumber": payroll_number
        }
        
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
        logger.error(f"Get batch payments failed: {e}")
        return {"error": f"Get batch payments failed: {e}"}

@mcp.tool()
def get_batch_status(
    client_id: str, 
    batch_ids: str
) -> Dict[str, Any]:
    """
    Get the statuses for a list of batches
    
    Args:
        client_id: Client identifier
        batch_ids: Comma separated list of batches (e.g. 20191,20192,20193...)
        
    Returns:
        Dictionary containing statuses for a provided list of payroll batches
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBatchStatus"
        params = {
            "clientId": client_id,
            "batchIds": batch_ids
        }
        
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
        logger.error(f"Get batch status failed: {e}")
        return {"error": f"Get batch status failed: {e}"}

@mcp.tool()
def get_billing_code_totals_by_pay_group(
    client_id: str, 
    batch_id: str, 
    options: str
) -> Dict[str, Any]:
    """
    Get total billing amount for a client and batch broken out by pay group
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch identifier
        options: A string containing zero or more of the keywords in the options table
        
    Returns:
        Dictionary containing billing code totals for a specified payroll batch, broken out by pay group
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBillingCodeTotalsByPayGroup"
        params = {
            "clientId": client_id,
            "batchId": batch_id,
            "options": options
        }
        
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
        logger.error(f"Get billing code totals by pay group failed: {e}")
        return {"error": f"Get billing code totals by pay group failed: {e}"}

# Batch 36: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_billing_code_totals_for_batch(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Get total billing amount for a client and batch
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch identifier
        
    Returns:
        Dictionary containing list of billing codes and the total billing amount for the specified client and payroll batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBillingCodeTotalsForBatch"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Get billing code totals for batch failed: {e}")
        return {"error": f"Get billing code totals for batch failed: {e}"}

@mcp.tool()
def get_billing_code_totals_with_costs(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Get total billing amount with costs for a client and batch
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch identifier
        
    Returns:
        Dictionary containing list of billing codes, the total billing amount, and the total billing costs for the specified client and payroll batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBillingCodeTotalsWithCosts"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Get billing code totals with costs failed: {e}")
        return {"error": f"Get billing code totals with costs failed: {e}"}

@mcp.tool()
def get_billing_rule_unbundled(
    client_id: str, 
    billing_rule_num: str
) -> Dict[str, Any]:
    """
    Get an unbundled billing rule for clientId and billingRuleNum
    
    Args:
        client_id: Client identifier
        billing_rule_num: Unbundled billing rule number
        
    Returns:
        Dictionary containing unbundled billing rule information for the specified client and billing rule number
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBillingRuleUnbundled"
        params = {
            "clientId": client_id,
            "billingRuleNum": billing_rule_num
        }
        
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
        logger.error(f"Get billing rule unbundled failed: {e}")
        return {"error": f"Get billing rule unbundled failed: {e}"}

@mcp.tool()
def get_billing_vouchers(
    client_id: str, 
    pay_date_start: str, 
    pay_date_end: str, 
    bill_type: Optional[List[str]] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None, 
    options: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get list of billing vouchers for clientId and date range
    
    Args:
        client_id: Client identifier
        pay_date_start: Starting pay date, inclusive (format YYYY-MM-DD)
        pay_date_end: Ending pay date, inclusive (format YYYY-MM-DD)
        bill_type: Type of billing to retrieve the amount for (optional)
        count: Number of vouchers returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        options: One or more options: "Initialized", "PEOClientAccounting" (optional)
        
    Returns:
        Dictionary containing list of employee billing vouchers for the specified client and pay dates
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBillingVouchers"
        params = {
            "clientId": client_id,
            "payDateStart": pay_date_start,
            "payDateEnd": pay_date_end
        }
        
        if bill_type:
            params["billType"] = bill_type
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        if options:
            params["options"] = options
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get billing vouchers failed: {e}")
        return {"error": f"Get billing vouchers failed: {e}"}

@mcp.tool()
def get_billing_vouchers_by_batch(
    client_id: str, 
    batch_id: str, 
    bill_type: Optional[List[str]] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None, 
    options: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get list of initialized or finalized billing vouchers for clientId and batchId
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch identifier
        bill_type: Type of billing to retrieve the amount for (optional)
        count: Number of vouchers returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        options: One or more options: "Initialized", "PEOClientAccounting", "BillSort" (optional)
        
    Returns:
        Dictionary containing billing vouchers based on the payroll batch that was used to generate them
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBillingVouchersByBatch"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
        if bill_type:
            params["billType"] = bill_type
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        if options:
            params["options"] = options
        
        query_string = urllib.parse.urlencode(params, doseq=True)
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
        logger.error(f"Get billing vouchers by batch failed: {e}")
        return {"error": f"Get billing vouchers by batch failed: {e}"}

# Batch 37: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_bulk_year_to_date_values(
    download_id: Optional[str] = None, 
    client_id: Optional[str] = None, 
    employee_id: Optional[str] = None, 
    voucher_id: Optional[str] = None, 
    as_of_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get bulk year to date values
    
    Args:
        download_id: Used to check status of and eventually download the compiled YTD data (optional)
        client_id: Return results for only this client (optional)
        employee_id: Return results for only this employee (optional)
        voucher_id: Return results for only this voucher (optional)
        as_of_date: The method will return year-to-date payroll data starting from January first of the year provided and ending in this date (optional)
        
    Returns:
        Dictionary containing JSON object summary of year-to-date values for different payroll variables
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getBulkYearToDateValues"
        params = {}
        
        if download_id:
            params["downloadId"] = download_id
        if client_id:
            params["clientId"] = client_id
        if employee_id:
            params["employeeId"] = employee_id
        if voucher_id:
            params["voucherId"] = voucher_id
        if as_of_date:
            params["asOfDate"] = as_of_date
        
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
        logger.error(f"Get bulk year to date values failed: {e}")
        return {"error": f"Get bulk year to date values failed: {e}"}

@mcp.tool()
def get_clients_with_vouchers(
    pay_date_start: str, 
    pay_date_end: str
) -> Dict[str, Any]:
    """
    Get the list of clients with at least one payroll voucher
    
    Args:
        pay_date_start: Starting pay date, inclusive (format YYYY-MM-DD)
        pay_date_end: Ending pay date, inclusive (format YYYY-MM-DD)
        
    Returns:
        Dictionary containing list of clients who have at least one payroll voucher during the specified date range
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getClientsWithVouchers"
        params = {
            "payDateStart": pay_date_start,
            "payDateEnd": pay_date_end
        }
        
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
        logger.error(f"Get clients with vouchers failed: {e}")
        return {"error": f"Get clients with vouchers failed: {e}"}

@mcp.tool()
def get_employee_401k_contributions_by_date(
    client_id: str, 
    start_date: str, 
    end_date: str, 
    retirement_plan_id: Optional[str] = None, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of employee 401K contributions
    
    Args:
        client_id: Client identifier
        start_date: Start of the period from which to pull payroll vouchers
        end_date: End of the period from which to pull payroll vouchers
        retirement_plan_id: Enter a 401(k) plan ID to return data about that plan (optional)
        options: A string containing zero or more of the keywords in the options table (optional)
        
    Returns:
        Dictionary containing employee 401(k) contributions associated with vouchers within a specified date range
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getEmployee401KContributionsByDate"
        params = {
            "clientId": client_id,
            "startDate": start_date,
            "endDate": end_date
        }
        
        if retirement_plan_id:
            params["retirementPlanId"] = retirement_plan_id
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
        logger.error(f"Get employee 401K contributions by date failed: {e}")
        return {"error": f"Get employee 401K contributions by date failed: {e}"}

@mcp.tool()
def get_employee_for_batch(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Get list of employee IDs for clientId and batchId
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch identifier
        
    Returns:
        Dictionary containing list of employee IDs for the specified client and payroll batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getEmployeeForBatch"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Get employee for batch failed: {e}")
        return {"error": f"Get employee for batch failed: {e}"}

@mcp.tool()
def get_employee_override_rates(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get list of employee override rates
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing employee override rate information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getEmployeeOverrideRates"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get employee override rates failed: {e}")
        return {"error": f"Get employee override rates failed: {e}"}

# Batch 38: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_employee_payroll_summary(
    client_id: str, 
    employee_id: str, 
    year: str
) -> Dict[str, Any]:
    """
    Get an employee's payroll summary
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        year: Year for which you want to return payroll summary data
        
    Returns:
        Dictionary containing voucher-by-voucher payroll summary for the specified client, employee, and year
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getEmployeePayrollSummary"
        params = {
            "clientId": client_id,
            "employeeId": employee_id,
            "year": year
        }
        
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
        logger.error(f"Get employee payroll summary failed: {e}")
        return {"error": f"Get employee payroll summary failed: {e}"}

@mcp.tool()
def get_external_pto_balance(
    client_id: str, 
    batch_id: str, 
    include_history: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get external PTO balance data
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch identifier
        include_history: Whether to include historical PTO balance data in the response; valid values are true, false (default), or empty string (optional)
        
    Returns:
        Dictionary containing PTO balance information that was written to the PrismHR system from an external source
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getExternalPtoBalance"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
        if include_history:
            params["includeHistory"] = include_history
        
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
        logger.error(f"Get external PTO balance failed: {e}")
        return {"error": f"Get external PTO balance failed: {e}"}

@mcp.tool()
def get_manual_checks(
    client_id: str, 
    reference: Optional[str] = None, 
    employee_id: Optional[str] = None, 
    check_date: Optional[str] = None, 
    check_status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve information about manual checks
    
    Args:
        client_id: Client identifier
        reference: Manual check reference number (optional)
        employee_id: Employee identifier filter (optional)
        check_date: Check date filter formatted as YYYY-MM-DD (optional)
        check_status: Check status filter: (POST)ed, (INIT)ialized, or (PEND)ing (optional)
        
    Returns:
        Dictionary containing list of manual checks entered into the system
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getManualChecks"
        params = {
            "clientId": client_id
        }
        
        if reference:
            params["reference"] = reference
        if employee_id:
            params["employeeId"] = employee_id
        if check_date:
            params["checkDate"] = check_date
        if check_status:
            params["checkStatus"] = check_status
        
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
        logger.error(f"Get manual checks failed: {e}")
        return {"error": f"Get manual checks failed: {e}"}

@mcp.tool()
def get_payroll_approval(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Get payroll approval info for a client
    
    Args:
        client_id: Client identifier
        batch_id: Batch identifier
        
    Returns:
        Dictionary containing payroll approval information for a specific batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollApproval"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Get payroll approval failed: {e}")
        return {"error": f"Get payroll approval failed: {e}"}

@mcp.tool()
def get_payroll_batch_with_options(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Get a list of batches with payroll control options
    
    Args:
        client_id: Client identifier
        batch_id: ID of the payroll batch to return
        
    Returns:
        Dictionary containing list of payroll batches along with their batch-specific Payroll Control options
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollBatchWithOptions"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Get payroll batch with options failed: {e}")
        return {"error": f"Get payroll batch with options failed: {e}"}

# Batch 39: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_payroll_notes(
    client_id: str
) -> Dict[str, Any]:
    """
    Get payroll notes
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of payroll notes for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollNotes"
        params = {
            "clientId": client_id
        }
        
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
        logger.error(f"Get payroll notes failed: {e}")
        return {"error": f"Get payroll notes failed: {e}"}

@mcp.tool()
def get_payroll_schedule(
    schedule_code: str
) -> Dict[str, Any]:
    """
    Get a payroll schedule using scheduleCode
    
    Args:
        schedule_code: Payroll schedule identifier
        
    Returns:
        Dictionary containing details of the specified payroll schedule
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollSchedule"
        params = {
            "scheduleCode": schedule_code
        }
        
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
        logger.error(f"Get payroll schedule failed: {e}")
        return {"error": f"Get payroll schedule failed: {e}"}

@mcp.tool()
def get_payroll_schedule_codes() -> Dict[str, Any]:
    """
    Get a list of available schedule codes with their description
    
    Returns:
        Dictionary containing list of schedule codes and their descriptions
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollScheduleCodes"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get payroll schedule codes failed: {e}")
        return {"error": f"Get payroll schedule codes failed: {e}"}

@mcp.tool()
def get_payroll_summary(
    client_id: str, 
    year: Optional[str] = None, 
    batch_type: Optional[str] = None, 
    batch_id: Optional[str] = None, 
    include_details: Optional[bool] = None, 
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get payroll summary
    
    Args:
        client_id: Client identifier
        year: Calendar year (YYYY). Must be an existing year not greater than the current year and will default to the current year if no value is passed (optional)
        batch_type: One or more type of payroll batches separated by a comma to return: A=All Types is the default option; R=Scheduled; S=Special; J=Adjustment; V=Reversal; M=Manual (optional)
        batch_id: Valid payroll batch identifier for the selected client (optional)
        include_details: Can only be true if a batchId is passed. true will return the details of all the payroll vouchers for the given batchId in conjunction with sort (optional)
        sort: Specify the sort details to return for the list of payroll vouchers for the given batchId. You can only use this parameter if includeDetails is set to true. Only one of the following values is allowed: PAYCODE, POSITION, DEPT, LOC, DIV, SHIFT, PROJ and EMPLOYEE (default value) (optional)
        
    Returns:
        Dictionary containing list of completed payroll batches for a given client, for the specified batch types and calendar year
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollSummary"
        params = {
            "clientId": client_id
        }
        
        if year:
            params["year"] = year
        if batch_type:
            params["batchType"] = batch_type
        if batch_id:
            params["batchId"] = batch_id
        if include_details is not None:
            params["includeDetails"] = include_details
        if sort:
            params["sort"] = sort
        
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
        logger.error(f"Get payroll summary failed: {e}")
        return {"error": f"Get payroll summary failed: {e}"}

@mcp.tool()
def get_payroll_voucher_by_id(
    client_id: str, 
    voucher_id: str, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a payroll voucher for clientId and voucherId
    
    Args:
        client_id: Client identifier
        voucher_id: Payroll voucher number
        options: A string containing zero or more of the keywords in the options table (optional)
        
    Returns:
        Dictionary containing employee payroll voucher for the specified client and voucher
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollVoucherById"
        params = {
            "clientId": client_id,
            "voucherId": voucher_id
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
        logger.error(f"Get payroll voucher by id failed: {e}")
        return {"error": f"Get payroll voucher by id failed: {e}"}

# Batch 40: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_payroll_voucher_for_batch(
    client_id: str, 
    batch_id: str, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of employee payroll vouchers for clientId and batchId
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch identifier
        count: Number of vouchers returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        options: A string containing zero or more of the keywords in the options table (optional)
        
    Returns:
        Dictionary containing list of employee payroll vouchers for the specified client and payroll batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollVoucherForBatch"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
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
        logger.error(f"Get payroll voucher for batch failed: {e}")
        return {"error": f"Get payroll voucher for batch failed: {e}"}

@mcp.tool()
def get_payroll_vouchers(
    client_id: str, 
    pay_date_start: str, 
    pay_date_end: str, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of employee payroll vouchers for clientId and date range
    
    Args:
        client_id: Client identifier
        pay_date_start: Starting pay date, inclusive (format YYYY-MM-DD)
        pay_date_end: Ending pay date, inclusive (format YYYY-MM-DD)
        count: Number of vouchers returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        options: A string containing zero or more of the keywords in the options table (optional)
        
    Returns:
        Dictionary containing list of employee payroll vouchers for the specified client and pay dates
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollVouchers"
        params = {
            "clientId": client_id,
            "payDateStart": pay_date_start,
            "payDateEnd": pay_date_end
        }
        
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
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
        logger.error(f"Get payroll vouchers failed: {e}")
        return {"error": f"Get payroll vouchers failed: {e}"}

@mcp.tool()
def get_payroll_vouchers_for_employee(
    client_id: str, 
    employee_id: str, 
    pay_date_start: str, 
    pay_date_end: str, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None, 
    options: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of employee payroll vouchers for employeeId, clientId, and dates
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        pay_date_start: Start of date range
        pay_date_end: End of date range
        count: Number of vouchers returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        options: A string containing zero or more of the keywords in the options table (optional)
        
    Returns:
        Dictionary containing payroll vouchers for a specific employee, client, and date range
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getPayrollVouchersForEmployee"
        params = {
            "clientId": client_id,
            "employeeId": employee_id,
            "payDateStart": pay_date_start,
            "payDateEnd": pay_date_end
        }
        
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
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
        logger.error(f"Get payroll vouchers for employee failed: {e}")
        return {"error": f"Get payroll vouchers for employee failed: {e}"}

@mcp.tool()
def get_process_schedule(
    process_schedule_id: str
) -> Dict[str, Any]:
    """
    Get a process schedule using processScheduleId
    
    Args:
        process_schedule_id: Processing schedule identifier
        
    Returns:
        Dictionary containing details of the specified processing schedule
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getProcessSchedule"
        params = {
            "processScheduleId": process_schedule_id
        }
        
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
        logger.error(f"Get process schedule failed: {e}")
        return {"error": f"Get process schedule failed: {e}"}

@mcp.tool()
def get_process_schedule_codes() -> Dict[str, Any]:
    """
    Get a list of available process schedule IDs with their corresponding description
    
    Returns:
        Dictionary containing list of process schedule codes and their descriptions
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getProcessScheduleCodes"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get process schedule codes failed: {e}")
        return {"error": f"Get process schedule codes failed: {e}"}

# Batch 41: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_retirement_adj_voucher_list_by_date(
    client_id: str, 
    date_type: str, 
    start_date: str, 
    end_date: str, 
    employee_id: Optional[str] = None, 
    download_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get retirement adj voucher-list by date
    
    Args:
        client_id: Client identifier
        date_type: P = date adjustment was processed, A = adjustment date
        start_date: Process/Adjustment start date range (format: YYYY-MM-DD)
        end_date: Process/Adjustment end date range (format: YYYY-MM-DD)
        employee_id: Employee identifier (optional)
        download_id: Identifier used to check status of / download data (optional)
        
    Returns:
        Dictionary containing retirement adjustment voucher id's by adjustment (pay date) or process date
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getRetirementAdjVoucherListByDate"
        params = {
            "clientId": client_id,
            "dateType": date_type,
            "startDate": start_date,
            "endDate": end_date
        }
        
        if employee_id:
            params["employeeId"] = employee_id
        if download_id:
            params["downloadId"] = download_id
        
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
        logger.error(f"Get retirement adj voucher list by date failed: {e}")
        return {"error": f"Get retirement adj voucher list by date failed: {e}"}

@mcp.tool()
def get_scheduled_payments(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get scheduled payments information for an employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing employee's scheduled payment information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getScheduledPayments"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get scheduled payments failed: {e}")
        return {"error": f"Get scheduled payments failed: {e}"}

@mcp.tool()
def get_standard_hours(
    client_id: str
) -> Dict[str, Any]:
    """
    Get the list of standardHours objects for clientId
    
    Args:
        client_id: Client identifier
        
    Returns:
        Dictionary containing array of standardHours objects for the specified client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getStandardHours"
        params = {
            "clientId": client_id
        }
        
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
        logger.error(f"Get standard hours failed: {e}")
        return {"error": f"Get standard hours failed: {e}"}

@mcp.tool()
def get_year_to_date_values(
    client_id: str, 
    employee_id: str, 
    as_of_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get period to date payroll values
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        as_of_date: The ending date for PTD calculation (format YYYY-MM-DD) - if omitted, today's date is used (optional)
        
    Returns:
        Dictionary containing period to date (year, quarter, and month) payroll values
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/getYearToDateValues"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
        if as_of_date:
            params["asOfDate"] = as_of_date
        
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
        logger.error(f"Get year to date values failed: {e}")
        return {"error": f"Get year to date values failed: {e}"}

@mcp.tool()
def get_pay_group_schedule_report(
    client_id: str, 
    pay_group: str, 
    pay_date_start: str, 
    pay_date_end: str, 
    download_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Pay Group Schedule Report
    
    Args:
        client_id: Client ID associated with the payGroup
        pay_group: Pay group identifier
        pay_date_start: Start of report date range (format: YYYY-MM-DD)
        pay_date_end: End of report date range (format: YYYY-MM-DD)
        download_id: Identifier used to check status/download data (optional)
        
    Returns:
        Dictionary containing pay schedule information for a specified client, pay group, and date range
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/payGroupScheduleReport"
        params = {
            "clientId": client_id,
            "payGroup": pay_group,
            "payDateStart": pay_date_start,
            "payDateEnd": pay_date_end
        }
        
        if download_id:
            params["downloadId"] = download_id
        
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
        logger.error(f"Get pay group schedule report failed: {e}")
        return {"error": f"Get pay group schedule report failed: {e}"}

# Batch 42: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def reprint_check_stub(
    client_id: str, 
    employee_id: str, 
    voucher_id: str
) -> Dict[str, Any]:
    """
    Retrieve an employee's check stub
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        voucher_id: Payroll voucher number
        
    Returns:
        Dictionary containing PDF check stub generation status and redirect URL
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/payroll/v1/reprintCheckStub"
        params = {
            "clientId": client_id,
            "employeeId": employee_id,
            "voucherId": voucher_id
        }
        
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
        logger.error(f"Reprint check stub failed: {e}")
        return {"error": f"Reprint check stub failed: {e}"}

@mcp.tool()
def get_allowed_employee_list(
    prism_user_id: str, 
    client_id: str, 
    employee_id: Optional[str] = None, 
    last_name: Optional[str] = None, 
    first_name: Optional[str] = None, 
    employee_status_class: Optional[str] = None, 
    startpage: Optional[str] = None, 
    count: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of allowed employees
    
    Args:
        prism_user_id: PrismHR username
        client_id: Client identifier
        employee_id: Employee ID filter (optional)
        last_name: Employee last name filter (optional)
        first_name: Employee first name filter (optional)
        employee_status_class: Available options are A T L which are Active, Terminated, On Leave (optional)
        startpage: Pagination start location (first page = '0') (optional)
        count: Number of employees returned per page (optional)
        
    Returns:
        Dictionary containing list of employees associated with the specified client and accessible to the specified PrismHR user
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getAllowedEmployeeList"
        params = {
            "prismUserId": prism_user_id,
            "clientId": client_id
        }
        
        if employee_id:
            params["employeeId"] = employee_id
        if last_name:
            params["lastName"] = last_name
        if first_name:
            params["firstName"] = first_name
        if employee_status_class:
            params["employeeStatusClass"] = employee_status_class
        if startpage:
            params["startpage"] = startpage
        if count:
            params["count"] = count
        
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
        logger.error(f"Get allowed employee list failed: {e}")
        return {"error": f"Get allowed employee list failed: {e}"}

@mcp.tool()
def get_client_list_security(
    prism_user_id: str
) -> Dict[str, Any]:
    """
    Get list of allowed clients
    
    Args:
        prism_user_id: The PrismHR username
        
    Returns:
        Dictionary containing list of client IDs that the PrismHR user can access
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getClientList"
        params = {
            "prismUserId": prism_user_id
        }
        
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
        logger.error(f"Get client list security failed: {e}")
        return {"error": f"Get client list security failed: {e}"}

@mcp.tool()
def get_employee_client_list(
    prism_user_id: Optional[str] = None, 
    employee_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of applicable clients for a provided employee user
    
    Args:
        prism_user_id: Prism user identifier (optional)
        employee_id: Employee identifier (optional)
        
    Returns:
        Dictionary containing list of clients and the employee's status for the specified employee user
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getEmployeeClientList"
        params = {}
        
        if prism_user_id:
            params["prismUserId"] = prism_user_id
        if employee_id:
            params["employeeId"] = employee_id
        
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
        logger.error(f"Get employee client list failed: {e}")
        return {"error": f"Get employee client list failed: {e}"}

@mcp.tool()
def get_employee_list_security(
    prism_user_id: str, 
    client_id: str
) -> Dict[str, Any]:
    """
    Get list of allowed employees
    
    Args:
        prism_user_id: The PrismHR username
        client_id: Client identifier
        
    Returns:
        Dictionary containing list of employee IDs employed by the specified client that the PrismHR user can access
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getEmployeeList"
        params = {
            "prismUserId": prism_user_id,
            "clientId": client_id
        }
        
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
        logger.error(f"Get employee list security failed: {e}")
        return {"error": f"Get employee list security failed: {e}"}

# Batch 43: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_entity_access(
    prism_user_id: str, 
    client_id: str
) -> Dict[str, Any]:
    """
    Get entities access for a user
    
    Args:
        prism_user_id: The PrismHR username
        client_id: Client identifier
        
    Returns:
        Dictionary containing the entities that a PrismHR worksite manager or trusted advisor user can access
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getEntityAccess"
        params = {
            "prismUserId": prism_user_id,
            "clientId": client_id
        }
        
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
        logger.error(f"Get entity access failed: {e}")
        return {"error": f"Get entity access failed: {e}"}

@mcp.tool()
def get_manager_list(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Get list of managers that can see a given employee
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing list of PrismHR users that can see/manage a specified user
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getManagerList"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get manager list failed: {e}")
        return {"error": f"Get manager list failed: {e}"}

@mcp.tool()
def get_user_data_security(
    client_id: str, 
    prism_user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get entity access settings
    
    Args:
        client_id: Client identifier
        prism_user_id: ID of a Worksite Employee, Worksite Manager, or Worksite Trusted Advisor user (optional - omit to retrieve client data security object shell)
        
    Returns:
        Dictionary containing client entity access settings for a specified PrismHR user or client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getUserDataSecurity"
        params = {
            "clientId": client_id
        }
        
        if prism_user_id:
            params["prismUserId"] = prism_user_id
        
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
        logger.error(f"Get user data security failed: {e}")
        return {"error": f"Get user data security failed: {e}"}

@mcp.tool()
def get_user_details(
    prism_user_id: str
) -> Dict[str, Any]:
    """
    Get PrismHR user details
    
    Args:
        prism_user_id: The PrismHR username
        
    Returns:
        Dictionary containing the User Details of a PrismHR user
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getUserDetails"
        params = {
            "prismUserId": prism_user_id
        }
        
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
        logger.error(f"Get user details failed: {e}")
        return {"error": f"Get user details failed: {e}"}

@mcp.tool()
def get_user_list_security(
    client_id: Optional[str] = None, 
    user_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of PrismHR users
    
    Args:
        client_id: Client identifier (optional)
        user_type: User type: 'I' (service provider), 'M' (worksite manager), or 'A' (worksite trusted advisor) (optional)
        
    Returns:
        Dictionary containing list of PrismHR users
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getUserList"
        params = {}
        
        if client_id:
            params["clientId"] = client_id
        if user_type:
            params["userType"] = user_type
        
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
        logger.error(f"Get user list security failed: {e}")
        return {"error": f"Get user list security failed: {e}"}

# Batch 44: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_user_role_details(
    role_id: str
) -> Dict[str, Any]:
    """
    Get PrismHR user role details
    
    Args:
        role_id: User role identifier
        
    Returns:
        Dictionary containing information about the form- and field-level access granted by a particular user role
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getUserRoleDetails"
        params = {
            "roleId": role_id
        }
        
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
        logger.error(f"Get user role details failed: {e}")
        return {"error": f"Get user role details failed: {e}"}

@mcp.tool()
def get_user_roles_list() -> Dict[str, Any]:
    """
    Get PrismHR user roles list
    
    Returns:
        Dictionary containing complete list of PrismHR user roles
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/getUserRolesList"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get user roles list failed: {e}")
        return {"error": f"Get user roles list failed: {e}"}

@mcp.tool()
def is_client_allowed(
    prism_user_id: str, 
    client_id: str
) -> Dict[str, Any]:
    """
    Check if client is allowed
    
    Args:
        prism_user_id: The PrismHR username
        client_id: Client identifier
        
    Returns:
        Dictionary containing Boolean value: True if the PrismHR user can access the specified client, otherwise False
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/isClientAllowed"
        params = {
            "prismUserId": prism_user_id,
            "clientId": client_id
        }
        
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
        logger.error(f"Is client allowed failed: {e}")
        return {"error": f"Is client allowed failed: {e}"}

@mcp.tool()
def is_employee_allowed(
    prism_user_id: str, 
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Check if employee is allowed
    
    Args:
        prism_user_id: The PrismHR username
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing Boolean value: True if the PrismHR user can access the specified employee when employed by the specified client, otherwise False
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v1/isEmployeeAllowed"
        params = {
            "prismUserId": prism_user_id,
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Is employee allowed failed: {e}")
        return {"error": f"Is employee allowed failed: {e}"}

@mcp.tool()
def get_user_list_v2(
    client_id: Optional[str] = None, 
    user_type: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of PrismHR users (v2)
    
    Args:
        client_id: Client identifier (optional)
        user_type: User type: 'I' (service provider), 'M' (worksite manager), or 'A' (worksite trusted advisor) (optional)
        count: Number of users to return per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing list of PrismHR users with pagination support
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/prismSecurity/v2/getUserList"
        params = {}
        
        if client_id:
            params["clientId"] = client_id
        if user_type:
            params["userType"] = user_type
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get user list v2 failed: {e}")
        return {"error": f"Get user list v2 failed: {e}"}

# Batch 45: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_employee_image(
    user_id: str
) -> Dict[str, Any]:
    """
    Get employee image
    
    Args:
        user_id: User ID of the employee
        
    Returns:
        Dictionary containing employee image data in Base64 format
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/signOn/v1/getEmployeeImage"
        params = {
            "userId": user_id
        }
        
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
        logger.error(f"Get employee image failed: {e}")
        return {"error": f"Get employee image failed: {e}"}

@mcp.tool()
def get_favorites(
    user_id: str
) -> Dict[str, Any]:
    """
    Get favorites
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary containing array of the user's favorite PrismHR forms with names and formIds
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/signOn/v1/getFavorites"
        params = {
            "userId": user_id
        }
        
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
        logger.error(f"Get favorites failed: {e}")
        return {"error": f"Get favorites failed: {e}"}

@mcp.tool()
def get_vendor_info(
    client_id: str, 
    user_id: str, 
    ext_vendor_id: str
) -> Dict[str, Any]:
    """
    Get vendor info
    
    Args:
        client_id: Client identifier
        user_id: ID of the PrismHR user associated with the vendor field or fields
        ext_vendor_id: SSO Service ID associated with the vendor in PrismHR
        
    Returns:
        Dictionary containing vendor-specific custom field data associated with a particular PrismHR user
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/signOn/v1/getVendorInfo"
        params = {
            "clientId": client_id,
            "userId": user_id,
            "extVendorId": ext_vendor_id
        }
        
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
        logger.error(f"Get vendor info failed: {e}")
        return {"error": f"Get vendor info failed: {e}"}

@mcp.tool()
def get_all_subscriptions(
    user_string_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get all subscriptions
    
    Args:
        user_string_id: User-defined keyword string to (exact) match on (optional)
        
    Returns:
        Dictionary containing multiple subscriptions
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/subscription/v1/getAllSubscriptions"
        params = {}
        
        if user_string_id:
            params["userStringId"] = user_string_id
        
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
        logger.error(f"Get all subscriptions failed: {e}")
        return {"error": f"Get all subscriptions failed: {e}"}

@mcp.tool()
def get_events(
    subscription_id: str, 
    replay_id: str, 
    number_of_events: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get events from the event stream
    
    Args:
        subscription_id: ID of the subscription to use when retrieving events
        replay_id: The starting point in the event stream for retrieving events
        number_of_events: The number of events to retrieve (optional)
        
    Returns:
        Dictionary containing events from the event stream
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/subscription/v1/getEvents"
        params = {
            "subscriptionId": subscription_id,
            "replayId": replay_id
        }
        
        if number_of_events:
            params["numberOfEvents"] = number_of_events
        
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
        logger.error(f"Get events failed: {e}")
        return {"error": f"Get events failed: {e}"}

# Batch 46: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_new_events(
    subscription_id: str, 
    number_of_events: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get new events from the event stream
    
    Args:
        subscription_id: ID of the subscription to use when retrieving events
        number_of_events: The number of events to retrieve (optional)
        
    Returns:
        Dictionary containing new events from the event stream using stored replayId
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/subscription/v1/getNewEvents"
        params = {
            "subscriptionId": subscription_id
        }
        
        if number_of_events:
            params["numberOfEvents"] = number_of_events
        
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
        logger.error(f"Get new events failed: {e}")
        return {"error": f"Get new events failed: {e}"}

@mcp.tool()
def get_subscription(
    subscription_id: str
) -> Dict[str, Any]:
    """
    Get a subscription by its ID
    
    Args:
        subscription_id: ID of the subscription to retrieve
        
    Returns:
        Dictionary containing single subscription using its unique identifier
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/subscription/v1/getSubscription"
        params = {
            "subscriptionId": subscription_id
        }
        
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
        logger.error(f"Get subscription failed: {e}")
        return {"error": f"Get subscription failed: {e}"}

@mcp.tool()
def get_ach_file_list(
    originator_id: str, 
    post_date_start: str, 
    post_date_end: Optional[str] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get ACH files list
    
    Args:
        originator_id: ACH originator ID
        post_date_start: Starting date for range of post dates to return (format: YYYY-MM-DD)
        post_date_end: Optional end date for range of post dates to return (format: YYYY-MM-DD) (optional)
        count: Number of ACH files returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing list of ACH files that can be downloaded
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getACHFileList"
        params = {
            "originatorId": originator_id,
            "postDateStart": post_date_start
        }
        
        if post_date_end:
            params["postDateEnd"] = post_date_end
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get ACH file list failed: {e}")
        return {"error": f"Get ACH file list failed: {e}"}

@mcp.tool()
def get_ar_transaction_report(
    start_date: str, 
    end_date: str, 
    download_id: Optional[str] = None, 
    client_id: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generate an AR transaction report
    
    Args:
        start_date: AR transaction report start date (format: YYYY-MM-DD)
        end_date: AR transaction report end date (format: YYYY-MM-DD)
        download_id: Identifier used to check status of / download data (optional)
        client_id: Use this option to limit the response to one or more client IDs (optional)
        
    Returns:
        Dictionary containing AR transaction report generation status and download URL
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getARTransactionReport"
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        
        if download_id:
            params["downloadId"] = download_id
        if client_id:
            params["clientId"] = client_id
        
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
        logger.error(f"Get AR transaction report failed: {e}")
        return {"error": f"Get AR transaction report failed: {e}"}

@mcp.tool()
def get_data(
    schema_name: str, 
    class_name: str, 
    download_id: Optional[str] = None, 
    client_id: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Retrieve datasets from the system
    
    Args:
        schema_name: Name of the object schema
        class_name: Name of the object class
        download_id: Identifier used to check status of / download data (optional)
        client_id: Client ID filter (optional)
        
    Returns:
        Dictionary containing system data for external programs with build status and download URL
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getData"
        params = {
            "schemaName": schema_name,
            "className": class_name
        }
        
        if download_id:
            params["downloadId"] = download_id
        if client_id:
            params["clientId"] = client_id
        
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
        logger.error(f"Get data failed: {e}")
        return {"error": f"Get data failed: {e}"}

# Batch 47: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_employer_details(
    employer_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Employer Details
    
    Args:
        employer_id: Identification number for employer; if the web service user has client restrictions, enter clientId.employerId to retrieve data about a single employer (optional)
        
    Returns:
        Dictionary containing information about all employers in the system
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getEmployerDetails"
        params = {}
        
        if employer_id:
            params["employerId"] = employer_id
        
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
        logger.error(f"Get employer details failed: {e}")
        return {"error": f"Get employer details failed: {e}"}

@mcp.tool()
def get_invoice_data(
    client_id: str, 
    batch_id: Optional[str] = None, 
    invoice_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Invoice Data
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch ID, if returning all invoice data for a batch (optional)
        invoice_id: Invoice ID, if returning data about a specific invoice (optional)
        
    Returns:
        Dictionary containing data from a specified invoice or from all invoices associated with a particular payroll batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getInvoiceData"
        params = {
            "clientId": client_id
        }
        
        if batch_id:
            params["batchId"] = batch_id
        if invoice_id:
            params["invoiceId"] = invoice_id
        
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
        logger.error(f"Get invoice data failed: {e}")
        return {"error": f"Get invoice data failed: {e}"}

@mcp.tool()
def get_multi_entity_group_list(
    count: Optional[str] = None, 
    startpage: Optional[str] = None, 
    client_id: Optional[str] = None, 
    multi_entity_group_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Multi Entity Group List
    
    Args:
        count: Number of multientity groups returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        client_id: Client identifier (optional)
        multi_entity_group_id: Multi-entity group identifier (optional)
        
    Returns:
        Dictionary containing list of multi-entity groups with pagination support
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getMultiEntityGroupList"
        params = {}
        
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        if client_id:
            params["clientId"] = client_id
        if multi_entity_group_id:
            params["multiEntityGroupId"] = multi_entity_group_id
        
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
        logger.error(f"Get multi entity group list failed: {e}")
        return {"error": f"Get multi entity group list failed: {e}"}

@mcp.tool()
def get_payee(
    payee_id: Optional[str] = None, 
    payee_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve payee information
    
    Args:
        payee_id: Enter payee id to return specific payee (optional)
        payee_type: Payee Type (G- Garnishing Authority, D- State Disbursement Unit, T- Tax Authority, C- Carrier, O- Other) (optional)
        
    Returns:
        Dictionary containing system Payee information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getPayee"
        params = {}
        
        if payee_id:
            params["payeeId"] = payee_id
        if payee_type:
            params["payeeType"] = payee_type
        
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
        logger.error(f"Get payee failed: {e}")
        return {"error": f"Get payee failed: {e}"}

@mcp.tool()
def get_payments_pending(
    client_id: Optional[str] = None, 
    batch_id: Optional[str] = None, 
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Payments Pending information
    
    Args:
        client_id: Enter a client ID to return payments pending for only that client (optional)
        batch_id: Enter a batch number to return payment pending data for only that batch; a clientId is also required in this case (optional)
        status: Enter either WT.PEND or PAYPEND to only return batches in that status (optional)
        
    Returns:
        Dictionary containing information about payments and wire transfers in Pending status
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getPaymentsPending"
        params = {}
        
        if client_id:
            params["clientId"] = client_id
        if batch_id:
            params["batchId"] = batch_id
        if status:
            params["status"] = status
        
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
        logger.error(f"Get payments pending failed: {e}")
        return {"error": f"Get payments pending failed: {e}"}

# Batch 48: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_positive_pay_check_stub() -> Dict[str, Any]:
    """
    Get positive pay check stub
    
    Returns:
        Dictionary containing Positive Pay check stub IDs and the bank account IDs associated with them
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getPositivePayCheckStub"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Get positive pay check stub failed: {e}")
        return {"error": f"Get positive pay check stub failed: {e}"}

@mcp.tool()
def get_positive_pay_file_list(
    checking_acct: Optional[str] = None, 
    file_stub: Optional[str] = None, 
    date_created: Optional[str] = None, 
    date_created_start: Optional[str] = None, 
    date_created_end: Optional[str] = None, 
    most_recent: Optional[bool] = None, 
    count: Optional[str] = None, 
    startpage: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get positive pay files list
    
    Args:
        checking_acct: Enter the checking account used to create positive pay file (optional)
        file_stub: Enter the file stub name used to create positive pay file (optional)
        date_created: Specify a date in YYYY-MM-DD format to retrieve positive pay files created on that date; do not use in combination with start and end date parameters (optional)
        date_created_start: Start date to retrieve positive pay files created in a certain date range; must use in combination with dateCreatedEnd; do not use with dateCreated (optional)
        date_created_end: End date to retrieve positive pay files created within a certain date range; must use in combination with dateCreatedStart; do not use with dateCreated (optional)
        most_recent: If true, the endpoint returns the most recently created positive pay file record for the specified checkingAcct and date parameters (optional)
        count: Number of positive pay files returned per page (optional)
        startpage: Pagination start location (first page = '0') (optional)
        
    Returns:
        Dictionary containing list of existing positive pay files that can be recreated
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getPositivePayFileList"
        params = {}
        
        if checking_acct:
            params["checkingAcct"] = checking_acct
        if file_stub:
            params["fileStub"] = file_stub
        if date_created:
            params["dateCreated"] = date_created
        if date_created_start:
            params["dateCreatedStart"] = date_created_start
        if date_created_end:
            params["dateCreatedEnd"] = date_created_end
        if most_recent is not None:
            params["mostRecent"] = str(most_recent).lower()
        if count:
            params["count"] = count
        if startpage:
            params["startpage"] = startpage
        
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
        logger.error(f"Get positive pay file list failed: {e}")
        return {"error": f"Get positive pay file list failed: {e}"}

@mcp.tool()
def get_unbilled_benefit_adjustments(
    download_id: Optional[str] = None, 
    client_id: Optional[List[str]] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    include_term_client: Optional[str] = None, 
    status_class: Optional[str] = None
) -> Dict[str, Any]:
    """
    Unbilled Benefit Adjustments information
    
    Args:
        download_id: Identifier used to check status of / download data (optional)
        client_id: Use this option to limit the response to one or more client IDs (optional)
        start_date: Adjustment period filter start date (in YYYY-MM-DD format) (optional)
        end_date: Adjustment period filter end date (in YYYY-MM-DD format) (optional)
        include_term_client: Whether to include terminated clients in the response. Terminated clients are excluded by default (optional)
        status_class: Use this option to restrict the response based on employee status class. Allowed values are T (terminated), A (active), and L (on leave) (optional)
        
    Returns:
        Dictionary containing benefit adjustments that have not yet been billed with build status and download URL
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/getUnbilledBenefitAdjustments"
        params = {}
        
        if download_id:
            params["downloadId"] = download_id
        if client_id:
            params["clientId"] = client_id
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if include_term_client:
            params["includeTermClient"] = include_term_client
        if status_class:
            params["statusClass"] = status_class
        
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
        logger.error(f"Get unbilled benefit adjustments failed: {e}")
        return {"error": f"Get unbilled benefit adjustments failed: {e}"}

@mcp.tool()
def identify_ach_process_lock() -> Dict[str, Any]:
    """
    Identify ACH Process Lock
    
    Returns:
        Dictionary containing information about existing ACH process locks, specifically the associated user and the date and time of creation
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/identifyACHProcessLock"
        
        request = urllib.request.Request(
            url,
            headers={
                "sessionId": session_id,
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
        
    except Exception as e:
        logger.error(f"Identify ACH process lock failed: {e}")
        return {"error": f"Identify ACH process lock failed: {e}"}

@mcp.tool()
def positive_pay_download(
    download_id: Optional[str] = None, 
    checking_account: Optional[str] = None, 
    file_stub: Optional[str] = None, 
    start_check_date: Optional[str] = None, 
    end_check_date: Optional[str] = None, 
    include_voided_checks: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Download positive pay report
    
    Args:
        download_id: Identifier used to check status of / download data (optional)
        checking_account: To generate a positive pay file for only one bank account, enter a checking account ID (optional)
        file_stub: To generate a positive pay file for multiple bank accounts, enter the File Stub ID for the bank accounts you want to include in the file (optional)
        start_check_date: To report for a specific date range, enter the start check date (format: YYYY-MM-DD); an endCheckDate value is required in this case (optional)
        end_check_date: To report for a specific date range, enter the end check date (format: YYYY-MM-DD); a startCheckDate value is required in this case (optional)
        include_voided_checks: If true, includes voided check data in the file; if false (default), ignores voided check data (optional)
        
    Returns:
        Dictionary containing positive pay download file generation status and download URL
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/positivePayDownload"
        params = {}
        
        if download_id:
            params["downloadId"] = download_id
        if checking_account:
            params["checkingAccount"] = checking_account
        if file_stub:
            params["fileStub"] = file_stub
        if start_check_date:
            params["startCheckDate"] = start_check_date
        if end_check_date:
            params["endCheckDate"] = end_check_date
        if include_voided_checks is not None:
            params["includeVoidedChecks"] = str(include_voided_checks).lower()
        
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
        logger.error(f"Positive pay download failed: {e}")
        return {"error": f"Positive pay download failed: {e}"}

# Batch 49: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def recreate_positive_pay(
    download_id: Optional[str] = None, 
    file_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Recreate positive pay report
    
    Args:
        download_id: Identifier used to check status of / download data (optional)
        file_name: Name of the positive pay file to recreate (returned by getPositivePayFileList) (optional)
        
    Returns:
        Dictionary containing recreated positive pay file generation status and download URL
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/recreatePositivePay"
        params = {}
        
        if download_id:
            params["downloadId"] = download_id
        if file_name:
            params["fileName"] = file_name
        
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
        logger.error(f"Recreate positive pay failed: {e}")
        return {"error": f"Recreate positive pay failed: {e}"}

@mcp.tool()
def stream_ach_data(
    ach_batch_id: str, 
    ach_file_name: str
) -> Dict[str, Any]:
    """
    Stream ACH Data
    
    Args:
        ach_batch_id: ACH Batch Identifier
        ach_file_name: ACH File Name
        
    Returns:
        Dictionary containing securely streamed ACH file data
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/system/v1/streamACHData"
        params = {
            "achBatchId": ach_batch_id,
            "achFileName": ach_file_name
        }
        
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
        logger.error(f"Stream ACH data failed: {e}")
        return {"error": f"Stream ACH data failed: {e}"}

@mcp.tool()
def get_suta_information(
    client_id: str, 
    employee_id: str
) -> Dict[str, Any]:
    """
    Retrieve Employee SUTA Reporting Information
    
    Args:
        client_id: Client identifier
        employee_id: Employee identifier
        
    Returns:
        Dictionary containing employee's state unemployment tax (SUTA) reporting information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/taxRate/v1/getSutaInformation"
        params = {
            "clientId": client_id,
            "employeeId": employee_id
        }
        
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
        logger.error(f"Get SUTA information failed: {e}")
        return {"error": f"Get SUTA information failed: {e}"}

@mcp.tool()
def get_tax_authorities(
    state_code: Optional[str] = None, 
    authority_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get tax authorities
    
    Args:
        state_code: Two-character state code (optional)
        authority_id: Authority id (optional)
        
    Returns:
        Dictionary containing list of local tax authorities for the specified state
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/taxRate/v1/getTaxAuthorities"
        params = {}
        
        if state_code:
            params["stateCode"] = state_code
        if authority_id:
            params["authorityId"] = authority_id
        
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
        logger.error(f"Get tax authorities failed: {e}")
        return {"error": f"Get tax authorities failed: {e}"}

@mcp.tool()
def get_tax_rate(
    workers_comp_policy_id: str, 
    workers_comp_class: str, 
    employer_id: str, 
    effective_date: str, 
    client_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get tax rates
    
    Args:
        workers_comp_policy_id: Policy ID retrieved by getWorkersCompPolicyList
        workers_comp_class: Classification retrieved by getWorkersCompClasses
        employer_id: Employer identifier
        effective_date: The policy effective date (YYYY-MM-DD format)
        client_id: For future development. Client overrides are not currently supported. Leave blank (optional)
        
    Returns:
        Dictionary containing federal and state tax rates and limits including OASDI, FUTA, MediCare, and SUTA
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/taxRate/v1/getTaxRate"
        params = {
            "workersCompPolicyId": workers_comp_policy_id,
            "workersCompClass": workers_comp_class,
            "employerId": employer_id,
            "effectiveDate": effective_date
        }
        
        if client_id:
            params["clientId"] = client_id
        
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
        logger.error(f"Get tax rate failed: {e}")
        return {"error": f"Get tax rate failed: {e}"}

# Batch 50: Next 5 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_state_w4_params(
    state_code: str
) -> Dict[str, Any]:
    """
    Get W4 parameters for a given state
    
    Args:
        state_code: Two-character state code
        
    Returns:
        Dictionary containing Form W-4 parameters required in the specified state
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/taxRate/v1/getStateW4Params"
        params = {
            "stateCode": state_code
        }
        
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
        logger.error(f"Get state W4 params failed: {e}")
        return {"error": f"Get state W4 params failed: {e}"}

@mcp.tool()
def get_workers_comp_classes(
    state_code: str
) -> Dict[str, Any]:
    """
    Get workers' compensation classes
    
    Args:
        state_code: Two-character state code
        
    Returns:
        Dictionary containing list of workers' comp classification codes and descriptions for the specified state
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/taxRate/v1/getWorkersCompClasses"
        params = {
            "stateCode": state_code
        }
        
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
        logger.error(f"Get workers comp classes failed: {e}")
        return {"error": f"Get workers comp classes failed: {e}"}

@mcp.tool()
def get_workers_comp_policy_details(
    policy_id: str
) -> Dict[str, Any]:
    """
    Get workers' compensation policy with details
    
    Args:
        policy_id: Workers' compensation policy identifier
        
    Returns:
        Dictionary containing information about the specified workers' compensation policy
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/taxRate/v1/getWorkersCompPolicyDetails"
        params = {
            "policyId": policy_id
        }
        
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
        logger.error(f"Get workers comp policy details failed: {e}")
        return {"error": f"Get workers comp policy details failed: {e}"}

@mcp.tool()
def get_workers_comp_policy_list(
    effective_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get workers' compensation policy list
    
    Args:
        effective_date: Date when coverage begins under this policy (this is the beginning of the policy year) (optional)
        
    Returns:
        Dictionary containing list of all system-level workers' compensation policies with descriptive information
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/taxRate/v1/getWorkersCompPolicyList"
        params = {}
        
        if effective_date:
            params["effectiveDate"] = effective_date
        
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
        logger.error(f"Get workers comp policy list failed: {e}")
        return {"error": f"Get workers comp policy list failed: {e}"}

@mcp.tool()
def get_timesheet_batch_status(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Get the status of a payroll batch
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch number
        
    Returns:
        Dictionary containing current status of the specified payroll batch with checksum
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/timesheet/v1/getBatchStatus"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Get timesheet batch status failed: {e}")
        return {"error": f"Get timesheet batch status failed: {e}"}

# Batch 51: Final 3 endpoints from all_get_endpoints.txt

@mcp.tool()
def get_timesheet_param_data(
    client_id: str, 
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the list of available templates and batches
    
    Args:
        client_id: Client identifier
        user_id: User identifier used to match data submitted by Timesheet.upload with call to Timesheet.accept (optional)
        
    Returns:
        Dictionary containing list of templates and payroll batches available for web use
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/timesheet/v1/getParamData"
        params = {
            "clientId": client_id
        }
        
        if user_id:
            params["userId"] = user_id
        
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
        logger.error(f"Get timesheet param data failed: {e}")
        return {"error": f"Get timesheet param data failed: {e}"}

@mcp.tool()
def get_pay_import_definition(
    definition_id: str
) -> Dict[str, Any]:
    """
    Get pay import definition
    
    Args:
        definition_id: Template or pay import definition identifier
        
    Returns:
        Dictionary containing details of the pay import definition for a client
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/timesheet/v1/getPayImportDefinition"
        params = {
            "definitionId": definition_id
        }
        
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
        logger.error(f"Get pay import definition failed: {e}")
        return {"error": f"Get pay import definition failed: {e}"}

@mcp.tool()
def get_timesheet_data(
    client_id: str, 
    batch_id: str
) -> Dict[str, Any]:
    """
    Get the timesheet data for a payroll batch
    
    Args:
        client_id: Client identifier
        batch_id: Payroll batch number
        
    Returns:
        Dictionary containing timesheet data for employees in the payroll batch
    """
    try:
        username = os.getenv("PRISMHR_USERNAME")
        password = os.getenv("PRISMHR_PASSWORD") 
        peo_id = os.getenv("PRISMHR_PEO_ID")
        base_url = os.getenv("PRISMHR_BASE_URL", "https://salesdemoapi.prismhr.com/prismhr-api")
        
        if not all([username, password, peo_id]):
            return {"error": "Missing PrismHR credentials"}
        
        session_id = authenticate_prismhr(username, password, peo_id, base_url)
        if not session_id:
            return {"error": "Authentication failed"}
        
        url = f"{base_url}/services/rest/timesheet/v1/getTimeSheetData"
        params = {
            "clientId": client_id,
            "batchId": batch_id
        }
        
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
        logger.error(f"Get timesheet data failed: {e}")
        return {"error": f"Get timesheet data failed: {e}"}

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
