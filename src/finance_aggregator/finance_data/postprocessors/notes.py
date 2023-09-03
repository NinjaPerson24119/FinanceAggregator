from finance_aggregator.finance_data.constants import STANDARD_COLUMNS
import pandas as pd
from finance_aggregator.finance_data.postprocessors.postprocessor import Postprocessor

NOTES_COLUMN = "notes"
NotesConfig = dict[str, list[str]]


class WithNotes(Postprocessor):
    def __init__(self, notes_config: NotesConfig):
        self.notes_config = notes_config

    def generate_notes_for_row(self, row: pd.Series) -> str:
        notes = ""
        for note, substrings in self.notes_config.items():
            for substring in substrings:
                if substring.lower() in row[STANDARD_COLUMNS["NAME"]].lower():
                    notes += f"{note} "
        return notes

    def add_and_prefill_notes(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        copy = df.copy()
        copy[NOTES_COLUMN] = copy.apply(
            lambda row: self.generate_notes_for_row(row), axis=1
        )
        return copy

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.add_and_prefill_notes(df)
