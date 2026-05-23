"""Era rewriting service — transform modern content to target era.

MVP: returns mock rewritten content. Production: LLM-driven rewriting.
"""


def rewrite_for_era(understanding: dict, era: str, transcript: str) -> dict:
    """Rewrite video content for the target era.

    Returns dict with:
      - scenes: list of {index, dialogue, visual_prompt, transition}
      - world_building: str
    """
    # TODO: Integrate LLM for era-aware content rewriting
    era_templates = {
        "ancient-greece": {
            "dialogues": [
                "诸位，且看这市集之中，竟有如此琼浆玉液！此乃众神之赐福也。",
                "依我看，这杯中之物，堪比奥林匹斯山上的甘露。",
                "诸君，且听我说——此地便是雅典城中最负盛名的哲学之馆。",
            ],
            "world_building": "公元前5世纪的雅典集市，哲学家与市民在此辩论真理。",
        },
        "napoleonic": {
            "dialogues": [
                "诸位绅士，这家咖啡馆的出品，即使在巴黎也是首屈一指的。",
                "我以军人的荣誉担保，这里的咖啡值得一试。",
                "请允许我向各位推荐这家位于帝国大道上的优雅场所。",
            ],
            "world_building": "19世纪初的巴黎，拿破仑时代的欧洲正处于变革之中。",
        },
        "tang-dynasty": {
            "dialogues": [
                "诸位看官，此间茶肆虽不大，却藏着长安城里数一数二的好茶。",
                "此茶入口回甘，便是连宫中的贵人也赞不绝口。",
                "你看这店中陈设，颇有几分大明宫的风范。",
            ],
            "world_building": "盛唐时期的长安城，丝绸之路上的繁华之都。",
        },
        "medieval-tavern": {
            "dialogues": [
                "旅人啊，这家酒馆的蜜酒在整个王国都找不到第二家！",
                "我以剑与荣誉起誓，这里的烤肉配得上国王的宴席。",
                "来吧，冒险者，在篝火旁听我说一段传奇故事。",
            ],
            "world_building": "中世纪的石砌酒馆，冒险者在此集结，开启传奇旅程。",
        },
        "cyberpunk": {
            "dialogues": [
                "检测到高品质咖啡因化合物……这家店的数据评分很高。",
                "建议摄入。这里的氛围模块加载得很完美。",
                "全城的黑客都在这接头——这里不只是咖啡馆，是数据的中转站。",
            ],
            "world_building": "2077年的霓虹都市，高科技与低生活的交汇点。",
        },
        "victorian": {
            "dialogues": [
                "亲爱的先生，这家店的茶点无疑是伦敦最精致的。",
                "我已经写信给《泰晤士报》，推荐这间优雅的休憩之所。",
                "以女王的名义，这里的服务堪称模范。",
            ],
            "world_building": "19世纪维多利亚时代的伦敦，蒸汽与优雅的工业之都。",
        },
    }

    template = era_templates.get(era, era_templates["ancient-greece"])

    scenes = []
    for i, dialogue in enumerate(template["dialogues"]):
        scenes.append({
            "index": i,
            "dialogue": dialogue,
            "visual_prompt": f"{template['world_building']}，{understanding['scene_type']}场景，"
                            f"{'，'.join(understanding['key_objects'])}的时代化版本。",
            "transition": "dissolve" if i > 0 else "cut",
        })

    return {
        "scenes": scenes,
        "world_building": template["world_building"],
    }
