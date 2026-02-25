import pytest 
import requests 
from dotenv import load_dotenv 
load_dotenv()


class TestCreditBureau:

    @pytest.mark.parametrize("test_id, bvn, expected_status", [
        ("Positive Case", 12345678901, 200),
        ("Negative Case", -1234567890, 400),
        ("Edge Case", 00000000000, 400),
        ("Invalid BVN Letter", "abcdefghijk", 400),
        ("BVN Short", 12345678, 400),
        ("BVN Long", 123456789012345, 400),
    ])
    def test_get_credit_report_from_crc_bureau(self, base_url, api_headers, test_id, bvn, expected_status, request):
        """
        Credit Report from CRC - GET /creditbureaus/crc/:bvn
        """
        url = f"{base_url}/creditbureaus/crc/{bvn}"
        
        response = requests.get(url, headers=api_headers)
    
        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed on {test_id}: {response.text}"

        if response.status_code == 200:
            response_data = response.json()
            assert response_data.get("status") == "success"
            assert response_data.get("message") == "Successful"
            data = response_data.get("data")
            assert isinstance(data, dict)


    @pytest.mark.parametrize("test_id, bvn, expected_status", [
        ("Positive Case", 12345678901, 200),
        ("Negative Case", -1234567890, 400),
        ("Edge Case", 00000000000, 400),
        ("Invalid BVN Letter", "abcdefghijk", 400),
        ("BVN Short", 12345678, 400),
        ("BVN Long", 123456789012345, 400),
    ])
    def test_get_credit_report_from_firstcentral(self, base_url, api_headers, test_id, bvn, expected_status, request):
        """
        Credit Report from FirstCentral - GET /creditbureaus/firstcentral/:bvn
        """
        url = f"{base_url}/creditbureaus/firstcentral/{bvn}"
        
        response = requests.get(url, headers=api_headers)
    
        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed on {test_id}: {response.text}"

        if response.status_code == 200:
            response_data = response.json()
            assert response_data.get("status") == "success"
            assert "This is a test mode response" in response_data.get("message")
            data = response_data.get("data")
            assert isinstance(data, dict)
