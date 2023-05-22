from flask import Flask, render_template
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager()

posts = []


@app.route("/")
def index():
    return render_template("index.html", num_posts=len(posts))


if __name__ == '__main__':
    app.run()
