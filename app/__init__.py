import os
from flask import Flask
from flask_cors import CORS

# Initialize application
app = Flask(__name__)

# Enabling cors
CORS(app)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Import the application views
from app import views

# Register blue prints
from app.home.views import home
app.register_blueprint(home)

from app.model.views import model
app.register_blueprint(model)


