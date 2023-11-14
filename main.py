# ------------------------------------------
# Name: Reda Mohsen Reda
# Project Title: Dad Jokes Application
# Description: This is a simple GUI application that fetch a random dad joke or search for jokes
# ------------------------------------------
import requests
import tkinter as tk
from tkinter import messagebox
import logging


class DadJokes:
    def __init__(self, root):
        self.root = root
        root.title("Dad Joke Application")
        root.geometry("500x400")
        # Load the icon image file
        icon = tk.PhotoImage(file="assets/joking.png")
        # Set the icon for the window
        root.tk.call("wm", "iconphoto", root._w, icon)

        bg = "orange"
        fg = "blue"
        # Set the background color of the root window
        root.configure(bg=bg)

        self.input_frame = tk.Frame(root, padx=10, pady=10, bg=bg)
        self.input_frame.pack(side="top")

        input_search_label = tk.Label(self.input_frame, text="Search", padx=10, pady=10, bg=bg, fg=fg, font=("Arial", 14))
        input_search_label.grid(row=0, column=0, padx=10, pady=5)

        self.input_search_entry = tk.Entry(self.input_frame, width=20, fg=fg, font=("Arial", 12))
        self.input_search_entry.grid(row=0, column=1, padx=10, pady=5)

        buttons_frame = tk.Frame(self.root, padx=10, pady=10, bg=bg)
        buttons_frame.pack()

        search_button = tk.Button(buttons_frame, text="Search", padx=30, pady=5, fg=fg, font=("Arial", 12), command=self.on_search_button_selected)
        search_button.grid(row=0, column=0, padx=10, pady=5)

        random_button = tk.Button(buttons_frame, text="Random", padx=30, pady=5, fg=fg, font=("Arial", 12), command=self.on_random_button_selected)
        random_button.grid(row=0, column=1, padx=10, pady=5)

        self.output_frame = tk.Frame(self.root, padx=10, pady=10, bg=bg)
        self.output_frame.pack()

        self.jokes_listbox = tk.Listbox(self.output_frame, bg="white", fg="blue", font=("Arial", 12), width=300, height=200)
        self.jokes_listbox.pack()

        scrollbar = tk.Scrollbar(self.output_frame, command=self.jokes_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.jokes_listbox.config(yscrollcommand=scrollbar.set)

    def on_search_button_selected(self):
        try:
            term = self.get_search_term()
            if term:
                jokes = self.search_for_joke(term)
                if jokes:
                    self.show_jokes(jokes)
                else:
                    raise ValueError("Invalid Search Term!")
            else:
                raise ValueError("Invalid Search Term!")
        except ValueError as err:
            logging.error(f"ValueError occurred: {err}")
            messagebox.showerror("Error", err)

    def on_random_button_selected(self):
        try:
            random_joke = self.fetch_random_joke()
            if random_joke:
                self.show_joke(random_joke)
        except ValueError as err:
            logging.error(f"ValueError occurred: {err}")
            messagebox.showerror("Error", err)

    def get_search_term(self):
        return self.input_search_entry.get()


    def search_for_joke(self, term):
        try:
            headers = {"Accept": "application/json"}
            response = requests.get(f"https://icanhazdadjoke.com/search?term={term}", headers=headers)
            if response.status_code == 200:
                joke_data = response.json()
                jokes = [result["joke"] for result in joke_data.get("results", [])]
                return jokes
            else:
                raise ValueError(f"HTTP Request Failed: Error {response.status_code}")
        except Exception as err:
            raise ValueError(err)

    def fetch_random_joke(self):
        try:
            headers = {"Accept": "application/json"}
            response = requests.get("https://icanhazdadjoke.com/", headers=headers)
            if response.status_code == 200:
                joke_data = response.json()
                joke = joke_data.get("joke")
                return joke
            else:
                raise ValueError(f"HTTP Request Failed: Error {response.status_code}")
        except Exception as err:
            raise ValueError(err)

    def show_joke(self, joke):
        self.jokes_listbox.delete(0, tk.END)
        self.jokes_listbox.insert(tk.END, "* "+joke)

    def show_jokes(self, jokes):
        self.jokes_listbox.delete(0, tk.END)
        for joke in jokes:
            self.jokes_listbox.insert(tk.END, "* "+joke)


def main():
    root = tk.Tk()
    app = DadJokes(root)
    root.mainloop()


if __name__ == "__main__":
    main()

