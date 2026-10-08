from importlib import import_module
from typing import Any

from omniroboagent.backends.skills.base import SkillBackend
from omniroboagent.backends.skills.registry import (
    SkillBackendRegistry,
    create_skill_backend,
    register_skill_backend,
    skill_backend_registry,
)

_EXPORTS = {
    "LiberoPi05PolicyBackend": (
        "omniroboagent.backends.skills.pi05_libero",
        "LiberoPi05PolicyBackend",
    ),
    "LanguageSkillBackend": (
        "omniroboagent.backends.skills.language",
        "LanguageSkillBackend",
    ),
    "LocalPolicyBackend": (
        "omniroboagent.backends.skills.local",
        "LocalPolicyBackend",
    ),
    "OpenPIRoboCasaPolicyBackend": (
        "omniroboagent.backends.skills.openpi",
        "OpenPIRoboCasaPolicyBackend",
    ),
    "OpenPIWebSocketPolicyBackend": (
        "omniroboagent.backends.skills.openpi",
        "OpenPIWebSocketPolicyBackend",
    ),
    "RLDXRemotePolicyBackend": (
        "omniroboagent.backends.skills.rldx",
        "RLDXRemotePolicyBackend",
    ),
    "XR1LocalPolicyBackend": (
        "omniroboagent.backends.skills.xiaomi",
        "XiaomiRobotics1VLAPolicyBackend",
    ),
    "XR1RemotePolicyBackend": (
        "omniroboagent.backends.skills.xiaomi_remote",
        "XiaomiRemotePolicyBackend",
    ),
    "XiaomiRobotics1VLAPolicyBackend": (
        "omniroboagent.backends.skills.xiaomi",
        "XiaomiRobotics1VLAPolicyBackend",
    ),
    "XiaomiRemotePolicyBackend": (
        "omniroboagent.backends.skills.xiaomi_remote",
        "XiaomiRemotePolicyBackend",
    ),
}


def __getattr__(name: str) -> Any:
    try:
        module_name, attribute = _EXPORTS[name]
    except KeyError as error:
        raise AttributeError(name) from error
    value = getattr(import_module(module_name), attribute)
    globals()[name] = value
    return value


__all__ = [
    "LiberoPi05PolicyBackend",
    "LanguageSkillBackend",
    "LocalPolicyBackend",
    "OpenPIRoboCasaPolicyBackend",
    "OpenPIWebSocketPolicyBackend",
    "RLDXRemotePolicyBackend",
    "XR1LocalPolicyBackend",
    "XR1RemotePolicyBackend",
    "XiaomiRobotics1VLAPolicyBackend",
    "XiaomiRemotePolicyBackend",
    "SkillBackend",
    "SkillBackendRegistry",
    "create_skill_backend",
    "register_skill_backend",
    "skill_backend_registry",
]
