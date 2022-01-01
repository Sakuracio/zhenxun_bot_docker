from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER
import asyncio
from utils.utils import get_message_text, get_message_imgs
from services.log import logger
from utils.message_builder import image
from utils.manager import group_manager
from configs.config import Config

__zx_plugin_name__ = "广播 [Superuser]"
__plugin_usage__ = """
usage：
    指令：
        广播- ?[消息] ?[图片]
        示例：广播- 你们好！
""".strip()
__plugin_des__ = "昭告天下！"
__plugin_cmd__ = ["广播-"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {"broadcast": "广播"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_BROADCAST",
    True,
    help_="被动 广播 进群默认开关状态",
    default_value=True,
)

broadcast = on_command("广播-", priority=1, permission=SUPERUSER, block=True)


@broadcast.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    rst = ""
    for img in imgs:
        rst += image(img)
    sid = bot.self_id
    gl = await bot.get_group_list(self_id=sid)
    gl = [
        g["group_id"]
        for g in gl
        if await group_manager.check_group_task_status(g["group_id"], "broadcast")
    ]
    g_cnt = len(gl)
    cnt = 0
    error = ""
    x = 0.25
    for g in gl:
        cnt += 1
        if cnt / g_cnt > x:
            await broadcast.send(f"已播报至 {int(cnt / g_cnt * 100)}% 的群聊")
            x += 0.25
        try:
            await bot.send_group_msg(self_id=sid, group_id=g, message=msg + rst)
            logger.info(f"GROUP {g} 投递广播成功")
        except Exception as e:
            logger.error(f"GROUP {g} 投递广播失败：{type(e)}")
            error += f"GROUP {g} 投递广播失败：{type(e)}\n"
        await asyncio.sleep(0.5)
    await broadcast.send(f"已播报至 100% 的群聊")
    if error:
        await broadcast.send(f"播报时错误：{error}")
