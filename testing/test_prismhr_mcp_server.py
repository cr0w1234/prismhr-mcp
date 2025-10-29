import asyncio
import os
from fastmcp import Client

from dotenv import load_dotenv

async def test_server():
    # Test the MCP server using streamable-http transport.
    # Use "/sse" endpoint if using sse transport.
    load_dotenv(override=True)
    
    # MCP_SERVER_URL = 'http://localhost:8080/mcp/'
    MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8080/mcp/')
    
    '''
    USE DICT JSON FORMAT FOR TOOL CALL INPUTS? (in mcp server file)
    # Call http_get tool
    print(">>> 🪛  Calling http_get tool for getting popular movies")
    result = await client.call_tool("http_get", {"url": "https://api.themoviedb.org/3/movie/popular?api_key=5b039ea0afb5076e4e73b46c912a6b77"})
    print(f"<<< ✅ Result: {result[0].text}")'''
    
    async with Client(MCP_SERVER_URL) as client:
        # List available tools
        tools = await client.list_tools()
        print(f"{len(tools)} tools found")
        for tool in tools:
            print(f">>> 🛠️  Tool found: {tool.name}")

        
        # Test get_employee_list tool
        print("\n>>> 🪛  Testing get_employee_list tool")
        try:
            # You'll need to replace '12345' with an actual client ID from your PrismHR demo account
            client_id = os.getenv('PRISMHR_CLIENT_ID', '132')  # Default for testing
            
            print(f"Calling get_employee_list with client_id: {client_id}")
            result = await client.call_tool("get_employee_list", {
                "client_id": client_id
            })
            
            print(f"<<< ✅ get_employee_list Result:")
            # print(result)
            print(f"Response: {result.content[0].text}")
            
        except Exception as e:
            print(f"<<< ❌ get_employee_list Error: {e}")
        
        # Test get_employee tool (if we have an employee ID)
        print("\n>>> 🪛  Testing get_employee tool")
        try:
            employee_id = os.getenv('PRISMHR_EMPLOYEE_ID', 'J00809')  # Default for testing
            
            print(f"Calling get_employee with client_id: {client_id}, employee_id: {employee_id}")
            result = await client.call_tool("get_employee", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            
            print(f"<<< ✅ get_employee Result:")
            print(f"Response: {result.content[0].text}")
            
        except Exception as e:
            print(f"<<< ❌ get_employee Error: {e}")
        
        # Test test_connection tool
        print("\n>>> 🪛  Testing test_connection tool")
        try:
            result = await client.call_tool("test_connection", {})
            print(f"<<< ✅ test_connection Result:")
            print(f"Response: {result.content[0].text}")
            
        except Exception as e:
            print(f"<<< ❌ test_connection Error: {e}")
        

        client_id = os.getenv('PRISMHR_CLIENT_ID', '132')
        
        print("\n" + "="*60)
        print("TESTING BATCH 1 - FIRST 5 ENDPOINTS")
        print("="*60)
        
        # Test 1: get_job_applicant_list
        print("\n>>> 🪛  Testing get_job_applicant_list")
        try:
            result = await client.call_tool("get_job_applicant_list", {
                "client_id": client_id,
                "count": "10"
            })
            print(f"<<< ✅ get_job_applicant_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_job_applicant_list Error: {e}")
        
        # Test 2: get_job_applicants
        print("\n>>> 🪛  Testing get_job_applicants")
        try:
            result = await client.call_tool("get_job_applicants", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_job_applicants Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_job_applicants Error: {e}")
        
        # Test 3: get_benefit_enrollment_status
        print("\n>>> 🪛  Testing get_benefit_enrollment_status")
        try:
            result = await client.call_tool("get_benefit_enrollment_status", {
                "client_id": client_id,
                "count": "10"
            })
            print(f"<<< ✅ get_benefit_enrollment_status Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_enrollment_status Error: {e}")
        
        # Test 4: get_401k_match_rules (requires additional parameters)
        print("\n>>> 🪛  Testing get_401k_match_rules")
        try:
            # Note: This requires benefit_group_id and retirement_plan_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_401k_match_rules", {
                "client_id": client_id,
                "benefit_group_id": "test_group",
                "retirement_plan_id": "test_plan"
            })
            print(f"<<< ✅ get_401k_match_rules Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_401k_match_rules Error: {e}")
        
        # Test 5: get_aca_offered_employees
        print("\n>>> 🪛  Testing get_aca_offered_employees")
        try:
            result = await client.call_tool("get_aca_offered_employees", {
                "client_id": client_id,
                "count": "10"
            })
            print(f"<<< ✅ get_aca_offered_employees Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_aca_offered_employees Error: {e}")
        
        # Test connection
        print("\n>>> 🪛  Testing test_connection")
        try:
            result = await client.call_tool("test_connection", {})
            print(f"<<< ✅ test_connection Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ test_connection Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 2 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 6: get_absence_journal
        print("\n>>> 🪛  Testing get_absence_journal")
        try:
            # Note: This requires journal_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_absence_journal", {
                "client_id": client_id,
                "journal_id": ["test_journal_id"]
            })
            print(f"<<< ✅ get_absence_journal Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_absence_journal Error: {e}")
        
        # Test 7: get_absence_journal_by_date
        print("\n>>> 🪛  Testing get_absence_journal_by_date")
        try:
            result = await client.call_tool("get_absence_journal_by_date", {
                "client_id": client_id,
                "journal_date_start": "2024-01-01",
                "journal_date_end": "2024-01-31",
                "count": "10"
            })
            print(f"<<< ✅ get_absence_journal_by_date Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_absence_journal_by_date Error: {e}")
        
        # Test 8: get_active_benefit_plans
        print("\n>>> 🪛  Testing get_active_benefit_plans")
        try:
            employee_id = os.getenv('PRISMHR_EMPLOYEE_ID', 'J00809')
            result = await client.call_tool("get_active_benefit_plans", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_active_benefit_plans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_active_benefit_plans Error: {e}")
        
        # Test 9: get_available_benefit_plans
        print("\n>>> 🪛  Testing get_available_benefit_plans")
        try:
            employee_id = os.getenv('PRISMHR_EMPLOYEE_ID', 'J00809')
            result = await client.call_tool("get_available_benefit_plans", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_available_benefit_plans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_available_benefit_plans Error: {e}")
        
        # Test 10: get_benefit_adjustments
        print("\n>>> 🪛  Testing get_benefit_adjustments")
        try:
            employee_id = os.getenv('PRISMHR_EMPLOYEE_ID', 'J00809')
            result = await client.call_tool("get_benefit_adjustments", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_benefit_adjustments Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_adjustments Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 3 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 11: get_benefit_confirmation_data
        print("\n>>> 🪛  Testing get_benefit_confirmation_data")
        try:
            # Note: This requires confirm_num which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_benefit_confirmation_data", {
                "client_id": client_id,
                "employee_id": employee_id,
                "confirm_num": "test_confirm_num"
            })
            print(f"<<< ✅ get_benefit_confirmation_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_confirmation_data Error: {e}")
        
        # Test 12: get_benefit_confirmation_list
        print("\n>>> 🪛  Testing get_benefit_confirmation_list")
        try:
            result = await client.call_tool("get_benefit_confirmation_list", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_benefit_confirmation_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_confirmation_list Error: {e}")
        
        # Test 13: get_benefit_plan_list
        print("\n>>> 🪛  Testing get_benefit_plan_list")
        try:
            result = await client.call_tool("get_benefit_plan_list", {})
            print(f"<<< ✅ get_benefit_plan_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_plan_list Error: {e}")
        
        # Test 14: get_benefit_plans
        print("\n>>> 🪛  Testing get_benefit_plans")
        try:
            result = await client.call_tool("get_benefit_plans", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_benefit_plans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_plans Error: {e}")
        
        # Test 15: get_benefit_rule
        print("\n>>> 🪛  Testing get_benefit_rule")
        try:
            result = await client.call_tool("get_benefit_rule", {
                "client_id": client_id,
                "effective_date": "2024-01-01"
            })
            print(f"<<< ✅ get_benefit_rule Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_rule Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 4 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 16: get_benefit_workflow_grid
        print("\n>>> 🪛  Testing get_benefit_workflow_grid")
        try:
            result = await client.call_tool("get_benefit_workflow_grid", {
                "client_id": client_id,
                "workflow_level": "B"
            })
            print(f"<<< ✅ get_benefit_workflow_grid Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_workflow_grid Error: {e}")
        
        # Test 17: get_benefits_enrollment_trace
        print("\n>>> 🪛  Testing get_benefits_enrollment_trace")
        try:
            result = await client.call_tool("get_benefits_enrollment_trace", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_benefits_enrollment_trace Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefits_enrollment_trace Error: {e}")
        
        # Test 18: get_client_benefit_plan_setup_details
        print("\n>>> 🪛  Testing get_client_benefit_plan_setup_details")
        try:
            # Note: This requires plan_id and plan_class which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_client_benefit_plan_setup_details", {
                "client_id": client_id,
                "plan_id": "test_plan_id",
                "plan_class": "G"
            })
            print(f"<<< ✅ get_client_benefit_plan_setup_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_benefit_plan_setup_details Error: {e}")
        
        # Test 19: get_client_benefit_plans
        print("\n>>> 🪛  Testing get_client_benefit_plans")
        try:
            result = await client.call_tool("get_client_benefit_plans", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_client_benefit_plans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_benefit_plans Error: {e}")
        
        # Test 20: get_cobra_codes
        print("\n>>> 🪛  Testing get_cobra_codes")
        try:
            result = await client.call_tool("get_cobra_codes", {})
            print(f"<<< ✅ get_cobra_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_cobra_codes Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 5 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 21: get_cobra_employee
        print("\n>>> 🪛  Testing get_cobra_employee")
        try:
            result = await client.call_tool("get_cobra_employee", {
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_cobra_employee Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_cobra_employee Error: {e}")
        
        # Test 22: get_dependents
        print("\n>>> 🪛  Testing get_dependents")
        try:
            result = await client.call_tool("get_dependents", {
                "client_id": client_id,
                "employee_id": employee_id,
                "only_active": "true"
            })
            print(f"<<< ✅ get_dependents Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_dependents Error: {e}")
        
        # Test 23: get_disability_plan_enrollment_details
        print("\n>>> 🪛  Testing get_disability_plan_enrollment_details")
        try:
            # Note: This requires group_benefit_plan_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_disability_plan_enrollment_details", {
                "group_benefit_plan_id": "test_plan_id",
                "effective_date": "2024-01-01"
            })
            print(f"<<< ✅ get_disability_plan_enrollment_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_disability_plan_enrollment_details Error: {e}")
        
        # Test 24: get_eligible_flex_spending_plans
        print("\n>>> 🪛  Testing get_eligible_flex_spending_plans")
        try:
            result = await client.call_tool("get_eligible_flex_spending_plans", {
                "client_id": client_id,
                "employee_id": employee_id,
                "as_of_date": "2024-01-01"
            })
            print(f"<<< ✅ get_eligible_flex_spending_plans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_eligible_flex_spending_plans Error: {e}")
        
        # Test 25: get_eligible_zip_codes
        print("\n>>> 🪛  Testing get_eligible_zip_codes")
        try:
            # Note: This requires plan_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_eligible_zip_codes", {
                "plan_id": "test_plan_id"
            })
            print(f"<<< ✅ get_eligible_zip_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_eligible_zip_codes Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 6 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 26: get_employee_premium
        print("\n>>> 🪛  Testing get_employee_premium")
        try:
            # Note: This requires plan_id and effective_date which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_employee_premium", {
                "client_id": client_id,
                "employee_id": employee_id,
                "effective_date": "2024-01-01",
                "plan_id": "test_plan_id",
                "options": "PremiumRates,ContributionRates"
            })
            print(f"<<< ✅ get_employee_premium Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_premium Error: {e}")
        
        # Test 27: get_employee_retirement_summary
        print("\n>>> 🪛  Testing get_employee_retirement_summary")
        try:
            # Note: This requires plan_id and plan_year which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_employee_retirement_summary", {
                "client_id": client_id,
                "employee_id": employee_id,
                "plan_id": "test_plan_id",
                "plan_year": "2024"
            })
            print(f"<<< ✅ get_employee_retirement_summary Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_retirement_summary Error: {e}")
        
        # Test 28: get_enroll_input_list
        print("\n>>> 🪛  Testing get_enroll_input_list")
        try:
            # Note: This requires plan_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_enroll_input_list", {
                "client_id": client_id,
                "employee_id": employee_id,
                "plan_id": "test_plan_id"
            })
            print(f"<<< ✅ get_enroll_input_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_enroll_input_list Error: {e}")
        
        # Test 29: get_enrollment_plan_details
        print("\n>>> 🪛  Testing get_enrollment_plan_details")
        try:
            # Note: This requires plan_id and offer_type which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_enrollment_plan_details", {
                "plan_id": "test_plan_id",
                "offer_type": "MED",
                "effective_date": "2024-01-01"
            })
            print(f"<<< ✅ get_enrollment_plan_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_enrollment_plan_details Error: {e}")
        
        # Test 30: get_fsa_reimbursements
        print("\n>>> 🪛  Testing get_fsa_reimbursements")
        try:
            result = await client.call_tool("get_fsa_reimbursements", {
                "client_id": client_id,
                "employee_id": employee_id,
                "plan_year": "2024",
                "account_type": "FSA"
            })
            print(f"<<< ✅ get_fsa_reimbursements Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_fsa_reimbursements Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 7 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 31: get_flex_plans
        print("\n>>> 🪛  Testing get_flex_plans")
        try:
            result = await client.call_tool("get_flex_plans", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_flex_plans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_flex_plans Error: {e}")
        
        # Test 32: get_group_benefit_plan
        print("\n>>> 🪛  Testing get_group_benefit_plan")
        try:
            # Note: This requires plan_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_group_benefit_plan", {
                "plan_id": "test_plan_id"
            })
            print(f"<<< ✅ get_group_benefit_plan Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_group_benefit_plan Error: {e}")
        
        # Test 33: get_group_benefit_rates
        print("\n>>> 🪛  Testing get_group_benefit_rates")
        try:
            # Note: This requires plan_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_group_benefit_rates", {
                "plan_id": "test_plan_id",
                "date": "2024-01-01",
                "options": "BILLING,PREMIUM"
            })
            print(f"<<< ✅ get_group_benefit_rates Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_group_benefit_rates Error: {e}")
        
        # Test 34: get_group_benefit_types
        print("\n>>> 🪛  Testing get_group_benefit_types")
        try:
            result = await client.call_tool("get_group_benefit_types", {
                "type_code": "MED"
            })
            print(f"<<< ✅ get_group_benefit_types Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_group_benefit_types Error: {e}")
        
        # Test 35: get_life_event_code_details
        print("\n>>> 🪛  Testing get_life_event_code_details")
        try:
            result = await client.call_tool("get_life_event_code_details", {
                "client_id": client_id,
                "life_event_code": "MARRIAGE"
            })
            print(f"<<< ✅ get_life_event_code_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_life_event_code_details Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 8 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 36: get_monthly_aca_info
        print("\n>>> 🪛  Testing get_monthly_aca_info")
        try:
            result = await client.call_tool("get_monthly_aca_info", {
                "client_id": client_id,
                "employee_id": [employee_id]
            })
            print(f"<<< ✅ get_monthly_aca_info Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_monthly_aca_info Error: {e}")
        
        # Test 37: get_pto_requests_list
        print("\n>>> 🪛  Testing get_pto_requests_list")
        try:
            result = await client.call_tool("get_pto_requests_list", {
                "client_id": client_id,
                "employee_id": [employee_id],
                "statuses": "N,A",
                "pto_starts_after_date": "2024-01-01"
            })
            print(f"<<< ✅ get_pto_requests_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pto_requests_list Error: {e}")
        
        # Test 38: get_paid_time_off
        print("\n>>> 🪛  Testing get_paid_time_off")
        try:
            result = await client.call_tool("get_paid_time_off", {
                "client_id": client_id,
                "employee_id": employee_id
            })
            print(f"<<< ✅ get_paid_time_off Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_paid_time_off Error: {e}")
        
        # Test 39: get_paid_time_off_plans
        print("\n>>> 🪛  Testing get_paid_time_off_plans")
        try:
            result = await client.call_tool("get_paid_time_off_plans", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_paid_time_off_plans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_paid_time_off_plans Error: {e}")
        
        # Test 40: get_plan_year_info
        print("\n>>> 🪛  Testing get_plan_year_info")
        try:
            result = await client.call_tool("get_plan_year_info", {
                "plan_type": "F",
                "plan_year": "2024"
            })
            print(f"<<< ✅ get_plan_year_info Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_plan_year_info Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 9 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 41: get_pto_absence_codes
        print("\n>>> 🪛  Testing get_pto_absence_codes")
        try:
            result = await client.call_tool("get_pto_absence_codes", {
                "client_id": client_id,
                "absence_code": "VAC"
            })
            print(f"<<< ✅ get_pto_absence_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pto_absence_codes Error: {e}")
        
        # Test 42: get_pto_auto_enroll_rules
        print("\n>>> 🪛  Testing get_pto_auto_enroll_rules")
        try:
            result = await client.call_tool("get_pto_auto_enroll_rules", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_pto_auto_enroll_rules Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pto_auto_enroll_rules Error: {e}")
        
        # Test 43: get_pto_classes
        print("\n>>> 🪛  Testing get_pto_classes")
        try:
            result = await client.call_tool("get_pto_classes", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_pto_classes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pto_classes Error: {e}")
        
        # Test 44: get_pto_plan_details
        print("\n>>> 🪛  Testing get_pto_plan_details")
        try:
            # Note: This requires pto_plan_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_pto_plan_details", {
                "client_id": client_id,
                "pto_plan_id": "test_pto_plan_id"
            })
            print(f"<<< ✅ get_pto_plan_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pto_plan_details Error: {e}")
        
        # Test 45: get_pto_register_types
        print("\n>>> 🪛  Testing get_pto_register_types")
        try:
            result = await client.call_tool("get_pto_register_types", {
                "client_id": client_id,
                "pto_type_code": "VAC"
            })
            print(f"<<< ✅ get_pto_register_types Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pto_register_types Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 10 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 46: get_retirement_loans
        print("\n>>> 🪛  Testing get_retirement_loans")
        try:
            result = await client.call_tool("get_retirement_loans", {
                "client_id": client_id,
                "employee_id": "J00809"
            })
            print(f"<<< ✅ get_retirement_loans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_retirement_loans Error: {e}")
        
        # Test 47: get_retirement_plan
        print("\n>>> 🪛  Testing get_retirement_plan")
        try:
            result = await client.call_tool("get_retirement_plan", {
                "client_id": client_id,
                "employee_id": "J00809",
                "effective_date": "2024-01-01",
                "is_active": True
            })
            print(f"<<< ✅ get_retirement_plan Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_retirement_plan Error: {e}")
        
        # Test 48: get_section125_plans
        print("\n>>> 🪛  Testing get_section125_plans")
        try:
            result = await client.call_tool("get_section125_plans", {
                "plan_type": "H",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_section125_plans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_section125_plans Error: {e}")
        
        # Test 49: get_retirement_census_export
        print("\n>>> 🪛  Testing get_retirement_census_export")
        try:
            # Note: This is a complex export operation that may require specific plan IDs
            result = await client.call_tool("get_retirement_census_export", {
                "report_format": "Census",
                "plan_id": "ALL",
                "client_id": client_id
            })
            print(f"<<< ✅ get_retirement_census_export Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_retirement_census_export Error: {e}")
        
        # Test 50: get_aca_large_employer
        print("\n>>> 🪛  Testing get_aca_large_employer")
        try:
            result = await client.call_tool("get_aca_large_employer", {
                "client_id": client_id,
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_aca_large_employer Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_aca_large_employer Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 11 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 51: get_active_employee_count_by_entity
        print("\n>>> 🪛  Testing get_active_employee_count_by_entity")
        try:
            result = await client.call_tool("get_active_employee_count_by_entity", {
                "client_id": client_id,
                "entity_type": "department",
                "include_obsolete": False
            })
            print(f"<<< ✅ get_active_employee_count_by_entity Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_active_employee_count_by_entity Error: {e}")
        
        # Test 52: get_all_prism_client_contacts
        print("\n>>> 🪛  Testing get_all_prism_client_contacts")
        try:
            result = await client.call_tool("get_all_prism_client_contacts", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_all_prism_client_contacts Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_all_prism_client_contacts Error: {e}")
        
        # Test 53: get_backup_assignments
        print("\n>>> 🪛  Testing get_backup_assignments")
        try:
            result = await client.call_tool("get_backup_assignments", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_backup_assignments Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_backup_assignments Error: {e}")
        
        # Test 54: get_benefit_group
        print("\n>>> 🪛  Testing get_benefit_group")
        try:
            # Note: This requires group_id which we don't have
            # We'll test with placeholder values to see the error response
            result = await client.call_tool("get_benefit_group", {
                "client_id": client_id,
                "group_id": ["test_group_id"]
            })
            print(f"<<< ✅ get_benefit_group Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_benefit_group Error: {e}")
        
        # Test 55: get_bill_pending
        print("\n>>> 🪛  Testing get_bill_pending")
        try:
            result = await client.call_tool("get_bill_pending", {
                "client_id": client_id,
                "status": "Pending",
                "start_bill_date": "2024-01-01",
                "end_bill_date": "2024-12-31"
            })
            print(f"<<< ✅ get_bill_pending Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_bill_pending Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 12 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 56: get_bundled_billing_rule
        print("\n>>> 🪛  Testing get_bundled_billing_rule")
        try:
            result = await client.call_tool("get_bundled_billing_rule", {
                "client_id": client_id,
                "wc_code": "001",
                "state": "CA"
            })
            print(f"<<< ✅ get_bundled_billing_rule Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_bundled_billing_rule Error: {e}")
        
        # Test 57: get_client_billing_bank_account
        print("\n>>> 🪛  Testing get_client_billing_bank_account")
        try:
            result = await client.call_tool("get_client_billing_bank_account", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_client_billing_bank_account Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_billing_bank_account Error: {e}")
        
        # Test 58: get_client_codes
        print("\n>>> 🪛  Testing get_client_codes")
        try:
            result = await client.call_tool("get_client_codes", {
                "client_id": client_id,
                "options": "BenefitGroup,Department,Pay",
                "exclude_obsolete": True
            })
            print(f"<<< ✅ get_client_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_codes Error: {e}")
        
        # Test 59: get_client_events
        print("\n>>> 🪛  Testing get_client_events")
        try:
            result = await client.call_tool("get_client_events", {
                "client_id": client_id,
                "from_date": "2024-01-01",
                "thru_date": "2024-12-31"
            })
            print(f"<<< ✅ get_client_events Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_events Error: {e}")
        
        # Test 60: get_client_list
        print("\n>>> 🪛  Testing get_client_list")
        try:
            result = await client.call_tool("get_client_list", {
                "in_active": False
            })
            print(f"<<< ✅ get_client_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_list Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 13 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 61: get_client_location_details
        print("\n>>> 🪛  Testing get_client_location_details")
        try:
            result = await client.call_tool("get_client_location_details", {
                "client_id": client_id,
                "location_id": "LOC001"
            })
            print(f"<<< ✅ get_client_location_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_location_details Error: {e}")
        
        # Test 62: get_client_master
        print("\n>>> 🪛  Testing get_client_master")
        try:
            result = await client.call_tool("get_client_master", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_client_master Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_master Error: {e}")
        
        # Test 63: get_client_ownership
        print("\n>>> 🪛  Testing get_client_ownership")
        try:
            result = await client.call_tool("get_client_ownership", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_client_ownership Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_ownership Error: {e}")
        
        # Test 64: get_doc_expirations
        print("\n>>> 🪛  Testing get_doc_expirations")
        try:
            result = await client.call_tool("get_doc_expirations", {
                "client_id": client_id,
                "doc_types": "I9",
                "days_out": "30",
                "employee_id": "J00809"
            })
            print(f"<<< ✅ get_doc_expirations Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_doc_expirations Error: {e}")
        
        # Test 65: get_employee_list_by_entity
        print("\n>>> 🪛  Testing get_employee_list_by_entity")
        try:
            result = await client.call_tool("get_employee_list_by_entity", {
                "client_id": client_id,
                "entity_type": "location",
                "entity_id": "LOC001",
                "status_class": "A"
            })
            print(f"<<< ✅ get_employee_list_by_entity Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_list_by_entity Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 14 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 66: get_employees_in_pay_group
        print("\n>>> 🪛  Testing get_employees_in_pay_group")
        try:
            result = await client.call_tool("get_employees_in_pay_group", {
                "client_id": client_id,
                "pay_group": "PG001"
            })
            print(f"<<< ✅ get_employees_in_pay_group Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employees_in_pay_group Error: {e}")
        
        # Test 67: get_gl_cutback_check_post
        print("\n>>> 🪛  Testing get_gl_cutback_check_post")
        try:
            result = await client.call_tool("get_gl_cutback_check_post", {
                "gl_company": "GL001",
                "tran_date": "12/15/24"
            })
            print(f"<<< ✅ get_gl_cutback_check_post Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_gl_cutback_check_post Error: {e}")
        
        # Test 68: get_gl_data
        print("\n>>> 🪛  Testing get_gl_data")
        try:
            result = await client.call_tool("get_gl_data", {
                "type": "Journal"
            })
            print(f"<<< ✅ get_gl_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_gl_data Error: {e}")
        
        # Test 69: get_gl_invoice_post
        print("\n>>> 🪛  Testing get_gl_invoice_post")
        try:
            result = await client.call_tool("get_gl_invoice_post", {
                "gl_company": "GL001",
                "inv_date": "12/15/24"
            })
            print(f"<<< ✅ get_gl_invoice_post Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_gl_invoice_post Error: {e}")
        
        # Test 70: get_gl_journal_post
        print("\n>>> 🪛  Testing get_gl_journal_post")
        try:
            result = await client.call_tool("get_gl_journal_post", {
                "gl_company": "GL001",
                "tran_date": "12/15/24"
            })
            print(f"<<< ✅ get_gl_journal_post Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_gl_journal_post Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 15 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 71: get_geo_locations
        print("\n>>> 🪛  Testing get_geo_locations")
        try:
            result = await client.call_tool("get_geo_locations", {
                "zip_code": "10001"
            })
            print(f"<<< ✅ get_geo_locations Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_geo_locations Error: {e}")
        
        # Test 72: get_labor_allocations
        print("\n>>> 🪛  Testing get_labor_allocations")
        try:
            result = await client.call_tool("get_labor_allocations", {
                "client_id": client_id,
                "template_id": "TEMPLATE001"
            })
            print(f"<<< ✅ get_labor_allocations Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_labor_allocations Error: {e}")
        
        # Test 73: get_labor_union_details
        print("\n>>> 🪛  Testing get_labor_union_details")
        try:
            result = await client.call_tool("get_labor_union_details", {
                "client_id": client_id,
                "union_code": "UNION001"
            })
            print(f"<<< ✅ get_labor_union_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_labor_union_details Error: {e}")
        
        # Test 74: get_message_list
        print("\n>>> 🪛  Testing get_message_list")
        try:
            result = await client.call_tool("get_message_list", {
                "user_id": "USER001",
                "from_date": "2024-01-01",
                "to_date": "2024-12-31",
                "un_read_only": True
            })
            print(f"<<< ✅ get_message_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_message_list Error: {e}")
        
        # Test 75: get_messages
        print("\n>>> 🪛  Testing get_messages")
        try:
            result = await client.call_tool("get_messages", {
                "user_id": "USER001",
                "message_id": ["MSG001", "MSG002"]
            })
            print(f"<<< ✅ get_messages Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_messages Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 16 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 76: get_osha_300a_stats
        print("\n>>> 🪛  Testing get_osha_300a_stats")
        try:
            result = await client.call_tool("get_osha_300a_stats", {
                "client_id": client_id,
                "report_year": "2024",
                "location_code": "LOC001"
            })
            print(f"<<< ✅ get_osha_300a_stats Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_osha_300a_stats Error: {e}")
        
        # Test 77: get_pay_day_rules
        print("\n>>> 🪛  Testing get_pay_day_rules")
        try:
            result = await client.call_tool("get_pay_day_rules", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_pay_day_rules Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pay_day_rules Error: {e}")
        
        # Test 78: get_pay_group_details
        print("\n>>> 🪛  Testing get_pay_group_details")
        try:
            result = await client.call_tool("get_pay_group_details", {
                "client_id": client_id,
                "pay_group_code": "PG001"
            })
            print(f"<<< ✅ get_pay_group_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pay_group_details Error: {e}")
        
        # Test 79: get_payroll_schedule
        print("\n>>> 🪛  Testing get_payroll_schedule")
        try:
            result = await client.call_tool("get_payroll_schedule", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_payroll_schedule Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_schedule Error: {e}")
        
        # Test 80: get_prism_client_contact
        print("\n>>> 🪛  Testing get_prism_client_contact")
        try:
            result = await client.call_tool("get_prism_client_contact", {
                "client_id": client_id,
                "contact_id": "CONTACT001"
            })
            print(f"<<< ✅ get_prism_client_contact Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_prism_client_contact Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 17 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 81: get_retirement_plan_list
        print("\n>>> 🪛  Testing get_retirement_plan_list")
        try:
            result = await client.call_tool("get_retirement_plan_list", {
                "client_id": client_id,
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_retirement_plan_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_retirement_plan_list Error: {e}")
        
        # Test 82: get_suta_billing_rates
        print("\n>>> 🪛  Testing get_suta_billing_rates")
        try:
            result = await client.call_tool("get_suta_billing_rates", {
                "client_id": client_id,
                "state_code": "CA",
                "effective_date": "2024-01-01",
                "location_code": "LOC001"
            })
            print(f"<<< ✅ get_suta_billing_rates Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_suta_billing_rates Error: {e}")
        
        # Test 83: get_suta_rates
        print("\n>>> 🪛  Testing get_suta_rates")
        try:
            result = await client.call_tool("get_suta_rates", {
                "state": "CA",
                "client_id": client_id,
                "effective_date": "2024-01-01",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_suta_rates Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_suta_rates Error: {e}")
        
        # Test 84: get_unbundled_billing_rules
        print("\n>>> 🪛  Testing get_unbundled_billing_rules")
        try:
            result = await client.call_tool("get_unbundled_billing_rules", {
                "client_id": client_id,
                "rule_id": "RULE001",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_unbundled_billing_rules Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_unbundled_billing_rules Error: {e}")
        
        # Test 85: get_wc_accrual_modifiers
        print("\n>>> 🪛  Testing get_wc_accrual_modifiers")
        try:
            result = await client.call_tool("get_wc_accrual_modifiers", {
                "client_id": client_id,
                "state_code": "CA",
                "effective_date": "2024-01-01"
            })
            print(f"<<< ✅ get_wc_accrual_modifiers Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_wc_accrual_modifiers Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 18 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 86: get_wc_billing_modifiers
        print("\n>>> 🪛  Testing get_wc_billing_modifiers")
        try:
            result = await client.call_tool("get_wc_billing_modifiers", {
                "client_id": client_id,
                "state_code": "CA",
                "location_code": "LOC001",
                "existing_effective_date": "2024-01-01"
            })
            print(f"<<< ✅ get_wc_billing_modifiers Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_wc_billing_modifiers Error: {e}")
        
        # Test 87: get_client_location_details_v2
        print("\n>>> 🪛  Testing get_client_location_details_v2")
        try:
            result = await client.call_tool("get_client_location_details_v2", {
                "client_id": client_id,
                "location_id": "LOC001"
            })
            print(f"<<< ✅ get_client_location_details_v2 Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_location_details_v2 Error: {e}")
        
        # Test 88: get_suta_billing_rates_v2
        print("\n>>> 🪛  Testing get_suta_billing_rates_v2")
        try:
            result = await client.call_tool("get_suta_billing_rates_v2", {
                "client_id": client_id,
                "state_code": "CA",
                "location_code": "ALL",
                "effective_date": "2024-01-01",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_suta_billing_rates_v2 Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_suta_billing_rates_v2 Error: {e}")
        
        # Test 89: get_billing_code
        print("\n>>> 🪛  Testing get_billing_code")
        try:
            result = await client.call_tool("get_billing_code", {
                "billing_code": "BILL001",
                "only_active": "true",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_billing_code Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_billing_code Error: {e}")
        
        # Test 90: get_client_category_list
        print("\n>>> 🪛  Testing get_client_category_list")
        try:
            result = await client.call_tool("get_client_category_list", {
                "client_category_id": "CAT001",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_client_category_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_category_list Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 19 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 91: get_contact_type_list
        print("\n>>> 🪛  Testing get_contact_type_list")
        try:
            result = await client.call_tool("get_contact_type_list", {})
            print(f"<<< ✅ get_contact_type_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_contact_type_list Error: {e}")
        
        # Test 92: get_course_codes_list
        print("\n>>> 🪛  Testing get_course_codes_list")
        try:
            result = await client.call_tool("get_course_codes_list", {
                "client_id": client_id,
                "course_code_id": "COURSE001"
            })
            print(f"<<< ✅ get_course_codes_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_course_codes_list Error: {e}")
        
        # Test 93: get_deduction_code_details
        print("\n>>> 🪛  Testing get_deduction_code_details")
        try:
            result = await client.call_tool("get_deduction_code_details", {
                "deduction_code": "DED001"
            })
            print(f"<<< ✅ get_deduction_code_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_deduction_code_details Error: {e}")
        
        # Test 94: get_department_code
        print("\n>>> 🪛  Testing get_department_code")
        try:
            result = await client.call_tool("get_department_code", {
                "client_id": client_id,
                "department_code": "DEPT001"
            })
            print(f"<<< ✅ get_department_code Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_department_code Error: {e}")
        
        # Test 95: get_division_code
        print("\n>>> 🪛  Testing get_division_code")
        try:
            result = await client.call_tool("get_division_code", {
                "client_id": client_id,
                "division_code": "DIV001"
            })
            print(f"<<< ✅ get_division_code Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_division_code Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 20 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 96: get_eeo_codes
        print("\n>>> 🪛  Testing get_eeo_codes")
        try:
            result = await client.call_tool("get_eeo_codes", {
                "eeo_code_type": "Class",
                "eeo_code": "EEO001"
            })
            print(f"<<< ✅ get_eeo_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_eeo_codes Error: {e}")
        
        # Test 97: get_event_codes
        print("\n>>> 🪛  Testing get_event_codes")
        try:
            result = await client.call_tool("get_event_codes", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_event_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_event_codes Error: {e}")
        
        # Test 98: get_holiday_code_list
        print("\n>>> 🪛  Testing get_holiday_code_list")
        try:
            result = await client.call_tool("get_holiday_code_list", {
                "year": "2024"
            })
            print(f"<<< ✅ get_holiday_code_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_holiday_code_list Error: {e}")
        
        # Test 99: get_naics_code_list
        print("\n>>> 🪛  Testing get_naics_code_list")
        try:
            result = await client.call_tool("get_naics_code_list", {
                "naics_code": "311221",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_naics_code_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_naics_code_list Error: {e}")
        
        # Test 100: get_pay_grades
        print("\n>>> 🪛  Testing get_pay_grades")
        try:
            result = await client.call_tool("get_pay_grades", {
                "client_id": client_id,
                "pay_grade_code": "PG001"
            })
            print(f"<<< ✅ get_pay_grades Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pay_grades Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 21 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 101: get_paycode_details
        print("\n>>> 🪛  Testing get_paycode_details")
        try:
            result = await client.call_tool("get_paycode_details", {
                "paycode_id": "PC001"
            })
            print(f"<<< ✅ get_paycode_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_paycode_details Error: {e}")
        
        # Test 102: get_position_classifications
        print("\n>>> 🪛  Testing get_position_classifications")
        try:
            result = await client.call_tool("get_position_classifications", {
                "position_class": "MANAGER"
            })
            print(f"<<< ✅ get_position_classifications Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_position_classifications Error: {e}")
        
        # Test 103: get_position_code
        print("\n>>> 🪛  Testing get_position_code")
        try:
            result = await client.call_tool("get_position_code", {
                "client_id": client_id,
                "position_code": "POS001"
            })
            print(f"<<< ✅ get_position_code Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_position_code Error: {e}")
        
        # Test 104: get_project_code
        print("\n>>> 🪛  Testing get_project_code")
        try:
            result = await client.call_tool("get_project_code", {
                "client_id": client_id,
                "project_code": "PROJ001"
            })
            print(f"<<< ✅ get_project_code Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_project_code Error: {e}")
        
        # Test 105: get_project_phase
        print("\n>>> 🪛  Testing get_project_phase")
        try:
            result = await client.call_tool("get_project_phase", {
                "client_id": client_id,
                "class_code": "CLASS001",
                "project_phase_code": "PHASE001"
            })
            print(f"<<< ✅ get_project_phase Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_project_phase Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 22 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 106: get_rating_code
        print("\n>>> 🪛  Testing get_rating_code")
        try:
            result = await client.call_tool("get_rating_code", {
                "client_id": client_id,
                "rating_code_id": "RATE001"
            })
            print(f"<<< ✅ get_rating_code Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_rating_code Error: {e}")
        
        # Test 107: get_shift_code
        print("\n>>> 🪛  Testing get_shift_code")
        try:
            result = await client.call_tool("get_shift_code", {
                "client_id": client_id,
                "shift_code": "SHIFT001"
            })
            print(f"<<< ✅ get_shift_code Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_shift_code Error: {e}")
        
        # Test 108: get_skill_code
        print("\n>>> 🪛  Testing get_skill_code")
        try:
            result = await client.call_tool("get_skill_code", {
                "client_id": client_id,
                "skill_code": "SKILL001"
            })
            print(f"<<< ✅ get_skill_code Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_skill_code Error: {e}")
        
        # Test 109: get_user_defined_fields
        print("\n>>> 🪛  Testing get_user_defined_fields")
        try:
            result = await client.call_tool("get_user_defined_fields", {
                "client_id": client_id,
                "field_type": "EmployeeDetails",
                "type_id": ["TYPE001", "TYPE002"]
            })
            print(f"<<< ✅ get_user_defined_fields Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_user_defined_fields Error: {e}")
        
        # Test 110: get_deduction_arrears
        print("\n>>> 🪛  Testing get_deduction_arrears")
        try:
            result = await client.call_tool("get_deduction_arrears", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "options": ""
            })
            print(f"<<< ✅ get_deduction_arrears Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_deduction_arrears Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 23 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 111: get_deductions
        print("\n>>> 🪛  Testing get_deductions")
        try:
            result = await client.call_tool("get_deductions", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "options": ""
            })
            print(f"<<< ✅ get_deductions Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_deductions Error: {e}")
        
        # Test 112: get_employee_loans
        print("\n>>> 🪛  Testing get_employee_loans")
        try:
            result = await client.call_tool("get_employee_loans", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "loan_id": "LOAN001"
            })
            print(f"<<< ✅ get_employee_loans Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_loans Error: {e}")
        
        # Test 113: get_garnishment_details
        print("\n>>> 🪛  Testing get_garnishment_details")
        try:
            result = await client.call_tool("get_garnishment_details", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "docket_number": "DOCKET001",
                "garnishment_type": "C"
            })
            print(f"<<< ✅ get_garnishment_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_garnishment_details Error: {e}")
        
        # Test 114: get_garnishment_payment_history
        print("\n>>> 🪛  Testing get_garnishment_payment_history")
        try:
            result = await client.call_tool("get_garnishment_payment_history", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "docket_number": "DOCKET001"
            })
            print(f"<<< ✅ get_garnishment_payment_history Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_garnishment_payment_history Error: {e}")
        
        # Test 115: get_voluntary_recurring_deductions
        print("\n>>> 🪛  Testing get_voluntary_recurring_deductions")
        try:
            result = await client.call_tool("get_voluntary_recurring_deductions", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_voluntary_recurring_deductions Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_voluntary_recurring_deductions Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 24 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 116: get_document_types
        print("\n>>> 🪛  Testing get_document_types")
        try:
            result = await client.call_tool("get_document_types", {
                "document_type_id": ["DOC001", "DOC002"]
            })
            print(f"<<< ✅ get_document_types Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_document_types Error: {e}")
        
        # Test 117: get_ruleset
        print("\n>>> 🪛  Testing get_ruleset")
        try:
            result = await client.call_tool("get_ruleset", {
                "user_id": "testuser",
                "client_id": client_id,
                "user_type": "I",
                "context": "default"
            })
            print(f"<<< ✅ get_ruleset Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_ruleset Error: {e}")
        
        # Test 118: check_for_garnishments
        print("\n>>> 🪛  Testing check_for_garnishments")
        try:
            result = await client.call_tool("check_for_garnishments", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ check_for_garnishments Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ check_for_garnishments Error: {e}")
        
        # Test 119: download_1095c
        print("\n>>> 🪛  Testing download_1095c")
        try:
            result = await client.call_tool("download_1095c", {
                "client_id": client_id,
                "employee_id": ["EMP001"],
                "year": "2024"
            })
            print(f"<<< ✅ download_1095c Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ download_1095c Error: {e}")
        
        # Test 120: download_w2
        print("\n>>> 🪛  Testing download_w2")
        try:
            result = await client.call_tool("download_w2", {
                "client_id": client_id,
                "employee_id": ["EMP001"],
                "year": "2024"
            })
            print(f"<<< ✅ download_w2 Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ download_w2 Error: {e}")

        print("\n" + "="*60)
        print("TESTING BATCH 25 - NEXT 4 ENDPOINTS (skipping getEmployee as it already exists)")
        print("="*60)
        
        # Test 121: get_1095c_years
        print("\n>>> 🪛  Testing get_1095c_years")
        try:
            result = await client.call_tool("get_1095c_years", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_1095c_years Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_1095c_years Error: {e}")
        
        # Test 122: get_1099_years
        print("\n>>> 🪛  Testing get_1099_years")
        try:
            result = await client.call_tool("get_1099_years", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_1099_years Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_1099_years Error: {e}")
        
        # Test 123: get_ach_deductions
        print("\n>>> 🪛  Testing get_ach_deductions")
        try:
            result = await client.call_tool("get_ach_deductions", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_ach_deductions Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_ach_deductions Error: {e}")
        
        # Test 124: get_address_info
        print("\n>>> 🪛  Testing get_address_info")
        try:
            result = await client.call_tool("get_address_info", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_address_info Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_address_info Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 26 - NEXT 4 ENDPOINTS (skipping getEmployeeList as it already exists)")
        print("="*60)
        
        # Test 126: get_employee_events
        print("\n>>> 🪛  Testing get_employee_events")
        try:
            result = await client.call_tool("get_employee_events", {
                "employee_id": "EMP001",
                "client_id": client_id
            })
            print(f"<<< ✅ get_employee_events Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_events Error: {e}")
        
        # Test 128: get_employee_ssn_list
        print("\n>>> 🪛  Testing get_employee_ssn_list")
        try:
            result = await client.call_tool("get_employee_ssn_list", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_employee_ssn_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_ssn_list Error: {e}")
        
        # Test 129: get_employees_ready_for_everify
        print("\n>>> 🪛  Testing get_employees_ready_for_everify")
        try:
            result = await client.call_tool("get_employees_ready_for_everify", {})
            print(f"<<< ✅ get_employees_ready_for_everify Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employees_ready_for_everify Error: {e}")
        
        # Test 130: get_employers_info
        print("\n>>> 🪛  Testing get_employers_info")
        try:
            result = await client.call_tool("get_employers_info", {
                "employee_id": "EMP001",
                "client_id": client_id
            })
            print(f"<<< ✅ get_employers_info Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employers_info Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 27 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 131: get_everify_status
        print("\n>>> 🪛  Testing get_everify_status")
        try:
            result = await client.call_tool("get_everify_status", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_everify_status Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_everify_status Error: {e}")
        
        # Test 132: get_future_ee_change
        print("\n>>> 🪛  Testing get_future_ee_change")
        try:
            result = await client.call_tool("get_future_ee_change", {
                "event_object_id": "EVT001"
            })
            print(f"<<< ✅ get_future_ee_change Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_future_ee_change Error: {e}")
        
        # Test 133: get_garnishment_employee
        print("\n>>> 🪛  Testing get_garnishment_employee")
        try:
            result = await client.call_tool("get_garnishment_employee", {
                "client_id": client_id,
                "garnishment_id": "GARN001"
            })
            print(f"<<< ✅ get_garnishment_employee Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_garnishment_employee Error: {e}")
        
        # Test 134: get_history
        print("\n>>> 🪛  Testing get_history")
        try:
            result = await client.call_tool("get_history", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "type": ["P", "S", "J"]
            })
            print(f"<<< ✅ get_history Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_history Error: {e}")
        
        # Test 135: get_i9_data
        print("\n>>> 🪛  Testing get_i9_data")
        try:
            result = await client.call_tool("get_i9_data", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "options": "AdditionalMetadata"
            })
            print(f"<<< ✅ get_i9_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_i9_data Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 28 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 136: get_leave_requests
        print("\n>>> 🪛  Testing get_leave_requests")
        try:
            result = await client.call_tool("get_leave_requests", {
                "client_id": client_id,
                "leave_id": "LEAVE001"
            })
            print(f"<<< ✅ get_leave_requests Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_leave_requests Error: {e}")
        
        # Test 137: get_life_event
        print("\n>>> 🪛  Testing get_life_event")
        try:
            result = await client.call_tool("get_life_event", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_life_event Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_life_event Error: {e}")
        
        # Test 138: get_osha
        print("\n>>> 🪛  Testing get_osha")
        try:
            result = await client.call_tool("get_osha", {
                "client_id": client_id,
                "case_number": "OSHA001"
            })
            print(f"<<< ✅ get_osha Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_osha Error: {e}")
        
        # Test 139: get_pay_card_employees
        print("\n>>> 🪛  Testing get_pay_card_employees")
        try:
            result = await client.call_tool("get_pay_card_employees", {
                "client_id": client_id,
                "transit_number": "123456789"
            })
            print(f"<<< ✅ get_pay_card_employees Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pay_card_employees Error: {e}")
        
        # Test 140: get_pay_rate_history
        print("\n>>> 🪛  Testing get_pay_rate_history")
        try:
            result = await client.call_tool("get_pay_rate_history", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_pay_rate_history Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pay_rate_history Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 29 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 141: get_pending_approval
        print("\n>>> 🪛  Testing get_pending_approval")
        try:
            result = await client.call_tool("get_pending_approval", {
                "client_id": client_id,
                "type": "A",
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_pending_approval Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pending_approval Error: {e}")
        
        # Test 142: get_position_rate
        print("\n>>> 🪛  Testing get_position_rate")
        try:
            result = await client.call_tool("get_position_rate", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_position_rate Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_position_rate Error: {e}")
        
        # Test 143: get_scheduled_deductions
        print("\n>>> 🪛  Testing get_scheduled_deductions")
        try:
            result = await client.call_tool("get_scheduled_deductions", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_scheduled_deductions Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_scheduled_deductions Error: {e}")
        
        # Test 144: get_status_history_for_adjustment
        print("\n>>> 🪛  Testing get_status_history_for_adjustment")
        try:
            result = await client.call_tool("get_status_history_for_adjustment", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_status_history_for_adjustment Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_status_history_for_adjustment Error: {e}")
        
        # Test 145: get_termination_date_range
        print("\n>>> 🪛  Testing get_termination_date_range")
        try:
            result = await client.call_tool("get_termination_date_range", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_termination_date_range Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_termination_date_range Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 30 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 146: get_w2_years
        print("\n>>> 🪛  Testing get_w2_years")
        try:
            result = await client.call_tool("get_w2_years", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_w2_years Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_w2_years Error: {e}")
        
        # Test 147: reprint_1099
        print("\n>>> 🪛  Testing reprint_1099")
        try:
            result = await client.call_tool("reprint_1099", {
                "client_id": client_id,
                "employee_id": ["EMP001"],
                "year": "2023"
            })
            print(f"<<< ✅ reprint_1099 Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ reprint_1099 Error: {e}")
        
        # Test 148: reprint_w2c
        print("\n>>> 🪛  Testing reprint_w2c")
        try:
            result = await client.call_tool("reprint_w2c", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "year": "2023"
            })
            print(f"<<< ✅ reprint_w2c Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ reprint_w2c Error: {e}")
        
        # Test 149: get_bulk_outstanding_invoices
        print("\n>>> 🪛  Testing get_bulk_outstanding_invoices")
        try:
            result = await client.call_tool("get_bulk_outstanding_invoices", {
                "client_id": client_id,
                "download_id": None
            })
            print(f"<<< ✅ get_bulk_outstanding_invoices Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_bulk_outstanding_invoices Error: {e}")
        
        # Test 150: get_client_accounting_template
        print("\n>>> 🪛  Testing get_client_accounting_template")
        try:
            result = await client.call_tool("get_client_accounting_template", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_client_accounting_template Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_accounting_template Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 31 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 151: get_client_gl_data
        print("\n>>> 🪛  Testing get_client_gl_data")
        try:
            result = await client.call_tool("get_client_gl_data", {
                "client_id": client_id,
                "pay_date_start": "2023-01-01",
                "pay_date_end": "2023-12-31"
            })
            print(f"<<< ✅ get_client_gl_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_gl_data Error: {e}")
        
        # Test 152: get_gl_codes
        print("\n>>> 🪛  Testing get_gl_codes")
        try:
            result = await client.call_tool("get_gl_codes", {
                "gl_code": "1000"
            })
            print(f"<<< ✅ get_gl_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_gl_codes Error: {e}")
        
        # Test 153: get_gl_detail_download
        print("\n>>> 🪛  Testing get_gl_detail_download")
        try:
            result = await client.call_tool("get_gl_detail_download", {
                "batch_id": "BATCH001",
                "client_id": [client_id],
                "gl_detail_code_type": ["P", "T"]
            })
            print(f"<<< ✅ get_gl_detail_download Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_gl_detail_download Error: {e}")
        
        # Test 154: get_gl_invoice_detail
        print("\n>>> 🪛  Testing get_gl_invoice_detail")
        try:
            result = await client.call_tool("get_gl_invoice_detail", {
                "gl_company": "COMP001",
                "inv_date": "12/31/23",
                "include_posted": "true"
            })
            print(f"<<< ✅ get_gl_invoice_detail Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_gl_invoice_detail Error: {e}")
        
        # Test 155: get_gl_setup
        print("\n>>> 🪛  Testing get_gl_setup")
        try:
            result = await client.call_tool("get_gl_setup", {
                "gl_template": "TEMPLATE001",
                "gl_type": "P",
                "gl_object_id": "OBJ001"
            })
            print(f"<<< ✅ get_gl_setup Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_gl_setup Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 32 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 156: get_outstanding_invoices
        print("\n>>> 🪛  Testing get_outstanding_invoices")
        try:
            result = await client.call_tool("get_outstanding_invoices", {
                "client_id": client_id,
                "show_only_deposit_match": "1000.00"
            })
            print(f"<<< ✅ get_outstanding_invoices Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_outstanding_invoices Error: {e}")
        
        # Test 157: get_pending_cash_receipts
        print("\n>>> 🪛  Testing get_pending_cash_receipts")
        try:
            result = await client.call_tool("get_pending_cash_receipts", {
                "cash_receipt_batch_id": "ALL",
                "include_post_type": "true",
                "include_deposit_type": "true",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_pending_cash_receipts Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pending_cash_receipts Error: {e}")
        
        # Test 158: get_client_gl_data_v2
        print("\n>>> 🪛  Testing get_client_gl_data_v2")
        try:
            result = await client.call_tool("get_client_gl_data_v2", {
                "client_id": client_id,
                "pay_date_start": "2023-01-01",
                "pay_date_end": "2023-12-31"
            })
            print(f"<<< ✅ get_client_gl_data_v2 Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_gl_data_v2 Error: {e}")
        
        # Test 159: get_assigned_pending_approvals
        print("\n>>> 🪛  Testing get_assigned_pending_approvals")
        try:
            result = await client.call_tool("get_assigned_pending_approvals", {
                "prism_user_id": "testuser",
                "client_id": client_id
            })
            print(f"<<< ✅ get_assigned_pending_approvals Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_assigned_pending_approvals Error: {e}")
        
        # Test 160: get_onboard_tasks
        print("\n>>> 🪛  Testing get_onboard_tasks")
        try:
            result = await client.call_tool("get_onboard_tasks", {
                "client_list": client_id,
                "from_date": "2023-01-01",
                "task": "1"
            })
            print(f"<<< ✅ get_onboard_tasks Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_onboard_tasks Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 33 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 161: get_staffing_placement
        print("\n>>> 🪛  Testing get_staffing_placement")
        try:
            result = await client.call_tool("get_staffing_placement", {
                "vendor_id": "VENDOR001",
                "staffing_client": "CLIENT001",
                "placement_id": "PLACEMENT001"
            })
            print(f"<<< ✅ get_staffing_placement Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_staffing_placement Error: {e}")
        
        # Test 162: get_staffing_placement_list
        print("\n>>> 🪛  Testing get_staffing_placement_list")
        try:
            result = await client.call_tool("get_staffing_placement_list", {
                "employee_id": "EMP001",
                "client_id": client_id,
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_staffing_placement_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_staffing_placement_list Error: {e}")
        
        # Test 163: check_permissions_request_status
        print("\n>>> 🪛  Testing check_permissions_request_status")
        try:
            result = await client.call_tool("check_permissions_request_status", {
                "web_service_user": "testuser"
            })
            print(f"<<< ✅ check_permissions_request_status Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ check_permissions_request_status Error: {e}")
        
        # Test 164: get_api_permissions
        print("\n>>> 🪛  Testing get_api_permissions")
        try:
            result = await client.call_tool("get_api_permissions", {})
            print(f"<<< ✅ get_api_permissions Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_api_permissions Error: {e}")
        
        # Test 165: get_new_hire_questions
        print("\n>>> 🪛  Testing get_new_hire_questions")
        try:
            result = await client.call_tool("get_new_hire_questions", {
                "state_code": "CA"
            })
            print(f"<<< ✅ get_new_hire_questions Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_new_hire_questions Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 34 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 166: get_new_hire_required_fields
        print("\n>>> 🪛  Testing get_new_hire_required_fields")
        try:
            result = await client.call_tool("get_new_hire_required_fields", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_new_hire_required_fields Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_new_hire_required_fields Error: {e}")
        
        # Test 167: check_initialization_status
        print("\n>>> 🪛  Testing check_initialization_status")
        try:
            result = await client.call_tool("check_initialization_status", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ check_initialization_status Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ check_initialization_status Error: {e}")
        
        # Test 168: get_approval_summary
        print("\n>>> 🪛  Testing get_approval_summary")
        try:
            result = await client.call_tool("get_approval_summary", {
                "client_id": client_id,
                "batch_id": "BATCH001",
                "options": "ITEMIZEDDEDUCTIONS"
            })
            print(f"<<< ✅ get_approval_summary Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_approval_summary Error: {e}")
        
        # Test 169: get_batch_info
        print("\n>>> 🪛  Testing get_batch_info")
        try:
            result = await client.call_tool("get_batch_info", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ get_batch_info Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_batch_info Error: {e}")
        
        # Test 170: get_batch_list_by_date
        print("\n>>> 🪛  Testing get_batch_list_by_date")
        try:
            result = await client.call_tool("get_batch_list_by_date", {
                "client_id": client_id,
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "date_type": "PAY",
                "pay_group": "PG001"
            })
            print(f"<<< ✅ get_batch_list_by_date Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_batch_list_by_date Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 35 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 171: get_batch_list_for_approval
        print("\n>>> 🪛  Testing get_batch_list_for_approval")
        try:
            result = await client.call_tool("get_batch_list_for_approval", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_batch_list_for_approval Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_batch_list_for_approval Error: {e}")
        
        # Test 172: get_batch_list_for_initialization
        print("\n>>> 🪛  Testing get_batch_list_for_initialization")
        try:
            result = await client.call_tool("get_batch_list_for_initialization", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_batch_list_for_initialization Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_batch_list_for_initialization Error: {e}")
        
        # Test 173: get_batch_payments
        print("\n>>> 🪛  Testing get_batch_payments")
        try:
            result = await client.call_tool("get_batch_payments", {
                "client_id": client_id,
                "payroll_number": "PAY001"
            })
            print(f"<<< ✅ get_batch_payments Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_batch_payments Error: {e}")
        
        # Test 174: get_batch_status
        print("\n>>> 🪛  Testing get_batch_status")
        try:
            result = await client.call_tool("get_batch_status", {
                "client_id": client_id,
                "batch_ids": "20191,20192,20193"
            })
            print(f"<<< ✅ get_batch_status Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_batch_status Error: {e}")
        
        # Test 175: get_billing_code_totals_by_pay_group
        print("\n>>> 🪛  Testing get_billing_code_totals_by_pay_group")
        try:
            result = await client.call_tool("get_billing_code_totals_by_pay_group", {
                "client_id": client_id,
                "batch_id": "BATCH001",
                "options": "Costs"
            })
            print(f"<<< ✅ get_billing_code_totals_by_pay_group Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_billing_code_totals_by_pay_group Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 36 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 176: get_billing_code_totals_for_batch
        print("\n>>> 🪛  Testing get_billing_code_totals_for_batch")
        try:
            result = await client.call_tool("get_billing_code_totals_for_batch", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ get_billing_code_totals_for_batch Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_billing_code_totals_for_batch Error: {e}")
        
        # Test 177: get_billing_code_totals_with_costs
        print("\n>>> 🪛  Testing get_billing_code_totals_with_costs")
        try:
            result = await client.call_tool("get_billing_code_totals_with_costs", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ get_billing_code_totals_with_costs Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_billing_code_totals_with_costs Error: {e}")
        
        # Test 178: get_billing_rule_unbundled
        print("\n>>> 🪛  Testing get_billing_rule_unbundled")
        try:
            result = await client.call_tool("get_billing_rule_unbundled", {
                "client_id": client_id,
                "billing_rule_num": "RULE001"
            })
            print(f"<<< ✅ get_billing_rule_unbundled Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_billing_rule_unbundled Error: {e}")
        
        # Test 179: get_billing_vouchers
        print("\n>>> 🪛  Testing get_billing_vouchers")
        try:
            result = await client.call_tool("get_billing_vouchers", {
                "client_id": client_id,
                "pay_date_start": "2023-01-01",
                "pay_date_end": "2023-12-31",
                "bill_type": ["1", "2"],
                "count": "10",
                "startpage": "0",
                "options": ["Initialized"]
            })
            print(f"<<< ✅ get_billing_vouchers Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_billing_vouchers Error: {e}")
        
        # Test 180: get_billing_vouchers_by_batch
        print("\n>>> 🪛  Testing get_billing_vouchers_by_batch")
        try:
            result = await client.call_tool("get_billing_vouchers_by_batch", {
                "client_id": client_id,
                "batch_id": "BATCH001",
                "bill_type": ["1", "2"],
                "count": "10",
                "startpage": "0",
                "options": ["Initialized", "BillSort"]
            })
            print(f"<<< ✅ get_billing_vouchers_by_batch Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_billing_vouchers_by_batch Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 37 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 181: get_bulk_year_to_date_values
        print("\n>>> 🪛  Testing get_bulk_year_to_date_values")
        try:
            result = await client.call_tool("get_bulk_year_to_date_values", {
                "client_id": client_id,
                "as_of_date": "2023-12-31"
            })
            print(f"<<< ✅ get_bulk_year_to_date_values Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_bulk_year_to_date_values Error: {e}")
        
        # Test 182: get_clients_with_vouchers
        print("\n>>> 🪛  Testing get_clients_with_vouchers")
        try:
            result = await client.call_tool("get_clients_with_vouchers", {
                "pay_date_start": "2023-01-01",
                "pay_date_end": "2023-12-31"
            })
            print(f"<<< ✅ get_clients_with_vouchers Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_clients_with_vouchers Error: {e}")
        
        # Test 183: get_employee_401k_contributions_by_date
        print("\n>>> 🪛  Testing get_employee_401k_contributions_by_date")
        try:
            result = await client.call_tool("get_employee_401k_contributions_by_date", {
                "client_id": client_id,
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "retirement_plan_id": "PLAN001",
                "options": "CENSUS"
            })
            print(f"<<< ✅ get_employee_401k_contributions_by_date Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_401k_contributions_by_date Error: {e}")
        
        # Test 184: get_employee_for_batch
        print("\n>>> 🪛  Testing get_employee_for_batch")
        try:
            result = await client.call_tool("get_employee_for_batch", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ get_employee_for_batch Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_for_batch Error: {e}")
        
        # Test 185: get_employee_override_rates
        print("\n>>> 🪛  Testing get_employee_override_rates")
        try:
            result = await client.call_tool("get_employee_override_rates", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_employee_override_rates Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_override_rates Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 38 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 186: get_employee_payroll_summary
        print("\n>>> 🪛  Testing get_employee_payroll_summary")
        try:
            result = await client.call_tool("get_employee_payroll_summary", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "year": "2023"
            })
            print(f"<<< ✅ get_employee_payroll_summary Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_payroll_summary Error: {e}")
        
        # Test 187: get_external_pto_balance
        print("\n>>> 🪛  Testing get_external_pto_balance")
        try:
            result = await client.call_tool("get_external_pto_balance", {
                "client_id": client_id,
                "batch_id": "BATCH001",
                "include_history": "true"
            })
            print(f"<<< ✅ get_external_pto_balance Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_external_pto_balance Error: {e}")
        
        # Test 188: get_manual_checks
        print("\n>>> 🪛  Testing get_manual_checks")
        try:
            result = await client.call_tool("get_manual_checks", {
                "client_id": client_id,
                "reference": "REF001",
                "employee_id": "EMP001",
                "check_date": "2023-12-01",
                "check_status": "POST"
            })
            print(f"<<< ✅ get_manual_checks Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_manual_checks Error: {e}")
        
        # Test 189: get_payroll_approval
        print("\n>>> 🪛  Testing get_payroll_approval")
        try:
            result = await client.call_tool("get_payroll_approval", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ get_payroll_approval Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_approval Error: {e}")
        
        # Test 190: get_payroll_batch_with_options
        print("\n>>> 🪛  Testing get_payroll_batch_with_options")
        try:
            result = await client.call_tool("get_payroll_batch_with_options", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ get_payroll_batch_with_options Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_batch_with_options Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 39 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 191: get_payroll_notes
        print("\n>>> 🪛  Testing get_payroll_notes")
        try:
            result = await client.call_tool("get_payroll_notes", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_payroll_notes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_notes Error: {e}")
        
        # Test 192: get_payroll_schedule
        print("\n>>> 🪛  Testing get_payroll_schedule")
        try:
            result = await client.call_tool("get_payroll_schedule", {
                "schedule_code": "WEEKLY"
            })
            print(f"<<< ✅ get_payroll_schedule Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_schedule Error: {e}")
        
        # Test 193: get_payroll_schedule_codes
        print("\n>>> 🪛  Testing get_payroll_schedule_codes")
        try:
            result = await client.call_tool("get_payroll_schedule_codes", {})
            print(f"<<< ✅ get_payroll_schedule_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_schedule_codes Error: {e}")
        
        # Test 194: get_payroll_summary
        print("\n>>> 🪛  Testing get_payroll_summary")
        try:
            result = await client.call_tool("get_payroll_summary", {
                "client_id": client_id,
                "year": "2023",
                "batch_type": "R,S",
                "include_details": True,
                "sort": "EMPLOYEE"
            })
            print(f"<<< ✅ get_payroll_summary Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_summary Error: {e}")
        
        # Test 195: get_payroll_voucher_by_id
        print("\n>>> 🪛  Testing get_payroll_voucher_by_id")
        try:
            result = await client.call_tool("get_payroll_voucher_by_id", {
                "client_id": client_id,
                "voucher_id": "VOUCHER001",
                "options": "CENSUS"
            })
            print(f"<<< ✅ get_payroll_voucher_by_id Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_voucher_by_id Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 40 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 196: get_payroll_voucher_for_batch
        print("\n>>> 🪛  Testing get_payroll_voucher_for_batch")
        try:
            result = await client.call_tool("get_payroll_voucher_for_batch", {
                "client_id": client_id,
                "batch_id": "BATCH001",
                "count": "10",
                "startpage": "0",
                "options": "CENSUS"
            })
            print(f"<<< ✅ get_payroll_voucher_for_batch Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_voucher_for_batch Error: {e}")
        
        # Test 197: get_payroll_vouchers
        print("\n>>> 🪛  Testing get_payroll_vouchers")
        try:
            result = await client.call_tool("get_payroll_vouchers", {
                "client_id": client_id,
                "pay_date_start": "2023-01-01",
                "pay_date_end": "2023-12-31",
                "count": "20",
                "startpage": "0",
                "options": "CENSUS"
            })
            print(f"<<< ✅ get_payroll_vouchers Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_vouchers Error: {e}")
        
        # Test 198: get_payroll_vouchers_for_employee
        print("\n>>> 🪛  Testing get_payroll_vouchers_for_employee")
        try:
            result = await client.call_tool("get_payroll_vouchers_for_employee", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "pay_date_start": "2023-01-01",
                "pay_date_end": "2023-12-31",
                "count": "10",
                "startpage": "0",
                "options": "CENSUS"
            })
            print(f"<<< ✅ get_payroll_vouchers_for_employee Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payroll_vouchers_for_employee Error: {e}")
        
        # Test 199: get_process_schedule
        print("\n>>> 🪛  Testing get_process_schedule")
        try:
            result = await client.call_tool("get_process_schedule", {
                "process_schedule_id": "SCHEDULE001"
            })
            print(f"<<< ✅ get_process_schedule Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_process_schedule Error: {e}")
        
        # Test 200: get_process_schedule_codes
        print("\n>>> 🪛  Testing get_process_schedule_codes")
        try:
            result = await client.call_tool("get_process_schedule_codes", {})
            print(f"<<< ✅ get_process_schedule_codes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_process_schedule_codes Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 41 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 201: get_retirement_adj_voucher_list_by_date
        print("\n>>> 🪛  Testing get_retirement_adj_voucher_list_by_date")
        try:
            result = await client.call_tool("get_retirement_adj_voucher_list_by_date", {
                "client_id": client_id,
                "date_type": "P",
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "employee_id": "EMP001",
                "download_id": "DOWNLOAD001"
            })
            print(f"<<< ✅ get_retirement_adj_voucher_list_by_date Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_retirement_adj_voucher_list_by_date Error: {e}")
        
        # Test 202: get_scheduled_payments
        print("\n>>> 🪛  Testing get_scheduled_payments")
        try:
            result = await client.call_tool("get_scheduled_payments", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_scheduled_payments Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_scheduled_payments Error: {e}")
        
        # Test 203: get_standard_hours
        print("\n>>> 🪛  Testing get_standard_hours")
        try:
            result = await client.call_tool("get_standard_hours", {
                "client_id": client_id
            })
            print(f"<<< ✅ get_standard_hours Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_standard_hours Error: {e}")
        
        # Test 204: get_year_to_date_values
        print("\n>>> 🪛  Testing get_year_to_date_values")
        try:
            result = await client.call_tool("get_year_to_date_values", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "as_of_date": "2023-12-31"
            })
            print(f"<<< ✅ get_year_to_date_values Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_year_to_date_values Error: {e}")
        
        # Test 205: get_pay_group_schedule_report
        print("\n>>> 🪛  Testing get_pay_group_schedule_report")
        try:
            result = await client.call_tool("get_pay_group_schedule_report", {
                "client_id": client_id,
                "pay_group": "WEEKLY",
                "pay_date_start": "2023-01-01",
                "pay_date_end": "2023-12-31",
                "download_id": "DOWNLOAD001"
            })
            print(f"<<< ✅ get_pay_group_schedule_report Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pay_group_schedule_report Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 42 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 206: reprint_check_stub
        print("\n>>> 🪛  Testing reprint_check_stub")
        try:
            result = await client.call_tool("reprint_check_stub", {
                "client_id": client_id,
                "employee_id": "EMP001",
                "voucher_id": "VOUCHER001"
            })
            print(f"<<< ✅ reprint_check_stub Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ reprint_check_stub Error: {e}")
        
        # Test 207: get_allowed_employee_list
        print("\n>>> 🪛  Testing get_allowed_employee_list")
        try:
            result = await client.call_tool("get_allowed_employee_list", {
                "prism_user_id": "testuser",
                "client_id": client_id,
                "employee_id": "EMP001",
                "last_name": "Smith",
                "first_name": "John",
                "employee_status_class": "A",
                "startpage": "0",
                "count": "10"
            })
            print(f"<<< ✅ get_allowed_employee_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_allowed_employee_list Error: {e}")
        
        # Test 208: get_client_list_security
        print("\n>>> 🪛  Testing get_client_list_security")
        try:
            result = await client.call_tool("get_client_list_security", {
                "prism_user_id": "testuser"
            })
            print(f"<<< ✅ get_client_list_security Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_client_list_security Error: {e}")
        
        # Test 209: get_employee_client_list
        print("\n>>> 🪛  Testing get_employee_client_list")
        try:
            result = await client.call_tool("get_employee_client_list", {
                "prism_user_id": "testuser",
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_employee_client_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_client_list Error: {e}")
        
        # Test 210: get_employee_list_security
        print("\n>>> 🪛  Testing get_employee_list_security")
        try:
            result = await client.call_tool("get_employee_list_security", {
                "prism_user_id": "testuser",
                "client_id": client_id
            })
            print(f"<<< ✅ get_employee_list_security Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_list_security Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 43 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 211: get_entity_access
        print("\n>>> 🪛  Testing get_entity_access")
        try:
            result = await client.call_tool("get_entity_access", {
                "prism_user_id": "testuser",
                "client_id": client_id
            })
            print(f"<<< ✅ get_entity_access Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_entity_access Error: {e}")
        
        # Test 212: get_manager_list
        print("\n>>> 🪛  Testing get_manager_list")
        try:
            result = await client.call_tool("get_manager_list", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_manager_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_manager_list Error: {e}")
        
        # Test 213: get_user_data_security
        print("\n>>> 🪛  Testing get_user_data_security")
        try:
            result = await client.call_tool("get_user_data_security", {
                "client_id": client_id,
                "prism_user_id": "testuser"
            })
            print(f"<<< ✅ get_user_data_security Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_user_data_security Error: {e}")
        
        # Test 214: get_user_details
        print("\n>>> 🪛  Testing get_user_details")
        try:
            result = await client.call_tool("get_user_details", {
                "prism_user_id": "testuser"
            })
            print(f"<<< ✅ get_user_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_user_details Error: {e}")
        
        # Test 215: get_user_list_security
        print("\n>>> 🪛  Testing get_user_list_security")
        try:
            result = await client.call_tool("get_user_list_security", {
                "client_id": client_id,
                "user_type": "M"
            })
            print(f"<<< ✅ get_user_list_security Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_user_list_security Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 44 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 216: get_user_role_details
        print("\n>>> 🪛  Testing get_user_role_details")
        try:
            result = await client.call_tool("get_user_role_details", {
                "role_id": "ROLE001"
            })
            print(f"<<< ✅ get_user_role_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_user_role_details Error: {e}")
        
        # Test 217: get_user_roles_list
        print("\n>>> 🪛  Testing get_user_roles_list")
        try:
            result = await client.call_tool("get_user_roles_list", {})
            print(f"<<< ✅ get_user_roles_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_user_roles_list Error: {e}")
        
        # Test 218: is_client_allowed
        print("\n>>> 🪛  Testing is_client_allowed")
        try:
            result = await client.call_tool("is_client_allowed", {
                "prism_user_id": "testuser",
                "client_id": client_id
            })
            print(f"<<< ✅ is_client_allowed Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ is_client_allowed Error: {e}")
        
        # Test 219: is_employee_allowed
        print("\n>>> 🪛  Testing is_employee_allowed")
        try:
            result = await client.call_tool("is_employee_allowed", {
                "prism_user_id": "testuser",
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ is_employee_allowed Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ is_employee_allowed Error: {e}")
        
        # Test 220: get_user_list_v2
        print("\n>>> 🪛  Testing get_user_list_v2")
        try:
            result = await client.call_tool("get_user_list_v2", {
                "client_id": client_id,
                "user_type": "M",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_user_list_v2 Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_user_list_v2 Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 45 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 221: get_employee_image
        print("\n>>> 🪛  Testing get_employee_image")
        try:
            result = await client.call_tool("get_employee_image", {
                "user_id": "USER001"
            })
            print(f"<<< ✅ get_employee_image Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employee_image Error: {e}")
        
        # Test 222: get_favorites
        print("\n>>> 🪛  Testing get_favorites")
        try:
            result = await client.call_tool("get_favorites", {
                "user_id": "USER001"
            })
            print(f"<<< ✅ get_favorites Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_favorites Error: {e}")
        
        # Test 223: get_vendor_info
        print("\n>>> 🪛  Testing get_vendor_info")
        try:
            result = await client.call_tool("get_vendor_info", {
                "client_id": client_id,
                "user_id": "USER001",
                "ext_vendor_id": "VENDOR001"
            })
            print(f"<<< ✅ get_vendor_info Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_vendor_info Error: {e}")
        
        # Test 224: get_all_subscriptions
        print("\n>>> 🪛  Testing get_all_subscriptions")
        try:
            result = await client.call_tool("get_all_subscriptions", {
                "user_string_id": "test_subscription"
            })
            print(f"<<< ✅ get_all_subscriptions Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_all_subscriptions Error: {e}")
        
        # Test 225: get_events
        print("\n>>> 🪛  Testing get_events")
        try:
            result = await client.call_tool("get_events", {
                "subscription_id": "SUB001",
                "replay_id": "REPLAY001",
                "number_of_events": "10"
            })
            print(f"<<< ✅ get_events Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_events Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 46 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 226: get_new_events
        print("\n>>> 🪛  Testing get_new_events")
        try:
            result = await client.call_tool("get_new_events", {
                "subscription_id": "SUB001",
                "number_of_events": "10"
            })
            print(f"<<< ✅ get_new_events Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_new_events Error: {e}")
        
        # Test 227: get_subscription
        print("\n>>> 🪛  Testing get_subscription")
        try:
            result = await client.call_tool("get_subscription", {
                "subscription_id": "SUB001"
            })
            print(f"<<< ✅ get_subscription Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_subscription Error: {e}")
        
        # Test 228: get_ach_file_list
        print("\n>>> 🪛  Testing get_ach_file_list")
        try:
            result = await client.call_tool("get_ach_file_list", {
                "originator_id": "ORIG001",
                "post_date_start": "2024-01-01",
                "post_date_end": "2024-12-31",
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_ach_file_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_ach_file_list Error: {e}")
        
        # Test 229: get_ar_transaction_report
        print("\n>>> 🪛  Testing get_ar_transaction_report")
        try:
            result = await client.call_tool("get_ar_transaction_report", {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "download_id": "DOWNLOAD001",
                "client_id": [client_id]
            })
            print(f"<<< ✅ get_ar_transaction_report Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_ar_transaction_report Error: {e}")
        
        # Test 230: get_data
        print("\n>>> 🪛  Testing get_data")
        try:
            result = await client.call_tool("get_data", {
                "schema_name": "Employee",
                "class_name": "EmployeeData",
                "download_id": "DOWNLOAD001",
                "client_id": [client_id]
            })
            print(f"<<< ✅ get_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_data Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 47 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 231: get_employer_details
        print("\n>>> 🪛  Testing get_employer_details")
        try:
            result = await client.call_tool("get_employer_details", {
                "employer_id": "100.33"
            })
            print(f"<<< ✅ get_employer_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_employer_details Error: {e}")
        
        # Test 232: get_invoice_data
        print("\n>>> 🪛  Testing get_invoice_data")
        try:
            result = await client.call_tool("get_invoice_data", {
                "client_id": client_id,
                "batch_id": "BATCH001",
                "invoice_id": "INV001"
            })
            print(f"<<< ✅ get_invoice_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_invoice_data Error: {e}")
        
        # Test 233: get_multi_entity_group_list
        print("\n>>> 🪛  Testing get_multi_entity_group_list")
        try:
            result = await client.call_tool("get_multi_entity_group_list", {
                "count": "10",
                "startpage": "0",
                "client_id": client_id,
                "multi_entity_group_id": "GROUP001"
            })
            print(f"<<< ✅ get_multi_entity_group_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_multi_entity_group_list Error: {e}")
        
        # Test 234: get_payee
        print("\n>>> 🪛  Testing get_payee")
        try:
            result = await client.call_tool("get_payee", {
                "payee_id": "PAYEE001",
                "payee_type": "G"
            })
            print(f"<<< ✅ get_payee Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payee Error: {e}")
        
        # Test 235: get_payments_pending
        print("\n>>> 🪛  Testing get_payments_pending")
        try:
            result = await client.call_tool("get_payments_pending", {
                "client_id": client_id,
                "batch_id": "BATCH001",
                "status": "PAYPEND"
            })
            print(f"<<< ✅ get_payments_pending Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_payments_pending Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 48 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 236: get_positive_pay_check_stub
        print("\n>>> 🪛  Testing get_positive_pay_check_stub")
        try:
            result = await client.call_tool("get_positive_pay_check_stub", {})
            print(f"<<< ✅ get_positive_pay_check_stub Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_positive_pay_check_stub Error: {e}")
        
        # Test 237: get_positive_pay_file_list
        print("\n>>> 🪛  Testing get_positive_pay_file_list")
        try:
            result = await client.call_tool("get_positive_pay_file_list", {
                "checking_acct": "CHECK001",
                "file_stub": "STUB001",
                "date_created": "2024-01-01",
                "most_recent": True,
                "count": "10",
                "startpage": "0"
            })
            print(f"<<< ✅ get_positive_pay_file_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_positive_pay_file_list Error: {e}")
        
        # Test 238: get_unbilled_benefit_adjustments
        print("\n>>> 🪛  Testing get_unbilled_benefit_adjustments")
        try:
            result = await client.call_tool("get_unbilled_benefit_adjustments", {
                "download_id": "DOWNLOAD001",
                "client_id": [client_id],
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "include_term_client": "true",
                "status_class": "A"
            })
            print(f"<<< ✅ get_unbilled_benefit_adjustments Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_unbilled_benefit_adjustments Error: {e}")
        
        # Test 239: identify_ach_process_lock
        print("\n>>> 🪛  Testing identify_ach_process_lock")
        try:
            result = await client.call_tool("identify_ach_process_lock", {})
            print(f"<<< ✅ identify_ach_process_lock Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ identify_ach_process_lock Error: {e}")
        
        # Test 240: positive_pay_download
        print("\n>>> 🪛  Testing positive_pay_download")
        try:
            result = await client.call_tool("positive_pay_download", {
                "download_id": "DOWNLOAD001",
                "checking_account": "CHECK001",
                "file_stub": "STUB001",
                "start_check_date": "2024-01-01",
                "end_check_date": "2024-12-31",
                "include_voided_checks": True
            })
            print(f"<<< ✅ positive_pay_download Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ positive_pay_download Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 49 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 241: recreate_positive_pay
        print("\n>>> 🪛  Testing recreate_positive_pay")
        try:
            result = await client.call_tool("recreate_positive_pay", {
                "download_id": "DOWNLOAD001",
                "file_name": "POSITIVE_PAY_FILE.txt"
            })
            print(f"<<< ✅ recreate_positive_pay Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ recreate_positive_pay Error: {e}")
        
        # Test 242: stream_ach_data
        print("\n>>> 🪛  Testing stream_ach_data")
        try:
            result = await client.call_tool("stream_ach_data", {
                "ach_batch_id": "BATCH001",
                "ach_file_name": "ACH_FILE.txt"
            })
            print(f"<<< ✅ stream_ach_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ stream_ach_data Error: {e}")
        
        # Test 243: get_suta_information
        print("\n>>> 🪛  Testing get_suta_information")
        try:
            result = await client.call_tool("get_suta_information", {
                "client_id": client_id,
                "employee_id": "EMP001"
            })
            print(f"<<< ✅ get_suta_information Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_suta_information Error: {e}")
        
        # Test 244: get_tax_authorities
        print("\n>>> 🪛  Testing get_tax_authorities")
        try:
            result = await client.call_tool("get_tax_authorities", {
                "state_code": "CA",
                "authority_id": "AUTH001"
            })
            print(f"<<< ✅ get_tax_authorities Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_tax_authorities Error: {e}")
        
        # Test 245: get_tax_rate
        print("\n>>> 🪛  Testing get_tax_rate")
        try:
            result = await client.call_tool("get_tax_rate", {
                "workers_comp_policy_id": "POLICY001",
                "workers_comp_class": "CLASS001",
                "employer_id": "EMP001",
                "effective_date": "2024-01-01",
                "client_id": client_id
            })
            print(f"<<< ✅ get_tax_rate Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_tax_rate Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 50 - NEXT 5 ENDPOINTS")
        print("="*60)
        
        # Test 246: get_state_w4_params
        print("\n>>> 🪛  Testing get_state_w4_params")
        try:
            result = await client.call_tool("get_state_w4_params", {
                "state_code": "CA"
            })
            print(f"<<< ✅ get_state_w4_params Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_state_w4_params Error: {e}")
        
        # Test 247: get_workers_comp_classes
        print("\n>>> 🪛  Testing get_workers_comp_classes")
        try:
            result = await client.call_tool("get_workers_comp_classes", {
                "state_code": "CA"
            })
            print(f"<<< ✅ get_workers_comp_classes Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_workers_comp_classes Error: {e}")
        
        # Test 248: get_workers_comp_policy_details
        print("\n>>> 🪛  Testing get_workers_comp_policy_details")
        try:
            result = await client.call_tool("get_workers_comp_policy_details", {
                "policy_id": "POLICY001"
            })
            print(f"<<< ✅ get_workers_comp_policy_details Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_workers_comp_policy_details Error: {e}")
        
        # Test 249: get_workers_comp_policy_list
        print("\n>>> 🪛  Testing get_workers_comp_policy_list")
        try:
            result = await client.call_tool("get_workers_comp_policy_list", {
                "effective_date": "2024-01-01"
            })
            print(f"<<< ✅ get_workers_comp_policy_list Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_workers_comp_policy_list Error: {e}")
        
        # Test 250: get_timesheet_batch_status
        print("\n>>> 🪛  Testing get_timesheet_batch_status")
        try:
            result = await client.call_tool("get_timesheet_batch_status", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ get_timesheet_batch_status Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_timesheet_batch_status Error: {e}")
        
        print("\n" + "="*60)
        print("TESTING BATCH 51 - FINAL 3 ENDPOINTS")
        print("="*60)
        
        # Test 251: get_timesheet_param_data
        print("\n>>> 🪛  Testing get_timesheet_param_data")
        try:
            result = await client.call_tool("get_timesheet_param_data", {
                "client_id": client_id,
                "user_id": "USER001"
            })
            print(f"<<< ✅ get_timesheet_param_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_timesheet_param_data Error: {e}")
        
        # Test 252: get_pay_import_definition
        print("\n>>> 🪛  Testing get_pay_import_definition")
        try:
            result = await client.call_tool("get_pay_import_definition", {
                "definition_id": "DEF001"
            })
            print(f"<<< ✅ get_pay_import_definition Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_pay_import_definition Error: {e}")
        
        # Test 253: get_timesheet_data
        print("\n>>> 🪛  Testing get_timesheet_data")
        try:
            result = await client.call_tool("get_timesheet_data", {
                "client_id": client_id,
                "batch_id": "BATCH001"
            })
            print(f"<<< ✅ get_timesheet_data Result:")
            print(f"Response: {result.content[0].text}")
        except Exception as e:
            print(f"<<< ❌ get_timesheet_data Error: {e}")
        
        print("\n" + "="*60)
        print("🎉 ALL 253 ENDPOINTS COMPLETED! 🎉")
        print("="*60)
        

if __name__ == "__main__":
    asyncio.run(test_server())
