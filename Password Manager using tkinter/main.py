import tkinter
import random
from tkinter import messagebox  # to use a messagebox from tkinter u have to do like this
import pyperclip  # pyperclip module to automatically copy paste the password generated
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)  # minimum 8 letters
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for char in range(1, nr_letters)]  # suppose (1, 8), so now it chooses random 7 letters since last not included.

    password_symbols = [random.choice(symbols) for char in range(1, nr_symbols)]

    password_numbers = [random.choice(numbers) for char in range(1, nr_numbers)]

    password_list = password_letter+password_symbols+password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    # instead of doing it like this u can directly place the letters in the string.
    """password = ""
    for char in password_list:
      password += char"""

    password_entry.insert(0, password)
    pyperclip.copy(password)   # now the password that's generated automatically copy's in clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #

def add():
    web = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {web: {"email": email, "password": password}}  # json format

    if len(web) == 0 or len(password) == 0:  # if the length of the words or anything is 0 then we can bring up a pop-up window
        tkinter.messagebox.showinfo(title="Oops",
                                    message="Please don't leave any fields empty!")  # now using this messagebox that we have imported, we can bring up a pop up window.
    else:
        is_ok = tkinter.messagebox.askokcancel(title=web,  # if everything is correct we can bring up an ok or cancel pop up window
                                               message=f"These are the details entered: \nEmail: {email} \nPassword:{password} \nis it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:  # if there is no file we can do the except clause
                    data = json.load(data_file)  # reading the file
                    data.update(new_data)        # using the object of the file we can update
            except FileNotFoundError:   # we can make a file and add the data
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file)
            else:    # now for the 2nd entry we execute the try block commands and if there is no errors we  can write the updated/ append data.
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file)  # loading the data from try clause and updating it and writing it to append it.
                # data.write(f"{web} | {email} | {password}\n")    instead of formatting in a bad way we can use the json format
            finally:
                website_entry.delete(0, 'end')
                password_entry.delete(0, 'end')

# ---------------- SEARCH FOR EMAIL AND PASS FROM A WEBSITE NAME ----------------- #

def find_password():
    web = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            for email in data[web]:
                show_web_email = data[web]["email"]
                show_web_pass = data[web]["password"]
            tkinter.messagebox.showinfo(title=f"{web.title()}", message=f"Email: {show_web_email} \nPassword: {show_web_pass}")

    except KeyError:
        tkinter.messagebox.showinfo(message=f"No Details for {web} exists.")

    except FileNotFoundError:
        tkinter.messagebox.showinfo(message="No Data File Found.")


# ---------------------------- UI SETUP ------------------------------- #

window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")


# Loading Image

canvas = tkinter.Canvas(width=200, height=200, bg="white", highlightthickness=0)  # bg is background color of the image, highlight thickness is to remove the unwanted line
logo_img = tkinter.PhotoImage(file="logo.png")  # to load the image
canvas.create_image(100, 90, image=logo_img)   # x , y position for the image
canvas.grid(column=1, row=0)

# Labels

website = tkinter.Label(text="Website:", bg="white", font=("Courier", 10, "bold"))
website.grid(column=0, row=1)

Email = tkinter.Label(text="Email/Username:", bg="white", font=("Courier", 10, "bold"))
Email.grid(column=0, row=2)

Password = tkinter.Label(text="Password:", bg="white", font=("Courier", 10, "bold"))
Password.grid(column=0, row=3)

# Entries

website_entry = tkinter.Entry(width=35, bg="white")
website_entry.grid(column=1, row=1, columnspan=2, sticky="W")  # sticky="EW" means stick to east and west so we can get perfect alignment
website_entry.focus()

email_entry = tkinter.Entry(width=35, bg="white")
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")  # column span is to occupy more columns/ to make it wider
email_entry.insert(tkinter.END, string="mohammedkaysar05@gmail.com")  # to start with a starting email since u mostly use only 1 email.


password_entry = tkinter.Entry(width=21, bg="white")
password_entry.grid(column=1, row=3, sticky="EW")

# Button

generate_pass = tkinter.Button(text="Generate Password", bg="white", command=generate_pass)
generate_pass.grid(column=2, row=3, sticky="EW")


add_pass = tkinter.Button(text="Add", width=36, bg="white", command=add)
add_pass.grid(column=1,  row=5, columnspan=2, sticky="EW")

search_data = tkinter.Button(text="Search", bg="white", command=find_password)
search_data.grid(column=2, row=1, sticky="EW")


window.mainloop()
