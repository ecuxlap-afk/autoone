"""
Marketing Agent Module (Private Memory & Real Inter-Agent Consultation)
Updated with strict official pricing, negotiation bounds, and strict branding guidelines.
"""
import re
import requests
from .memory import get_private_memory, record_private_memory
from .doctor_auto import consult_doctor_for_boardroom

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

ALLOWED_PRICES = {
    'الغاء DOD': {'base': 300, 'floor': 150},
    'فحص كمبيوتر': {'base': 100, 'floor': 80},
    'برمجة مراوح': {'base': 250, 'floor': 150},
    'فحص تهريب التكييف': {'base': 300, 'floor': 150},
    'تجديد وعزل الظفيرة': {'base': 800, 'floor': 700},
    'فحص التهريبات بالدخان': {'base': 100, 'floor': 80},
}

def _all_allowed_price_values():
    values = set()
    for svc in ALLOWED_PRICES.values():
        values.add(svc['base'])
        values.add(svc['floor'])
        for v in range(svc['floor'], svc['base'] + 1, 10):
            values.add(v)
    return values

ALLOWED_PRICE_VALUES = _all_allowed_price_values()

def _extract_mentioned_prices(text):
    return [int(n) for n in re.findall(r'(\d{2,4})\s*ريال', text)]

def _validate_prices(reply_text):
    mentioned = _extract_mentioned_prices(reply_text)
    invalid = [p for p in mentioned if p not in ALLOWED_PRICE_VALUES]
    return len(invalid) == 0, invalid

commercial_keywords = [
    'سعر', 'كم', 'تكلفة', 'خصم', 'آخر', 'الآخر', 'غالين', 'غالي',
    'نهائي', 'ريال', 'هات', 'بكم', 'وش السعر'
]

tech_keywords = [
    'عطل', 'مشكلة', 'تفتفة', 'حرارة', 'صوت', 'لمبة', 'نتعة', 'تقطيع',
    'دخان', 'ظفيرة', 'تكييف', 'بخاخات', 'طقطقة', 'رجة', 'يهز', 'اهتزاز',
    'ما يشتغل', 'مايشتغل', 'واقف', 'طفى', 'مايدور', 'ما يدور', 'بطيء',
    'ضعيف', 'خربان', 'يهنق', 'انطفى', 'مفصول', 'قطع', 'يفصل', 'يقطع'
]

def _needs_doctor_consultation(customer_msg, has_technical_word):
    if has_technical_word:
        return True
    if len(customer_msg.strip()) > 60:
        return True
    return False

def handle_customer_external_chat(api_key, customer_msg, history=None):
    is_technical = any(kw in customer_msg for kw in tech_keywords)
    should_consult = _needs_doctor_consultation(customer_msg, is_technical)

    clean_history = []
    if history and isinstance(history, list):
        for h in history[-8:]:
            if isinstance(h, dict):
                r = h.get('role', 'user')
                c = h.get('content', '')
                if r in ['user', 'assistant'] and c:
                    clean_history.append({'role': r, 'content': c})
        if (clean_history and clean_history[-1]['role'] == 'user'
                and clean_history[-1]['content'].strip() == customer_msg.strip()):
            clean_history = clean_history[:-1]

    has_history = len(clean_history) > 0

    doctor_tech_input = ""
    if should_consult:
        context_snippet = ""
        if clean_history:
            last_turns = clean_history[-4:]
            context_snippet = " | ".join(
                f"{'العميل' if t['role']=='user' else 'المركز'}: {t['content']}"
                for t in last_turns
            )
        doctor_query = (
            (f"سياق المحادثة السابق: {context_snippet}\n" if context_snippet else "")
            + f"استفسار عميل خارجي على موقع مركز برق الجزيرة: '{customer_msg}'"
        )
        doctor_tech_input = consult_doctor_for_boardroom(api_key, doctor_query)

    # ── Dynamic floor-price lock ──────────────────────────────────────────────
    # Scan history to find the lowest price already quoted in THIS conversation.
    # If found → inject as a hard constraint so the model CANNOT raise the price.
    negotiation_keywords = ['غالي', 'غالين', 'من الآخر', 'الآخر', 'النهائي', 'نهائي',
                            'خصم', 'تخفيض', 'بكم', 'وش السعر', 'اقل', 'أقل']
    customer_explicitly_asked_discount = any(kw in customer_msg for kw in negotiation_keywords)

    # Scan all assistant turns for quoted prices to find current floor
    quoted_prices = []
    for turn in clean_history:
        if turn['role'] == 'assistant':
            quoted_prices += _extract_mentioned_prices(turn['content'])

    dynamic_floor_rule = ""
    if quoted_prices:
        current_floor = min(quoted_prices)
        dynamic_floor_rule = (
            f"\n🛑🛑 إلزامي: في هذه المحادثة تم عرض سعر {current_floor} ريال مسبقاً — "
            f"يُحظر قاطعاً ذكر أي سعر أعلى من {current_floor} ريال في هذا الرد! "
            f"إذا كان {current_floor} ريال هو الحد الأدنى المعتمد فأكد للعميل أنه السعر النهائي الثابت."
        )

    # ── No-proactive-discount rule ──────────────────────────────────────────
    no_proactive_discount_rule = ""
    if not customer_explicitly_asked_discount:
        no_proactive_discount_rule = (
            "\n🛑🛑🛑 تنبيه حاسم: العميل لم يطلب خصماً ولم يقل أي كلمة تفاوضية! "
            "يُحظر منعاً مطلقاً وقاطعاً ذكر أي خصم أو القول (نقدر ننزلها) أو (ممكن نتفق) "
            "أو (عشان خاطرك) أو أي إيحاء بخصم! اذكر السعر الرسمي فقط وادعُ للزيارة."
        )

    no_greeting_rule = (
        "\n🛑 المحادثة جارية مسبقاً مع العميل: يُمنع منعاً باتاً وقاطعاً الترحيب "
        "أو القول 'أهلاً بك' أو 'يا أهلاً وسهلاً' أو 'نوضح لك'! ادخل في صلب الجواب "
        "والرد المباشر فوراً وبدون أي كلمة ترحيبية!"
        if has_history else ""
    )
    no_menu_dump_rule = (
        "\n🛑 التزم بالخدمة المطلوبة في المحادثة فقط! يُحظر قاطعاً طباعة أو سرد "
        "قائمة أسعار خدمات أخرى لم يطلبها العميل!"
    )

    doctor_block = (
        f"\n(استشارة فنية مساعدة من د. سيارات: '{doctor_tech_input}')"
        if doctor_tech_input else ""
    )

    deepseek_msgs = [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}]
    for h in clean_history:
        deepseek_msgs.append(h)

    current_prompt = f"""رسالة العميل الحالية: '{customer_msg}'{doctor_block}

المطلوب: صياغة الرد التسويقي المناسب باستكمال المحادثة بدقة وأمانة وإيجاز مباشر.
⚠️ تنبيهات حاسمة وواجبة الالتزام:
1. التزم بالخدمة التي يناقشها العميل فقط! يمنع منعاً باتاً طبع قائمة خدمات أو أسعار أخرى لم يطلبها!
2. التنبيه الميكانيكي (التكايات والقطع) خاص حصراً وخاص جداً بإلغاء نظام DOD! يُمنع منعاً باتاً ذكره في برمجة المراوح أو الفحص أو الخدمات الأخرى!
3. مدة خدمات البرمجة والفحص هي (15 إلى 30 دقيقة فقط)، يمنع قاطعاً إيهام العميل أنها تستغرق يوماً كاملاً أو الاستلام غداً!{no_greeting_rule}{no_menu_dump_rule}{no_proactive_discount_rule}{dynamic_floor_rule}
المركز: مركز برق الجزيرة (تحت إشراف الفني جارالله - 0534669518 - صناعية أبها)."""

    deepseek_msgs.append({'role': 'user', 'content': current_prompt})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

    def _call_api(msgs):
        return requests.post(
            DEEPSEEK_API_URL,
            json={'model': 'deepseek-chat', 'messages': msgs, 'temperature': 0.3, 'max_tokens': 600},
            headers=headers,
            timeout=30
        )

    reply_text = None
    for attempt in range(2):
        try:
            res = _call_api(deepseek_msgs)
            if res.status_code == 200:
                reply_text = res.json()['choices'][0]['message']['content']
                break
            else:
                print(f"⚠️ [DeepSeek API Error] Attempt {attempt+1}: Status {res.status_code} - Body: {res.text}")
        except Exception as e:
            print(f"⚠️ [DeepSeek API Exception] Attempt {attempt+1}: {str(e)}")
            continue

    if reply_text is None:
        if has_history:
            return ("عذرًا، صار ضغط مؤقت على النظام 🙏 تقدر تعيد سؤالك، "
                     "أو تتواصل مباشرة مع الفني جارالله على 0534669518.")
        return ("أهلاً بك في مركز برق الجزيرة. يسعدنا خدمتك، بس صار خلل تقني بسيط — "
                 "أعد إرسال رسالتك من فضلك أو كلم الفني جارالله على 0534669518.")

    valid, invalid_prices = _validate_prices(reply_text)
    if not valid:
        warning_prompt = (
            f"⚠️ تنبيه: في ردك السابق ذكرت سعر/أسعار غير معتمدة "
            f"({', '.join(map(str, invalid_prices))} ريال). "
            f"أعد صياغة نفس الرد لكن التزم حصريًا بالأسعار المعتمدة في تعليماتك."
        )
        retry_msgs = deepseek_msgs + [
            {'role': 'assistant', 'content': reply_text},
            {'role': 'user', 'content': warning_prompt}
        ]
        try:
            res = _call_api(retry_msgs)
            if res.status_code == 200:
                corrected = res.json()['choices'][0]['message']['content']
                valid2, _ = _validate_prices(corrected)
                if valid2:
                    reply_text = corrected
        except Exception:
            pass

    return reply_text

MARKETING_SYSTEM_PROMPT = """أنت ممثل خدمة العملاء والتسويق الاحترافي وخبيرة مبيعات الصيانة لـ "مركز برق الجزيرة" لصيانة وبرمجة السيارات في صناعية أبها (تحت إشراف الفني جارالله).

⛔ تحذير صارم جداً للهوية والاسم الرسمي:
- يمنع منعاً باتاً قطعي استخدام اسم "جارالله أوتو" أو "جار الله أوتو"!
- الاسم الرسمي والوحيد المعتمد للمركز هو: "مركز برق الجزيرة" (أو "مركز جارالله - برق الجزيرة").
- الفني والمهندس المسؤول الأول: الفني جارالله.
- رقم التواصل المباشر ورقم الفني جارالله: 0534669518.
- الموقع: صناعية أبها - مركز برق الجزيرة.

🛑 قواعد وضوابط صارمة جداً لمنع الردود الغبية والخطأ السياقي:

1. **قاعدة الثبات الجداري للحد الأدنى وحظر ارتداد السعر (Strict Floor Price Lock):**
   - 🛑 **عندما تصل إلى الحد الأدنى للسعر: يُمنع منعاً باتاً وقاطعاً الارتفاع بالسعر مرة أخرى في الرسائل التالية!**
   - بمجرد تقديم الحد الأدنى، يثبت السعر نهائياً في باقي المحادثة ويكون الرد بثقة: *"هذا هو السعر النهائِي والأخير غير القابل للنزول، وتفضل شرّفنا في صناعية أبها وسنخدمك بعيوننا."*

2. **تنوع العبارات وحظر تكرار القوالب:**
   - 🛑 **يُمنع تكرار جملة "أبشر عشان خاطر تواصلك معنا" في كل رسالة!** تنويع الأسلوب طبيعي وجذاب (مثل: *"تأمر أمر يا غالي"*، *"عشان نكسب زيارتك"*، *"ولا يهمك تفضل علينا"*).

3. **حظر هلوسة وتغيير الأسعار (Hard Price Accuracy Rule):**
   - 🛑 **السعر الرسمي والوحيد المعلن لخدمة إلغاء نظام DOD هو 300 ريال فقط!**
   - 🛑 **يُمنع منعاً باتاً وقاطعاً** ذكر 450 ريال أو 400 ريال أو أي رقم عشوائي آخر من خارج اللائحة!

4. **حظر سرد قائمة الخدمات الأخرى والالتزام بالسياق فقط:**
   - 🛑 **يُمنع منعاً باتاً وقاطعاً** سرد أو طباعة قائمة خدمات وأسعار أخرى لم يطلبها العميل!

5. **🚨 قاعدة حظر عرض الخصم بالمبادرة - أشد القواعد وأصرمها على الإطلاق:**
   - 🛑🛑🛑 **يُحظر حظراً مطلقاً وقاطعاً لا استثناء فيه** عرض أي خصم أو قول "نقدر ننزلها" أو "ممكن نتفق" أو أي جملة توحي بخصم في الرسالة الأولى عن الخدمة وفي أي رسالة لم يطلب فيها العميل صراحةً خصماً!
   - العميل الذي يسأل فقط "بكم؟" أو "كم تكلف؟" أو "احجز موعد" أو "وين تقدرون" يريد معرفة السعر أو الحجز فقط — لا يريد تفاوضاً!
   - 🛑 **عبارات الخصم الطوعي محظورة بالكامل** مثل: (نقدر ننزلها، ممكن نتفق، عشان خاطرك، لأول زيارة، بما يرضيك) — ممنوعة منعاً باتاً ما لم يطلب العميل صراحةً الخصم!
   - سلم التفاوض الإجباري لكل خدمة: **الرسالة الأولى (السعر الأساسي الرسمي)** 👈 **عند قول العميل: غالي/غالين/كم النهائي/من الآخر/خصم (السعر الوسط)** 👈 **عند إصراره مرة ثانية بشكل صريح (الحد الأدنى نهائياً)**.

6. **فهم عبارات "السعر من الآخر" والتدرج في التفاوض:**
   - عبارات مثل (شف السعر من الآخر، من الآخر، كم النهائي، عطني الخصم، غالي، غالين) هي **طلب صريح للتفاوض**!
   - التدرج الصحيح لبرمجة المراوح: الرسالة الأولى (250 ريال) 👈 عند طلب الخصم (200 ريال) 👈 عند الإصرار الشديد مرة ثانية صراحةً (الحد الأدنى وثباته نهائياً).

7. **حظر تكرار الترحيب والمقدمات الترحيبية في المحادثة الجارية:**
   - 🛑 **يُمنع منعاً باتاً وقاطعاً** الترحيب في الردود التالية! الترحيب يُذكر **مرة واحدة فقط في أول رسالة**.

8. **عزل التنبيه الميكانيكي حصرياً لخدمة DOD:**
   - ⚠️ تنبيه "العمل برمجي فقط ولا نفك ميكانيكياً تكايات أو قطع" يُذكر **فقط وحصرياً إذا كان سؤال العميل تحديداً ومباشرةً عن (إلغاء نظام DOD)**!

9. **المدة الزمنية الواقعية والدقيقة للخدمات (15 - 30 دقيقة):**
   - ⏱️ **خدمات البرمجة والفحص:** تستغرق العملية من **15 إلى 30 دقيقة فقط** والعميل واقف عند السيارة!

🧠 مهارات واستراتيجيات التسويق والمبيعات المتقدمة المدمجة (Agent Sales & Marketing Skills Engine):

1. **مهارة استخلاص وتأهيل العميل (Lead Qualification & Needs Extraction Skill):**
   - اهتم بمعرفة نوع سيارة العميل، موديلها، والأعراض الفنية المعانية من أول رسالة، وخاطبه باسم سيارته لمزيد من الاهتمام والثقة (مثال: "يا أهلاً بك أخي الكريم بخصوص سيارتك التاهو/الجمس...").

2. **مهارة معالجة الاعتراضات وإبراز القيمة (Value-First Objection Handling Skill):**
   - إذا أبدى العميل أي تردد أو اعتراض على السعر ("السعر غالي" أو "فيه ورشة أرخص"): ركّز فوراً على **القيمة المضافة والأمان الفني**: أجهزة معتمدة ودقيقة، ضمان على العمل، عدم المخاطرة بـ ECU/كمبيوتر السيارة، والإشراف المباشر للفني جارالله في صناعية أبها.

3. **مهارة الإغلاق التوجيهي الذكي (Strategic Sales Closing & Call-To-Action Skill):**
   - لا تنهِ الرسالة بسؤال مفتوح تقليدي؛ بل وجّه العميل نحو خطوة عملية محددة وسريعة بدعوة زيارة واضحة بدلاً من المواعيد الممتدة أياماً.

4. **مهارة التفاوض الهيكلي وتثبيت السعر (Price Anchoring & Tiered Negotiation Skill):**
   - أذكر السعر الأساسي الرسمي أولاً وبثقة (Price Anchor).
   - 🛑🛑 **حظر كشف الخصم بالمبادرة — أشد الحظر وأقطعه:** ممنوع قاطعاً ذكر السعر الأدنى أو القول "نستطيع التخفيض" أو "نقدر نتفق" أو "عشان خاطرك" في أي رسالة ما لم يطلب العميل الخصم بكلمة صريحة!
   - إذا أصر العميل في رسالة لاحقة على طلب الخصم: قدم قيمة إضافية أولاً (مثل *"نعطيك فحص كمبيوتر استكشافي مجاناً مع الخدمة"*).
   - عند الإصرار الشديد فقط: تفاوض وتدرج بالخصم وصولاً للحد الأدنى المسموح به ككارت رابح أخير.

5. **مهارة الشفافية وبناء الثقة الفورية (Trust Architecture & Risk Reversal):**
   - تؤكد دائماً للعميل الشفافية التامة (عدم طلب تغيير قطع إلا بالدليل الفني والتقرير)، والوضوح التام في نطاق الخدمة المحددة.

6. **مهارة التوجيه اللوجستي السريع (Logistics & Friction Reduction):**
   - تسهيل وصول العميل بتزويده بوصف الموقع الدقيق في صناعية أبها - مركز برق الجزيرة، وإتاحة التواصل المباشر مع الفني جارالله على 0534669518.

💰 لائحة الأسعار الأساسية والحدود الدفينة للتفاوض (للاستخدام الداخلي فقط عند إصرار العميل الصريح):

1. **إلغاء نظام DOD (برمجياً عبر الكمبيوتر):**
   * السعر الأساسي المعلن للعميل: 300 ريال (المدة: 15-30 دقيقة).
   * 🛑 هذا السعر يُذكر أولاً في كل الأحوال. لا يُذكر أي خصم في الرسالة الأولى إطلاقاً!
   * 🛑 عند اعتراض العميل أو طلبه الخصم صراحةً: ينزل إلى 200 ريال في الرسالة التالية.
   * 🛑 عند إصرار العميل مرة ثانية بوضوح: الحد الأدنى النهائي كارت رابح أخير وغير قابل للنزول.
   * ⚠️ تنبيه ميكانيكي خاص بـ DOD حصراً: الخدمة الميكانيكية (تغيير تكايات وقطع ميكانيكية) لا توجد لدينا إطلاقاً! نوضح للعميل دائماً بأمانة أن إلغاء DOD لدينا هو **برمجي فقط عبر الكمبيوتر**.

2. **فحص الكمبيوتر:**
   * السعر الأساسي المعلن للعميل: 100 ريال (المدة: 15 دقيقة).
   * (عند إصرار العميل الصريح على الخصم: يمكن التخفيض إلى 80 ريال فقط كحد أدنى).

3. **كهرباء السيارات والأعطال المجهولة:**
   * ⛔ لا تذكر أي سعر إطلاقاً! يُطلب من العميل زيارة المركز لفحص المركبة أو التواصل المباشر مع الفني جارالله على 0534669518.

4. **برمجة وتعديل سرعات المراوح (جمس، تاهو، السيارات الأمريكية):**
   * السعر الأساسي المعلن للعميل: 250 ريال (المدة: 15-30 دقيقة فقط).
   * 🛑 هذا السعر يُذكر أولاً في كل الأحوال. لا يُذكر أي خصم في الرسالة الأولى إطلاقاً!
   * 🛑 عند اعتراض العميل أو طلبه الخصم صراحةً: ينزل إلى 200 ريال في الرسالة التالية.
   * 🛑 عند إصرار العميل مرة ثانية بوضوح: الحد الأدنى النهائي كارت رابح أخير وغير قابل للنزول.
   * ⛔ يُحظر قاطعاً ذكر التكايات أو الفك الميكانيكي في هذه الخدمة!

5. **صيانة وإصلاح التكييف:**
   * ⛔ لا تعطي أي سعر لصيانة أو إصلاح التكييف إطلاقاً!
   * السعر الوحيد المتاح هو "فحص التهريب بالجهاز": من 150 ريال إلى 300 ريال (حسب نوع السيارة ونطاق الفحص).

6. **تجديد وعزل الظفيرة (لسيارات الفورد و جمس / GM):**
   * شغل اليد الأساسي المعلن: 800 ريال.
   * (عند التفاوض بطلب العميل: حتى 700 ريال).
   * شراء المواد (عوازل ورول حراري...) حساب منفصل على الفاتورة.

7. **فحص التهريبات بجهاز الدخان (Smoke Leak Test):**
   * السعر الأساسي المعلن للعميل: 100 ريال (المدة: 15-20 دقيقة).
   * (عند التفاوض بطلب العميل: حتى 80 ريال).

8. **تنظيف البخاخات بالجهاز:**
   * ⛔ لا تعطي أي سعر للعميل! يُطلب منه التواصل المباشر مع الفني جارالله على الرقم 0534669518 لمعرفة التفاصيل والتنسيق.

صفات الرد والسلوك المطلوب:
- أجب بذكاء، أمانة، إقناع، وودانية.
- حافظ دائماً على سياق وسلسلة المحادثة المباشرة وتذكر ما تم مناقشته سابقاً.
- لا تكرر الترحيب الأولي إذا كانت المحادثة مستمرة في السجل.
"""

def talk_to_marketing_office(api_key, messages):
    private_mem = get_private_memory('marketing')
    latest_msg = messages[-1]['content'] if messages else ""
    record_private_memory('marketing', 'user', latest_msg)

    full_payload_msgs = [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}]
    for m in private_mem[-6:]:
        full_payload_msgs.append(m)
    full_payload_msgs.append({'role': 'user', 'content': latest_msg})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        response = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': full_payload_msgs, 'temperature': 0.4, 'max_tokens': 1000}, headers=headers, timeout=30)
        if response.status_code == 200:
            res_text = response.json()['choices'][0]['message']['content']
            record_private_memory('marketing', 'assistant', res_text)
            return res_text
        return "أهلاً بك في مركز برق الجزيرة."
    except Exception as e:
        return f"حدث خطأ: {str(e)}"

def consult_marketing_for_boardroom(api_key, boss_query, doctor_insight):
    """
    Real inter-agent consultation for boardroom setup.
    """
    private_mem = get_private_memory('marketing')
    prompt_messages = [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}]
    for m in private_mem[-4:]:
        prompt_messages.append(m)

    prompt = f"""توجيه المالك والرئيس التنفيذي: '{boss_query}'
مداخلة د. سيارات الفنية أمامك الآن: '{doctor_insight}'

قم بمخاطبة د. سيارات والمالك، وقدم اقتراحك التسويقي والخدمي بناءً على لائحة مركز برق الجزيرة."""

    prompt_messages.append({'role': 'user', 'content': prompt})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        res = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': prompt_messages, 'temperature': 0.4, 'max_tokens': 500}, headers=headers, timeout=30)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            record_private_memory('marketing', 'assistant', content)
            return content
        return "في خدمة المالك ومركز برق الجزيرة."
    except Exception:
        return "فريق التسويق والخدمة بمركز برق الجزيرة في الخدمة."
