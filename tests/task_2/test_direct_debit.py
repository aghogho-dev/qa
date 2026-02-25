import pytest 
import requests 
from dotenv import load_dotenv
load_dotenv()


class TestDirectDebit:
    
    @pytest.mark.parametrize("test_id, limit, page, expected_status", [
        ("valid_limit_10", 10, 1, 200),  
        ("valid_limit_max", 100, 1, 200),
        ("boundary_limit_zero", 0, 1, 400),
        ("invalid_type_string", "abc", 1, 400),
        ("invalid_value_negative", -1, 1, 400)
    ])
    def test_get_all_banks(self, base_url, api_headers, test_id, limit, page, expected_status, request):
        """
        Get All Banks - GET /direct-debit/banks?limit=x&page=y
        """
        url = f"{base_url}/direct-debit/banks"
        params = {"limit": limit, "page": page, "sort_dir": "ASC"}

        response = requests.get(url, params=params, headers=api_headers)

    
        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed {test_id}: Expected {expected_status} but got {response.status_code}"

        if response.status_code == 200:
            response_data = response.json()
            assert response_data.get("status") == "success"
            assert isinstance(response_data.get("data"), dict), f"{test_id}: Data is not a dictionary"


    @pytest.mark.parametrize("test_id, bank_id, expected_status", [
        ("Positive Case", 1, 200),
        ("Positive Case: bank_id high", 100, 200),
        ("Boundary Case: bank_id zero", 0, 400),
        ("Invalid bank_id: letter", "a", 400),
        ("Invalid bank_id: negative", -1, 400)
    ])
    def test_get_details_bank(self, base_url, api_headers, test_id, bank_id, expected_status, request):
        """
        Get Details Bank - GET /direct-debit/banks?bank_id=x
        """
        url = f"{base_url}/direct-debit/banks"
        params = {"bank_id": bank_id}

        response = requests.get(url, params=params, headers=api_headers)

        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed {test_id}: Got {response.status_code}"

        if response.status_code == 200:
            response_data = response.json()
            assert response_data.get("status") == "success"
            assert isinstance(response_data.get("data"), dict), f"{test_id}: Data returned is not a dictionary"


    @pytest.mark.parametrize("test_id, payload, expected_status", [
        ("Positive Case", {"account_number": "2150302690", "bank_code": "057"}, 200),
        ("Missing account number", {"bank_code": "057"}, 400),
        ("Missing bank code", {"account_number": "2150302690"}, 400),
        ("Invalid account number format", {"account_number": "ABC1234567", "bank_code": "057"}, 400),
        ("Account number too short", {"account_number": "123456", "bank_code": "057"}, 400),
        ("Account number too long", {"account_number": "123456789012345", "bank_code": "057"}, 400),
        ("Negative account number and bank code", {"account_number": "-1234567890", "bank_code": "-057"}, 400),
        ("Missing account number and bank code", {}, 400),
        ("SQL Injection Attempt bank code", {"account_number": "1234567890", "bank_code": "057' OR 1=1 --"}, 400),
    ])
    def test_post_verify_bank_account_number(self, base_url, api_headers, test_id, payload, expected_status, request):
        """
        Verify Bank Account No - POST /direct-debit/banks/account-lookup
        """
        
        url = f"{base_url}/direct-debit/banks/account-lookup"
        
        
        response = requests.post(url, json=payload, headers=api_headers)
    
        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed on {test_id}: {response.text}"

        if response.status_code == 200:
            response_data = response.json()
            assert response_data.get("status") == "success"
            data = response_data.get("data")
            assert isinstance(data, dict)
            assert "account_name" in data
            assert "bvn" in data
            





    
