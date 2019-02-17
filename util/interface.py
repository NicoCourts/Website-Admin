"""Provides an interface for the NicoCourts.com API"""
import base64 as b64
import json
import bson
import requests as r
from .crypto import Crypto


class APICaller:
    """Provides an interface one can use to interact with the API"""

    def __init__(self, url="https://api.nicocourts.com/"):
        """Initialize the class with the (local) private key and spin up the crypto library."""
        self.url = url
        self.crypto = Crypto()

    def get_nonce(self):
        """Returns a bytearray of the current nonce, ready for hashing"""
        res = r.get(self.url + "nonce/").json()
        return b64.standard_b64decode(res['value'])

    def get_image_list(self):
        """Fetch and return a JSON object full of image metadata"""
        params = self.sign_obj({})
        res = r.get(self.url + "images/", params).read().decode("utf-8")
        return res.json()

    def get_posts(self):
        """Fetch a JSON object containing the current posts"""
        res = r.get(self.url + "posts/all/")
        return res.json()

    def post_object(self, obj, path=""):
        """Creates a POST request to the API with the provided JSON object.

        Client can include an (optional) an API route to post to."""
        signed_obj = self.sign_obj(obj)
        res = r.post(self.url + path, signed_obj)
        return res.json()

    def sign_obj(self, obj):
        """Sign the object (with a nonce) and return a bytearray for the query"""
        nonce = self.get_nonce()
        json_obj = json.dumps(obj).encode('utf-8')
        sig = self.crypto.sign_blob(nonce + json_obj)

        signed_obj = {"Payload":obj,
                      "Nonce": str(b64.standard_b64encode(nonce), 'utf-8'),
                      "Sig":sig}

        return signed_obj

    def upload_img(self, filename):
        """Upload an image to the API"""
        with open(filename, 'rb') as f:
            thing = bson.dumps({'img':f.read()})
        print(bson.loads(thing))
