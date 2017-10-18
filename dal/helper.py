import pyotp


def validate_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)
