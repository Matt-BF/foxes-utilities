import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import six
import sys
import math
import zipfile
import glob
import os
from flask_app import app

def render_mpl_table(
    data,
    col_width=7.0,
    row_height=0.625,
    font_size=10,
    header_color="#40466e",
    row_colors=["#f1f1f2", "w"],
    edge_color="w",
    bbox=[0, 0, 1, 1],
    header_columns=0,
    ax=None,
    **kwargs,
):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array(
            [col_width, row_height]
        )
        fig, ax = plt.subplots(figsize=size)
        ax.axis("off")

    mpl_table = ax.table(
        cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs
    )

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight="bold", color="w")
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    return ax


def fetch_receivals(sheet_name, date):
    # use creds to create a client to interact with the Google Drive API
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(os.getcwd(), "FoxES-cfb72d294a6e.json"), scope
    )
    client = gspread.authorize(creds)
    # print(today)
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheet_name).worksheet(f"Recebimentos {date}")
    df = pd.DataFrame(sheet.get_all_records(default_blank=np.nan))
    labs = set(i.split("-")[0] for i in df.columns)

    for lab in labs:
        col_filter = [i for i in df.columns if i.split("-")[0] == lab]
        lab_df = df[col_filter]
        lab_df = lab_df.dropna(how="all", axis=1)
        if not lab_df.empty:
            num_samples = lab_df.size - sum(lab_df.isna().sum())
            lab_df = lab_df.fillna(0)
            lab_df = lab_df.astype(int)

            df_shape = math.ceil(num_samples / 20)
            lab_df = np.reshape(
                lab_df.melt()["value"].sort_values(ascending=False).values,
                (20, df_shape),
            )
            lab_df = pd.DataFrame(lab_df)
            lab_df.columns = [f"Laboratorio {lab} ({date})"] + [
                "" for _ in lab_df.columns[1:]
            ]

            lab_df.iloc[-1, -1] = f"Recebidas na data: {num_samples}"
            lab_df = lab_df.replace(0, "")

            render_mpl_table(lab_df, header_columns=0)
            plt.savefig(os.path.join(app.config["UPLOAD_FOLDER"],f"{date}_{lab}.png"), dpi=600, bbox_inches="tight")


def zip_pngs(date):
    with zipfile.ZipFile(os.path.join(app.config["UPLOAD_FOLDER"],f"{date}.zip"), "w") as zip:
        for png in glob.glob(os.path.join(app.config["UPLOAD_FOLDER"],f"{date}*.png")):
            zip.write(png, os.path.basename(png))

def zip_pdfs(save_folder):
    with zipfile.ZipFile(os.path.join(app.config["UPLOAD_FOLDER"],f"laudos.zip"), "w") as zip:
        for pdf in glob.glob(os.path.join(app.config["UPLOAD_FOLDER"],"*.pdf")):
            zip.write(pdf, os.path.basename(pdf))