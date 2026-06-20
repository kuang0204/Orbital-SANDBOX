import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import SkillTag, JobListing, ApplicationOutcome, Profile, Alumni


def seed():
    print("Clearing existing data...")
    ApplicationOutcome.objects.all().delete()
    JobListing.objects.all().delete()
    SkillTag.objects.all().delete()
    Profile.objects.all().delete()
    Alumni.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    print("Creating skill tags...")
    skills_data = [
        ('Python', 'Language'),
        ('JavaScript', 'Language'),
        ('TypeScript', 'Language'),
        ('Java', 'Language'),
        ('C++', 'Language'),
        ('Go', 'Language'),
        ('SQL', 'Database'),
        ('PostgreSQL', 'Database'),
        ('MongoDB', 'Database'),
        ('React', 'Frontend'),
        ('Vue.js', 'Frontend'),
        ('Angular', 'Frontend'),
        ('HTML/CSS', 'Frontend'),
        ('Tailwind CSS', 'Frontend'),
        ('Node.js', 'Backend'),
        ('Django', 'Backend'),
        ('Flask', 'Backend'),
        ('Spring Boot', 'Backend'),
        ('Express.js', 'Backend'),
        ('Docker', 'DevOps'),
        ('Kubernetes', 'DevOps'),
        ('AWS', 'Cloud'),
        ('GCP', 'Cloud'),
        ('Azure', 'Cloud'),
        ('Git', 'Tools'),
        ('Linux', 'Tools'),
        ('REST API', 'Backend'),
        ('GraphQL', 'Backend'),
        ('Machine Learning', 'AI/ML'),
        ('Deep Learning', 'AI/ML'),
        ('TensorFlow', 'AI/ML'),
        ('PyTorch', 'AI/ML'),
        ('Data Analysis', 'Data'),
        ('Data Visualization', 'Data'),
        ('Tableau', 'Data'),
        ('Figma', 'Design'),
        ('UI/UX Design', 'Design'),
        ('Agile/Scrum', 'Process'),
        ('Product Management', 'Process'),
        ('Communication', 'Soft Skill'),
        ('Leadership', 'Soft Skill'),
        ('Problem Solving', 'Soft Skill'),
    ]
    skills = {}
    for name, category in skills_data:
        skill, _ = SkillTag.objects.get_or_create(name=name, category=category)
        skills[name] = skill
    print(f"  Created {SkillTag.objects.count()} skill tags")

    print("Creating demo users...")
    demo_user = User.objects.create_user(username='alice', email='alice@u.nus.edu', password='password123')
    Profile.objects.create(
        user=demo_user,
        faculty='SOC',
        major='Computer Science',
        year_of_study='3',
        gpa_range='3.5-4.0',
        experiences='SWE Intern at Shopee (2025)\nTeaching Assistant for CS1101S',
        projects='NUSHire - Orbital project\nPersonal portfolio website',
        portfolio_links='https://github.com/alice',
    )
    demo_user.profile.skills.add(
        skills['Python'], skills['JavaScript'], skills['React'], skills['Django'],
        skills['SQL'], skills['Git'], skills['AWS'], skills['Docker'],
        skills['TypeScript'], skills['Node.js'], skills['REST API']
    )

    demo_user2 = User.objects.create_user(username='bob', email='bob@u.nus.edu', password='password123')
    Profile.objects.create(
        user=demo_user2,
        faculty='SOC',
        major='Computer Science',
        year_of_study='2',
        gpa_range='3.0-3.5',
        experiences='Summer internship at a startup\nHackathon participant',
        projects='Task management app\nE-commerce website',
        portfolio_links='https://github.com/bob',
    )
    demo_user2.profile.skills.add(
        skills['Python'], skills['Java'], skills['SQL'], skills['Git'],
        skills['Linux'], skills['HTML/CSS'], skills['Problem Solving']
    )

    print("Creating job listings...")
    jobs_data = [
        {
            'company': 'Google',
            'role': 'Software Engineering Intern 2026',
            'description': 'Work on real-world projects that impact billions of users. As a Software Engineering Intern at Google, you will work on a specific project critical to Google\'s needs with opportunities to switch teams and projects. You will be matched to a team based on your skills and interests.',
            'application_link': 'https://careers.google.com/jobs/',
            'deadline': '2026-09-30',
            'role_type': 'SWE',
            'required_skills': ['Python', 'Java', 'C++', 'Data Structures', 'Algorithms', 'Git', 'Problem Solving'],
        },
        {
            'company': 'Meta',
            'role': 'Frontend Engineering Intern',
            'description': 'Join Meta\'s frontend team to build and improve user-facing features used by billions. You will work with React, GraphQL, and cutting-edge web technologies to deliver seamless experiences across Meta\'s family of apps.',
            'application_link': 'https://www.metacareers.com/jobs/',
            'deadline': '2026-08-15',
            'role_type': 'SWE',
            'required_skills': ['JavaScript', 'TypeScript', 'React', 'GraphQL', 'HTML/CSS', 'REST API', 'Git'],
        },
        {
            'company': 'Shopee',
            'role': 'Data Science Intern',
            'description': 'Analyze large-scale e-commerce data to derive actionable insights. You will work closely with product and engineering teams to design experiments, build dashboards, and develop machine learning models to improve user experience and business metrics.',
            'application_link': 'https://careers.shopee.sg/',
            'deadline': '2026-07-31',
            'role_type': 'DS',
            'required_skills': ['Python', 'SQL', 'Machine Learning', 'Data Analysis', 'Data Visualization', 'Tableau'],
        },
        {
            'company': 'ByteDance',
            'role': 'Backend Engineering Intern',
            'description': 'Build and maintain high-performance distributed systems powering TikTok and other ByteDance products. You will design scalable APIs, optimize database queries, and work on real-time data processing pipelines.',
            'application_link': 'https://jobs.bytedance.com/',
            'deadline': '2026-08-31',
            'role_type': 'SWE',
            'required_skills': ['Python', 'Go', 'SQL', 'PostgreSQL', 'Docker', 'REST API', 'Redis'],
        },
        {
            'company': 'GovTech',
            'role': 'Product Management Intern',
            'description': 'Drive digital transformation for Singapore\'s government services. You will work with cross-functional teams to define product roadmaps, gather user requirements, and deliver impactful solutions that serve millions of Singaporeans.',
            'application_link': 'https://www.govtechcareers.sg/',
            'deadline': '2026-06-30',
            'role_type': 'PM',
            'required_skills': ['Product Management', 'Agile/Scrum', 'Communication', 'Data Analysis', 'UI/UX Design', 'Leadership'],
        },
        {
            'company': 'Grab',
            'role': 'Software Engineering Intern',
            'description': 'Build solutions that power Southeast Asia\'s superapp. You\'ll work on backend services, mobile features, or data pipelines that serve millions of users across the region in ride-hailing, food delivery, and financial services.',
            'application_link': 'https://grab.careers/',
            'deadline': '2026-07-15',
            'role_type': 'SWE',
            'required_skills': ['Python', 'JavaScript', 'SQL', 'AWS', 'Docker', 'REST API', 'Git'],
        },
        {
            'company': 'DBS Bank',
            'role': 'Technology Intern',
            'description': 'Join DBS\'s technology team to work on digital banking solutions. You will be involved in developing and maintaining banking applications, learning about financial technology, and contributing to real projects that impact millions of customers.',
            'application_link': 'https://www.dbs.com/careers/',
            'deadline': '2026-07-01',
            'role_type': 'SWE',
            'required_skills': ['Java', 'SQL', 'Python', 'Git', 'Agile/Scrum', 'Problem Solving'],
        },
        {
            'company': 'Apple',
            'role': 'UI/UX Design Intern',
            'description': 'Design world-class user experiences for Apple\'s products and services. You will collaborate with engineers, product managers, and other designers to create intuitive and beautiful interfaces that delight users worldwide.',
            'application_link': 'https://jobs.apple.com/',
            'deadline': '2026-09-15',
            'role_type': 'UIUX',
            'required_skills': ['Figma', 'UI/UX Design', 'HTML/CSS', 'JavaScript', 'Communication', 'Problem Solving'],
        },
    ]
    for jd in jobs_data:
        required = jd.pop('required_skills')
        job = JobListing.objects.create(**jd)
        for skill_name in required:
            if skill_name in skills:
                job.required_skills.add(skills[skill_name])
    print(f"  Created {JobListing.objects.count()} job listings")

    print("Creating sample outcomes...")
    jobs = JobListing.objects.all()
    alice = User.objects.get(username='alice')
    bob = User.objects.get(username='bob')
    ApplicationOutcome.objects.create(
        user=alice, job=jobs[0], status='offer',
        channel='portal', interview_format='online',
        timeline='Applied Aug, Interview Sep, Offer Oct',
        notes='LeetCode practice was essential'
    )
    ApplicationOutcome.objects.create(
        user=bob, job=jobs[2], status='rejection',
        channel='linkedin', interview_format='online',
        timeline='Applied Jul, Rejected Aug',
        notes='Should have prepared more SQL questions'
    )
    print("  Created sample outcomes")

    print("Creating alumni...")
    # Matched to seeded companies by name (JobDetailSerializer filters company__iexact).
    alumni_data = [
        # Google
        {
            'name': 'Rachel Tan',
            'linkedin_url': 'https://www.linkedin.com/in/rachel-tan-nus/',
            'email': 'rachel.tan@alumni.nus.edu.sg',
            'company': 'Google',
            'current_role': 'Software Engineer, Search',
            'graduation_year': 2022,
            'faculty': 'SOC',
        },
        {
            'name': 'Marcus Lim',
            'linkedin_url': 'https://www.linkedin.com/in/marcus-lim-swe/',
            'email': 'marcus.lim@alumni.nus.edu.sg',
            'company': 'Google',
            'current_role': 'Senior Software Engineer',
            'graduation_year': 2019,
            'faculty': 'SOC',
        },
        # Meta
        {
            'name': 'Priya Nair',
            'linkedin_url': 'https://www.linkedin.com/in/priya-nair-frontend/',
            'email': 'priya.nair@alumni.nus.edu.sg',
            'company': 'Meta',
            'current_role': 'Frontend Engineer, React',
            'graduation_year': 2021,
            'faculty': 'SOC',
        },
        {
            'name': 'Daniel Wong',
            'linkedin_url': 'https://www.linkedin.com/in/daniel-wong-meta/',
            'email': 'daniel.wong@alumni.nus.edu.sg',
            'company': 'Meta',
            'current_role': 'Product Designer',
            'graduation_year': 2020,
            'faculty': 'ENG',
        },
        # Shopee
        {
            'name': 'Chloe Sim',
            'linkedin_url': 'https://www.linkedin.com/in/chloe-sim-data/',
            'email': 'chloe.sim@alumni.nus.edu.sg',
            'company': 'Shopee',
            'current_role': 'Data Scientist',
            'graduation_year': 2023,
            'faculty': 'SCI',
        },
        {
            'name': 'Arjun Mehta',
            'linkedin_url': 'https://www.linkedin.com/in/arjun-mehta-ds/',
            'email': 'arjun.mehta@alumni.nus.edu.sg',
            'company': 'Shopee',
            'current_role': 'Machine Learning Engineer',
            'graduation_year': 2021,
            'faculty': 'SOC',
        },
        # Grab
        {
            'name': 'Nurul Aisyah',
            'linkedin_url': 'https://www.linkedin.com/in/nurul-aisyah-grab/',
            'email': 'nurul.aisyah@alumni.nus.edu.sg',
            'company': 'Grab',
            'current_role': 'Backend Engineer, Payments',
            'graduation_year': 2022,
            'faculty': 'SOC',
        },
        {
            'name': 'Kevin Teo',
            'linkedin_url': 'https://www.linkedin.com/in/kevin-teo-grab/',
            'email': 'kevin.teo@alumni.nus.edu.sg',
            'company': 'Grab',
            'current_role': 'Engineering Manager',
            'graduation_year': 2017,
            'faculty': 'ENG',
        },
    ]
    for ad in alumni_data:
        Alumni.objects.create(**ad)
    print(f"  Created {Alumni.objects.count()} alumni")

    print("\nSeed completed successfully!")
    print(f"  Users: {User.objects.filter(is_superuser=False).count()}")
    print(f"  Skills: {SkillTag.objects.count()}")
    print(f"  Jobs: {JobListing.objects.count()}")
    print(f"  Outcomes: {ApplicationOutcome.objects.count()}")
    print(f"  Alumni: {Alumni.objects.count()}")
    print(f"\nDemo accounts:")
    print(f"  alice / password123 (has SWE skills)")
    print(f"  bob / password123 (has basic skills)")


if __name__ == '__main__':
    seed()
