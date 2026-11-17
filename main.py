from tkinter import filedialog
import tkinter as tk
import pandas as pd
import os
from dotenv import load_dotenv
import logging

# для загрузки файлы из системы
root = tk.Tk()
root.withdraw()

# настройка путей
SKIPROWS_EXCEL = 8
load_dotenv()
CSV_PATH = os.getenv('CSV_PATH')
CSV_PATH1 = os.getenv('CSV_PATH1') # test

# логгирование для дебага
file_log = logging.FileHandler('logfile.log')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.DEBUG)


# сбор, обновление данных - удаление дубликатов
def write_csv(csv_path, data_frame):
    
    if os.path.exists(csv_path):
        old_df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig')

        combined_df = pd.concat([old_df, data_frame])
    else:
        combined_df = data_frame

    clean_df = combined_df.drop_duplicates(subset=['Артикул'], keep='first')# удаляем по первому совпадению
    clean_df.to_csv(csv_path, sep=";", encoding='utf-8-sig', index=False)

if __name__ == '__main__':

    # открытие окна для выбора файла и его загрузки 
    file_path = filedialog.askopenfilename(
        title='Выберите файл для',
        filetypes=[('Файлы Excel', '{*.xlsx}'), ('Все файлы', "*.*")]
    )
    logging.info(f'Файл: {file_path}')

    # читаем эксельку и подготавливаем фрейм для записи в csv
    uniqe_articul = pd.read_excel(file_path, skiprows=SKIPROWS_EXCEL, header=None, engine='openpyxl')
    logging.debug(f'Файл: {file_path} прочитан')

    new_df_articul = uniqe_articul.get([5, 79]).rename(columns={5: 'Артикул', 79: 'Цена'}).dropna()
    logging.debug(f'Фрейм создан')

    # функция записи в csv(удаляет дубликаты)
    write_csv(CSV_PATH, new_df_articul)

