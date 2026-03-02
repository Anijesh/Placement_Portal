from app import create_app
from extensions import db
from models import User,Branch

app = create_app()

def create_admin():
    admin_email= 'admin@example.com'
    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin = User(
            email=admin_email,
            role="admin"
        )
        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully")
    else:
        print("Admin already exists")

def create_branch():
    default_branches = ['CSE','ECE','EEE','MECH','CIVIL',]
    for branch_name in default_branches:
        existing_branch = Branch.query.filter_by(name=branch_name).first()
        if not existing_branch:
            branch=Branch(name=branch_name)
            db.session.add(branch)
    db.session.commit()
    print("Default branch created")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
        create_branch()

    app.run(debug=True)
