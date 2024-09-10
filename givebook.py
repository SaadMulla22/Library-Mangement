from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import sqlite3
con =sqlite3.connect('library.db')
cur = con.cursor()
class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False,False)
        query = "SELECT * FROM books WHERE bookstatus=0"
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
        heading = Label(self.topFrame, text='Lend a Book', font='Arial 12 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)
        self.bookname = StringVar()
        self.lbl_name = Label(self.bottomFrame, text='BookName:', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame,textvariable=self.bookname)
        self.combo_name['values']=book_list
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
        self.Bookid = bookname.split('-')[0]
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
