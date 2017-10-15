import os

from flask_api import FlaskAPI
from app import create_app

app = create_app()

# Launch server
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
