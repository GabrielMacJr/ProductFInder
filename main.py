from pickle import TRUE
import PySimpleGUI as sg
from helpers import *
from data import *


def run():
    """Gathers specific data about an item and outputs an excel sheet with the data.
       The following data is gathered: hyperlinks, details, price, shipping price, rating, number of reviews, page found 
    """
    sg.theme('DefaultNoMoreNagging') 
    layout = [
        [sg.Text('Product Search'), sg.Input(key='user_input', size=(54,1))],
        [sg.Text('File Name'), sg.Input(key='file_name', size=(54,1))],
        [sg.Text('Saving Location'), sg.Input(key='save_folder'), sg.FolderBrowse()],
        [sg.Button('Complete Search'), sg.Exit()],
            ]
    window = sg.Window("ProductFinder", layout, element_justification='right')
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if isinstance(values['user_input'], type(None)) is not True:
            search_term_pages, search_term_obejct  = user_search(values['user_input'])
        if search_term_obejct == 'Nothing Found':
                sg.popup('Searh Item Not Found')
        else: 
            folder_exists, file_exists = verify_file_folder_exist(values['save_folder'], values['file_name'])
            data = get_data(search_term_pages, search_term_obejct)
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif bool(values['user_input']) == True and bool(values['file_name']) == True and bool(values['save_folder']) == True:
                if folder_exists == True and file_exists == False:
                    create_excel_file(data, values['file_name'], values['save_folder'])
                    window['user_input']('') 
                    window['file_name']('') 
                    sg.popup(f"File: '{values['file_name']}' created", f"Saved at: {values['save_folder']}")
                elif folder_exists == True and file_exists == True:
                    clicked = sg.popup_yes_no('File already exists.', f'Do you want to overwrite the existing file?')
                    if clicked == 'Yes':
                        create_excel_file(data, values['file_name'], values['save_folder'])
                        window['user_input']('') 
                        window['file_name']('') 
                        sg.popup(f"File: '{values['file_name']}' created", f"Saved at: {values['save_folder']}")
                    else:
                        window['file_name']('') 
                else:  
                    if folder_exists == False:
                        sg.popup_error('Saving path does not exist. Provide a correct saving destination')
            else:
                sg.popup_error('Can not complete search. Please fill out all fields')
    window.close()

if __name__ == '__main__':
    run()