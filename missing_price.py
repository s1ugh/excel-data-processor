import os
from dotenv import load_dotenv
import pandas as pd
from main import write_csv

# настройка путей
load_dotenv()
CSV_PATH_MISSING_PRICE = os.getenv('CSV_PATH_MISSING_PRICE')
CSV_PATH_MISSING_NAME = os.getenv('CSV_PATH_MISSING_NAME')
CSV_PATH_MATCH = os.getenv('CSV_PATH_MATCH')


ready_price = os.getenv('ready_price')
movement_art = os.getenv('movement_art')

# чтение файлов и подготовка фрейма
ready_price_df = pd.read_csv(ready_price, sep=';', encoding='utf-8', on_bad_lines='skip')
movement_art_df = pd.read_csv(movement_art, sep=';', encoding='utf-8', on_bad_lines='skip')

# поиск совпадений и раздедление на три возможных файла

merged_df = pd.merge(ready_price_df, movement_art_df, on= 'Артикул',how='outer', indicator=True)

# 1 - файл: совпадения только с правого файла
missing_price = merged_df[merged_df['_merge'] == 'right_only'].copy()

# 2 - файл: совпадения только с левого файлы
missing_name = merged_df[merged_df['_merge'] == 'left_only'].copy()

# 3 - файл: совпадения с обоих файлов
data_match = merged_df[merged_df['_merge'] == 'both'].copy()

# удаляем колонки совпадений _merge
missing_price.drop(columns=['_merge'], inplace=True)
missing_name.drop(columns=['_merge'], inplace=True)
data_match.drop(columns=['_merge'], inplace=True)
merged_df.drop(columns=['_merge'], inplace=True)

# записываем в файлы
write_csv(CSV_PATH_MISSING_PRICE, missing_price)
write_csv(CSV_PATH_MISSING_NAME, missing_name)
write_csv(CSV_PATH_MATCH, data_match)
