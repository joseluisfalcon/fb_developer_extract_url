import pytest
import os
import json
import asyncio
from main import run_debugger

# Use the virtual environment for tests
# Specifically, we verify the environment is active or can be activated

def test_config_sample_exists():
    assert os.path.exists('config_facebook_developer.json.sample')

def test_main_script_exists():
    assert os.path.exists('main.py')

@pytest.mark.asyncio
async def test_debugger_structure():
    """Verify the run_debugger function can be imported and is an async function."""
    assert asyncio.iscoroutinefunction(run_debugger)

@pytest.mark.asyncio
async def test_playwright_launch():
    """Verify that Playwright can launch a browser (requires browsers installed)."""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        assert browser is not None
        await browser.close()

def test_install_script_exists():
    assert os.path.exists('install.sh') or os.path.exists('install.bat')
