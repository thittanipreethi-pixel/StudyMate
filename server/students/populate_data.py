"""
Populate academic structure for BSc Computer Science (Arts & Science).
"""
import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from students.models import Department, Year, Semester, Subject

# BSc Computer Science - 3 years, 6 semesters (Arts & Science)
DATA = [
    # Year 1
    {"department": "BSc Computer Science", "year": 1, "semester": 1, "subjects": [
        "Language – Tamil / Hindi",
        "English – I",
        "Mathematical Foundations",
        "Digital Computer Fundamentals",
        "Programming in C",
        "Environmental Studies",
    ]},
    {"department": "BSc Computer Science", "year": 1, "semester": 2, "subjects": [
        "English – II",
        "Statistics for Computer Science",
        "Data Structures",
        "Object Oriented Programming",
        "Python Programming",
        "Value Education",
    ]},
    # Year 2
    {"department": "BSc Computer Science", "year": 2, "semester": 3, "subjects": [
        "Discrete Mathematics",
        "Database Management Systems",
        "Computer Networks",
        "Operating Systems",
        "Java Programming",
        "Soft Skills",
    ]},
    {"department": "BSc Computer Science", "year": 2, "semester": 4, "subjects": [
        "Linear Algebra",
        "Software Engineering",
        "Web Technology",
        "Microprocessor and Assembly Language",
        "Design and Analysis of Algorithms",
        "Gender Studies",
    ]},
    # Year 3
    {"department": "BSc Computer Science", "year": 3, "semester": 5, "subjects": [
        "Theory of Computation",
        "Computer Graphics",
        "Mobile Application Development",
        "Cloud Computing",
        "Elective – I",
        "Extension Activities",
    ]},
    {"department": "BSc Computer Science", "year": 3, "semester": 6, "subjects": [
        "Artificial Intelligence",
        "Data Science",
        "Cyber Security",
        "Project Work",
        "Elective – II",
    ]},
]


def populate_data():
    print("Populating BSc Computer Science (Arts & Science) data...")
    depts_created = 0
    years_created = 0
    semesters_created = 0
    subjects_created = 0

    for entry in DATA:
        dept_name = entry["department"]
        year_num = entry["year"]
        sem_num = entry["semester"]

        department, c = Department.objects.get_or_create(
            name=dept_name,
            defaults={"code": "BSC-CS"},
        )
        if c:
            depts_created += 1
            print(f"Department: {dept_name}")

        year, c = Year.objects.get_or_create(
            name=f"Year {year_num}",
            defaults={"number": year_num},
        )
        if c:
            years_created += 1

        semester, c = Semester.objects.get_or_create(
            department=department,
            year=year,
            number=sem_num,
            defaults={"name": f"Semester {sem_num}"},
        )
        if c:
            semesters_created += 1

        for subj_name in entry["subjects"]:
            subject, c = Subject.objects.get_or_create(
                semester=semester,
                name=subj_name.strip(),
                defaults={"code": ""},
            )
            if c:
                subjects_created += 1
                print(f"  + {subj_name}")

    print(f"\nDone. Departments: {Department.objects.count()}, Years: {Year.objects.count()}, "
          f"Semesters: {Semester.objects.count()}, Subjects: {Subject.objects.count()}")


if __name__ == "__main__":
    populate_data()
