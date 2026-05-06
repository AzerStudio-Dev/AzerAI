"""
AzerAI - Azərbaycan Dilində Qabaqcıl Səsli AI Asistent
Plugin Əsaslı, Çoxdilli AI Asistent Framework
"""
from .azerai import Assistant
from .plugins import get_all_tools, get_plugin_info, get_plugin_prompts, get_plugin_updates

__all__ = [
    "Assistant",
    "get_all_tools", 
    "get_plugin_info",
    "get_plugin_prompts",
    "get_plugin_updates"
]
