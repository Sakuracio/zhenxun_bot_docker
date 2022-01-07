from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.rule import to_me
from utils.utils import get_message_text, is_number
from services.log import logger
from utils.manager import group_manager


__zx_plugin_name__ = "超级用户被动开关 [Superuser]"
__plugin_usage__ = """
usage：
    超级用户被动开关
    指令：
        开启/关闭广播通知
""".strip()
__plugin_des__ = "超级用户被动开关"
__plugin_cmd__ = [
    "开启/关闭广播通知",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


oc_gb = on_command(
    "开启广播通知",
    aliases={"关闭广播通知"},
    rule=to_me(),
    permission=SUPERUSER,
    priority=1,
    block=True,
)


@oc_gb.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    group = get_message_text(event.json())
    if group:
        if is_number(group):
            group = int(group)
            for g in await bot.get_group_list():
                if g["group_id"] == group:
                    break
            else:
                await oc_gb.finish("没有加入这个群...", at_sender=True)
            if state["_prefix"]["raw_command"] == "开启广播通知":
                logger.info(f"USER {event.user_id} 开启了 GROUP {group} 的广播")
                await oc_gb.finish(await group_manager.open_group_task(group, "broadcast",), at_sender=True)
            else:
                logger.info(f"USER {event.user_id} 关闭了 GROUP {group} 的广播")
                await oc_gb.finish(await group_manager.close_group_task(group, "broadcast"), at_sender=True)
        else:
            await oc_gb.finish("请输入正确的群号", at_sender=True)
    else:
        await oc_gb.finish("请输入要关闭广播的群号", at_sender=True)