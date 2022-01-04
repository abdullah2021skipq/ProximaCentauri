import requests
import pytest

url = "https://uy6nl52jga.execute-api.us-east-2.amazonaws.com/prod"
item = {"URL_ADDRESS": "www.test123.com"}
item1 = {
		"URL_ADDRESS": "www.test123.com",
		"updateValue": "www.test123456.com"
		}

def test_health():
    response = requests.get(url+"/health")
    statusCode = response.status_code
    assert statusCode == 200

def test_url_post():
    response = requests.post(url+"/url",json=item)
    statusCode = response.status_code
    assert statusCode == 200

def test_url_delete():
    response = requests.delete(url+"/url",json=item)
    statusCode = response.status_code
    assert statusCode == 200

def test_url_patch():
    requests.post(url+"/url",json=item)
    response = requests.patch(url+"/url",json=item1)
    statusCode = response.status_code
    assert statusCode == 200