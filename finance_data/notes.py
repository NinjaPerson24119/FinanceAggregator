from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS

class FinanceDataWithNotes(FinanceDataBase):
    NOTES_COLUMN = 'notes'

    def __init__(self, finance_data, notes_config):
        self.finance_data = finance_data
        self.notes_config = notes_config

    def prefill_notes_column(self):
        # TODO
        with open(os.path.join(config_dir, notes_prefill_filename), 'r') as f:
            c = json.load(f)
    
        def notes_row(in_row):
            notes_cell = ''
            for note in c[EXTENDED_COLUMNS['NOTES']]:
                for substring in c[EXTENDED_COLUMNS['NOTES']][note]:
                    if substring.lower() in in_row[STANDARD_COLUMNS['NAME']].lower():
                        notes_cell += f'{note} '
            return notes_cell
        self.df[EXTENDED_COLUMNS['NOTES']] = self.df.apply(lambda row: notes_row(row), axis=1)
