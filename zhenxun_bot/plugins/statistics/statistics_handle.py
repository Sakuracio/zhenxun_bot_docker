from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from models.group_info import GroupInfo
from nonebot.typing import T_State
from pathlib import Path
from configs.path_config import DATA_PATH, IMAGE_PATH
from utils.utils import get_message_text
from utils.image_utils import BuildMat
from utils.message_builder import image
from utils.manager import plugins2settings_manager
import asyncio
import os

try:
    import ujson as json
except ModuleNotFoundError:
    import json


__zx_plugin_name__ = "功能调用统计可视化"
__plugin_usage__ = """
usage：
    功能调用统计可视化
    指令：
        功能调用统计
        日功能调用统计
        周功能调用统计 ?[功能]
        月功能调用统计 ?[功能]
        我的功能调用统计
        我的日功能调用统计 ?[功能]
        我的周功能调用统计 ?[功能]
        我的月功能调用统计 ?[功能]
""".strip()
__plugin_superuser_usage__ = """
usage：
    功能调用统计可视化
    指令：
        全局功能调用统计
        全局日功能调用统计
        全局周功能调用统计 ?[功能]
        全局月功能调用统计 ?[功能]
""".strip()
__plugin_des__ = "功能调用统计可视化"
__plugin_cmd__ = [
    "功能调用统计",
    "全局功能调用统计 [_superuser]",
    "全局日功能调用统计 [_superuser]",
    "全局周功能调用统计 ?[功能] [_superuser]",
    "全局月功能调用统计 ?[功能] [_superuser]",
    "周功能调用统计 ?[功能]",
    "月功能调用统计 ?[功能]",
    "我的功能调用统计",
    "我的日功能调用统计 ?[功能]",
    "我的周功能调用统计 ?[功能]",
    "我的月功能调用统计 ?[功能]",
]
__plugin_type__ = ("功能调用统计可视化", 1)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["功能调用统计"],
}


statistics = on_command(
    "功能调用统计",
    aliases={
        "全局功能调用统计",
        "全局日功能调用统计",
        "全局周功能调用统计",
        "全局月功能调用统计",
        "日功能调用统计",
        "周功能调用统计",
        "月功能调用统计",
        "我的功能调用统计",
        "我的日功能调用统计",
        "我的周功能调用统计",
        "我的月功能调用统计",
    },
    priority=5,
    block=True,
)


statistics_group_file = Path(DATA_PATH) / "statistics" / "_prefix_count.json"
statistics_user_file = Path(DATA_PATH) / "statistics" / "_prefix_user_count.json"


@statistics.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if state["_prefix"]["raw_command"][:2] == "全局":
        if str(event.user_id) in bot.config.superusers:
            data: dict = json.load(open(statistics_group_file, "r", encoding="utf8"))
            if state["_prefix"]["raw_command"][2] == '日':
                itype = 'day_statistics'
            elif state["_prefix"]["raw_command"][2] == '周':
                itype = 'week_statistics'
            elif state["_prefix"]["raw_command"][2] == '月':
                itype = 'month_statistics'
            else:
                itype = 'total_statistics'
            tmp_dict = {}
            data = data[itype]
            if itype in ["day_statistics", "total_statistics"]:
                for key in data['total']:
                    tmp_dict[key] = data['total'][key]
            else:
                for group in data.keys():
                    if group != 'total':
                        for day in data[group].keys():
                            for plugin_name in data[group][day].keys():
                                if data[group][day][plugin_name] is not None:
                                    if tmp_dict.get(plugin_name) is None:
                                        tmp_dict[plugin_name] = 1
                                    else:
                                        tmp_dict[plugin_name] += data[group][day][plugin_name]
            bar_graph = await init_bar_graph(tmp_dict, state["_prefix"]["raw_command"])
            await asyncio.get_event_loop().run_in_executor(None, bar_graph.gen_graph)
            await statistics.finish(image(b64=bar_graph.pic2bs4()))
        return
    if state["_prefix"]["raw_command"][:2] == "我的":
        itype = "user"
        key = str(event.user_id)
        state["_prefix"]["raw_command"] = state["_prefix"]["raw_command"][2:]
        if not statistics_user_file.exists():
            await statistics.finish("统计文件不存在...", at_sender=True)
    else:
        if not isinstance(event, GroupMessageEvent):
            await statistics.finish("请在群内调用此功能...")
        itype = "group"
        key = str(event.group_id)
        if not statistics_group_file.exists():
            await statistics.finish("统计文件不存在...", at_sender=True)
    plugin = ""
    if state["_prefix"]["raw_command"][0] == "日":
        arg = "day_statistics"
    elif state["_prefix"]["raw_command"][0] == "周":
        arg = "week_statistics"
    elif state["_prefix"]["raw_command"][0] == "月":
        arg = "month_statistics"
    else:
        arg = "total_statistics"
    if msg:
        plugin = plugins2settings_manager.get_plugin_module(msg)
        if not plugin:
            if arg not in ["day_statistics", "total_statistics"]:
                await statistics.finish("未找到此功能的调用...", at_sender=True)
    if itype == "group":
        data: dict = json.load(open(statistics_group_file, "r", encoding="utf8"))
        if not data[arg].get(str(event.group_id)):
            await statistics.finish("该群统计数据不存在...", at_sender=True)
    else:
        data: dict = json.load(open(statistics_user_file, "r", encoding="utf8"))
        if not data[arg].get(str(event.user_id)):
            await statistics.finish("该用户统计数据不存在...", at_sender=True)
    day_index = data["day_index"]
    data = data[arg][key]
    if itype == "group":
        name = await GroupInfo.get_group_info(event.group_id)
        name = name.group_name if name else str(event.group_id)
    else:
        name = event.sender.card if event.sender.card else event.sender.nickname
    img = await generate_statistics_img(data, arg, name, plugin, day_index)
    await statistics.send(image(b64=img))


async def generate_statistics_img(
    data: dict, arg: str, name: str, plugin: str, day_index: int
):
    try:
        plugin = plugins2settings_manager.get_plugin_data(plugin)['cmd'][0]
    except (KeyError, IndexError):
        pass
    bar_graph = None
    if arg == "day_statistics":
        bar_graph = await init_bar_graph(data, f"{name} 日功能调用统计")
    elif arg == "week_statistics":
        if plugin:
            current_week = day_index % 7
            week_lst = []
            if current_week == 0:
                week_lst = [1, 2, 3, 4, 5, 6, 7]
            else:
                for i in range(current_week + 1, 7):
                    week_lst.append(str(i))
                for i in range(current_week + 1):
                    week_lst.append(str(i))
            count = []
            for i in range(7):
                if int(week_lst[i]) == 7:
                    try:
                        count.append(data[str(0)][plugin])
                    except KeyError:
                        count.append(0)
                else:
                    try:
                        count.append(data[str(week_lst[i])][plugin])
                    except KeyError:
                        count.append(0)
            week_lst = ["7" if i == "0" else i for i in week_lst]
            bar_graph = BuildMat(
                y=count,
                mat_type="line",
                title=f"{name} 周 {plugin} 功能调用统计【为7天统计】",
                x_index=week_lst,
                display_num=True,
                background=[
                    f"{IMAGE_PATH}/background/create_mat/{x}"
                    for x in os.listdir(f"{IMAGE_PATH}/background/create_mat")
                ],
                bar_color=["*"],
            )
        else:
            bar_graph = await init_bar_graph(update_data(data), f"{name} 周功能调用统计【为7天统计】")
    elif arg == "month_statistics":
        if plugin:
            day_index = day_index % 30
            day_lst = []
            for i in range(day_index + 1, 30):
                day_lst.append(i)
            for i in range(day_index + 1):
                day_lst.append(i)
            count = [data[str(day_lst[i])][plugin] for i in range(30)]
            day_lst = [str(x + 1) for x in day_lst]
            bar_graph = BuildMat(
                y=count,
                mat_type="line",
                title=f"{name} 月 {plugin} 功能调用统计【为30天统计】",
                x_index=day_lst,
                display_num=True,
                background=[
                    f"{IMAGE_PATH}/background/create_mat/{x}"
                    for x in os.listdir(f"{IMAGE_PATH}/background/create_mat")
                ],
                bar_color=["*"],
            )
        else:
            bar_graph = await init_bar_graph(update_data(data), f"{name} 月功能调用统计【为30天统计】")
    elif arg == "total_statistics":
        bar_graph = await init_bar_graph(data, f"{name} 功能调用统计")
    await asyncio.get_event_loop().run_in_executor(None, bar_graph.gen_graph)
    return bar_graph.pic2bs4()


async def init_bar_graph(data: dict, title: str) -> BuildMat:
    return await asyncio.get_event_loop().run_in_executor(None, _init_bar_graph, data, title)


def _init_bar_graph(data: dict, title: str) -> BuildMat:
    bar_graph = BuildMat(
        y=[data[x] for x in data.keys() if data[x] != 0],
        mat_type="barh",
        title=title,
        x_index=[x for x in data.keys() if data[x] != 0],
        display_num=True,
        background=[
            f"{IMAGE_PATH}/background/create_mat/{x}"
            for x in os.listdir(f"{IMAGE_PATH}/background/create_mat")
        ],
        bar_color=["*"],
    )
    return bar_graph


def update_data(data: dict):
    tmp_dict = {}
    for day in data.keys():
        for plugin_name in data[day].keys():
            # print(f'{day}：{plugin_name} = {data[day][plugin_name]}')
            if data[day][plugin_name] is not None:
                if tmp_dict.get(plugin_name) is None:
                    tmp_dict[plugin_name] = 1
                else:
                    tmp_dict[plugin_name] += data[day][plugin_name]
    return tmp_dict

