"""
Dataset exporter module for saving generated real DS-CDMA tensors in NumPy .npz format.
"""

from typing import Dict, Any, Union
from pathlib import Path
import numpy as np


def save_dataset(data: Dict[str, Any], filepath: Union[str, Path]) -> Path:
    """
    Saves generated dataset dictionary to a compressed .npz file.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        path,
        tensor=data['tensor'],
        A_true=data['A_true'],
        C_true=data['C_true'],
        S_true=data['S_true'],
        antenna_pos=data['antenna_pos'],
        user_pos=data['user_pos'],
        rank_R=data['rank_R'],
    )
    return path


def load_dataset(filepath: Union[str, Path]) -> Dict[str, Any]:
    """
    Loads a dataset dictionary from a .npz file.
    """
    path = Path(filepath)
    with np.load(path) as loaded:
        return {
            'tensor': loaded['tensor'],
            'A_true': loaded['A_true'],
            'C_true': loaded['C_true'],
            'S_true': loaded['S_true'],
            'antenna_pos': loaded['antenna_pos'],
            'user_pos': loaded['user_pos'],
            'rank_R': int(loaded['rank_R']),
        }
