import sqlite3
import glob
import os
import sys
import unicodedata
import requests
import scrython

#### TODO ####
# 1. getKorean(eng)
# 2. getKoreanType(eng, land=False)
# 3. convertText(eng, order=0)
LAND_COLOR = {'W': '#eddfb8', 'U': '#b7cbe4', 'B': '#a39e9b',
              'R': '#dc9f83', 'G': '#bbd0bd', 'M': '#e5d594', 'C': '#d0cbc8'}
CLIENT_FOLDER = "C:\Program Files (x86)\Steam\steamapps\common\MTGA\MTGA_Data\Downloads\Raw"
# To be Fixed: To make it work with all computers.


def getKorean(eng):
    db_path = os.path.join(CLIENT_FOLDER, "Raw_CardDatabase_*.mtga")
    for db in glob.glob(db_path):
        try:
            card_conn = sqlite3.connect(db)
            card_cursor = card_conn.cursor()

            table_name = 'Localizations'
            eng_column = 'enUS'
            ko_column = 'koKR'

            query = f"""
            SELECT {ko_column}
            FROM {table_name}
            WHERE {eng_column} LIKE ?
            """

            card_cursor.execute(query, (eng, ))
            try:
                row = card_cursor.fetchone()
                card_conn.close()
                return row[0]
            except:
                # Not found.
                card_conn.close()
                # Keyword 연결일 경우 생각해야 함
                if '.% ' in eng:
                    splitDot = eng.split('.% ')
                    splitKorFirst = getKorean(splitDot[0]+'.%')
                    splitKorSecond = getKorean(splitDot[1])
                    if splitKorFirst != "(미완성)" and splitKorSecond != "(미완성)":
                        return splitKorFirst+" "+splitKorSecond
                    else:
                        return "(미완성)"
                elif '. ' in eng:
                    splitDot = eng.split('. ')
                    splitKorFirst = getKorean(splitDot[0]+'.')
                    if splitKorFirst != "(미완성)":
                        return splitKorFirst+" "+getKorean(splitDot[1])
                    else:
                        return "(미완성)"
                elif ',' not in eng:
                    return "(미완성)"
                else:
                    ans = ""
                    splitComma = eng.split(', ')
                    for split in splitComma:
                        splitKor = getKorean(split)
                        if splitKor == "(미완성)":
                            return "(미완성)"
                        else:
                            ans += splitKor+', '
                    return ans.rstrip(', ')

        except sqlite3.Error as e:
            print(f"Error happened in sqlite3 - {db}: {e}")
        finally:
            if card_conn:
                card_conn.close()
    return "(미완성)"


def getKoreanType(card, land=False):
    ans = ""
    type = card.type_line().split(" ")
    for t in type:
        ans += " "
        if t == '—':
            ans += "—"
        else:
            ans += getKorean(t)
    ans = ans.strip()

    if land:
        if len(card.colors()) == 0:
            ans = "<color=#373a3c>{{{#!wiki style=\"margin: -5px -10px; padding: 5px 10px; background: linear-gradient(to right, #d0cbc8, #d0cbc8);\"\n"+ans+"}}} "
        elif len(card.colors()) >= 3:
            ans = "<color=#373a3c>{{{#!wiki style=\"margin: -5px -10px; padding: 5px 10px; background: linear-gradient(to right, #e5d594, #e5d594);\"\n"+ans+"}}} "
        elif len(card.colors()) == 1:
            ans = "<color=#373a3c>{{{#!wiki style=\"margin: -5px -10px; padding: 5px 10px; background: linear-gradient(to right, "+LAND_COLOR[card.colors()[
                0]]+", "+LAND_COLOR[card.colors()[0]]+");\"\n"+ans+"}}} "
    return ans


def convertText(eng, order=0):
    # order 0: scryfall oracle => mtg arena oracle
    # order 1: mtg arena oracle => scryfall oracle + add symbol pic
    ans = ""
    if order == 1:
        # MTG Arena Oracle to Scryfall Oracle
        split_eng = list(eng)
        inside_bracket = False
        first_o = True
        for letter in split_eng:
            if inside_bracket:
                # We are inside bracket.
                if letter == '}':
                    # end of bracket.
                    inside_bracket = False
                    ans += '.svg|width=15px]]'
                elif letter == 'o':
                    if not first_o:
                        # Close bracket
                        ans += '.svg|width=15px]][[파일:mtg-symbol-'
                    else:
                        first_o = False
                elif letter == '(' or letter == ')' or letter == '/':
                    # Ignore
                    pass
                else:
                    ans += letter.lower()
            else:
                if letter == '{':
                    inside_bracket = True
                    first_o = True
                    ans += "[[파일:mtg-symbol-"
                else:
                    ans += letter
        return ans

    else:
        # Scryfall Oracle to MTGA Oracle
        split_eng = list(eng)
        inside_brackets = False
        for i in range(len(split_eng)):
            letter = split_eng[i]
            if inside_brackets:
                if i == len(split_eng)-1:
                    ans += '}'
                    break
                elif letter == '}':
                    if split_eng[i+1] == '{':
                        pass
                    else:
                        inside_brackets = False
                        ans += '}'
                elif letter == '{':
                    ans += 'o'
                elif split_eng[i+1] == '/':
                    if split_eng[i-1] == '/':
                        ans += letter
                    else:
                        ans += '('+letter
                elif split_eng[i-1] == '/':
                    ans += letter+')'
                else:
                    ans += letter
            else:
                if letter == '{':
                    inside_brackets = True
                    ans += '{o'
                elif letter == '"' or letter == "'" or letter == "\n":
                    ans += '%'

                else:
                    ans += letter

        return ans


def getKoreanText(eng):
    # Could includ {oG} or something like that
    return convertText(getKorean(convertText(eng)), order=1)
