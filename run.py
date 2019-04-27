# from app import create_app
#
#
# app = create_app()
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


from app import db, create_app

app = create_app()
db.create_all(app=create_app())


if __name__ == '__main__':
    app.run(debug=True)
