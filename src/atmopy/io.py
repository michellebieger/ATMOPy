"""Handles building input files and namelists."""
import typing as t
from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum

import numpy as np
import numpy.typing as npt


def to_fortran_bool(value: bool) -> str:
    """Convert python bool to fortran bool."""
    if value:
        return ".true."
    else:
        return ".false."


def create_namelist(
    title: str, params: t.Optional[t.Dict[str, t.Union[float, str, int, bool]]] = None
) -> str:
    """Creates namelist text string.

    Args:
        title: header of namelist
        params: values to put in

    Returns:
        Namelist format of parameters.

    """
    base = [f"&{title.upper()}"]
    namelist_params = []

    params = params or {}

    for k, v in params.items():
        value_text = None
        if isinstance(v, str):
            value_text = f"'{v}'"
        elif isinstance(v, bool):
            value_text = to_fortran_bool(v)
        else:
            value_text = f"{v}"
        namelist_params.append(f"{k} = {value_text}")

    return "\n".join(base + namelist_params + ["/"])


class ChemistryType(str, Enum):
    """Define chemsitry type."""

    EQUIL = ("eq",)
    NONEQUIL = "noneq"


@dataclass
class ChemistryInputSection:
    """Builds chemistry input."""

    chem: t.Optional[ChemistryType] = ChemistryType.EQUIL

    fcoeff: t.Optional[str] = None
    """NASA polynomial file"""
    fcoeffnine: t.Optional[str] = None
    """NASA 9 polynomial file"""

    element_factor: t.Optional[npt.NDArray[np.float64]] = None  # ele_xfactor

    metallacity: t.Optional[float] = 0.0
    """In log 10 units mate"""

    tfreeze_eq: t.Optional[float] = 0.0

    condenstation_nh3: t.Optional[bool] = False
    condenstation_h2o: t.Optional[bool] = False

    gibbs_step_size: t.Optional[float] = 2

    rainout: t.Optional[bool] = False

    def build_section(self, input_filename: str, output_filename: str) -> str:
        """Build chemistry input into FORTRAN namelist."""
        my_output = asdict(self)

        my_output["fAin"] = input_filename
        my_output = {
            k: v for k, v in my_output.items() if v is not None
        }  # Remove nones

        if self.chem == ChemistryType.EQUIL:
            my_output["fAeqout"] = output_filename
        else:
            my_output["fAneqout"] = output_filename

        mappings = {
            "element_factor": "ele_xfactor",
            "metallicity": "MdH",
            "condenstation_nh3": "cond_NH3",
            "condenstation_h2o": "cond_H2O",
            "gibbs_step_size": "chem_conv",
        }

        my_output = {mappings.get(k, k): v for k, v in my_output.items()}

        return create_namelist("CHEMISTRY", my_output)
