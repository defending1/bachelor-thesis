from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union, Dict, Any
import tomllib


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
        dataset_output (str): Output file path for dataset generator.
        plot_output (str): Output file path for localization plot.
        restore_physical_scale (bool): Whether to restore physical scale during CP-ALS.
    """

    num_sources: int = 3  # R
    num_antennas: int = 4  # I
    spreading_gain: int = 16  # J
    num_symbols: int = 100  # K
    area_side: float = 100.0
    min_dist: float = 0.1
    seed: Optional[int] = None
    dataset_output: str = "dscdma_dataset.npz"
    plot_output: str = "antenna_localization_plot.pdf"
    restore_physical_scale: bool = True

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

    @classmethod
    def from_toml(cls, path: Optional[Union[str, Path]] = None) -> "SimConfig":
        """
        Loads configuration from a .toml file.
        If path is None, defaults to package configuration 'experiments/dscdma/config.toml'.
        """
        target_path: Optional[Path] = None

        if path is not None:
            target_path = Path(path)
            if not target_path.exists():
                raise FileNotFoundError(f"Config file not found at: {target_path.resolve()}")
        else:
            pkg_config = Path(__file__).parent / "config.toml"
            if pkg_config.exists():
                target_path = pkg_config
            else:
                config = cls()
                config.validate()
                return config

        with open(target_path, "rb") as f:
            data = tomllib.load(f)

        cfg_dict: Dict[str, Any] = data.get("dscdma", data)

        if "seed" in cfg_dict:
            val = cfg_dict["seed"]
            if val is None or (
                isinstance(val, str) and val.lower() in ("none", "null", "random", "")
            ):
                cfg_dict["seed"] = None
            elif isinstance(val, (int, str)):
                cfg_dict["seed"] = int(val)

        fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in cfg_dict.items() if k in fields}

        config = cls(**filtered)
        config.validate()
        return config

