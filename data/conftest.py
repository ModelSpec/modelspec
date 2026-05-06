import pytest

from tools.middleware.factory import get_middleware_class

def pytest_addoption(parser):
    parser.addoption(
        "--modeling-tool",
        action="store",
        default="both",
        choices=["umple", "ecore", "both"],
    )

def pytest_generate_tests(metafunc):
    if "modelingTool" in metafunc.fixturenames:
        config_choice = metafunc.config.getoption("--modeling-tool")

        if config_choice == "both":
            modeling_tools = ["umple", "ecore"]
        else:
            modeling_tools = [config_choice]

        metafunc.parametrize("modelingTool", modeling_tools, ids=modeling_tools)

@pytest.fixture
def mw(modelingTool):
    return get_middleware_class(modelingTool)