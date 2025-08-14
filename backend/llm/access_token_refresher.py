# Automates Access Token retrieval

import requests
import hashlib
import base64
import secrets

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode

def generate_pkce():
    """
    Generate PKCE code verifier and code challenge.
    """
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge


def build_authorization_url(client_id, redirect_uri, scope, code_challenge):
    """
    Construct the authorization URL with PKCE parameters.
    """
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
    }
    return f"{auth_url}?{urlencode(params)}"


def automate_login(driver, username, password):
    """
    Automate login using Selenium.
    """
    # Wait for username field and enter the username
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'signInFormUsername'))
    ).send_keys(username)

    # Wait for password field and enter the password
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'signInFormPassword'))
    ).send_keys(password)

    # Wait for the submit button and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, 'signInSubmitButton'))
    ).click()

    # Wait for redirection to capture the authorization code
    WebDriverWait(driver, 10).until(lambda d: 'code=' in d.current_url)
    return driver.current_url


def exchange_code_for_token(token_url, client_id, client_secret, authorization_code, redirect_uri, code_verifier):
    """
    Exchange the authorization code for an access token.
    """
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier,
    }

    response = requests.post(token_url, data=token_data)
    return response


# Step 1: Initialize Parameters
client_id = 'client_id_here'
client_secret = 'client_secret_here'
auth_url = 'https://us-east-1.amazoncognito.com/oauth2/authorize'
token_url = 'https://us-east-1.amazoncognito.com/oauth2/token'
redirect_uri = 'https://oauth.pstmn.io/v1/callback'
scope = 'openid'
username = 'email_here'
password = 'password_here'

# Step 2: Generate PKCE
code_verifier, code_challenge = generate_pkce()

# Step 3: Build Authorization URL
authorization_url = build_authorization_url(client_id, redirect_uri, scope, code_challenge)
print("Authorization URL:", authorization_url)

# Step 4: Set Up Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Navigate to the authorization URL
    driver.get(authorization_url)

    # Automate login and get the redirected URL
    redirected_url = automate_login(driver, username, password)
    print("Redirected URL:", redirected_url)

    # Extract the authorization code
    parsed_url = urlparse(redirected_url)
    authorization_code = parse_qs(parsed_url.query).get('code', [None])[0]

    if not authorization_code:
        raise Exception("Authorization code not found in redirected URL.")

    print("Authorization Code:", authorization_code)

    # Step 5: Exchange Authorization Code for Access Token
    response = exchange_code_for_token(
        token_url, client_id, client_secret, authorization_code, redirect_uri, code_verifier
    )

    # Step 6: Handle the Response
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print("Access Token:", access_token)
        
        # Write the access token to a file
        with open("access_token.txt", "w") as token_file:
            token_file.write(access_token)
            print("Access token saved to access_token.txt")
    else:
        print("Failed to retrieve access token:", response.json())

finally:
    driver.quit()
