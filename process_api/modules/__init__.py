from process_api.modules.condition import ConditionModule
from process_api.modules.console import ConsoleModule
from process_api.modules.loop import LoopModule
from process_api.modules.switch import SwitchModule
from process_api.modules.system import SystemModule


def register(api):
    ConditionModule.register(api)
    ConsoleModule.register(api)
    LoopModule.register(api)
    SwitchModule.register(api)
    SystemModule.register(api)
