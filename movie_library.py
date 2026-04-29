
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x600")

        self.file_path = "movielibrary.json"
        self.movies = self.load_data()

        # --- Frames ---
        # Frame для полей ввода
        input_frame = tk.Frame(root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        # Frame для фильтрации
        filter_frame = tk.Frame(root, padx=10, pady=5)
        filter_frame.pack(fill=tk.X)
        
        # Frame для таблицы
        table_frame = tk.Frame(root, padx=10, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # --- Поля для ввода ---
        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, sticky=tk.W, padx=5)

        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.genre_entry = tk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=1, column=1, sticky=tk.W, padx=5)

        tk.Label(input_frame, text="Год выпуска:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.year_entry = tk.Entry(input_frame, width=10)
        self.year_entry.grid(row=0, column=3, sticky=tk.W, padx=5)

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.rating_entry = tk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, sticky=tk.W, padx=5)
        
        # --- Кнопка добавления ---
        add_button = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        add_button.grid(row=0, column=4, rowspan=2, padx=20, ipady=10)

        # --- Поля для фильтрации ---
        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=20)
        self.filter_genre_entry.grid(row=0, column=1, sticky=tk.W, padx=5)

        tk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.filter_year_entry = tk.Entry(filter_frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, sticky=tk.W, padx=5)

        filter_button = tk.Button(filter_frame, text="Применить фильтр", command=self.filter_movies)
        filter_button.grid(row=0, column=4, padx=10)
        
        reset_button = tk.Button(filter_frame, text="Сбросить", command=self.reset_filter)
        reset_button.grid(row=0, column=5, padx=5)


        # --- Таблица для вывода ---
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год выпуска")
        self.tree.heading("rating", text="Рейтинг")
        
        # Настройка ширины колонок
        self.tree.column("title", width=300)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=100, anchor=tk.CENTER)
        self.tree.column("rating", width=100, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_table(self.movies)

    def update_table(self, movie_list):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Заполнение таблицы
        for movie in movie_list:
            self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year_str = self.year_entry.get()
        rating_str = self.rating_entry.get()

        # --- Валидация ---
        if not all([title, genre, year_str, rating_str]):
            messagebox.showerror("Ошибка ввода", "Все поля должны быть заполнены!")
            return

        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Год должен быть числом.")
            return

        try:
            rating = float(rating_str.replace(',', '.')) # Замена запятой на точку для float
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Рейтинг должен быть числом от 0 до 10.")
            return

        # --- Добавление данных ---
        new_movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(new_movie)
        
        self.save_data()
        self.update_table(self.movies)
        
        # --- Очистка полей ---
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def filter_movies(self):
        filter_genre = self.filter_genre_entry.get().lower()
        filter_year = self.filter_year_entry.get()

        filtered_list = self.movies

        if filter_genre:
            filtered_list = [m for m in filtered_list if filter_genre in m["genre"].lower()]
        
        if filter_year:
            try:
                year_val = int(filter_year)
                filtered_list = [m for m in filtered_list if m["year"] == year_val]
            except ValueError:
                messagebox.showerror("Ошибка фильтра", "Год для фильтрации должен быть числом.")
                return

        self.update_table(filtered_list)

    def reset_filter(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.update_table(self.movies)

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return [] # Возвращаем пустой список в случае ошибки чтения или пустого файла


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
