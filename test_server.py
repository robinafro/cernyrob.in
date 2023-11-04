from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth/', methods=['POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # You can now process the `username` and `password` as needed
        # Perform authentication or any other actions you want

        if username == 'your_username' and password == 'your_password':
            return 'OK'  # Successful login
        else:
            return 'Incorrect username or password.', 401

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/clicker/')
def clicker():
    return render_template('clicker.html')

if __name__ == '__main__':
    app.run(debug=True)