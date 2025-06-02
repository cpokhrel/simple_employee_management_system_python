import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import dbconnection


window = ctk.CTk()
window.title("Employee Management System")
window.geometry("900x420")
window.config(bg="#161C25")
window.resizable(False,False)

font1 = ("Arial",20,"bold")
font2 = ("Arial",12,"bold")

#Functions for data manipulation
def add_to_treeview():
    employees = dbconnection.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('',END,values=employee)

# Clear function
def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
    id_entry.delete(0,END)
    name_entry.delete(0,END)
    role_entry.delete(0,END)
    Variable1.set('Male')
    status_entry.delete(0,END)

#Insert function
def insert():
    id   = id_entry.get()
    name = name_entry.get()
    role = role_entry.get()
    gender = Variable1.get()
    status = status_entry.get()
    if not (id and name and role and gender and status):
        messagebox.showerror('Error', 'Enter all values')
    elif dbconnection.id_exists(id):
        messagebox.showerror('Error','ID already exists.')
    else:
        dbconnection.insert_employee(id,name,role,gender,status)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success','Data has been inserted.')

#Display data
def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        id_entry.insert(0,row[0])
        name_entry.insert(0,row[1])
        role_entry.insert(0,row[2])
        Variable1.set(row[3])
        status_entry.insert(0,row[4])
    else:
        pass

# Delete function
def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error','Chose and employee to delete.')
    else:
        id= id_entry.get()
        dbconnection.delete_employee(id)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success','Data has been deleted.')

# Update function
def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error','Select an employee to update.')
    else:
        id= id_entry.get()
        name = name_entry.get()
        role = role_entry.get()
        gender = Variable1.get()
        status = status_entry.get()
        dbconnection.update_employee(name,role,gender,status,id)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success','Data has been updated successfully.')

#Data entry section 
id_label = ctk.CTkLabel(window,font=font1,text="ID",text_color="#fff",bg_color="#161C25")
id_label.place(x=20,y=20)
id_entry = ctk.CTkEntry(window,font=font1,bg_color="#161C25")
id_entry.place(x=100,y=20)

name_label = ctk.CTkLabel(window,font=font1,text="Name",text_color="#fff",bg_color="#161C25")
name_label.place(x=20,y=80)
name_entry = ctk.CTkEntry(window,font=font1,bg_color="#161C25")
name_entry.place(x=100,y=80)

role_label = ctk.CTkLabel(window,font=font1,text="Role",text_color="#fff",bg_color="#161C25")
role_label.place(x=20,y=140)
role_entry = ctk.CTkEntry(window,font=font1,bg_color="#161C25")
role_entry.place(x=100,y=140)

gender_label = ctk.CTkLabel(window,font=font1,text="Gender",text_color="#fff",bg_color="#161C25")
gender_label.place(x=20,y=200)

options = ['Male','Female']
Variable1 = StringVar()

gender_options = ctk.CTkComboBox(window,font=font1,bg_color="#161C25",variable=Variable1,values=options,state='readonly')
gender_options.set('Male')
gender_options.place(x=100,y=200)

status_label = ctk.CTkLabel(window,font=font1,text="Status",text_color="#fff",bg_color="#161C25")
status_label.place(x=20,y=260)
status_entry = ctk.CTkEntry(window,font=font1,bg_color="#161C25")
status_entry.place(x=100,y=260)

#buttons widgets
add_button = ctk.CTkButton(window,command=insert,font=font1,text_color="#fff",bg_color="#161C25",text="Add Employee",cursor='hand2',width=260)
add_button.place(x=20,y=310)

clear_button = ctk.CTkButton(window,command=lambda:clear(True),font=font1,text_color="#fff",bg_color="#161C25",text="New Employee",cursor='hand2',width=260)
clear_button.place(x=20,y=360)

update_button = ctk.CTkButton(window,command=update,font=font1,text_color="#fff",bg_color="#161C25",text="Update Employee",cursor='hand2',width=260)
update_button.place(x=300,y=360)

delete_button = ctk.CTkButton(window,command=delete,font=font1,text_color="#fff",bg_color="#161C25",text="Delete Employee",cursor='hand2',width=260)
delete_button.place(x=580,y=360)

#Data display section
style = ttk.Style(window)
style.theme_use('clam')
style.configure('Treeview',font=font2,foreground='#fff',background='#000',fieldground='#313837')
style.map('Treeview',background=[('selected','#1A8F2D')])

tree = ttk.Treeview(window,height=15)
tree['columns']=('ID','Name','Role','Gender','Status')

tree.column('#0',width=0,stretch=tk.NO) #Hide the first column
tree.column('ID',anchor=tk.CENTER,width=120)
tree.column('Name',anchor=tk.CENTER,width=120)
tree.column('Role',anchor=tk.CENTER,width=120)
tree.column('Gender',anchor=tk.CENTER,width=120)
tree.column('Status',anchor=tk.CENTER,width=120)

#headings
tree.heading('ID',text='ID')
tree.heading('Name',text='Name')
tree.heading('Role',text='Role')
tree.heading('Gender',text='Gender')
tree.heading('Status',text='Status')

tree.place(x=400,y=20)

#tree bind
tree.bind('<<TreeviewSelect>>',display_data)
#End function
add_to_treeview()

#main loop
window.mainloop()