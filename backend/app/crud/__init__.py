"""
CRUD operations package.
"""
from .chart import chart as _chart
from .interpretation import interpretation as _interpretation
from .base import CRUDBase

class _Crud:
    chart = _chart
    interpretation = _interpretation

crud = _Crud()

__all__ = ["crud", "CRUDBase"]