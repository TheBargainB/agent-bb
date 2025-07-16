"""Promotions research agent module."""

from .config import PromotionsAgentConfig, DEFAULT_PROMOTIONS_CONFIG
from .agent import create_promotions_agent

__all__ = ["create_promotions_agent", "PromotionsAgentConfig", "DEFAULT_PROMOTIONS_CONFIG"] 