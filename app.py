from flask import Flask
from models import init_db
import os

# імпортація BLUEPRINT
from product.routes import product_bp
from auth.routes import auth_bp

app = Flask(__name__)
app.secret_key = '123'
init_db()

# Реєстрація BLUEPRINT
app.register_blueprint(product_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
