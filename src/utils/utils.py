import logging

import pandas as pd
from tqdm import tqdm

# from model import Intention
from src.utils.model import Intention

# Configuración del logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def change_values(df, column, value, value_to_change):
    df[column] = df[column].replace(value, value_to_change)
    return df


class GPTIntentionProcessor:
    def __init__(
        self, model, batch_size=20, max_attempts=3, partial_path="partial_results.xlsx"
    ):
        self.model = model
        self.batch_size = batch_size
        self.max_attempts = max_attempts
        self.intentions = []
        self.partial_path = partial_path

    def process_batches(
        self,
        df,
        description_column="DESCRIPCION_SOLICITUD",
        column_category="MOTIVO",
        save_interval=None,
    ):
        for i in tqdm(range(0, len(df), self.batch_size), desc="Processing batches"):
            text = self.concat_descriptions(
                df, description_column, column_category, i, i + self.batch_size
            )
            text_size = len(text.split("\n"))
            attempts = 0  # Reinicia los intentos para cada lote

            output = self.get_output_with_retry(text, text_size, attempts)

            if output and len(output.intentions) == text_size:
                self.intentions.append(output.intentions)
            else:
                logging.warning(
                    f"Failed to process batch {i // self.batch_size + 1} after {self.max_attempts} attempts"
                )
                self.intentions.append(
                    [
                        Intention(
                            id=0,
                            category="Categoria no identificada",
                            subcategory="Causa no identificada",
                            reason="Motivo no identificado",
                            probability=0,
                        )
                    ]
                    * text_size
                )

            if (
                save_interval
                and (i * self.batch_size) % (self.batch_size * save_interval) == 0
            ):
                logging.info(
                    f"Saving partial results after processing {i + self.batch_size} rows"
                )
                self.save_partial_results(df, i + self.batch_size)

    def concat_descriptions(self, df, column_descripction, column_category, start, end):
        batch_description = df[column_descripction].iloc[start:end]
        batch_category = df[column_category].iloc[start:end]
        text = [
            f" {num+1}) \t Descripción:'{desc}'"
            for num, (desc, cat) in enumerate(
                zip(batch_description.values, batch_category.values)
            )
        ]
        return "\n".join(text)

    def get_output_with_retry(self, text, text_size, attempts):
        output = None
        while (
            output is None or len(output.intentions) != text_size
        ) and attempts < self.max_attempts:
            try:
                output = self.model.get_intentions(text)
            except Exception as e:
                logging.error(f"Error in batch {attempts + 1}: {str(e)}")
                output = None
            attempts += 1
        return output

    def generate_output_dataframe(self, df):
        oup = [o.category for sublist in self.intentions for o in sublist]
        oup_df = pd.DataFrame(oup, columns=["category"])

        oup = [o.subcategory for sublist in self.intentions for o in sublist]
        oup_df["subcategory"] = oup

        oup = [o.reason for sublist in self.intentions for o in sublist]
        oup_df["reason"] = oup

        assert len(oup_df) == len(df)

        df.reset_index(drop=True, inplace=True)
        oup_df.reset_index(drop=True, inplace=True)
        return pd.concat([df, oup_df], axis=1)

    def generate_output_partial(self, df, end):
        partial_category = [o.category for sublist in self.intentions for o in sublist]
        partial_category = partial_category[:end]

        partial_subcategory = [o.subcategory for sublist in self.intentions for o in sublist]
        partial_subcategory = partial_subcategory[:end]

        partial_reason = [o.reason for sublist in self.intentions for o in sublist]
        partial_reason = partial_reason[:end]

        partial_df = df.iloc[:end].copy()
        partial_df.reset_index(drop=True, inplace=True)
        oup_df = pd.DataFrame(partial_category, columns=["category"])
        oup_df["subcategory"] = partial_subcategory
        oup_df["reason"] = partial_reason

        oup_df.reset_index(drop=True, inplace=True)
        return pd.concat([partial_df, oup_df], axis=1)

    def save_partial_results(self, df, end):
        partial_df = self.generate_output_partial(df, end)
        partial_df.to_excel(self.partial_path, index=False)
        logging.info(f"Partial results saved to {self.partial_path}")


class FileManager:
    @staticmethod
    def save_to_excel(df, file_path):
        df.to_excel(file_path, index=False)
        logging.info(f"DataFrame saved to {file_path}")
