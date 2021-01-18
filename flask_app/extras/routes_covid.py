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
from flask_app.worker import celery

from flask_app import app
from flask_app.scripts.auto_recebimentos import zip_pdfs
from flask_app.scripts.analyze_covid import consolidate, analyze_csv
from flask_app.scripts.auto_worklab_chrome import auto_laudo
from flask_app.scripts.pdf_extract import separate_laudos
from flask_app.scripts.notifica import parse_day_runs, compare_day_laudos, send_mail

covid_bp = Blueprint("covid_bp", __name__, template_folder="templates")


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
                url_for("covid_bp.covid_result", table_file=filename, kind=kind)
            )

    return render_template("covid.html")


@covid_bp.route("/extras/covid/<table_file>_<kind>", methods=["GET", "POST"])
def covid_result(table_file, kind):
    try:
        consolidated_table = consolidate(
            os.path.join(app.config["UPLOAD_FOLDER"], table_file), kind=kind
        )
        cols = consolidated_table[1]
        consolidated_table = consolidated_table[0]

        if request.method == "POST":
            table_name = os.path.join(app.config["UPLOAD_FOLDER"], table_file)

            # Start a Celery task and send user to the results page
            task = celery.send_task(
                "tasks.start_auto_laudo", args=[table_name], kwargs={},
            )

            return redirect(url_for("covid_bp.submission_complete", task_id=task.id))

        return render_template(
            "results.html",
            table_file_name=table_file,
            table=consolidated_table,
            cols=cols,
        )
    except Exception:
        flash("Sua placa está fora dos padrões, favor reveja", "alert-danger")
        return redirect(url_for("covid_bp.covid"))


@covid_bp.route("/extras/receivals", methods=["GET", "POST"])
def receivals():
    pngs = glob.glob(app.config["UPLOAD_FOLDER"] + "/*.png") + glob.glob(
        app.config["UPLOAD_FOLDER"] + "/*.zip"
    )
    for png in pngs:
        try:
            os.remove(png)
        except FileNotFoundError:
            pass

    if request.method == "POST":
        try:
            form_data = request.form.to_dict()
            date = "".join(form_data["data"].split("-")[::-1][0:2])
            save_folder = app.config["UPLOAD_FOLDER"]
            task = celery.send_task(
                "tasks.start_fetch_receivals",
                args=[form_data["planilha"], date, save_folder],
                kwargs={},
            )

            return redirect(
                url_for("covid_bp.png_download", task_id=task.id, date=date)
            )

        except Exception as e:
            flash(f"Erro: {e}", "alert-danger")
            return redirect(url_for("covid_bp.receivals"))

    return render_template("receivals.html")


@covid_bp.route("/extras/notify", methods=["GET", "POST"])
def notify():
    if request.method == "POST":
        try:
            form_data = request.form.to_dict()
            date = "".join(form_data["data"].split("-")[::-1][0:2])
            nums = parse_day_runs(form_data["planilha"], date)
            laudos = compare_day_laudos(form_data["worklab_table"], nums)
            flash("Email enviado para a vigilância", "alert-success")
            return send_mail(laudos, form_data["data"])

        except Exception as e:
            flash(f"Erro: {e}", "alert-danger")
            return redirect(url_for("covid_bp.notify"))

    return render_template("notify.html")


@covid_bp.route("/extras/pdf_extract", methods=["GET", "POST"])
def pdf_route():
    pdfs = glob.glob(app.config["UPLOAD_FOLDER"] + "/*.pdf")
    for pdf in pdfs:
        try:
            os.remove(pdf)
        except FileNotFoundError:
            pass
    try:
        os.remove(app.config["UPLOAD_FOLDER"] + "/laudos.zip")
    except FileNotFoundError:
        pass

    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("Adicione um arquivo", "alert-danger")
            return redirect(url_for("covid_bp.pdf_route"))
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file", "alert-danger")
            return redirect(url_for("covid_bp.pdf_route"))

        if "pdf" not in file.filename:
            flash("Adicione um arquivo pdf", "alert-danger")
            return redirect(url_for("covid_bp.pdf_route"))

        if file and "pdf" in file.filename:
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            try:
                separate_laudos(file_path)
                os.remove(file_path)
                zip_pdfs(app.config["UPLOAD_FOLDER"])
                return send_from_directory(
                    app.config["UPLOAD_FOLDER"], "laudos.zip", as_attachment=True
                )
            except Exception as e:
                flash(f"Há algo de errado com o seu PDF: {e}", "alert-danger")

    return render_template("pdf_divide.html")


## celery views after submission
@covid_bp.route("/extras/submission_complete_<task_id>", methods=["GET"])
def submission_complete(task_id):
    status = celery.AsyncResult(task_id).status
    error = None
    if status == "FAILURE":
        try:
            error = celery.AsyncResult(task_id).get()
        except Exception as e:
            error = e

    return render_template("submission.html", status=status, error=error)

@covid_bp.route("/extras/pngs_<task_id>_<date>", methods=["GET"])
def png_download(task_id, date):
    status = celery.AsyncResult(task_id).status
    error = None
    if status == "SUCCESS":
        return send_from_directory(
            app.config["UPLOAD_FOLDER"], f"{date}.zip", as_attachment=True)
    else:
        try:
            error = celery.AsyncResult(task_id).get()
        except Exception as e:
            error = e

    return render_template("png_download.html", status=status, error=error)