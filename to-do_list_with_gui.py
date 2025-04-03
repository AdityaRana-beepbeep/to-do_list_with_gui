import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
import threading
import time

def update_task_list():
    task_listbox.delete(0, tk.END)
    for i, t in enumerate(tasks, start=1):
        task_listbox.insert(tk.END, f"{i}. {t}")

def alert_checker():
    while True:
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")
        for t in tasks:
            if f"(Due: {current_time})" in t:
                root.after(0, show_notification, t)
                tasks.remove(t)
                root.after(0, update_task_list)
        time.sleep(60)

def show_notification(task):
    messagebox.showinfo("Reminder", f"Task Alert: {task}")

def add_new_task():
    task_text = task_entry.get().strip()
    task_date = date_entry.get()
    task_time = time_entry.get().strip()
    if task_text and task_time:
        due = f"(Due: {task_date} {task_time})"
        tasks.append(f"{task_text} {due}")
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        update_task_list()
        messagebox.showinfo("Success", "Task Added Successfully!")
    else:
        messagebox.showerror("Error", "Please enter both task and time!")

def remove_task():
    selected = task_listbox.curselection()
    if selected:
        task_name = tasks[selected[0]]
        tasks.pop(selected[0])
        update_task_list()
        messagebox.showinfo("Deleted", f"Task '{task_name}' removed successfully!")
    else:
        messagebox.showwarning("Warning", "Please select a task to remove!")

def close_app():
    root.destroy()

def update_clock():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    root.after(1000, update_clock)

tasks = []
root = tk.Tk()
root.title("TODO List")
root.geometry("450x550")
root.configure(bg="#e3f2fd")

threading.Thread(target=alert_checker, daemon=True).start()

tk.Label(root, text="👋 Welcome to Your TODO List!", font=("Arial", 14, "bold"), bg="#e3f2fd").pack(pady=10)

clock_label = tk.Label(root, font=("Arial", 12, "bold"), bg="#e3f2fd")
clock_label.pack()
update_clock()

tk.Label(root, text="Enter Task:", font=("Arial", 11), bg="#e3f2fd").pack(anchor='w', padx=20)
task_entry = tk.Entry(root, font=("Arial", 12), width=30)
task_entry.pack(pady=5, padx=20)

tk.Label(root, text="Select Date:", font=("Arial", 11), bg="#e3f2fd").pack(anchor='w', padx=20)
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
date_entry.pack(pady=5, padx=20)

tk.Label(root, text="Enter Time (HH:MM AM/PM):", font=("Arial", 11), bg="#e3f2fd").pack(anchor='w', padx=20)
time_entry = tk.Entry(root, font=("Arial", 12), width=10)
time_entry.pack(pady=5, padx=20)

tk.Button(root, text="➕ Add Task", font=("Arial", 12), bg="#64dd17", command=add_new_task).pack(pady=5, padx=20, fill=tk.X)
tk.Button(root, text="❌ Remove Task", font=("Arial", 12), bg="#ff1744", command=remove_task).pack(pady=5, padx=20, fill=tk.X)
tk.Button(root, text="🚪 Exit", font=("Arial", 12), bg="#ff6f00", command=close_app).pack(pady=5, padx=20, fill=tk.X)

task_listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=10, bd=1, relief=tk.FLAT)
task_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

update_task_list()
root.mainloop()
