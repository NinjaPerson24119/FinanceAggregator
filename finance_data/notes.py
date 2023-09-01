from finance_data.finance_data import FinanceData
from finance_data import STANDARD_COLUMNS
from pydantic import BaseModel
import pandas as pd

NOTES_COLUMN = 'notes'

class NotesConfig(BaseModel):
    note: dict[str, list[str]]

class FinanceDataWithNotes(FinanceData):
    def __init__(self, finance_data: FinanceData, notes_config: NotesConfig):
        self.finance_data = finance_data
        self.notes_config = notes_config

    def generate_notes_for_row(self, row: pd.Series) -> str:
        notes = ''
        for note, substrings in self.notes_config.items():
            for substring in substrings:
                if substring.lower() in row[STANDARD_COLUMNS['NAME']].lower():
                    notes += f'{note} '
        return notes

    def add_and_prefill_notes(self):
        self.df[NOTES_COLUMN] = self.df.apply(lambda row: self.generate_notes_for_row(row), axis=1)

    def postprocess(self):
        super().postprocess()
        self.add_and_prefill_notes()
