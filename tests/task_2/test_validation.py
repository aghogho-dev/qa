import pytest 
import requests 
from dotenv import load_dotenv
load_dotenv()

class TestValidation:

    @pytest.mark.parametrize("test_id, bvn, payload, expected_status", [
        ("Positive Contact", 12345678901, {"contact":"08068888878"}, 200),
        ("Negative Contact", 12345678901, {"contact":"-08068888878"}, 400),
        ("No Contact", 12345678901, {"contact":""}, 400), # Security Risk. Should not get to the server
        ("Invalid Contact", 12345678901, {"contact":"abcdefghij@"}, 400),
        ("Invalid BVN Length", 111, {"contact":"08068888878"}, 400), # Security Risk. Should not reach the server
        ("Empty Contact/Payload", 12345678901, {}, 400), 
        ("SQL Injection Contact", 12345678901, {"contact":"08068888878' OR 1=1 --"}, 400),
        ("XSS Script Attempt", 12345678901, {"contact": "<script>alert('xss')</script>"}, 400),
    ])
    def test_post_initialize_bvn_consent(self, base_url, api_headers, test_id, bvn, payload, expected_status, request):
        """
        Initialize BVN Consent - POST: /verification/bvn/:bvn
        """
        url = f"{base_url}/verification/bvn/{bvn}"
        
        response = requests.post(url, json=payload, headers=api_headers)
    
        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed on {test_id}: {response.text}"

        if response.status_code == 200:
            response_data = response.json()
            assert response_data.get("status") == "otp"
            assert response_data.get("message") == "Please provide OTP sent to contact"
            data = response_data.get("data")
            assert isinstance(data, str)
            

    @pytest.mark.parametrize("test_id, bvn, payload, expected_status", [
        ("Correct OTP", 12345678901, {"otp":"123456"}, 200),
        ("Short OTP", 12345678901, {"otp":"1234"}, 400),
        ("Long OTP", 12345678901, {"otp":"123456789"}, 400),
        ("Invalid OTP Letter", 12345678901, {"otp":"abcdef"}, 400),
        ("Invalid OTP Letter Short", 12345678901, {"otp":"abc"}, 400),
        ("Negative OTP", 12345678901, {"otp":"-123456"}, 400),
        ("Missing OTP", 12345678901, {}, 400),
        ("Space OTP", 12345678901, {"otp":"   "}, 400),
        ("SQL Injection OTP", 12345678901, {"otp":"123456' OR 1=1 --"}, 400),

    ])
    def test_put_complete_bvn_details(self, base_url, api_headers, test_id, bvn, payload, expected_status, request):
        """
        Complete BVN Details - PUT: /verification/bvn/:bvn
        """
        url = f"{base_url}/verification/bvn/{bvn}"


        
        response = requests.put(url, json=payload, headers=api_headers)
    
        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed on {test_id}: {response.text}"

        if response.status_code == 200:
            response_data = response.json()
            assert response_data.get("status") == "success"
            assert response_data.get("message") == "Successful"
            data = response_data.get("data")
            assert isinstance(data, dict)
            assert "bvn" in data
            assert "first_name" in data
            assert "last_name" in data
            assert "dob" in data
            assert "mobile" in data


        