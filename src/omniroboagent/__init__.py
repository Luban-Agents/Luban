"""OmniRoboAgent public package."""

from importlib import import_module
from typing import Any

_EXPORTS = {
    "DefaultAgent": ("omniroboagent.agent_core", "DefaultAgent"),
    "DirectPipeline": ("omniroboagent.pipelines", "DirectPipeline"),
    "SelfEvolvingAgent": ("omniroboagent.agent_core", "SelfEvolvingAgent"),
    "SyncRuntime": ("omniroboagent.runtimes", "SyncRuntime"),
}


def __getattr__(name: str) -> Any:
    try:
        module_name, attribute = _EXPORTS[name]
    except KeyError as error:
        raise AttributeError(name) from error
    value = getattr(import_module(module_name), attribute)
    globals()[name] = value
    return value


__all__ = ["DefaultAgent", "DirectPipeline", "SelfEvolvingAgent", "SyncRuntime"]
