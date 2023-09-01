from finance_data.constants import STANDARD_COLUMNS
from pydantic import BaseModel
import pandas as pd
from postprocessor import Postprocessor

NOTES_COLUMN = 'notes'

class NotesConfig(BaseModel):
    note: dict[str, list[str]]

class WithNotes(Postprocessor):
    def __init__(self, notes_config: NotesConfig):
        self.notes_config = notes_config

    def generate_notes_for_row(self, row: pd.Series) -> str:
        notes = ''
        for note, substrings in self.notes_config.items():
            for substring in substrings:
                if substring.lower() in row[STANDARD_COLUMNS['NAME']].lower():
                    notes += f'{note} '
        return notes

    def add_and_prefill_notes(self, df: pd.DataFrame) -> pd.DataFrame:
        copy = df.copy()
        copy[NOTES_COLUMN] = df.apply(lambda row: self.generate_notes_for_row(row), axis=1)
        return copy

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.add_and_prefill_notes(df)
