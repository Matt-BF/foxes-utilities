import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from flask_app import app
import os

def make_xml(csv):
    df = pd.read_csv(csv)
    df = df.dropna()
    now = datetime.now()
    # Build XML
    # root elements
    root = ET.Element("Registro")
    protocol = ET.SubElement(root, "Protocolo")
    protocol.text = "1"
    id_ = ET.SubElement(root, "ID")
    id_.text = f"{str(now.date()).replace('-','')}_{str(now.time()).replace(':','').replace('.','')}"

    # lote elements
    lote = ET.SubElement(root, "Lote")

    cod_lab = ET.SubElement(lote, "CodLab")
    cod_lab.text = "875"

    cod_lote_lab = ET.SubElement(lote, "CodLoteLab")
    cod_lote_lab.text = id_.text
    data_lote = ET.SubElement(lote, "DataLote")
    data_lote.text = str(now.date())
    hora_lote = ET.SubElement(lote, "HoraLote")
    hora_lote.text = str(now.time()).split(".")[0]

    for idx in df.index:
        # pedido elements
        pedido = ET.SubElement(lote, "Pedido")

        cod_ped_lab = ET.SubElement(pedido, "CodPedLab")
        cod_ped_lab.text = str(idx + 1)
        data_ped = ET.SubElement(pedido, "DataPed")
        data_ped.text = str(now.date())
        hora_ped = ET.SubElement(pedido, "HoraPed")
        hora_ped.text = str(now.time()).split(".")[0]

        paciente = ET.SubElement(pedido, "Paciente")
        #cod_pac_lab = ET.SubElement(paciente, "CodPacLab")
        #cod_pac_lab.text = str(idx + 1)
        nome = ET.SubElement(paciente, "Nome")
        nome.text = df.loc[idx, "Nome"].upper()
        sexo = ET.SubElement(paciente, "Sexo")
        sexo.text = df.loc[idx, "Sexo"].capitalize()
        data_nasc = ET.SubElement(paciente, "DataNasc")
        data_nasc.text = str(
            datetime.strftime(datetime.strptime(df.loc[idx, "Nascimento"], "%d/%m/%Y"), "%Y-%m-%d")
        )
        
        for exam_code in df.loc[idx, "Exames"].split(","):
            exame = ET.SubElement(pedido, "Exame")
            cod_exm_apoio = ET.SubElement(exame, "CodExmApoio")
            cod_exm_apoio.text = f"1543|{exam_code}|1"
            cod_exam_lab = ET.SubElement(exame, "CodExmLab")
            cod_exam_lab.text = f"1543|{exam_code}|1"
            data_coleta = ET.SubElement(exame, "DataColeta")
            data_coleta.text = str(now.date())

    tree = ET.ElementTree(root)
    file_name = f"{str(now.date()).replace('-','')}_arquivo_importacao.xml"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
    tree.write(save_path)
    return file_name