from docxtpl import DocxTemplate
from datetime import datetime
import os
import random


def make_orcamento(contents):

    contents["Total"] = 0
    for item in contents["tbl_contents"]:  # lista de 3 em 3
        item["total"] = int(item.get("num")) * float(item.get("price"))
        contents["Total"] += item["total"]

    contents["Date"] = datetime.strftime(datetime.today().date(), "%d/%m/%Y")
    contents["proposal_number"] = str(random.randrange(0, 999999999))
    date_format = contents["Date"].replace("/", "-")
    target_file = os.path.join(
        os.getcwd(),
        f"flask_app/uploads/FoxES_orcamento_{contents['empresa'].replace(' ','_')}_{date_format}_{contents['proposal_number']}.docx",
    )

    template = DocxTemplate(
        os.path.join(os.getcwd(), "flask_app/uploads/orcamento_template.docx")
    )

    template.render(contents)
    template.save(target_file)

    return target_file
