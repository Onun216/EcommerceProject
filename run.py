from infortech import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
        app.run(host='localhost', port=8080, debug=True)
