"""Provides an interface for the NicoCourts.com API"""
import base64 as b64
import json
import requests as r
import requests_toolbelt as tb
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
        res = r.get(self.url + "images/")
        try:
            response = res.json()
        except ValueError:
            response = res.status

        return  response

    def get_posts(self):
        """Fetch a JSON object containing the current posts"""
        return self.post_object(None, path="posts/all/")
    
    def create_post(self, post):
        """Create a new post"""
        return self.post_object(post, path="post/")

    def post_object(self, obj, path=""):
        """Creates a POST request to the API with the provided JSON object.

        Client can include an (optional) an API route to post to."""
        signed_obj = self.sign_obj(obj)
        res = r.post(self.url + path, json=signed_obj)

        try:
            response = res.json()
        except ValueError:
            response = res.status

        return  response

    def upload_img(self, filename):
        """Upload an image to the API"""
        with open(filename, 'rb') as f:
            img = f.read()

        signed_obj = self.sign_obj(None)

        # Make the request
        mpf = tb.multipart.MultipartEncoder(fields = {
            "Nonce":signed_obj['Nonce'], "Sig":signed_obj["Sig"], "Filename":filename,
            "img": open(filename, 'rb')
        })

        res = r.post(self.url + "upload/", data=mpf, headers={"Content-Type":mpf.content_type})

        try:
            response = res.json()
        except ValueError:
            response = res.status

        return  response

    def sign_obj(self, obj):
        """Sign the object (with a nonce) and return a bytearray for the query"""
        nonce = self.get_nonce()
        if obj is None:
            sig = self.crypto.sign_blob(nonce)
            json_obj = json.dumps([]).encode('utf-8')
        else:
            json_obj = json.dumps(obj).encode('utf-8')
            sig = self.crypto.sign_blob(nonce + json_obj)

        signed_obj = {"Payload": b64.standard_b64encode(json_obj),
                      "Nonce": str(b64.standard_b64encode(nonce), 'utf-8'),
                      "Sig": sig}

        return signed_obj
