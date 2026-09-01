"""
Configuration module for the DS-CDMA simulation framework.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SimConfig:
    """
    Simulation parameters for exact rank-R DS-CDMA tensor generation.

    Attributes:
        num_sources (int): Number of sources/users (R).
        num_antennas (int): Number of receiver antennas (I).
        spreading_gain (int): Length of spreading code per symbol (J).
        num_symbols (int): Number of transmitted real symbols per user (K).
        area_side (float): Side length of 2D bounding area [0, area_side]^2 for positions.
        min_dist (float): Minimum distance lower bound to avoid numerical instability.
        seed (Optional[int]): Random seed for reproducibility.
    """

    num_sources: int = 3  # R
    num_antennas: int = 2  # I
    spreading_gain: int = 16  # J
    num_symbols: int = 100  # K
    area_side: float = 100.0
    min_dist: float = 0.1
    seed: Optional[int] = 42

    def validate(self) -> None:
        """
        Validates the configuration parameters.

        Raises:
            ValueError: If parameters are invalid.
        """
        if self.num_sources <= 0:
            raise ValueError(f"num_sources (R) must be > 0, got {self.num_sources}")
        if self.num_antennas <= 0:
            raise ValueError(f"num_antennas (I) must be > 0, got {self.num_antennas}")
        if self.spreading_gain <= 0:
            raise ValueError(f"spreading_gain (J) must be > 0, got {self.spreading_gain}")
        if self.num_symbols <= 0:
            raise ValueError(f"num_symbols (K) must be > 0, got {self.num_symbols}")
        if self.area_side <= 0:
            raise ValueError(f"area_side must be > 0, got {self.area_side}")
        if self.min_dist <= 0:
            raise ValueError(f"min_dist must be > 0, got {self.min_dist}")
