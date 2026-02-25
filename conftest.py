import os
import pytest
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".env.local", override=True)

def pytest_addoption(parser):
    # Add the --scopes flag to command line
    parser.addoption(
        "--scopes", 
        action="store", 
        default="all", 
        help="Comma-separated list of scope keys to select"
    )

@pytest.fixture
def requested_scopes(request):
    # Fixture to retrieve the scopes passed
    return request.config.getoption("--scopes")

@pytest.fixture(scope="session")
def api_headers():
    return {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

@pytest.fixture(scope="session")
def base_url():
    return f"{os.getenv("BASE_API_URL")}"


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")
    cells.insert(3, "<th>Latency</th>")
    cells.pop()

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{getattr(report, 'description', '')}</td>")
    cells.insert(3, f"<td>{getattr(report, 'latency', 'N/A')}</td>")
    cells.pop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__).strip()
    report.latency = getattr(item, "latency", "N/A")
