import tkinter as tk
from tkinter import messagebox
import random

class FifteenGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Игра в 15")

        #Меню
        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)

        self.game_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Игра", menu=self.game_menu)
        self.game_menu.add_command(label="Новая игра", command=self.new_game)

        #Уровни сложности 
        self.difficulty_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Сложность", menu=self.difficulty_menu)
        self.difficulty_menu.add_command(label="3x3", command=lambda: self.set_size(3))
        self.difficulty_menu.add_command(label="4x4", command=lambda: self.set_size(4))
        self.difficulty_menu.add_command(label="5x5", command=lambda: self.set_size(5))

        self.menu.add_command(label="Выход", command=self.root.quit)

        # Игровое поле
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.buttons = []  # Кнопки для игрового поля
        self.size = 4  # Размер поля по умолчанию 4x4
        self.tiles = []  # Хранение текущего состояния плиток

        self.root.bind("<Configure>", self.update_tile_sizes)
        self.new_game()

    def create_widgets(self):
        """Создает кнопки для игрового поля."""
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.buttons.clear()

        for row in range(self.size):
            for col in range(self.size):
                btn = tk.Button(self.frame, text="", command=lambda r=row, c=col: self.move_tile(r, c))
                btn.grid(row=row, column=col, sticky="nsew")
                self.buttons.append(btn)

        for row in range(self.size):
            self.frame.grid_rowconfigure(row, weight=1)
            self.frame.grid_columnconfigure(row, weight=1)
        self.update_board()

    def update_board(self):
        """Обновляет отображение игрового поля."""
        for idx, btn in enumerate(self.buttons):
            value = self.tiles[idx]
            btn.config(text=value if value != 0 else "", state=tk.NORMAL if value != 0 else tk.DISABLED)
        self.update_tile_sizes()

    def update_tile_sizes(self, event=None):
        """Обновляет размер плиток в зависимости от размеров окна."""
        frame_width = self.frame.winfo_width()
        frame_height = self.frame.winfo_height()
        tile_width = frame_width // self.size
        tile_height = frame_height // self.size

        for btn in self.buttons:
            btn.config(width=tile_width // 10, height=tile_height // 20)

    def move_tile(self, row, col):
        """Обрабатывает перемещение плитки."""
        idx = row * self.size + col
        zero_idx = self.tiles.index(0)

        # Проверяем, можно ли переместить плитку
        if idx in (zero_idx - 1, zero_idx + 1, zero_idx - self.size, zero_idx + self.size):
            if (idx % self.size == 0 and zero_idx % self.size == self.size - 1) or \
               (idx % self.size == self.size - 1 and zero_idx % self.size == 0):
                return  # Исключение перехода между рядами

            self.tiles[zero_idx], self.tiles[idx] = self.tiles[idx], self.tiles[zero_idx]
            self.update_board()

            if self.check_victory():
                messagebox.showinfo("Победа!", "Поздравляем! Вы собрали головоломку!")

    def check_victory(self):
        """Проверяет, собрана ли головоломка."""
        return self.tiles == list(range(1, self.size**2)) + [0]

    def new_game(self):
        """Запускает новую игру."""
        self.tiles = list(range(1, self.size**2)) + [0]
        random.shuffle(self.tiles)
        self.create_widgets()

    def set_size(self, size):
        """Устанавливает размер поля и запускает новую игру."""
        self.size = size
        self.new_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = FifteenGame(root)
    root.mainloop()