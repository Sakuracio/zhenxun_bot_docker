from configs.config import Config
import nonebot


Config.add_plugin_config(
    "genshin",
    "mhyVersion",
    "2.11.1"
)

Config.add_plugin_config(
    "genshin",
    "salt",
    "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"
)

Config.add_plugin_config(
    "genshin",
    "client_type",
    "5"
)

nonebot.load_plugins("plugins/genshin/query_user")



