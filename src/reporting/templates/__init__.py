"""
Rapor şablonları
"""
from .base_template import BaseReport
from .data_analysis_template import DataAnalysisReport
from .custom_template import CustomReport

__all__ = ['BaseReport', 'DataAnalysisReport', 'CustomReport']