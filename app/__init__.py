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
from app.docs.views import docs
app.register_blueprint(docs)

from app.predictions.views import predictions
app.register_blueprint(predictions)


