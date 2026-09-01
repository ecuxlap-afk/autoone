"""
Chief Orchestrator Agent (المدير والمشرف العام لـ جار الله أوتو)
Executes REAL Sequential Inter-Agent Consultations:
1. Orchestrator opens boardroom meeting using HIS private memory.
2. Doctor Auto responds using HIS private technical memory.
3. Marketing Agent reads Doctor's input and responds using HIS private customer memory.
4. Booking Agent reads Doctor's + Marketing's inputs and responds using HIS private operational memory.
"""
import requests
from .memory import get_private_memory, record_private_memory
from .doctor_auto import talk_to_doctor_office, consult_doctor_for_boardroom
from .marketing import talk_to_marketing_office, consult_marketing_for_boardroom
from .booking import talk_to_booking_office, consult_booking_for_boardroom

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

ORCHESTRATOR_SYSTEM_PROMPT = """أنت المشرف العام والمدير التنفيذي لورشة "جار الله أوتو".

في اجتماعات مجلس الإدارة:
- أنت تترأس اجتماع الطاولة المستديرة مع المالك ورؤساء الأقسام (د. سيارات، مسؤول التسويق، مدير المواعيد).
- افتح الاجتماع بكلمة موجزة ومباشرة، ووجه الأسئلة أو المهام لرؤساء الأقسام بأسمائهم للحفاظ على حيوية وتفاعل النقاش."""

def handle_hq_room_chat(api_key, room, messages):
    if room == 'doctor_auto':
        return talk_to_doctor_office(api_key, messages)
    elif room == 'marketing':
        return talk_to_marketing_office(api_key, messages)
    elif room == 'booking':
        return talk_to_booking_office(api_key, messages)
    elif room == 'orchestrator':
        return talk_to_private_orchestrator(api_key, messages)
    else:
        # Real Sequential Multi-Agent Inter-Discussion Boardroom Pipeline
        return run_real_inter_agent_boardroom(api_key, messages)

def talk_to_private_orchestrator(api_key, messages):
    private_mem = get_private_memory('orchestrator')
    latest_msg = messages[-1]['content'] if messages else ""
    record_private_memory('orchestrator', 'user', latest_msg)

    prompt_messages = [{'role': 'system', 'content': ORCHESTRATOR_SYSTEM_PROMPT}]
    for m in private_mem[-6:]:
        prompt_messages.append(m)
    prompt_messages.append({'role': 'user', 'content': latest_msg})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        res = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': prompt_messages, 'temperature': 0.3, 'max_tokens': 1000}, headers=headers, timeout=30)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            record_private_memory('orchestrator', 'assistant', content)
            return content
        return "أهلاً سعادة الرئيس في مكتب المدير العام."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"

def run_real_inter_agent_boardroom(api_key, messages):
    """
    TRUE Sequential Multi-Agent Inter-Agent Discussion:
    1. Orchestrator opens the boardroom using Orchestrator Private Memory.
    2. Doctor Auto executes via HIS Private Memory -> generates technical consultation.
    3. Marketing Agent executes via HIS Private Memory -> reads Doctor's consultation & generates marketing response.
    4. Booking Agent executes via HIS Private Memory -> reads Doctor's + Marketing's inputs & generates booking response.
    """
    boss_query = messages[-1]['content'] if messages else "افتتاح اجتماع العمل لتوزيع المهام واستماع التوجيهات"

    # Step 1: Orchestrator Opening
    orch_private_mem = get_private_memory('orchestrator')
    record_private_memory('orchestrator', 'user', boss_query)

    orch_prompt = [{'role': 'system', 'content': ORCHESTRATOR_SYSTEM_PROMPT}]
    for m in orch_private_mem[-4:]:
        orch_prompt.append(m)
    orch_prompt.append({'role': 'user', 'content': f"توجيه المالك والرئيس التنفيذي: '{boss_query}'. افتح النقاش باختصار وواقعية وبدون أرقام وهمية لفتح المجال لباقي رؤساء الأقسام."})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    orch_opening = "أهلاً بك يا سعادة الرئيس في اجتماع مجلس الإدارة. افتتحنا النقاش لمتابعة توجيهاتك السديدة مع رؤساء الأقسام."
    try:
        res1 = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': orch_prompt, 'temperature': 0.3, 'max_tokens': 400}, headers=headers, timeout=30)
        if res1.status_code == 200:
            orch_opening = res1.json()['choices'][0]['message']['content']
            record_private_memory('orchestrator', 'assistant', orch_opening)
    except Exception:
        pass

    # Step 2: Real Consultation Call to Doctor Auto Agent (Private Memory)
    doctor_reply = consult_doctor_for_boardroom(api_key, boss_query)

    # Step 3: Real Consultation Call to Marketing Agent (Private Memory + Reading Doctor Auto's Reply!)
    marketing_reply = consult_marketing_for_boardroom(api_key, boss_query, doctor_reply)

    # Step 4: Real Consultation Call to Booking Agent (Private Memory + Reading Doctor's & Marketing's Replies!)
    booking_reply = consult_booking_for_boardroom(api_key, boss_query, doctor_reply, marketing_reply)

    # Return clean, separate agent response objects
    return [
        {
            'icon': '👔',
            'title': 'المشرف العام (افتتاح النقاش وإدارة الاجتماع)',
            'content': orch_opening
        },
        {
            'icon': '🩺',
            'title': 'د. سيارات (رئيس القسم التقني والفحص)',
            'content': doctor_reply
        },
        {
            'icon': '📢',
            'title': 'مسؤول التسويق وخدمة العملاء (استماع واستجابة تقنية)',
            'content': marketing_reply
        },
        {
            'icon': '📅',
            'title': 'مدير المواعيد والعمليات (التنظيم والتنسيق التشغيلي)',
            'content': booking_reply
        }
    ]
