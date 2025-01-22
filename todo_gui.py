import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
import threading

BASE_URL = "http://localhost:5000/api/todos"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")
        self.root.geometry("600x400")
        self.setup_styles()
        self.create_widgets()
        self.load_todos()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom Colors
        self.bg_color = "#2D2D2D"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#4CAF50"
        self.delete_color = "#F44336"
        
        # Configure Styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TButton', 
                           background=self.accent_color, 
                           foreground=self.fg_color,
                           padding=5,
                           font=('Helvetica', 10, 'bold'))
        self.style.map('TButton',
                      background=[('active', '#45A049'), ('disabled', '#A5A5A5')])
        self.style.configure('Delete.TButton', background=self.delete_color)
        self.style.configure('TEntry', fieldbackground="#424242", foreground=self.fg_color)


        # Custom Checkbutton Style
        self.style.configure('Custom.TCheckbutton',
                            background=self.bg_color,
                            foreground=self.fg_color,
                            indicatorcolor=self.bg_color,
                            indicatordepth=1,
                            indicatorrelief='raised',
                            indicatorsize=14)
        self.style.map('Custom.TCheckbutton',
                      indicatorbackground=[('selected', self.accent_color), ('!selected', self.bg_color)],
                      indicatorcolor=[('selected', self.accent_color), ('!selected', self.bg_color)])



    def create_widgets(self):
        # Main Container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.header = ttk.Frame(self.main_frame)
        self.header.pack(fill=tk.X)
        ttk.Label(self.header, text="Todo List", font=('Helvetica', 18, 'bold')).pack(side=tk.LEFT)

        # Add Todo Section
        self.add_frame = ttk.Frame(self.main_frame)
        self.add_frame.pack(fill=tk.X, pady=10)
        
        self.new_todo = ttk.Entry(self.add_frame, width=40, font=('Helvetica', 12))
        self.new_todo.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        ttk.Button(
            self.add_frame, 
            text="＋ Add", 
            command=self.add_todo,
            style='TButton'
        ).pack(side=tk.LEFT)

        # Todo List Container
        self.list_container = ttk.Frame(self.main_frame)
        self.list_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        self.canvas = tk.Canvas(self.list_container, bg=self.bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def load_todos(self):
        # Clear existing todos
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Fetch todos from API
        try:
            response = requests.get(BASE_URL)
            todos = response.json()
        except requests.ConnectionError:
            messagebox.showerror("Error", "Could not connect to API")
            return

        # Create todo items
        for todo in todos:
            self.create_todo_item(todo)

    def create_todo_item(self, todo):
        frame = ttk.Frame(self.scrollable_frame)
        frame.todo_id = todo['id']
        frame.pack(fill=tk.X, pady=3)

        # Traditional Checkbutton
        self.var = tk.BooleanVar(value=todo['completed'])
        self.chk = ttk.Checkbutton(
            frame,
            variable=self.var,
            command=lambda: self.toggle_complete(todo, self.var),
            style='Custom.TCheckbutton'
        )
        self.chk.pack(side=tk.LEFT, padx=5)

        # Todo Title with strike-through capability
        self.title_font = font.Font(family='Helvetica', size=12)
        self.strike_font = font.Font(family='Helvetica', size=12, overstrike=1)
        
        self.title_label = ttk.Label(
            frame, 
            text=todo['title'],
            font=self.strike_font if todo['completed'] else self.title_font,
            foreground="#BDBDBD" if todo['completed'] else self.fg_color
        )
        self.title_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Edit Button
        ttk.Button(
            frame, 
            text="✎ Edit", 
            command=lambda t=todo: self.edit_todo(t),
            style='TButton'
        ).pack(side=tk.LEFT, padx=2)

        # Delete Button
        ttk.Button(
            frame, 
            text="🗑 Delete", 
            command=lambda t=todo: self.delete_todo(t),
            style='Delete.TButton'
        ).pack(side=tk.LEFT)

    def add_todo(self):
        title = self.new_todo.get()
        if not title:
            messagebox.showwarning("Warning", "Please enter a todo title")
            return

        try:
            response = requests.post(BASE_URL, json={'title': title})
            if response.status_code == 201:
                self.new_todo.delete(0, tk.END)
                self.load_todos()
        except requests.ConnectionError:
            messagebox.showerror("Error", "Could not connect to API")

    def edit_todo(self, todo):
        def save_edit():
            new_title = edit_entry.get()
            try:
                requests.put(
                    f"{BASE_URL}/{todo['id']}",
                    json={'title': new_title}
                )
                edit_win.destroy()
                self.load_todos()
            except requests.ConnectionError:
                messagebox.showerror("Error", "Could not connect to API")

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Todo")
        
        ttk.Label(edit_win, text="Edit Todo:").pack(padx=10, pady=5)
        edit_entry = ttk.Entry(edit_win, width=40)
        edit_entry.pack(padx=10, pady=5)
        edit_entry.insert(0, todo['title'])
        
        ttk.Button(edit_win, text="Save", command=save_edit).pack(pady=5)

    def delete_todo(self, todo):
        try:
            response = requests.delete(f"{BASE_URL}/{todo['id']}")
            if response.status_code == 200:
                self.load_todos()
        except requests.ConnectionError:
            messagebox.showerror("Error", "Could not connect to API")

    def toggle_complete(self, todo, var):
        #in case of error, revert to original state
        original_state = not var.get()
        new_state = var.get()
     
        self.update_todo_appearance(todo['id'], new_state)
        
        # API sync in background thread
        def api_call():
            try:
                response = requests.put(
                    f"{BASE_URL}/{todo['id']}",
                    json={'completed': new_state}
                )
                if not response.ok:
                    raise Exception("API update failed")
            except Exception as e:
                # Revert UI on error
                self.root.after(0, lambda: self.revert_todo_state(
                    todo['id'], original_state, var
                ))
                self.root.after(0, lambda: messagebox.showerror(
                    "Sync Error", 
                    f"Failed to save changes: {str(e)}"
                ))

        threading.Thread(target=api_call, daemon=True).start()

    def update_todo_appearance(self, todo_id, completed):
        # Update specific todo item
        for frame in self.scrollable_frame.winfo_children():
            if hasattr(frame, 'todo_id') and frame.todo_id == todo_id:
                children = frame.winfo_children()
                # Update checkbutton
                checkbutton = children[0]
                # Update label
                label = children[1]
                label.configure(
                    font=self.strike_font if completed else self.title_font,
                    foreground="#BDBDBD" if completed else self.fg_color
                )
                break


    def revert_todo_state(self, todo_id, original_state, var):
        var.set(original_state)
        self.update_todo_appearance(todo_id, original_state)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()