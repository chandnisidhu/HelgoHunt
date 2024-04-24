import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import requests
import subprocess
from io import BytesIO

def perform_search(query_file, db_file, output_file, params, seq_type):
    # Choose the appropriate Diamond command based on the sequence type
    diamond_command = [
        'diamond', 'blastp' if seq_type == 'Protein' else 'blastx',
        '--query', query_file,
        '--db', db_file,
        '--outfmt', params["outfmt"],
        '--evalue', params["evalue"],
        '--threads', params["threads"],
        '--query-cover', params["query_cov"],
        '--subject-cover', params["subject_cov"],
        '--block-size', params["block_size"],
        '--max-target-seqs', params["max_target_seqs"],
        '--out', output_file
    ]

    try:
        subprocess.call(diamond_command)
        messagebox.showinfo("Search Complete", "DIAMOND search completed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", "Error occurred during DIAMOND search: {}".format(e))

def validate_input(query_file, db_file):
    if not query_file:
        messagebox.showerror("Error", "Please upload a query sequence file.")
        return False
    elif not db_file:
        messagebox.showerror("Error", "Please select a DIAMOND database.")
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
        "query_cov": query_cov_entry.get(),
        "subject_cov": subject_cov_entry.get(),
        "block_size": block_size_entry.get(),
        "max_target_seqs": max_target_seqs_entry.get()
    }
    
    seq_type = seq_type_combobox.get()

    if validate_input(query_file, db_file):
        perform_search(query_file, db_file, output_file, params, seq_type)

def upload_sequence():
    file_path = filedialog.askopenfilename()
    if file_path:
        query_entry.delete(0, tk.END)
        query_entry.insert(tk.END, file_path)

def select_database():
    file_path = filedialog.askopenfilename()
    if file_path:
        db_entry.delete(0, tk.END)
        db_entry.insert(tk.END, file_path)

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

# Create your GUI elements on top of the background label
input_frame = ttk.Frame(root, padding="10", relief="raised")
input_frame.pack()

query_label = ttk.Label(input_frame, text="Query Sequence:")
query_label.grid(row=0, column=0, sticky=tk.W)
query_entry = ttk.Entry(input_frame, width=50)
query_entry.grid(row=0, column=1, sticky=tk.W)

upload_button = ttk.Button(input_frame, text="Upload Sequence", command=upload_sequence)
upload_button.grid(row=0, column=2, sticky=tk.W)

db_label = ttk.Label(input_frame, text="DIAMOND Database:")
db_label.grid(row=1, column=0, sticky=tk.W)
db_entry = ttk.Entry(input_frame, width=50)
db_entry.grid(row=1, column=1, sticky=tk.W)

select_db_button = ttk.Button(input_frame, text="Select Database", command=select_database)
select_db_button.grid(row=1, column=2, sticky=tk.W)

seq_type_label = ttk.Label(input_frame, text="Seq Type:")
seq_type_label.grid(row=2, column=0, sticky=tk.W)
seq_type_combobox = ttk.Combobox(input_frame, values=["Protein", "Nucleotide"], width=20)
seq_type_combobox.grid(row=2, column=1, sticky=tk.W)

output_label = ttk.Label(input_frame, text="Output File:")
output_label.grid(row=3, column=0, sticky=tk.W)
output_entry = ttk.Entry(input_frame, width=50)
output_entry.grid(row=3, column=1, sticky=tk.W)

params_frame = ttk.LabelFrame(root, text="DIAMOND Parameters", padding="10")
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

query_cov_label = ttk.Label(params_frame, text="Query Coverage:")
query_cov_label.grid(row=2, column=0, sticky=tk.W)
query_cov_entry = ttk.Entry(params_frame, width=10)
query_cov_entry.grid(row=2, column=1, sticky=tk.W)
query_cov_entry.insert(tk.END, "90")

subject_cov_label = ttk.Label(params_frame, text="Subject Coverage:")
subject_cov_label.grid(row=3, column=0, sticky=tk.W)
subject_cov_entry = ttk.Entry(params_frame, width=10)
subject_cov_entry.grid(row=3, column=1, sticky=tk.W)
subject_cov_entry.insert(tk.END, "90")

block_size_label = ttk.Label(params_frame, text="Block Size (billions):")
block_size_label.grid(row=4, column=0, sticky=tk.W)
block_size_entry = ttk.Entry(params_frame, width=10)
block_size_entry.grid(row=4, column=1, sticky=tk.W)
block_size_entry.insert(tk.END, "1")

max_target_seqs_label = ttk.Label(params_frame, text="Max Target Sequences:")
max_target_seqs_label.grid(row=5, column=0, sticky=tk.W)
max_target_seqs_entry = ttk.Entry(params_frame, width=10)
max_target_seqs_entry.grid(row=5, column=1, sticky=tk.W)
max_target_seqs_entry.insert(tk.END, "25")

outfmt_label = ttk.Label(params_frame, text="Output Format:")
outfmt_label.grid(row=6, column=0, sticky=tk.W)
outfmt_combobox = ttk.Combobox(params_frame, values=["0", "5", "6", "100", "101"], width=5)
outfmt_combobox.grid(row=6, column=1, sticky=tk.W)
outfmt_combobox.current(2)

search_button = ttk.Button(root, text="Search", command=search_sequence)
search_button.pack(pady=(10, 0))

export_button = ttk.Button(root, text="Export Results", command=export_results)
export_button.pack(pady=(10, 0))

copyright_label = ttk.Label(root, text="©csidhu@MPI")
copyright_label.pack(side=tk.BOTTOM)

root.mainloop()
