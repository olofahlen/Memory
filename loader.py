import pathlib

import pandas as pd

from constants import NAMES


def read_words(name: NAMES) -> None:
    folder = pathlib.Path(name)
    out = (
        pd.concat(
            [
                pd.read_csv(file, header=None).squeeze(axis=1)
                for file in folder.glob("*.csv")
            ]
        )
        .sort_values()
        .reset_index(drop=True)
        .rename(name)
    )
    return out
