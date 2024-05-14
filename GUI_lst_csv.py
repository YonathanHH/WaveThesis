import tkinter as tk
from tkinter import filedialog
from t2listing import *
import numpy as np

diff_int = 0.2
def convert_to_csv():
    listing_file = filedialog.askopenfilename(filetypes=[("TOUGH2 Listing Files", "*.LISTING"),("TOUGH2 Listing Files", "*.listing")])
    if listing_file:
        try:
            p0 = float(p0_entry.get())
            block_value = str(block_entry.get())  # pp0_entry.get()
            lst = t2listing(listing_file)  # This is to load the listing files
            time, press = lst.history(('e', block_value, 'Pressure'))  # the block_value specifies the block
            press_bar = (press / 100000) - p0  # this is to convert it from pa to bar

            csv_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if csv_file:
                np.savetxt(csv_file, np.vstack((time, press_bar)).T, delimiter=',')
                result_label.config(text="CSV file saved successfully!")
            else:
                result_label.config(text="CSV file not saved.")
        except ValueError:
            result_label.config(text="Invalid input for p0 or block value.")
    else:
        result_label.config(text="No TOUGH2 Listing File selected.")


root = tk.Tk()
root.title("TOUGH2 Listing to CSV Converter")

p0_label = tk.Label(root, text="Initial Pressure (p0):")
p0_label.pack(pady=5)

p0_entry = tk.Entry(root)
p0_entry.insert(0, "0")
p0_entry.pack(pady=5)

block_label = tk.Label(root, text="Block Value:")
block_label.pack(pady=5)

block_entry = tk.Entry(root)
block_entry.insert(0, "aaa01")
block_entry.pack(pady=5)

select_button = tk.Button(root, text="Select TOUGH2 Listing File", command=convert_to_csv)
select_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()