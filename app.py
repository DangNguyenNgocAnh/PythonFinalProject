from logging import debug
from Website import create_app
from flask import Flask, render_template

app = create_app()
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)