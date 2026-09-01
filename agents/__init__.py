"""
Multi-Agent Package for AutoOne Automotive Platform
"""
from .orchestrator import process_user_request
from .marketing import MARKETING_SYSTEM_PROMPT
from .doctor_auto import DOCTOR_AUTO_SYSTEM_PROMPT
from .booking import BOOKING_SYSTEM_PROMPT

__all__ = ['process_user_request', 'MARKETING_SYSTEM_PROMPT', 'DOCTOR_AUTO_SYSTEM_PROMPT', 'BOOKING_SYSTEM_PROMPT']
