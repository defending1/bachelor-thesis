"""
CP Tensor Factorization dataclass and container object.
"""

from typing import Tuple, List, Optional, Union, Any
import numpy as np


class CP:
    """
    Encapsulates CP tensor factorization state, including input tensor, rank, factor matrices,
    weights, reconstruction error, and fitting parameters.

    Attributes:
        tensor (Optional[np.ndarray]): Target tensor being decomposed.
        rank (Optional[int]): CP decomposition rank R.
        factors (Optional[List[np.ndarray]]): List of factor matrices [A, B, C, ...].
        weights (Optional[np.ndarray]): Component weights if normalized.
        rec_error (Optional[float]): Relative reconstruction error ||T - T_rec||_F / ||T||_F.
        runtime (Optional[float]): Total fitting runtime in seconds.
    """

    def __init__(
        self,
        tensor: Optional[np.ndarray] = None,
        rank: Optional[int] = None,
        factors: Optional[Union[Tuple[np.ndarray, ...], List[np.ndarray]]] = None,
        weights: Optional[np.ndarray] = None,
        rec_error: Optional[float] = None,
        runtime: Optional[float] = None,
    ):
        self.tensor = tensor
        self.rank = rank
        self.factors = list(factors) if factors is not None else None
        self.weights = weights
        self.rec_error = rec_error
        self.runtime = runtime

    @property
    def A(self) -> Optional[np.ndarray]:
        """First mode factor matrix (Mode 0)."""
        return self.factors[0] if (self.factors and len(self.factors) > 0) else None

    @A.setter
    def A(self, val: np.ndarray) -> None:
        if self.factors is None:
            self.factors = [val]
        else:
            self.factors[0] = val

    @property
    def B(self) -> Optional[np.ndarray]:
        """Second mode factor matrix (Mode 1)."""
        return self.factors[1] if (self.factors and len(self.factors) > 1) else None

    @B.setter
    def B(self, val: np.ndarray) -> None:
        if self.factors is None:
            self.factors = [None, val]
        elif len(self.factors) == 1:
            self.factors.append(val)
        else:
            self.factors[1] = val

    @property
    def C(self) -> Optional[np.ndarray]:
        """Third mode factor matrix (Mode 2) or Code matrix for 3D tensors."""
        if self.factors is None:
            return None
        if len(self.factors) == 2:
            return self.factors[1]
        return self.factors[2] if len(self.factors) > 2 else None

    @C.setter
    def C(self, val: np.ndarray) -> None:
        if self.factors is None or len(self.factors) < 2:
            raise IndexError("Cannot set C on factors list with fewer than 2 elements.")
        if len(self.factors) == 2:
            self.factors[1] = val
        else:
            self.factors[2] = val

    @property
    def S(self) -> Optional[np.ndarray]:
        """Mode 2 / Signal matrix for 3D DS-CDMA tensors."""
        return self.factors[2] if (self.factors and len(self.factors) > 2) else None

    @S.setter
    def S(self, val: np.ndarray) -> None:
        if self.factors is None or len(self.factors) < 3:
            raise IndexError("Cannot set S on factors list with fewer than 3 elements.")
        self.factors[2] = val

    def compute(
        self,
        tensor: Optional[np.ndarray] = None,
        rank: Optional[int] = None,
        nonnegative: bool = False,
        n_iter_max: int = 2000,
        tol: float = 1e-9,
        random_state: Optional[int] = 42,
        restore_physical_scale: bool = False,
        n_restarts: int = 10,
        **kwargs,
    ) -> "CP":
        """
        Fits CP decomposition on target tensor using standard ALS or non-negative CP-ALS.

        Args:
            tensor (Optional[np.ndarray]): Target tensor. Uses self.tensor if None.
            rank (Optional[int]): CP rank R. Uses self.rank if None.
            nonnegative (bool): If True, runs solve_nonnegative_cp_als; otherwise solve_cp_als.
            n_iter_max (int): Max ALS iterations.
            tol (float): Convergence tolerance.
            random_state (Optional[int]): Base random seed.
            restore_physical_scale (bool): Transfer mode scale for 3D physical tensors.
            n_restarts (int): Number of initialization restarts.

        Returns:
            CP: Self instance with populated factors, rec_error, and runtime.
        """
        from .als import solve_cp_als, solve_nonnegative_cp_als

        target_tensor = tensor if tensor is not None else self.tensor
        target_rank = rank if rank is not None else self.rank

        if target_tensor is None:
            raise ValueError("No tensor provided for CP computation.")
        if target_rank is None:
            raise ValueError("No rank provided for CP computation.")

        self.tensor = target_tensor
        self.rank = target_rank

        if nonnegative:
            cp_res = solve_nonnegative_cp_als(
                tensor=target_tensor,
                rank=target_rank,
                n_iter_max=n_iter_max,
                tol=tol,
                n_restarts=n_restarts,
                random_state=random_state,
                **kwargs,
            )
        else:
            cp_res = solve_cp_als(
                tensor=target_tensor,
                rank=target_rank,
                n_iter_max=n_iter_max,
                tol=tol,
                random_state=random_state,
                restore_physical_scale=restore_physical_scale,
                n_restarts=n_restarts,
                **kwargs,
            )

        self.factors = cp_res.factors
        self.weights = cp_res.weights
        self.rec_error = cp_res.rec_error
        self.runtime = cp_res.runtime
        return self

    def reconstruct(self) -> np.ndarray:
        """
        Reconstructs dense tensor from CP factors and weights using TensorLy's cp_to_tensor.

        Returns:
            np.ndarray: Reconstructed dense tensor.
        """
        if self.factors is None:
            raise ValueError("Cannot reconstruct tensor: CP factors are None.")

        import tensorly as tl
        reconstructed = tl.cp_to_tensor((self.weights, self.factors))
        if self.tensor is None:
            self.tensor = reconstructed
        return reconstructed

    def __iter__(self):
        """Allows tuple unpacking: (factors, rec_err) = cp"""
        return iter((tuple(self.factors) if self.factors else (), self.rec_error))

    def __repr__(self) -> str:
        shape_str = f"shape={self.tensor.shape}" if self.tensor is not None else "tensor=None"
        err_str = f"{self.rec_error:.6e}" if self.rec_error is not None else "None"
        return f"<CP rank={self.rank}, {shape_str}, rec_error={err_str}>"
