import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url, up_to_page):
    products = []
    # Loop through page numbers
    for page_number in range(1, up_to_page + 1):
        # Construct the URL for the current page
        page_url = f"{url}?page={page_number}"
        
        # Fetch the HTML content of the page
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        FIRST_DIV = first_tag_type_dropdown.get()
        FIRST_CLASS = first_tag_class_entry.get()
        FIRST_ATTRIBUTE = first_tag_attr_entry.get()

        SECOND_DIV = second_tag_type_dropdown.get()
        SECOND_CLASS = second_tag_class_entry.get()
        SECOND_ATTRIBUTE = second_tag_attr_entry.get()

        THIRD_DIV = third_tag_type_dropdown.get()
        THIRD_CLASS = third_tag_class_entry.get()
        THIRD_ATTRIBUTE = third_tag_attr_entry.get()

        # Extract product names and prices based on checkbox states
        if checkbox_first_var.get() != 1:
            first_tags = soup.find_all(FIRST_DIV, class_=FIRST_CLASS)
            for first_tag in first_tags:
                first = first_tag.find(FIRST_ATTRIBUTE).text.strip()
                products.append({'first': first})
        elif checkbox_second_var.get() != 1:
            second_tags = soup.find_all(SECOND_DIV, class_=SECOND_CLASS)
            for second_tag in second_tags:
                second = second_tag.find(SECOND_ATTRIBUTE).text.strip()
                products.append({'second': second})
        elif checkbox_third_var.get() != 1:
            third_tags = soup.find_all(THIRD_DIV, class_=THIRD_CLASS)
            for third_tag in third_tags:
                third = third_tag.find(THIRD_ATTRIBUTE).text.strip()
                products.append({'third': third})
    
    return products

def save_to_csv(products):
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['first','second','third']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for product in products:
                writer.writerow(product)
        messagebox.showinfo("Success", "Data has been saved successfully!")

def fetch_and_save():
    url = url_entry.get()
    up_to_page = int(up_to_page_entry.get())
    if url and up_to_page:
        products = scrape_website(url, up_to_page)
        save_to_csv(products)
    else:
        messagebox.showwarning("Warning", "Please enter a valid URL and up to page number!")

def show_info():
    info_text = "This is a web scraper application.\n"
    info_text += "Enter the URL of the olx product page you want to scrape example:https://www.olx.bg/nedvizhimi-imoti/prodazhbi/.\n"
    info_text += "specify the number of pages to scrape up to,\n"
    info_text += "then click 'Fetch and Save' to scrape the data and save it to a CSV file.\n"
    info_text += "Make sure the URL and up to page number are valid.\n\n"
    info_text += "Developed by [some dude with free time]"
    messagebox.showinfo("Information", info_text)

def toggle_first_inputs():
    if checkbox_first_var.get() == 1:
        # Disable the first set of inputs
        first_tag_type_dropdown.config(state="disabled")
        first_tag_class_entry.config(state="disabled")
        first_tag_attr_entry.config(state="disabled")
    else:
        # Enable the first set of inputs
        first_tag_type_dropdown.config(state="normal")
        first_tag_class_entry.config(state="normal")
        first_tag_attr_entry.config(state="normal")

def toggle_second_inputs():
    if checkbox_second_var.get() == 1:
        # Disable the second set of inputs
        second_tag_type_dropdown.config(state="disabled")
        second_tag_class_entry.config(state="disabled")
        second_tag_attr_entry.config(state="disabled")
    else:
        # Enable the second set of inputs
        second_tag_type_dropdown.config(state="normal")
        second_tag_class_entry.config(state="normal")
        second_tag_attr_entry.config(state="normal")

def toggle_third_inputs():
    if checkbox_third_var.get() == 1:
        # Disable the third set of inputs
        third_tag_type_dropdown.config(state="disabled")
        third_tag_class_entry.config(state="disabled")
        third_tag_attr_entry.config(state="disabled")
    else:
        # Enable the third set of inputs
        third_tag_type_dropdown.config(state="normal")
        third_tag_class_entry.config(state="normal")
        third_tag_attr_entry.config(state="normal")

# Create Tkinter GUI
window = tk.Tk()
window.title("Web Scraper for OLX")
window.geometry("520x400")

# URL Entry
url_label = tk.Label(window, text="Enter URL:")
url_label.place(x=10, y=10)
url_entry = tk.Entry(window, width=50)
url_entry.place(x=100,y=10)

up_to_page_label = tk.Label(window, text="Up to Page:")
up_to_page_label.place(x=10, y=40)  # Adjust x and y coordinates as needed
up_to_page_entry = tk.Entry(window, width=10)
up_to_page_entry.place(x=100, y=40)  # Adjust x and y coordinates as needed

# First Tag Type
first_tag_type_var = tk.StringVar()
first_tag_type_label = tk.Label(window, text="First Tag Type/Class/attr:")
first_tag_type_label.place(x=10, y=140) 
first_tag_type_dropdown = tk.Entry(window, width=10)
first_tag_type_dropdown.place(x=170, y=140) 

# First Tag Class Entry
first_tag_class_entry = tk.Entry(window, width=20)
first_tag_class_entry.place(x=240, y=140) 

# First Tag attribute Entry
first_tag_attr_entry = tk.Entry(window, width=10)
first_tag_attr_entry.place(x=370, y=140) 


# Second Tag Type
second_tag_type_var = tk.StringVar()
second_tag_type_label = tk.Label(window, text="Second Tag Type/Class/attr:")
second_tag_type_label.place(x=10, y=160) 
second_tag_type_dropdown = tk.Entry(window, width=10)
second_tag_type_dropdown.place(x=170, y=160) 

# Second Tag Class Entry
second_tag_class_entry = tk.Entry(window, width=20)
second_tag_class_entry.place(x=240, y=160) 

# Second Tag attribute Entry
second_tag_attr_entry = tk.Entry(window, width=10)
second_tag_attr_entry.place(x=370, y=160) 

# Third Tag Type
third_tag_type_var = tk.StringVar()
third_tag_type_label = tk.Label(window, text="Third Tag Type/Class/attr:")
third_tag_type_label.place(x=10, y=180) 
third_tag_type_dropdown = tk.Entry(window, width=10)
third_tag_type_dropdown.place(x=170, y=180) 

# Third Tag Class Entry
third_tag_class_entry = tk.Entry(window, width=20)
third_tag_class_entry.place(x=240, y=180) 

# Third Tag attribute Entry
third_tag_attr_entry = tk.Entry(window, width=10)
third_tag_attr_entry.place(x=370, y=180) 

# Checkboxes
checkbox_first_var = tk.IntVar()
checkbox_first = tk.Checkbutton(window, text="Disable", variable=checkbox_first_var, command=toggle_first_inputs)
checkbox_first.place(x=430, y=135)

checkbox_second_var = tk.IntVar()
checkbox_second = tk.Checkbutton(window, text="Disable", variable=checkbox_second_var, command=toggle_second_inputs)
checkbox_second.place(x=430, y=155)

checkbox_third_var = tk.IntVar()
checkbox_third = tk.Checkbutton(window, text="Disable", variable=checkbox_third_var, command=toggle_third_inputs)
checkbox_third.place(x=430, y=175)

# Fetch Button
fetch_button = tk.Button(window, text="Fetch and Save", command=fetch_and_save)
fetch_button.place(x=10, y=70)

# Info Button
info_button = tk.Button(window, text="Info", command=show_info)
info_button.place(x=380, y=70)

window.mainloop()
