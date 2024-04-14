import csv
import re
from pathlib import Path
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, scrolledtext


BASE_PATH = Path.cwd()
CSV_FILE_PATH = BASE_PATH / "Tranzistor.csv"


class TranzistorDirectoryApp(tk.Tk):
    def __init__(self, storage: list[dict]):
        super().__init__()
        self.title('Справочник транзисторов')
        self.geometry('640x520')
        self.storage = storage

        Label(self, text="Введите наименование транзистора:").pack(pady=10)
        self.search_entry = Entry(self, width=50)
        self.search_entry.pack(pady=10)

        Button(self, text="Поиск", command=self.search_tranzistor).pack(pady=10)

        self.results_text = scrolledtext.ScrolledText(self, width=70, height=30)
        self.results_text.pack(pady=20)

    def search_tranzistor(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showinfo("Ошибка", "Введите значение для поиска!")
            return

        pattern = re.compile(f"^{query}$", flags=2)
        found_tranzistors = [
            tranzistor for tranzistor in self.storage
            if re.match(pattern, tranzistor["Наименование транзистора"])
        ]

        self.results_text.delete('1.0', tk.END)
        if found_tranzistors:
            for tranzistor in found_tranzistors:
                for key, value in tranzistor.items():
                    self.results_text.insert(tk.END, f"{key}: {value}\n")
                self.results_text.insert(tk.END, "-" * 60 + "\n")
        else:
            messagebox.showinfo("Результат", "Указанное наименование отсутствует!")


def add_item_from_csv(storage: list):
    with open(CSV_FILE_PATH, "r", encoding="utf-8") as fi:
        csv_reader = csv.DictReader(fi, delimiter="|", dialect="excel")
        for line in csv_reader:
            storage.append(line)


if __name__ == '__main__':
    tranzistors: list = []
    add_item_from_csv(tranzistors)
    app = TranzistorDirectoryApp(storage=tranzistors)
    app.mainloop()
