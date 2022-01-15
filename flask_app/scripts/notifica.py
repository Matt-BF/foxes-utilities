import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

today2 = datetime.today().strftime("%d/%m")
today3 = datetime.today().strftime("%d%m%y")

def parse_day_runs(sheet_name: str, day) -> set:
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "FoxES-cfb72d294a6e.json", scope
    )
    client = gspread.authorize(creds)
    # print(today)
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheet_name).worksheet(f"Rodadas {day}")

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_values()
    flat = set()
    for lst in list_of_hashes:
        for i in lst:
            try:
                flat.add(int(i))
            except ValueError:
                pass

    return flat


def compare_day_laudos(table: str, nums: set) -> pd.DataFrame:
    df = pd.read_csv(table)
    df = df[["Codigo", "Nome", "Resultado"]].dropna()
    df["Nome"] = df["Nome"].apply(lambda x: x.split("Nome: ")[1])
    df["Codigo"] = df["Codigo"].astype(int)
    df["Resultado"] = df["Resultado"].apply(lambda x: x.split(" ,")[0])
    df = df.set_index("Codigo")

    # Filter only nums ran today
    df = df.reindex(nums).dropna()

    return df


def send_mail(df, day2):
    print(f"ENVIANDO EMAIL PARA A VISA", "\n")

    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.starttls()
    smtpObj.login("lab@foxesbm.com", "labfoxestop")
    msg = MIMEMultipart()
    msg["Subject"] = "Notificações Covid-19 - FoxES"
    msg_text = f"""Boa noite,

Segue anexa a lista de exames executados no dia {day2}.
Qualquer dúvida estamos à disposição."""

    msg.attach(MIMEText(msg_text))

    part = MIMEApplication(df.to_csv(), Name=f"{day2}.csv")
    part["Content-Disposition"] = f'attachment; filename="{day2}.csv"'
    msg.attach(part)

    smtpObj.sendmail(
        "lab@foxesbm.com", ["guilherme.borelli@foxesbm.com","paulinia.ve@gmail.com"], msg.as_string()
    )
