"""Handles building input files and namelists."""
import typing as t


def create_namelist(
    title: str, params: t.Optional[t.Dict[str, t.Union[float, str, int]]] = None
) -> str:
    """Creates namelist text string.

    Args:
        title: header of namelist
        params: values to put in

    """
    base = [f"&{title.upper()}"]
    namelist_params = []

    params = params or {}

    for k, v in params.items():
        value_text = None
        if isinstance(v, str):
            value_text = f"'{v}'"
        else:
            value_text = f"{v}"
        namelist_params.append(f"{k} = {value_text}")

    return "\n".join(base + namelist_params + ["/"])
