import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageGrab
class Paint:
    def __init__(self, master):
        self.master = master
        self.master.title("Paint by rakuzan2weak#2522")
        self.master.geometry("1240x720")
         # Создание холста
        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # добавляем кнопку ластика
        self.lastik = tk.Button(self.master, text='Erase', command=self.choose_lastik)
        self.lastik.pack(side='left', padx=5, pady=5)

        # Создание меню
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.new_file)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save", command=self.save_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_app)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Clear", command=self.clear_canvas)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.colormenu = tk.Menu(self.menubar, tearoff=0)
        self.colormenu.add_command(label="Choose Color", command=self.choose_color)
        self.menubar.add_cascade(label="Color", menu=self.colormenu)

        self.master.config(menu=self.menubar)

        # Инициализация переменных
        self.color = "black"
        self.start_x = None
        self.start_y = None
        self.lastik_flag = False # флаг ластика

        # Привязка событий
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

    def choose_color(self):
        # Выбор цвета
        self.color = colorchooser.askcolor()[1]

    def clear_canvas(self):
        # Очистка холста
        self.canvas.delete("all")

    def new_file(self):
        # Создание нового файла
        self.clear_canvas()

    def open_file(self):
        # Открытие файлов изображений
        filepath = filedialog.askopenfilename()
        if filepath:
            img = Image.open(filepath)
            draw = ImageDraw.Draw(img)
            self.canvas.delete("all")
            self.canvas.image = tk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")

    def save_file(self):
        # Сохранение файла
        filepath = filedialog.asksaveasfilename(defaultextension=".png")
        if filepath:
            x = self.master.winfo_rootx() + self.canvas.winfo_x()
            y = self.master.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(filepath)

    def exit_app(self):
        # Выход из приложения
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def draw(self, event):
        # Рисование на холсте
        if self.start_x and self.start_y:
            # если флаг ластика - рисуем белую линию (на белом фоне она стирает)
            if self.lastik_flag:
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, width=10, fill='white')
            else:
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, width=3, fill=self.color, capstyle=tk.ROUND, smooth=True)

        self.start_x = event.x
        self.start_y = event.y

    def stop_draw(self, event):
        # Остановка рисования
        if self.start_x and self.start_y:
            if self.lastik_flag:
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, width=10, fill='white')
            else:
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, width=3, fill=self.color, capstyle=tk.ROUND, smooth=True)

        self.start_x = None
        self.start_y = None

    def choose_lastik(self):
        # переключение флага ластика
        self.lastik_flag = not self.lastik_flag


if __name__ == "__main__":
    root = tk.Tk()
    Paint(root)
    root.mainloop()