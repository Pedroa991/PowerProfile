""" Script Vessel Tool - Power Profile """

import os
import pandas as pd
import numpy as np

SCRIPT_VERSION = "V1.0"

COLS_PARSED = {
    "Load": "float",
    "RPM": "float",
    "Total_Fuel": "float",
    "SMH": "float",
    "Asset": "str",
}


def merge_eng_ref(
    df_engine: pd.DataFrame, df_engref_interpolated: pd.DataFrame, param_ref: str
) -> pd.DataFrame:
    """Concatena os dados do motor com os dados do tmi"""
    param_ref_round = f"{param_ref}_round"
    df_engine[param_ref_round] = df_engine[param_ref].round()
    df_merged = df_engine.merge(
        df_engref_interpolated,
        left_on=param_ref_round,
        right_on=param_ref,
        how="left",
        suffixes=["", "_y"],
    )
    df_merged.drop(columns=[param_ref_round, param_ref + "_y"], inplace=True)
    return df_merged


def extraction_eng_data(path_db: str) -> pd.DataFrame:
    """Extrai as informações necessárias para a geração do perfil de potência"""
    cols = list(COLS_PARSED.keys())
    cols.insert(0, "Timestamp")
    df_eng = pd.read_csv(
        path_db + r"\history_output.csv",
        usecols=cols,
        dtype=COLS_PARSED,
        parse_dates=["Timestamp"],
    )
    return df_eng


def interpolation_eng_ref(path_engref: str) -> tuple[pd.DataFrame, str]:
    """Pega os dados do TMI e interpola"""
    df_engref = pd.read_excel(path_engref, sheet_name="TMI REF")
    param_ref = df_engref.columns[0]
    df_engref.set_index(param_ref, inplace=True)
    df_engref_interpolated = pd.DataFrame(
        index=np.arange(df_engref.index.min(), df_engref.index.max(), 1)
    )

    df_engref_interpolated = pd.concat([df_engref, df_engref_interpolated])

    df_engref_interpolated = df_engref_interpolated.sort_index()
    df_engref_interpolated.interpolate(inplace=True)
    df_engref_interpolated = df_engref_interpolated.loc[
        ~df_engref_interpolated.index.duplicated(keep="first")
    ]
    path = os.path.dirname(path_engref) + r"\interpolação.csv"
    df_engref_interpolated.index.name = param_ref
    df_engref_interpolated.to_csv(path)
    df_engref_interpolated.reset_index(inplace=True)
    return df_engref_interpolated, param_ref


def main(path_db: str, path_engref: str) -> None:
    """Função principal"""

    df_engref_interpolated, param_ref = interpolation_eng_ref(path_engref)
    df_engine = extraction_eng_data(path_db)
    df_final = merge_eng_ref(df_engine, df_engref_interpolated, param_ref)
    df_final.to_csv(os.path.dirname(path_engref) + r"\powerprofile.csv", index=False)


if __name__ == "__main__":

    print("Execute o script através da GUI!")

    # Test Mode

    # print("MODO DE TESTE!!!")

    # main(os.getenv("PATH_ENGREF"), os.getenv("PATH_BD"))
