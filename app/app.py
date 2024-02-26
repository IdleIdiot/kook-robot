import copy
import os
import random
import time


from datetime import datetime

from khl import Bot, Message
# init Bot
from khl.card import CardMessage

# from src.core.wrapper.chatgpt.chat import chat
from src.core.wrapper.trigram.trigram import yi
from src.core.structure.trigram.chitchat import CHITCHAT
from src.core.structure.message.card import HelpCard, GameListCard
from src.utils.common import json_load

# define parameters for match game
ALL_MATCH_INFO = dict()
ALL_BOT_CREATE_CHANNEL = dict()

# load static configuration file
config_path = os.path.join("../src/config", "configuration.json")
config = json_load(config_path)

# object instance
bot = Bot(token=config["bot"]["bot_token"])


# register wrapper, send `/hello` in channel to invoke
@bot.command(name='hello')
async def hello(msg: Message):
    random.seed()
    await msg.reply(random.choice(CHITCHAT))


@bot.command(name="help")
async def help_doc(msg: Message):
    await msg.reply(CardMessage(HelpCard()))


@bot.command(name="random")
async def dice(msg: Message, interval: int = 100):
    if interval < 1:
        await msg.reply("随机上限需要大于0 且为整数")
        return

    random.seed(datetime.now())
    await msg.reply("{}".format(random.randint(0, interval + 1)))


@bot.command(name="yi")
async def destiny(msg: Message, wish: str, pray: str, yi_date: str = datetime.now().__format__("%Y%m%d")):
    await msg.reply("批阴阳断五行，看掌中日月。 "
                    "测风水勘六合，拿袖中乾坤。 "
                    "天闻若雷，了然今生前世。 "
                    "神目如电，看穿仙界凡间。 "
                    "天地万物无所不知，阴阳八卦生死明了。"
                    "待我掐指一算，便可知晓... ...")
    ori, shift, turn_symbol_desc, main_indicate, support_indicate = yi(wish, pray, yi_date)
    await msg.reply("本卦：{}".format(ori))
    await msg.reply("变卦: {}".format(shift))
    await msg.reply("卦象: {}".format(turn_symbol_desc))
    await msg.reply("主解: {}".format(main_indicate))
    if support_indicate:
        await msg.reply("辅解: {}".format(support_indicate))


@bot.command(name="match")
async def match_game(msg: Message, game_name: str, expect_member_num: int):
    channel_name = "DEFAULT"
    await msg.reply("开始匹配, 匹配游戏：{},  房间数量：{}".format(game_name, expect_member_num))
    cur_id = msg.author_id
    if game_name not in ALL_MATCH_INFO.keys():
        ALL_MATCH_INFO.update({game_name: []})

    ALL_MATCH_INFO[game_name].append(cur_id)

    count = 0
    while True:
        current_member_num = len(ALL_MATCH_INFO[game_name])

        if current_member_num >= expect_member_num:
            await msg.reply("匹配成功！请耐心等待其他玩家接受私信并进入语音频道！")
            all_members = copy.deepcopy(ALL_MATCH_INFO[game_name])

            # 设置字典中已判断匹配完成的用户ID为 0， 表示已就绪
            cur_index = ALL_MATCH_INFO[game_name].index(cur_id)
            ALL_MATCH_INFO[game_name][cur_index] = 0
            break
        time.sleep(3)
        if count % 10 == 0:
            await msg.reply("正在匹配玩家中，当前队伍人数：{}".format(current_member_num))

        count += 1

    # 判断所有人就绪，创建语音频道，发送私信给当前玩家告知语音频道信息
    is_ready = False
    while True:
        for cursor in ALL_MATCH_INFO[game_name]:
            if cursor == 0:
                is_ready = True
            else:
                is_ready = False
                break

        if is_ready:
            break

    # 创建且仅创建一个语音频道
    if cur_id == all_members[0]:
        ALL_MATCH_INFO.pop(game_name)
        parameters = {
            "guild_id": msg.ctx.guild.id,
            "parent_id": config["bot_channel_group_id"],
            "name": game_name + "~~" + str(int(datetime.timestamp(datetime.now()))),
            "type": 2,
            "limit_amount": expect_member_num
        }
        result = await msg.ctx.gate.request("POST", "channel/create", data=parameters)
        if result["id"]:
            channel_name = result["name"]
            ALL_BOT_CREATE_CHANNEL.update({result["id"]: datetime.timestamp(datetime.now())})
            await msg.reply("语音频道已创建完成!")

        for member in all_members:
            await msg.ctx.gate.request("POST", "direct-message/create", data={
                "target_id": member,
                "content": "匹配成功，加入语音频道：{} 和小伙伴一起开黑吧".format(channel_name)
            })


@bot.command(name="show_game_list")
async def get_game_list(msg: Message):
    # TODO: to show game list but still not good
    method = "GET"
    route = "game"
    resp_data = await bot.client.gate.request(method=method, route=f"{route}")
    await msg.reply(CardMessage(GameListCard(resp_data["items"])))


@bot.command(name="chatGPT")
async def chat_with_bot(msg: Message, ques: str):
    try:
        time_consuming, answer = chat(ques)
    except Exception as error:
        print("Interface ERROR: {}".format(error))
        await msg.reply("Interface ERROR，Please contact to administrator！")
    else:
        await msg.reply("Time occupancy：{}s, Response：{}".format(time_consuming, answer))


# everything done, go ahead now!

# now invite the bot to a server, and send '/hello' in any channel
# (remember to grant the bot with read & send permissions)

if __name__ == '__main__':
    bot.run()
