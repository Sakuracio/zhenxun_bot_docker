from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from utils.http_utils import AsyncHttpx
from configs.config import Config
from .data_source import get_data


__zx_plugin_name__ = "鸡汤"
__plugin_usage__ = """
usage：
    不喝点什么感觉有点不舒服
    指令：
        鸡汤
""".strip()
__plugin_des__ = "喏，亲手为你煮的鸡汤"
__plugin_cmd__ = ["鸡汤"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["鸡汤", "毒鸡汤"],
}

url = "https://v2.alapi.cn/api/soul"


jitang = on_command("鸡汤", aliases={"毒鸡汤"}, priority=5, block=True)


@jitang.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        data, code = await get_data(url)
        if code != 200:
            await jitang.finish(data, at_sender=True)
        await jitang.send(data["data"]["content"])
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 发送鸡汤:" + data["data"]["content"]
        )
    except Exception as e:
        await jitang.send("鸡汤煮坏掉了...")
        logger.error(f"鸡汤煮坏掉了 {type(e)}：{e}")
