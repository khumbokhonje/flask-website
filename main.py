from journal import create_app
from notes import create_note_app

noteapp = create_note_app()
app = create_app()

if __name__ == "__main__":
    # app.run(debug=True)
    noteapp.run(debug=True)

