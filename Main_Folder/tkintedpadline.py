import json
import tkinter as tk
from tkinter import filedialog

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
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

class TrafficConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Configuration")
        self.data = None

        self.scrollable_frame = ScrollableFrame(self.root)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.red_light_frame = self.create_section_frame("Red Light Line", 0)
        self.create_red_light_entries(self.red_light_frame)
        self.speed_test_frame = self.create_section_frame("Speed Test Line", 1)
        self.create_speed_test_entries(self.speed_test_frame)
        self.create_buttons()
        self.status = tk.Label(self.scrollable_frame.scrollable_frame, text="")
        self.status.grid(row=5, column=0, columnspan=2, pady=10)

    def create_section_frame(self, title, row):
        frame = tk.LabelFrame(self.scrollable_frame.scrollable_frame, text=title, padx=10, pady=10)
        frame.grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")
        return frame
    
    def create_red_light_entries(self, frame):
        self.red_line_start_x = self.create_entry(frame, "Red Line Start X:", 0, 0)
        self.red_line_start_y = self.create_entry(frame, "Red Line Start Y:", 0, 1)
        self.red_line_end_x = self.create_entry(frame, "Red Line End X:", 1, 0)
        self.red_line_end_y = self.create_entry(frame, "Red Line End Y:", 1, 1)

    def create_speed_test_entries(self, frame):
        self.green_line_start_x = self.create_entry(frame, "Green Line Start X:", 0, 0)
        self.green_line_start_y = self.create_entry(frame, "Green Line Start Y:", 0, 1)
        self.green_line_end_x = self.create_entry(frame, "Green Line End X:", 1, 0)
        self.green_line_end_y = self.create_entry(frame, "Green Line End Y:", 1, 1)
        self.blue_line_start_x = self.create_entry(frame, "Blue Line Start X:", 2, 0)
        self.blue_line_start_y = self.create_entry(frame, "Blue Line Start Y:", 2, 1)
        self.blue_line_end_x = self.create_entry(frame, "Blue Line End X:", 3, 0)
        self.blue_line_end_y = self.create_entry(frame, "Blue Line End Y:", 3, 1)

    def create_entry(self, frame, label_text, row, column, columnspan=1):
        label = tk.Label(frame, text=label_text)
        label.grid(row=row, column=column, padx=5, pady=5, sticky="e")
        entry = tk.Entry(frame)
        entry.grid(row=row, column=column + 1, padx=5, pady=5, columnspan=columnspan, sticky="w")
        return entry

    def create_buttons(self):
        button_frame = tk.Frame(self.scrollable_frame.scrollable_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        self.load_button = tk.Button(button_frame, text="Load JSON", command=self.load_json)
        self.load_button.grid(row=0, column=0, padx=10)
        self.save_button = tk.Button(button_frame, text="Save JSON", command=self.save_json)
        self.save_button.grid(row=0, column=1, padx=10)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            self.populate_entries()

    def populate_entries(self):
        if self.data:
            self.clear_entries()
            self.red_line_start_x.insert(0, self.data["red_light_line"]["red_line_start"]["x"])
            self.red_line_start_y.insert(0, self.data["red_light_line"]["red_line_start"]["y"])
            self.red_line_end_x.insert(0, self.data["red_light_line"]["red_line_end"]["x"])
            self.red_line_end_y.insert(0, self.data["red_light_line"]["red_line_end"]["y"])

            self.green_line_start_x.insert(0, self.data["speed_test_line"]["green_line_start"]["x"])
            self.green_line_start_y.insert(0, self.data["speed_test_line"]["green_line_start"]["y"])
            self.green_line_end_x.insert(0, self.data["speed_test_line"]["green_line_end"]["x"])
            self.green_line_end_y.insert(0, self.data["speed_test_line"]["green_line_end"]["y"])
            self.blue_line_start_x.insert(0, self.data["speed_test_line"]["blue_line_start"]["x"])
            self.blue_line_start_y.insert(0, self.data["speed_test_line"]["blue_line_start"]["y"])
            self.blue_line_end_x.insert(0, self.data["speed_test_line"]["blue_line_end"]["x"])
            self.blue_line_end_y.insert(0, self.data["speed_test_line"]["blue_line_end"]["y"])

    def clear_entries(self):
        self.red_line_start_x.delete(0, tk.END)
        self.red_line_start_y.delete(0, tk.END)
        self.red_line_end_x.delete(0, tk.END)
        self.red_line_end_y.delete(0, tk.END)
        self.green_line_start_x.delete(0, tk.END)
        self.green_line_start_y.delete(0, tk.END)
        self.green_line_end_x.delete(0, tk.END)
        self.green_line_end_y.delete(0, tk.END)
        self.blue_line_start_x.delete(0, tk.END)
        self.blue_line_start_y.delete(0, tk.END)
        self.blue_line_end_x.delete(0, tk.END)
        self.blue_line_end_y.delete(0, tk.END)

    def save_json(self):
        self.data = {
            "red_light_line": {
               "red_line_start": {"x": int(self.red_line_start_x.get()), "y": int(self.red_line_start_y.get())},
               "red_line_end": {"x": int(self.red_line_end_x.get()), "y": int(self.red_line_end_y.get())}
            },
            "speed_test_line": {
                "green_line_start": {"x": int(self.green_line_start_x.get()), "y": int(self.green_line_start_y.get())},
                "green_line_end": {"x": int(self.green_line_end_x.get()), "y": int(self.green_line_end_y.get())},
                "blue_line_start": {"x": int(self.blue_line_start_x.get()), "y": int(self.blue_line_start_y.get())},
                "blue_line_end": {"x": int(self.blue_line_end_x.get()), "y": int(self.blue_line_end_y.get())}
            },

        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
            self.status.config(text=f"Configuration saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficConfigGUI(root)
    root.mainloop()
