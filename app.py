from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import validators

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "askldhjas$#@s;adllfju12312!@#123"
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"])

@app.route('/')
def index():
    if 'username' in session:
        if session['username'] == 'admin':
            return list(db.get_all_users(connection))
        else:
            return render_template("index.html", gadgets=db.get_all_gadgets(connection))
    return "You are not logged in."

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute") 
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, username)
        
        if user:
            if utils.is_password_match(password, user[2]):
                session['username'] = user[1]
                session['user_id'] = user[0]
                return redirect(url_for('index'))
            else:
                flash("Password dose not match", "danger")
                return render_template('login.html')
            
        else:
            flash("Invalid username", "danger")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per minute") 
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not utils.is_strong_password(password):
            flash("Sorry You Entered a weak Password Please Choose a stronger one", "danger")
            return render_template('register.html')
        
        user = db.get_user(connection, username)
        if user:
            flash("Username already exists. Please choose a different username.", "danger")
            return render_template('register.html')
        else:
            db.add_user(connection, username, password)
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/upload-gadget', methods=['GET', 'POST'])
@limiter.limit("10 per minute") 
def uploadGadget():
    if not 'user_id' in session:
        flash("Please Login to do this action", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        gadgetImage = request.files['image']
        if not gadgetImage or gadgetImage.filename == '':
            flash("Image Is Required", "danger")
            return render_template("upload-gadget.html")

        if validators.allowed_file(gadgetImage.filename) or not validators.allowed_file_size(gadgetImage):
            flash("Invalid File is Uploaded", "danger")
            return render_template("upload-gadget.html")

        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
    
        image_url = f"uploads/{gadgetImage.filename}"
        gadgetImage.save("static/" + image_url)
        user_id = session['user_id']
        db.add_gadget(connection, user_id, title, description, price, image_url)
        return redirect(url_for('index'))
    return render_template('upload-gadget.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.init_db(connection)
    db.seed_admin_user(connection)
    db.init_gadget_table(connection)
    app.run(debug=True)
