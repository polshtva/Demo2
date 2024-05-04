from tkinter import messagebox
import pyodbc
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import datetime
import threading
import time
import string
from datetime import datetime, timedelta

connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=bd_acc;Trusted_Connection=yes'
connection = pyodbc.connect(connectionString, autocommit=True)
dbCursor = connection.cursor()
dbClient =  connection.cursor()
dbService =  connection.cursor()
History =  connection.cursor()
login_attempts = 0
failed_attempts = 0
History = connection.cursor()
# History.execute("""
#     CREATE TABLE hist (
#         id INT IDENTITY(1,1) PRIMARY KEY,
#         timestamp DATETIME,
#         username VARCHAR(255),
#         status VARCHAR(50)
#     )
# """)



def open_order_form(info_window):
    info_window.withdraw()
    window_order_form = tk.Toplevel(info_window)
    window_order_form.geometry('600x350')
    window_order_form.config(bg='white')
    window_order_form.config(background="#DCEDC1")
    window_order_form.title("Открытие формы заказа")

    order_number_label = tk.Label(window_order_form, text="Номер заказа:", fg="#8DB441", bg="#DCEDC1", font="Bold")
    order_number_label.grid(row=0, column=0, padx=10, pady=10)

    order_number_entry = tk.Entry(window_order_form)
    order_number_entry.grid(row=0, column=1, padx=10, pady=10)

    dbClient.execute("SELECT Id_client FROM Client")
    client_data = dbClient.fetchall()
    client_data = [item[0] for item in client_data]

    client_label = tk.Label(window_order_form, text="Клиент:", fg="#8DB441", bg="#DCEDC1", font="Bold")
    client_label.grid(row=1, column=0, padx=10, pady=10)

    client_combobox = ttk.Combobox(window_order_form, values=client_data)
    client_combobox.grid(row=1, column=1, padx=10, pady=10)

    def add_order():
        order_number = order_number_entry.get()
        client = client_combobox.get()

        dbClient.execute("SELECT Id_service FROM Service")
        service_data = dbClient.fetchall()
        service_data = [item[0] for item in service_data]

        if order_number in service_data:
            messagebox.showinfo("Успех", "Заказ успешно создан!")
        else:
            messagebox.showinfo("Ошибка!", "Нет такой услуги")

    add_order_button = tk.Button(window_order_form, text="Добавить заказ", command=add_order)
    add_order_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def exit_form():
        window_order_form.destroy()
        info_window.deiconify()

    exit_button = tk.Button(window_order_form, text="Вернуться на главную страницу", command=exit_form)
    exit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def open_product_acceptance(info_window):
    info_window.withdraw()
    window_product_acceptance = tk.Toplevel(info_window)
    window_product_acceptance.geometry('600x350')
    window_product_acceptance.config(bg='white')
    window_product_acceptance.config(background="#DCEDC1")
    window_product_acceptance.title("Открытие формы приемки товара")

    order_number_label = tk.Label(window_product_acceptance, text="Номер заказа:", fg="#8DB441", bg="#DCEDC1", font="Bold")
    order_number_label.grid(row=0, column=0, padx=10, pady=10)

    order_number_entry = tk.Entry(window_product_acceptance)
    order_number_entry.grid(row=0, column=1, padx=10, pady=10)

    dbClient.execute("SELECT Id_client FROM Client")
    client_data = dbClient.fetchall()
    client_data = [item[0] for item in client_data]

    client_label = tk.Label(window_product_acceptance, text="Клиент:", fg="#8DB441", bg="#DCEDC1", font="Bold")
    client_label.grid(row=1, column=0, padx=10, pady=10)

    client_combobox = ttk.Combobox(window_product_acceptance, values=client_data)
    client_combobox.grid(row=1, column=1, padx=10, pady=10)

    def create_new_service():
        new_service_window = tk.Toplevel(window_product_acceptance)
        new_service_window.geometry('400x300')
        new_service_window.config(bg='white')
        new_service_window.title("Создание новой услуги")
        new_service_window.config(background="#DCEDC1")

        id__label = tk.Label(new_service_window, text="Номер услуги:", fg="#8DB441", bg="#DCEDC1", font="Bold")
        id__label.grid(row=0, column=0, padx=10, pady=10)

        id_entry = tk.Entry(new_service_window)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        id_service_label = tk.Label(new_service_window, text="ID услуги:", fg="#8DB441", bg="#DCEDC1", font="Bold")
        id_service_label.grid(row=1, column=0, padx=10, pady=10)

        id_service_entry = tk.Entry(new_service_window)
        id_service_entry.grid(row=1, column=1, padx=10, pady=10)

        name_service_label = tk.Label(new_service_window, text="Название услуги:", fg="#8DB441", bg="#DCEDC1", font="Bold")
        name_service_label.grid(row=2, column=0, padx=10, pady=10)

        name_service_entry = tk.Entry(new_service_window)
        name_service_entry.grid(row=2, column=1, padx=10, pady=10)

        cost_label = tk.Label(new_service_window, text="Стоимость:", fg="#8DB441", bg="#DCEDC1", font="Bold")
        cost_label.grid(row=3, column=0, padx=10, pady=10)

        cost_entry = tk.Entry(new_service_window)
        cost_entry.grid(row=3, column=1, padx=10, pady=10)

        def save_service():
            id =  id_entry.get()
            id_service = id_service_entry.get()
            name_service = name_service_entry.get()
            cost = cost_entry.get()

            # Save the new service details to the database (Service table)
            dbService.execute("INSERT INTO Service (ID, Name_sevice, Id_service, Cost) VALUES (?, ?, ?, ?)",
                  (id, name_service, id_service, cost))
            dbService.commit()

            messagebox.showinfo("Успех", "Новая услуга успешно создана!")

            new_service_window.destroy()

        save_button = tk.Button(new_service_window, text="Сохранить", command=save_service)
        save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def generate_order():
        order_number = order_number_entry.get()
        client = client_combobox.get()

        # Check if the order number exists in the Service table
        dbClient.execute("SELECT * FROM Service WHERE Id_service = ?", (order_number,))
        existing_order = dbClient.fetchone()

        if existing_order:
            messagebox.showinfo("Успех", "Заказ успешно сгенерирован!")
        else:
            create_new_service_button = tk.Button(window_product_acceptance, text="Создать новую услугу", command=create_new_service)
            create_new_service_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    generate_order_button = tk.Button(window_product_acceptance, text="Сформировать заказ", command=generate_order)
    generate_order_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    def exit_form():
        window_product_acceptance.destroy()
        info_window.deiconify()

    exit_button = tk.Button( window_product_acceptance, text="Вернуться на главную страницу", command=exit_form)
    exit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)



# Функция для управления пользователями
def open_user_management(info_window):
    info_window.withdraw()
    window_user_management = tk.Toplevel(info_window)
    window_user_management.geometry('1000x750')
    window_user_management.config(bg='white')
    window_user_management.config(background="#DCEDC1")
    window_user_management.title("Логика для управления пользователями")
    title_label = tk.Label(window_user_management, text="История входа пользователей", font=("Arial", 16), background="#DCEDC1", fg="black")
    title_label.pack(pady=10)

    sort_frame = tk.Frame(window_user_management, bg="#DCEDC1")
    sort_frame.pack(padx=10, pady=10, anchor="w")

    # Sorting variables
    sort_username_var = tk.StringVar()
    sort_date_var = tk.StringVar()

    def update_sorting(event=None):
        # Clear the Treeview before sorting
        treeview.delete(*treeview.get_children())

        # Fetch data from the login_history table
        History.execute("SELECT timestamp, username, status FROM hist")
        rows = History.fetchall()

        # Fetch and display sorted data based on selected options
        sort_username = sort_username_var.get()
        sort_date = sort_date_var.get()

        # Build the key functions for sorting based on selected options
        key_username = lambda row: row[1]  # Username column
        key_date = lambda row: row[0]  # Timestamp column

        # Sort the data based on selected options
        sorted_rows = rows

        if sort_username == "В алфавитном порядке":
            sorted_rows = sorted(sorted_rows, key=key_username)
        elif sort_username == "В обратном порядке":
            sorted_rows = sorted(sorted_rows, key=key_username, reverse=True)

        if sort_date == "По возрастанию":
            sorted_rows = sorted(sorted_rows, key=key_date)
        elif sort_date == "По убыванию":
            sorted_rows = sorted(sorted_rows, key=key_date, reverse=True)

        for row in sorted_rows:
            treeview.insert("", "end", values=(row[0],row[1],row[2]))

    # Combobox and label for sorting by username
    sort_username_label = tk.Label(sort_frame, text="Сортировка по логину:", background="#DCEDC1")
    sort_username_label.grid(row=0, column=0, sticky="w", pady=5)

    sort_username_combobox = ttk.Combobox(sort_frame, textvariable=sort_username_var, state="readonly")
    sort_username_combobox["values"] = ["Не сортировать", "В алфавитном порядке", "В обратном порядке"]
    sort_username_combobox.current(0)
    sort_username_combobox.grid(row=0, column=1, padx=10, sticky="w")
    sort_username_combobox.bind("<<ComboboxSelected>>", update_sorting)

    # Combobox and label for sorting by date
    sort_date_label = tk.Label(sort_frame, text="Сортировка по дате:", background="#DCEDC1")
    sort_date_label.grid(row=1, column=0, sticky="w", pady=5)

    sort_date_combobox = ttk.Combobox(sort_frame, textvariable=sort_date_var, state="readonly")
    sort_date_combobox["values"] = ["Не сортировать", "По возрастанию", "По убыванию"]
    sort_date_combobox.current(0)
    sort_date_combobox.grid(row=1, column=1, padx=10, sticky="w")
    sort_date_combobox.bind("<<ComboboxSelected>>", update_sorting)

    # Treeview setup
    treeview = ttk.Treeview(window_user_management)
    treeview["columns"] = ("Timestamp", "Username", "Status")
    treeview.column("#0", width=0, stretch="NO")
    treeview.column("Timestamp", width=150)
    treeview.column("Username", width=150)
    treeview.column("Status", width=150)

    # Add column headings
    treeview.heading("#0", text="", anchor="w")
    treeview.heading("Timestamp", text="Время")
    treeview.heading("Username", text="Логин пользователя")
    treeview.heading("Status", text="Статус")

    # Fetch data from the login_history table
    History.execute("SELECT timestamp, username, status FROM hist")
    rows = History.fetchall()

    for row in rows:
        treeview.insert("", "end", values=(row[0],row[1],row[2]))

    treeview.pack(expand=True, fill="both")

    def exit_form():
        window_user_management.destroy()
        info_window.deiconify()

    exit_button = tk.Button(window_user_management, text="Вернуться на главную страницу", command=exit_form)
    exit_button.pack(pady=10)

    window_user_management.mainloop()







# Функция для открытия окна с информацией о пользователе
def user_info_window(user):
    info_window = tk.Toplevel(root)
    info_window.geometry('600x350')
    info_window.config(bg='white')
    info_window.config(background="#DCEDC1")
    info_window.title("Информация о пользователе")

    username_label = tk.Label(info_window, text=f"Привет, {user}!", fg="#8DB441", bg="#DCEDC1", font="Bold")
    username_label.pack(pady=20)

    order_button = tk.Button(info_window, text="Форма заказа", command=lambda: open_order_form(info_window))
    order_button.pack(pady=10)

    product_acceptance_button = tk.Button(info_window, text="Форма приемки товара", command=lambda: open_product_acceptance(info_window))
    product_acceptance_button.pack(pady=10)


    user_management_button = tk.Button(info_window, text="Управление пользователями", command=lambda: open_user_management(info_window))
    user_management_button.pack(pady=10)

def login():
    global login_attempts
    username = username_entry.get() 
    password = password_entry.get()
    
    dbCursor.execute(f"SELECT role, fio, photo_path FROM accounts WHERE login='{username}' AND password='{password}'")
    user = dbCursor.fetchone()

    dbClient.execute(f"SELECT Fio, Login, Password FROM Client WHERE Login='{username}' AND Password='{password}'")
    user_client =  dbClient.fetchone()

    if user:
        if user:
        # Успешная авторизация
            login_attempts = 0
            History.execute(f"INSERT INTO hist (timestamp, username, status) VALUES (CURRENT_TIMESTAMP, '{username}', 'Успешно')")
            connection.commit()
            root.withdraw()
            user_info_window(user)
            username_entry.configure(state="disabled")
            password_entry.configure(state="disabled")
            login_button.configure(state="disabled")
            # Запуск таймера сессии в отдельном потоке
            session_thread = threading.Thread(target=update_session_duration)
            session_thread.start()


    else:
        if user_client:
            # Успешная авторизация клиента
            login_attempts = 0
            History.execute(f"INSERT INTO hist (timestamp, username, status) VALUES (CURRENT_TIMESTAMP, '{username}', 'Успешно')")
            connection.commit()
            root.withdraw()
            client_info_window(user_client)
            username_entry.configure(state="disabled")
            password_entry.configure(state="disabled")
            login_button.configure(state="disabled")
            # Запуск таймера сессии в отдельном потоке
            session_thread = threading.Thread(target=update_session_duration)
            session_thread.start()
        else:
            # Неуспешная авторизация
            login_attempts += 1
            if login_attempts >= 2:
                messagebox.showwarning("Неуспешная авторизация", "Слишком много неудачных попыток авторизации. Пожалуйста, подождите некоторое время перед следующей попыткой.")
                History.execute(f"INSERT INTO hist (timestamp, username, status) VALUES (CURRENT_TIMESTAMP, '{username}', 'Неуспешно')")
                connection.commit()
                user_captcha()
            else:
                messagebox.showerror("Ошибка авторизации", "Неверное имя пользователя или пароль.")
                History.execute(f"INSERT INTO hist (timestamp, username, status) VALUES (CURRENT_TIMESTAMP, '{username}', 'Неуспешно')")
                connection.commit()


def generate_captcha():
    characters = string.ascii_letters + string.digits
    captcha = ''.join(random.sample(characters, k=3))
    captcha = ''.join(random.choice([captcha, f"{captcha[0]} {captcha[1]} {captcha[2]}"]))  # Добавление шума
    return captcha

def check_captcha(captcha_number, captcha_input, captcha_window, text_label, check_button):
    global failed_attempts

    if captcha_input.get() == captcha_number:
        messagebox.showinfo(title="Результат", message="Капча пройдена. Попробуйте авторизироваться ещё раз.", parent=captcha_window)
        captcha_window.destroy()
    else:
        failed_attempts += 1

        if failed_attempts >= 3:
            check_button.config(state="disabled")
            captcha_input.config(state="disabled")
            messagebox.showwarning(title="Результат", message="Неправильный ответ на капчу. Вход заблокирован на 10 секунд.", parent=captcha_window)
            time.sleep(10)
            check_button.config(state="normal")
            captcha_input.config(state="normal")
            failed_attempts = 0
            regenerate_captcha(captcha_input, text_label, check_button, captcha_window)
        else:
            messagebox.showwarning(title="Результат", message="Неправильный ответ на капчу. Попробуйте еще раз.", parent=captcha_window)
            regenerate_captcha(captcha_input, text_label, check_button, captcha_window)
            captcha_number = generate_captcha()
            text_label.config(text=f'Напишите {captcha_number}')

def regenerate_captcha(captcha_input, text_label, check_button, captcha_window):
    captcha_number = generate_captcha()
    text_label.config(text=f'Напишите {captcha_number}')
    captcha_input.delete(0, tk.END)
    check_button.config(command=lambda: check_captcha(captcha_number, captcha_input, captcha_window, text_label, check_button))

def user_captcha():
    captcha_number = generate_captcha()
    captcha_window = tk.Toplevel(root)
    captcha_window.geometry('250x250')
    captcha_window.config(bg='white')
    captcha_window.title("Капча")
    captcha_window.config(background="#DCEDC1")

    captcha_window.attributes('-topmost', True)  

    frame = tk.Frame(captcha_window, bg='#DCEDC1')
    frame.pack(expand=True)

    text_label = tk.Label(frame, text=f'Напишите {captcha_number}', fg='#8DB441', bg='#DCEDC1', font="Bold")
    text_label.pack()

    captcha_input = tk.Entry(frame, width=30)
    captcha_input.pack()

    check_button = tk.Button(frame, text="Отправить", background='#8DB441')
    check_button.pack(pady=5, padx=10)  # Добавление отступа по вертикали и горизонтали
    regenerate_button = tk.Button(frame, text="Перегенерировать", background='#8DB441', command=lambda: regenerate_captcha(captcha_input, text_label, check_button, captcha_window))
    regenerate_button.pack(pady=5, padx=10)

    check_button.config(command=lambda: check_captcha(captcha_number, captcha_input, captcha_window, text_label, check_button))

    # Размещение frame по центру окна
    captcha_window.update()
    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()
    screen_width = captcha_window.winfo_screenwidth()
    screen_height = captcha_window.winfo_screenheight()
    x = (screen_width // 2) - (frame_width // 2)
    y = (screen_height // 2) - (frame_height // 2)
    captcha_window.geometry(f'+{x}+{y}')

    # Закрытие окна капчи после завершения основного окна
    captcha_window.protocol("WM_DELETE_WINDOW", root.destroy)

    # Захват фокуса на окне captcha_window
    captcha_window.grab_set()



def update_session_duration():
    session_duration = 1800  # Установите начальную продолжительность сессии в секундах

    while session_duration > 0:
        time.sleep(1)
        session_duration -= 1

    # Выполните действия по истечении срока действия сессии здесь


# Создайте поток для выполнения функции update_session_duration
session_thread = threading.Thread(target=update_session_duration)
session_thread.start()


# Функция для выхода из системы и блокировки входа на определенное время
def logout():
    username_entry.configure(state="normal")
    password_entry.configure(state="normal")
    login_button.configure(state="normal")
    error_label.configure(text="Ваш аккаунт заблокирован на 3 минуты.")
    root.after(3 * 60 * 1000, reset_login)

# Функция для сброса формы входа после истечения времени блокировки аккаунта
def reset_login():
    error_label.configure(text="")
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")

client_combobox = None
basket_treeview = None

    
def save_data():
    selected_user = client_combobox.get()  # Получение выбранного пользователя
    # if selected_user:
    #     database_name = f"{selected_user}_services.db"  # Имя базы данных для текущего пользователя
    #     create_service_table(database_name)  # Создание таблицы услуг для текущего пользователя

    #     connection_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=.;DATABASE={database_name};Trusted_Connection=yes'
    #     conn = pyodbc.connect(connection_str, autocommit=True)
    #     cursor = conn.cursor()

    #     # Очистка таблицы перед сохранением новых данных
    #     cursor.execute("DELETE FROM Service")

    #     # Получение данных из treeview и сохранение их в таблице Service
    #     for child in basket_treeview.get_children():
    #         values = basket_treeview.item(child)['values']
    #         cursor.execute("INSERT INTO Service VALUES (?, ?, ?, ?)", values)

    #     conn.close()

# Пример использования функции save_data

basket_items = []  # Global list to store the values added to the cart

def add_to_cart(treeview, basket_treeview):
    selected_item = treeview.focus()
    if selected_item:
        values = treeview.item(selected_item)['values']
        basket_items.append(values)  # Store the values in the basket_items list
        basket_treeview.insert("", "end", values=values)


def load_saved_cart_items(basket_treeview):
    for item in basket_items:
        basket_treeview.insert("", "end", values=item)

def open_user(info_window):
    info_window.withdraw()
    user_window = tk.Toplevel(info_window)
    user_window.geometry('600x650')
    user_window.config(bg='white')
    user_window.config(background="#DCEDC1")
    user_window.title("Услуги")
    style = ttk.Style()
    style.configure(".", font=("Times New Roman", 10))
    dbService.execute("SELECT ID, Name_sevice, Id_service, Cost FROM Service")
    service_data = dbService.fetchall()

    treeview = ttk.Treeview(user_window, columns=("ID", "Name_sevice", "Id_service", "Cost"))
    treeview.column("#0", width=0, stretch="NO")
    treeview.column("ID", anchor="center", width=50)
    treeview.column("Name_sevice", anchor="w", width=200)
    treeview.column("Id_service", anchor="center", width=100)
    treeview.column("Cost", anchor="center", width=160)

    treeview.heading("#0", text="", anchor="w")
    treeview.heading("ID", text="ID", anchor="center")
    treeview.heading("Name_sevice", text="Наименование услуги", anchor="w")
    treeview.heading("Id_service", text="Стоимость руб. за час", anchor="center")
    treeview.heading("Cost", text="Код услуги", anchor="center")

    for row in service_data:
        treeview.insert("", "end", values=(row[0], row[1], row[3], row[2]))

    treeview.pack(fill="both", expand=True)

    basket_label = tk.Label(user_window, text="Ваша корзина", font=("Times New Roman", 12, "bold"), bg="#DCEDC1")
    basket_label.pack(pady=10)
    
    basket_treeview = ttk.Treeview(user_window, columns=("ID", "Name_sevice", "Id_service", "Cost"))
    basket_treeview.column("#0", width=0, stretch="NO")
    basket_treeview.column("ID", anchor="center", width=50)
    basket_treeview.column("Name_sevice", anchor="w", width=200)
    basket_treeview.column("Id_service", anchor="center", width=100)
    basket_treeview.column("Cost", anchor="center", width=160)

    basket_treeview.heading("#0", text="", anchor="w")
    basket_treeview.heading("ID", text="ID", anchor="center")
    basket_treeview.heading("Name_sevice", text="Наименование услуги", anchor="w")
    basket_treeview.heading("Id_service", text="Стоимость руб. за час", anchor="center")
    basket_treeview.heading("Cost", text="Код услуги", anchor="center")


    load_saved_cart_items(basket_treeview)  # Pass basket_treeview as an argument

    basket_treeview.pack(fill="both", expand=True)


    def remove_from_cart():
        selected_item = basket_treeview.focus()
        if selected_item:
            basket_treeview.delete(selected_item)

    def clear_cart():
        basket_treeview.delete(*basket_treeview.get_children())

    def return_to_main():   
        user_window.destroy()
        info_window.deiconify() 


    buttons_frame = tk.Frame(user_window, bg="#DCEDC1")
    buttons_frame.pack(pady=10)

    add_to_cart_button = tk.Button(buttons_frame, text="Добавить в корзину",  command=lambda: add_to_cart(treeview, basket_treeview), background="#8affbd")
    add_to_cart_button.pack(side="left", padx=10)

    remove_from_cart_button = tk.Button(buttons_frame, text="Удалить из корзины", command=remove_from_cart, background="#ff8a8a")
    remove_from_cart_button.pack(side="left", padx=10)

    clear_cart_button = tk.Button(buttons_frame, text="Очистить корзину", command=clear_cart, background="#ff8a8a")
    clear_cart_button.pack(side="left", padx=10)
    return_button = tk.Button(buttons_frame, text="Вернуться на главную", command=return_to_main)
    return_button.pack(side="left", padx=10)


    basket_treeview.pack(fill="both", expand=True)

def client_info_window(user_client):
    info_window = tk.Toplevel(root)
    info_window.geometry('600x350')
    info_window.config(bg='white')
    info_window.config(background="#DCEDC1")
    info_window.title("Информация пользователя")

    role = "Клиент"
    fio = user_client[0]
    image_path = "anonymous.png"
    img = Image.open(image_path)
    img = img.resize((200, 200))

    photo = ImageTk.PhotoImage(img)
    photo_label = tk.Label(info_window, image=photo)
    photo_label.image = photo
    photo_label.pack()

    label_role = tk.Label(info_window, text="Роль пользователя: " + role, background="#DCEDC1")
    label_role.pack()

    label_fio = tk.Label(info_window, text="ФИО: " + fio, background="#DCEDC1")
    label_fio.pack()

   

    # Расчет оставшегося времени сеанса
    session_start_time = datetime.now()
    session_end_time = session_start_time + timedelta(minutes=150)  # Длительность сеанса - 2 часа 30 минут

    def update_session_time():
        remaining_time = session_end_time - datetime.now()
        time_string = str(remaining_time).split('.')[0]  
        time_label.config(text="Оставшееся время: " + time_string)

        if remaining_time <= timedelta(minutes=15) and remaining_time > timedelta():  
           
            if not hasattr(update_session_time, "warning_shown"):
                messagebox.showinfo("Предупреждение", "Осталось 15 минут до окончания сеанса!")
                update_session_time.warning_shown = True  

        if remaining_time <= timedelta():  
            info_window.destroy()
            logout()  

        info_window.after(1000, update_session_time)  

    time_label = tk.Label(info_window, text="Оставшееся время: ", background="#DCEDC1")
    time_label.pack()

    update_session_time()  # Начать обновление времени

    client_button = tk.Button(info_window, text="Посмотреть услуги", command=lambda: open_user(info_window), background="#8affbd")
    client_button.pack() 
    exit_button = tk.Button(info_window, text="Выход", command=lambda: exit_to_root(info_window, root), background="#ff8a8a")
    exit_button.pack(side='bottom')

   
    
def user_info_window(user):
    info_window = tk.Toplevel(root)
    info_window.geometry('600x600')
    info_window.config(bg='white')
    info_window.config(background="#DCEDC1")
    info_window.title("Информация пользователя")
    
    role = user[0]
    fio = user[1]
    photo_filename = user[2]
    photo_path = os.path.join(r"C:\Users\79123\Desktop\практика", photo_filename)
    # Display user photo
    image = Image.open(photo_path).resize((200, 200))
    photo = ImageTk.PhotoImage(image)
    photo_label = tk.Label(info_window, image=photo)
    photo_label.image = photo 
    photo_label.pack()
    label_role = tk.Label(info_window, text="Роль пользователя: " + role, background="#DCEDC1")
    label_role.pack()
    label_fio = tk.Label(info_window, text="ФИО: " + fio, background="#DCEDC1")
    label_fio.pack()
    session_start_time = datetime.now()
    session_end_time = session_start_time + timedelta(minutes=150)  # Длительность сеанса - 2 часа 30 минут

    def update_session_time():
        remaining_time = session_end_time - datetime.now()
        time_string = str(remaining_time).split('.')[0]  # Форматирование оставшегося времени в формат ЧЧ:ММ:СС
        time_label.config(text="Оставшееся время: " + time_string)

        if remaining_time <= timedelta(minutes=15):  # Показать сообщение, когда остается 15 минут
            messagebox.showinfo("Предупреждение", "Осталось 15 минут до окончания сеанса!")

        if remaining_time <= timedelta():  # Истекло время сеанса
            info_window.destroy()
            logout()  # Выполнение действий при выходе

        info_window.after(1000, update_session_time)  # Обновление времени каждую секунду

    time_label = tk.Label(info_window, text="Оставшееся время: ", background="#DCEDC1")
    time_label.pack()

    update_session_time()  # Начать обновление времени
    if role == 'Продавец':
        button_text = 'Сформировать заказ'
        button_command = lambda: open_order_form(info_window)
    elif role == 'Старший смены':
        button_text = 'Принять товар'
        button_command = lambda: open_product_acceptance(info_window)
    elif role == 'Администратор':
        button_text = 'Проконтролировать всех пользователей по истории входа'
        button_command = lambda:  open_user_management(info_window)
    

    action_button = tk.Button(info_window, text=button_text, command=button_command, background="#8affbd")
    action_button.pack()
    exit_button = tk.Button(info_window, text="Выход", command=lambda: exit_to_root(info_window, root), background="#ff8a8a")
    exit_button.pack(side='bottom')

def exit_to_root(info_window, root):
    info_window.destroy()
    root.deiconify()
    username_entry.configure(state="normal")  # Включить поле ввода логина
    password_entry.configure(state="normal")  # Включить поле ввода пароля
    username_entry.delete(0, tk.END)  # Очистить поле ввода логина
    password_entry.delete(0, tk.END)  # Очистить поле ввода пароля
    login_button.configure(state="normal") 

def show_password():
    global show_password_state
    if show_password_state:
        password_entry.configure(show="*")
        show_password_state = False
    else:
        password_entry.configure(show="")
        show_password_state = True

root = tk.Tk()
root.title('Лесопарк')
root.geometry('600x350')
root.config(bg='white')
root.config(background="#DCEDC1")

password_frame = tk.Frame(root, bg='#DCEDC1')
password_frame.place(relx=0.5, rely=0.5, anchor='center')

username_label = tk.Label(password_frame, text='Логин:', fg='#8DB441', bg='#DCEDC1', font="Bold")
username_label.grid(row=2, column=0)

username_entry = tk.Entry(password_frame, width=30)
username_entry.grid(row=3, column=0, columnspan=2)

password_label = tk.Label(password_frame, text='Пароль:', fg='#8DB441', bg='#DCEDC1', font="Bold")
password_label.grid(row=4, column=0)
password_entry = tk.Entry(password_frame, show='*', width=30)
password_entry.grid(row=5, column=0, columnspan=2)
show_password_state = False

show_image = ImageTk.PhotoImage(Image.open("show.png").resize((20, 20)))
show_button = tk.Button(password_frame, image=show_image, command=show_password)
show_button.grid(row=5, column=3, padx=5, pady=5)

login_button = tk.Button(password_frame, text='Войти', command=login, background='#8DB441')
login_button.grid(row=6, column=0, pady=5)

error_label = tk.Label(root, text="", fg='red', bg='#DCEDC1')
error_label.pack()

root.mainloop()
