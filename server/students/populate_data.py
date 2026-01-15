"""
Script to populate academic structure data
"""
import sys
import os
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from students.models import Department, Year, Semester, Subject

# Data from user
data = [
    {
        "department": "CSE",
        "semester": 1,
        "year": 1,
        "subjects": [
            "MA25C01 Applied Calculus",
            "EN25C01 English Essentials – I",
            "UC25H01 Heritage of Tamils",
            "PH25C01 Applied Physics – I",
            "CY25C01 Applied Chemistry – I",
            "CS25C01 Computer Programming: C",
            "CS25C03 Essentials of Computing",
            "ME25C04 Makerspace",
            "UC25A01 Life Skills for Engineers – I",
            "UC25A02 Physical Education – I"
        ]
    },
    {
        "department": "CSE",
        "semester": 2,
        "year": 1,
        "subjects": [
            "MA25C02 Linear Algebra",
            "EE25C01 Basic Electrical and Electronics Engineering",
            "CS25C06 Digital Principles and Computer Organization",
            "UC25H02 Tamils and Technology",
            "PH25C03 Applied Physics (CSIE) – II",
            "CS25C07 Object Oriented Programming",
            "EN25C02 English Essentials – II",
            "ME25C05 Re-Engineering for Innovation",
            "UC25A03 Life Skills for Engineers – II",
            "UC25A04 Physical Education – II"
        ]
    },
    {
        "department": "EEE",
        "semester": 1,
        "year": 1,
        "subjects": [
            "MA25C01 Applied Calculus",
            "EE25C03 Fundamentals of Electrical and Electronics Engineering",
            "UC25H01 Heritage of Tamils",
            "EN25C01 English Essentials – I",
            "PH25C01 Applied Physics – I",
            "CY25C01 Applied Chemistry – I",
            "CS25C01 Computer Programming: C",
            "ME25C04 Makerspace",
            "UC25A01 Life Skills for Engineers – I",
            "UC25A02 Physical Education – I"
        ]
    },
    {
        "department": "EEE",
        "semester": 2,
        "year": 1,
        "subjects": [
            "MA25C03 Transforms and its Applications",
            "UC25H02 Tamils and Technology",
            "GE25C01 Basic Civil and Mechanical Engineering",
            "PH25C04 Applied Physics (EE) – II",
            "ME25C01 Engineering Drawing",
            "EN25C02 English Essentials – II",
            "CS25C04 Data Structures and Algorithms",
            "ME25C05 Re-Engineering for Innovation",
            "UC25A03 Life Skills for Engineers – II",
            "UC25A04 Physical Education – II"
        ]
    },
    {
        "department": "ECE",
        "semester": 1,
        "year": 1,
        "subjects": [
            "MA25C01 Applied Calculus",
            "EN25C01 English Essentials – I",
            "UC25H01 Heritage of Tamils",
            "Introduction to Electronics Engineering",
            "PH25C01 Applied Physics – I",
            "CY25C01 Applied Chemistry – I",
            "Computer Programming",
            "ME25C04 Makerspace"
        ]
    },
    {
        "department": "ECE",
        "semester": 2,
        "year": 1,
        "subjects": [
            "Transforms and its Applications",
            "Tamils and Technology",
            "Applied Physics (ECE) – II",
            "EN25C02 English Essentials – II",
            "Electron Devices",
            "Data Structures and OOPS with Python",
            "Circuits and Network Analysis",
            "Reverse Engineering"
        ]
    },
    {
        "department": "IT",
        "semester": 1,
        "year": 1,
        "subjects": [
            "MA25C01 Applied Calculus",
            "EN25C01 English Essentials – I",
            "UC25H01 Heritage of Tamils",
            "PH25C01 Applied Physics – I",
            "CY25C01 Applied Chemistry – I",
            "CS25C01 Computer Programming: C",
            "CS25C03 Essentials of Computing",
            "ME25C04 Makerspace",
            "UC25A01 Life Skills for Engineers – I",
            "UC25A02 Physical Education – I"
        ]
    },
    {
        "department": "IT",
        "semester": 2,
        "year": 1,
        "subjects": [
            "MA25C02 Linear Algebra",
            "UC25H02 Tamils and Technology",
            "EE25C01 Basic Electrical and Electronics Engineering",
            "PH25C03 Applied Physics (CSIE) – II",
            "IT25201 Foundations of Data Science using Python",
            "IT25202 Digital Principles and System Design",
            "EN25C02 English Essentials – II",
            "ME25C05 Re-Engineering for Innovation",
            "UC25A03 Life Skills for Engineers – II",
            "UC25A04 Physical Education – II"
        ]
    }
]

def populate_data():
    """Populate academic structure from JSON data"""
    print("Starting data population...")
    
    # Create Year
    year, created = Year.objects.get_or_create(name="Year 1", defaults={'number': 1})
    print(f"Year: {year.name} ({'created' if created else 'exists'})")
    
    departments_created = 0
    semesters_created = 0
    subjects_created = 0
    
    for entry in data:
        # Create or get Department
        dept_name = entry['department']
        department, created = Department.objects.get_or_create(
            name=dept_name,
            defaults={'code': dept_name}
        )
        if created:
            departments_created += 1
            print(f"Created department: {dept_name}")
        
        # Create or get Semester
        semester_num = entry['semester']
        semester, created = Semester.objects.get_or_create(
            department=department,
            year=year,
            number=semester_num,
            defaults={'name': f"Semester {semester_num}"}
        )
        if created:
            semesters_created += 1
            print(f"Created semester: {dept_name} - Year {entry['year']} - Semester {semester_num}")
        
        # Create Subjects
        for subject_name in entry['subjects']:
            # Extract code if present (format: "CODE Name" or just "Name")
            parts = subject_name.split(' ', 1)
            code = parts[0] if len(parts) > 1 and len(parts[0]) <= 15 else ''
            name = parts[1] if len(parts) > 1 else subject_name
            
            subject, created = Subject.objects.get_or_create(
                semester=semester,
                name=name,
                defaults={'code': code}
            )
            if created:
                subjects_created += 1
                print(f"  Created subject: {name}")
    
    print(f"\n✅ Population complete!")
    print(f"  Departments: {departments_created} new")
    print(f"  Semesters: {semesters_created} new")
    print(f"  Subjects: {subjects_created} new")
    print(f"\nTotal: {Department.objects.count()} departments, {Semester.objects.count()} semesters, {Subject.objects.count()} subjects")

if __name__ == '__main__':
    populate_data()



