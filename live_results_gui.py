import tkinter as tk
from tkinter import ttk
from voting import get_live_results


class LiveResultsGUI(tk.Tk):
    def __init__(self, refresh_interval=5000):
        super().__init__()
        self.tree = None
        self.title("Real-Time Voting Results")
        self.geometry("400x300")
        self.refresh_interval = refresh_interval  # in milliseconds
        self.create_widgets()
        self.update_results()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("Party", "Votes"), show="headings")
        self.tree.heading("Party", text="Party")
        self.tree.heading("Votes", text="Votes")
        self.tree.column("Party", anchor="center")
        self.tree.column("Votes", anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def update_results(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
        results = get_live_results()
        if results:
            for party, votes in results:
                self.tree.insert("", "end", values=(party, votes))
        else:
            self.tree.insert("", "end", values=("No Data", 0))
        self.after(self.refresh_interval, self.update_results)


def run_live_results_gui():
    app = LiveResultsGUI()
    app.mainloop()


if __name__ == "__main__":
    run_live_results_gui()
