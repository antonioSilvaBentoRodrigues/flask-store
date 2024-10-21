from api import create_app
from database.models import db


if __name__ == '__main__':
    app = create_app()
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)