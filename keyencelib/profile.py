"""Keyence LJV7シリーズによるプロファイル測定プログラム."""

import os
import time
from collections import deque
from contextlib import contextmanager
from threading import Thread
from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

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
        self.monitor = ProfileMonitor()
        self._is_monioring = False
        self._cache = None

    @contextmanager
    def open(self, with_monitor: bool = False) -> None:
        """Connect to equipment and enable measurement.

        Parameters
        ----------
        with_monitor : bool, optional, default to False
            If true, continuous measurement starts and the shape is displayed in
            real-time.
        """
        try:
            EstablishCommunication()
            if with_monitor:
                self._start_monitoring()
            yield
        finally:
            TerminateCommunication()
            if with_monitor:
                self._stop_monitoring()

    def get(self, tag: Any = None) -> np.ndarray:
        """Get the current profile and save it.

        Parameters
        ----------
            tag: Any, optional
                Tag name when saved.
        """
        if self._is_monioring:
            vec = self._cache
        else:
            vec = GetProfileAdvance()

        if self.savedir is not None:
            tag = tag if tag is not None else ''
            self._save(vec, tag)
        return vec

    def _start_monitoring(self) -> None:
        def loop() -> None:
            while self._is_monioring:
                vec = self._cache = GetProfileAdvance()
                self.monitor.plot(vec)

        self.monitor.setup()
        self._thread = Thread(target=loop)
        self._is_monioring = True
        self._thread.start()

    def _stop_monitoring(self) -> None:
        self._is_monioring = False
        self._thread.join()

    def _save(self, vec: np.ndarray, tag: str) -> None:
        os.makedirs(self.savedir, exist_ok=True)
        savepath = os.path.join(self.savedir, self.csvname)
        mode = 'a' if os.path.exists(savepath) else 'w'
        with open(savepath, mode=mode) as file:
            np.savetxt(
                file, np.append(vec, tag),
                header=','.join([str(i) for i in range(vec.shape[0])]+['tag']))


class ProfileMonitor:

    def __init__(self, axis: plt.Axes = None, *args, **kwargs) -> None:
        """Display realtime plotting.

        Parameters
        ----------
        axis : matplotlib.pyplot.Axes, optional
        """
        self.ylim_semirange = 5e4
        self.axis = axis
        self.args = args
        self.kwargs = kwargs
        self._times = deque(maxlen=10)

    def fps(self) -> float:
        """Calculate frames per second (FPS).

        Returns
        -------
        float
            fps
        """
        if self._is_monioring:
            delta = np.diff(self._times)
            return np.mean(len(delta) / delta)

    def setup(self) -> None:
        if self.axis is not None:
            ax = self.axis
        else:
            ax = self.plt.subplot()
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
        self.axis = ax

    def plot(self, vec: np.ndarray) -> None:
        self._times.append(time.perf_counter())
        if self._lines is not None:
            self._lines.remove()

        if len(vec) > 0:
            vecmean = np.mean(vec)
            self._ax.set_ylim(
                vecmean-self.ylim_semirange, vecmean+self.ylim_semirange)
        self._lines, = self._ax.plot(vec, *self.args, **self.kwargs)
        plt.pause(0.001)
