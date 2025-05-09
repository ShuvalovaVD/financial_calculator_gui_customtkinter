import json
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


def check_day(s):
    if s.count(".") != 2:
        return False
    d, m, y = s.split(".")
    if len(m) != 2 or (not m.isdigit()):
        return False
    m = int(m)
    if m < 1 or m > 12:
        return False
    if len(y) != 4 or (not y.isdigit()):
        return False
    y = int(y)
    if y < 0:
        return False
    if len(d) != 2 or (not d.isdigit()):
        return False
    d = int(d)
    days_in_february = 29 if (y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)) else 28
    days_in_months = {1: 31, 2: days_in_february, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30,
                      12: 31}
    if d < 1 or d > days_in_months[m]:
        return False
    return True


def check_day_in_period(day, start_period, finish_period):
    dd_day, mm_day, yyyy_day = map(int, day.split("."))
    if start_period != None:
        dd_start, mm_start, yyyy_start = map(int, start_period.split("."))
        if yyyy_day < yyyy_start:
            return False
        elif yyyy_day == yyyy_start and mm_day < mm_start:
            return False
        elif yyyy_day == yyyy_start and mm_day == mm_start and dd_day < dd_start:
            return False
    if finish_period != None:
        dd_finish, mm_finish, yyyy_finish = map(int, finish_period.split("."))
        if yyyy_day > yyyy_finish:
            return False
        elif yyyy_day == yyyy_finish and mm_day > mm_finish:
            return False
        elif yyyy_day == yyyy_finish and mm_day == mm_finish and dd_day > dd_finish:
            return False
    return True


def report_error(error_text):
    global my_font
    dialog_window = ctk.CTkToplevel()
    dialog_window.title("Ошибка")
    dialog_window.geometry("700x100")
    ctk.CTkLabel(master=dialog_window, text="Ошибка:", text_color="red", font=my_font, pady=10).pack()
    ctk.CTkLabel(master=dialog_window, text=error_text, text_color="#fff5f0", font=my_font, pady=10).pack()


def redraw_diagram(labels, values):
    global fig, ax, canvas
    ax.clear()  # стираем старую диаграмму

    # рисуем новую диаграмму
    # wedges - секторы, texts - подписи, autotexts - %
    wedges, texts, autotexts = ax.pie(
        values,
        startangle=90,  # первый сектор начинаем с 90 градусов
        wedgeprops={"edgecolor": "#fff5f0", "linewidth": 1},  # клинья между секторами
        autopct="%.1f%%",  # формат отображения %
        pctdistance=0.80,  # расстояние от центра до % - 80% от радиуса
        textprops={"color": "#fff5f0"},  # %
        colors = sns.color_palette('dark')[1:len(values) + 1]
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
    ax.set_title("Распределение трат по категориям:", color="#fff5f0", fontdict={"fontfamily": "Tahoma",
                                                                                 "fontsize": 14})
    # настройка отображения
    fig.tight_layout()  # автоматически корректирует отступы, чтобы ничего не накладывалось друг на друга
    canvas.draw()  # отрисовываем canvas


def redraw_window():
    global scrollable_frame, data, my_font
    period_info = scrollable_frame.winfo_children()[0].cget("text")[:-1]
    if period_info == "За весь период":
        start_period = finish_period = None
    elif period_info[:15] == "За период после":
        start_period, finish_period = period_info[16:], None
    elif period_info[:12] == "За период до":
        start_period, finish_period = None, period_info[13:]
    else:
        start_period, finish_period = period_info[10:].split(" - ")

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(master=scrollable_frame, text=period_info + ":", text_color="#fff5f0", font=my_font).pack()
    labels, values = [], []
    pos = 1
    for category, info in data.items():
        total_price = 0
        flag_category = False
        for day, purchase, price in info:
            if check_day_in_period(day, start_period, finish_period):
                total_price += price
                if not flag_category:
                    ctk.CTkLabel(master=scrollable_frame, text=f"{category}:", text_color="#fff5f0",
                                 font=my_font).pack()
                    flag_category = True
                ctk.CTkLabel(master=scrollable_frame, text=f"{pos}. {day} - {purchase} - {price}р.",
                             text_color="#fff5f0", font=my_font).pack()
                pos += 1
        if total_price > 0:
            labels.append(category)
            values.append(total_price)
    if labels == values == []:
        ctk.CTkLabel(master=scrollable_frame, text="Нет трат", text_color="#fff5f0", font=my_font).pack()
        labels = ["Ничего"]
        values = [100]

    redraw_diagram(labels, values)


def display():
    global entry_start_period, entry_finish_period, scrollable_frame
    start_period, finish_period = entry_start_period.get(), entry_finish_period.get()
    period_info = None
    if start_period != "" and finish_period != "":
        if (not check_day(start_period)) or (not check_day(finish_period)):
            report_error("Вы ввели некорректную дату")
            return
        dd_start, mm_start, yyyy_start = map(int, start_period.split("."))
        dd_finish, mm_finish, yyyy_finish = map(int, finish_period.split("."))
        if yyyy_start > yyyy_finish:
            report_error("Вы ввели некорректную дату")
            return
        if yyyy_start == yyyy_finish and mm_start > mm_finish:
            report_error("Вы ввели некорректную дату")
            return
        if yyyy_start == yyyy_finish and mm_start == mm_finish and dd_start > dd_finish:
            report_error("Вы ввели некорректную дату")
            return
        period_info = f"За период {start_period} - {finish_period}:"
    elif start_period != "":
        finish_period = None
        if not check_day(start_period):
            report_error("Вы ввели некорректную дату")
            return
        period_info = f"За период после {start_period}:"
    elif finish_period != "":
        start_period = None
        if not check_day(finish_period):
            report_error("Вы ввели некорректную дату")
            return
        period_info = f"За период до {finish_period}:"
    else:
        start_period = finish_period = None
        period_info = "За весь период:"

    scrollable_frame.winfo_children()[0].configure(text=period_info)
    redraw_window()


def add_purchase():
    global my_font
    dialog_window = ctk.CTkToplevel()
    dialog_window.title("Добавить запись")
    dialog_window.geometry("500x350")

    def add_purchase_loc():
        global data
        nonlocal combobox_category, entry_day, entry_purchase, entry_price
        category, day, purchase, price = (combobox_category.get(), entry_day.get(), entry_purchase.get(),
                                          entry_price.get())
        if not check_day(day):
            report_error("Вы ввели некорректную дату")
            return

        if "-" in purchase:
            report_error("Знака '-' не должно быть в названии покупки")
            return

        if (not price.isdigit()) or int(price) < 1:
            report_error("Цена должна быть целым положительным числом")
            return

        data[category].append([day, purchase, int(price)])

        redraw_window()

    label_add = ctk.CTkLabel(master=dialog_window, text="Данные о записи:", text_color="#fff5f0", font=my_font)
    combobox_category = ctk.CTkComboBox(master=dialog_window, values=["Еда", "Жильё", "Одежда", "Проезд", "Здоровье",
                                        "Развлечения", "Быт", "Прочее"], font=my_font, state="readonly",
                                        text_color="#fff5f0", dropdown_font=("Tahoma", 12),
                                        dropdown_text_color="#fff5f0", border_color="#cd8921", button_color="#cd8921",
                                        dropdown_hover_color="#cd8921")
    combobox_category.set("Еда")
    label_day = ctk.CTkLabel(master=dialog_window, text="День:", text_color="#fff5f0", font=my_font)
    entry_day = ctk.CTkEntry(master=dialog_window, placeholder_text="дд.мм.гггг", placeholder_text_color="#c1b6ac",
                             text_color="#fff5f0", font=my_font, justify="center", width=200,
                             border_color="#cd8921")
    label_puchase = ctk.CTkLabel(master=dialog_window, text="Покупка:", text_color="#fff5f0", font=my_font)
    entry_purchase = ctk.CTkEntry(master=dialog_window, placeholder_text="что оплачено",
                                  placeholder_text_color="#c1b6ac", text_color="#fff5f0", font=my_font,
                                  justify="center", width=200, border_color="#cd8921")
    label_price = ctk.CTkLabel(master=dialog_window, text="Цена:", text_color="#fff5f0", font=my_font)
    entry_price = ctk.CTkEntry(master=dialog_window, placeholder_text="в рублях", placeholder_text_color="#c1b6ac",
                               text_color="#fff5f0", justify="center", width=200, font=my_font, border_color="#cd8921")
    button_add = ctk.CTkButton(master=dialog_window, text="Добавить", text_color="#fff5f0", font=my_font, width=320,
                               command=add_purchase_loc, fg_color="#cd8921", hover_color="#a26c1a")

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
        global scrollable_frame, data
        nonlocal entry_delete
        answer = entry_delete.get()
        if not answer.isdigit():
            report_error("Вы ввели что-то отличное от целого неотрицательного числа")
            return

        category = None
        flag_is_del = False
        for widget in scrollable_frame.winfo_children()[1:]:
            if "." not in widget.cget("text"):
                category = widget.cget("text")[:-1]
                continue
            if widget.cget("text").split(".")[0] == answer:
                day, purchase, price = widget.cget("text")[len(answer) + 2:].split(" - ")
                price = int(price[:-2])
                data[category].remove([day, purchase, price])
                flag_is_del = True
                break

        if not flag_is_del:
            report_error("Пункта с данным номером нет в истории трат")
            return

        redraw_window()

    label_delete = ctk.CTkLabel(master=dialog_window, text="Номер записи:", text_color="#fff5f0", font=my_font)
    entry_delete = ctk.CTkEntry(master=dialog_window, font=my_font, justify="center", text_color="#fff5f0",
                                border_color="#cd8921")
    button_delete = ctk.CTkButton(master=dialog_window, text="Удалить", text_color="#fff5f0", font=my_font,
                                  command=delete_purchase_loc, fg_color="#cd8921", hover_color="#a26c1a")
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
    dialog_window.geometry("400x200")

    def answer_yes():
        global scrollable_frame, data, my_font
        period_info = scrollable_frame.winfo_children()[0].cget("text")[:-1]
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        if period_info == "За весь период":
            start_period = finish_period = None
        elif period_info[:15] == "За период после":
            start_period, finish_period = period_info[16:], None
        elif period_info[:12] == "За период до":
            start_period, finish_period = None, period_info[13:]
        else:
            start_period, finish_period = period_info[10:].split(" - ")

        for category, info in data.items():
            elems_to_del = []
            for day, purchase, price in info:
                if check_day_in_period(day, start_period, finish_period):
                    elems_to_del.append([day, purchase, price])
            for elem in elems_to_del:
                data[category].remove(elem)

        ctk.CTkLabel(master=scrollable_frame, text=period_info + ":", text_color="#fff5f0", font=my_font).pack()
        ctk.CTkLabel(master=scrollable_frame, text="Нет трат", text_color="#fff5f0", font=my_font).pack()
        redraw_diagram(["Ничего"], [100])
        dialog_window.destroy()

    def answer_no():
        dialog_window.destroy()

    label_clear = ctk.CTkLabel(master=dialog_window,
                               text="Уверены, что хотите\nудалить все записи\nза указанный период?",
                               text_color="#fff5f0", font=my_font)
    button_yes = ctk.CTkButton(master=dialog_window, text="Да", text_color="#fff5f0", font=my_font, command=answer_yes,
                               fg_color="#cd8921", hover_color="#a26c1a")
    button_no = ctk.CTkButton(master=dialog_window, text="Нет", text_color="#fff5f0", font=my_font, command=answer_no,
                              fg_color="#cd8921", hover_color="#a26c1a")
    rows, columns = 2, 2
    for i in range(rows):
        dialog_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        dialog_window.columnconfigure(index=i, weight=1)
    label_clear.grid(row=0, column=0, columnspan=2)
    button_yes.grid(row=1, column=0)
    button_no.grid(row=1, column=1)


def choose_button(value):
    global segmented_button
    # взлом класса CTkSegmentedButton для изменения поведения сегментированной кнопки
    # по умолчанию она ведёт себя как переключатель, а мне нужны три самостоятельные кнопки
    segmented_button._unselect_button_by_value(value)
    segmented_button._current_value = ""

    if value == "+":
        add_purchase()
    elif value == "-":
        delete_purchase()
    elif value == "x":
        clear_all()


# перед началом работы приложения загружаем данные
# в файле data.json данные записаны в словарь, где ключи - категории, значения - списки, которые имеют формат:
# ["дата", "покупка", цена]
# таким образом, data.json содержит всю историю трат, распределённую по категориям
with open(file="data.json", mode="r", encoding="utf-8") as file_in:
    data = json.load(file_in)

# первичная настройка графического интерфейса приложения
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.title("Финансовый калькулятор")
root.geometry("1000x600")
my_font = ctk.CTkFont(family="Tahoma", size=20)

# виджеты
frame_for_diagram = ctk.CTkFrame(master=root)  # рамка для диаграммы
label_period = ctk.CTkLabel(master=root, text="Период:", text_color="#fff5f0", font=my_font)
entry_start_period = ctk.CTkEntry(master=root, placeholder_text="дд.мм.гггг", placeholder_text_color="#c1b6ac",
                                  text_color="#fff5f0", font=my_font, justify="center", border_color="#cd8921")
label_dash = ctk.CTkLabel(master=root, text="-", text_color="#fff5f0", font=my_font)
entry_finish_period = ctk.CTkEntry(master=root, placeholder_text="дд.мм.гггг", placeholder_text_color="#c1b6ac",
                                   text_color="#fff5f0", font=my_font, justify="center", border_color="#cd8921")
button_done = ctk.CTkButton(master=root, text="Отобразить", text_color="#fff5f0", font=my_font, width=420,
                            command=display, fg_color="#cd8921", hover_color="#a26c1a")
label_history = ctk.CTkLabel(master=root, text="История расходов:", text_color="#fff5f0", font=my_font)
scrollable_frame = ctk.CTkScrollableFrame(master=root, width=420, height=300, border_width=2, border_color="#cd8921",
                                          scrollbar_button_color="#90867e", scrollbar_button_hover_color="#716963")
segmented_button = ctk.CTkSegmentedButton(master=root, text_color="#fff5f0", font=ctk.CTkFont(family="Tahoma", size=40),
                                          command=choose_button, fg_color="#716963", corner_radius=50,
                                          unselected_color="#90867e", unselected_hover_color="#cd8921",
                                          selected_color="#cd8921", selected_hover_color="#a26c1a", values=["+", "-", "x"])

# глобальная сетка
rows, columns = 10, 10
for i in range(rows):
    root.rowconfigure(index=i, weight=1)
for i in range(columns):
    root.columnconfigure(index=i, weight=1)
frame_for_diagram.grid(row=0, rowspan=10, column=0, columnspan=5)
label_period.grid(row=0, column=5, columnspan=5, pady=(30, 2.5))
entry_start_period.grid(row=1, column=5, columnspan=2, pady=2.5)
label_dash.grid(row=1, column=7, pady=2.5)
entry_finish_period.grid(row=1, column=8, columnspan=2, pady=2.5)
button_done.grid(row=2, column=5, columnspan=5, pady=2.5)
label_history.grid(row=3, column=5, columnspan=5, pady=2.5)
scrollable_frame.grid(row=4, rowspan=5, column=5, columnspan=5, pady=2.5)
segmented_button.grid(row=9, column=5, columnspan=5, pady=(2.5, 5), ipadx=50, ipady=5)

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
fig = plt.figure(figsize=(5, 5.8), facecolor="#242424")
ax = fig.add_subplot(111)

# встраиваем фигуру fig в рамку frame с помощью canvas
canvas = FigureCanvasTkAgg(fig, master=frame_for_diagram)
canvas.get_tk_widget().pack(fill="both", expand=True)
# на старте отрисовываем диаграмму
redraw_diagram(labels, values)

# на старте отображаем загруженную историю трат за весь период
ctk.CTkLabel(master=scrollable_frame, text="За весь период:", text_color="#fff5f0", font=my_font).pack()
if labels == ["Ничего"]:
    ctk.CTkLabel(master=scrollable_frame, text="Нет трат", text_color="#fff5f0", font=my_font).pack()
else:
    pos = 1
    for category, info in data.items():
        if len(info) == 0:
            continue
        ctk.CTkLabel(master=scrollable_frame, text=f"{category}:", text_color="#fff5f0", font=my_font).pack()
        for day, purchase, price in info:
            ctk.CTkLabel(master=scrollable_frame,
                         text=f"{pos}. {day} - {purchase} - {price}р.", text_color="#fff5f0", font=my_font).pack()
            pos += 1

plt.close()  # завершает процессы, связанные с графиками
root.mainloop()

# после завершения работы приложения сохраняем данные
with open(file="data.json", mode="w", encoding="utf-8") as file_out:
    json.dump(data, file_out, indent=2, ensure_ascii=False)
