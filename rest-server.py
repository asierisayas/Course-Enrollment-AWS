#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect

import sys
import requests
import json

app = Flask(__name__, static_url_path="")

@app.route('/', methods=['GET'])
def home_page():
	students = requests.get("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/students").json()
	
	studentList = []
	for item in students:
		student = {}
		student['sID'] = item['sID']
		student['Name'] = item['Name']
		student['Major'] = item['Major']
		student['GPA'] = item['GPA']
		student['DOB'] = item['DOB']
		studentList.append(student)

	return render_template('index.html', students = studentList)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student_page():
	if request.method == 'POST':
		student = {
			"sID": "{}".format(request.form['sID']),
			"Name": "{}".format(request.form['Name']),
			"Major": "{}".format(request.form['Major']),
			"GPA": "{}".format(request.form['GPA']),
			"DOB": "{}".format(request.form['DOB'])
		}
		print (student)
		entry = requests.post("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/student", data = json.dumps(student))
		
		return redirect('/')	
	else:
		return render_template('addStudent.html')

@app.route('/student/viewDetails/<int:student_id>', methods=['GET'])
def view_student_details(student_id):
	result = requests.get("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/students").json()
	student = {}
	for item in result:
		if item['sID'] == student_id:
			student['sID'] = item['sID']
			student['Name'] = item['Name']
			student['Major'] = item['Major']
			student['GPA'] = item['GPA']
			student['DOB'] = item['DOB']
	print (json.dumps)
	return render_template('viewStudentDetails.html', student = student)

@app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
	if request.method == 'POST':
		student = {
			"sID": "{}".format(student_id),
			"Name": "{}".format(request.form['Name']),
			"Major": "{}".format(request.form['Major']),
			"GPA": "{}".format(request.form['GPA'])
		}
		print (json.dumps(student))
		result = requests.put("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/student", data = json.dumps(student))
		return redirect('/')
	else:
		result = requests.get("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/students").json()
		student = {}
		for item in result:
			if item['sID'] == student_id:
				student['sID'] = item['sID']
				student['Name'] = item['Name']
				student['Major'] = item['Major']
				student['GPA'] = item['GPA']
				student['DOB'] = item['DOB']
	
		return render_template("updateStudent.html", student = student)
@app.route('/department/add', methods=['GET', 'POST'])
def add_department_page():
	if request.method == 'POST':
		department = {
			"Department": "{}".format(request.form['dptName']),
			"Location": "{}".format(request.form['Location'])
		}
		
		entry = requests.post("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/department", data = json.dumps(department))
		return redirect('/')
	else:
		return render_template('addDepartment.html')

@app.route('/instructor/add', methods=['GET', 'POST'])
def add_instructor_page():
	if request.method == 'POST':
		instructor = {
			"iID": "{}".format(request.form['iID']),
			"iName": "{}".format(request.form['iName']),
			"Department": "{}".format(request.form['dptName'])
		}

		print (instructor)
		entry = requests.post("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/instructor", data = json.dumps(instructor))
		return redirect('/')
	else:
		return render_template('addInstructor.html')

@app.route('/courses', methods=['GET', 'POST'])
def view_courses_page():
	courses = requests.get("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/courses").json()
	
	courseList = []
	course_count = 0;
	for item in courses:
		course_count += 1
		course = {}
		course['cID'] = item['cID']
		course['Name'] = item['Name']
		course['Department'] = item['Department']
		courseList.append(course)

	return render_template('viewCourses.html', courses = courseList, courseCount = course_count)	

@app.route('/course/delete/<int:course_id>', methods=['GET'])
def delete_course(course_id):
	course = {
		"cID": "{}".format(course_id)
	}
	print (course)

	delete = requests.delete("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/course", data=json.dumps(course))
	print (delete)
	return redirect('/')

@app.route('/course/add', methods=['GET', 'POST'])
def add_course_page():
	if request.method == 'POST':
		course = {
			"cID": "{}".format(request.form['cID']),
			"cName": "{}".format(request.form['cName']),
			"Department": "{}".format(request.form['Department'])
		}
		print (course)
		entry = requests.post("https://3qrkx5yvf6.execute-api.us-east-2.amazonaws.com/prod/course", data = json.dumps(course))
		return redirect('/')
	else:
		return render_template('addCourse.html')

if __name__ == '__main__':
    #app.run(debug=True, port=5000) #local
    app.run(debug=True, host='0.0.0.0', port=80) #EC2