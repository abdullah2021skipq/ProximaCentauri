import requests
import pytest

url = "https://vbm2zuqr17.execute-api.us-east-2.amazonaws.com/prod/"


'''
TEST RESPONSE OF LOADING URLS FROM BUCKET
'''
def test_bucket_put():
    response = requests.put(url+"BUCKET_LIST", params = {
                                                            "bucket_name": 'sikandarbakhtskipq',
                                                            "object_key": 'urls_dict.json'})
    statusCode = response.status_code
    assert statusCode == 200


'''
TEST RESPONSE OF POST URLS TO TABLE
'''

def test_url_post():
    response = requests.post(url+"TABLE", params = {
                                                        "url_name" : "Test",
                                                        "url" : "www.testing.com"})
    statusCode = response.status_code
    assert statusCode == 200
