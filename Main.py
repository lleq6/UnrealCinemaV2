import sqlite3
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def GetConnection():
    return sqlite3.connect("Database/Cinema.db")

def MainWindow():
    Root = Tk()
    Root.title("Unreal Cinema V.2")
    Width = 900
    Height = 600
    X = Root.winfo_screenwidth() / 2 - Width / 2
    Y = Root.winfo_screenheight() / 2 - Height / 2
    Root.resizable(False, False)
    Root.geometry("%dx%d+%d+%d"%(Width, Height, X, Y))
    Root.iconphoto(False, PhotoImage(file="Image/Application.png"))
    Root.option_add("*font", "Helvetica 10")
    Root.rowconfigure(0, weight=1)
    Root.columnconfigure(0, weight=5)
    Root.columnconfigure(1, weight=1)
    return Root

def ShowMovies():
    if UID.get() == 0:
        ButtonLogin["text"] = "Sign in"
        ButtonLogin["image"] = IconSignIn
        ButtonLogin["command"] = LoginFrame
        ButtonLogin["bg"] = "#709fb0"
        ButtonLogin["fg"] = "white"
    else:
        ButtonLogin["text"] = "Sign out"
        ButtonLogin["image"] = IconSignOut
        ButtonLogin["command"] = OnLogout
        ButtonLogin["bg"] = "#709fb0"
        ButtonLogin["fg"] = "white"
        ButtonProfile["text"] = "Profile"
        ButtonProfile["image"] = IconProfile
        ButtonProfile["command"] = ProfileFrame
        ButtonProfile["bg"] = "#709fb0"
        ButtonProfile["fg"] = "white"
        ButtonTicket["text"] = "Tickets"
        ButtonTicket["image"] = IconTicket
        ButtonTicket["command"] = ShowTickets
        ButtonTicket["bg"] = "#709fb0"
        ButtonTicket["fg"] = "white"
    Movies = Frame(Root, bg="#709fb0")
    Movies.rowconfigure(2, weight=1)
    Movies.columnconfigure((0, 1), weight=1)
    Label(Movies, text="Unreal Cinema V.2 : Movies", font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=0, columnspan=2, pady=10)
    Button(Movies, image=IconNowShowing, text="Now Showing", bg="#28527a", fg="white", command=lambda:OnChange(1), compound=LEFT).grid(row=1, column=0, padx=10, ipadx=10, pady=10, sticky="e")
    Button(Movies, image=IconComingSoon, text="Coming Soon", bg="#28527a", fg="white", command=lambda:OnChange(0), compound=LEFT).grid(row=1, column=1, padx=10, ipadx=10, pady=10, sticky="w")
    Body = Canvas(Movies, bg="#709fb0")
    PosterFrame = Frame(Body, bg="#709fb0")
    PosterFrame.columnconfigure((0, 1), weight=1)
    LoadMovie(PosterFrame)
    Body.create_window((0, 0), window=PosterFrame, anchor="n", width=735)
    Scroller = Scrollbar(Movies, orient=VERTICAL, command=Body.yview)
    Scroller.grid(row=2, column=1, sticky="nes")
    Body.configure(yscrollcommand=Scroller.set)
    PosterFrame.update_idletasks()
    Body.config(scrollregion=Body.bbox("all"))
    Body.grid(row=2, columnspan=2, sticky="news")
    Movies.grid(row=0, column=0, sticky="news")

def CreateMenu():
    global MenuBar
    global ButtonLogin
    global ButtonProfile
    global ButtonTicket
    MenuBar = Frame(Root, bg="#28527a")
    MenuBar.columnconfigure((0, 1), weight=1)
    Label(MenuBar, textvariable=Title, bg="#28527a", fg="white").grid(row=0, columnspan=2, pady=10)
    ButtonLogin = Button(MenuBar, image=IconSignIn, text="Sign in", bg="#709fb0", fg="white", command=LoginFrame, compound=LEFT, width=70)
    ButtonLogin.grid(row=1, ipadx=10, columnspan=2, pady=10)
    ButtonProfile = Button(MenuBar, image=IconProfile, text="Profile", bg="#709fb0", fg="white", command=ProfileFrame, compound=LEFT, width=70)
    ButtonTicket = Button(MenuBar, image=IconTicket, text="Tickets", bg="#709fb0", fg="white", command=ShowTickets, compound=LEFT, width=70)
    if UID.get() != 0:
        ButtonProfile.grid(row=2, columnspan=2, pady=10, ipadx=10)
        ButtonTicket.grid(row=3, columnspan=2, pady=10, ipadx=10)
    MenuBar.grid(row=0, column=1, sticky="news")

def LoginFrame():
    SetDefault()
    global UsernameEntry
    global PasswordEntry
    ButtonLogin["text"] = "Back"
    ButtonLogin["image"] = IconBack
    ButtonLogin["command"] = ShowMovies
    ButtonLogin["bg"] = "orange"
    ButtonLogin["fg"] = "black"
    Login = Frame(Root, bg="#709fb0")
    Login.columnconfigure((0, 1), weight=1)
    Label(Login, text="Unreal Cinema V.2 : Sign in", font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=0, columnspan=2, pady=10)
    Label(Login, bg="#709fb0").grid(row=1, pady=10)
    Label(Login, bg="#709fb0").grid(row=2, pady=10)
    Label(Login, image=IconLogin, bg="#709fb0").grid(row=3, columnspan=2, pady=3)
    Label(Login, text="Username", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=4, columnspan=2, pady=3)
    UsernameEntry = Entry(Login, font=("Helvetica 16"), bg="#28527a", fg="white", textvariable=Username)
    UsernameEntry.grid(row=5, columnspan=2, pady=3)
    Label(Login, text="Password", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=6, columnspan=2, pady=3)
    PasswordEntry = Entry(Login, font=("Helvetica 16"), bg="#28527a", fg="white", textvariable=Password, show="*")
    PasswordEntry.grid(row=7, columnspan=2, pady=3)
    Label(Login, bg="#709fb0").grid(row=8, pady=5)
    Button(Login, image=IconSignIn, text="Sign in", font=("Helvetica 12"), bg="#28527a", fg="white", width=70, command=OnLogin, compound=LEFT).grid(row=9, column=0, padx=10, pady=10, sticky="e", ipadx=10)
    Button(Login, image=IconSignUp, text="Sign up", font=("Helvetica 12"), bg="#28527a", fg="white", width=70, command=RegisterFrame, compound=LEFT).grid(row=9, column=1, padx=10, pady=10, sticky="w", ipadx=10)
    Login.grid(row=0, column=0, sticky="news")

def OnLogin():
    if UsernameEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter username!")
        UsernameEntry.focus()
    elif PasswordEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter password!")
        PasswordEntry.focus()
    else:
        Connection = GetConnection()
        Cursor = Connection.cursor()
        Cursor.execute("SELECT * FROM Accounts WHERE Username = ? AND Password = ?", [Username.get(), Password.get()])
        Data = Cursor.fetchone()
        if Data:
            UID.set(Data[0])
            Firstname.set(Data[3])
            Lastname.set(Data[4])
            Title.set("Welcome\n{0} {1}".format(Firstname.get(), Lastname.get()))
            ShowMovies()
            ShowButton()
        else:
            messagebox.showwarning("Unreal Cinema V.2", "Username is invalid or password is invalid.\nPlease try again.")
            PasswordEntry.focus()

def ShowButton():
    ButtonProfile.grid(row=2, columnspan=2, pady=10, ipadx=10)
    ButtonTicket.grid(row=3, columnspan=2, pady=10, ipadx=10)

def ProfileFrame():
    global FirstnameEntry
    global LastnameEntry
    global OldPasswordEntry
    global NewPasswordEntry
    global ConfirmNewPasswordEntry
    ButtonProfile["text"] = "Back"
    ButtonProfile["image"] = IconBack
    ButtonProfile["command"] = ShowMovies
    ButtonProfile["bg"] = "orange"
    ButtonProfile["fg"] = "black"
    ButtonTicket["text"] = "Tickets"
    ButtonTicket["image"] = IconTicket
    ButtonTicket["command"] = ShowTickets
    ButtonTicket["bg"] = "#709fb0"
    ButtonTicket["fg"] = "white"
    DetailFrame = Frame(Root, bg="#709fb0")
    DetailFrame.rowconfigure((1, 2), weight=1)
    DetailFrame.columnconfigure((0, 1), weight=1)
    Label(DetailFrame, text="Unreal Cinema V.2 : Profile", font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=0, columnspan=2, pady=10)
    Profile = Frame(DetailFrame, bg="#709fb0")
    Profile.columnconfigure((0, 1), weight=1)
    Label(Profile, image=IconUser, bg="#709fb0").grid(row=0, columnspan=2, pady=10)
    Label(Profile, text="Firstname :", bg="#709fb0", fg="white").grid(row=1, column=0, sticky="e", pady=10)
    Label(Profile, text="Lastname :", bg="#709fb0", fg="white").grid(row=2, column=0, sticky="e", pady=10)
    FirstnameEntry = Entry(Profile, textvariable=Firstname, bg="#28527a", fg="white")
    FirstnameEntry.grid(row=1, column=1, sticky="w", pady=10)
    LastnameEntry = Entry(Profile, textvariable=Lastname, bg="#28527a", fg="white")
    LastnameEntry.grid(row=2, column=1, sticky="w", pady=10)
    Button(Profile, image=IconSave, text="Save", width=70, bg="#28527a", fg="white", command=OnSaveProfile, compound=LEFT).grid(row=3, columnspan=2, pady=10, ipadx=10)
    Profile.grid(row=1, column=0, sticky="news")
    PasswordFrame = Frame(DetailFrame, bg="#709fb0")
    PasswordFrame.columnconfigure((0, 1), weight=1)
    Label(PasswordFrame, image=IconPassword, bg="#709fb0").grid(row=0, columnspan=2, pady=10)
    Label(PasswordFrame, text="Old Password :", bg="#709fb0", fg="white").grid(row=1, column=0, sticky="e", pady=10)
    Label(PasswordFrame, text="New Password :", bg="#709fb0", fg="white").grid(row=2, column=0, sticky="e", pady=10)
    Label(PasswordFrame, text="Confirm New Password :", bg="#709fb0", fg="white").grid(row=3, column=0, sticky="e", pady=10)
    OldPasswordEntry = Entry(PasswordFrame, textvariable=OldPassword, bg="#28527a", fg="white", show="*")
    OldPasswordEntry.grid(row=1, column=1, sticky="w", pady=10)
    NewPasswordEntry = Entry(PasswordFrame, textvariable=NewPassword, bg="#28527a", fg="white", show="*")
    NewPasswordEntry.grid(row=2, column=1, sticky="w", pady=10)
    ConfirmNewPasswordEntry = Entry(PasswordFrame, textvariable=ConfirmNewPassword, bg="#28527a", fg="white", show="*")
    ConfirmNewPasswordEntry.grid(row=3, column=1, sticky="w", pady=10)
    Button(PasswordFrame, image=IconChange, text="Change Password", width=120, bg="#28527a", fg="white", command=OnChangePassword, compound=LEFT).grid(row=4, columnspan=2, pady=10, ipadx=10)
    PasswordFrame.grid(row=1, column=1, sticky="news")
    CardFrame = Frame(DetailFrame, bg="#709fb0")
    CardFrame.columnconfigure((0, 1), weight=1)
    Connection = GetConnection()
    Cursor = Connection.cursor()
    Cursor.execute("SELECT * FROM MemberCards WHERE UID = ?", [UID.get()])
    Data = Cursor.fetchone()
    if Data:
        Label(CardFrame, image=IconCard, text="Membership on {0}".format(Data[2]), bg="#709fb0", fg="white", compound=TOP).grid(row=0, columnspan=2, pady=10)
        Button(CardFrame, image=IconCancel, text="Cancel Membership", bg="orange", fg="white", width=120, command=OnCancelMembership, compound=LEFT).grid(row=1, columnspan=2, pady=10, ipadx=10)
    else:
        Label(CardFrame, image=IconNoCard, text="No Member Card", bg="#709fb0", fg="white", compound=TOP).grid(row=0, columnspan=2, pady=10)
        Label(CardFrame, text="Member Card Discount 20%", bg="#709fb0", fg="white").grid(row=1, columnspan=2, pady=10)
        Label(CardFrame, text="Price : 150 Baht", bg="#709fb0", fg="white").grid(row=2, columnspan=2, pady=10)
        Button(CardFrame, image=IconBuy, text="Buy", bg="#28527a", fg="white", width=70, command=OnBuyCard, compound=LEFT).grid(row=3, columnspan=2, pady=10, ipadx=10)
    CardFrame.grid(row=2, columnspan=2, sticky="news")
    DetailFrame.grid(row=0, column=0, sticky="news")

def OnBuyCard():
    Condition = messagebox.askyesno("Unreal Cinema V.2", "Do you want to buy a member card?")
    if Condition:
        TimeNow = datetime.datetime.now()
        Connection = GetConnection()
        Cursor = Connection.cursor()
        Cursor.execute("INSERT INTO MemberCards (UID, Date) VALUES (?, ?)", [UID.get(), TimeNow.strftime("%m/%d/%Y")])
        Connection.commit()
        messagebox.showinfo("Unreal Cinema V.2", "Buy member card successfully.")
        ProfileFrame()

def OnCancelMembership():
    Condition = messagebox.askyesno("Unreal Cinema V.2", "Do you want to cancel a membership?")
    if Condition:
        Connection = GetConnection()
        Cursor = Connection.cursor()
        Cursor.execute("DELETE FROM MemberCards WHERE UID = ?", [UID.get()])
        Connection.commit()
        messagebox.showinfo("Unreal Cinema V.2", "Cancel membership successfully.")
        ProfileFrame()

def OnSaveProfile():
    if FirstnameEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter firstname!")
        FirstnameEntry.focus()
    elif LastnameEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter lastname!")
        LastnameEntry.focus()
    else:
        Connection = GetConnection()
        Cursor = Connection.cursor()
        Cursor.execute("UPDATE Accounts SET Firstname = ?, Lastname = ? WHERE ID = ?", [Firstname.get(), Lastname.get(), UID.get()])
        Connection.commit()
        Title.set("Welcome\n{0} {1}".format(Firstname.get(), Lastname.get()))
        messagebox.showinfo("Unreal Cinema V.2", "Save successfully.")

def OnChangePassword():
    if OldPasswordEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter old password!")
        OldPasswordEntry.focus()
    elif NewPasswordEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter new password!")
        NewPasswordEntry.focus()
    elif ConfirmNewPasswordEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter confirm new password!")
        ConfirmNewPasswordEntry.focus()
    else:
        if NewPasswordEntry.get() == ConfirmNewPasswordEntry.get():
            Connection = GetConnection()
            Cursor = Connection.cursor()
            Cursor.execute("SELECT Password FROM Accounts WHERE ID = ?", [UID.get()])
            Data = Cursor.fetchone()
            if Data:
                if OldPassword.get() == Data[0]:
                    Cursor.execute("UPDATE Accounts SET Password = ? WHERE ID = ?", [NewPassword.get(), UID.get()])
                    Connection.commit()
                    messagebox.showinfo("Unreal Cinema V.2", "Change password successfully.")
                    OldPassword.set("")
                    NewPassword.set("")
                    ConfirmNewPassword.set("")
                else:
                    messagebox.showwarning("Unreal Cinema V.2", "Old password you entered did not match!")
                    NewPasswordEntry.focus()
            else:
                messagebox.showinfo("Unreal Cinema V.2", "Change password unsuccessfully.")
        else:
            messagebox.showwarning("Unreal Cinema V.2", "Confirm password you entered did not match!")
            ConfirmNewPasswordEntry.focus()

def ShowTickets():
    ButtonTicket["text"] = "Back"
    ButtonTicket["image"] = IconBack
    ButtonTicket["command"] = ShowMovies
    ButtonTicket["bg"] = "orange"
    ButtonTicket["fg"] = "black"
    ButtonProfile["text"] = "Profile"
    ButtonProfile["image"] = IconProfile
    ButtonProfile["command"] = ProfileFrame
    ButtonProfile["bg"] = "#709fb0"
    ButtonProfile["fg"] = "white"
    TicketFrame = Frame(Root, bg="#709fb0")
    TicketFrame.rowconfigure(1, weight=1)
    TicketFrame.columnconfigure((0, 1), weight=1)
    Label(TicketFrame, text="Unreal Cinema V.2 : Tickets", font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=0, columnspan=2, pady=10)
    Body = Canvas(TicketFrame, bg="#709fb0")
    PosterFrame = Frame(Body, bg="#709fb0")
    PosterFrame.columnconfigure((0, 1, 2), weight=1)
    Connection = GetConnection()
    Cursor = Connection.cursor()
    Cursor.execute("SELECT * FROM Tickets WHERE UID = ? ORDER BY TID ASC", [UID.get()])
    Data = Cursor.fetchall()
    if Data:
        Row = 1
        Column = 0
        for Ticket in Data:
            Label(PosterFrame, image=Tickets[Ticket[2] - 1], bg="#709fb0").grid(row=Row - 1, column=Column, pady=5)
            Button(PosterFrame, image=IconMagnifiying, bg="#28527a", command=lambda Index = Ticket[0]:OnSelectTicket(Index)).grid(row=Row - 1, column=Column, pady=5)
            Label(PosterFrame, text="TICKET : {0}\n{1}".format(Ticket[0], GetMovieName(Ticket[2])), bg="#709fb0", fg="white").grid(row=Row, column=Column, pady=10, sticky="s")
            Column += 1
            if Column == 3:
                Column = 0
                Row += 2
    else:
        MainFrame = Frame(TicketFrame, bg="#709fb0")
        MainFrame.rowconfigure(0, weight=1)
        MainFrame.columnconfigure((0, 1), weight=1)
        Label(MainFrame, text="No Ticket!", font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=0, columnspan=2, pady=10)
        MainFrame.grid(row=1, columnspan=2, sticky="news")
    Body.create_window((0, 0), window=PosterFrame, anchor="n", width=735)
    Scroller = Scrollbar(TicketFrame, orient=VERTICAL, command=Body.yview)
    Scroller.grid(row=1, column=1, sticky="nes")
    Body.configure(yscrollcommand=Scroller.set)
    PosterFrame.update_idletasks()
    Body.config(scrollregion=Body.bbox("all"))
    Body.grid(row=1, columnspan=2, sticky="news")
    TicketFrame.grid(row=0, column=0, sticky="news")

def GetMovieName(ID):
    Name = ""
    Connection = GetConnection()
    Cursor = Connection.cursor()
    Cursor.execute("SELECT Name FROM Movies WHERE ID = ?", [ID])
    Data = Cursor.fetchone()
    if Data:
        Name = Data[0]
    else:
        Name = "Unknown"
    return Name

def OnSelectTicket(ID):
    ButtonTicket["command"] = ShowTickets
    TicketFrame = Frame(Root, bg="#709fb0")
    TicketFrame.rowconfigure((1, 2), weight=1)
    TicketFrame.columnconfigure((0, 1), weight=1)
    Label(TicketFrame, text="Unreal Cinema V.2 : Ticket ID {0}".format(ID), font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=0, columnspan=2, pady=10)
    Connection = GetConnection()
    Cursor = Connection.cursor()
    Cursor.execute("SELECT * FROM Tickets WHERE TID = ?", [ID])
    Data = Cursor.fetchone()
    if Data:
        DetailFrame = Frame(TicketFrame, bg="#709fb0")
        DetailFrame.columnconfigure((0, 1), weight=1)
        Label(DetailFrame, image=Posters[Data[2] - 1], bg="#709fb0").grid(row=0, columnspan=2, pady=10)
        Label(DetailFrame, text=GetMovieName(Data[2]), font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=1, columnspan=2, pady=8)
        Label(DetailFrame, text="Showtime :", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=2, column=0, pady=8, sticky="e")
        Label(DetailFrame, text=Data[3], font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=2, column=1, pady=8, sticky="w")
        Label(DetailFrame, text="Seat no", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=3, columnspan=2, pady=8)
        Label(DetailFrame, text=Data[4], font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=4, columnspan=2, pady=8)
        DetailFrame.grid(rowspan=3, columnspan=2, sticky="news")
    else:
        ErrorFrame = Frame(TicketFrame, bg="#709fb0")
        ErrorFrame.rowconfigure(0, weight=1)
        ErrorFrame.columnconfigure((0, 1), weight=1)
        Label(ErrorFrame, text="No Data Ticket!", font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=0, columnspan=2)
        ErrorFrame.grid(rowspan=3, columnspan=2, sticky="news")
    TicketFrame.grid(row=0, column=0, sticky="news")

def OnLogout():
    ButtonLogin["text"] = "Sign in"
    ButtonLogin["image"] = IconSignIn
    ButtonLogin["command"] = LoginFrame
    ButtonLogin["bg"] = "#709fb0"
    ButtonLogin["fg"] = "white"
    ButtonProfile.grid_forget()
    ButtonTicket.grid_forget()
    SetDefault()
    ShowMovies()

def SetDefault():
    UID.set(0)
    Username.set("")
    Password.set("")
    ConfirmPassword.set("")
    Firstname.set("")
    Lastname.set("")
    Title.set("")

def RegisterFrame():
    SetDefault()
    global UsernameEntry
    global PasswordEntry
    global ConfirmPasswordEntry
    global FirstnameEntry
    global LastnameEntry
    ButtonLogin["text"] = "Back"
    ButtonLogin["image"] = IconBack
    ButtonLogin["command"] = LoginFrame
    ButtonLogin["bg"] = "orange"
    ButtonLogin["fg"] = "black"
    Login = Frame(Root, bg="#709fb0")
    Login.columnconfigure((0, 1), weight=1)
    Label(Login, text="Unreal Cinema V.2 : Sign up", font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=0, columnspan=2, pady=10)
    Label(Login, image=IconLogin, bg="#709fb0").grid(row=1, columnspan=2, pady=3)
    Label(Login, text="Username", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=2, columnspan=2, pady=3)
    UsernameEntry = Entry(Login, font=("Helvetica 16"), bg="#28527a", fg="white", textvariable=Username)
    UsernameEntry.grid(row=3, columnspan=2, pady=3)
    Label(Login, text="Password", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=4, columnspan=2, pady=3)
    PasswordEntry = Entry(Login, font=("Helvetica 16"), bg="#28527a", fg="white", textvariable=Password, show="*")
    PasswordEntry.grid(row=5, columnspan=2, pady=3)
    Label(Login, text="Confirm Password", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=6, columnspan=2, pady=3)
    ConfirmPasswordEntry = Entry(Login, font=("Helvetica 16"), bg="#28527a", fg="white", textvariable=ConfirmPassword, show="*")
    ConfirmPasswordEntry.grid(row=7, columnspan=2, pady=3)
    Label(Login, text="Firstname", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=8, columnspan=2, pady=3)
    FirstnameEntry = Entry(Login, font=("Helvetica 16"), bg="#28527a", fg="white", textvariable=Firstname)
    FirstnameEntry.grid(row=9, columnspan=2, pady=3)
    Label(Login, text="Lastname", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=10, columnspan=2, pady=3)
    LastnameEntry = Entry(Login, font=("Helvetica 16"), bg="#28527a", fg="white", textvariable=Lastname)
    LastnameEntry.grid(row=11, columnspan=2, pady=3)
    Label(Login, bg="#709fb0").grid(row=12, pady=1)
    Button(Login, image=IconSignUp, text="Sign up", font=("Helvetica 12"), bg="#28527a", fg="white", width=100, command=OnRegister, compound=LEFT).grid(row=13, columnspan=2, padx=10, pady=10, ipady=5, ipadx=10)
    Login.grid(row=0, column=0, sticky="news")

def OnRegister():
    if UsernameEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter username!")
        UsernameEntry.focus()
    elif PasswordEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter password!")
        PasswordEntry.focus()
    elif ConfirmPasswordEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter confirm password!")
        ConfirmPasswordEntry.focus()
    elif FirstnameEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter firstname!")
        FirstnameEntry.focus()
    elif LastnameEntry.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please enter lastname!")
        LastnameEntry.focus()
    else:
        if PasswordEntry.get() == ConfirmPasswordEntry.get():
            Connection = GetConnection()
            Cursor = Connection.cursor()
            Cursor.execute("SELECT Username FROM Accounts WHERE Username = ?", [Username.get()])
            Data = Cursor.fetchall()
            if Data:
                messagebox.showwarning("Unreal Cinema V.2", "Username '{0}' already exists!\nPlease try again.".format(Username.get()))
                UsernameEntry.focus()
            else:
                Cursor.execute("INSERT INTO Accounts (Username, Password, Firstname, Lastname) VALUES (?, ?, ?, ?)", [Username.get(), Password.get(), Firstname.get(), Lastname.get()])
                Connection.commit()
                messagebox.showinfo("Unreal Cinema V.2", "Register successfully!")
                UID.set(0)
                Username.set("")
                Password.set("")
                ConfirmPassword.set("")
                Firstname.set("")
                Lastname.set("")
                Title.set("")
                LoginFrame()
        else:
            messagebox.showwarning("Unreal Cinema V.2", "The passwords you entered did not match!")
            ConfirmPasswordEntry.focus()

def LoadPoster():
    Connection = GetConnection()
    Cursor = Connection.cursor()
    Cursor.execute("SELECT ID FROM Movies ORDER BY ID ASC")
    Data = Cursor.fetchall()
    for Movie in Data:
        Posters.append(PhotoImage(file="Poster/{0}.png".format(Movie[0])))
        Tickets.append(PhotoImage(file="Poster/{0}.png".format(Movie[0])).subsample(2, 2))

def LoadMovie(PosterFrame):
    Connection = GetConnection()
    Cursor = Connection.cursor()
    Cursor.execute("SELECT * FROM Movies WHERE IsShow = ? ORDER BY ID DESC", [IsShow])
    Data = Cursor.fetchall()
    Row = 1
    Column = 0
    for Movie in Data:
        Button(PosterFrame, image=Posters[Movie[0] - 1], bg="#28527a" if Movie[5] == 1 else "red", command=lambda Index = Movie[0]:OnSelectMovie(Index)).grid(row=Row - 1, column=Column, pady=5)
        Label(PosterFrame, text="{0}\nDate: {1} IMDb : {2}".format(Movie[1], Movie[3], Movie[4]), bg="#709fb0", fg="white").grid(row=Row, column=Column, pady=10, sticky="s")
        Column += 1
        if Column == 2:
            Column = 0
            Row += 2

def OnChange(Value):
    global IsShow
    if Value == 1:
        IsShow = Value
    else:
        IsShow = Value
    ShowMovies()

def OnSelectMovie(Index):
    global Showtimes
    Connection = GetConnection()
    Cursor = Connection.cursor()
    Cursor.execute("SELECT Name, IsShow FROM Movies WHERE ID = ?", [Index])
    Movie = Cursor.fetchone()
    if Movie:
        if Movie[1] == 1:
            SelectedIndex.set(Index)
            MovieName.set(Movie[0])
            Cursor.execute("SELECT [Index], Showtime FROM Showtimes WHERE ID = ?", [Index])
            Showtimes = Cursor.fetchall()
            if Showtimes:
                Showtime()
            else:
                MainFrame = Frame(Root, bg="#709fb0")
                MainFrame.rowconfigure(1, weight=1)
                MainFrame.columnconfigure((0, 1), weight=1)
                Button(MainFrame, image=IconBack, text="Back", bg="#28527a", fg="white", width=70, command=OnBack, compound=LEFT).grid(row=0, column=0, sticky="w", padx=10, pady=10, ipadx=10)
                Label(MainFrame, text="Movie ID: {0} No Movie Showtime!".format(Index), font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=1, columnspan=2)
                MainFrame.grid(row=0, column=0, sticky="news")
        else:
            MainFrame = Frame(Root, bg="#709fb0")
            MainFrame.rowconfigure(1, weight=1)
            MainFrame.columnconfigure((0, 1), weight=1)
            Button(MainFrame, image=IconBack, text="Back", bg="#28527a", fg="white", width=70, command=OnBack, compound=LEFT).grid(row=0, column=0, sticky="w", padx=10, pady=10, ipadx=10)
            Label(MainFrame, text="No Movie Showtime!", font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=1, columnspan=2)
            MainFrame.grid(row=0, column=0, sticky="news")
    else:
        MainFrame = Frame(Root, bg="#709fb0")
        MainFrame.rowconfigure(1, weight=1)
        MainFrame.columnconfigure((0, 1), weight=1)
        Button(MainFrame, image=IconBack, text="Back", bg="#28527a", fg="white", width=70, command=OnBack, compound=LEFT).grid(row=0, column=0, sticky="w", padx=10, pady=10, ipadx=10)
        Label(MainFrame, text="Movie ID {0} Data Not found!".format(Index), font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=1, columnspan=2)
        MainFrame.grid(row=0, column=0, sticky="news")

def Showtime():
    SelectedShowtime.set("")
    global Tree
    MainFrame = Frame(Root, bg="#709fb0")
    MainFrame.rowconfigure(1, weight=1)
    MainFrame.columnconfigure((0, 1, 2), weight=1)
    Button(MainFrame, image=IconBack, text="Back", bg="#28527a", fg="white", width=70, command=OnBack, compound=LEFT).grid(row=0, column=0, sticky="w", padx=10, pady=10, ipadx=10)
    Label(MainFrame, textvariable=MovieName, font=("Helvetica 12 bold"), bg="#709fb0", fg="white").grid(row=0, column=1, padx=10, pady=10)
    Button(MainFrame, image=IconNext, text="Next", bg="#28527a", fg="white", width=70, command=OnNext, compound=RIGHT).grid(row=0, column=2, sticky="e", padx=10, pady=10, ipadx=10)
    Tree = ttk.Treeview(MainFrame, show="headings", columns=("#1", "#2"))
    Scroll = ttk.Scrollbar(MainFrame, orient="vertical", command=Tree.yview)
    Scroll.grid(row=1, column=2, sticky="nes")
    Tree.configure(yscrollcommand=Scroll.set)
    Tree.grid(row=1, columnspan=3, sticky="news")
    Tree.heading("#1", text="Index")
    Tree.heading("#2", text="Showtime")
    Tree.column("#1", width=100, minwidth=100, anchor=CENTER)
    Tree.column("#2", width=100, minwidth=100, anchor=CENTER)
    Tree.bind("<<TreeviewSelect>>", OnSelectShowtime)
    for Showtime in Showtimes:
        Tree.insert("", END, values=Showtime)
    MainFrame.grid(row=0, column=0, sticky="news")

def OnSelectShowtime(Event):
    for Item in Tree.selection():
        Showtime = Tree.item(Item)['values']
        SelectedShowtime.set(Showtime[1])

def OnBack():
    SelectedIndex.set("")
    SelectedShowtime.set("")
    ShowMovies()

def OnNext():
    if SelectedShowtime.get() == "":
        messagebox.showwarning("Unreal Cinema V.2", "Please select showtime.")
    else:
        ShowSeats()

def ShowSeats():
    SelectedSeatList.clear()
    global SeatVariable
    Connection = GetConnection()
    Cursor = Connection.cursor()
    MainFrame = Frame(Root, bg="#709fb0")
    MainFrame.rowconfigure(1, weight=1)
    MainFrame.columnconfigure((0, 1, 2), weight=1)
    Button(MainFrame, image=IconBack, text="Back", bg="#28527a", fg="white", width=70, command=Showtime, compound=LEFT).grid(row=0, column=0, sticky="w", padx=10, pady=10, ipadx=10)
    Label(MainFrame, text="{0} ({1})".format(MovieName.get(), SelectedShowtime.get()), font=("Helvetica 12 bold"), bg="#709fb0", fg="white").grid(row=0, column=1, padx=10, pady=10)
    Button(MainFrame, image=IconNext, text="Checkout", bg="#28527a", fg="white", width=70, command=OnCheckout, compound=RIGHT).grid(row=0, column=2, sticky="e", padx=10, pady=10, ipadx=10)
    Cursor.execute("SELECT SeatID FROM Seats WHERE ID = ? AND Showtime = ?", [SelectedIndex.get(), SelectedShowtime.get()])
    Data = Cursor.fetchall()
    if Data:
        SeatVariable = [IntVar() for i in range(len(Data))]
        SeatFrame = Frame(MainFrame, bg="#709fb0")
        SeatFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        Label(SeatFrame, image=IconSeatEnable, text="Executive 200 Baht", font=("Helvetica 12 bold"), compound=LEFT, bg="#709fb0", fg="white").grid(row=0, columnspan=10, pady=20)
        Row = 2
        Column = 0
        for Seat in Data:
            Convert = str(Seat[0]).split()[0][1] + str(Seat[0]).split()[0][2]
            Seats = GetSeatInTicket()
            if Seat[0] in Seats:
                Label(SeatFrame, image=IconSeatDisable, bg="#709fb0").grid(row=Row - 1, column=Column)
                Checkbutton(SeatFrame, text=Seat[0], bg="#709fb0", compound=LEFT, variable=DisableSeat, command=OnSelectSeatDisable).grid(row=Row, column=Column, pady=10, sticky="s")
            else:
                Label(SeatFrame, image=IconSeatEnable, bg="#709fb0").grid(row=Row - 1, column=Column)
                Checkbutton(SeatFrame, text=Seat[0], bg="#709fb0", compound=LEFT, variable=SeatVariable[int(Convert) - 1], command=lambda SeatID = Seat[0]:OnSelectSeat(SeatID)).grid(row=Row, column=Column, pady=10, sticky="s")
            Column += 1
            if Column == 10:
                Column = 0
                Row += 2
        SeatFrame.grid(row=1, columnspan=3, sticky="news")
    else:
        Label(MainFrame, text="Movie ID {0} Seat Not found!".format(SelectedIndex.get()), font=("Helvetica 20 bold"), bg="#709fb0", fg="white").grid(row=1, columnspan=3)
    MainFrame.grid(row=0, column=0, sticky="news")

def GetSeatInTicket():
    SeatInTicket = ""
    Connection = GetConnection()
    Cursor = Connection.cursor()
    Cursor.execute("SELECT Seats FROM Tickets WHERE ID = ? AND Showtime = ?", [SelectedIndex.get(), SelectedShowtime.get()])
    Seats = Cursor.fetchall()
    if Seats:
        for Seat in Seats:
            SeatInTicket += ", ".join(Seat) + ", "
    return SeatInTicket

def OnSelectSeat(SeatID):
    Convert = int(str(SeatID).split()[0][1] + str(SeatID).split()[0][2])
    for i in range(len(SeatVariable)):
        Value = SeatVariable[i]
        if Value.get() == 1:
            if SeatID not in SelectedSeatList and Convert - 1 == i:
                SelectedSeatList.append(SeatID)
        else:
            if SeatID in SelectedSeatList and Convert - 1 == i:
                SelectedSeatList.remove(SeatID)

def OnSelectSeatDisable():
    DisableSeat.set(1)

def OnCheckout():
    if len(SelectedSeatList) < 1:
        messagebox.showwarning("Unreal Cinema V.2", "Please select seat.")
        
    else:
        if UID.get() == 0:
            messagebox.showwarning("Unreal Cinema V.2", "Please login first.")
            LoginFrame()
        else:
            Total = CalculatePayment()
            Discount = 0
            Percent = 0
            Connection = GetConnection()
            Cursor = Connection.cursor()
            Cursor.execute("SELECT * FROM MemberCards WHERE UID = ?", [UID.get()])
            Data = Cursor.fetchone()
            if Data:
                Discount = Total * 20 / 100
                Percent = Discount * 100 / Total
            Pay = Total - Discount
            MainFrame = Frame(Root, bg="#709fb0")
            MainFrame.columnconfigure((0, 1), weight=1)
            Button(MainFrame, image=IconBack, text="Back", bg="#28527a", fg="white", width=70, command=ShowSeats, compound=LEFT).grid(row=0, column=0, sticky="w", padx=10, pady=10, ipadx=10)
            Label(MainFrame, image=Posters[int(SelectedIndex.get()) - 1], bg="#709fb0").grid(row=1, columnspan=2, pady=2)
            Label(MainFrame, text="Selected Seat : ", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=2, column=0, pady=2, sticky="e")
            Label(MainFrame, text=", ".join(sorted(SelectedSeatList)), font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=2, column=1, pady=2, sticky="w")
            Label(MainFrame, text="Showtime : ", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=3, column=0, pady=2, sticky="e")
            Label(MainFrame, textvariable=SelectedShowtime, font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=3, column=1, pady=2, sticky="w")
            Label(MainFrame, text="Total : ", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=4, column=0, pady=2, sticky="e")
            Label(MainFrame, text="%.2f Baht" % (Total), font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=4, column=1, pady=2, sticky="w")
            Label(MainFrame, text="Discount : ", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=5, column=0, pady=2, sticky="e")
            Label(MainFrame, text="%.2f (-%d%%) Baht" % (Discount, Percent), font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=5, column=1, pady=2, sticky="w")
            Label(MainFrame, text="Net price to pay : ", font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=6, column=0, pady=2, sticky="e")
            Label(MainFrame, text="%.2f Baht" % (Pay), font=("Helvetica 16"), bg="#709fb0", fg="white").grid(row=6, column=1, pady=2, sticky="w")
            Button(MainFrame, image=IconConfirm, text="Confirm", bg="#28527a", fg="white", font=("Helvetica 16"), width=100, command=OnConfirm, compound=LEFT).grid(row=7, columnspan=2, pady=2, ipadx=10)
            MainFrame.grid(row=0, column=0, sticky="news")

def CalculatePayment():
    Total = 0
    for Variable in SeatVariable:
        if Variable.get() == 1:
            Total += 200
    return Total

def OnConfirm():
    if SelectedIndex.get() == "" or SelectedShowtime.get() == "" or len(SelectedSeatList) < 1:
        return
    Condition = messagebox.askyesno("Unreal Cinema V.2", "Are you sure?\nYou want to confirm?")
    if Condition:
        Connection = GetConnection()
        Cursor = Connection.cursor()
        Cursor.execute("INSERT INTO Tickets (UID, ID, Showtime, Seats) VALUES (?, ?, ?, ?)", [UID.get(), SelectedIndex.get(), SelectedShowtime.get(), ", ".join(sorted(SelectedSeatList))])
        Connection.commit()
        MainFrame = Frame(Root, bg="#709fb0")
        MainFrame.rowconfigure((0, 1), weight=1)
        MainFrame.columnconfigure((0, 1), weight=1)
        Label(MainFrame, image=IconSuccess, bg="#709fb0", text="Successfully", font=("Helvetica 16 bold"), fg="white", compound=TOP).grid(row=0, columnspan=2, sticky="s", pady=10)
        Button(MainFrame, text="Back to Main Page", font=("Helvetica 16"), bg="#28527a", fg="white", width=30, command=ShowMovies).grid(row=1, columnspan=2, sticky="n", pady=10, ipady=5)
        MainFrame.grid(row=0, column=0, sticky="news")

Root = MainWindow()
Posters = []
Tickets = []
IsShow = 1
MovieName = StringVar()
SelectedIndex = StringVar()
SelectedShowtime = StringVar()
SelectedSeatList = []
DisableSeat = IntVar()
DisableSeat.set(1)
UID = IntVar()
Username = StringVar()
Password = StringVar()
ConfirmPassword = StringVar()
OldPassword = StringVar()
NewPassword = StringVar()
ConfirmNewPassword = StringVar()
Firstname = StringVar()
Lastname = StringVar()
Title = StringVar()
IconNowShowing = PhotoImage(file="Image/NowShowing.png").subsample(20, 20)
IconComingSoon = PhotoImage(file="Image/ComingSoon.png").subsample(20, 20)
IconSignIn = PhotoImage(file="Image/SignIn.png").subsample(20, 20)
IconSignUp = PhotoImage(file="Image/SignUp.png").subsample(20, 20)
IconSignOut = PhotoImage(file="Image/SignOut.png").subsample(20, 20)
IconBack = PhotoImage(file="Image/Back.png").subsample(20, 20)
IconNext = PhotoImage(file="Image/Next.png").subsample(20, 20)
IconConfirm = PhotoImage(file="Image/Confirm.png").subsample(20, 20)
IconProfile = PhotoImage(file="Image/Profile.png").subsample(20, 20)
IconTicket = PhotoImage(file="Image/Ticket.png").subsample(20, 20)
IconSeatEnable = PhotoImage(file="Image/SeatEnable.png")
IconSeatDisable = PhotoImage(file="Image/SeatDisable.png")
IconSuccess = PhotoImage(file="Image/Success.png")
IconLogin = PhotoImage(file="Image/Login.png").subsample(7, 7)
IconUser = PhotoImage(file="Image/User.png").subsample(7, 7)
IconPassword = PhotoImage(file="Image/Password.png").subsample(8, 8)
IconSave = PhotoImage(file="Image/Save.png").subsample(20, 20)
IconBuy = PhotoImage(file="Image/Buy.png").subsample(20, 20)
IconCancel = PhotoImage(file="Image/Cancel.png").subsample(20, 20)
IconChange = PhotoImage(file="Image/Change.png").subsample(20, 20)
IconCard = PhotoImage(file="Image/MemberCard.png").subsample(3, 3)
IconNoCard = PhotoImage(file="Image/MemberNoCard.png").subsample(3, 3)
IconMagnifiying = PhotoImage(file="Image/MagnifyingGlass.png").subsample(15, 15)
LoadPoster()
CreateMenu()
ShowMovies()
Root.mainloop()