from app import create_app
from extensions import db
from models import User

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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()

    app.run(debug=True)
