from util.crypto import Crypto
from util.interface import APICaller

c = APICaller(url="http://localhost:8080/")
print(c.upload_img('asdf.svg'))
