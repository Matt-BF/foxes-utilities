from flask import (
    Blueprint,
    render_template,
    url_for,
    flash,
    send_from_directory,
    request,
    redirect,
    after_this_request,
)
import os
import glob
from threading import Thread
from flask_app import app
from flask_app.scripts import auto_recebimentos

from flask_app.scripts.analyze_covid import consolidate, analyze_csv
from flask_app.scripts.auto_worklab_chrome import async_auto_laudo

covid_bp = Blueprint("covid_bp", __name__, template_folder="templates")
covid_table_bp = Blueprint("covid_table_bp", __name__, template_folder="templates")


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
            flash("Adicione um arquivo", "alert-danger")
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


@covid_table_bp.route("/extras/covid/<table_file>_<kind>", methods=["GET", "POST"])
def covid_result(table_file, kind):
    try:
        consolidated_table = consolidate(
            os.path.join(app.config["UPLOAD_FOLDER"], table_file), kind=kind
        )
        cols = consolidated_table[1]
        consolidated_table = consolidated_table[0]
        
        if request.method == "POST":
            table = analyze_csv(os.path.join(app.config["UPLOAD_FOLDER"], table_file))
            try:
                Thread(target=async_auto_laudo,args=(app,table, os.path.join(app.config["UPLOAD_FOLDER"], "chromedriver"))).start()
                flash("Sua placa está sendo laudada no worklab, verifique lá o andamento dos laudos", "alert-success")
            except Exception as e:
                flash(f"Houve algum erro durante o laudo: {e}", "alert-danger")

        return render_template(
            "results.html",
            table_file_name=table_file,
            table=consolidated_table,
            cols=cols,
        )
    except Exception:
        flash("Sua placa está fora dos padrões, favor reveja", "alert-danger")
        return redirect(url_for("covid_bp.covid"))

@covid_bp.route("/extras/receivals", methods=["GET","POST"])
def receivals():
    pngs = glob.glob(app.config["UPLOAD_FOLDER"] + "/*.png") + glob.glob(app.config["UPLOAD_FOLDER"] + "/*.zip")
    for png in pngs:
        try:
            os.remove(png)
        except FileNotFoundError:
            pass

    if request.method == "POST":
        try:
            form_data = request.form.to_dict()
            date = "".join(form_data["data"].split("-")[::-1][0:2])
            auto_recebimentos.fetch_receivals(form_data["planilha"], date)
            auto_recebimentos.zip_pngs(date)
            return(send_from_directory(app.config["UPLOAD_FOLDER"], f"{date}.zip", as_attachment=True))

        except Exception as e:
            print(e)
            flash(f"Erro: {e}", "alert-danger")
            return(redirect(url_for("covid_bp.receivals")))

    return render_template("receivals.html")