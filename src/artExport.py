import scrython as scry
import requests
import time
import os
from parentDir import get_parent_dir

def _save_image(path, url, name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Ensure the directory exists
        if not os.path.exists(path):
            os.makedirs(path)

        with open('{}{}.png'.format(path, name), 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except OSError as e:
        print(f"OS error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

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

def _get_all_cards(card_array):
    card_list = []
    for card in card_array:
        time.sleep(0.5)
        id_ = card['id']
        card = scry.cards.Id(id=id_)
        card_list.append(card)

    return card_list

def runArtExport():
    print("Welcome to ArtExport Module.")
    while True:
        print("Choose a mode.")
        print("- 1) Search by name")
        print("- 2) Search by set name (download all card images in the set)")
        print("- p) Move to Previous Page")
        print("- q) Quit the Program")
        print()
        user_input = input("Your Choice: ")

        while True:
            if user_input[0] == '1':
                break
            elif user_input[0] == '2':
                break
            elif user_input[0] == 'p':
                return 0
            elif user_input[0] == 'q':
                return -1
            else:
                user_input = input("Wrong input! Your Choice: ")

        if user_input[0] == '1':
            while True:
                card_name = input("Input Card Name: ")
                try:
                    card = scry.Named(fuzzy=card_name)
                    try:
                        _save_image(f"{get_parent_dir()}/art/indiv/", card.image_uris(0, 'png'), card.name())
                        print("Art Successfully Saved in ../art/indiv folder.")
                    except Exception as e:
                        print(f"Art Save Failed: {e}")
                    break
                except Exception as e:
                    print(f"Please refine your input. (Try again): {e}")
                    if input("Enter p to go to the previous page. Enter anything else not to do so: ")[0] == 'p':
                        return 0

        elif user_input[0] == '2':
            while True:
                try:
                    set_name = input("Input Set Name or Code: ")
                    set_card_list = _get_all_pages(set_name)
                    set_cards = _get_all_cards(set_card_list)

                    card_num = 0
                    for card in set_cards:
                    
                        time.sleep(0.05)
                        
                        try:
                            _save_image(f"{get_parent_dir()}/art/{set_name}/", card.image_uris(0, 'png'), card.name())
                            print(f"Succesfully Saved {card.name()}.png in ../art/{set_name}")
                            card_num+=1
                        except:
                            continue
                    print("=============================")
                    print(f"Successfully Saved {card_num} Cards in ../art/{set_name}")
                    break
                except Exception as e:
                    print(f"Something went wrong. Please try again: {e}")
                    if input("Enter p to go to the previous page. Enter anything else not to do so: ")[0] == 'p':
                        return 0