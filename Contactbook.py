import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

class ContactBook:
    def __init__(self, master):
        self.master = master
        self.master.title("Contact Book")
        self.master.geometry("500x400")
        
        self.contacts = []
        self.filename = "contacts.json"
        self.load_contacts()
        
        # Create GUI elements
        self.create_widgets()
        self.update_listbox()
    
    def create_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self.master, padding="10")
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_contacts)
        
        # Contacts listbox
        self.listbox = tk.Listbox(self.master, width=50, height=10)
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(self.master, padding="10")
        button_frame.pack(fill=tk.X)
        
        self.add_button = ttk.Button(button_frame, text="Add Contact", command=self.add_contact)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.view_button = ttk.Button(button_frame, text="View Contact", command=self.view_contact)
        self.view_button.pack(side=tk.LEFT, padx=5)
        
        self.update_button = ttk.Button(button_frame, text="Update Contact", command=self.update_contact)
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(button_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack(side=tk.LEFT, padx=5)
    
    def add_contact(self):
        name = simpledialog.askstring("Add Contact", "Enter name:")
        if name:
            phone = simpledialog.askstring("Add Contact", "Enter phone number:")
            email = simpledialog.askstring("Add Contact", "Enter email:")
            address = simpledialog.askstring("Add Contact", "Enter address:")
            
            contact = {
                "name": name,
                "phone": phone,
                "email": email,
                "address": address
            }
            
            self.contacts.append(contact)
            self.update_listbox()
            self.save_contacts()
    
    def view_contact(self):
        try:
            index = self.listbox.curselection()[0]
            contact = self.contacts[index]
            messagebox.showinfo("Contact Details",
                                f"Name: {contact['name']}\n"
                                f"Phone: {contact['phone']}\n"
                                f"Email: {contact['email']}\n"
                                f"Address: {contact['address']}")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a contact to view.")
    
    def update_contact(self):
        try:
            index = self.listbox.curselection()[0]
            contact = self.contacts[index]
            
            name = simpledialog.askstring("Update Contact", "Enter name:", initialvalue=contact['name'])
            phone = simpledialog.askstring("Update Contact", "Enter phone number:", initialvalue=contact['phone'])
            email = simpledialog.askstring("Update Contact", "Enter email:", initialvalue=contact['email'])
            address = simpledialog.askstring("Update Contact", "Enter address:", initialvalue=contact['address'])
            
            if name:
                contact['name'] = name
                contact['phone'] = phone
                contact['email'] = email
                contact['address'] = address
                
                self.update_listbox()
                self.save_contacts()
                messagebox.showinfo("Success", "Contact updated successfully.")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a contact to update.")
    
    def delete_contact(self):
        try:
            index = self.listbox.curselection()[0]
            contact = self.contacts[index]
            if messagebox.askyesno("Delete Contact", f"Are you sure you want to delete {contact['name']}?"):
                del self.contacts[index]
                self.update_listbox()
                self.save_contacts()
                messagebox.showinfo("Success", "Contact deleted successfully.")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
    
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def search_contacts(self, event):
        search_term = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            if search_term in contact['name'].lower() or search_term in contact['phone']:
                self.listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.contacts = json.load(f)

    def save_contacts(self):
        with open(self.filename, 'w') as f:
            json.dump(self.contacts, f)

if __name__ == "__main__":
  root = tk.Tk()
  contact_book = ContactBook(root)
  root.mainloop()
