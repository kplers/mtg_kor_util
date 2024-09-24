import scrython as scry
import os
import time
import arenaSql
from parentDir import get_parent_dir


#### TODO ####
# 2. writeOracleText(card) (Incomplete)
# 5. writeLegality(card)
# 6. writeSets(card)
# 7. arenaSql.py
# 8. Writing a code to implement special types of cards

CARDCOLOR = {'W': 'white', 'U': 'blue', 'B': 'black',
             'R': 'red', 'G': 'green', 'C': 'silver'}
LAND_COLOR = {'W': '#eddfb8', 'U': '#b7cbe4', 'B': '#a39e9b',
              'R': '#dc9f83', 'G': '#bbd0bd', 'M': '#e5d594', 'C': '#d0cbc8'}


def isType(card, type):
    return (type in card.type_line().split(" "))


def writeColor(card):
    ans = ""
    if (len(card.colors()) == 1):
        ans += """{{{#!wiki style="display: inline-block; max-width: 270px; margin-right: 5px;" 
||<nopad> [[파일:"""+card.name()+""".png|width=265px]] ||}}}{{{#!wiki style="display: inline-block; max-width: 600px; margin-top: -18px;" 
||<tablealign=left><tablebordercolor=#393d3f><width=600px><height=1px><bgcolor="""
        ans += CARDCOLOR[card.colors()[0]]
        ans += "> ||\n"

    elif (len(card.colors()) == 0):
        ans += """{{{#!wiki style="display: inline-block; max-width: 270px; margin-right: 5px;" 
||<nopad> [[파일:"""+card.name()+""".png|width=265px]] ||}}}{{{#!wiki style="display: inline-block; max-width: 600px; margin-top: -18px;" 
||<tablealign=left><tablebordercolor=#393d3f><width=600px><height=1px><bgcolor=silver> ||
"""

    else:
        ans += """{{{#!wiki style="display: inline-block; max-width: 270px; margin-right: 5px;" 
||<nopad> [[파일:"""+card.name()+""".png|width=265px]] ||}}}{{{#!wiki style="display: inline-block; max-width: 600px; margin-top: -18px;" 
||<tablealign=left><tablebordercolor=#393d3f><width=600px><height=1px>"""
        ans+='{{{#!wiki style="margin: -5px -10px; padding: 5px 10px; background: linear-gradient(to right' 
        for color in card.colors():
            ans += ", "+CARDCOLOR[color]
            ans += ", "+CARDCOLOR[color]
            ans += ", "+CARDCOLOR[color]
        ans += ");\"\n}}}||\n"

    return ans


def isModal(card):
    try:
        modal_check = scry.cards.Search(q=f'"{card.name()}" is:modal')
        return True
    except:
        return False


def writeOracleText(card):
    # Should divide by cases of card types
    # Cases:
    #  1. General Case
    #  2. Multiface Cards (Not Implemented at this point)
    #  3. Planeswalkers
    #  5. Split Cards (Not Implemented at this point)
    #  6. Adventure Cards (Not Implemented at this point)
    #  7. Sagas (Not Implemented at this point)
    #  8. Classes (Not Implemented at this point)
    #  9. Level Up Cards (Not Implemented at this point)
    #  10. Dice Cards (Not Implemented at this point)
    #  11. Prototypes (Not Implemented at this point)
    #  12. Mutate Cards (Not Implemented at this point)
    #  13. Modal Cards
    ans = ""
    if isType(card, 'Planeswalker'):
        # 3. Planeswalkers
        pass
    elif isModal(card):
        # 13. Modal Cards
        oracleTexts = card.oracle_text().split('\n•')
        oracleText = ' •'.join(oracleTexts)
        oracleTexts = oracleText.split('\n')
        korTexts = []
        for oracleLine in oracleTexts:
            korTexts.append(arenaSql.getKoreanText(oracleLine))
        first = True
        # Identify where is the modal part
        for korText in korTexts:
            if not first:
                ans += "{{{#!wiki style=\"margin: 6px;\"\n}}}"
            else:
                first = False
            if '•' in korText:
                # Modal Part.

                modeSplit = korText.split(' •')
                ans += modeSplit[0]+"{{{#!wiki style=\"margin: 6px;\"\n}}}"
                ans += '{{{#!wiki style="margin-left: -10px;"'
                for modeSplitText in modeSplit[1:]:
                    ans += '\n *' + modeSplitText
                ans += "}}}"
        return ans

    else:
        # 1. General Case
        trial=arenaSql.getKoreanText(card.oracle_text())
        if "(미완성)" not in trial:
            first=True
            for textLine in trial.split("\n"):
                if first:
                    first = False
                else:
                    ans += "{{{#!wiki style=\"margin: 6px;\"\n}}}"
                ans += textLine
        else:
            oracleTexts = card.oracle_text().split('\n')
            first = True
            for oracleLine in oracleTexts:
                if first:
                    first = False
                else:
                    ans += "{{{#!wiki style=\"margin: 6px;\"\n}}}"
                ans += arenaSql.getKoreanText(oracleLine)
    return ans


def writeLoyalty(card):
    try:
        loyalty = card.loyalty()
        return f"""||'''충성도: {loyalty}'''||\n"""
    except:
        # This is not a planeswalker.
        return ""


def writePowerToughness(card):
    try:
        power = card.power()
        toughness = card.toughness()
        return f"""||'''{power}/{toughness}'''||\n"""
    except:
        return ""


def writeDefense(card):
    try:
        defense = card.scryfallJson['defense']
        if not defense:
            return ""
        else:
            return f"""||'''방어도: {defense}'''||\n"""
    except:
        return ""


def writeLegality(card):
    pass


def writeSets(card):
    pass


def _get_all_pages(set_code):
    page_count = 1
    all_data = []
    while True:
        time.sleep(0.5)
        page = scry.cards.Search(q='set:{}'.format(set_code), page=page_count)
        all_data = all_data + page.data()
        page_count += 1
        if not page.has_more():
            break

    return all_data


def _get_all_cards_by_color(card_array):
    # Order: White / Blue / Black / Red / Green / Multicolored / Colorless / Lands
    card_list = [[], [], [], [], [], [], [], []]
    colors = ['W', 'U', 'B', 'R', 'G']
    for card in card_array:
        time.sleep(0.2)
        id_ = card['id']
        card = scry.cards.Id(id=id_)
        if len(card.colors()) == 0:
            if 'Land' in card.type_line().split(" "):
                card_list[7].append(card)
            else:
                card_list[6].append(card)
        elif len(card.colors()) >= 2:
            card_list[5].append(card)
        else:
            card_list[colors.index(card.colors()[0])].append(card)

    return card_list


def _get_all_cards(card_array):
    card_list = []
    for card in card_array:
        time.sleep(0.2)
        id_ = card['id']
        card = scry.cards.Id(id=id_)
        card_list.append(card)

    return card_list


def _mana_symbols(card):
    mana_cost = card.mana_cost()
    costs = []
    ans = ""
    for letter in mana_cost:
        if letter == '{':
            costs.append("")
        elif letter == '}':
            continue
        elif letter == '/':
            continue
        else:
            costs[-1] = costs[-1]+letter.lower()
    for cost in costs:
        ans += f"[[파일:mtg-symbol-{cost}.svg|width=20px]]"
    ans += " }}}\n"
    return ans


def alchemy():
    print("Welcome to Alchemy Namuwiki Document Creator!")
    parDir = get_parent_dir()
    while True:
        set_code = input(
            "Please give a set name / code (in English, e.g. YBLB): ")
        set_name = input(
            "Please give the Korean main set name (precisely, excluding alchemy): ")
        set_path = f"{parDir}\\namu"
        if not os.path.exists(set_path):
            os.makedirs(set_path)
        cards = _get_all_cards_by_color(_get_all_pages(set_code))
        with open(set_path+'\\'+set_code+'.txt', "w", encoding='utf-8') as t:
            t.write(f"""[include(틀:상위 문서, top1=매직 더 개더링/카드 일람/{set_name})]
[include(틀:매직 더 개더링/카드 일람/{set_name})]
[목차]

== 개요 ==
[[{set_name}]]의 알케미 전용 카드를 정리한 문서.
[include(틀:매직 더 개더링/사용 가능 범위, 제목=사용 가능 범위,
알케미사용가능=, 히스토릭사용가능=, 타임리스사용가능=,)]

""")
            korean_colors = ['백색', '청색', '흑색', '적색', '녹색', '다색', '무색', '대지']

            for index, color_cards in enumerate(cards):
                t.write(f"== {korean_colors[index]} ==\n")

                for card in color_cards:
                    t.write(f"=== {card.name()} ===\n")
                    t.write(writeColor(card))
                    t.write("""||{{{+1 '''"""+card.name()+"""'''}}} {{{#!wiki style="float: right;" 
                            """)
                    t.write(_mana_symbols(card))
                    t.write(arenaSql.getKorean(card.name())+"||\n")
                    t.write("||")
                    # Type
                    if cards.index(color_cards) == 7:
                        t.write(arenaSql.getKoreanType(
                            card, land=True))
                    else:
                        t.write(arenaSql.getKoreanType(card))
                    t.write("||\n")
                    t.write("||{{{#!wiki style=\"word-break: keep-all;\"\n")
                    # Oracle text
                    try:
                        t.write(writeOracleText(card))
                        t.write("}}}||\n")
                        # power/toughness
                        t.write(writePowerToughness(card))
                        # Loyalty
                        t.write(writeLoyalty(card))
                        # defense
                        t.write(writeDefense(card))
                        t.write("\n}}}\n")
                    except:
                        t.write("(미완성)}}}||\n\n}}}\n")

            t.write(f"[[분류:매직 더 개더링/카드/{set_name}|카드 일람/알케미]]")
        print(f"The document has been saved to ..\namu\{set_name} 알케미.txt")
        if input("Continue, or move to previous? (p for previous): ") == 'p':
            return 0


def ordinary():
    pass
