import DatabaseKey
from cryptography.fernet import Fernet
import random
import sqlite3

Chars = 'abcdefghijklmnopqrstuv1234567890'
CipheredPsw = []
for x in range(8):
    Password = ""
    for y in range(6):
        Text = random.choice(Chars)
        Password+=(Text)
    Pass = bytes(Password, "ascii")
    
    Cipher_Suite = Fernet(DatabaseKey.key)
    CipheredText = Cipher_Suite.encrypt(bytes(Pass))
    CipheredPsw.append(CipheredText)
    
conn=sqlite3.connect('OnlineHomework.db')
c=conn.cursor()

c.execute('''CREATE TABLE  IF NOT EXISTS `TeacherLogin` (
	`Username`	TEXT NOT NULL,
	`Password`	INT NOT NULL,
	`Class`	TEXT NOT NULL,
	`TeacherID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE);''')

c.execute('''CREATE TABLE  IF NOT EXISTS `StudentLogin` (
        'FirstName'     TEXT NOT NULL,
	`Username`	TEXT NOT NULL,
	`Password`	INT NOT NULL,
	`StudentID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Class`	TEXT NOT NULL);''')

c.execute('''INSERT INTO StudentLogin (FirstName, Username, Password, Class)
    VALUES
        ('Fred', 'FSmith',?, '13A/Ch2'),
        ('John', 'JTucker',?, '13A/Ch2'),
        ('Michael', 'MJefford',?, '13A/Ch2'),
        ('Robert', 'RThomas',?, '13B/Ch1');''', (CipheredPsw[0], CipheredPsw[1], CipheredPsw[2], CipheredPsw[3]))

c.execute('''INSERT INTO TeacherLogin(Username,Password,Class)
    VALUES('HTucker',?,'12C/C1'),
    ('ACooper',?,'12C/Ma1'),
    ('KSmith',?,'12C/Ch1'),
    ('FElston',?,'12C/Ch1');''', (CipheredPsw[4], CipheredPsw[5], CipheredPsw[6], CipheredPsw[7]))


c.execute('''CREATE TABLE `Classes` (
	`ClassID`	INTEGER NOT NULL,
	`TeacherID`	INTEGER NOT NULL,
	`StudentID`	INTEGER NOT NULL,
	`Subject`	INTEGER NOT NULL,
	PRIMARY KEY(`ClassID`));''')

c.execute('''CREATE TABLE `Completed Homework` (
	`Name`	TEXT NOT NULL,
	`Score`	INTEGER NOT NULL,
	PRIMARY KEY(`Name`));''')

c.execute('''CREATE TABLE `Previous Homework` (
	`StudentAns`	TEXT,
	`Correct?`	TEXT NOT NULL,
	`Multiple Choice?`	TEXT NOT NULL,
	`Question`	TEXT,
	`CorrectAns`	TEXT,
	`StudentName`	INTEGER,
	`Score`	INTEGER,
	`HomeworkID`	INTEGER);''')

c.execute('''CREATE TABLE `QuestionID` (
	`QuestionID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`QText`	TEXT NOT NULL,
	`QAnswer`	TEXT NOT NULL,
	`QUnit`	INTEGER NOT NULL,
	`QTopic`	INTEGER NOT NULL,
	`MChoice`	BOOLEAN NOT NULL);''')

c.execute('''CREATE TABLE `SetHomework` (
	`HomeworkID`	INTEGER NOT NULL,
	`ClassID`	INTEGER,
	`TeacherID`	INTEGER);''')

c.execute('''CREATE TABLE `StudentScore` (
	`StudentID`	INTEGER NOT NULL,
	`HomeworkID`	INTEGER NOT NULL,
	`ClassID`	INTEGER NOT NULL,
	`Score`	INTEGER NOT NULL);''')

conn.commit()
conn.close()
