import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = os.environ.get('http://{}.s3.amazonaws.com/'.format(S3_BUCKET))
    DEBUG = True
    PORT = 5000


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

class AWSBucket(Config):
    
    SECRET_KEY = os.urandom(32)
    DEBUG = True
    PORT = 5000
