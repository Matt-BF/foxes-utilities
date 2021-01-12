import os
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "19486b6b76667a65561a91e7fb95f136"
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "flask_app/uploads")


# extras blueprints
from flask_app.extras.routes_covid import covid_bp
from flask_app.extras.routes_orcamentos import orcamentos_bp

app.register_blueprint(covid_bp)
app.register_blueprint(orcamentos_bp)

from flask_app import routes