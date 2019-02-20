from app import app
from flask_wtf.csrf import CSRFProtect
import instagram_api
import instagram_web

if __name__ == '__main__':
    app.run()
