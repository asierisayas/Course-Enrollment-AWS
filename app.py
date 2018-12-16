import sys
import json
import logging
import pymysql

rds_host = "schooldb.cmgqdpk2xfxi.us-east-2.rds.amazonaws.com"
username = "aisayas3"
password = "" //Enter password
db_name = "schoolDB"

def getStudents(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306,
        )
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    studentlist=[]
    for item in rows:
        student = {}
        student['sID'] = item[0]
        student['Name'] = item[1]
        student['Major'] = item[2]
        student['GPA'] = item[3]
        student['DOB'] = item[4]
        studentlist.append(student)
    print json.dumps(studentlist)
    return studentlist

def getStudentDetails(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306,
        )
    statement = "SELECT * FROM student WHERE student.STUDENT_ID = {}".format(event['sID'])
    cursor = conn.cursor()
    cursor.execute(statement)
    
    
    studentInfo = cursor.fetchall()
    student = {}
    student['sID'] = studentInfo[0][0]
    student['Name'] = studentInfo[0][1]
    student['Major'] = studentInfo[0][2]
    student['GPA'] = studentInfo[0][3]
    student['DOB'] = studentInfo[0][4]
    
    print student
    return student
    
def getCourseCount(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306
        )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course")
    course_count = 0;

    for row in cursor:
        course_count += 1

    return course_count

def getCourses(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306
        )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course")

    courseList = []
    for item in cursor:
        course = {}
        course['cID'] = item[0]
        course['Name'] = item[1]
        course['Department'] = item[2]
        courseList.append(course)
    print json.dumps(courseList)
    return courseList

def deleteCourse(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306
        )
    
    cursor = conn.cursor()
    statement = "DELETE from course WHERE course.COURSE_ID = {}".format(event['cID'])
    cursor.execute(statement)
    conn.commit()
    
def addStudent(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306
        )   
    statement = "INSERT INTO student (STUDENT_ID,NAME,MAJOR,GPA,DOB) VALUES ({}, '{}', '{}', {}, '{}')".format(event['sID'], event['Name'], event['Major'], event['GPA'], event['DOB'])
    
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()

def updateStudent(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306
        ) 
    statement = "UPDATE student SET Name='{}', MAJOR='{}', GPA={}, DOB='{}' WHERE STUDENT_ID ={}".format(event['Name'], event['Major'], event['GPA'], event['DOB'], event['sID'])

    cursor = conn.cursor()
    print statement
    cursor.execute(statement)
    conn.commit()
    
def addCourse(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306
        )
    statement = "INSERT INTO course (COURSE_ID,NAME,DEPARTMENT) VALUES ({}, '{}', '{}')".format(event['cID'], event['cName'], event['Department']) 

    conn = conn.cursor()
    cursor.execute(statement)   
    conn.commit()

def addInstructor(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306
        )
    statement = "INSERT INTO instructor (INSTRUCTOR_ID,NAME,DEPARTMENT) VALUES ({}, '{}', '{}')".format(event['iID'], event['iName'], event['Department'])
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()
    
def addDepartment(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306
        )
    statement = "INSERT INTO department (DEPARTMENT,LOCATION) VALUES ('{}', '{}')".format(event['Department'], event['Location'])
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()
    
    
def RDS_init(event, context):
    conn = pymysql.connect(rds_host, user = username, passwd = password, db = db_name,port = 3306, 
        )
        
    course_count = 0;
    student_count = 0;
    semester_count = 0;
    instructor_count = 0;
    
    cursor = conn.cursor()
    cursor.execute("drop table if exists semester")
    cursor.execute("drop table if exists offers")
    cursor.execute("drop table if exists student")
    cursor.execute("drop table if exists course")
    cursor.execute("drop table if exists instructor")
    cursor.execute("drop table if exists department")
    #Add students to RDS
    cursor.execute("CREATE TABLE student (STUDENT_ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, MAJOR TEXT NOT NULL, GPA FLOAT NOT NULL, DOB TEXT NOT NULL)")
    cursor.execute("INSERT INTO student (STUDENT_ID,NAME,MAJOR,GPA,DOB) VALUES (54321, 'Alan', 'ECE', 3.2, '02/10/1990')")
    cursor.execute("INSERT INTO student (STUDENT_ID,NAME,MAJOR,GPA,DOB) VALUES (54322, 'Bob', 'CS', 3.6, '08/15/1988')")
    cursor.execute("INSERT INTO student (STUDENT_ID,NAME,MAJOR,GPA,DOB) VALUES (54323, 'Charlie', 'ECE', 3.7, '05/12/1989')")
    cursor.execute("INSERT INTO student (STUDENT_ID,NAME,MAJOR,GPA,DOB) VALUES (54324, 'Dylan', 'CS', 3.7, '04/11/1988')")
    cursor.execute("INSERT INTO student (STUDENT_ID,NAME,MAJOR,GPA,DOB) VALUES (54325, 'Eric', 'ECE', 3.4, '10/29/1987')")
    
    #Add department table
    cursor.execute("CREATE TABLE department (DEPARTMENT VARCHAR(5) PRIMARY KEY NOT NULL, LOCATION TEXT NOT NULL)")
    cursor.execute("INSERT INTO department (DEPARTMENT,LOCATION) VALUES ('ECE', 'Van Leer')")
    cursor.execute("INSERT INTO department (DEPARTMENT,LOCATION) VALUES ('CS', 'Klaus')")
    
    #Add course table
    cursor.execute("CREATE TABLE course (COURSE_ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, DEPARTMENT VARCHAR(5) NOT NULL)")
    cursor.execute("INSERT INTO course (COURSE_ID,NAME,DEPARTMENT) VALUES (4813, 'Cloud Computing', 'ECE');")
    cursor.execute("INSERT INTO course (COURSE_ID,NAME,DEPARTMENT) VALUES (4400, 'Computer Architecture', 'ECE');")
    cursor.execute("INSERT INTO course (COURSE_ID,NAME,DEPARTMENT) VALUES (6020, 'Algorithms', 'CS');")
    cursor.execute("INSERT INTO course (COURSE_ID,NAME,DEPARTMENT) VALUES (6400, 'Database Systems', 'CS');")
    
    #Add offers table
    cursor.execute("CREATE TABLE offers (COURSE_ID INT NOT NULL,DEPARTMENT VARCHAR(5) NOT NULL,PRIMARY KEY(COURSE_ID, DEPARTMENT),FOREIGN KEY (COURSE_ID) REFERENCES course(COURSE_ID) ON DELETE CASCADE ON UPDATE CASCADE,FOREIGN KEY (DEPARTMENT) REFERENCES department(DEPARTMENT) ON DELETE CASCADE ON UPDATE CASCADE)")

    #Add instructor table
    cursor.execute("CREATE TABLE instructor (INSTRUCTOR_ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NUll, DEPARTMENT VARCHAR(5) NOT NULL)")
    cursor.execute("INSERT INTO instructor (INSTRUCTOR_ID, NAME, DEPARTMENT) VALUES (12345, 'Johnson', 'CS')")
    cursor.execute("INSERT INTO instructor (INSTRUCTOR_ID, NAME, DEPARTMENT) VALUES (98237, 'Smith', 'CS')")
    cursor.execute("INSERT INTO instructor (INSTRUCTOR_ID, NAME, DEPARTMENT) VALUES (53453, 'Madisetti', 'ECE')")
    cursor.execute("INSERT INTO instructor (INSTRUCTOR_ID, NAME, DEPARTMENT) VALUES (98234, 'Yoder', 'ECE')")
   
    
    #Add semester table
    cursor.execute("CREATE TABLE semester(STUDENT_ID INT NOT NULL,COURSE_ID INT NOT NULL, INSTRUCTOR_ID INT NOT NULL, SEMESTER TEXT NOT NULL,YEAR INT NOT NULL, MARKS INT NOT NULL,FOREIGN KEY (STUDENT_ID) REFERENCES student(STUDENT_ID) ON DELETE CASCADE ON UPDATE CASCADE,FOREIGN KEY (COURSE_ID) REFERENCES course(COURSE_ID) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY (INSTRUCTOR_ID) REFERENCES instructor(INSTRUCTOR_ID) ON DELETE CASCADE ON UPDATE CASCADE, PRIMARY KEY (STUDENT_ID, COURSE_ID))")
    cursor.execute("INSERT INTO semester (STUDENT_ID, COURSE_ID, INSTRUCTOR_ID, SEMESTER, YEAR, MARKS) VALUES (54321, 6400, 12345, 'Fall', 2015, 91)")
    cursor.execute("INSERT INTO semester (STUDENT_ID, COURSE_ID, INSTRUCTOR_ID, SEMESTER, YEAR, MARKS) VALUES (54321, 4813, 98237, 'Spring', 2015, 85)")
    cursor.execute("INSERT INTO semester (STUDENT_ID, COURSE_ID, INSTRUCTOR_ID, SEMESTER, YEAR, MARKS) VALUES (54322, 6020, 98237, 'Fall', 2015, 88)")
    cursor.execute("INSERT INTO semester (STUDENT_ID, COURSE_ID, INSTRUCTOR_ID, SEMESTER, YEAR, MARKS) VALUES (54323, 4400, 53453, 'Fall', 2015, 79)")
    cursor.execute("INSERT INTO semester (STUDENT_ID, COURSE_ID, INSTRUCTOR_ID, SEMESTER, YEAR, MARKS) VALUES (54324, 6020, 53453, 'Spring', 2015, 75)")
    cursor.execute("INSERT INTO semester (STUDENT_ID, COURSE_ID, INSTRUCTOR_ID, SEMESTER, YEAR, MARKS) VALUES (54324, 6400, 98234, 'Fall', 2015, 75)")
    cursor.execute("INSERT INTO semester (STUDENT_ID, COURSE_ID, INSTRUCTOR_ID, SEMESTER, YEAR, MARKS) VALUES (54325, 4813, 98234, 'Spring', 2015, 84)")
    conn.commit()
    
    cursor.execute("SELECT * FROM department")
    print cursor.fetchall()
    
    cursor.execute("SELECT * FROM course")
    for row in cursor:
        course_count +=1
    cursor.execute("SELECT * FROM student")
    for row in cursor:
        student_count +=1
        
    cursor.execute("SELECT * FROM semester")
    for row in cursor:
        semester_count += 1
        
    cursor.execute("SELECT * FROM instructor")
    for row in cursor:
        instructor_count += 1

        
    return "Added %d items to course; Added %d items to student; Added %d items to semester; Added %d items to instructor" %(course_count, student_count, semester_count, instructor_count)
    