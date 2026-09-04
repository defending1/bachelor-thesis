# Experiments Project

Unified repository for tensor decomposition experiments and applications:
1. **DS-CDMA** (`experiments.dscdma`): 3D spatial tensor synthesis & CP-ALS signal recovery.
2. **Tensor Data EEM** (`experiments.tensor_data_eem`): EEM Fluorescence Spectroscopy Non-Negative CP decomposition.
3. **Typical Rank** (`experiments.typical_rank`): Typical rank distribution estimation of random tensors.

## Shared Utilities
The project includes shared CP decomposition tools under `experiments.utils.cp`:
- `metrics`: Relative reconstruction error and tensor norm calculations.
- `als`: Standard CP-ALS and Non-Negative CP-ALS solvers powered by TensorLy.
- `alignment`: Greedy column factor alignment based on cosine similarity.

## Getting Started
Run tests or execution commands using `uv`:
```bash
uv sync
uv run pytest
uv run dscdma-generator [config.toml]
uv run dscdma-plot [config.toml]
uv run eem-experiment
uv run typical-rank-experiment
```

