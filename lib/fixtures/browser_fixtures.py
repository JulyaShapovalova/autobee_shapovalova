from typing import Callable, Dict
import pytest
from playwright.sync_api import Browser, BrowserContext, BrowserType
import os
from lib.helpers.url_helper import get_domain_without_region


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        'no_viewport': True,
        'ignore_https_errors': True,
    }


@pytest.fixture(scope='session')
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        'args': [
            '--start-maximized',
            '--disable-notifications',
            '--disable-infobars',
            '--window-size=1920,1080',
        ]
    }


@pytest.fixture(scope='session')
def launch_browser(
        browser_type_launch_args: Dict,
        browser_type: BrowserType,
) -> Callable[..., Browser]:
    def launch(**kwargs: Dict) -> Browser:
        launch_options = {**browser_type_launch_args, **kwargs}
        browser = browser_type.launch(**launch_options)
        return browser
    return launch


@pytest.fixture
def browser(launch_browser: Callable[[], Browser], browser_type_launch_args, request) -> None:
    browser = launch_browser()
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser, browser_context_args) -> None:
    context: BrowserContext = browser.new_context(**browser_context_args)
    if os.getenv('ADDITIONAL_COOKIE'):
        context.add_cookies(
            [
                {
                    'name': os.getenv('ADDITIONAL_COOKIE'),
                    'value': 'true',
                    'domain': f'.{get_domain_without_region(os.getenv("BASE_URL"))}',
                    'path': '/',
                },
            ]
        )
    yield context
    context.close()
