import pandas as pd


def analyze_csv(plate_csv, drop=False, kind="384"):
    df = pd.read_csv(plate_csv, skiprows=range(19))

    df = df.set_index("Sample")
    df = df[["Well", "Target", "Cq"]]

    df["Wells"] = df.index.map(lambda x: " ".join(df.loc[x, "Well"].values))

    a = pd.pivot_table(df, values="Cq", index="Sample", columns="Target", dropna=drop)
    a["Wells"] = df["Wells"].drop_duplicates()

    # add 96 well information
    plate_wells = df.index.map(lambda x: " ".join(df.loc[x, "Well"].values)).unique()
    plate_wells = plate_wells.drop(
        ["A01 A01 A01", "A02 A02 A02"]
    )  # Water and positive control

    if kind == "384":
        rack = "R1-A2 R2-A2 R1-A3 R2-A3 R1-A4 R2-A4 R1-A5 R2-A5 R1-A6 R2-A6 R1-A7 R2-A7 R1-A8 R2-A8 R1-A9 R2-A9 R1-A10 R2-A10 R1-A11 R2-A11 R1-A12 R2-A12 R1-B1 R2-B1 R1-B2 R2-B2 R1-B3 R2-B3 R1-B4 R2-B4 R1-B5 R2-B5 R1-B6 R2-B6 R1-B7 R2-B7 R1-B8 R2-B8 R1-B9 R2-B9 R1-B10 R2-B10 R1-B11 R2-B11 R1-B12 R2-B12 R1-C1 R2-C1 R1-C2 R2-C2 R1-C3 R2-C3 R1-C4 R2-C4 R1-C5 R2-C5 R1-C6 R2-C6 R1-C7 R2-C7 R1-C8 R2-C8 R1-C9 R2-C9 R1-C10 R2-C10 R1-C11 R2-C11 R1-C12 R2-C12 R1-D1 R2-D1 R1-D2 R2-D2 R1-D3 R2-D3 R1-D4 R2-D4 R1-D5 R2-D5 R1-D6 R2-D6 R1-D7 R2-D7 R1-D8 R2-D8 R1-D9 R2-D9 R1-D10 R2-D10 R1-D11 R2-D11 R1-D12 R2-D12 R1-E1 R2-E1 R1-E2 R2-E2 R1-E3 R2-E3 R1-E4 R2-E4 R1-E5 R2-E5 R1-E6 R2-E6 R1-E7 R2-E7 R1-E8 R2-E8 R1-E9 R2-E9 R1-E10 R2-E10 R1-E11 R2-E11 R1-E12 R2-E12 R1-F1 R2-F1 R1-F2 R2-F2 R1-F3 R2-F3 R1-F4 R2-F4 R1-F5 R2-F5 R1-F6 R2-F6 R1-F7 R2-F7 R1-F8 R2-F8 R1-F9 R2-F9 R1-F10 R2-F10 R1-F11 R2-F11 R1-F12 R2-F12 R1-G1 R2-G1 R1-G2 R2-G2 R1-G3 R2-G3 R1-G4 R2-G4 R1-G5 R2-G5 R1-G6 R2-G6 R1-G7 R2-G7 R1-G8 R2-G8 R1-G9 R2-G9 R1-G10 R2-G10 R1-G11 R2-G11 R1-G12 R2-G12 R1-H1 R2-H1 R1-H2 R2-H2 R1-H3 R2-H3 R1-H4 R2-H4 R1-H5 R2-H5 R1-H6 R2-H6 R1-H7 R2-H7 R1-H8 R2-H8 R1-H9 R2-H9 R1-H10 R2-H10 R1-H11 R2-H11 R1-H12 R2-H12 R3-A1 R4-A1 R3-A2 R4-A2 R3-A3 R4-A3 R3-A4 R4-A4 R3-A5 R4-A5 R3-A6 R4-A6 R3-A7 R4-A7 R3-A8 R4-A8 R3-A9 R4-A9 R3-A10 R4-A10 R3-A11 R4-A11 R3-A12 R4-A12 R3-B1 R4-B1 R3-B2 R4-B2 R3-B3 R4-B3 R3-B4 R4-B4 R3-B5 R4-B5 R3-B6 R4-B6 R3-B7 R4-B7 R3-B8 R4-B8 R3-B9 R4-B9 R3-B10 R4-B10 R3-B11 R4-B11 R3-B12 R4-B12 R3-C1 R4-C1 R3-C2 R4-C2 R3-C3 R4-C3 R3-C4 R4-C4 R3-C5 R4-C5 R3-C6 R4-C6 R3-C7 R4-C7 R3-C8 R4-C8 R3-C9 R4-C9 R3-C10 R4-C10 R3-C11 R4-C11 R3-C12 R4-C12 R3-D1 R4-D1 R3-D2 R4-D2 R3-D3 R4-D3 R3-D4 R4-D4 R3-D5 R4-D5 R3-D6 R4-D6 R3-D7 R4-D7 R3-D8 R4-D8 R3-D9 R4-D9 R3-D10 R4-D10 R3-D11 R4-D11 R3-D12 R4-D12 R3-E1 R4-E1 R3-E2 R4-E2 R3-E3 R4-E3 R3-E4 R4-E4 R3-E5 R4-E5 R3-E6 R4-E6 R3-E7 R4-E7 R3-E8 R4-E8 R3-E9 R4-E9 R3-E10 R4-E10 R3-E11 R4-E11 R3-E12 R4-E12 R3-F1 R4-F1 R3-F2 R4-F2 R3-F3 R4-F3 R3-F4 R4-F4 R3-F5 R4-F5 R3-F6 R4-F6 R3-F7 R4-F7 R3-F8 R4-F8 R3-F9 R4-F9 R3-F10 R4-F10 R3-F11 R4-F11 R3-F12 R4-F12 R3-G1 R4-G1 R3-G2 R4-G2 R3-G3 R4-G3 R3-G4 R4-G4 R3-G5 R4-G5 R3-G6 R4-G6 R3-G7 R4-G7 R3-G8 R4-G8 R3-G9 R4-G9 R3-G10 R4-G10 R3-G11 R4-G11 R3-G12 R4-G12 R3-H1 R4-H1 R3-H2 R4-H2 R3-H3 R4-H3 R3-H4 R4-H4 R3-H5 R4-H5 R3-H6 R4-H6 R3-H7 R4-H7 R3-H8 R4-H8 R3-H9 R4-H9 R3-H10 R4-H10 R3-H11 R4-H11 R3-H12 R4-H12".split()

    elif kind == "96":
        rack = "A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 B1 B2 B3 B4 B5 B6 B7 B8 B9 B10 B11 B12 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D12 E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 E11 E12 F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12 G1 G2 G3 G4 G5 G6 G7 G8 G9 G10 G11 G12 H1 H2 H3 H4 H5 H6 H7 H8 H9 H10 H11 H12".split()

    well_rack = dict(zip(rack, plate_wells))

    for idx in a.index:
        for k, v in well_rack.items():
            if a.loc[idx, "Wells"] == v:
                a.loc[idx, "Well_96"] = k

    # positive samples
    pos = a[(a["N1"] < 40) & (a["N2"] < 40)]

    # negative samples
    neg_null = a[(pd.isnull(a["N1"]) & (pd.isnull(a["N2"])) & (a["RP"] < 40))]
    neg_N1 = a[(a["N1"] > 40) & (pd.isnull(a["N2"])) & (a["RP"] < 40)]
    neg_N2 = a[(pd.isnull(a["N1"]) & (a["N2"] > 40) & (a["RP"] < 40))]
    neg_N1_N2 = a[(a["N1"] > 40) & (a["N2"] > 40) & (a["RP"] < 40)]
    neg = pd.concat([neg_null, neg_N1, neg_N2, neg_N1_N2])

    # inconclusive samples
    # N1_inc = a[(a["N1"]<40) & (pd.isnull(a["N2"])) & (pd.isnull(a["RP"]))]
    # N2_inc = a[(pd.isnull(a["N1"])) & (a["N2"]<40) & (pd.isnull(a["RP"]))]
    # N1_RP_inc = a[(a["N1"]<40) & (pd.isnull(a["N2"])) & (a["RP"]<40)]
    # N2_RP_inc = a[(pd.isnull(a["N1"])) & (a["N2"]<40) & (a["RP"]<40)]
    # all_nan_inc = a[(pd.isnull(a["N1"])) & (pd.isnull(a["N2"])) & (pd.isnull(a["RP"]))]
    # inc = pd.concat([N1_inc,N2_inc,N1_RP_inc,N2_RP_inc,all_nan_inc])
    pos_neg = pd.concat([pos, neg])
    inc = a.loc[~a.index.isin(pos_neg.index)]

    return (pos, neg, inc)


def consolidate(plate_csv, kind="384"):
    anal = analyze_csv(plate_csv, kind=kind)
    anal[0]["Result"] = "POSITIVO"
    anal[1]["Result"] = "NEGATIVO"
    anal[2]["Result"] = "INCONCLUSIVO"
    consol = pd.concat([anal[0], anal[1], anal[2]]).sort_values(by="Sample")

    return (
        consol.to_html(
            table_id="my_table",
            classes=[
                "table",
                "table-hover",
                "table-sm",
                "table-bordered",
                "table-striped",
            ],
        ),
        consol.columns,
    )
