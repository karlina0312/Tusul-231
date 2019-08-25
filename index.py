
from tkinter import *
from get_text import *
from tkinter import filedialog as fd
import webbrowser
from tkinter import messagebox
from identify import *
from PIL import Image, ImageTk


def get_file():
   
    print("browse document..")
    global filepath
    filename = fd.askopenfilename() 
    filepath = filename
    if str(filename) == "" or str(filename) == "()":
        print("nothing selected")
    else :
        print(str(filename) + " selected")


def get_url():
   
    print("enter url..")
    global in_url
    url_button.destroy()
    in_url = Entry(main_window, width=17)
    in_url.grid(row=3, column=0, pady=30)


def submit_file():
    global filepath

    if str(filepath) == "" or str(filepath) == "()" or filepath == None:
        print("warning box displayed")
        messagebox.showwarning("Warning","File not selected, Please select a valid file.")
        return
    print("file submitted..")

    try :
        test_file = ocr_space_file(filename=filepath, language='eng') 
        json_str = json.loads(test_file)
        extracted_text = json_str["ParsedResults"][0]["ParsedText"]
        extracted_text = extracted_text.replace(" \r\n",  " ")
    except KeyError as e:
        print(str(e))
        if str(e) == '\'ParsedResults\'' :
            messagebox.showerror("Error", "Document type is not valid, Select a valid document")
        return
    except TypeError as e :
        messagebox.showerror("Error", "Requests limit increased.")
        return
    except requests.exceptions.ConnectionError as e : 
         messagebox.showerror("Error", "Can't connect to internet")
         return
    print("text extracted..")

    if str(extracted_text) == "":
        messagebox.showerror("Error", "Image or pdf quality is too lower.")
        return
    with open("predict/predict", "w") as text_file:
        text_file.write("yes	%s" % extracted_text)
    print("text written to file..")
   
    print("making prediction..")
    predicted_label = make_predictions()
    print("prediction made..")
   
    filepath = ''
    
    print("showing result..")
    show_result(predicted_label)


def submit_url():
  
    global in_url
    global fileurl
    global url_button
    if in_url == None :
        messagebox.showwarning("Warning", " Please enter a valid url.")
        return
    fileurl = in_url.get() 
    if fileurl == '' or fileurl == None:
        print("nothing entered")
        print("warning box displayed")
        messagebox.showwarning("Warning", "Input box empty, Please enter a valid url.")
        return
    else :
        print(str(fileurl) + " entered")
    print("url submitted")

    try :
        test_file = ocr_space_url(str(fileurl), language='eng') # Make request to OCR.space API
        json_str = json.loads(test_file) # Decode JSON data
        extracted_text = json_str["ParsedResults"][0]["ParsedText"] # Get text from JSON
        extracted_text = extracted_text.replace(" \r\n",  " ")
    except KeyError as e:
        if str(e) == '\'ParsedResults\'' :
            messagebox.showerror("Error", "URL is not valid, Enter a valid url")
        return
    except TypeError as e : 
        messagebox.showerror("Error", "Requests limit increased.")
        return
    except requests.exceptions.ConnectionError as e : 
         messagebox.showerror("Error", "Can't connect to internet")
         return
    print("text extracted..")

    if str(extracted_text) == "":
        messagebox.showerror("Error", "Image or pdf quality is too lower.")
        return
    with open("predict/predict", "w") as text_file:
        text_file.write("yes	%s" % extracted_text)
    print("text written to file..")
    
    print("making prediction..")
    predicted_label = make_predictions()
    print("prediction made..")

    in_url.destroy()
    url_button = Button(main_window, text="Enter URL", command=get_url)
    url_button.config(bg='black', fg='yellow')
    url_button.grid(row=3, column=0, pady=30)
 
    fileurl = ''
    in_url = None

    print("showing result..")
    show_result(predicted_label)

# open linedin
def open_linkedin(event):
     webbrowser.open_new(r"https://www.linkedin.com/in/hana-yoshikage-b71b93161/")

# open github
def open_github(event):
     webbrowser.open_new(r"https://github.com/hane0312")

# open twitter
def open_twitter(event):
     webbrowser.open_new(r"https://twitter.com/Aquadota")

# close result window
def close_result(): 
    global result_win
    result_win.destroy()
    result_win = None
    print("Tsonh haagdlaa..")


def show_result(label):
    
    global result_win 
    if result_win != None :
        result_win.destroy()
        result_win = None
    result_win = Tk()
    result_win.title('Predicted result')
    
    result_screen_width = result_win.winfo_screenwidth()
    result_screen_height = result_win.winfo_screenheight()
    
    result_window_width = 600
    result_window_height = 150
    
    result_x_cordinate = int((result_screen_width/2) - (result_window_width/2))
    result_y_cordinate = int((result_screen_height/2) - (result_window_height/2))

    result_win.geometry("{}x{}+{}+{}".format(result_window_width, result_window_height, result_x_cordinate, result_y_cordinate))
    result_win.resizable(width=FALSE, height=FALSE)
    result_win.config(bg='black')
    result_text = ''
    if label == 1:
        result_text = 'Document is form 16'
    else :
        result_text = 'Document is not form 16'

    result_title_text = Label(result_win, text=result_text)
    result_title_text.config(bg='black', fg='yellow')  
    result_title_text.config(font=footerfont)           
    result_title_text.config(height=2)       
    result_title_text.grid(row=0, column=0, padx=200, pady=30)

    close_button = Button(result_win, text="Ok", command=close_result)
    close_button.config(bg='black', fg='yellow')
    close_button.grid(row=1, column=0)
    result_win.protocol("WM_DELETE_WINDOW", on_closing_result)
    print("tsonh ongoiloo..")


def on_closing_main():
    if messagebox.askokcancel("Garah", "Ta garah uu?"):
        main_window.destroy()
        print("tsonh haagdlaa....")

def on_closing_result():
    result_win.destroy()
    print("tsonh haagdlaa..")

labelfont = ('times', 20, 'bold')
footerfont = ('times', 15, 'bold')
filepath = None
fileurl = None
result_win = None
# Entry for URl
in_url = None

print("application ajillaj ehellee....")


main_window = Tk()
main_window.title('Document Recognition Application')

screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

window_width = 900
window_height = 600

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

main_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
main_window.resizable(width=FALSE, height=FALSE)
main_window.config(bg='black')

# title
title_text = Label(main_window, text='Document Recognition Application')
title_text.config(bg='black', fg='yellow')  
title_text.config(font=labelfont)           
title_text.config(height=2)       
title_text.grid(row=0, column=0, columnspan=3, padx=200, pady=75)

browse_button = Button(main_window, text="Browse Document", command=get_file)
browse_button.config(bg='black', fg='yellow')
browse_button.grid(row=1, column=0, pady=30)

arrow1 = Label(main_window, text='===>>>>>')
arrow1.config(bg='black', fg='yellow')  
arrow1.config(font=labelfont)           
arrow1.config(height=2)       
arrow1.grid(row=1, column=1)

# file oruulah hesgiin button
submit_file = Button(main_window, text="Submit", command=submit_file)
submit_file.config(bg='black', fg='yellow')
submit_file.grid(row=1, column=2)

sep_text = Label(main_window, text='OR')
sep_text.config(bg='black', fg='yellow')  
sep_text.config(font=labelfont)           
sep_text.config(height=2)       
sep_text.grid(row=2, column=1)


#  footer hesgiin text
footer_text = Label(main_window, text='<< Made with \u2665 by Hane Tech >>')
footer_text.config(bg='black', fg='yellow')  
footer_text.config(font=footerfont)           
footer_text.config(height=1)       
footer_text.grid(row=4, column=1, pady=(75, 0))

#  linkedin icon
linkedin_logo = Image.open("icons/linkedin.png")
image_linkedin = ImageTk.PhotoImage(linkedin_logo)
label_linkedin = Label(image=image_linkedin, bg='black', cursor="hand2")
label_linkedin.grid(row=5, column=1, pady=(7,0))
label_linkedin.bind("<Button-1>", open_linkedin)

#  github icon
github_logo = Image.open("icons/github.png")
image_github = ImageTk.PhotoImage(github_logo)
label_github = Label(image=image_github, bg='black', cursor="hand2")
label_github.grid(row=5, column=1, padx=(0,75), pady=(7,0))
label_github.bind("<Button-1>", open_github)

#  twitter icon
twitter_logo = Image.open("icons/twitter.png")
image_twitter = ImageTk.PhotoImage(twitter_logo)
label_twitter = Label(image=image_twitter, bg='black', cursor="hand2")
label_twitter.grid(row=5, column=1, padx=(75, 0), pady=(7,0))
label_twitter.bind("<Button-1>", open_twitter)

main_window.protocol("WM_DELETE_WINDOW", on_closing_main)
# undsen tsonhiig duudah
main_window.mainloop()
