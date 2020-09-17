from flask_app import app
from flask import render_template
import json


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html", error=error), 500
