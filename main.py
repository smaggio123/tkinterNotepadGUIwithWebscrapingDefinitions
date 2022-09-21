import requests
import bs4
from tkinter import *
import tkinter.scrolledtext as tkscrolled
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox #import messagebox library


def lookUpDictionary():
    """
    Webscrapes the term on dictionary.com and writes the results to the result box
    :return: void
    """
    #Clears contents of tab1
    clearTab1()
    #Gets word from input
    term = termInputTab1.get()
    #url of dictionary.com search for vocab word
    url='https://www.dictionary.com/browse/'+term
    #get content of url
    request_result = requests.get(url)
    #parse url
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    #get all of the span tags
    heading_object = soup.find_all('span',class_="one-click-content css-nnyc96 e1q3nk1v1")
    definition = ''
    #for all of the span tags
    for info in heading_object:
        definition += info.getText()
        definition += "\n"
    resultBoxTab1.insert(INSERT, definition)

def lookUpThesaurus():
    """
    Webscrapes the terms on dictionary.com and writes the results to the result box
    :param term: The term to look up
    :return: void
    """
    #Clears contents of tab2
    clearTab2()
    #Gets the term from the input
    term = termInputTab2.get()
    # url of dictionary.com search for vocab word
    url = 'https://www.dictionary.com/browse/' + term
    # get content of url
    request_result = requests.get(url)
    # parse url
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    # get all of the span tags
    #heading_obj = soup.find_all('a',_class='css-1icv1bo e15p0a5t0')
    heading_object = soup.find_all('a',class_="css-1icv1bo e15p0a5t0")
    
    definition = ''
    # for all of the span tags
    for info in heading_object:
        definition += info.getText()
        definition += "\n"
    resultBoxTab2.insert(INSERT, definition)

def clearTab1():
    """
    Clears contents of tab 1
    :return: void
    """
    resultBoxTab1.delete("1.0","end")
def saveTab1():
    """
    Copies definition to clipboard
    :return: void
    """
    window.clipboard_clear()
    window.clipboard_append(resultBoxTab1.get("1.0",END))

def clearTab2():
    """
    Clears contents of tab 2
    :return: void
    """
    resultBoxTab2.delete("1.0","end")
def saveTab2():
    """
    Copies search result to clipboard
    :return: void
    """
    window.clipboard_clear()
    window.clipboard_append(resultBoxTab2.get("1.0",END))

def updateFileName():
    """
    Updates label displaying current file name
    :return: void
    """
    global filePathLabelTab3
    filePathLabelTab3.config(text="Current path: " + currentFile)

def clearTab3():
    """
    Clears contents in tab 3
    :return: void
    """
    resultBoxTab3.delete("1.0","end")

def openTab3():
    """
    Opens file to edit
    :return:
    """
    global currentFile
    #If there is something written in the text box
    if len(str(resultBoxTab3.get(1.0, END)))>1:
        #Ask the user to save
        answer = messagebox.askyesnocancel(title='Save?',message='Save work before open?')
        #If user clicks "yes"
        if (answer == True):
            #save
            if currentFile == "untitled.txt":
                saveAsTab3()
            else:
                saveTab3()
        #elif(answer==False):
            #just open
        #else:
            #don't do anything

    #Clear tab 3 text box
    clearTab3()
    #Get file from user
    filepath = filedialog.askopenfilename(title="Open file okay?",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    #If no file specified
    if filepath == "":
        return
    #Open selected file
    file = open(filepath, 'r')
    #Update current file name and display it
    currentFile = filepath
    updateFileName()
    #Put file contents in text box
    resultBoxTab3.insert(INSERT, file.read()[:-1])
    #Close file
    file.close()

def saveAsTab3():
    """
    Name file and save it
    :return: void
    """
    #save as
    file = filedialog.asksaveasfile(defaultextension = '.txt',
                                    filetypes = [
                                        ("Text file", ".txt"),
                                        ("HTML file", ".html"),
                                        ("All files", ".*"),
                                    ])
    #If no file specified
    if file is None:
        return
    #Get name of file
    filetext = str(resultBoxTab3.get(1.0, END))
    #Update current file and display it
    global currentFile
    currentFile = file.name
    updateFileName()
    #Write text box content to file
    file.write(filetext)
    file.close()

def saveTab3():
    """
    Quick save function
    :return: void
    """
    global currentFile
    #If file has a name
    if currentFile != "untitled.txt":
        #Write content of text box to file
        file = open(currentFile,'w')
        filetext = str(resultBoxTab3.get(1.0, END))
        file.write(filetext)
        file.close()
    else:
        saveAsTab3()
currentFile="untitled.txt"

#Making window
window = Tk()
SIZING = 580
sizing_str = str(SIZING)+"x"+str(SIZING)
QUARTING = (SIZING/4)-10
window.geometry(sizing_str)

#Making notebook that hold the tabs
notebook = ttk.Notebook(window)
#Initializing tabs
tab1 = Frame(notebook)
tab2 = Frame(notebook)
tab3 = Frame(notebook)
#Adding tabs to the notebook
notebook.add(tab1,text="Dictionary")
notebook.add(tab2,text="Thesaurus")
notebook.add(tab3,text="Notes")
notebook.pack(expand=TRUE,fill="both")

"""
Tab1
"""
#Term label
termLabelTab1 = Label(tab1, text = "Term")
termLabelTab1.place(x=QUARTING,y=0)
#Term input
termInputTab1 = Entry(tab1)
termInputTab1.place(x=QUARTING+40,y=0)
#Search button
searchBtnTab1 = Button(tab1,text="Search",command=lookUpDictionary)
searchBtnTab1.place(x=QUARTING+200,y=0)
#Result label
resultLabelTab1 = Label(tab1, text="Definition Result")
resultLabelTab1.place(x=QUARTING+50,y=50)
#Adding scroll wheel to result box
resultBoxTab1 = tkscrolled.ScrolledText(tab1,height=30,width=60)
#Result box
resultBoxTab1.place(x=30,y=80)
#Clear button
clearBtnTab1 = Button(tab1,text="Clear",command=clearTab1)
clearBtnTab1.place(x=540,y=80)
#Save button
saveBtnTab1 = Button(tab1,text="copy to clipboard",command=saveTab1)
saveBtnTab1.place(x=540,y=120)

"""
Tab2
"""
#Term label
termLabelTab2 = Label(tab2, text = "Term")
termLabelTab2.place(x=QUARTING,y=0)
#Input label
termInputTab2 = Entry(tab2)
termInputTab2.place(x=QUARTING+40,y=0)
#Search label
searchBtnTab2 = Button(tab2,text="Search",command=lookUpThesaurus)
searchBtnTab2.place(x=QUARTING+200,y=0)
#Result label
resultLabelTab2 = Label(tab2, text="Thesaurus Result")
resultLabelTab2.place(x=QUARTING+50,y=50)
#Adding scroll wheel to result box
resultBoxTab2 = tkscrolled.ScrolledText(tab2,height=30,width=60)
#Result box
resultBoxTab2.place(x=30,y=80)
#Clear button
clearBtnTab2 = Button(tab2,text="Clear",command=clearTab2)
clearBtnTab2.place(x=540,y=80)
#Save button
saveBtnTab2 = Button(tab2,text="copy to clipboard",command=saveTab2)
saveBtnTab2.place(x=540,y=120)

"""
Tab3
"""
#Displays current file
filePathLabelTab3 = Label(tab3, text="Current path: " + currentFile)
filePathLabelTab3.place(x=QUARTING+50,y=0)
#Notes label
resultLabelTab3 = Label(tab3, text="Notes")
resultLabelTab3.place(x=QUARTING+50,y=30)
#Place to write text
resultBoxTab3 = tkscrolled.ScrolledText(tab3,height=30,width=60)
resultBoxTab3.place(x=30,y=60)
#Open button
openBtnTab3 = Button(tab3,text="open",command=openTab3)
openBtnTab3.place(x=540,y=80)
#Save as button
saveAsBtnTab3 = Button(tab3,text="save as",command=saveAsTab3)
saveAsBtnTab3.place(x=540,y=110)
#Quick save button
saveBtnTab3 = Button(tab3,text="save",command=saveTab3)
saveBtnTab3.place(x=540,y=140)

window.mainloop()