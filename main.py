from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import sqlite3

import addbook,addmember,givebook
con =sqlite3.connect('library.db')
cur = con.cursor()
class Main(object):
    def __init__(self,Master):
        self.Master = Master

        def displayStatistics(evt):
            count_books = cur.execute("SELECT count(Bookid) FROM books").fetchall()
            count_members = cur.execute("SELECT count(memberid) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(bookstatus) FROM books WHERE bookstatus=1").fetchall()
            print(count_books)
            self.lbl_book_count.config(text='Total: '+str(count_books[0][0])+'books in library')
            self.lbl_member_count.config(text='Total member'+str(count_members[0][0]))
            self.lbl_taken_count.config(text='Taken Books'+str(taken_books[0][0]))
            displaybooks(self)

        def displaybooks(self):
            books = cur.execute("SELECT * FROm books").fetchall()
            count = 0

            self.list_books.delete(0,END)
            for book in books:
                print(book)
                self.list_books.insert(count,str(book[0])+"-"+book[1])
                count += 1
            def bookInfo(evt):
                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('-')[0]
                book = cur.execute("SELECT * FROM books WHERE Bookid=?",(id,))
                book_info = book.fetchall()
                print(book_info)
                self.list_details.delete(0,'end')
                self.list_details.insert(0,"Book Name: "+book_info[0][1])
                self.list_details.insert(0, "Book Author: " + book_info[0][2])
                self.list_details.insert(0, "Book Page: " + book_info[0][3])
                self.list_details.insert(0, "Book Language: " + book_info[0][4])
                if book_info[0][5] == 0:
                    self.list_details.insert(4,"Status : Available")
                else:
                    self.list_details.insert(4,"Status : Unavailable")
            def doubleClick(evt):
                global given_id
                value = str(self.list_books.get(self.list_books.curselection()))
                given_id = value.split('-')[0]
                give_book = GiveBook()

            self.list_books.bind('<<ListboxSelect>>',bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>',displayStatistics)
            #self.tabs.bind('<ButtonRelease-1>',displaybooks)
            self.list_books.bind('<Double-Button-1>',doubleClick)
        mainframe= Frame(self.Master)
        mainframe.pack()
        topframe = Frame(mainframe,width=1350,height=70,bg="#f8f8f8",padx=20,relief=SUNKEN,borderwidth=2)
        topframe.pack(side=TOP,fill=X)
        centerframe = Frame(mainframe,width=1350,relief=RIDGE,bg="#e0f0f0",height=680)
        centerframe.pack(side=TOP)
        centerleftframe = Frame(centerframe,width=900,height=700,bg='#e0f0f0',borderwidth=2,relief=SUNKEN)
        centerleftframe.pack(side=LEFT)
        centerRightframe = Frame(centerframe,width=450,height=700,bg='#e0f0f0',borderwidth=2,relief=SUNKEN)
        centerRightframe.pack()
        searbar_frame = LabelFrame(centerRightframe,width=440,height=75,text="SearchBox",bg='#9bc9ff')
        searbar_frame.pack(fill=BOTH)
        self.lbl_search = Label(searbar_frame,text="Search:",font="Arial 12 bold",bg="#9bc9ff",fg="white")
        self.lbl_search.grid(row=0,column=0,padx=20,pady=10)
        self.ent_search= Entry(searbar_frame,width=30,bd=10)
        self.ent_search.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
        self.btn_search = Button(searbar_frame,text="Search",font='arial 12',bg='#fcc324',fg='white',command=self.searchBooks)
        self.btn_search.grid(row=0,column=4,padx=20,pady=20) 


        listbar_frame = LabelFrame(centerRightframe,width=440,height=175,text="ListBox",bg='#fcc324')
        listbar_frame.pack(fill=BOTH)
        lbl_list = Label(listbar_frame,text="Sort by",font="times 16 bold",fg="#2488ff",bg="#fcc324")
        lbl_list.grid(row=0,column=2)
        self.listChoice = IntVar()
        rb1 = Radiobutton(listbar_frame,text='All Books',var=self.listChoice,value=1,bg="#fcc324")
        rb2 = Radiobutton(listbar_frame,text='In Library',var=self.listChoice,value=2,bg="#fcc324")
        rb3 = Radiobutton(listbar_frame,text='Borrowed Books',var=self.listChoice,value=3,bg="#fcc324")

        rb1.grid(row=1,column=0)
        rb2.grid(row=1,column=1)
        rb3.grid(row=1,column=2)

        btn_list = Button(listbar_frame,text="List Books",bg="#2488ff",fg='white',font='arial 12',command=self.listBooks)
        btn_list.grid(row=1,column=3,padx=40,pady=10)

        image_bar = Frame(centerRightframe,width=414,height=350)
        image_bar.pack(fill=BOTH)
        self.title_right=Label(image_bar,text="Welcome to My library",font="arial 16 bold")
        self.title_right.grid(row=0)
        self.img_library=PhotoImage(file='icons/library.png')
        self.lblImg=Label(image_bar,image=self.img_library)
        self.lblImg.grid(row=1)

        self.iconbook=PhotoImage(file='icons/add_book.png')
        self.btnbook = Button(topframe,text='Add Book',image=self.iconbook,compound=LEFT,font="Arial 12 bold",command=self.addBook)
        self.btnbook.pack(side=LEFT,padx=10)
        self.iconmember = PhotoImage(file='icons/users.png')
        self.btnmember = Button(topframe,text='Add Member',padx=10,font="Arial 12 bold",command=self.addMember)
        self.btnmember.configure(image=self.iconmember,compound=LEFT)
        self.btnmember.pack(side=LEFT)
        self.icongive = PhotoImage(file='icons/givebook.png')
        self.btngive = Button(topframe,text="Give Book",padx=10,font="Arial 12 bold",image=self.icongive,compound=LEFT,command=self.giveBook)
        self.btngive.pack(side=LEFT)
        

        self.tabs=ttk.Notebook(centerleftframe,width=900,height=660)
        self.tabs.pack()
        self.tab1_icon=PhotoImage(file='icons/books.png')
        self.tab2_icon=PhotoImage(file='icons/members.png')
        self.tab1=ttk.Frame(self.tabs)
        self.tab2=ttk.Frame(self.tabs)
        self.tabs.add(self.tab1,text='library management',image=self.tab1_icon,compound=LEFT)
        self.tabs.add(self.tab2,text='Statistics',image=self.tab2_icon,compound=LEFT)

        self.list_books = Listbox(self.tab1,width=40,height=30,bd=5,font='times 12 bold')
        self.sb =  Scrollbar(self.tab1,orient=VERTICAL)
        self.list_books.grid(row=0,column=0,padx=(10,0),pady=10,sticky=N)
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)
        self.list_details=Listbox(self.tab1,width=80,height=30,bd=5,font='times 12 bold')
        self.list_details.grid(row=0,column=1,padx=(10,0),pady=10,sticky=N)
        self.lbl_book_count=Label(self.tab2,text="",font='verdana 14 bold',pady=20)
        self.lbl_book_count.grid(row=0)
        self.lbl_member_count = Label(self.tab2,text="",font='verdana 14 bold',pady=20)
        self.lbl_member_count.grid(row=1,sticky=W)
        self.lbl_taken_count = Label(self.tab2,text="" ,font='verdana 14 bold',pady=20)
        self.lbl_taken_count.grid(row=2,sticky=W)

        displaybooks(self)
        displayStatistics(self)
    def addBook(self):
        add=addbook.AddBook()
    def addMember(self):
        member=addmember.AddMember()
    def searchBooks(self):
        value = self.ent_search.get()
        search = cur.execute("SELECT * FROM books WHERE bookname LIKE ?",('%'+value+'%',)).fetchall()
        print(search)
        self.list_books.delete(0,END)
        count = 0
        for book in search:
            self.list_books.insert(count,str(book[0])+"-"+book[1])
            count += 1
    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allbooks = cur.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0,END)

            count = 0
            for book in allbooks:
                self.list_books.insert(count,str(book[0])+"-"+book[1])
                count += 1
        elif value==2:
            book_in_library = cur.execute("SELECT * FROM books WHERE bookstatus = ?",(0,)).fetchall()
            self.list_books.delete(0,END)
            count = 0
            for book in book_in_library:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        else:
            taken_books = cur.execute("SELECT * FROM books WHERE bookstatus = ?",(0,)).fetchall()
            self.list_books.delete(0, END)
            count = 0
            for book in taken_books:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
    def giveBook(self):
        give_book = givebook.GiveBook()
class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False,False)
        global given_id
        self.Bookid = int(given_id)
        query = "SELECT * FROM books"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(str(book[0])+"-"+book[1])
        query2 = "SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0])+"-"+member[1])

        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)
        self.bottomFrame = Frame(self, height=600, bg='#fcc234')
        self.bottomFrame.pack(fill=X)

        self.top_image = PhotoImage(file='icons/addperson.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text='Add Person', font='Arial 12 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)
        self.bookname = StringVar()
        self.lbl_name = Label(self.bottomFrame, text='BookName:', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame,textvariable=self.bookname)
        self.combo_name['values']=book_list
        self.combo_name.current(self.Bookid-1)
        self.combo_name.place(x=150,y=45)



        self.membername = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text='Member Name:', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.membername)
        self.combo_member['values']=member_list
        self.combo_member.place(x=150, y=85)

        button = Button(self.bottomFrame, text='Lend Book',command=self.lendBook)
        button.place(x=220, y=150)
    def lendBook(self):
        bookname = self.bookname.get()
        membername = self.membername.get()
        if (bookname and membername != ""):
            try:
                query = "INSERT INTO 'borrows' (bbookid,bmemberid) VALUES(?,?)"
                cur.execute(query,(bookname,membername))
                con.commit()
                messagebox.showinfo("Success","Success added to database",icon='info')
                cur.execute("UPDATE books SET bookstatus=? WHERE Bookid =?",(1,self.Bookid))
                con.commit()

            except:
                messagebox.showerror("Error", "Cant add to database", icon='warning')
        else:
            messagebox.showerror("Error","Fields cant be empty",icon='warning')

def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1350x750+300+200")
    root.iconbitmap('icons/icon.ico')
    root.mainloop()
if __name__=='__main__':
    main()