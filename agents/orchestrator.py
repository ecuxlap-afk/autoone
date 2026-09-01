"""
Chief Orchestrator Agent (المدير والمشرف العام على فريق الوكلاء)
Directs requests through independent sub-agent executions:
1. Doctor Auto (Technical Diagnosis Agent)
2. Marketing & Customer Service Agent
3. Booking Agent (Service Scheduling)
"""

from .doctor_auto import get_technical_diagnosis
from .marketing import format_customer_response
from .booking import handle_booking_request

def process_user_request(api_key, messages):
    """
    Real Multi-Agent Pipeline Execution:
    - Extracts the latest user query.
    - Executes Doctor Auto Technical Agent for expert diagnostic analysis.
    - Executes Marketing & Customer Service Agent to format the response warmly for Jarallah Auto.
    - Returns the final combined response.
    """
    if not messages:
        return "أهلاً بك! كيف يمكنني مساعدتك اليوم في صيانة أو برمجة سيارتك؟"

    last_user_message = messages[-1].get('content', '')

    # Step 1: Execute Doctor Auto Technical Agent (إرسال مستقل لدكتور السيارات)
    tech_diagnosis = get_technical_diagnosis(api_key, last_user_message)

    # Step 2: Execute Marketing & Customer Service Agent (إرسال مستقل لوكيل التسويق والخدمة)
    final_response = format_customer_response(api_key, last_user_message, tech_diagnosis)

    # Step 3: Check if booking is mentioned or needed
    if any(keyword in last_user_message for keyword in ['حجز', 'موعد', 'زيارة', 'ورشة', 'فحص', 'أجي', 'أجيكم']):
        booking_info = handle_booking_request(api_key, last_user_message)
        if booking_info:
            final_response += f"\n\n---\n📅 **ترتيب الموعد (خدمة الحجز):**\n{booking_info}"

    return final_response
