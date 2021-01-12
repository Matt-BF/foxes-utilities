from flask import (
    Blueprint,
    render_template,
    url_for,
    flash,
    send_file,
    request,
    redirect,
)
import os
import glob
from flask_app import app
from flask_app.scripts.orcamentos import make_orcamento

orcamentos_bp = Blueprint("orcamentos_bp", __name__, template_folder="templates")


@orcamentos_bp.route("/extras/orcamentos", methods=["GET", "POST"])
def orcamentos():
    orcamentos_list = glob.glob(app.config["UPLOAD_FOLDER"] + "/FoxES_orcamento*.docx")
    if len(orcamentos_list) > 0:
        for orcamento in orcamentos_list:
            os.remove(orcamento)

    if request.method == "POST":
        contents = request.form.to_dict()
        content_items = {}  # dados servicos
        final_data = []
        for k in contents:
            if (
                k.startswith("service_")
                or k.startswith("price_")
                or k.startswith("num_")
            ) and contents[k] != "":
                content_items[k.split("_")[0]] = contents[k]
                if len(content_items) % 3 == 0:
                    final_data.append(content_items)
                    content_items = {}

        contents_final = {"tbl_contents": final_data}
        contents_final["cliente"] = contents["cliente"]
        contents_final["empresa"] = contents["empresa"]
        contents_final["endereco"] = contents.get("endereco", "S/I")
        contents_final["service"] = contents["service"]
        # print(contents_final)
        output_orcamento = make_orcamento(contents_final)
        return send_file(output_orcamento, as_attachment=True)

    return render_template("orcamentos.html")
