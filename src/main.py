import scrython
import artExport
import namuWikiDocSet
import arenaDataKoreanJson
import scryInfo
### 이 프로그램은 다음 기능을 가지고 있습니다. ###
# (ver 0.1 기준 - 2024-09-19)

# 1. 카드 이름을 입력하면, 그에 해당하는 고화질 png 파일이 art 폴더에 저장됩니다. (art-save)
# 2. 알케미 세트 코드를 입력하면, 그에 해당하는 나무위키 문서 형식을 자동으로 생성합니다. (템플릿 제외)
# 3. 세트 코드와 색을 입력하면, 그에 해당하는 나무위키 문서 형식을 자동으로 생성합니다. (템플릿 제외)
# - 다만, 매직 더 개더링 폴더에 한글 번역이 존재하지 않을 경우 텍스트는 (To be complete)로 대체합니다.
# 4. 카드 이름을 입력하면, 그에 해당하는 정보를 선택하여 열람할 수 있습니다.
# 5. 세트 코드를 입력하면, 아레나에서 데이터를 추출해 한글 번역 파일을 json으로 만듭니다.


#### TODO ####
# Improve Function 2 - Support more types of cards and italicizing keywords
# Implement function 3 and 4.
# Implement function 5.

if __name__ == '__main__':
    print("=========================================")
    print()
    print("Welcome to Scryfall-Namuwiki-Util ver 0.1")
    print()

    while (True):
        print("=========================================")
        print("Choose the functionality to use:")
        print(" * 1) Art Export")
        print(" * 2) Create Alchemy Set's Namuwiki Document")
        # print(" * 3) Create Ordinary Set's Namuwiki Document")
        # print(" * 4) Get Information of a card")
        print(" * 5) Export JSON file of a set")
        print(" * 6) Export JSON file of a special guest set")
        print(" * 7) Export JSON file of a alchemy set")
        print(" * q) Quit the program")
        print("=========================================")

        user_input = input("Your Choice: ")
        while (True):
            if user_input=='':
                print("Invalid Input! Input a number (1~4)")
                user_input = input("Your Choice: ")
            elif user_input[0] == '1':
                break
            elif user_input[0] == '2':
                break
            # elif user_input[0] == '3':
            #     break
            # elif user_input[0] == '4':
            #     break
            elif user_input[0] == '5':
                break
            elif user_input[0]=='6':
                break
            elif user_input[0]=='7':
                break
            elif user_input[0] == 'q':
                print("See you next time!")
                quit()
            else:
                print("Invalid Input! Input a number (1~4)")
                user_input = input("Your Choice: ")

        if user_input[0] == '1':
            # Art Export Module
            if(artExport.runArtExport()==-1):
                quit()
        elif user_input[0] == '2':
            # Alchemy Set Document Module
            namuWikiDocSet.alchemy()
        # elif user_input[0] == '3':
        #     # Ordinary Set Document Module
        #     namuWikiDocSet.ordinary()
        # elif user_input[0] == '4':
        #     # Information
        #     scryInfo.runInfo()
        elif user_input[0] == '5':
            # Export JSON file of a set
            set_code=input("Input the set code: ")
            arenaDataKoreanJson.getSet(set_code)
        elif user_input[0]=='6':
            set_code=input("Input the set code: ")
            arenaDataKoreanJson.getSet("SPG-"+set_code, digital=True)
        elif user_input[0]=='7':
            set_code=input("Input the main set code: ")
            year_code=input("What is the year code? (for example, if it is Y24, input 24): ")
            arenaDataKoreanJson.getSet("Y"+year_code+"-"+set_code, digital=True)
