import requests


class ChannelWrapper:
    def __init__(self, kook, bot):
        # base_url = "https://www.kookapp.cn"
        self.kook = kook
        self.bot = bot

    def delete_channel(self, channel_id):
        # bot_token = "1/MTMwMjk=/O+HH+EVstgBVGY0j/RauYA=="
        requests.request(method="POST",
                         url="{}/api/v3/channel/delete".format(self.kook.base_url),
                         params={"channel_id": channel_id},
                         headers={"Authorization": "Bot {}".format(self.bot.token)})
