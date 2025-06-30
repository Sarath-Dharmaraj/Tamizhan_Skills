import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import os

FILENAME = "tasks.txt"

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task + "\n")

def refresh_tasks():
    selected_indices = [i for i, var in enumerate(checkbox_vars) if var.get()]
    for widget in task_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()

    for i, task in enumerate(tasks):
        is_done = task.startswith("[✓]")
        selected = (i in selected_indices or select_all_var.get())
        var = tk.BooleanVar(value=selected)
        display_text = task.replace("[✓] ", "")
        font_to_use = strike_font if is_done else normal_font

        checkbox = tk.Checkbutton(
            task_frame,
            text=display_text,
            variable=var,
            font=font_to_use,
            command=update_button_states
        )
        checkbox.pack(anchor="w", pady=2)
        checkbox_vars.append(var)

    update_button_states()

def add_task():
    task = entry.get().strip()
    if task:
        tasks.append(task)
        save_tasks(tasks)
        refresh_tasks()
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

def delete_task():
    to_delete = [i for i, var in enumerate(checkbox_vars) if var.get()]
    for index in reversed(to_delete):
        tasks.pop(index)
    save_tasks(tasks)
    refresh_tasks()

def edit_task():
    selected = [i for i, var in enumerate(checkbox_vars) if var.get()]
    if len(selected) == 1:
        new_text = entry.get().strip()
        if new_text:
            tasks[selected[0]] = new_text
            save_tasks(tasks)
            refresh_tasks()
            entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")

def mark_complete():
    for i, var in enumerate(checkbox_vars):
        if var.get() and not tasks[i].startswith("[✓]"):
            tasks[i] = "[✓] " + tasks[i]
    save_tasks(tasks)
    refresh_tasks()

def toggle_select_all():
    state = select_all_var.get()
    for var in checkbox_vars:
        var.set(state)
    update_button_states()

def update_button_states():
    selected_count = sum(var.get() for var in checkbox_vars)
    delete_btn.config(state="normal" if selected_count > 0 else "disabled")
    complete_btn.config(state="normal" if selected_count > 0 else "disabled")
    edit_btn.config(state="normal" if selected_count == 1 else "disabled")

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# --- GUI Setup ---
tasks = load_tasks()
checkbox_vars = []

root = tk.Tk()
root.title("To-Do List App")
root.geometry("600x500")
root.resizable(False, False)

normal_font = tkfont.Font(family="Helvetica", size=10)
strike_font = tkfont.Font(family="Helvetica", size=10, overstrike=1)

select_all_var = tk.BooleanVar()
root.bind("<Return>", lambda event: add_task())

# Entry Frame
entry_frame = tk.LabelFrame(root, text="New Task", padx=10, pady=10)
entry_frame.pack(fill="x", padx=10, pady=(10, 0))

entry = tk.Entry(entry_frame, width=50, font=("Helvetica", 12))
entry.pack()
entry.focus()

# Main layout
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Task Frame Container
task_frame_container = tk.LabelFrame(main_frame, text="Tasks", padx=0, pady=0)
task_frame_container.pack(side="left", fill="both", expand=True, padx=(0, 5))

# Header with Select All
task_header = tk.Frame(task_frame_container)
task_header.pack(fill="x", pady=(0, 5), anchor="ne")

select_all_label = tk.Label(task_header, text="Select All")
select_all_label.pack(side="left")

select_all_cb = tk.Checkbutton(
    task_header,
    variable=select_all_var,
    command=toggle_select_all
)
select_all_cb.pack(side="left")

# Scrollable Task Frame
canvas = tk.Canvas(task_frame_container, borderwidth=0, highlightthickness=0)
scrollbar = tk.Scrollbar(task_frame_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.bind_all("<MouseWheel>", on_mousewheel)

task_frame = scrollable_frame

# Button Frame
button_frame = tk.Frame(main_frame)
button_frame.pack(side="right", fill="y")

add_btn = tk.Button(button_frame, text="Add", width=12, command=add_task)
add_btn.pack(pady=5)

edit_btn = tk.Button(button_frame, text="Edit", width=12, command=edit_task)
edit_btn.pack(pady=5)

delete_btn = tk.Button(button_frame, text="Delete", width=12, command=delete_task)
delete_btn.pack(pady=5)

complete_btn = tk.Button(button_frame, text="Complete", width=12, command=mark_complete)
complete_btn.pack(pady=5)

edit_btn.config(state="disabled")
delete_btn.config(state="disabled")
complete_btn.config(state="disabled")

refresh_tasks()
root.mainloop()