import datetime
from tkinter import *
from tkinter import ttk, messagebox
import pyodbc as py
from PIL import Image, ImageTk
from tkinter import Tk, Label, Entry, OptionMenu, StringVar, Button, messagebox


def closeWindow(window):
    window.destroy()

def open_windowTask(user_id):
    new_windowTask = Tk()
    new_windowTask.title("Добавить заявку")
    new_windowTask.attributes('-fullscreen',True)
 
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    equipment_label = Label(new_windowTask, text='Название оборудования', font=label_font, **base_padding)
    equipment_label.pack()
    equipment_entry = Entry(new_windowTask, bg='#fff',fg='#444', font=font_entry)
    equipment_entry.pack()
    
    type_server_label = Label(new_windowTask, text='Тип неисправности', font=label_font, **base_padding)
    type_server_label.pack()
    type_server_entry = Entry(new_windowTask, bg='#fff', fg='#444', font=font_entry)
    type_server_entry.pack()
    
    desc_server_label = Label(new_windowTask, text='Описание проблемы', font=label_font, **base_padding)
    desc_server_label.pack()
    desc_server_entry = Text(new_windowTask, bg='#fff', fg='#444', font=font_entry, height=5)
    desc_server_entry.pack()
    
    status_var = "В ожидании"

    employ_data = "Поиск работника"
    btn_save = Button(new_windowTask, text='Отправить заявку', command=lambda: save_and_update_treeview(current_date, equipment_entry, type_server_entry, desc_server_entry, user_id, status_var, employ_data, new_windowTask))
    btn_save.pack()
    
    btn_close = Button(new_windowTask, text='Закрыть', command=lambda: closeWindow(new_windowTask))
    btn_close.pack()

def save_and_update_treeview(current_date, equipment_entry, type_server_entry, desc_server_entry, user_id, status, employ_data, new_windowTask):
    writeDataTask(current_date, equipment_entry.get(), type_server_entry.get(), desc_server_entry.get("1.0", "end-1c"), user_id, status, employ_data)
    closeWindow(new_windowTask)

def writeDataTask(data, equipment, type, desc, user_id, status, employ_data):
    connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
    connection = py.connect(connectionStr)
    dbCursor = connection.cursor()
    dbCursor.execute("INSERT INTO Servers (Data_Server, Equipment, Type_Server, Desc_Server, Id_Client, Status_Server, Employ_Data) VALUES (?, ?, ?, ?, ?, ?, ?)", (data, equipment, type, desc, user_id, status, employ_data))
    print("Данные добавились")
    connection.commit()
    connection.close()

def open_userwindow(user_id):
    new_windowUser = Tk()
    new_windowUser.title("Окно юзера")
    new_windowUser.attributes('-fullscreen',True)
    
    # Добавление кнопки создания заявки
    btn_save = Button(new_windowUser, text='Создать заявку', command=lambda: open_windowTask(user_id))
    btn_save.pack()
    
    # Создание и настройка Treeview
    tree = ttk.Treeview(new_windowUser, columns=("Id", "Date", "Equipment", "Type", "Description", "Client", "Status", "Employ_Data"), show="headings")
    
    tree.column("#0", width=0, stretch="NO")
    tree.column("Id", anchor="center", width=50)
    tree.column("Date", anchor="w", width=100)
    tree.column("Equipment", anchor="center", width=150)
    tree.column("Type", anchor="center", width=160)
    tree.column("Description", anchor="center", width=360)
    tree.column("Client", anchor="center", width=50)
    tree.column("Status", anchor="center", width=260)
    tree.column("Employ_Data", anchor="center", width=260)
    
    tree.heading("Id", text="ID")
    tree.heading("Date", text="Дата заявки")
    tree.heading("Equipment", text="Название оборудования")
    tree.heading("Type", text="Тип")
    tree.heading("Description", text="Описание")
    tree.heading("Client", text="Id клиент")
    tree.heading("Status", text="Статус")
    tree.heading("Employ_Data", text="Обслуживающий заявку")
    
    tree.pack(fill="both", expand=True)

    # Загрузка данных из базы данных и добавление только соответствующих user_id записей в Treeview
    connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
    connection = py.connect(connectionStr)
    dbCursor = connection.cursor()
    dbCursor.execute("SELECT Id_Server, Data_Server, Equipment, Type_Server, Desc_Server, Id_Client, Status_Server, Employ_Data FROM Servers")
    rows = dbCursor.fetchall()

    for row in rows:
        if row[5] == user_id:  # Проверяем, соответствует ли значение Client переданному user_id
            tree.insert("", "end", values=list(row))  # Используем список вместо кортежа

    connection.close()
    role = 1
    update_table(tree, new_windowUser, user_id, role)
    
    tree.bind("<Double-1>", lambda event: open_request_window(event, tree))

def open_menagerwindow(user_id):
    new_windowMenager = Tk()
    new_windowMenager.title("Окно менаджера")
    new_windowMenager.attributes('-fullscreen',True)
     # Добавление кнопки создания заявки
    btn_save = Button(new_windowMenager, text='Создать заявку', command=lambda: open_windowTask(user_id))
    btn_save.pack()
    
    # Создание и настройка Treeview
    tree = ttk.Treeview(new_windowMenager, columns=("Id", "Date", "Equipment", "Type", "Description", "Client", "Status", "Employ_Data"), show="headings")
    
    tree.column("#0", width=0, stretch="NO")
    tree.column("Id", anchor="center", width=50)
    tree.column("Date", anchor="w", width=100)
    tree.column("Equipment", anchor="center", width=150)
    tree.column("Type", anchor="center", width=160)
    tree.column("Description", anchor="center", width=360)
    tree.column("Client", anchor="center", width=50)
    tree.column("Status", anchor="center", width=260)
    tree.column("Employ_Data", anchor="center", width=260)
    
    tree.heading("Id", text="ID")
    tree.heading("Date", text="Дата заявки")
    tree.heading("Equipment", text="Название оборудования")
    tree.heading("Type", text="Тип")
    tree.heading("Description", text="Описание")
    tree.heading("Client", text="Id клиент")
    tree.heading("Status", text="Статус")
    tree.heading("Employ_Data", text="Обслуживающий заявку")
    
    tree.pack(fill="both", expand=True)

    # Загрузка данных из базы данных и добавление только соответствующих user_id записей в Treeview
    connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
    connection = py.connect(connectionStr)
    dbCursor = connection.cursor()
    dbCursor.execute("SELECT Id_Server, Data_Server, Equipment, Type_Server, Desc_Server, Id_Client, Status_Server, Employ_Data FROM Servers")
    rows = dbCursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=list(row))  # Используем список вместо кортежа

    connection.close()

    role = 3
    update_table(tree, new_windowMenager, user_id, role)
    tree.bind("<Double-1>", lambda event: open_request_window_menager(event, tree))

def get_user_logins_with_role_two():
    logins = []
    try:
        connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
        conn = py.connect(connectionStr)
        cursor = conn.cursor()
        cursor.execute("SELECT Login FROM Users WHERE Role = 2")
        rows = cursor.fetchall()
        for row in rows:
            logins.append(row[0])
        conn.close()
    except py.Error as ex:
                messagebox.showerror("Ошибка", f"Ошибка при получении логинов: {ex}")
    return logins

def open_request_window_menager(event, tree):
    item = tree.selection()[0]  # Получаем выбранный элемент
    request_data = tree.item(item, "values")  # Получаем данные о выбранной заявке
    if request_data:
        # Создаем новое окно для редактирования заявки
        edit_windowReq = Tk()
        edit_windowReq.title("Редактировать заявку")
        
        # Функция для обновления описания в базе данных
        def update_description():
            id_server = request_data[0]  # Получаем Id_Server
            new_status = status_var.get()  # Получаем выбранный статус
            new_equipment = equipment_entry.get()  # Получаем новое название оборудования
            new_type = type_server_entry.get()  # Получаем новый тип
            selected_login = user_var.get()  # Получаем выбранный логин
            try:
                connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
                conn = py.connect(connectionStr)
                cursor = conn.cursor()
                # Обновляем данные в базе данных
                cursor.execute("UPDATE Servers SET Status_Server = ?, Equipment = ?, Type_Server = ?, Employ_Data = ? WHERE Id_Server = ?", 
                            (new_status, new_equipment, new_type, selected_login, id_server))
                conn.commit()  # Применяем изменения
                conn.close()
                messagebox.showinfo("Успех", "Данные успешно обновлены.")
                edit_windowReq.destroy()  # Закрываем окно редактирования после успешного обновления
            except py.Error as ex:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении данных: {ex}")

        # Отображаем существующие данные в окне редактирования
        Label(edit_windowReq, text="ID:").grid(row=0, column=0)
        Label(edit_windowReq, text=request_data[0]).grid(row=0, column=1)
        
        Label(edit_windowReq, text="Дата:").grid(row=1, column=0)
        Label(edit_windowReq, text=request_data[1]).grid(row=1, column=1)
        
        equipment_label = Label(edit_windowReq, text='Название оборудования', font=label_font, **base_padding)
        equipment_label.grid(row=4, column=0)
        equipment_entry = Entry(edit_windowReq, bg='#fff',fg='#444', font=font_entry)
        equipment_entry.insert(0, request_data[2])  # Вставляем существующее название оборудования
        equipment_entry.grid(row=4, column=1)

        type_label = Label(edit_windowReq, text='Тип', font=label_font, **base_padding)
        type_label.grid(row=5, column=0)
        type_server_entry = Entry(edit_windowReq, bg='#fff', fg='#444', font=font_entry)
        type_server_entry.insert(0, request_data[3])  # Вставляем существующий тип
        type_server_entry.grid(row=5, column=1)

        status_label = Label(edit_windowReq, text='Статус', font=label_font, **base_padding)
        status_label.grid(row=6, column=0)
        status_var = StringVar(edit_windowReq)
        status_var.set(request_data[6])  # Устанавливаем существующий статус
        status_dropdown = OptionMenu(edit_windowReq, status_var, "в ожидании", "выполнено", "не выполнено")
        status_dropdown.grid(row=6, column=1)

        desc_server_label = Label(edit_windowReq, text='Описание:')
        desc_server_label.grid(row=7, column=0)
        Label(edit_windowReq, text=request_data[4]).grid(row=7, column=1)

      # Получаем логины пользователей с ролью 2
        user_logins = get_user_logins_with_role_two()

        # Устанавливаем первый логин по умолчанию
        user_var = StringVar(edit_windowReq)
        user_var.set(user_logins[0])

        # Создаем выпадающий список из логинов
        user_dropdown = OptionMenu(edit_windowReq, user_var, *user_logins)
        user_dropdown.grid(row=8, column=1)

        # Кнопка для сохранения изменений
        Button(edit_windowReq, text="Сохранить изменения", command=update_description).grid(row=8, columnspan=2)
        
        # Функция для закрытия окна редактирования
        def close_edit_window():
            edit_windowReq.destroy()
        
        # Кнопка для закрытия окна редактирования
        Button(edit_windowReq, text="Закрыть", command=close_edit_window).grid(row=9, columnspan=2)
        
        # Отображаем окно редактирования
        edit_windowReq.mainloop()
    else:
        messagebox.showinfo("Ошибка", "Не выбрана заявка для редактирования")

def open_employwindow(user_id):
    new_windowEmploy = Tk()
    new_windowEmploy.title("Окно сотрудника")
    new_windowEmploy.attributes('-fullscreen',True)
    
    # Добавление кнопки создания заявки
    btn_save = Button(new_windowEmploy, text='Создать заявку', command=lambda: open_windowTask(user_id))
    btn_save.pack()
    
    # Создание и настройка Treeview
    tree = ttk.Treeview(new_windowEmploy, columns=("Id", "Date", "Equipment", "Type", "Description", "Client", "Status"), show="headings")
    
    tree.column("#0", width=0, stretch="NO")
    tree.column("Id", anchor="center", width=50)
    tree.column("Date", anchor="w", width=100)
    tree.column("Equipment", anchor="center", width=150)
    tree.column("Type", anchor="center", width=160)
    tree.column("Description", anchor="center", width=360)
    tree.column("Client", anchor="center", width=50)
    tree.column("Status", anchor="center", width=260)
    tree.column("Employ_Data", anchor="center", width=260)
    
    tree.heading("Id", text="ID")
    tree.heading("Date", text="Дата заявки")
    tree.heading("Equipment", text="Название оборудования")
    tree.heading("Type", text="Тип")
    tree.heading("Description", text="Описание")
    tree.heading("Client", text="Id клиент")
    tree.heading("Status", text="Статус")
    
    tree.pack(fill="both", expand=True)

    # Загрузка данных из базы данных и добавление только соответствующих user_id записей в Treeview
    connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
    connection = py.connect(connectionStr)
    dbCursor = connection.cursor()
    dbCursor.execute("SELECT Id_Server, Data_Server, Equipment, Type_Server, Desc_Server, Id_Client, Status_Server FROM Servers")
    rows = dbCursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=list(row))  # Используем список вместо кортежа

    connection.close()

    role = 2
    update_table(tree, new_windowEmploy, user_id, role)
    tree.bind("<Double-1>", lambda event: open_request_window_employ(event, tree))

def open_request_window_employ(event, tree):
    item = tree.selection()[0]  # Получаем выбранный элемент
    request_data = tree.item(item, "values")  # Получаем данные о выбранной заявке
    if request_data:
        # Создаем новое окно для редактирования заявки
        edit_window = Tk()
        edit_window.title("Редактировать заявку")
        
        # Функция для обновления описания в базе данных
        def update_description():
            id_server = request_data[0]  # Получаем Id_Server
            new_status = status_var.get()  # Получаем выбранный статус
            new_equipment = equipment_entry.get()  # Получаем новое название оборудования
            new_type = type_server_entry.get()  # Получаем новый тип
            try:
                connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
                conn = py.connect(connectionStr)
                cursor = conn.cursor()
                # Обновляем данные в базе данных
                cursor.execute("UPDATE Servers SET Status_Server = ?, Equipment = ?, Type_Server = ? WHERE Id_Server = ?", 
                               ( new_status, new_equipment, new_type, id_server))
                conn.commit()  # Применяем изменения
                conn.close()
                messagebox.showinfo("Успех", "Данные успешно обновлены.")
                edit_window.destroy()  # Закрываем окно редактирования после успешного обновления
            except py.Error as ex:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении данных: {ex}")
        
        # Отображаем существующие данные в окне редактирования
        Label(edit_window, text="ID:").grid(row=0, column=0)
        Label(edit_window, text=request_data[0]).grid(row=0, column=1)
        
        Label(edit_window, text="Дата:").grid(row=1, column=0)
        Label(edit_window, text=request_data[1]).grid(row=1, column=1)
        
        equipment_label = Label(edit_window, text='Название оборудования', font=label_font, **base_padding)
        equipment_label.grid(row=4, column=0)
        equipment_entry = Entry(edit_window, bg='#fff',fg='#444', font=font_entry)
        equipment_entry.insert(0, request_data[2])  # Вставляем существующее название оборудования
        equipment_entry.grid(row=4, column=1)

        type_label = Label(edit_window, text='Тип', font=label_font, **base_padding)
        type_label.grid(row=5, column=0)
        type_server_entry = Entry(edit_window, bg='#fff', fg='#444', font=font_entry)
        type_server_entry.insert(0, request_data[3])  # Вставляем существующий тип
        type_server_entry.grid(row=5, column=1)

        status_label = Label(edit_window, text='Статус', font=label_font, **base_padding)
        status_label.grid(row=6, column=0)
        status_var = StringVar(edit_window)
        status_var.set(request_data[6])  # Устанавливаем существующий статус
        status_dropdown = OptionMenu(edit_window, status_var, "в ожидании", "выполнено", "не выполнено")
        status_dropdown.grid(row=6, column=1)

        desc_server_label = Label(edit_window, text='Описание:')
        desc_server_label.grid(row=7, column=0)
        Label(edit_window, text=request_data[4]).grid(row=7, column=1)

        # Кнопка для сохранения изменений
        Button(edit_window, text="Сохранить изменения", command=update_description).grid(row=8, columnspan=2)
        
        # Функция для закрытия окна редактирования
        def close_edit_window():
            edit_window.destroy()
        
        # Кнопка для закрытия окна редактирования
        Button(edit_window, text="Закрыть", command=close_edit_window).grid(row=9, columnspan=2)
        
        # Отображаем окно редактирования
        edit_window.mainloop()
    else:
        messagebox.showinfo("Ошибка", "Не выбрана заявка для редактирования")
 

def update_table(tree, window, user_id, role):
    try:
        connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
        conn = py.connect(connectionStr)
        cursor = conn.cursor()
        # Выполнение SQL-запроса для получения данных
        cursor.execute("SELECT * FROM Servers")
        data = cursor.fetchall()
        # Очистка таблицы Tkinter
        tree.delete(*tree.get_children())
        # Заполнение таблицы Tkinter новыми данными
        for row in data:
            # Преобразование каждой строки данных в список и добавление в Treeview
            if user_id == row[5] or role == 2 or role == 3:
                tree.insert("", "end", values=list(row))
        # Закрытие соединения с базой данных
        conn.close()
    except py.Error as ex:
        print("Ошибка при подключении к базе данных:", ex)

    # Вызов функции update_table через 5 секунд
    window.after(1000, lambda: update_table(tree, window, user_id, role))
    tree.bind("<Double-1>", lambda event: open_request_window(event, tree))


def open_request_window(event, tree):
    item = tree.selection()[0]  # Получаем выбранный элемент
    request_data = tree.item(item, "values")  # Получаем данные о выбранной заявке
    if request_data:
        # Создаем новое окно для редактирования заявки
        edit_window = Tk()
        edit_window.title("Редактировать заявку")
        
        # Функция для обновления описания в базе данных
        def update_description():
            new_description = desc_server_entry.get("1.0", "end-1c")  # Получаем обновленное описание
            id_server = request_data[0]  # Получаем Id_Server
            try:
                connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
                conn = py.connect(connectionStr)
                cursor = conn.cursor()
                # Обновляем описание в базе данных
                cursor.execute("UPDATE Servers SET Desc_Server = ? WHERE Id_Server = ?", (new_description, id_server))
                conn.commit()  # Применяем изменения
                conn.close()
                messagebox.showinfo("Успех", "Описание успешно обновлено.")
                edit_window.destroy()  # Закрываем окно редактирования после успешного обновления
            except py.Error as ex:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении описания: {ex}")
        
        # Отображаем существующие данные в окне редактирования
        Label(edit_window, text="ID:").grid(row=0, column=0)
        Label(edit_window, text=request_data[0]).grid(row=0, column=1)
        
        Label(edit_window, text="Дата:").grid(row=1, column=0)
        Label(edit_window, text=request_data[1]).grid(row=1, column=1)
        
        Label(edit_window, text="Оборудование:").grid(row=2, column=0)
        Label(edit_window, text=request_data[2]).grid(row=2, column=1)
        
        desc_server_label = Label(edit_window, text='Описание:')
        desc_server_label.grid(row=3, column=0)
        desc_server_entry = Text(edit_window, height=5, width=50)
        desc_server_entry.insert("1.0", request_data[4])  # Вставляем существующее описание
        desc_server_entry.grid(row=3, column=1)
    
        # Кнопка для сохранения изменений
        Button(edit_window, text="Сохранить изменения", command=update_description).grid(row=4, columnspan=2)
        
        # Функция для закрытия окна редактирования
        def close_edit_window():
            edit_window.destroy()
        
        # Кнопка для закрытия окна редактирования
        Button(edit_window, text="Закрыть", command=close_edit_window).grid(row=5, columnspan=2)
        
        # Отображаем окно редактирования
        edit_window.mainloop()
    else:
        messagebox.showinfo("Ошибка", "Не выбрана заявка для редактирования")

def auth():
    try:
        connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
        connection = py.connect(connectionStr, autocommit=True)
        dbCursor = connection.cursor()
        username = username_entry.get()
        password = password_entry.get()
        dbCursor.execute("SELECT * FROM [User] WHERE Login=? AND Password=?", (username, password))
        user = dbCursor.fetchone()

        if user:
            role = user[3]
            if role == 1:
                print("Добро пожаловать, {}!".format(username))
                open_userwindow(user[0])
                closeWindow(window)
            elif role == 2:
                print("Добро пожаловать, {}!".format(username))
                open_employwindow(user[0])
                closeWindow(window)
            else:
                print("Добро пожаловать, {}!".format(username))
                open_menagerwindow(user[0])
                closeWindow(window)
        else:
            messagebox.showerror("Ошибка", "Данные не найдены")
    except py.Error as e:
        print("Error during authentication:", e)
    finally:
        if dbCursor is not None:
            dbCursor.close()
        if connection is not None:
            connection.close()

def toggle_password_visibility():
    if show_password_var.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")            


def close_app(window):
    window.destroy()

window = Tk()
window.title('Авторизация')
window.attributes('-fullscreen',True)
window.resizable(False, False)
window.configure(background='black')

font_header = ('Arial', 35)
font_entry = ('Arial', 22)
label_font = ('Arial', 21)
base_padding = {'padx': 20, 'pady': 18}
header_padding = {'padx': 20, 'pady': 22}

close_img = Image.open("close.png")  # Подставьте ваше изображение
close_img = close_img.resize((50, 50), Image.LANCZOS)  # Используем LANCZOS вместо ANTIALIAS
close_img = ImageTk.PhotoImage(close_img)

close_btn = Button(window, image=close_img, command=lambda: close_app(window), bd=0, bg='black')
close_btn.image = close_img
close_btn.place(relx=1.0, rely=0.0, anchor="ne")


main_label = Label(window, text='Авторизация', font=font_header, justify=CENTER, **header_padding, bg="black", fg="green")
main_label.pack()

username_label = Label(window, text='Имя пользователя', font=label_font, **base_padding, bg="black", fg="white")
username_label.pack()

username_entry = Entry(window, bg='#fff', fg='#444', font=font_entry)
username_entry.pack()

password_label = Label(window, text='Пароль', font=label_font, **base_padding, bg="black", fg="white")
password_label.pack()

password_entry = Entry(window, bg='#fff', fg='#444', font=font_entry, show='*')
password_entry.pack()

show_password_var = IntVar()
show_password_checkbox = Checkbutton(window, text="Показать пароль", variable=show_password_var, command=toggle_password_visibility, bg="black", fg="green")
show_password_checkbox.pack(**base_padding)

send_btn = Button(window, text='Войти', command=auth, font=('Arial', 24), bg='green', fg='black', width=10, height=2 )
send_btn.pack(**base_padding)


window.mainloop()