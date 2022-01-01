from pathlib import Path
from ruamel.yaml import YAML
from utils.manager import plugins_manager
from utils.utils import get_matchers
import nonebot

try:
    import ujson as json
except ModuleNotFoundError:
    import json


_yaml = YAML(typ="safe")


def init_plugins_data(data_path):
    """
    初始化插件数据信息
    """
    plugin2data_file = Path(data_path) / "manager" / "plugin_manager.json"
    plugin2data_file.parent.mkdir(parents=True, exist_ok=True)
    _data = {}
    if plugin2data_file.exists():
        _data = json.load(open(plugin2data_file, "r", encoding="utf8"))
    _matchers = get_matchers()
    for matcher in _matchers:
        _plugin = nonebot.plugin.get_plugin(matcher.module)
        try:
            _module = _plugin.module
        except AttributeError:
            if matcher.module not in _data.keys():
                plugins_manager.add_plugin_data(
                    matcher.module, matcher.module, error=True
                )
            else:
                plugins_manager.set_module_data(matcher.module, "error", True)
                plugin_data = plugins_manager.get(matcher.module)
                if plugin_data:
                    plugins_manager.set_module_data(
                        matcher.module, "version", plugin_data.get("version")
                    )
        else:
            try:
                plugin_version = _module.__getattribute__("__plugin_version__")
            except AttributeError:
                plugin_version = None
            try:
                plugin_name = _module.__getattribute__("__zx_plugin_name__")
            except AttributeError:
                plugin_name = matcher.module
            try:
                plugin_author = _module.__getattribute__("__plugin_author__")
            except AttributeError:
                plugin_author = None
            if matcher.module in plugins_manager.keys():
                plugins_manager.set_module_data(matcher.module, "error", False)
            if matcher.module not in plugins_manager.keys():
                plugins_manager.add_plugin_data(
                    matcher.module,
                    plugin_name=plugin_name,
                    author=plugin_author,
                    version=plugin_version,
                )
            elif plugins_manager[matcher.module]["version"] is None or (
                plugin_version is not None
                and plugin_version > plugins_manager[matcher.module]["version"]
            ):
                plugins_manager.set_module_data(
                    matcher.module, "plugin_name", plugin_name
                )
                plugins_manager.set_module_data(matcher.module, "author", plugin_author)
                plugins_manager.set_module_data(
                    matcher.module, "version", plugin_version
                )
            if matcher.module in _data.keys():
                plugins_manager.set_module_data(
                    matcher.module, "error", _data[matcher.module]["error"]
                )
                plugins_manager.set_module_data(
                    matcher.module, "plugin_name", _data[matcher.module]["plugin_name"]
                )
    plugins_manager.save()
