from tkinter import *
from tkinter import messagebox
import random
import json


#---------------------------    Password Generation   -------------------------

def pw_generate():
    """
    This function generates a random password and and inserts to the textbox designated to display and store password.
    :return:
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    password_text.insert(0,password)



#-------------------------------  Data Validation, Password Storage and Search ----------------------

def validate(w,e):
    """
    This function does validation of website and email. Password not verified because it is geneated by a function
    :param w:   Website name
    :param e:   Email
    :return:  True if both email and website correct. False otherwise.
    """
    if len(w) < 3 or (".com" in w == False):
        return False
    if len(e) < 10 or ("@" in e == False) or (".com" in e == False):
        return False
    return True


def save_password():
    """
    This function stores the user input in file after validation and confirmation from the user
    :return:
    """

    website = website_text.get()
    email = email_text.get()
    password = password_text.get()
    is_ok = False
    data = {
        website : {
            "email" : email,
            "password" : password
            }
    }


    if validate(website, email):       #If the data is valid get user confirmation
        is_ok = messagebox.askokcancel(title = "Confirm",message = f"These are the values entered: \nWebsite:{website}\nEmail:{email}\nPassword: {password}")
    else:
        messagebox.showinfo("Oops!","Invalid info for website or email")
    if is_ok:     #If valid and user confirmed
        val = {}
        try:
            save_file = open("data.json","r")
            val = json.load(save_file)
            save_file.close()
        except json.decoder.JSONDecodeError:
            pass
        except FileNotFoundError:
            pass
        finally:
            save_file = open("data.json","w")
            val.update(data)
            json.dump(val,save_file, indent=4)
            website_text.delete(0,END)
            website_text.insert(0,"")
            password_text.delete(0,END)
            password_text.insert(0,"")
            website_text.focus()
        #save_file.close()



def search():
    """
    This function searches and displays the password for the site entered by the user
    :return:
    """
    website = website_text.get()
    try:
        with open("data.json","r") as file:
            data = json.load(file)
            email = data[website]["email"]
            password = data[website]["password"]
    except FileNotFoundError:
        messagebox.showerror("Oops!", "There are no records!")
    except KeyError:
        messagebox.showerror("Oops!",f"No record for {website} exist")
    else:
        messagebox.showinfo(f"{website}",f"Email: {email}\nPassword: {password}")





#----------------------    UI SETUP   ---------------------


#Setup Window
window = Tk()
window.title("Password Manager")
window.minsize(width=500,height=420)
window.config(padx = 50,pady=50)

#Setup Canvas
canvas = Canvas(height = 200,width = 200)
img = PhotoImage(file="logo.png")
canvas.create_image(100,125,image = img)
canvas.grid(column = 1,row = 0)

#Setup Labels
website_label = Label(text = "Website:")
email_label = Label(text = "Email:")
password_label = Label(text = "Password:  " )
website_label.grid(column = 0, row = 1)
email_label.grid(column = 0, row = 2)
password_label.grid(column = 0, row = 3)

#Setup Textboxes(Entry)
website_text = Entry(width = 35)
website_text.focus()
email_text = Entry(width = 35)
email_text.insert(0,"abcde@gmail.com")
password_text = Entry(width = 35)
website_text.grid(column = 1, row = 1)
email_text.grid(column = 1,row = 2)
password_text.grid(column = 1, row = 3)

#Setup Buttons
generate_password = Button(text = "Generate Password",width = 15,command= pw_generate)
generate_password.grid(column = 2, row = 3)
add = Button(text = "Add",width = 25,command = save_password)
add.grid(column = 1, row = 4)
search = Button(text = "Search",width = 15,command = search)
search.grid(column = 2,row = 1)


window.mainloop()
