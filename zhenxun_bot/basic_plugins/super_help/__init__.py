from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from .data_source import create_help_image
from pathlib import Path


__zx_plugin_name__ = '超级用户帮助 [Superuser]'


superuser_help_image = Path(IMAGE_PATH) / 'superuser_help.png'

if superuser_help_image.exists():
    superuser_help_image.unlink()

super_help = on_command(
    "超级用户帮助", rule=to_me(), priority=1, permission=SUPERUSER, block=True
)


@super_help.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if not superuser_help_image.exists():
        await create_help_image()
    x = image(superuser_help_image)
    await super_help.finish(x)
