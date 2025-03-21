import datetime

import pandas as pd

from ..configs.config import config, logger
from ..utils.model import GPTIntentions, IntentionList
from ..utils.prompt import PROMPT
from ..utils.utils import FileManager, GPTIntentionProcessor


def load_data(path):
    """Load data from a xlsx file"""
    logger.info(f"Loading data from {path}")
    return pd.read_excel(path)


def filter_data(
    df: pd.DataFrame,
    base: str,
):
    """Filter data by column and value"""
    df = df.query(
        f"PRODUCTO != '' & PRODUCTO != 0 & CANAL_ORIGEN == 'Clientes'" # MESA == '{config.BASES[base]}' & 
    )
    logger.info(f"Filtered data by {base}")
    return df


def train_model(df: pd.DataFrame, base: str):
    """Train a model"""
    model = GPTIntentions(pydantic_object=IntentionList, prompt=PROMPT)
    processor = GPTIntentionProcessor(model, batch_size=100) # el batch_size es el número de descripciones que se envían al modelo en cada iteración
    processor.process_batches(
        df, description_column="DESCRIPCION", column_category="MOTIVO", save_interval=50 # el save_interval es el intervalo en el que se guardan los resultados parciales
    )
    df = processor.generate_output_dataframe(df)
    logger.info(f"Trained model for {base}, processed {len(df)} rows")
    return df


def save_results(df: pd.DataFrame, base: str, mes: str, path: str = "./results"):
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    full_path = f"{path}/{base}_{mes}_{date}.xlsx"
    logger.info(f"Saving results to {full_path}")
    FileManager.save_to_excel(df, full_path)
    return full_path


def root_flow(base: str, mes: str, df):
    df_filtered = filter_data(df, base)
    df_concat = train_model(df_filtered, base)
    file_path = save_results(df_concat, base, mes)
    return df_concat, file_path
