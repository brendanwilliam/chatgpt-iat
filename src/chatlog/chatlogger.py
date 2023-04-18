# Date: Feb 24, 2023
# Author: Brendan Keane
# Description: Takes '.html' files from saved ChatGPT chats and converts them to
#              a single '.csv' file with the following columns: 'author',
#              'message', 'datetime'


# Imports ======================================================================
import re
import os
import pandas as pd
from bs4 import BeautifulSoup

# Global variables =============================================================
IMPORT_PATH = './html/'
EXPORT_PATH = './csv/'

# Functions ====================================================================

def extract_chatlog(filepath):

  # Opens and parses the html file
  with open(filepath) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

  # Regex match between parentheses to get the file name
  file_name = re.search(r'\((.+)\)', filepath).group(1)
  print(file_name)

  # Gets all chatgpt responses as DOM elements
  chats = soup.find_all('div', class_='min-h-[20px] flex flex-col items-start gap-4 whitespace-pre-wrap')

  # Version number
  aTags = soup.find_all('a')
  version = aTags[-1].text
  print('Version: ' + version)
  print('Messages saved: ' + str(len(chats)))

  # Creates an empty dataframe to store the chatlog
  chat_list = pd.DataFrame(columns=['datetime', 'chat_index', 'author', 'message', 'version'])

  # Loops through the chatgpt responses and adds them to the dataframe
  for i in range(len(chats)):
    chat = chats[i]
    user = ''
    if i%2 == 0:
      user = 'human'
    else:
      user = 'chatgpt'

    chat_list.loc[i] = [file_name, i, user, chat.text, version]

  # Saves dataframe to csv in the csv folder
  chat_list.to_csv(EXPORT_PATH + file_name + '.csv', index=False)

def extract_all_chatlogs():
  # Gets all the html files in the saved_chats folder
  html_files = os.listdir(IMPORT_PATH)

  # Loops through the html files and extracts the chatlog
  for html_file in html_files:
    print('=====================')
    extract_chatlog(IMPORT_PATH + html_file)
    print('=====================\n\n')


def combine_chat_data():
  # Gets all the csv files in the csv folder
  csv_files = os.listdir(EXPORT_PATH)

  # Creates an empty dataframe to store the chatlog
  chat_list = pd.DataFrame(columns=['datetime', 'chat_index', 'author', 'message', 'version'])

  # Loops through the csv files and adds them to the dataframe
  for csv_file in csv_files:
    chat_file = pd.read_csv(EXPORT_PATH + csv_file)
    chat_list = pd.concat([chat_list, chat_file])

  # Saves dataframe to csv in the csv folder
  chat_list.to_csv('./full_chat_log.csv', index=False)


# Main ==========================================================================
if __name__ == '__main__':
  extract_all_chatlogs()
  combine_chat_data()
