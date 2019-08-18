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

        return response

    def get_posts(self, path="posts/all/"):
        """Fetch a JSON object containing the current posts"""
        return self.post_object('', path).json()
    
    def create_post(self, post):
        """Create a new post"""
        return self.post_object(post, "post/")

    def update_post(self, post, postid):
        """Update a current post"""
        return self.post_object(post, "post/" + postid)
    
    def toggle_visible(self, postid):
        """Toggle the visibility of a post."""
        return self.post_object('', 'post/toggle/' + postid)

    def post_object(self, obj, path=""):
        """Creates a POST request to the API with the provided JSON object.

        Client can include an (optional) an API route to post to."""
        signed_obj = self.sign_obj(obj)
        res = r.post(self.url + path, data=json.dumps(signed_obj))

        return res

    def upload_img(self, filename):
        """Upload an image to the API"""
        #with open(filename, 'rb') as f:
        #    img = f.read()

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
        """Sign the object (with a nonce) and return a dict for the query"""
        nonce = self.get_nonce()
        if obj is '':
            sig = self.crypto.sign_blob(nonce)
            json_obj = json.dumps([]).encode('utf-8')
        else:
            json_obj = json.dumps(obj).encode('utf-8')
            sig = self.crypto.sign_blob(nonce + json_obj)

        signed_obj = {"Payload": b64.standard_b64encode(json_obj).decode('ASCII'),
                      "Nonce": b64.standard_b64encode(nonce).decode('ASCII'),
                      "Sig": sig}

        return signed_obj
