import os
from contextlib import contextmanager
from typing import Any, Optional

import numpy as np
import pandas as pd

from keyencelib.ljv7 import (EstablishCommunication, GetProfileAdvance,
                             TerminateCommunication)


class Profiler:
    """Class for continuous profile measurement.

    Parameters
    ----------
    savedir : str, optional
        The directory for saving profiles. If None, profiles are not saved.
    """
    def __init__(self, savedir: Optional[str] = None) -> None:
        self.savedir = savedir
        self.csvname = 'profile_history.csv'

    @contextmanager
    def open(self) -> None:
        """Connect to equipment and enable measurement."""
        try:
            EstablishCommunication()
            yield
        finally:
            TerminateCommunication()

    def get(self, tag: Any = None) -> np.ndarray:
        """Get the current profile and save it.

        Parameters
        ----------
            tag: Any, optional
                Tag name when saved.
        """
        vec = GetProfileAdvance()

        if self.savedir is not None:
            tag = tag if tag is not None else ''
            self._save(vec, tag)
        return vec

    def _save(self, vec: np.ndarray, tag: str) -> None:
        os.makedirs(self.savedir, exist_ok=True)
        path = os.path.join(self.savedir, self.csvname)
        columns = ['tag']+[str(i) for i in range(vec.shape[0])]
        if os.path.exists(path):
            mode, header = 'a', False
        else:
            mode, header = 'w', True

        pd.DataFrame(
            np.atleast_2d(np.append(tag, vec)), columns=columns).to_csv(
                path, mode=mode, header=header, index=False)
