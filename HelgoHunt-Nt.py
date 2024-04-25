import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import requests
import os
from io import BytesIO
from PIL import Image, ImageTk

def perform_search(query_file, db_file, output_file, params):
    blast_command = [
        'blastn',
        '-query', query_file,
        '-db', db_file,
        '-outfmt', params["outfmt"],
        '-evalue', params["evalue"],
        '-perc_identity', params["perc_identity"],
        '-num_threads', params["threads"],
        '-max_target_seqs', params["max_target_seqs"],
        '-out', output_file
    ]

    try:
        subprocess.call(blast_command)
        messagebox.showinfo("Search Complete", "BLAST search completed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", "Error occurred during BLAST search: {}".format(e))

def validate_input(query_file, db_file):
    if not query_file:
        messagebox.showerror("Error", "Please upload a query sequence file.")
        return False
    elif not db_file:
        messagebox.showerror("Error", "Please select a BLAST database file.")
        return False
    return True

def search_sequence():
    query_file = query_entry.get()
    db_file = db_entry.get()
    output_file = output_entry.get()

    params = {
        "evalue": evalue_entry.get(),
        "threads": threads_entry.get(),
        "outfmt": outfmt_combobox.get(),
        "perc_identity": perc_identity_entry.get(),
        "max_target_seqs": max_target_seqs_entry.get()
    }

    if validate_input(query_file, db_file):
        perform_search(query_file, db_file, output_file, params)

def upload_sequence():
    file_path = filedialog.askopenfilename()
    if file_path:
        query_entry.delete(0, tk.END)
        query_entry.insert(tk.END, file_path)

def select_database():
    file_path = filedialog.askopenfilename()
    if file_path:
        db_entry.delete(0, tk.END)
        db_name = os.path.splitext(os.path.basename(file_path))[0]  # Remove extension from filename
        db_entry.insert(tk.END, os.path.join(os.path.dirname(file_path), db_name))  # Retain path and append base filename

def export_results():
    output_file = output_entry.get()
    if output_file:
        messagebox.showinfo("Export Results", "Search results exported to: {}".format(output_file))

root = tk.Tk()
root.title("Welcome to HelgoHunt")

# Function to fetch image from URL
def fetch_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        image = Image.open(BytesIO(response.content))
        return image
    except requests.RequestException as e:
        print("Error fetching image:", e)
        return None

# Fetch the image from URL
image_url = "https://drive.google.com/uc?id=1W2PCIFbcJShRkl11wqfotVh0NzuyXdvX"
original_image = fetch_image(image_url)

# Resize the image to 2x15 cm
target_width_cm = 10
target_height_cm = 2
dpi = 300  # Typical screen resolution
target_width_pixels = int(target_width_cm * dpi / 2.54)  # Convert cm to inches
target_height_pixels = int(target_height_cm * dpi / 2.54)  # Convert cm to inches
resized_image = original_image.resize((target_width_pixels, target_height_pixels))

# Convert the resized image to Tkinter PhotoImage
logo_image = ImageTk.PhotoImage(resized_image)

# Create a canvas widget
canvas = tk.Canvas(root, width=target_width_pixels, height=target_height_pixels)
canvas.pack(side=tk.BOTTOM, anchor=tk.SE)  # Pack the canvas to the bottom right corner

# Display the logo image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=logo_image)  # Adjust the coordinates as needed

input_frame = ttk.Frame(root, padding="10", relief="raised")
input_frame.pack()

query_label = ttk.Label(input_frame, text="Query Sequence:")
query_label.grid(row=0, column=0, sticky=tk.W)
query_entry = ttk.Entry(input_frame, width=50)
query_entry.grid(row=0, column=1, sticky=tk.W)

upload_button = ttk.Button(input_frame, text="Upload Sequence", command=upload_sequence)
upload_button.grid(row=0, column=2, sticky=tk.W)

db_label = ttk.Label(input_frame, text="BLAST Database File:")
db_label.grid(row=1, column=0, sticky=tk.W)
db_entry = ttk.Entry(input_frame, width=50)
db_entry.grid(row=1, column=1, sticky=tk.W)

select_db_button = ttk.Button(input_frame, text="Select Database", command=select_database)
select_db_button.grid(row=1, column=2, sticky=tk.W)

output_label = ttk.Label(input_frame, text="Output File:")
output_label.grid(row=2, column=0, sticky=tk.W)
output_entry = ttk.Entry(input_frame, width=50)
output_entry.grid(row=2, column=1, sticky=tk.W)

params_frame = ttk.LabelFrame(root, text="BLAST Parameters", padding="10")
params_frame.pack(fill="both", padx=10, pady=(10, 0))

evalue_label = ttk.Label(params_frame, text="E-value:")
evalue_label.grid(row=0, column=0, sticky=tk.W)
evalue_entry = ttk.Entry(params_frame, width=10)
evalue_entry.grid(row=0, column=1, sticky=tk.W)
evalue_entry.insert(tk.END, "0.001")

threads_label = ttk.Label(params_frame, text="Threads:")
threads_label.grid(row=1, column=0, sticky=tk.W)
threads_entry = ttk.Entry(params_frame, width=10)
threads_entry.grid(row=1, column=1, sticky=tk.W)
threads_entry.insert(tk.END, "1")

perc_identity_label = ttk.Label(params_frame, text="Percentage Identity:")
perc_identity_label.grid(row=2, column=0, sticky=tk.W)
perc_identity_entry = ttk.Entry(params_frame, width=10)
perc_identity_entry.grid(row=2, column=1, sticky=tk.W)
perc_identity_entry.insert(tk.END, "90")

max_target_seqs_label = ttk.Label(params_frame, text="Max Target Sequences:")
max_target_seqs_label.grid(row=3, column=0, sticky=tk.W)
max_target_seqs_entry = ttk.Entry(params_frame, width=10)
max_target_seqs_entry.grid(row=3, column=1, sticky=tk.W)
max_target_seqs_entry.insert(tk.END, "25")

outfmt_label = ttk.Label(params_frame, text="Output Format:")
outfmt_label.grid(row=4, column=0, sticky=tk.W)
outfmt_combobox = ttk.Combobox(params_frame, values=["0", "5", "6", "100", "101"], width=5)
outfmt_combobox.grid(row=4, column=1, sticky=tk.W)
outfmt_combobox.current(2)

search_button = ttk.Button(root, text="Search", command=search_sequence)
search_button.pack(pady=(10, 0))

export_button = ttk.Button(root, text="Export Results", command=export_results)
export_button.pack(pady=(10, 0))

copyright_label = ttk.Label(root, text="©csidhu@MPI")
copyright_label.pack(side=tk.BOTTOM)

root.mainloop()
