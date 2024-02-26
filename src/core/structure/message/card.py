from khl.card import Card, Types, Module, Element


def HelpCard() -> Card:
    card = Card(theme=Types.Theme.INFO, size=Types.Size.LG)
    # title
    card.append(Module.Header("二年级课代表"))
    card.append(Module.Section(Element.Text("人工智障: 卜卦、算卦、不解卦 ~ ")))

    # base wrapper
    card.append(
        Module.Section(
            Element.Text(
                """
                `/help` - 机器人指令使用手册
                """, type=Types.Text.KMD
            )
        )
    )

    # other wrapper
    card.append(
        Module.Section(
            Element.Text(
                """
                `/yi {wish} {pray} {datetime}` - 易经算卦
                `/random {interval}` - 摇骰子
                `/match {game} {player_number}` - 匹配开黑玩家
                `/chatGPT {question}` - 和人工智障讨论问题
                """, type=Types.Text.KMD
            )
        )
    )

    card.append(
        Module.Context(
            Element.Text(
                """
                卦象吉凶，概不负责，如有雷同，纯属巧合
                """, type=Types.Text.KMD
            )
        )
    )

    return card


def GameListCard(items) -> Card:
    card = Card(theme=Types.Theme.INFO, size=Types.Size.LG)
    card.append(Module.Header("二年级课代表"))
    card.append(Module.Section(Element.Text("人工智障: 卜卦、算卦、不解卦 ~ ")))

    # limit card length
    for item in items:
        card.append(
            Module.Section(
                Element.Text(
                    "{}: {}".format(item["id"], item["name"]), type=Types.Text.KMD
                )
            )
        )
    return card
