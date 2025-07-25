from tkinter import *
import tkinter as tk
from db_comms import *
from tkinter import messagebox

app = tk.Tk()
app.title('CRMLite - Local DB')
app.geometry('500x500')

tk.Label(app,text='Συνδεθείτε:').pack()

tk.Label(app,text='Username').pack()
user_entry = Entry(app)
user_entry.pack()

tk.Label(app,text='Password:').pack()
passw_entry = Entry(app,show='•	')
passw_entry.pack()

def clear_app():
    for widget in app.winfo_children():
        widget.forget()



def start_auth():
    global username
    global is_admin
    username = user_entry.get()
    password = passw_entry.get()
    auth_check,u_exist = auth(username,password)
    if u_exist == True:
        is_admin = check_admin(username)
        if auth_check == True:
            home()
        else:
            messagebox.showerror('Σφάλμα σύνδεσης','Ο κωδικός πρόσβασης είναι λάθος')
    else:
        messagebox.showerror('Σφάλμα σύνδεσης!','Δεν υπάρχει χρήστης με αυτό το όνομα!')

tk.Button(app,text='Σύνδεση',command=start_auth).pack()


def new_customer_front():
    window = tk.Toplevel(app)
    window.title('Εγγραφή πελάτη | CRM Lite Local DB')
    window.geometry('400x400')


    tk.Label(window,text='Ονοματεπώνυμο πελάτη').pack()
    name_e = Entry(window)
    name_e.pack()

    tk.Label(window,text='Τηλέφωνο').pack()
    phone_e = Entry(window)
    phone_e.pack()

    tk.Label(window,text='Email').pack()
    email_e=Entry(window)
    email_e.pack()

    tk.Label(window,text='Διεύθυνση κατοικίας').pack()
    add_e = Entry(window)
    add_e.pack()

    tk.Label(window,text='ΑΦΜ').pack()
    vat_e = Entry(window)
    vat_e.pack()

    def sbt_cust_creation():
        name = name_e.get()
        phone = int(phone_e.get())
        add = add_e.get()
        vat = int(vat_e.get())
        email = email_e.get()
        res,cust_id = new_customer_back(name,phone,email,add,vat,username)
        window.destroy()
        messagebox.showinfo('CRMLite Local DB',f"Ο πελάτης προστέθηκε! Κωδικός πελάτη: {cust_id}")
    tk.Button(window,text='Δημιουργία',command=sbt_cust_creation).pack()
    tk.Button(window,text='<-- Πίσω',command=home).pack()


def delete_customer_front():
    window = Toplevel(app)
    window.title('Διαγραφή πελάτη - Admin CRMLite DB Mode')
    window.geometry('400x400')

    tk.Label(window,text='Επιλέξτε ενα').pack()
    tk.Label(window,text='Αρ. Τηλεφώνου:').pack()
    p_e = Entry(window)
    p_e.pack()

    tk.Label(window,text='ή').pack()
    tk.Label(window,text='ΑΦΜ').pack()
    vat_e = Entry(window)
    vat_e.pack()

    def sbt_cust_delete():
        p = int(p_e.get())
        vat = int(vat_e.get())
        if p and vat:
            messagebox.showerror('CRMLite Local DB','Σφάλμα! εισάγετε ΜΟΝΟ αριθμό τηλεφώνου ή ΑΦΜ')
        else:
            if p:
                res = delete_customer_front(p,username)
            elif vat:
                res = delete_customer_vat(vat,username)
            window.destroy()
            messagebox.showinfo('CRMLite Local DB',f"{res}")
    tk.Button(window,text='Διαγραφή',command=sbt_cust_delete).pack()
    tk.Button(window,text='<-- Πίσω',command=home).pack()
    
def edit_customer():
    window = Toplevel(app)
    window.title('Επεξεργασία πελάτη - CRMLite Local DB')
    window.geometry('500x500')
    tk.Label(window,text='Κινητό τηλέφωνο:').pack()
    p_e = Entry(window)
    p_e.pack()
    def sbt_search():
        phone = int(p_e.get())
        valid_phone = check_phone(phone)
        if valid_phone == True:
            for widget in window.winfo_children():
                widget.forget()
            c_name,c_phone,c_email,c_address,c_vat,cust_id = get_cust_details(phone)
            tk.Label(window,text=f"Στοιχεία πελάτη: \n Ονοματεπώνυμο: {c_name} \n Κινητό τηλέφωνο: {c_phone} \n Email:{c_email} \n Διεύθυνση: {c_address} \n ΑΦΜ: {c_vat} \n Κωδικός πελάτη: {cust_id}").pack()
            tk.Label(window,text=f" Αφήστε κενά τα στοιχεία που θέλετε να διατηρηθούν: \n\n ").pack()
            

            tk.Label(window,text='Όνομα:').pack()
            n_name_e = Entry(window)
            n_name_e.pack()

            tk.Label(window,text='Κινητό:').pack()
            n_phone_e = Entry(window)
            n_phone_e.pack()

            tk.Label(window,text='Email:').pack()
            n_email_e = Entry(window)
            n_email_e.pack()

            tk.Label(window,text='Διεύθυνση:').pack()
            n_address_e = Entry(window)
            n_address_e.pack()

            tk.Label(window,text='ΑΦΜ').pack()
            n_vat_e = Entry(window)
            n_vat_e.pack()

            def sbt_edit():
                n_name = n_name_e.get()
                n_phone = n_phone_e.get()
                if n_phone:
                    n_phone = int(n_phone)
                n_email = n_email_e.get()
                n_address = n_address_e.get()
                n_vat = n_vat_e.get()
                if n_vat:
                    n_vat = int(n_vat)

                modify_customer(phone,n_name,n_phone,n_email,n_address,n_vat,username)

                window.destroy()
                messagebox.showinfo('Δημιουργία πελάτη - CRMLite DB',f"Έγινε επεξεργασία πελάτη: {cust_id}")
                home()

            tk.Button(window,text='Επεξεργασία πελάτη',command=sbt_edit).pack()
            tk.Button(window,text='<-- Πίσω',command=home).pack()
        else:
            messagebox.showerror('Δημιουργία πελάτη - CRMLite DB','Δεν βρέθηκε πελάτης με αυτό το τηλεφωνο!')
    tk.Button(window,text='Αναζήτηση αριθμού',command=sbt_search).pack()
    tk.Button(window,text='<-- Πίσω',command=home).pack()


def customer_lookup():
    window = Toplevel(app)
    window.title('Αναζήτηση πελάτη - CRMLite LocalDB')
    window.geometry('400x400')


    tk.Label(window,text='Κινητό:').pack()
    p_e = Entry(window)
    p_e.pack()
    def sbt_lookup():
        phone = int(p_e.get())
        cust_found = check_phone(phone)
        if cust_found == True:
            for widget in window.winfo_children():
                widget.pack_forget()
            c_name,c_phone,c_email,c_address,c_vat,cust_id = get_cust_details(phone)
            tk.Label(window,text=f"Στοιχεία πελάτη: \n Ονοματεπώνυμο: {c_name} \n Κινητό τηλέφωνο: {c_phone} \n Email:{c_email} \n Διεύθυνση: {c_address} \n ΑΦΜ: {c_vat} \n Κωδικός πελάτη: {cust_id}").pack()
            tk.Label(window,text=f"{find_cust_orders(phone)}").pack()
            tk.Button(window,text='Κλεισιμο παραθύρου',command=window.destroy).pack()
        else:
            messagebox.showerror('Προβολή πελάτη - CRMLite LocalDB','Ο πελάτης δεν βρέθηκε!')
    tk.Button(window,text='Αναζήτηση',command=sbt_lookup).pack()
    tk.Button(window,text='<-- Πίσω',command=home).pack()


def customers_tab():
    clear_app()
    tk.Button(app,text='Καταχώρηση νέου πελάτη',command=new_customer_front).pack()
    tk.Button(app,text='Επεξεργασία πελάτη',command=edit_customer).pack()
    tk.Button(app,text='Αναζήτηση πελάτη',command=customer_lookup).pack()

    tk.Button(app,text='<-- Πίσω',command=home).pack()

def admin_page():
    clear_app()
    tk.Button(app,text='Διαγραφή πελάτη',command=delete_customer_front).pack()
    tk.Button(app,text='<-- Πίσω',command=home).pack()


def home():
    clear_app()
    tk.Label(app,text=f"Καλωσόρισες {username}").pack()
    if is_admin == True:
        tk.Label(app,text='Admin Panel',fg='red').pack()
        tk.Button(app,text='Λειτουργίες Administrator',command=admin_page).pack()

    tk.Button(app,text='Πελάτες',command=customers_tab).pack()





app.mainloop()

