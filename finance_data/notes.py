from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS
from pydantic import BaseModel
import pandas as pd

class NotesConfig(BaseModel):
    note: dict[str, list[str]]

class FinanceDataWithNotes(FinanceDataBase):
    NOTES_COLUMN = 'notes'

    def __init__(self, finance_data: FinanceDataBase, notes_config: NotesConfig):
        self.finance_data = finance_data
        self.notes_config = notes_config

    def generate_notes_for_row(self, row: pd.Series):
        notes = ''
        for note, substrings in self.notes_config.items():
            for substring in substrings:
                if substring.lower() in row[STANDARD_COLUMNS['NAME']].lower():
                    notes += f'{note} '
        return notes

    def add_and_prefill_notes(self):
        self.df[self.NOTES_COLUMN] = self.df.apply(lambda row: self.generate_notes_for_row(row), axis=1)

    def postprocess(self):
        super().postprocess()
        self.add_and_prefill_notes()
