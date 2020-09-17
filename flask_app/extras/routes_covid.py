from flask import (
    Blueprint,
    render_template,
    url_for,
    flash,
    send_file,
    request,
    redirect,
    after_this_request,
)
import os
import glob
from flask_app import app

from .analyze_covid import consolidate


covid_bp = Blueprint("covid_bp", __name__, template_folder="templates")
covid_table_bp = Blueprint("covid_table_bp", __name__, template_folder="templates")


@covid_bp.route("/")
@covid_bp.route("/extras/covid", methods=["GET", "POST"])
def covid():
    csvs = glob.glob(app.config["UPLOAD_FOLDER"] + "/*.csv")
    for csv in csvs:
        try:
            os.remove(csv)
        except FileNotFoundError:
            pass

    if request.method == "POST":
        kind = request.form.to_dict()["plate_type"]
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part", "alert-danger")
            return redirect(url_for("covid_bp.covid"))
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file", "alert-danger")
            return redirect(url_for("covid_bp.covid"))
        if file and "csv" in file.filename:
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            return redirect(
                url_for("covid_table_bp.covid_result", table_file=filename, kind=kind)
            )

    return render_template("covid.html")


@covid_table_bp.route("/extras/covid/<table_file>_<kind>", methods=["GET"])
def covid_result(table_file, kind):
    consolidated_table = consolidate(
        os.path.join(app.config["UPLOAD_FOLDER"], table_file), kind=kind
    )
    cols = consolidated_table[1]
    consolidated_table = consolidated_table[0]

    return render_template(
        "results.html", table_file_name=table_file, table=consolidated_table, cols=cols
    )

