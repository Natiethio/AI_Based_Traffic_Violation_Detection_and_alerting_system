import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw

import json

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
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class TrafficConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Configuration")
        self.data = None
        self.image = None
        self.image_label = None

        self.scrollable_frame = ScrollableFrame(self.root)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.create_widgets()
        
    def create_widgets(self):
        # Create a frame for each section and center-align the entries
        self.red_light_frame = self.create_section_frame("Red Light Line", 0)
        self.create_red_light_entries(self.red_light_frame)

        self.speed_test_frame = self.create_section_frame("Speed Test Line", 1)
        self.create_speed_test_entries(self.speed_test_frame)
        
        self.license_plate_frame = self.create_section_frame("License Plate Recognition", 2)
        self.create_license_plate_entries(self.license_plate_frame)
        
        self.lane_frame = self.create_section_frame("Lanes", 3)
        self.create_lane_entries(self.lane_frame)

        self.create_buttons()
        self.status = tk.Label(self.scrollable_frame.scrollable_frame, text="")
        self.status.grid(row=5, column=0, columnspan=2, pady=10)

    def create_section_frame(self, title, row):
        frame = tk.LabelFrame(self.scrollable_frame.scrollable_frame, text=title, padx=10, pady=10)
        frame.grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")
        return frame

    def create_red_light_entries(self, frame):
        self.red_light_start_x = self.create_entry(frame, "Start X:", 0, 0)
        self.red_light_start_y = self.create_entry(frame, "Start Y:", 0, 1)
        self.red_light_end_x = self.create_entry(frame, "End X:", 1, 0)
        self.red_light_end_y = self.create_entry(frame, "End Y:", 1, 1)

    def create_speed_test_entries(self, frame):
        self.speed_start_initial_x = self.create_entry(frame, "Start Initial X:", 0, 0)
        self.speed_start_initial_y = self.create_entry(frame, "Start Initial Y:", 0, 1)
        self.speed_end_initial_x = self.create_entry(frame, "End Initial X:", 1, 0)
        self.speed_end_initial_y = self.create_entry(frame, "End Initial Y:", 1, 1)
        self.speed_start_final_x = self.create_entry(frame, "Start Final X:", 2, 0)
        self.speed_start_final_y = self.create_entry(frame, "Start Final Y:", 2, 1)
        self.speed_end_final_x = self.create_entry(frame, "End Final X:", 3, 0)
        self.speed_end_final_y = self.create_entry(frame, "End Final Y:", 3, 1)

    def create_license_plate_entries(self, frame):
        self.license_top_left_x = self.create_entry(frame, "Top Left X:", 0, 0)
        self.license_top_left_y = self.create_entry(frame, "Top Left Y:", 0, 1)
        self.license_top_right_x = self.create_entry(frame, "Top Right X:", 1, 0)
        self.license_top_right_y = self.create_entry(frame, "Top Right Y:", 1, 1)
        self.license_bottom_left_x = self.create_entry(frame, "Bottom Left X:", 2, 0)
        self.license_bottom_left_y = self.create_entry(frame, "Bottom Left Y:", 2, 1)
        self.license_bottom_right_x = self.create_entry(frame, "Bottom Right X:", 3, 0)
        self.license_bottom_right_y = self.create_entry(frame, "Bottom Right Y:", 3, 1)

    def create_lane_entries(self, frame):
        self.lane_count_value = self.create_entry(frame, "Number of Lanes:", 0, 0, columnspan=2)
        self.lanes = []
        self.add_lane_button = tk.Button(frame, text="Add Lane", command=self.add_lane)
        self.add_lane_button.grid(row=1, column=0, pady=5)
        self.remove_lane_button = tk.Button(frame, text="Remove Lane", command=self.remove_lane)
        self.remove_lane_button.grid(row=1, column=1, pady=5)

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
        self.display_button = tk.Button(button_frame, text="Display on Image", command=self.display_on_image)
        self.display_button.grid(row=0, column=2, padx=10)
        self.load_image_button = tk.Button(button_frame, text="Load Image", command=self.load_image)
        self.load_image_button.grid(row=0, column=3, padx=10)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            self.populate_entries()

    def populate_entries(self):
        if self.data:
            self.clear_entries()
            self.red_light_start_x.insert(0, self.data["red_light_line"]["start"]["x"])
            self.red_light_start_y.insert(0, self.data["red_light_line"]["start"]["y"])
            self.red_light_end_x.insert(0, self.data["red_light_line"]["end"]["x"])
            self.red_light_end_y.insert(0, self.data["red_light_line"]["end"]["y"])

            self.speed_start_initial_x.insert(0, self.data["speed_test_line"]["start_initial"]["x"])
            self.speed_start_initial_y.insert(0, self.data["speed_test_line"]["start_initial"]["y"])
            self.speed_end_initial_x.insert(0, self.data["speed_test_line"]["end_initial"]["x"])
            self.speed_end_initial_y.insert(0, self.data["speed_test_line"]["end_initial"]["y"])
            self.speed_start_final_x.insert(0, self.data["speed_test_line"]["start_final"]["x"])
            self.speed_start_final_y.insert(0, self.data["speed_test_line"]["start_final"]["y"])
            self.speed_end_final_x.insert(0, self.data["speed_test_line"]["end_final"]["x"])
            self.speed_end_final_y.insert(0, self.data["speed_test_line"]["end_final"]["y"])

            self.license_top_left_x.insert(0, self.data["license_plate_recognition"]["top_left"]["x"])
            self.license_top_left_y.insert(0, self.data["license_plate_recognition"]["top_left"]["y"])
            self.license_top_right_x.insert(0, self.data["license_plate_recognition"]["top_right"]["x"])
            self.license_top_right_y.insert(0, self.data["license_plate_recognition"]["top_right"]["y"])
            self.license_bottom_left_x.insert(0, self.data["license_plate_recognition"]["bottom_left"]["x"])
            self.license_bottom_left_y.insert(0, self.data["license_plate_recognition"]["bottom_left"]["y"])
            self.license_bottom_right_x.insert(0, self.data["license_plate_recognition"]["bottom_right"]["x"])
            self.license_bottom_right_y.insert(0, self.data["license_plate_recognition"]["bottom_right"]["y"])

            self.lane_count_value.insert(0, self.data["lane"]["number_of_lanes"])
            self.populate_lanes(self.data["lane"]["lanes"])

    def clear_entries(self):
        self.red_light_start_x.delete(0, tk.END)
        self.red_light_start_y.delete(0, tk.END)
        self.red_light_end_x.delete(0, tk.END)
        self.red_light_end_y.delete(0, tk.END)

        self.speed_start_initial_x.delete(0, tk.END)
        self.speed_start_initial_y.delete(0, tk.END)
        self.speed_end_initial_x.delete(0, tk.END)
        self.speed_end_initial_y.delete(0, tk.END)
        self.speed_start_final_x.delete(0, tk.END)
        self.speed_start_final_y.delete(0, tk.END)
        self.speed_end_final_x.delete(0, tk.END)
        self.speed_end_final_y.delete(0, tk.END)

        self.license_top_left_x.delete(0, tk.END)
        self.license_top_left_y.delete(0, tk.END)
        self.license_top_right_x.delete(0, tk.END)
        self.license_top_right_y.delete(0, tk.END)
        self.license_bottom_left_x.delete(0, tk.END)
        self.license_bottom_left_y.delete(0, tk.END)
        self.license_bottom_right_x.delete(0, tk.END)
        self.license_bottom_right_y.delete(0, tk.END)

        self.lane_count_value.delete(0, tk.END)
        for lane in self.lanes:
            lane[0].destroy()
            lane[1].destroy()
        self.lanes.clear()

    def populate_lanes(self, lanes):
        for lane in lanes:
            self.add_lane()
            self.lanes[-1][0].insert(0, lane["start"]["x"])
            self.lanes[-1][1].insert(0, lane["start"]["y"])
            self.lanes[-1][2].insert(0, lane["end"]["x"])
            self.lanes[-1][3].insert(0, lane["end"]["y"])

    def add_lane(self):
        frame = tk.Frame(self.lane_frame)
        frame.grid(row=len(self.lanes) + 2, column=0, columnspan=2, pady=5, sticky="ew")
        start_x = self.create_entry(frame, "Start X:", 0, 0)
        start_y = self.create_entry(frame, "Start Y:", 0, 1)
        end_x = self.create_entry(frame, "End X:", 1, 0)
        end_y = self.create_entry(frame, "End Y:", 1, 1)
        self.lanes.append((start_x, start_y, end_x, end_y))

    def remove_lane(self):
        if self.lanes:
            lane = self.lanes.pop()
            lane[0].destroy()
            lane[1].destroy()
            lane[2].destroy()
            lane[3].destroy()

    def save_json(self):
        data = {
            "red_light_line": {
                "start": {"x": self.red_light_start_x.get(), "y": self.red_light_start_y.get()},
                "end": {"x": self.red_light_end_x.get(), "y": self.red_light_end_y.get()}
            },
            "speed_test_line": {
                "start_initial": {"x": self.speed_start_initial_x.get(), "y": self.speed_start_initial_y.get()},
                "end_initial": {"x": self.speed_end_initial_x.get(), "y": self.speed_end_initial_y.get()},
                "start_final": {"x": self.speed_start_final_x.get(), "y": self.speed_start_final_y.get()},
                "end_final": {"x": self.speed_end_final_x.get(), "y": self.speed_end_final_y.get()}
            },
            "license_plate_recognition": {
                "top_left": {"x": self.license_top_left_x.get(), "y": self.license_top_left_y.get()},
                "top_right": {"x": self.license_top_right_x.get(), "y": self.license_top_right_y.get()},
                "bottom_left": {"x": self.license_bottom_left_x.get(), "y": self.license_bottom_left_y.get()},
                "bottom_right": {"x": self.license_bottom_right_x.get(), "y": self.license_bottom_right_y.get()}
            },
            "lane": {
                "number_of_lanes": self.lane_count_value.get(),
                "lanes": [
                    {
                        "start": {"x": lane[0].get(), "y": lane[1].get()},
                        "end": {"x": lane[2].get(), "y": lane[3].get()}
                    } for lane in self.lanes
                ]
            }
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(data, file)
            self.status.config(text="JSON saved successfully!")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.status.config(text="Image loaded successfully!")

    def display_image(self):
        if not self.image or not self.data:
            messagebox.showerror("Error", "Image or data not loaded")
            return

        new_window = tk.Toplevel(self.root)
        new_window.title("Annotated Image")

        image_copy = self.image.copy()
        draw = ImageDraw.Draw(image_copy)

        # Draw red light line
        draw.line(
            [
                (int(self.red_light_start_x.get()), int(self.red_light_start_y.get())),
                (int(self.red_light_end_x.get()), int(self.red_light_end_y.get()))
            ],
            fill="red", width=2
        )

        # Draw speed test lines
        draw.line(
            [
                (int(self.speed_start_initial_x.get()), int(self.speed_start_initial_y.get())),
                (int(self.speed_end_initial_x.get()), int(self.speed_end_initial_y.get()))
            ],
            fill="blue", width=2
        )
        draw.line(
            [
                (int(self.speed_start_final_x.get()), int(self.speed_start_final_y.get())),
                (int(self.speed_end_final_x.get()), int(self.speed_end_final_y.get()))
            ],
            fill="blue", width=2
        )

        # Draw license plate recognition box
        draw.polygon(
            [
                (int(self.license_top_left_x.get()), int(self.license_top_left_y.get())),
                (int(self.license_top_right_x.get()), int(self.license_top_right_y.get())),
                (int(self.license_bottom_right_x.get()), int(self.license_bottom_right_y.get())),
                (int(self.license_bottom_left_x.get()), int(self.license_bottom_left_y.get()))
            ],
            outline="yellow", width=2
        )

        # Draw lanes
        for lane in self.lanes:
            draw.line(
                [
                    (int(lane[0].get()), int(lane[1].get())),
                    (int(lane[2].get()), int(lane[3].get()))
                ],
                fill="green", width=2
            )

        image_copy.thumbnail((800, 600))
        tk_image = ImageTk.PhotoImage(image_copy)
        
        image_label = tk.Label(new_window, image=tk_image)
        image_label.image = tk_image
        image_label.pack(pady=10)

    def display_on_image(self):
        self.display_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficConfigGUI(root)
    root.mainloop()