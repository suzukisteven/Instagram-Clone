import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    DEBUG = True
    PORT = 5000

    # App Secret
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    # Amazon AWS S3 Bucket
    S3_BUCKET = os.environ.get("S3_BUCKET")
    S3_KEY = os.environ.get("S3_KEY")
    S3_SECRET = os.environ.get("S3_SECRET")
    S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"
    
    # Braintree
    BT_ENVIRONMENT = os.environ.get("BT_ENVIRONMENT")
    BT_MERCHANT_ID = os.environ.get("BT_MERCHANT_ID")
    BT_PUBLIC_KEY = os.environ.get("BT_PUBLIC_KEY")
    BT_PRIVATE_KEY = os.environ.get("BT_PRIVATE_KEY")

    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
