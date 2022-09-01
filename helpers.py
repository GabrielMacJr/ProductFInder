import PySimpleGUI as sg
import os

def create_excel_file(data, file_name, file_location):
    """Creates an excel file
       :param data: data provided
       :param file_name: name of file
       :param file_location: saving directory
    """
    data.to_excel(f"{file_location}/{file_name}.xlsx", index=False)
    
    
def verify_file_folder_exist(file_location,file_name):
    """Verifies if saving directory exists 
       and if the file exists
       :param data: data provided
       :param file_name: name of file
       :param file_location: saving directory
       :returns:
            - folder_exists - True if saving directory exists or False if it does not exist
            - file_exists - True if file exists or False if it does not exist
    """
    folder_exists = True
    file_exists = False
    if os.path.exists( f"{file_location}") == True:
        if os.path.exists(f"{file_location}/{file_name}.xlsx") == False:
            return(folder_exists, file_exists)
        else:
            file_exists = True
            return(folder_exists, file_exists)
    else: 
        folder_exists = False
        return(folder_exists, file_exists)
    
