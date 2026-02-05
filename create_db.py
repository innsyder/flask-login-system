from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    print("Database created")

    hashed_pw = generate_password_hash("secret123")
    user = User(username="admin", password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()

    print("User added: admin / secret123")