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
        
        # Extract product names and prices
        product_tags = soup.find_all('div', class_='css-u2ayx9')
        location_tags = soup.find_all('p', class_='css-1a4brun', attrs={'data-testid': 'location-date'})
        if not product_tags or not location_tags:
            break
        
        for product_tag, location_tag in zip(product_tags, location_tags):
            name = product_tag.find('h6').text.strip()
            price_tag = product_tag.find('p', attrs={'data-testid': 'ad-price'})
            location = location_tag.text.strip().split(' - ')[0]
            date = location_tag.text.strip().split(' - ')[-1]
            if price_tag:
                price = price_tag.text.strip()
            else:
                price = "Price not found"
            products.append({'name': name, 'price': price, 'location': location, 'date': date})
    
    return products

def save_to_csv(products):
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['name', 'price', 'location', 'date']
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

# Create Tkinter GUI
window = tk.Tk()
window.title("Web Scraper for OLX")
window.geometry("420x100")

# URL Entry
url_label = tk.Label(window, text="Enter URL:")
url_label.place(x=10, y=10)
url_entry = tk.Entry(window, width=50)
url_entry.place(x=100,y=10)

up_to_page_label = tk.Label(window, text="Up to Page:")
up_to_page_label.place(x=10, y=40)  # Adjust x and y coordinates as needed
up_to_page_entry = tk.Entry(window, width=10)
up_to_page_entry.place(x=100, y=40)  # Adjust x and y coordinates as needed


# Fetch Button
fetch_button = tk.Button(window, text="Fetch and Save", command=fetch_and_save)
fetch_button.place(x=10, y=70)

# Info Button
info_button = tk.Button(window, text="Info", command=show_info)
info_button.place(x=380, y=70)

window.mainloop()
