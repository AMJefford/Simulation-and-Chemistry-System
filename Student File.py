from tkinter import *
import tkinter.messagebox as tm
import sqlite3
import array
import string
import DatabaseKey
from cryptography.fernet import Fernet
from Simulation import *
import random
import time

class Login:
    def __init__(self, root):
        
        self.__UsernameE = Entry(root)
        self.__PasswordE = Entry(root,show = "*")
        self.CreateDisplay()
        
    def CreateDisplay(self):
        
        UsernameL = Label(root,text = "Username").grid(row = 0, padx = 5)
        PasswordL = Label(root,text = "Password").grid(row = 1, padx = 5)
        
        self.__UsernameE.grid(row = 0, column = 1)
        self.__PasswordE.grid(row = 1, column = 1)

        root.minsize(width = 250,height = 80)
        Button(text = "Login", command = self.ButtonClicked).grid(column = 2, pady = 5)
        
    def ButtonClicked(self):
            Username = self.__UsernameE.get()
            Password = self.__PasswordE.get()
            Database.CheckCreds(Username,Password)

class Main(object):
    def __init__(self, StudentSetClass, StudentFN, Username):
        self.__StudentSN = Username[1:]
        self.__Class = StudentSetClass
        self.__StudentFN = StudentFN
        print(self.__StudentFN)
        
        Main.MainWindow(self)

        
    def MainWindow(self):
        Window = Toplevel(root)

        OnlineHomework = Label(Window,  text = "Online Homework", font = ("Georgia", 20),bg = "#E59866", fg = "white").grid(sticky = N+S+E+W)
        
        Description = Label(Window, bg = "white", text = '''Hello! Welcome to the self marking homework system! This program will allow your
                            homework to be automatically marked upon completion. \nMeaning you wont have to wait for a result or feedback!''').grid(padx = 20, pady = 5)
        
        Window["bg"] = "white"
        Window.title("Home")
        Window.resizable(height = False, width = False)

        GoToHomework = Button(Window, text = "Check To-Do Homework", command = lambda: ToCompleteClass(self.__Class, self.__StudentSN, self.__StudentFN))
        GoToHomework.grid(padx = 300, pady = 5, sticky = N+E+S+W)

        PreviousHomework = Button(Window, text = "Check Previous Homework", command = lambda: PreviousHomeworkClass(self.__Class, self.__StudentSN, self.__StudentFN))
        PreviousHomework.grid(padx = 300, pady = 5, sticky = N+E+S+W)

        SimulationButton = Button(Window, text = "Go To Simulation", command = lambda: Simulation.RunSimulation())
        SimulationButton.grid(padx = 300, pady = 5, sticky = N+E+S+W)
   
        menuBar = Menu(Window)
        Window.winfo_toplevel()['menu'] = menuBar
        file = Menu(menuBar)
        file.add_command(label = 'Log Out', command = Window.destroy)
        file.add_command(label = 'Help', command = Main.Help)
        menuBar.add_cascade(label = "File", menu = file)


    def Help():
        Window = Toplevel(root)
        Info = Text(Window, height = 30, width = 100)
        Info.pack()
        Info.insert(END,'''HELP:
This program is intended for acedemic purposes. In the main menu you will find three options: 
Check To-Do Homework
Check Previous Homework
Go To Simulation

Check To-Do Homework:
    Here you will be presented with any live homework set by your teachers that you have yet to 
complete. Upon selection, you will be presented with a series of questions that have been set for 
you where you can either type of select your answer. Once the series of questions have been 
completed, you will be presented with a new page displaying your score, and the questions you got 
correct/incorrect, along with the correct answer. Your scores and answers will then be available to 
view by your teachers.

Check Previous Homework:
    Selecting this option will allow you to view any homework that you have completed before. A list of your previous homework will be shown where you can then select an option to view the questions
and answers to the homework, along with your score.

Go To Simulation:
    The simulation is a classic PV=nRT simulation whereby you can alter the conditions to view the 
effects. You have three conditions to change: temperature, volume, and number of moles. To gradually
change a condition, click either the green (increase) or red (decrease) button. To view the effect 
more quickly, hold down the chosen button. 

If there is any further help required, please email:
	help@system.co.uk ''')  

class ToCompleteClass(object):
    def __init__(self, StudentSetClass, StudentSN, StudentFN):
        self.__Class = StudentSetClass
        self.__StudentFN = StudentFN
        self.__StudentSN = StudentSN
        self.__ListofButtons = []
        self.__HomeworkData = []
        self.SelectHomework()
        
    def SelectHomework(self):
        Window = Toplevel(root)
        Window.title("Select a homework to complete.")
        ListOfHomeworks = []
        try:
            HomeworkFile = open("Live Homework.txt","r")
        except FileNotFoundError:
            tm.showinfo("File Error.", "Can Not Find File.")
            Window.withdraw()
            return
            
        for line in HomeworkFile:
            line = (line.strip("\n")).split(",")
            self.__HomeworkData.append(line)
        HomeworkFile.close()

        Info1 = Label(Window, text = "You have no homework to complete!")
        Info = Label(Window, text = "Select one of the following homework to complete:")
        
        if len(self.__HomeworkData) == 0:
            Info1.grid()
            
        else:
            
            Info.grid()
            def DetermineSelection(button):
                ButtonText = button['text']
                CompletedList = []
                QuestionData = []
                Text = ButtonText.split("-")
                self.__HomeworkSelection = Text[0].strip(" ")
                
                Window.destroy()
                print(self.__HomeworkSelection)
                self.LiveHomework(0, 0, CompletedList, QuestionData)

            def PrintOptions():
                try:
                    CompletedHomework = open("Completed Homework.txt", "r")

                except FileNotFoundError:
                    tm.showinfo("File Error.", "Completed Homework File Not Found.")
                    Window.withdraw()
                    return
                    
                CompletedHomework = CompletedHomework.readlines()
                
                StudentsCompletedHomework = []
                for X in range(len(CompletedHomework)):
                        StudentsCompleted = str(CompletedHomework[X]).split(",")
                        StudentCompletedHWID = str(StudentsCompleted[1]).strip("\n")
                        if StudentsCompleted[0] == (self.__StudentFN + " " + self.__StudentSN):
                            StudentsCompletedHomework.append(StudentCompletedHWID)
                for Y in range(len(self.__HomeworkData)):
                    if self.__HomeworkData[Y][8] == self.__Class and self.__HomeworkData[Y][9] not in ListOfHomeworks and self.__HomeworkData[Y][9] not in StudentsCompletedHomework:
                                                
                                                        HomeworkInfo = str(self.__HomeworkData[Y][9]) + " - " + str(self.__HomeworkData[Y][2]) + " -" + str(self.__HomeworkData[Y][3])
                                                        Button1 = Button(Window, text = HomeworkInfo)
                                                        Button1.configure(command = lambda button = Button1:  DetermineSelection(button))
                                                        Button1.grid(sticky = N+E+W+S)
                                                        self.__ListofButtons.append(Button1)
                                                        ListOfHomeworks.append(self.__HomeworkData[Y][9])
                if not ListOfHomeworks:
                     Info1.grid()
                     Info.destroy()

            PrintOptions()
                  

    
    def LiveHomework(self, Y, Score, CompletedList, QuestionData):
        
        self.__HomeworkData = []
        try:
            HomeworkFile = open("Live Homework.txt","r")

        except FileNotFoundError:
            tm.showinfo("File Error.","Live Homework File Not Found.")
            return
            
        for line in HomeworkFile:
            line = (line.strip("\n")).split(",")
            self.__HomeworkData.append(line)
        HomeworkFile.close()
        
        if Y+1 <= len(self.__HomeworkData):
            
                        QuestionText = self.__HomeworkData[Y][0]
                        self.__MCAnswers = []
                        if self.__HomeworkData[Y][4] == "MC":
                                self.__MCAnswers.append(self.__HomeworkData[Y][5])
                                self.__MCAnswers.append(self.__HomeworkData[Y][6])
                                self.__MCAnswers.append(self.__HomeworkData[Y][7])
                                self.__MCAnswers.append(self.__HomeworkData[Y][1])
                                self.__CorrectAnswer = self.__HomeworkData[Y][1]
                        random.shuffle(self.__MCAnswers)
        else:
            self.WriteScoretoFile(Score, CompletedList, QuestionData, Y)
            return
            
        if self.__HomeworkData[Y][8] == self.__Class and self.__HomeworkData[Y][9] == self.__HomeworkSelection:
                
                            
                self.__Unit = self.__HomeworkData[Y][2]
                self.__Topic = self.__HomeworkData[Y][3]
                print(self.__Topic)
                print(self.__Unit)
                NewWindow = Toplevel(root)
                NewWindow.title("Homework.")
                NewWindow.geometry("+200+200")
                NewWindow["bg"] = "#ffffff"
                NewWindow.resizable(width = False, height = False)
                QuestionData.append(self.__HomeworkData[Y])
                NewWindow.title("Get Homework")
                var = StringVar()
                var.set("Label")
                label = Label(NewWindow, text = QuestionText, bg = "#ffffff").grid(columnspan = 2, pady = 5, row = 0, column = 0, sticky = N+E+S+W)
                self.v = IntVar()
                self.v.set(0)
                if self.__MCAnswers:
                    
                    for val in range(len(self.__MCAnswers)):
                        UserChoiceMC = Radiobutton(NewWindow,
                      indicatoron = False,
                      text = self.__MCAnswers[val],
                      tristatevalue = "x",
                      padx = 20,
                      variable = self.v, value = val).grid(sticky = N+E+S+W, columnspan = 2)

                else:
                    self.AnswerBox = Entry(NewWindow)
                    self.AnswerBox.grid(columnspan = 2, sticky = N+E+S+W)
            
                NextButton = Button(NewWindow, text = "Confirm Answer",command = lambda: self.Confirm(NewWindow, Y, Score,
                                        CompletedList, QuestionData)).grid(padx = 20, pady = 20, row = 10, column = 1, sticky = E)

        else:
            self.LiveHomework(Y+1, Score, CompletedList, QuestionData)

    def Confirm(self, NewWindow, Y, Score, CompletedList, QuestionData):
        Correct = False
        KeyAnswer = ""
        KeyWords = []
        print(self.__HomeworkData[Y][4])
        if self.__HomeworkData[Y][4] == 'MC':

            UserAnswer = self.v.get()
            UserAns = (self.__MCAnswers[UserAnswer])
            CompletedUsersAnswer = UserAns
            if UserAns == self.__CorrectAnswer:
                Score += 1
                Correct = True
                
        elif self.__HomeworkData[Y][4] == 'Not MC':
            UserAnswer = self.AnswerBox.get()
            WordsIn = 0
            if "/" in self.__HomeworkData[Y][1]:
                KeyWords = ((self.__HomeworkData[Y][1]).lower()).split("/")
                
            elif " " in self.__HomeworkData[Y][1]:
                KeyWords = ((self.__HomeworkData[Y][1]).lower()).split(" ")

            else:
                KeyAnswer = (self.__HomeworkData[Y][1]).lower()
                
            UserAnswer = UserAnswer.split(" ")
            
            CompletedUsersAnswer = self.AnswerBox.get()
            
            for x in range(len(UserAnswer)):
                if UserAnswer[x].lower() in KeyWords:
                    WordsIn += 1
            if WordsIn >= 3 or UserAnswer[x] == KeyAnswer:
                Score += 1
                Correct = True
                
        Answer = [CompletedUsersAnswer, str(Correct) ,self.__HomeworkData[Y][4] , self.__HomeworkData[Y][0], self.__HomeworkData[Y][1]]
        CompletedList.append(Answer)
        NewWindow.destroy()
        self.LiveHomework(Y+1, Score, CompletedList, QuestionData)

        
    def WriteScoretoFile(self, Score, CompletedList, QuestionData, Y):
        try:
            StudentScoreFile = open("Student Scores File.txt", "a")
            
        except FileNotFoundError:
            tm.showinfo("File Error.", "Can Not Save Score.")
            return
        
        StudentScoreFile.write(self.__StudentFN + " " + self.__StudentSN + "," + str(Score) +"," + self.__Class + "," + self.__HomeworkSelection + "\n")
        StudentScoreFile.close()
        
        try:
            CompletedHomework = open("Completed Homework.txt","a")
            
        except FileNotFoundError:
            tm.showinfo("File Error.","Can Not Save Progress.")
            return
            
        CompletedHomework.write(self.__StudentFN + " " + self.__StudentSN + "," + self.__HomeworkSelection + "\n")
        CompletedHomework.close()
        
        try:
            PreviousHomework = open("Previous Homework.txt", "a")

        except FileNotFoundError:
            tm.showinfo("File Error.","Previous Homework File Not Found.")
            return
            
        CrucialInfo = "," + self.__StudentFN + " " + self.__StudentSN + "," + self.__HomeworkSelection + "," + str(Score) + "," + self.__Unit + "," + self.__Topic
        
        for X in range(len(CompletedList)):
            NoExcess = str.maketrans("", "", "[]''")
            print(CompletedList[X])
            Pure = ((str(CompletedList[X])).translate(NoExcess))
            PreviousHomework.write(Pure)
            PreviousHomework.write(CrucialInfo)
            PreviousHomework.write("\n")
        PreviousHomework.close()
        self.CompletedScreen(CompletedList, QuestionData, Score)

    def CompletedScreen(self, CompletedList, QuestionData, Score):
        Window = Toplevel(root)
        Window.geometry("600x600")#mass e, prot mg, lig, similar?
        Window.title("Results.")#ligand complex

        def Data(CompletedList, QuestionData, Score):
        
            Congratulations = str("Your score: ") + str(Score)
            Label(frame, text = Congratulations).grid()
            
            for x in range(len(CompletedList)):
                Label(frame, text = (CompletedList[x][3]).capitalize()).grid()
        
                if CompletedList[x][1] == 'True':
                    Label(frame, text = "Your answer was correct: ").grid()
                    Label(frame, text = CompletedList[x][0]).grid()

                else:

                    Label(frame, text = "Your answer was: ").grid()
                    Label(frame, text = CompletedList[x][0]).grid()
                    
                    if CompletedList[x][2] == "MC":
                        Label(frame, text = "Correct answer: ").grid()
                        Label(frame, text = CompletedList[x][4]).grid()
                        
                    else:
                        Label(frame, text = "Your answer must include at least 3 of the below key words: ").grid()
                        Label(frame, text = CompletedList[x][4]).grid()
  
                Label(frame, text = "\n").grid()   


        def ChangeScroll(event):
                    self.Canvas.configure(scrollregion = self.Canvas.bbox("all"), width = 550, height = 550)


        MyFrame=Frame(Window, relief = GROOVE, width = 550, height = 550, bd = 1)
        MyFrame.place(x = 10,y = 10)

        self.Canvas = Canvas(MyFrame)
        frame = Frame(self.Canvas)
        myscrollbar = Scrollbar(MyFrame, orient = "vertical",command = self.Canvas.yview)
        self.Canvas.configure(yscrollcommand = myscrollbar.set)

        myscrollbar.pack(side = "right",fill = "y")
        self.Canvas.pack(side = "left")
        self.Canvas.create_window((200,200), window = frame, anchor = 'nw')
        frame.bind("<Configure>",ChangeScroll)
        Data(CompletedList, QuestionData, Score)
               
class PreviousHomeworkClass(object):
    def __init__(self, Class, StudentSurname, StudentFN):
        self.__Class = Class
        self.__StudentSN = StudentSurname
        self.__StudentFN = StudentFN
        self.PresentData()

    def PresentData(self):
        try:
            PreviousHwResults = open("Previous Homework.txt", "r")
        except FileNotFoundError:
            tm.showinfo("File Error","Previous Homework File Not Found.")
            return
        
        PreviousHwResults = PreviousHwResults.readlines()
        if not PreviousHwResults:
            tm.showinfo("None.", "There are no completed homeworks.")
            return
            
        Window = Toplevel(root)
        
        Window.geometry("650x270")
        Window.title("Previous Homework.")

        def ChangeScroll(event):
                    self.Canvas.configure(scrollregion = self.Canvas.bbox("all"))


        MyFrame = Frame(Window, relief = GROOVE, bd = 1)
        MyFrame.place(x = 10,y = 10)

        self.Canvas = Canvas(MyFrame)
        self.__Frame = Frame(self.Canvas)
        myscrollbar = Scrollbar(MyFrame, orient = "vertical", command = self.Canvas.yview)
        hscrollbar = Scrollbar(MyFrame, orient = "horizontal", command = self.Canvas.xview)
                        
        self.Canvas.configure(yscrollcommand = myscrollbar.set)
        self.Canvas.configure(xscrollcommand = hscrollbar.set)

        hscrollbar.pack(fill = "x")
        myscrollbar.pack(side = "right",fill = "y")
        self.Canvas.pack(side = "left")
        IDS = []
        self.__StudentData = []
        
        if len(PreviousHwResults) == 0:
            Label(self.__Frame, text = "There are no completed homeworks yet!").grid()
        
        else:
            def ViewPreAnswers(button):
                def ChangeScroll2(event):
                    self.Canvas2.configure(scrollregion = self.Canvas2.bbox("all"))

                Window = Toplevel(root)
                Window.title("Previous Homework.")
                Window.geometry("530x230")
                MyFrame2 = Frame(Window,relief = GROOVE,bd = 1)
                MyFrame2.place(x = 10,y = 10)

                self.Canvas2 = Canvas(MyFrame2, width = 500, height = 200)
                self.__Frame = Frame(self.Canvas2)
                myscrollbar = Scrollbar(MyFrame2,orient = "vertical",command = self.Canvas2.yview)
                hscrollbar = Scrollbar(MyFrame2, orient = "horizontal", command = self.Canvas2.xview)

                self.Canvas2.configure(xscrollcommand = hscrollbar.set)
                self.Canvas2.configure(yscrollcommand = myscrollbar.set)

                hscrollbar.pack(fill = "x")
                myscrollbar.pack(side = "right",fill = "y")
                self.Canvas2.pack(side = "left")
                self.Canvas2.create_window((0,0),window = self.__Frame,anchor = 'nw')

                ButtonText = button['text']
                Text = ButtonText.split(":")
                HomeworkID = Text[1]
                Label(self.__Frame, text = "Question").grid(row = 0, sticky = W, padx = 5, pady = 5)
                Label(self.__Frame, text = "Answer/Key Words").grid(row = 0, column = 1, sticky = W, padx = 5, pady = 5)
                Label(self.__Frame, text = "Your answer").grid(row = 0, column = 2, sticky = W, padx = 5, pady = 5)
                
                for x in range(len(self.__StudentData)):
                    if self.__StudentData[x][6] == HomeworkID:#0 = user ans, 1 = if correct, 2 = mc, 3 = question, 4 = acc answer, 5 = name, 6 = id, 7 = score
                        Label(self.__Frame, text = self.__StudentData[x][3]).grid(row = x + 2, sticky = W, padx = 5, pady = 5)#question
                        Label(self.__Frame, text = self.__StudentData[x][4]).grid(row = x + 2, sticky = W, column = 1, padx = 5, pady = 5)#acc answer
                        Label(self.__Frame, text = self.__StudentData[x][0]).grid(row = x + 2, column = 2, sticky = W, padx = 5, pady = 5)
                        
                
                self.__Frame.bind("<Configure>", ChangeScroll2)
                        
            def PrintOptions():
                    Label(self.Canvas, text = "HomeworkID").grid(row = 0, sticky = W, padx = 5, pady = 5)
                    Label(self.Canvas, text = "Score").grid(column = 1, row = 0, sticky = W, padx = 5, pady = 5)
                    Label(self.Canvas, text = "Unit").grid(column = 2, row = 0, sticky = W, padx = 5, pady = 5)
                    Label(self.Canvas, text = "Topic").grid(column = 3, row = 0, sticky = W, padx = 5, pady = 5)

                    for line in range(len(PreviousHwResults)):
                        p = (PreviousHwResults[line])
                        l = p.split(",")
                        ID = l[6]
                        if l[5] == self.__StudentFN + " " + self.__StudentSN:
                            self.__StudentData.append(l)
                            if ID not in IDS:
                                
                                Label(self.Canvas, text = l[8]).grid(row = line + 1, sticky = W, column = 2, pady = 5)
                                IDS.append(ID)
                                Label(self.Canvas, text = l[6]).grid(row = line + 1, column = 0, sticky = W, padx = 5, pady = 5)#id
                                Label(self.Canvas, text = l[7]).grid(row = line + 1, column = 1, sticky = W, padx = 5, pady = 5)#score[8][9]
                                Label(self.Canvas, text = l[9].strip("\n")).grid(row = line + 1, column = 3, sticky = W, pady = 5, padx = 5)
                                Info = "View Answers to ID:" + str(ID)
                                ButtonID = Button(self.Canvas, text = Info)
                                ButtonID.configure(command = lambda button = ButtonID: ViewPreAnswers(button))
                                ButtonID.grid(sticky = W, column = 4, row = line + 1, padx = 5, pady = 5)
                    print(self.__StudentData)
                    print("here")
                    if not self.__StudentData:
                            Label(self.Canvas, text = "You have no completed homework yet.").grid()
                            
                                            
            PrintOptions()
            
        self.__Frame.bind("<Configure>", ChangeScroll)

class Database:          

    def CheckCreds(Username,Password):
        conn=sqlite3.connect('OnlineHomework.db', timeout = 1)
        c=conn.cursor()
        
        Cipher_Suite = Fernet(DatabaseKey.key)
        
        StudentUsername = []
        StudentPassword = []
        StudentFN = [] 
        StudentClass = []      

        c.execute("SELECT * FROM StudentLogin;")
        for column in c:
            StudentClass.append(column[4])
            StudentFN.append(column[0])


        c.execute("SELECT Username FROM StudentLogin;")
        for column in c:
            StudentUsername.append(column[0])
        
            
        c.execute("SELECT Password FROM StudentLogin;")
        for column in c:
            UncipheredText = Cipher_Suite.decrypt(column[-1])
            PlainText = (bytes(UncipheredText).decode("utf-8"))
            StudentPassword.append(PlainText)
            
        if Username in StudentUsername:
            Correct = int(StudentUsername.index(Username))
            
            StudentFN = StudentFN[(StudentUsername.index(Username))]
            
            if str(Password) == StudentPassword[Correct]:
                tm.showinfo("Login info", "Welcome " + Username)
                StudentSetClass = StudentClass[(StudentUsername.index(Username))]
                root.withdraw()
                Main(StudentSetClass, StudentFN, Username)
            else:
                tm.showerror("Login error", "Incorrect Username or Password. Please try again.")

                
                
        else:
            tm.showerror("Login error", "Incorrect Username or Password. Please try again.")
        print(StudentUsername)
        print(StudentClass)
        print(StudentFN)
        print(StudentPassword)
        conn.commit()
        conn.close()


  
root = Tk()
root.resizable(width=False,height=False)
root.wm_title("Please login.")
root.minsize(width=300,height=300)
Login(root)
root.mainloop()
