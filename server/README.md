# StudyMate Backend (Django + MongoDB)

## Setup Instructions

1. **Create and activate virtual environment:**
```bash
cd server
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create .env file:**
```bash
cp .env.example .env
# Edit .env and add your MongoDB URI and SECRET_KEY
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (Admin):**
```bash
python manage.py createsuperuser
# Use: username=Admin, email=jacsiceadmin@gmail.com, password=jacsice@Admin
```

6. **Run server:**
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/token/` - Login (returns JWT tokens)
- `POST /api/auth/register/` - Register new student

### Student APIs
- `GET /api/student/years/` - Get all years
- `GET /api/student/semesters/?year=<id>` - Get semesters by year
- `GET /api/student/subjects/?semester=<id>` - Get subjects by semester
- `GET /api/student/materials/?subject=<id>&search=<term>&type=<type>` - Get materials
- `GET /api/student/materials/<id>/download/` - Download material

### Admin APIs (Requires Admin role)
- `GET /api/admin/students/` - List all students
- `POST /api/admin/students/` - Create student
- `POST /api/admin/academic-structure/create_year/` - Create year
- `POST /api/admin/academic-structure/create_semester/` - Create semester
- `POST /api/admin/academic-structure/create_subject/` - Create subject
- `GET /api/admin/materials/` - List all materials
- `POST /api/admin/materials/` - Upload material

## MongoDB Connection

The backend uses MongoDB with the connection string:
```
mongodb+srv://nalliayanandhakumar_db_user:StudyMate@cluster0.giucynj.mongodb.net/
```

Make sure to update the `.env` file with the correct MongoDB URI.



