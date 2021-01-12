from docxtpl import DocxTemplate
from datetime import datetime
import pandas as pd
import os


def make_orcamento(contents):

    contents["Total"] = 0
    for item in contents["tbl_contents"]:
        item["total"] = int(item.get("number")) * float(item.get("price"))
        contents["Total"] += item["total"]

    contents["Date"] = datetime.strftime(datetime.today().date(), "%d/%m/%Y")

    target_file = os.path.join(os.getcwd(), "orcamento.docx")

    template = DocxTemplate(
        os.path.join(os.getcwd(), "flask_app/uploads/orcamento_template.docx")
    )

    template.render(contents)
    template.save(target_file)

    return target_file
