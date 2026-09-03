"""
Isolated Private Memory System for Each Agent
Stores private persistent memory and learning logs independently for each agent:
- orchestrator (المشرف العام)
- doctor_auto (دكتور السيارات التقني)
- marketing (مسؤول التسويق)
- booking (مدير المواعيد)
"""

import json
import os
import threading

MEMORY_FILE = 'agents_private_memory.json'
_memory_lock = threading.Lock()

_agent_memories = {
    'orchestrator': [],
    'doctor_auto': [],
    'marketing': [],
    'booking': []
}

def load_memories():
    global _agent_memories
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                _agent_memories = json.load(f)
        except Exception:
            pass

def save_memories():
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(_agent_memories, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def get_private_memory(agent_name, limit=10):
    with _memory_lock:
        load_memories()
        mem = _agent_memories.get(agent_name, [])
        return mem[-limit:]

def record_private_memory(agent_name, role, text):
    with _memory_lock:
        load_memories()
        if agent_name not in _agent_memories:
            _agent_memories[agent_name] = []
        _agent_memories[agent_name].append({
            'role': role,
            'content': text
        })
        _agent_memories[agent_name] = _agent_memories[agent_name][-50:]
        save_memories()

# Initialize on import
load_memories()
