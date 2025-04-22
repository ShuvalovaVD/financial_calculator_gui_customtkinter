import json
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def display():
    redraw_diagram()


def redraw_diagram():
    global fig, ax, labels, values, canvas
    ax.clear()  # стираем старую диаграмму

    # рисуем новую диаграмму
    # wedges - секторы, texts - подписи, autotexts - %
    wedges, texts, autotexts = ax.pie(
        values,
        startangle=90,  # первый сектор начинаем с 90 градусов
        wedgeprops={"edgecolor": "white", "linewidth": 1},  # клинья между секторами
        autopct="%.1f%%",  # формат отображения %
        pctdistance=0.80  # расстояние от центра до % - 80% от радиуса
    )
    # убираем подписи
    for text in texts:
        text.set_visible(False)
    # настройка легенды
    ax.legend(
        wedges,
        labels,
        title="Категории",
        loc="center",
        bbox_to_anchor=(0.5, 0),  # разместить по центру относительно диаграммы и сразу под ней
        ncol=2
    )
    ax.set_title("Распределение трат по категориям")
    # настройка отображения
    fig.tight_layout()  # автоматически корректирует отступы, чтобы ничего не накладывалось друг на друга
    canvas.draw()


def add_purchase():
    global my_font
    dialog_window = ctk.CTkToplevel()
    dialog_window.title("Добавить запись")
    dialog_window.geometry("500x350")

    def add_purchase_loc():
        pass

    label_add = ctk.CTkLabel(master=dialog_window, text="Данные о записи:", font=my_font)
    categories_list = ["Еда", "Жильё", "Одежда", "Проезд", "Здоровье", "Развлечения", "Быт", "Прочее"]
    combobox_category = ctk.CTkComboBox(master=dialog_window, values=categories_list, font=my_font, state="readonly")
    combobox_category.set("Еда")
    label_day = ctk.CTkLabel(master=dialog_window, text="День:", font=my_font)
    entry_day = ctk.CTkEntry(master=dialog_window, placeholder_text="дд.мм.гггг", font=my_font, justify="center",
                             width=200)
    label_puchase = ctk.CTkLabel(master=dialog_window, text="Покупка:", font=my_font)
    entry_purchase = ctk.CTkEntry(master=dialog_window, placeholder_text="что оплачено", font=my_font, justify="center",
                                  width=200)
    label_price = ctk.CTkLabel(master=dialog_window, text="Цена:", font=my_font)
    entry_price = ctk.CTkEntry(master=dialog_window, placeholder_text="в рублях", justify="center", width=200,
                               font=my_font)
    button_add = ctk.CTkButton(master=dialog_window, text="Добавить", font=my_font, command=add_purchase_loc,
                                   width=320)

    rows, columns = 5, 3
    for i in range(rows):
        dialog_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        dialog_window.columnconfigure(index=i, weight=1)
    label_add.grid(row=0, column=0, columnspan=3)
    combobox_category.grid(row=1, column=0)
    label_day.grid(row=1, column=1)
    entry_day.grid(row=1, column=2)
    label_puchase.grid(row=2, column=1)
    entry_purchase.grid(row=2, column=2)
    label_price.grid(row=3, column=1)
    entry_price.grid(row=3, column=2)
    button_add.grid(row=4, column=1, columnspan=2)


def delete_purchase():
    global my_font
    dialog_window = ctk.CTkToplevel()
    dialog_window.title("Удалить запись")
    dialog_window.geometry("300x200")

    def delete_purchase_loc():
        pass

    label_delete = ctk.CTkLabel(master=dialog_window, text="Номер записи:", font=my_font)
    entry_delete = ctk.CTkEntry(master=dialog_window, font=my_font)
    button_delete = ctk.CTkButton(master=dialog_window, text="Удалить", font=my_font, command=delete_purchase_loc)
    rows, columns = 3, 1
    for i in range(rows):
        dialog_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        dialog_window.columnconfigure(index=i, weight=1)
    label_delete.grid(row=0, column=0)
    entry_delete.grid(row=1, column=0)
    button_delete.grid(row=2, column=0)


def clear_all():
    global my_font
    dialog_window = ctk.CTkToplevel()
    dialog_window.title("Очистить всё")
    dialog_window.geometry("300x200")

    def answer_yes():
        pass

    def answer_no():
        dialog_window.destroy()

    label_clear = ctk.CTkLabel(master=dialog_window, text="Уверены, что хотите\nудалить все записи\nза указанный период?",
                               font=my_font)
    button_yes = ctk.CTkButton(master=dialog_window, text="Да", font=my_font, command=answer_yes)
    button_no = ctk.CTkButton(master=dialog_window, text="Нет", font=my_font, command=answer_no)
    rows, columns = 2, 2
    for i in range(rows):
        dialog_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        dialog_window.columnconfigure(index=i, weight=1)
    label_clear.grid(row=0, column=0, columnspan=2)
    button_yes.grid(row=1, column=0)
    button_no.grid(row=1, column=1)


# перед началом работы приложения загружаем данные
# в файле data.json данные записаны в словарь, где ключи - категории, значения - списки, которые имеют формат:
# ["дата", "покупка", цена], причем даты расположены в хронологическом порядке
# таким образом, data.json содержит всю историю трат, распределённую по категориям
with open(file="data.json", mode="r", encoding="utf-8") as file_in:
    data = json.load(file_in)

# первичная настройка графического интерфейса приложения
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.title("Финансовый калькулятор")
root.geometry("1000x600")
my_font = ctk.CTkFont(family="Roboto", size=20)

# виджеты
frame_for_diagram = ctk.CTkFrame(master=root)  # рамка для диаграммы
label_period = ctk.CTkLabel(master=root, text="Период:", font=my_font)
entry_start_period = ctk.CTkEntry(master=root, placeholder_text="дд.мм.гггг", font=my_font, justify="center")
label_dash = ctk.CTkLabel(master=root, text="-", font=my_font)
entry_finish_period = ctk.CTkEntry(master=root, placeholder_text="дд.мм.гггг", font=my_font, justify="center")
button_done = ctk.CTkButton(master=root, text="Отобразить", font=my_font, width=420, command=display)
label_history = ctk.CTkLabel(master=root, text="История расходов:", font=my_font)
scrollable_frame = ctk.CTkScrollableFrame(master=root, width=420)
button_add = ctk.CTkButton(master=root, text="Добавить запись", font=my_font, width=420, command=add_purchase)
button_delete = ctk.CTkButton(master=root, text="Удалить запись", font=my_font, width=420, command=delete_purchase)
button_clear = ctk.CTkButton(master=root, text="Очистить всё", font=my_font, width=420, command=clear_all)

# глобальная сетка
rows, columns = 10, 10
for i in range(rows):
    root.rowconfigure(index=i, weight=1)
for i in range(columns):
    root.columnconfigure(index=i, weight=1)
frame_for_diagram.grid(row=0, rowspan=10, column=0, columnspan=5)
label_period.grid(row=0, column=5, columnspan=5)
entry_start_period.grid(row=1, column=5, columnspan=2)
label_dash.grid(row=1, column=7)
entry_finish_period.grid(row=1, column=8, columnspan=2)
button_done.grid(row=2, column=5, columnspan=5)
label_history.grid(row=3, column=5, columnspan=5)
scrollable_frame.grid(row=4, rowspan=3, column=5, columnspan=5)
button_add.grid(row=7, column=5, columnspan=5)
button_delete.grid(row=8, column=5, columnspan=5)
button_clear.grid(row=9, column=5, columnspan=5)

# при запуске приложения нужно отобразить диаграмму и историю для всех трат за весь период
# => собираем данные для диаграммы за весь период
labels, values = [], []
for category, info in data.items():
    if len(info) == 0:
        continue
    labels.append(category)
    total_price = 0
    for day, purchase, price in info:
        total_price += price
    values.append(total_price)
if labels == values == []:  # если в data.json нет никаких данных, то отображаем диаграмму с ничем
    labels = ["Ничего"]
    values = [100]

# создание фигуры и графика
fig = plt.figure(figsize=(5, 5.8))
ax = fig.add_subplot(111)

# встраиваем фигуру fig в рамку frame с помощью canvas
canvas = FigureCanvasTkAgg(fig, master=frame_for_diagram)
canvas.get_tk_widget().pack(fill="both", expand=True)
redraw_diagram()  # на старте отрисовываем диаграмму

# на старте отображаем загруженную историю трат за весь период
current_history = []
for category, info in data.items():
    if len(info) == 0:
        continue
    ctk.CTkLabel(master=scrollable_frame, text=f"{category}:", font=my_font).pack()
    for day, purchase, price in info:
        current_history.append((category, day, purchase, price))
        ctk.CTkLabel(master=scrollable_frame,
                     text=f"{len(current_history)}. {day} - {purchase} - {price}р.", font=my_font).pack()

plt.close()  # завершает процессы, связанные с графиками
root.mainloop()

# после завершения работы приложения сохраняем данные
with open(file="data.json", mode="w", encoding="utf-8") as file_out:
    json.dump(data, file_out, indent=2, ensure_ascii=False)
