import os
from dotenv import load_dotenv
import pandas as pd
from tkinter import filedialog
import tkinter as tk
from main import write_csv

# настройка путей
load_dotenv()
SKIPROWS_MOV = 6
CSV_PATH_MOV = os.getenv('CSV_PATH_MOV')

# загрузка файлов из системы
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title='Выберите файл для',
    filetypes=[('Файлы Excel', '{*.xls}'), ('Все файлы', "*.*")]
)

# чтение эксельки и формирование фрейма
articul = pd.read_excel(file_path, skiprows=SKIPROWS_MOV, header=None)
articul_df = articul.get([4, 5]).rename(columns={4: 'Артикул', 5: 'Номенклатура'}).dropna()

# загрузка фрейма
write_csv(CSV_PATH_MOV, articul_df)

