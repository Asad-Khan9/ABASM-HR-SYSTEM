import time
import pyotp
import qrcode
key = "ABASMtestTWOfactorauthentication"



uri = pyotp.totp.TOTP(key).provisioning_uri(name="testuser", issuer_name="test_learning")


qrcode.make(uri).save("tot.png")