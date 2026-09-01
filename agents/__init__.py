"""
Multi-Agent Package for AutoOne Automotive Platform
"""
from .orchestrator import run_multi_agent_system
from .marketing import MARKETING_PROMPT
from .doctor_auto import DOCTOR_AUTO_PROMPT
from .booking import BOOKING_PROMPT

__all__ = ['run_multi_agent_system', 'MARKETING_PROMPT', 'DOCTOR_AUTO_PROMPT', 'BOOKING_PROMPT']
