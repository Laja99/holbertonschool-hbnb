import os
from app import create_app

config_class = os.getenv("FLASK_CONFIG", "config.DevelopmentConfig")
app = create_app(config_class)

if __name__ == "__main__":
    app.run()
