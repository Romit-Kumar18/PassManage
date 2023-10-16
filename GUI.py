import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from Profile import verify_profile, passfile_store, passfile_retrieve, save_profile
from PGen import random_generation


class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager App")

        self.notebook = ttk.Notebook(self)

        # Create and add tabs
        self.signup_tab = SignupTab(self.notebook)
        self.login_tab = LoginTab(self.notebook, self)
        self.generate_tab = GenerateTab(self.notebook)
        self.password_tab = PasswordTab(self.notebook, self)

        self.notebook.add(self.signup_tab, text="Sign Up")
        self.notebook.add(self.login_tab, text="Log In")
        self.notebook.add(self.password_tab, text="Password Manager")
        self.notebook.add(self.generate_tab, text="Generate Password")

        self.current_user = None  # To store the current user ID

        self.notebook.pack(expand=True, fill="both")

    def show_password_tab(self, user_id):
        self.current_user = user_id
        self.notebook.select(self.password_tab)
    def show_login_tab(self):
        self.notebook.select(self.login_tab)


class SignupTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.user_label = ttk.Label(self, text="Username:")
        self.user_label.pack(pady=10)

        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(pady=10)

        self.pass_label = ttk.Label(self, text="Password:")
        self.pass_label.pack(pady=10)

        self.pass_entry = ttk.Entry(self, show="*")
        self.pass_entry.pack(pady=10)

        self.signup_button = ttk.Button(self, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=20)

    def signup(self):
        user_id = self.user_entry.get()
        passwd = self.pass_entry.get()

        save_profile(user_id, passwd)
        messagebox.showinfo("Sign Up", "Sign Up successful!")

        # After successful signup, switch to the login tab
        app = self.winfo_toplevel()  # Access the top-level window
        app.show_login_tab()


class LoginTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Reference to the main app
        self.user_label = ttk.Label(self, text="Username:")
        self.user_label.pack(pady=10)

        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(pady=10)

        self.pass_label = ttk.Label(self, text="Password:")
        self.pass_label.pack(pady=10)

        self.pass_entry = ttk.Entry(self, show="*")
        self.pass_entry.pack(pady=10)

        self.login_button = ttk.Button(self, text="Log In", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        user_id = self.user_entry.get()
        passwd = self.pass_entry.get()

        if verify_profile(user_id, passwd):
            self.app.show_password_tab(user_id)
            messagebox.showinfo("Log In", "Login successful!")
        else:
            messagebox.showerror("Log In", "Login failed!")


class PasswordTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Reference to the main app

        self.label_entry = ttk.Entry(self)
        self.label_entry.pack(pady=10)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=10)

        self.save_button = ttk.Button(self, text="Save Password", command=self.save_password)
        self.save_button.pack(pady=10)

        self.retrieve_button = ttk.Button(self, text="Retrieve Password", command=self.retrieve_password)
        self.retrieve_button.pack(pady=10)

    def save_password(self):
        if self.app.current_user:
            user_id = self.app.current_user
            label = self.label_entry.get()
            stored_passwd = self.password_entry.get()

            passfile_store(user_id, label, stored_passwd)
            messagebox.showinfo("Password Saved", "Password saved successfully!")
        else:
            messagebox.showerror("Error", "Please log in before saving a password!")

    def retrieve_password(self):
        if self.app.current_user:
            user_id = self.app.current_user
            label = self.label_entry.get()

            retrieved_password = passfile_retrieve(user_id, label)
            pyperclip.copy(retrieved_password)
            messagebox.showinfo("Retrieved Password", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "Please log in before retrieving a password!")


class GenerateTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent.winfo_toplevel()

        self.length_label = ttk.Label(self, text="Password Length:")
        self.length_label.pack(pady=10)

        self.length_entry = ttk.Entry(self)
        self.length_entry.pack(pady=10)

        self.uppercase_var = tk.IntVar()
        self.uppercase_check = ttk.Checkbutton(self, text="Uppercase", variable=self.uppercase_var)
        self.uppercase_check.pack(pady=5)

        self.lowercase_var = tk.IntVar()
        self.lowercase_check = ttk.Checkbutton(self, text="Lowercase", variable=self.lowercase_var)
        self.lowercase_check.pack(pady=5)

        self.number_var = tk.IntVar()
        self.number_check = ttk.Checkbutton(self, text="Numbers", variable=self.number_var)
        self.number_check.pack(pady=5)

        self.symbol_var = tk.IntVar()
        self.symbol_check = ttk.Checkbutton(self, text="Symbols", variable=self.symbol_var)
        self.symbol_check.pack(pady=5)

        self.generate_button = ttk.Button(self, text="Generate Password", command=self.generate_and_copy)
        self.generate_button.pack(pady=10)

    def generate_and_copy(self):
        length = int(self.length_entry.get())
        Uchoice = self.uppercase_var.get()
        Lchoice = self.lowercase_var.get()
        Nchoice = self.number_var.get()
        Schoice = self.symbol_var.get()

        if self.app.current_user:
            password = random_generation(length, Uchoice, Lchoice, Nchoice, Schoice)
            if password:
                pyperclip.copy(password)
                messagebox.showinfo("Copy to Clipboard", "Password copied to clipboard!")
            else:
                messagebox.showerror("Error", "Password generation failed!")
        else:
            messagebox.showerror("Error", "Please log in before generating a password!")


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
