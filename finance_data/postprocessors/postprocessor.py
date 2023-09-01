from abc import ABC, abstractmethod
import pandas as pd


class Postprocessor(ABC):
    @abstractmethod
    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
