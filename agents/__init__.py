"""
Multi-Agent Package for AutoOne Enterprise Virtual HQ Platform
"""
from .orchestrator import handle_hq_room_chat
from .marketing import MARKETING_SYSTEM_PROMPT
from .doctor_auto import DOCTOR_AUTO_SYSTEM_PROMPT
from .booking import BOOKING_SYSTEM_PROMPT

__all__ = ['handle_hq_room_chat', 'MARKETING_SYSTEM_PROMPT', 'DOCTOR_AUTO_SYSTEM_PROMPT', 'BOOKING_SYSTEM_PROMPT']
