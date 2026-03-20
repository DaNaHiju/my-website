from flask import Flask, render_template

app = Flask(__name__)

# Mock Data for CV (In a real scenario, this could come from a database)
cv_data = {
    "name": "Jane Doe",
    "title": "DevOps Engineer | Python Developer",
    "summary": "Passionate DevOps Engineer with a strong background in Python development and automation. Experienced in building CI/CD pipelines and managing cloud infrastructure.",
    "experience": [
        {
            "role": "Senior DevOps Engineer",
            "company": "Tech Solutions Inc.",
            "duration": "2023 - Present",
            "description": "Leading the migration to containerized microservices architecture. Implemented automated testing and deployment pipelines using GitHub Actions and Docker."
        },
        {
            "role": "Python Developer",
            "company": "DataCorp",
            "duration": "2021 - 2023",
            "description": "Developed backend services using Flask and Django. Optimized database queries and improved application performance by 30%."
        }
    ],
    "education": [
        {
            "degree": "B.Sc. in Computer Science",
            "school": "University of Technology",
            "year": "2021"
        }
    ],
    "skills": ["Python", "Docker", "Kubernetes", "CI/CD", "AWS", "Linux", "Terraform", "Git"]
}

@app.route('/')
def home():
    return render_template('index.html', cv=cv_data)

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(debug=True)
