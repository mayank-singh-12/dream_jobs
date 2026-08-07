import datetime
from decimal import Decimal
from database import engine, SessionLocal
from models import (
    Base, User, UserRole, StudentProfile, StudentStatus,
    CompanyProfile, CompanyStatus, Job, JobStatus, JobMode, JobType,
    Application, ApplicationStatus
)
from app import app

def seed():
    print("Dropping and recreating database tables...")
    # Drop all tables and recreate them to fully clear data and schemas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Seeding database...")
    with SessionLocal() as db:
        # 1. Seed Admin User
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password="password123",
            role=UserRole.ADMIN
        )
        db.add(admin_user)

        # 2. Seed Company Users & Profiles
        companies_data = [
            ("TechCorp", "techcorp", "info@techcorp.com", "https://techcorp.com", "Leading software solutions provider.", "San Francisco", CompanyStatus.APPROVED),
            ("InnovateSoft", "innovate", "info@innovatesoft.com", "https://innovatesoft.com", "Cutting-edge software product development.", "Boston", CompanyStatus.APPROVED),
            ("GreenEnergy", "greenenergy", "contact@greenenergy.com", "https://greenenergy.com", "Renewable energy and grid optimization.", "Seattle", CompanyStatus.APPROVED),
            ("GlobalRetail", "globalretail", "jobs@globalretail.com", "https://globalretail.com", "Worldwide retail and supply-chain logistics.", "Chicago", CompanyStatus.APPROVED),
            ("BioHealth", "biohealth", "careers@biohealth.com", "https://biohealth.com", "Biomedical research and clinical trial support.", "San Diego", CompanyStatus.APPROVED),
            ("FinanceFlow", "financeflow", "recruitment@financeflow.com", "https://financeflow.com", "High-frequency trading and wealth management.", "New York", CompanyStatus.APPROVED),
            ("AutoTech", "autotech", "hr@autotech.com", "https://autotech.com", "Autonomous vehicle navigation systems.", "Detroit", CompanyStatus.APPROVED),
            ("SkyMedia", "skymedia", "media@skymedia.com", "https://skymedia.com", "Digital content creation and media platforms.", "Los Angeles", CompanyStatus.APPROVED),
            ("CyberShield", "cybershield", "secure@cybershield.com", "https://cybershield.com", "Enterprise firewall and threat prevention systems.", "Austin", CompanyStatus.APPROVED),
            ("CloudSphere", "cloudsphere", "cloud@cloudsphere.com", "https://cloudsphere.com", "Distributed cloud infrastructure solutions.", "Denver", CompanyStatus.APPROVED),
            ("PendingInc", "pendinginc", "wait@pendinginc.com", "https://pendinginc.com", "A startup currently waiting for approval.", "Miami", CompanyStatus.PENDING),
        ]

        companies = []
        for name, username, email, website, about, location, status in companies_data:
            c_user = User(
                username=username,
                email=email,
                password="password123",
                role=UserRole.COMPANY
            )
            c_profile = CompanyProfile(
                name=name,
                website=website,
                about=about,
                location=location,
                status=status
            )
            c_user.company_profile = c_profile
            db.add(c_user)
            companies.append(c_profile)

        # 3. Seed Student Users & Profiles
        students_data = [
            ("Alice", "Smith", "alice", "alice@example.com", "MIT", 9.5, StudentStatus.ACTIVE, "555-0101"),
            ("Bob", "Jones", "bob", "bob@example.com", "Stanford", 8.2, StudentStatus.ACTIVE, "555-0102"),
            ("Charlie", "Brown", "charlie", "charlie@example.com", "Harvard", 7.8, StudentStatus.ACTIVE, "555-0103"),
            ("Diana", "Prince", "diana", "diana@example.com", "UC Berkeley", 9.8, StudentStatus.ACTIVE, "555-0104"),
            ("Ethan", "Hunt", "ethan", "ethan@example.com", "Caltech", 8.0, StudentStatus.ACTIVE, "555-0105"),
            ("Fiona", "Gallagher", "fiona", "fiona@example.com", "NYU", 6.5, StudentStatus.ACTIVE, "555-0106"),
            ("George", "Clark", "george", "george@example.com", "Georgia Tech", 8.7, StudentStatus.ACTIVE, "555-0107"),
            ("Hannah", "Abbott", "hannah", "hannah@example.com", "UT Austin", 9.1, StudentStatus.ACTIVE, "555-0108"),
            ("Ian", "Malcolm", "ian", "ian@example.com", "Princeton", 7.2, StudentStatus.ACTIVE, "555-0109"),
            ("Julia", "Roberts", "julia", "julia@example.com", "Columbia", 8.9, StudentStatus.ACTIVE, "555-0110"),
            ("Kevin", "Bacon", "kevin", "kevin@example.com", "Penn State", 8.4, StudentStatus.ACTIVE, "555-0111"),
            ("Laura", "Croft", "laura", "laura@example.com", "Yale", 9.3, StudentStatus.ACTIVE, "555-0112"),
        ]

        students = []
        for first, last, username, email, school, cgpa, status, phone in students_data:
            s_user = User(
                username=username,
                email=email,
                password="password123",
                role=UserRole.STUDENT
            )
            s_profile = StudentProfile(
                first_name=first,
                last_name=last,
                school=school,
                cgpa=Decimal(str(cgpa)),
                status=status,
                phone_number=phone
            )
            s_user.student_profile = s_profile
            db.add(s_user)
            students.append(s_profile)

        # Flush to generate IDs
        db.flush()

        # 4. Seed Job Placement Drives (at least 10 rows)
        # Note: REJECTED value is "reject", PENDING is "pending", APPROVED is "approved", CLOSED is "closed"
        jobs_data = [
            (companies[0].id, "Software Engineer", "San Francisco", JobMode.REMOTE, JobType.FULL_TIME, JobStatus.APPROVED, "Design and implement scalable Python microservices.", 8.5),
            (companies[0].id, "Backend Developer", "Remote", JobMode.HYBRID, JobType.PART_TIME, JobStatus.APPROVED, "Maintain database migrations and API schemas.", 8.0),
            (companies[1].id, "Frontend Developer", "Boston", JobMode.REMOTE, JobType.FULL_TIME, JobStatus.APPROVED, "Develop interactive UI elements with modern Vue.js framework.", 7.5),
            (companies[1].id, "Data Analyst", "Boston", JobMode.ON_SITE, JobType.CONTRACT, JobStatus.APPROVED, "Perform product analytics using SQL and Jupyter notebooks.", 8.0),
            (companies[2].id, "Renewable Specialist", "Seattle", JobMode.REMOTE, JobType.FULL_TIME, JobStatus.APPROVED, "Analyze smart grid solar feeds and load distribution forecasts.", 8.2),
            (companies[5].id, "Financial Analyst", "New York", JobMode.ON_SITE, JobType.FULL_TIME, JobStatus.APPROVED, "Optimize algorithmic trading portfolios and model market trends.", 8.5),
            (companies[6].id, "Mobile App Dev", "Detroit", JobMode.REMOTE, JobType.CONTRACT, JobStatus.APPROVED, "Build robust native applications on iOS and Android platforms.", 7.8),
            (companies[8].id, "Cybersecurity Analyst", "Austin", JobMode.HYBRID, JobType.FULL_TIME, JobStatus.APPROVED, "Identify vulnerabilities and enforce enterprise security patches.", 9.0),
            (companies[9].id, "DevOps Engineer", "Denver", JobMode.REMOTE, JobType.FULL_TIME, JobStatus.APPROVED, "Configure and maintain CI/CD pipelines in a Kubernetes stack.", 8.5),
            (companies[3].id, "System Administrator", "Chicago", JobMode.ON_SITE, JobType.FULL_TIME, JobStatus.PENDING, "Configure local network firewalls and user directory accesses.", 7.0),
            (companies[4].id, "Product Manager", "San Diego", JobMode.HYBRID, JobType.FULL_TIME, JobStatus.REJECTED, "Direct cross-functional product visions for clinical interfaces.", 9.0),
            (companies[7].id, "QA Engineer", "Los Angeles", JobMode.REMOTE, JobType.CONTRACT, JobStatus.CLOSED, "Verify platform updates using manual test scripts and Selenium.", 7.5),
        ]

        jobs = []
        base_deadline = datetime.datetime.now() + datetime.timedelta(days=10)
        for c_id, title, location, mode, j_type, status, desc, cgpa in jobs_data:
            job = Job(
                company_id=c_id,
                title=title,
                location=location,
                mode=mode,
                job_type=j_type,
                job_status=status,
                description=desc,
                required_cgpa=Decimal(str(cgpa)) if cgpa else None,
                deadline=base_deadline
            )
            db.add(job)
            jobs.append(job)

        # Flush to generate Job IDs
        db.flush()

        # 5. Seed Applications (at least 10 rows)
        applications_data = [
            (students[0].id, jobs[0].id, ApplicationStatus.SHORTLISTED),
            (students[1].id, jobs[1].id, ApplicationStatus.PENDING),
            (students[2].id, jobs[2].id, ApplicationStatus.APPROVED),
            (students[3].id, jobs[7].id, ApplicationStatus.APPROVED),
            (students[4].id, jobs[3].id, ApplicationStatus.REJECTED),
            (students[6].id, jobs[4].id, ApplicationStatus.PENDING),
            (students[7].id, jobs[5].id, ApplicationStatus.SHORTLISTED),
            (students[9].id, jobs[8].id, ApplicationStatus.PENDING),
            (students[10].id, jobs[0].id, ApplicationStatus.REJECTED),
            (students[11].id, jobs[0].id, ApplicationStatus.APPROVED),
            (students[0].id, jobs[5].id, ApplicationStatus.PENDING),
            (students[1].id, jobs[3].id, ApplicationStatus.PENDING),
        ]

        for s_id, j_id, status in applications_data:
            new_app = Application(
                student_id=s_id,
                job_id=j_id,
                status=status,
                applied_at=datetime.datetime.now() - datetime.timedelta(days=1)
            )
            db.add(new_app)

        db.commit()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed()
