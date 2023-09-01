from abc import ABC, abstractmethod
import pandas as pd

class FinanceDataPostprocessor(ABC):
    @abstractmethod
    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
