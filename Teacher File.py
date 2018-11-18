from tkinter import *
import tkinter as tk
import tkinter.messagebox as tm
import sqlite3
import DatabaseKey
from cryptography.fernet import Fernet
from string import punctuation
import array
import time
import random
from Simulation import *


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
            Database.CheckCreds(Username, Password)

def MainWindow():
    
    Window = Toplevel(root)
    Title = Label(Window,  text = "Homework Manager", font = ("Georgia", 20), bg = "#E59866", fg = "white").grid(sticky = N+S+E+W)
    
    Description = Label(Window, bg = "white", text = '''Hello! Welcome to the self marking homework system!
This program will allow you\nto see homework for your classes with automatic feedback!''').grid(padx = 20, pady = 5)
    
    Window["bg"] = "white"
    Window.title("Home")

    Window.resizable(height = False, width = False)

    SetHomework = Button(Window, text = "Set Homework", command = lambda: SetHomeworkClass())
    SetHomework.grid(pady = 5, sticky = N+E+S+W, padx = 100)

    AddQuestion = Button(Window, text = "Add Question", command = lambda: AddQuestionClass()) 
    AddQuestion.grid(pady = 5, sticky = N+E+S+W, padx = 100)

    SimulationButton = Button(Window, text = "Go To Simulation", command = lambda: Simulation.RunSimulation()) 
    SimulationButton.grid(pady = 5, sticky = N+E+S+W, padx = 100)

    FindQuestionButton = Button(Window, text = "Lookup Question", command = lambda: FindQuestionClass())
    FindQuestionButton.grid(pady = 5, sticky = N+E+S+W, padx = 100)

    StudentScores = Button(Window, text = "View Students Scores", command = lambda: StudentScoresClass.ProduceFrame())
    StudentScores.grid(pady = 5, sticky = N+E+S+W, padx = 100)

    menuBar = Menu(Window)
    Window.winfo_toplevel()['menu'] = menuBar
    file = Menu(menuBar)
    file.add_command(label = 'Log Out', command = lambda: Window.destroy())
    file.add_command(label = 'Help', command = lambda: Help())
    menuBar.add_cascade(label = "File", menu = file)


    
def Help():
        Window = Toplevel(root)
        Window.title("Help")
        Info = Text(Window, height = 30, width = 100)
        Info.pack()
        Info.insert(END, '''HELP:
This program is intended for acedemic purposes. In the main menu you will find five options: 
Set Homework
Add Question
Go To Simulation
Lookup Question
View Students Scores

Set Homework:
	By selecting this option you will be presented with three drop down menus to select the 
class, unit, and topic of homework. You will then be shown a list of corresponding questions to 
choose from. Tick a box to select and set as part of the homework. Tick the 'select all' box to set all questions displayed. Click the confirm button to make homework available for the class.

Add Question:
	Complete all boxes shown on page. If any are left blank you will be asked to fill fully 
complete the form. Before adding your questions, click the 'Find Similar' button. You will be 
preseneted with a list of similar, currently available questions. You can then decide whether or notto still add the question by clicked 'Add question'.

Go To Simulation:
	This will take you to the PV = nRT simulation where you can control the conditions of the 
reaction. To increase a condition, select/hold the green button to the right of the condition. To 
decrease the condition, select/hold the red button to the right of the condition. Clicking a button shows a more gradual change while holding a button will increase the rate at which the condition is applied. 

Lookup Question:
	This allows you to seach through all currently available questions. You will be prompted to select an option to filter by. There are three options: multiple choice, unit and topic, and all. 

View Students Scores:
	You will be shown all students and their completed homework ID along with their score. To 
view more details about their homework, select the 'View more details' button. This will take you to a page that will show each question, the correct answer, and the students answer. 

If there is any further help required, please email:
	help@system.co.uk 
 ''') 

class StudentScoresClass:
    def ProduceFrame():
        Window = Toplevel(root)
        Window.title("Student Scores")
        Window.geometry("580x240")

        def DetermineSelection(Button):
            ButtonText = Button['text']
            Text = ButtonText.split(":")
            Identifier = Text[1]
            Identifier = Identifier.split("/")
            HomeworkID = Identifier[1]
            Name = Identifier[0].strip(" ")
            Window = Toplevel(root)
            Window.geometry("625x240")
            Window.title(Identifier)
            StudentData = []
            
            try:
                    PreviousHwResults = open("Previous Homework.txt", "r")
                    
            except FileNotFoundError:
                    print("File Error.")
                    tm.showinfo("Error", "Cannot find file for previous homework")
                    Window.withdraw()
                    return

            PreviousHwResults = PreviousHwResults.readlines()
            for line in range(len(PreviousHwResults)):
                        Line = (PreviousHwResults[line])
                        DataLine = Line.split(",")
                        ID = DataLine[6]
                        if ID == HomeworkID:
                            StudentData.append(DataLine)
                            
            def ScrollRegion(event):
                canvas.configure(scrollregion = canvas.bbox("all"))
                
            myframe = Frame(Window, relief = GROOVE, bd = 1)
            myframe.place(x = 10, y = 10)

            canvas = Canvas(myframe, width = 580, height = 200)
            frame = Frame(canvas)
            vscrollbar = Scrollbar(myframe, orient = "vertical", command = canvas.yview)
            hscrollbar = Scrollbar(myframe, orient = "horizontal", command = canvas.xview)

            canvas.configure(xscrollcommand = hscrollbar.set)
            canvas.configure(yscrollcommand = vscrollbar.set)

            hscrollbar.pack(fill = "x")
            vscrollbar.pack(side = "right",fill = "y")
            canvas.pack(side = "left")
            canvas_frame = canvas.create_window((0,0),window = frame,anchor = 'nw')

            
            frame.bind("<Configure>", ScrollRegion)

            Label(frame, text = "Question", bg = "#E59866", fg = "white").grid(row = 0, sticky = N+E+S+W, pady = 5)
            Label(frame, text = "Answer/Key Words", bg = "#E59866", fg = "white").grid(row = 0, column = 1, sticky = N+E+S+W, pady = 5)
            Label(frame, text = "Students answer", bg = "#E59866", fg = "white").grid(row = 0, column = 2, sticky = N+E+S+W, pady = 5)

            for x in range(len(StudentData)):
                if StudentData[x][6] == HomeworkID and StudentData[x][5] == Name:#0 = user ans, 1 = if correct, 2 = mc, 3 = question,
                                                                                        #4 = acc answer, 5 = name, 6 = id, 7 = score
                    Label(frame, text = StudentData[x][3]).grid(row = x + 2, sticky = W, padx = 5, pady = 5)#question
                    Label(frame, text = StudentData[x][4]).grid(row = x + 2, sticky = W, column = 1, padx = 5, pady = 5)#acc answer
                    Label(frame, text = StudentData[x][0]).grid(row = x + 2, column = 2, sticky = W, padx = 5, pady = 5)
   
        def Data():
                
                NameLabel = Label(frame, text = "Student Name", bg = "#E59866", fg = "white").grid(row = 0, sticky = N+E+S+W)
                ScoreLabel = Label(frame, text = "Student Score", bg = "#E59866", fg = "white").grid(row = 0, column = 1, sticky = N+E+S+W)
                ClassLabel = Label(frame, text = "Class", bg = "#E59866", fg = "white").grid(row = 0, column = 2, sticky = N+E+S+W)
                HomeworkID = Label(frame, text = "Homework ID", bg = "#E59866", fg = "white").grid(row = 0, column = 3, sticky = N+E+S+W)
                MoreInfo = Label(frame, text = "View more details", bg = "#E59866", fg = "white").grid(row = 0, column = 4, sticky = N+E+S+W)
                IDS = []
                StudentNames = []
                def Display(StudentData):
            
                            for Y in range(len(StudentData)):
                                
                                    ButtonID = Button(frame, text = "View: " + StudentData[0] + "/" + StudentData[3])#ID
                                    print(StudentData)
                                    ButtonID.configure(command = lambda Button = ButtonID: DetermineSelection(Button))
                                    ButtonID.grid(row = 2 + X, column = 4, sticky = N+E+S+W)
                                    Label(frame, text = StudentData[Y]).grid(pady = 5, padx = 10, row = 2 + X, column = Y, sticky = W+E)

                try:
                    StudentScores = open("Student Scores File.txt" , "r")

                except FileNotFoundError:
                    tm.showinfo("File Error.","No File For Student Scores Found.")
                    Window.withdraw()
                    return
                
                StudentScores = StudentScores.readlines()
                if StudentScores:
                    for X in range(len(StudentScores)):
                        StudentData = StudentScores[X].split(",")
                        StudentData[3] = StudentData[3].strip("\n")#the ID of the student in list
                        if StudentData[3] in IDS:
                            Pos = IDS.index(StudentData[3])
                            if StudentNames[Pos] == StudentData[0]: #if the position index of the ID in studentnames is equal to the name
                                #if somehow a student managed to duplicate its data to produce two completed homework under same ID. 
                                pass
                            else:
                                IDS.append(StudentData[3])
                                StudentNames.append(StudentData[0])
                                Display(StudentData)
                        else:
                            IDS.append(StudentData[3])
                            StudentNames.append(StudentData[0])
                            Display(StudentData)
                else:
                    Label(frame, text = "There are on current available homeworks to view").grid()

        def ScrollRegion(event):
                canvas.configure(scrollregion = canvas.bbox("all"))

        myframe = Frame(Window, relief = GROOVE, bd = 1)
        myframe.place(x = 10, y = 10)

        canvas = Canvas(myframe, width = 550, height = 200)
        frame = Frame(canvas)
        vscrollbar = Scrollbar(myframe, orient = "vertical", command = canvas.yview)
        hscrollbar = Scrollbar(myframe, orient = "horizontal", command = canvas.xview)
        
        canvas.configure(yscrollcommand = vscrollbar.set)
        canvas.configure(xscrollcommand = hscrollbar.set)

        vscrollbar.pack(side = "right",fill = "y")
        hscrollbar.pack(fill = "x")
        canvas.pack(side = "left")
        canvas_frame = canvas.create_window((0,0),window = frame,anchor = 'nw')
        
        frame.bind("<Configure>", ScrollRegion)
        Data()
      
class SetHomeworkClass:
    def __init__(self):
        
        self.ClassChosen = StringVar()#sets the type of trace variable this will be in the option menu widget
        self.UnitChosen = StringVar()
        self.TopicChosen = StringVar()
        self.DisplayScreen()#self is always automatically passed as a parameter but not received 

    def DisplayScreen(self):
        
        Classes = SetHomeworkClass.OpenClasses()
        
        Window = Toplevel(root) #forces new window to be toplevel/parent in tkinter
        Window.resizable(height = False, width = False)
        Window.title("Set Homework")
        Label(Window, text = "Please complete the following:", font = ('Georgia',15), bg = '#E59866', fg = "white").grid(columnspan = 4, sticky = N+E+W+S, ipady = 10)#sets style of widget
        TopicLabel = Label(Window, text = "Select the class: ").grid(row = 8, pady = 10, sticky = W)#creates three labels
        UnitLabel = Label(Window, text = "Select the Unit: ").grid(row = 9, pady = 10, sticky = W)
        TopicLabel = Label(Window, text = "Select the Topic: ").grid(row = 10, pady = 10, sticky = W)

        conn = sqlite3.connect("OnlineHomework.db")#makes connection to sqlite3 db
        c = conn.cursor()
        conn.commit()
        conn.close()#closes the connection
        
        UnitAndTopicList, InorganicTopics, PhysicalTopics, OrganicTopics, UnitList = OpenUnitAndTopic() #retrieves all information on units and topics to display in option menu from subroutine

        ClassMenu = OptionMenu(Window, self.ClassChosen , *Classes).grid(row = 8, column = 1, sticky = W)
        UnitMenu = OptionMenu(Window, self.UnitChosen , *UnitList).grid(row = 9, column = 1, sticky = W)#displays three option menus for the user to choose from
        TopicMenu = OptionMenu(Window, self.TopicChosen , "Select Unit").grid(row = 10, column = 1, sticky = W)
        PresentQuestions = []
        SetHomeworkButton = Button(Window, text = "View and Select Questions", command = lambda: self.CheckIfValid(Window,PresentQuestions)).grid(row = 11, column = 1, sticky = W, pady = 10)
                                                                                            #passes these 4 paramters into CheckIfValid method
                                                                                        
        def Change_Dropdown(*args):
            ChosenUnit = self.UnitChosen.get()
                
            if ChosenUnit == 'Inorganic Chemistry':
                self.TopicChosen.set(InorganicTopics[0])#set the TopicChosen variable to the first topic in the corresponding unit
                OptionMenu(Window, self.TopicChosen ,*InorganicTopics).grid( row = 10, column = 1, sticky = W)
                #the first argument identifies the parent, the second is the variable name for the option, the third is the list of dropdown values to be displayed

            elif ChosenUnit == 'Organic Chemistry':
                OptionMenu(Window, self.TopicChosen ,*OrganicTopics,).grid( row = 10, column = 1, sticky = W)
                self.TopicChosen.set(OrganicTopics[0])
                
            else:
                OptionMenu(Window, self.TopicChosen ,*PhysicalTopics).grid( row = 10, column = 1, sticky = W)
                self.TopicChosen.set(PhysicalTopics[0])
                
        self.UnitChosen.trace('w', Change_Dropdown)#automatically traces the classes variable every time the value changes

    def CheckIfValid(self, Window, PresentQuestions):
        Class = self.ClassChosen.get()#gets the values of the variables from within the class
        Unit = self.UnitChosen.get()
        Topic = self.TopicChosen.get()
        self.v = IntVar()#the value of multiple choice will be set to 0 if false and 1 if true
        self.v.set(0)#therefore is an intvar not a stringvar
        
        if Class == '' or Unit == '' or Topic == '':
            tm.showinfo("Error", "Please fill in all details.")

        else:
            for x in range(len(PresentQuestions)):
                PresentQuestions[x].destroy()#removes any present questions
                
            Info = Label(Window, text = "Please select the questions you would like to set: ")
            ConfirmSelection = Button(Window, text = "Set Homework", command = lambda: self.ConfirmHomework(QuestionsList, Window), pady = 10)
            Delete = Label(Window, text = "There are no questions available.\nPlease add questions from the main menu.")
            
            QuestionData = OpenFile()
            QuestionsList = []
            
            for x in range(len(QuestionData)):
                if QuestionData[x][3] == Topic:
                    QuestionsList.append(QuestionData[x][0])

            self.intvars = []

            for y in range(len(QuestionsList)):
                self.intvars.append(IntVar(value = 1))
                Check = Checkbutton(Window, text = QuestionsList[y], variable = self.intvars[y])
                Check.grid(row = 14 + y, column = 1, sticky = W)
                PresentQuestions.append(Check)
            
            if len(QuestionsList)>0:
                SelectAllBox = Checkbutton(Window, text = "Select All Questions", variable = self.v)
                SelectAllBox.grid(row = 13, sticky = W, column = 1, pady = 15, padx = 15)
                Info.grid(sticky = W, row = 12, column = 1)
                ConfirmSelection.grid(row = 100, column = 1, sticky = W)
                PresentQuestions.append(SelectAllBox)
                PresentQuestions.append(Info)
                PresentQuestions.append(ConfirmSelection)
    
            else:
                PresentQuestions.append(Delete)
                Delete.grid(sticky = W, row = 12, column = 1)

                
    def ConfirmHomework(self, QuestionsList, Window):
        SetQuestions = []
        QuestionData = OpenFile()
        try:
            LiveHomework = open("Live Homework.txt", "a")#opens the file with the operation to append
        except FileNotFoundError:
            tm.showinfo("Error.", "No File Found.")
            Window.withdraw()
            return
        try:
            HomeworkID = sum(1 for line in open('HomeworkID.txt'))#adds the number of lines there are in the file
        except FileNotFoundError:
            tm.showinfo("Error.", "No File Found.!")
            Window.withdraw()
            return
        
        HomeworkID = (HomeworkID + 1)#increases this value by 1, therefore for each homework set, there is a different ID

        try:
            HomeworkIDFile = open("HomeworkID.txt", "a")
            
        except FileNotFoundError:
            tm.showinfo("Error.", "No File Found!!!.")
            Window.withdraw()
            return
        HomeworkIDFile.write(str(HomeworkID) + "\n")#creates a new line and writes the new ID to the file
        HomeworkIDFile.close()
        
        if self.v.get() == 0:
            for x in range(len(QuestionsList)):
                if self.intvars[x].get() == 1:# if the state is on
                    SetQuestions.append(QuestionsList[x])#QuestionsList[x]
                    
                    for i, j in enumerate(QuestionData):# i = iterate value, j = question line value
                        if j[0] == QuestionsList[x]:#j[0] is question text, if this is equal to any index in QuestionsList
                            LiveHomework.write(",".join(j)+ "," + self.ClassChosen.get() + "," + str(HomeworkID) + "\n" )#joins all values in j by commas
        else:
            for i, j in enumerate(QuestionData):
                            if j[3] == self.TopicChosen.get():
                                SetQuestions.append(j[3])
                                LiveHomework.write(",".join(j)+ "," + self.ClassChosen.get() + "," + str(HomeworkID)+ "\n")
                                
        LiveHomework.close()
        if not SetQuestions:
            tm.showinfo("Error", "Please select questions to set.")
            
        else:
            tm.showinfo("Success", "Homework has been set.")
            Window.destroy()
        
    def OpenClasses():
        ClassesList = []
        try:
            ClassesFile = open("Classes.txt", "r")
        except FileNotFoundError:
            tm.showinfo("Error.", "No Classes Found.")
            return
        ClassesFile = ClassesFile.readlines()
        for line in ClassesFile:
            ClassesList.append(line.strip("\n"))
        return ClassesList


class AddQuestionClass:

    def __init__(self):
        
        Window = Toplevel(root)
        self.QuestionText = Entry(Window)
        
        self.v = StringVar()
        self.v.set("Not MC")

        self.Unit = StringVar(root)
        self.Topic = StringVar(root)
        AddQuestionClass.PresentGUI(self, Window)

        
    def PresentGUI(self, Window):
              
        Window.resizable(height = False, width = False)
        Label(Window, text = "Complete all details below", font = ('Georgia',15), bg = "#E59866", fg = "white").grid(columnspan = 5, sticky = N+E+W+S, ipady = 10)
        Question = Label(Window, text = "Question:").grid(row = 1, sticky = W, pady = 10, padx = 10)
        ListofWidgets = []
        self.QuestionText.grid(row = 1, column = 1, sticky = E+W)#how to make entry fill x axis

        Button(Window, text = "Check For Similar Questions", command = lambda: AddQuestionClass.Check(self, ListofWidgets, Window)).grid(row = 9, sticky =E + W, pady = 5, padx = 10)
        
        def ShowChoice():
            V = self.v.get()

            if V == 'MC':
                self.CorrectMCA.configure(state = 'normal')
                self.MCAnswer2.configure(state = 'normal')
                self.MCAnswer3.configure(state = 'normal')
                self.MCAnswer4.configure(state = 'normal')
                Option1.configure(state = 'normal')
                Option2.configure(state = 'normal')
                Option3.configure(state = 'normal')
                Option4.configure(state = 'normal')
                self.AnswerText.configure(state = 'disable')
                AnswerLabel.configure(state = 'disable')            

            else:
                self.CorrectMCA.configure(state = 'disable')
                self.MCAnswer2.configure(state = 'disable')
                self.MCAnswer3.configure(state = 'disable')
                self.MCAnswer4.configure(state = 'disable')
                Option1.configure(state = 'disable')
                Option2.configure(state = 'disable')
                Option3.configure(state = 'disable')
                Option4.configure(state ='disable')
                self.AnswerText.configure(state = 'normal')
                AnswerLabel.configure(state = 'normal')
       
        MCLabel = Label(Window, text = "Multiple Choice?").grid(row = 3, sticky = W, pady = 10, padx = 10)  
        MCButton = Radiobutton(Window, text = "Yes", variable = self.v, value = "MC", command = ShowChoice).grid(row = 3, column = 1, sticky = W)
        NotMCButton = Radiobutton(Window, text = "No", variable = self.v, value = "Not MC", command =  ShowChoice).grid(row = 3, column = 2, sticky = W)
                
        Label(Window, text = 'Multiple Choice Answers').grid(row = 6, pady = 10, sticky = W, padx = 10)

        Option1 = Label(Window, text = "Enter Correct Answer: ", state = 'disable')
        Option1.grid(row = 5, column = 1, padx = 10)
        
        self.CorrectMCA = Entry(Window, state = 'disable')
        self.CorrectMCA.grid(row = 6, column = 1, sticky = E+W)
        
        Option2 = Label(Window, text = "Enter Option 2: ", state = 'disable')
        Option2.grid(row = 5, column = 2, padx = 10)
        self.MCAnswer2 = Entry(Window, state = 'disable')
        self.MCAnswer2.grid(row = 6, column = 2, sticky = E+W)
        
        Option3 = Label(Window, text = "Enter Option 3: ", state = 'disable')
        Option3.grid(row = 5, column = 3, padx = 10)
        self.MCAnswer3 = Entry(Window, state = 'disable')
        self.MCAnswer3.grid(row = 6, column = 3, sticky = E+W)

        Option4 = Label(Window, text = "Enter Option 4: ", state = 'disable')
        Option4.grid(row = 5, column = 4, padx = 10)
        self.MCAnswer4 = Entry(Window, state = 'disable')
        self.MCAnswer4.grid(row = 6, column = 4, sticky = E+W)

        AnswerLabel = Label(Window, text = "Enter Key Words Students\nMust Include in Their Answers\n(Separate with '/') : ")
        AnswerLabel.grid(row = 4, sticky = W, pady = 10, padx = 10)
        self.AnswerText = Entry(Window)
        self.AnswerText.grid(row = 4, column = 1, sticky = E+W)

        TopicLabel = Label(Window, text = "Enter the Topic: ").grid(row = 8, pady = 10, sticky = W, padx = 10)
        UnitLabel = Label(Window, text = "Enter the Unit: ").grid(row = 7, pady = 10, sticky = W, padx = 10)
        
        UnitAndTopic, InorganicTopics, PhysicalTopics, OrganicTopics, UnitList = OpenUnitAndTopic()
        
        OptionMenu(Window, self.Unit, *UnitList).grid(row = 7, column = 1, sticky = E+ W)
        OptionMenu(Window, self.Topic, "Select A Unit").grid(row = 8, column = 1, sticky = E+ W)
 
    
        def ChangeDropdown(*args):
            ChosenUnit = self.Unit.get()
                
            if ChosenUnit == 'Inorganic Chemistry':
                OptionMenu(Window, self.Topic ,*InorganicTopics).grid(row = 8, column = 1, sticky = E + W)
                self.Topic.set(InorganicTopics[0])
                
            elif ChosenUnit == 'Organic Chemistry':
                OptionMenu(Window, self.Topic ,*OrganicTopics,).grid( row = 8, column = 1, sticky = E + W)
                self.Topic.set(OrganicTopics[0])
                
            else:
                OptionMenu(Window, self.Topic ,*PhysicalTopics).grid(row = 8, column = 1, sticky = E + W)
                self.Topic.set(PhysicalTopics[0])
                
        self.Unit.trace('w', ChangeDropdown)


    def Check(self, ListofWidgets, Window):
        ChosenTopic = self.Topic.get()
        ChosenUnit = self.Unit.get()
        AnswerText = self.AnswerText.get()
        QuestionText = self.QuestionText.get()
        CorrectMCA = self.CorrectMCA.get()
        MCAnswer2 = self.MCAnswer2.get()
        MCAnswer3 = self.MCAnswer3.get()
        MCAnswer4 = self.MCAnswer4.get()
        MC = self.v.get()

        if QuestionText != '' and AnswerText != '':
                AddQuestionClass.SaveNewQuestion(self, ListofWidgets, Window, ChosenTopic, ChosenUnit, QuestionText, AnswerText, MC, CorrectMCA, MCAnswer2, MCAnswer3, MCAnswer4)

        elif QuestionText != '' and CorrectMCA != '' and MCAnswer2 != '' and MCAnswer3 != '' and MCAnswer4 != '':
                AddQuestionClass.SaveNewQuestion(self, ListofWidgets, Window, ChosenTopic, ChosenUnit, QuestionText, AnswerText, MC, CorrectMCA, MCAnswer2, MCAnswer3, MCAnswer4)
        else:
                tm.showinfo("Error", "Please fill in all boxes")



    def SaveNewQuestion(self, ListofWidgets, Window, ChosenTopic, ChosenUnit, QuestionText, AnswerText, MC, CorrectMCA, MCAnswer2, MCAnswer3, MCAnswer4):
        try:
            QuestionFile = open("Get Questions.txt", "r")
        except FileNotFoundError:
            tm.showinfo("Error.", "File For Questions Not Found.")
            Window.withdraw()
            return
        QuestionText = QuestionText.lower()
        Similar = False
        AlreadyPresent = []
        for x in range(len(ListofWidgets)):
            ListofWidgets[x].grid_remove()

        QuestionText = (str(QuestionText).strip(punctuation)).split(" ")
        for line in QuestionFile:

            line = line.lower()
            line = line.split(",")
            line = (line[0])
            line = (line.strip("?")).split(" ")
            NumberOfWordsIn = 0
            for x in range(len(QuestionText)):
                if QuestionText[x] in line: #if input word is in the file text
                    NumberOfWordsIn += 1
            if NumberOfWordsIn >=3:
                if line not in AlreadyPresent:
                    Text = Label(Window, text = "These are some similar questions\n already available:")
                    Text.grid(row = 11)
                    SimilarQ = "•" + ((" ".join(line)).capitalize())
                    Widget = Label(Window, text = SimilarQ)
                    Widget.grid(row = 11 + len(AlreadyPresent), column = 1, sticky = W, padx = 10)
                    AlreadyPresent.append(line)
                    ListofWidgets.append(Widget)
                    ListofWidgets.append(Text)
                    Similar = True
               
                            
        if Similar == False:
            NoQuestions = Label(Window, text = "There are no similar questions currently available.")
            NoQuestions.grid(row = 11)
            ListofWidgets.append(NoQuestions)
            
        Button(Window, text = "Add Question", command = lambda: AddQuestionClass.WriteToTextfile(self, Window, ChosenTopic, ChosenUnit, QuestionText, AnswerText, MC, CorrectMCA, MCAnswer2, MCAnswer3, MCAnswer4)).grid(sticky = N+E+S+W, row = 10, padx = 10)

        QuestionFile.close()
            
    def WriteToTextfile(self, Window, ChosenTopic, ChosenUnit, QuestionText, AnswerText, MC, CorrectMCA, MCAnswer2, MCAnswer3, MCAnswer4):
        try:
            QuestionFile = open("Get Questions.txt", "a")
        except FileNotFoundError:
            tm.showinfo("Error.", "No File For Questions Found.")
            Window.withdraw()
            return
        QuestionText = self.QuestionText.get()
        if "?" not in QuestionText:
            QuestionText = QuestionText + "?"
        if MC == 'MC':
            QuestionFile.write((self.QuestionText.get()).capitalize() + "," + CorrectMCA.capitalize() + "," + ChosenUnit + ","
                               + ChosenTopic +  "," + MC + "," + MCAnswer2.capitalize() + "," + MCAnswer3.capitalize() + "," + MCAnswer4.capitalize() + "\n")
        else:           
            QuestionFile.write((self.QuestionText.get()).capitalize() + "," +  AnswerText.capitalize() + "," + ChosenUnit + "," + ChosenTopic + "," + MC + ",x,x,x" + "\n")
        tm.showinfo("Success", "Question added.")
        QuestionFile.close()
        Window.destroy()
        
def OpenUnitAndTopic():
        try:
            UnitAndTopic = open("Unit and Topic.txt","r")
        except FileNotFoundError:
            tm.showinfo("Error.", "No File For Unit and Topics Found.")
            return
        UnitAndTopicList = []
        for line in UnitAndTopic:
            line = (line.strip("\n")).split(",")
            UnitAndTopicList.append(line)
            
        UnitAndTopic.close()

                
        InorganicTopics = []
        PhysicalTopics = []
        OrganicTopics = []
        UnitList = []

        
        for x in range(len(UnitAndTopicList)):
            UnitList.append(UnitAndTopicList[x][0])
        for y in range(len(UnitAndTopicList)-1):
            InorganicTopics.append(UnitAndTopicList[1][y+1])
            PhysicalTopics.append(UnitAndTopicList[0][y+1])
            OrganicTopics.append(UnitAndTopicList[2][y+1])

        return UnitAndTopicList, InorganicTopics, PhysicalTopics, OrganicTopics, UnitList



def OpenFile():
        QuestionData = []
        try:
            QuestionFile = open("Get Questions.txt","r")
        except FileNotFoundError:
            tm.showinfo("File Error.", "No File For Questions Found")
            return
        for line in QuestionFile:
            line = (line.strip("\n")).split(",")
            QuestionData.append(line)
        QuestionFile.close()
        return QuestionData

class FindQuestionClass:
    def __init__(self):
        self.ListOfWidgets = []
        self.ListOfDropdown = []
        self.Display()
        

    def Display(self):
        QuestionData = OpenFile()
        self.Window = Toplevel(root)
        self.Window.wm_geometry("950x250")
        self.Window.title("Find Questions.")
        
        def Data():
             
            tkvar = StringVar(root)
            Choices = {'All', 'Unit and Topic' ,'Multiple Choice'}
            tkvar.set('Filter By')

            Label(self.frame, text = "Search for a question by filtering:", fg = "white", bg =
                  "#E59866").grid(sticky = N+E+S+W, columnspan = 100)
            popupMenu = OptionMenu(self.frame, tkvar, *Choices).grid(row = 1, sticky = N+E+S+W, columnspan = 2)

            self.SetTitles()
            
            def ChangeDropdown(self, *args):
                ChosenOption = tkvar.get()
                CheckChosen(ChosenOption)
                
            def CheckChosen(ChosenOption):
                if ChosenOption == 'Topic':
                    self.FilterByTopic(QuestionData)

                elif ChosenOption == "All":
                    self.All(QuestionData)

                elif ChosenOption == 'Unit and Topic':
                    self.FilterByUnit(QuestionData)

                else:
                    self.FilterByMC(QuestionData)
            
            tkvar.trace('w',ChangeDropdown)
            
        def ScrollRegion(event):
            
            self.canvas.configure(scrollregion = self.canvas.bbox("all"))

        self.myframe = Frame(self.Window, relief = GROOVE, bd = 1)
        self.myframe.place(x = 10,y = 10)

        self.canvas = Canvas(self.myframe, width = 900, height = 200)
        self.frame = Frame(self.canvas)
        vscrollbar = Scrollbar(self.myframe, orient = "vertical", command = self.canvas.yview)
        hscrollbar = Scrollbar(self.myframe, orient = "horizontal", command = self.canvas.xview)
        
        self.canvas.configure(yscrollcommand = vscrollbar.set)
        self.canvas.configure(xscrollcommand = hscrollbar.set)

        vscrollbar.pack(side = "right",fill = "y")
        hscrollbar.pack(fill = "x")
        self.canvas.pack(side = "left")
        self.canvas_frame = self.canvas.create_window((0,0),window = self.frame,anchor = 'nw')
        
        self.frame.bind("<Configure>", ScrollRegion)
        Data()

    def FilterByMC(self, QuestionData):
        
        for x in range(len(self.ListOfDropdown)):
            self.ListOfDropdown[x].destroy()
        
        for x in range(len(self.ListOfWidgets)):
            self.ListOfWidgets[x].destroy()
            
        MultipleChoiceQuestionData = []
        for x in range(len(QuestionData)):
            
            print(QuestionData[x][4])
            if QuestionData[x][4] == 'MC':
                MultipleChoiceQuestionData.append(QuestionData[x])
               
        for x in range(len(MultipleChoiceQuestionData)):
            for y in range(len(QuestionData[x])):
                widget = Label(self.frame, text = MultipleChoiceQuestionData[x][y])
                widget.grid(column = y, row = x + 4, padx = 10, sticky = W)
                self.ListOfWidgets.append(widget)                
                
    def FilterByUnit(self, QuestionData):
        
        for x in range(len(self.ListOfWidgets)):
            self.ListOfWidgets[x].destroy()
            
        self.Window.wm_geometry("950x250")
        self.canvas.config(width = 900, height = 200) 
        for x in range(len(self.ListOfWidgets)):
            self.ListOfWidgets[x].destroy()

        UnitAndTopicList, InorganicTopics, PhysicalTopics, OrganicTopics, UnitList = OpenUnitAndTopic()
        InorganicTopics.append("Sort only by Unit")
        PhysicalTopics.append("Sort only by Unit")
        OrganicTopics.append("Sort only by Unit")
        self.ChosenUnit = StringVar()
        self.ChosenUnit.set("Choose Unit")
        self.ChosenTopic = StringVar()
        self.ChosenTopic.set("Choose Topic")
        def ChangeDropdown(*args):
            
            self.canvas.config(width = 1200, height = 200)
            self.Window.wm_geometry("1250x250")
            ChosenUnit = self.ChosenUnit.get()
            self.GetResults(QuestionData, "Sort only by Unit", ChosenUnit)
    
            def changedropdown(*args):
                ChosenTopic = self.ChosenTopic.get()
                ChosenUnit = self.ChosenUnit.get()
                FindQuestionClass.GetResults(self, QuestionData, ChosenTopic, ChosenUnit)
                    
            
            if ChosenUnit == UnitList[0]:#PHYS
                    self.OptionMenu = OptionMenu(self.frame, self.ChosenTopic, *PhysicalTopics)
                    self.OptionMenu.grid(column = 4, row = 1, columnspan = 2, sticky = N+E+S+W)
                    self.ChosenTopic.set("Sort only by Unit")
                    self.ListOfDropdown.append(self.OptionMenu)
                    ChosenTopic = self.ChosenTopic.get()
                    

            if ChosenUnit == UnitList[1]:#IN
                    self.ChosenTopic.set("Sort only by Unit")
                    self.OptionMenu = OptionMenu(self.frame, self.ChosenTopic, *InorganicTopics)
                    self.OptionMenu.grid(column = 4, row = 1, columnspan = 2, sticky = N+E+S+W)
                    self.ListOfDropdown.append(self.OptionMenu)
                    ChosenTopic = self.ChosenTopic.get()
                    

            if ChosenUnit == UnitList[2]:#OR
                    self.ChosenTopic.set("Sort only by Unit")
                    self.OptionMenu = OptionMenu(self.frame, self.ChosenTopic, *OrganicTopics)
                    self.OptionMenu.grid(column = 4, row = 1, columnspan = 2, sticky = N+E+S+W)
                    self.ListOfDropdown.append(self.OptionMenu)
                    ChosenTopic = self.ChosenTopic.get()                    

            self.ChosenTopic.trace('w', changedropdown)

        UnitDropdown = OptionMenu(self.frame, self.ChosenUnit, *UnitList)
        UnitDropdown.grid(row = 1, sticky = N+E+S+W, column = 2, columnspan = 2)
        self.ListOfDropdown.append(UnitDropdown)
        self.ChosenUnit.trace('w', ChangeDropdown)

    def GetResults(self, QuestionData, Topic, Unit):
        self.canvas.config(width = 1200, height = 200)
        self.Window.wm_geometry("1250x250")

        ListOfQuestions = []
        
        
        for x in range(len(self.ListOfWidgets)):
            self.ListOfWidgets[x].destroy()
            
        for x in range(len(QuestionData)):
            if QuestionData[x][2] == Unit:
                if QuestionData[x][3] == Topic:
                        ListOfQuestions.append(QuestionData[x])
                elif Topic == "Sort only by Unit":
                    ListOfQuestions.append(QuestionData[x])

            
        if ListOfQuestions:            
            for y in range(len(ListOfQuestions)):
                for z in range(len(ListOfQuestions[y])):
                    widget = Label(self.frame, text = ListOfQuestions[y][z])
                    widget.grid(row = y+4, column = z, padx = 10, sticky = W)
                    self.ListOfWidgets.append(widget)
                                       
            

    def All(self, QuestionData):
        for x in range(len(self.ListOfDropdown)):
            self.ListOfDropdown[x].destroy()
            
        self.canvas.config(width = 1200, height = 200)
        self.Window.wm_geometry("1250x250")
        for x in range(len(self.ListOfWidgets)):
            self.ListOfWidgets[x].destroy()
        
        for x in range(len(QuestionData)):
            for y in range(len(QuestionData[x])):
                widget = Label(self.frame, text = QuestionData[x][y])
                widget.grid(row = x+4, column = y, padx = 10, sticky = W)
                self.ListOfWidgets.append(widget)

    def SetTitles(self):
        Label(self.frame, text = "Question").grid(row = 2, sticky = W, padx = 10)
        Label(self.frame, text = "Answer/KeyWords").grid(column = 1, row = 2, sticky = W, padx = 10)
        Label(self.frame, text = "Unit").grid(column = 2, row = 2, sticky = W, padx = 10)
        Label(self.frame, text = "Topic").grid(column = 3, row = 2, sticky = W, padx = 10)
        Label(self.frame, text = "Multiple Choice?").grid(column = 4, row = 2, sticky = W, padx = 10)
        Label(self.frame, text = "Multiple Choice Option 1").grid(column = 5, row = 2, sticky = W, padx = 10)
        Label(self.frame, text = "Multiple Choice Option 2").grid(column = 6, row = 2, sticky = W, padx = 10)
        Label(self.frame, text = "Multiple Choice Option 3").grid(column = 7, row = 2, sticky = W, padx = 10)
        
class Database:          

    def CheckCreds(Username,Password):
        conn=sqlite3.connect('OnlineHomework.db', timeout = 1)
        c=conn.cursor()
        
        Cipher_Suite = Fernet(DatabaseKey.key)
        
        TeacherUsername = []
        TeacherPassword = []
        c.execute("SELECT Password FROM TeacherLogin")
        for column in c:
            UncipheredText = Cipher_Suite.decrypt(column[-1])
            PlainText = (bytes(UncipheredText).decode("utf-8"))
            TeacherPassword.append(PlainText)

            
        c.execute("SELECT Username FROM TeacherLogin;")
        for column in c:
            TeacherUsername.append(column[0])
        print(TeacherUsername)
        print(TeacherPassword)
        if Username in TeacherUsername:
            Correct = int(TeacherUsername.index(Username))
            if str(Password) == TeacherPassword[Correct]:
                tm.showinfo("Login info", "Welcome " + Username)
                root.withdraw()
                MainWindow()
            else:
                tm.showerror("Login error", "Incorrect Username or Password. Please try again.")
                
        else:
            tm.showerror("Login error", "Incorrect Username or Password. Please try again.")
        conn.commit()
        conn.close()

root = Tk()
root.title("Please login")
root.resizable(width=False,height=False)

Login(root)
root.mainloop()
