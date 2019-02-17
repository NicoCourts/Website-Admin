"""Handle all the signing/hashing we need"""
import base64 as b64
import rsa

class Crypto:
    """Manages the cryptographic aspects of the project"""
    def __init__(self):
        # Read in private key file
        with open("private.pem", 'rb') as fil:
            keydata = fil.read()
            self.privkey = rsa.PrivateKey.load_pkcs1(keydata)
   
    def sign_blob(self, blob):
        """
        Take in a (binary) blob and sign it. Let the user handle the API call for the nonce.
        
        Parameters:
            blob: A binary blob that is to be signed.
        Returns:
            A hex-encoded string representation of the signature.
        """
        sig = rsa.sign(blob, self.privkey, 'SHA-512')
        return str(b64.standard_b64encode(sig), 'utf-8')
