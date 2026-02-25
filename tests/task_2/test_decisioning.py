import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


class TestDecisioning:

    @pytest.mark.parametrize("expected_status", [200])
    def test_get_decision_models(self, base_url, api_headers, expected_status, request):
        """
        GET /decisioning/models
        """
        url = f"{base_url}/decisioning/models"

        response = requests.get(url, headers=api_headers)

        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, response.text

        if response.status_code == 200:
            response_data = response.json()
            assert isinstance(response_data, dict)
            

    @pytest.mark.parametrize("test_id, model_id, expected_status", [
        ("Valid Model", 1, 200),        
        ("Invalid Model - Negative", -1, 400),       
        ("Edge Case", 0, 400),   
        ("Invalid Model - Letter", "a", 400),   
    ])
    def test_get_decision_model_details(self, base_url, api_headers, test_id, model_id, expected_status, request):
        """
        GET /decisioning/models/:id/settings
        """
        url = f"{base_url}/decisioning/models/{model_id}/settings"

        response = requests.get(url, headers=api_headers)

        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed on {test_id}: {response.text}"

        if response.status_code == 200:
            response_data = response.json()
            assert isinstance(response_data, dict)


    @pytest.mark.parametrize("test_id, model_id, expected_status", [
        ("Valid Model", 1, 200),        
        ("Invalid Model - Negative", -1, 400),       
    ])
    def test_oraculi_borrower_scoring(self, base_url, api_headers, test_id, model_id, expected_status, request):
        """
        POST /decisioning/models/{id}
        """
        url = f"{base_url}/decisioning/models/{model_id}"

        
        payload = {
            "gender": "Female",
            "marital_status": "Single",
            "age": "21",
            "location": "lagos",
            "no_of_dependent": "0",
            "type_of_residence": "Rented Apartment",
            "educational_attainment": "BSc, HND and Other Equivalent",
            "employment_status": "Employed",
            "sector_of_employment": "Other Financial",
            "monthly_net_income": "100,000 - 199,999",
            "employer_category": "Private Company",
            "bvn": "22536051111",
            "phone_number": "08012345678",
            "total_years_of_experience": 5,
            "time_with_current_employer": 2,
            "previous_lendsqr_loans": 3,
            "phone": "07062561111",
            "bvn_phone": "07062561111",
            "office_email": "adojohnsule@lendsqr.com",
            "personal_email": "adojohnsule@lendsqr.com",
            "amount": 10000
        }

        response = requests.post(url, json=payload, headers=api_headers)

        request.node.latency = f"{response.elapsed.total_seconds():.3f}s"

        assert response.status_code == expected_status, f"Failed on {test_id}: {response.text}"

        if response.status_code == 200:
            response_data = response.json()
            assert response_data.get("status") == "success"
            assert response_data.get("message") == "Successful"
            data = response_data.get("data")
            assert isinstance(data, dict)
            assert isinstance(data.get("total_weight"), int)
            assert isinstance(data.get("score"), float)
            assert isinstance(data.get("offers").get("success"), bool)