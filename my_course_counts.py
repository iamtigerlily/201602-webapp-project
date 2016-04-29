from os import chdir
from os.path import dirname, realpath

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

class Course:
	def __init__(self, year, season, department, crn, section_title, units, instructors, meetings, core, total_seats, enrolled_seats):
            self.year = year
            self.season = season
            self.department = department
            self.crn = crn
            self.waistlisted = waitlisted
            self.section_title = section_title
            self.units = units
            self.instructors = instructors
            self.meetings = meetings
            self.core = core
            self.total_seats = total_seats
            self.enrolled_seats = enrolled_seats

class Library:
        def __init__(self):
            self.courses = []
        def search_by_department(self, department):
            results = []
            for course in self.courses:
                open = True
                if course.department != department:
                    open = False
                if course.total_seats <= course.enrolled_seats:
                    open = False
                if(open):
                    results.append(course)
            return results

def get_library():
    library = Library()
    with open('counts.tsv') as fd:
        for line in fd.read().splitlines():
            fields = line.split('\t')
            course = Course(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8], fields[9], fields[10])
            library.courses.append(course)
        return library

def get_department_list():
    library = Library()
    department_list = []
    with open('counts.tsv') as fd:
      for line in fd.read().splitlines():
          fields = line.split('\t')
          if fields[2] not in department_list:
            department_list.append(fields[2])
    return department_list


@app.route('/')
def view_departments():
    departments = get_department_list()
    return render_template('base.html',departments = departments)
@app.route('/<department>')
def view_courses(department):
    library = get_library()
    course_list = library.search_by_department(department)
    return render_template('courses.html',  course_list = course_list)

# The functions below lets you access files in the css, js, and images folders.
# You should not change them unless you know what you are doing.

@app.route('/images/<file>')
def get_image(file):
    return send_from_directory('images', file)

@app.route('/css/<file>')
def get_css(file):
    return send_from_directory('css', file)

@app.route('/js/<file>')
def get_js(file):
    return send_from_directory('js', file)

if __name__ == '__main__':
    chdir(dirname(realpath(__file__)))
    app.run(debug=True)
