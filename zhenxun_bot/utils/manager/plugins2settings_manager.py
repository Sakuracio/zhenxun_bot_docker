from typing import List, Optional, Union, Tuple
from .data_class import StaticData
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


class Plugins2settingsManager(StaticData):
    """
    插件命令阻塞 管理器
    """

    def __init__(self, file: Path):
        self.file = file
        super().__init__(None)
        if file.exists():
            with open(file, "r", encoding="utf8") as f:
                self._data = yaml.load(f)
        if "PluginSettings" in self._data.keys():
            self._data = (
                self._data["PluginSettings"] if self._data["PluginSettings"] else {}
            )

    def add_plugin_settings(
        self,
        plugin: str,
        cmd: Optional[List[str]] = None,
        default_status: Optional[bool] = True,
        level: Optional[int] = 5,
        limit_superuser: Optional[bool] = False,
        plugin_type: Tuple[Union[str, int]] = ("normal",),
        data_dict: Optional[dict] = None,
    ):
        """
        添加一个插件设置
        :param plugin: 插件模块名称
        :param cmd: 命令 或 命令别名
        :param default_status: 默认开关状态
        :param level: 功能权限等级
        :param limit_superuser: 功能状态是否限制超级用户
        :param plugin_type: 插件类型
        :param data_dict: 封装好的字典数据
        """
        if data_dict:
            level = data_dict.get("level") if data_dict.get("level") is not None else 5
            default_status = (
                data_dict.get("default_status")
                if data_dict.get("default_status") is not None
                else True
            )
            limit_superuser = (
                data_dict.get("limit_superuser")
                if data_dict.get("limit_superuser") is not None
                else False
            )
            cmd = data_dict.get("cmd") if data_dict.get("cmd") is not None else []
        self._data[plugin] = {
            "level": level if level is not None else 5,
            "default_status": default_status if default_status is not None else True,
            "limit_superuser": limit_superuser
            if limit_superuser is not None
            else False,
            "cmd": cmd,
            "plugin_type": list(
                plugin_type if plugin_type is not None else ("normal",)
            ),
        }

    def get_plugin_data(self, module: str) -> dict:
        """
        通过模块名获取数据
        :param module: 模块名称
        """
        if self._data.get(module) is not None:
            return self._data.get(module)
        return {}

    def get_plugin_module(
        self, cmd: str, is_all: bool = False
    ) -> Union[str, List[str]]:
        """
        根据 cmd 获取功能 module
        :param cmd: 命令
        :param is_all: 获取全部包含cmd的模块
        """
        keys = []
        for key in self._data.keys():
            if cmd in self._data[key]["cmd"]:
                if is_all:
                    keys.append(key)
                else:
                    return key
        return keys

    def reload(self):
        """
        重载本地数据
        """
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                self._data: dict = yaml.load(f)
                self._data = self._data["PluginSettings"]
