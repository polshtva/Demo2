import datetime
from tkinter import *
from tkinter import ttk, messagebox
import pyodbc as py
from tkinter import Tk, Label, Entry, OptionMenu, StringVar, Button, messagebox

def open_windowTask(user_id):
    new_windowTask = Tk()
    new_windowTask.title("Добавить заявку")
    new_windowTask.attributes('-fullscreen', True)

    labels_entries = [
        ("Название оборудования", Entry),
        ("Тип неисправности", Entry),
        ("Описание проблемы", Text)
    ]
    entries = []
    for label_text, entry_type in labels_entries:
        label = Label(new_windowTask, text=label_text)
        label.pack()
        entry = entry_type(new_windowTask, bg='#fff', fg='#444')
        entry.pack()
        entries.append(entry)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    status_var = "В ожидании"
    employ_data = "Поиск работника"
    btn_save = Button(new_windowTask, text='Отправить заявку',
                      command=lambda: save_and_update_treeview(current_date, *entries, user_id, status_var, employ_data, new_windowTask))
    btn_save.pack()

    btn_close = Button(new_windowTask, text='Закрыть', command=lambda: closeWindow(new_windowTask))
    btn_close.pack()

def save_and_update_treeview(current_date, equipment_entry, type_server_entry, desc_server_entry, user_id, status, employ_data, new_windowTask):
    connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
    try:
        connection = py.connect(connectionStr)
        dbCursor = connection.cursor()
        dbCursor.execute("INSERT INTO Servers (Data_Server, Equipment, Type_Server, Desc_Server, Id_Client, Status_Server, Employ_Data) VALUES (?, ?, ?, ?, ?, ?, ?)", (current_date, equipment_entry.get(), type_server_entry.get(), desc_server_entry.get("1.0", "end-1c"), user_id, status, employ_data))
        connection.commit()
        connection.close()
        messagebox.showinfo("Успех", "Данные успешно добавлены.")
        closeWindow(new_windowTask)
    except py.Error as ex:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {ex}")

def open_window(user_id, title, role):
    new_window = Tk()
    new_window.title(title)
    new_window.attributes('-fullscreen', True)
    btn_save = Button(new_window, text='Создать заявку', command=lambda: open_windowTask(user_id))
    btn_save.pack()
    tree = ttk.Treeview(new_window, columns=("Id", "Date", "Equipment", "Type", "Description", "Client", "Status", "Employ_Data"), show="headings")
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
    tree.heading("Employ_Data", text="Сотрудник")
    tree.pack(fill="both", expand=True)
    connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
    connection = py.connect(connectionStr)
    dbCursor = connection.cursor()
    dbCursor.execute("SELECT Id_Server, Data_Server, Equipment, Type_Server, Desc_Server, Id_Client, Status_Server FROM Servers")
    rows = dbCursor.fetchall()
    for row in rows:
        if role == 1 or (role == 2 and row[5] == user_id):
            tree.insert("", "end", values=list(row))

    connection.close()
    update_table(tree, new_window, user_id, role)
    tree.bind("<Double-1>", lambda event: open_request_window(event, tree) if role == 1 else open_request_window_employ(event, tree) if role == 2 else open_request_window_manager(event, tree))

def open_request_window_employ(event, tree):
    request_data = tree.item(tree.selection()[0], "values") if tree.selection() else None
    if not request_data:
        messagebox.showinfo("Ошибка", "Не выбрана заявка для редактирования")
        return
    
    edit_window = Tk()
    edit_window.title("Редактировать заявку")

    def update_description():
        id_server, new_status, new_equipment, new_type = request_data[0], status_var.get(), equipment_entry.get(), type_server_entry.get()
        try:
            conn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes')
            cursor = conn.cursor()
            cursor.execute("UPDATE Servers SET Status_Server = ?, Equipment = ?, Type_Server = ? WHERE Id_Server = ?", (new_status, new_equipment, new_type, id_server))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Данные успешно обновлены.")
            edit_window.destroy()
        except py.Error as ex:
            messagebox.showerror("Ошибка", f"Ошибка при обновлении данных: {ex}")

    labels = ["ID:", "Дата:", "Название оборудования", "Тип", "Статус", "Описание:"]
    for i, label_text in enumerate(labels):
        Label(edit_window, text=label_text).grid(row=i, column=0)
    
    request_data_labels = [request_data[0], request_data[1], request_data[2], request_data[3], request_data[6], request_data[4]]
    for i, label_text in enumerate(request_data_labels):
        Label(edit_window, text=label_text).grid(row=i, column=1)

    status_var = StringVar(edit_window)
    status_var.set(request_data[6])
    status_dropdown = OptionMenu(edit_window, status_var, "в ожидании", "выполнено", "не выполнено")
    status_dropdown.grid(row=4, column=1)
    equipment_entry = Entry(edit_window, bg='#fff', fg='#444')
    equipment_entry.insert(0, request_data[2])
    equipment_entry.grid(row=2, column=1)
    type_server_entry = Entry(edit_window, bg='#fff', fg='#444')
    type_server_entry.insert(0, request_data[3])
    type_server_entry.grid(row=3, column=1)
    Button(edit_window, text="Сохранить изменения", command=update_description).grid(row=5, columnspan=2)
    Button(edit_window, text="Закрыть", command=edit_window.destroy).grid(row=6, columnspan=2)

def open_request_window_manager(event, tree):
    item = tree.selection()
    if not item:
        messagebox.showinfo("Ошибка", "Не выбрана заявка для назначения сотрудника")
        return
    request_data = tree.item(item, "values")
    if not request_data:
        messagebox.showinfo("Ошибка", "Не выбрана заявка для назначения сотрудника")
        return
    assign_window = Tk()
    assign_window.title("Назначить сотрудника")
    
    def assign_employee():
        selected_employee = employee_var.get()
        if not selected_employee:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите сотрудника.")
            return
        try:
            connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
            conn = py.connect(connectionStr)
            cursor = conn.cursor()
            cursor.execute("UPDATE Servers SET Employ_Data = ? WHERE Id_Server = ?", 
                           (selected_employee, request_data[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Сотрудник успешно назначен.")
            assign_window.destroy()
        except py.Error as ex:
            messagebox.showerror("Ошибка", f"Ошибка при назначении сотрудника: {ex}")
    try:
        connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
        conn = py.connect(connectionStr)
        cursor = conn.cursor()
        cursor.execute("SELECT Login FROM [User] WHERE Role = 2")
        employees = [row[0] for row in cursor.fetchall()]
        conn.close()
    except py.Error as ex:
        messagebox.showerror("Ошибка", f"Ошибка при загрузке данных о сотрудниках: {ex}")
        employees = []

    Label(assign_window, text="Выберите сотрудника:").grid(row=0, column=0, padx=5, pady=5)
    employee_var = StringVar(assign_window)
    employee_var.set(employees[0] if employees else "")
    employee_dropdown = OptionMenu(assign_window, employee_var, *employees)
    employee_dropdown.grid(row=0, column=1, padx=5, pady=5)
    Button(assign_window, text="Назначить сотрудника", command=assign_employee).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    Button(assign_window, text="Отмена", command=assign_window.destroy).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

def open_request_window(event, tree):
    request_data = tree.item(tree.selection()[0], "values") if tree.selection() else None
    if request_data:
        edit_window = Tk()
        edit_window.title("Редактировать заявку")
        def update_description():
            new_description = desc_server_entry.get("1.0", "end-1c")
            id_server = request_data[0]
            try:
                conn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes')
                cursor = conn.cursor()
                cursor.execute("UPDATE Servers SET Desc_Server = ? WHERE Id_Server = ?", (new_description, id_server))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Описание успешно обновлено.")
                edit_window.destroy()
            except py.Error as ex:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении описания: {ex}")
        Label(edit_window, text="ID:").grid(row=0, column=0)
        Label(edit_window, text=request_data[0]).grid(row=0, column=1)
        Label(edit_window, text="Дата:").grid(row=1, column=0)
        Label(edit_window, text=request_data[1]).grid(row=1, column=1)
        Label(edit_window, text="Оборудование:").grid(row=2, column=0)
        Label(edit_window, text=request_data[2]).grid(row=2, column=1)
        desc_server_label = Label(edit_window, text='Описание:').grid(row=3, column=0)
        desc_server_entry = Text(edit_window, height=5, width=50)
        desc_server_entry.insert("1.0", request_data[4])
        desc_server_entry.grid(row=3, column=1)
        Button(edit_window, text="Сохранить изменения", command=update_description).grid(row=4, columnspan=2)
        Button(edit_window, text="Закрыть", command=edit_window.destroy).grid(row=5, columnspan=2)
        edit_window.mainloop()
    else:
        messagebox.showinfo("Ошибка", "Не выбрана заявка для редактирования")

def update_table(tree, window, user_id, role):  
    try:
        connectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Account;Trusted_Connection=yes'
        conn = py.connect(connectionStr)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Servers")  # Выполнение SQL-запроса для получения данных
        data = cursor.fetchall()
        tree.delete(*tree.get_children()) # Очистка таблицы Tkinter
        for row in data: # Заполнение таблицы Tkinter новыми данными
            if user_id == row[5] or role == 2 or role == 3: # Преобразование каждой строки данных в список и добавление в Treeview
                tree.insert("", "end", values=list(row))
        conn.close() # Закрытие соединения с базой данных
    except py.Error as ex:
        print("Ошибка при подключении к базе данных:", ex)
    window.after(1000, lambda: update_table(tree, window, user_id, role)) # Вызов функции update_table через 1 секунду
    if(role == 1):
        tree.bind("<Double-1>", lambda event: open_request_window(event, tree))
    elif (role == 2):
        tree.bind("<Double-1>", lambda event: open_request_window_employ(event, tree)) 
    else:
        tree.bind("<Double-1>", lambda event: open_request_window_manager(event, tree))    

def closeWindow(window):
    window.destroy()

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
                open_window(user[0], 'Окно пользователя', role)
                closeWindow(window)
            elif role == 2:
                print("Добро пожаловать, {}!".format(username))
                open_window(user[0], 'Окно сотрудника', role)
                closeWindow(window)
            else:
                print("Добро пожаловать, {}!".format(username))
                open_window(user[0], 'Окно менеджера', role)
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

window = Tk()
window.title('Авторизация')
window.geometry("500x500")
window.resizable(False, False)
window.configure(background='white')
main_label = Label(window, text='Авторизация', bg="white", fg="green")
main_label.pack()
username_label = Label(window, text='Имя пользователя', bg="white", fg="white")
username_label.pack()
username_entry = Entry(window, bg='#fff', fg='#444')
username_entry.pack()
password_label = Label(window, text='Пароль',bg="white", fg="white")
password_label.pack()
password_entry = Entry(window, bg='#fff', fg='#444',show='*')
password_entry.pack()
show_password_var = IntVar()
show_password_checkbox = Checkbutton(window, text="Показать пароль", variable=show_password_var, command=toggle_password_visibility, bg="black", fg="green")
show_password_checkbox.pack()
send_btn = Button(window, text='Войти', command=auth, font=('Arial', 24), bg='green', fg='black', width=10, height=2 )
send_btn.pack()
window.mainloop()