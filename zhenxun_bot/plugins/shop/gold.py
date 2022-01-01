from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import GROUP
from utils.data_utils import init_rank
from models.bag_user import BagUser
from utils.message_builder import image
from utils.utils import get_message_text, is_number

__zx_plugin_name__ = "商店 - 我的金币"
__plugin_usage__ = """
usage：
    我的金币
    指令：
        我的金币
""".strip()
__plugin_des__ = "商店 - 我的金币"
__plugin_cmd__ = ["我的金币"]
__plugin_type__ = ("商店",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店", "我的金币"],
}


my_gold = on_command("我的金币", priority=5, block=True, permission=GROUP)

gold_rank = on_command("金币排行", priority=5, block=True, permission=GROUP)


@my_gold.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await my_gold.finish(await BagUser.get_my_total_gold(event.user_id, event.group_id))


@gold_rank.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    num = get_message_text(event.json())
    if is_number(num) and 51 > int(num) > 10:
        num = int(num)
    else:
        num = 10
    all_users = await BagUser.get_all_users(event.group_id)
    all_user_id = [user.user_qq for user in all_users]
    all_user_data = [user.gold for user in all_users]
    rank_image = await init_rank("金币排行", all_user_id, all_user_data, event.group_id, num)
    if rank_image:
        await gold_rank.finish(image(b64=rank_image.pic2bs4()))
