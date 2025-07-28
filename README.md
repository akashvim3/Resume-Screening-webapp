# Resume Screening Web Application

A modern Django web application that helps recruiters and hiring managers streamline their resume screening process. This application allows users to upload job descriptions and resumes, then automatically screens and matches resumes against job requirements.

## Features

- 🔐 User Authentication (Register/Login)
- 📝 Job Posting Management
- 📄 Resume Upload and Management
- 🤖 Automated Resume Screening
- 📊 Screening Results Dashboard
- 🎨 Modern and Responsive UI
- 🔍 Advanced Resume Analysis

## Tech Stack

- **Backend**: Django
- **Frontend**: Bootstrap 5, Custom CSS
- **Database**: SQLite
- **Icons**: Font Awesome
- **UI/UX**: Modern design with animations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/akashvim3/resume-screening-web.git
cd resume-screening-web
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## Usage

1. Register a new account or login
2. Create a new job posting with requirements
3. Upload resumes for screening
4. View screening results and analysis
5. Manage your job postings and resume database

## Project Structure

```
├── manage.py
├── requirements.txt
├── media/               # Uploaded files
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
├── screening/         # Main application
└── resume_screener/   # Project settings
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Django Framework
- UI components from Bootstrap 5
- Icons from Font Awesome
- Resume analysis powered by advanced algorithms

---

Developed with ❤️ by Akash
