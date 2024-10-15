from flask import Flask,render_template,request,session
from flask_session import Session
from User import User
from Database import Database
from Contacts import Contacts

app = Flask(__name__)
app.secret_key = 'encrypted'
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

@app.route('/')
def route():
    return render_template("home.html")

@app.route('/profile')
def profile():
    if session.get('email') is not None:
        email = session['email']
    return render_template("Profile.html",email=email)


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/login_form', methods=['POST'])
def login_form():
    email = request.form['email']
    password = request.form['password']

    u = User(email,password)
    con = Database("localhost","root","Test@123","AddressBook")
    call = con.user_login(u)

    if call:
        session["email"] = email
        return render_template("Profile.html", email=email)
    else:
        return render_template("login.html", msg="Try Again !")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register_form', methods=['POST'])
def register_form():
    email = request.form['email']
    password = request.form['password']

    u = User(email,password)
    con = Database("localhost","root","Test@123","AddressBook")
    call = con.user_register(u)

    if call:
        session['email'] = email
        return render_template("login.html", email=email)
    else:
        return render_template("register.html", msg="Try Again !")


@app.route("/displaycontact")
def display():
    if session.get("email") is not None:
        email = session['email']
        con = Database("localhost", "root", "Test@123", "AddressBook")
        call = con.display_contacts(email)

        if call:
            contacts = call
            return render_template("display.html",contacts=contacts)
        else:
            return render_template("display.html", msg="Error in getting contacts")


@app.route("/addcontact")
def addcontact():
    return render_template("addcontact.html")

@app.route("/addcontact_form", methods=["POST"])
def addcontact_form():
    if session.get("email") is not None:
        email = session['email']
        name = request.form['name']
        mobile = request.form['mobile']
        city = request.form['city']

        con = Database("localhost", "root", "Test@123", "AddressBook")
        c = Contacts(name, mobile, city)
        call = con.add_contact(email,c)

        if call:
            return render_template("addcontact.html",msg="Contact successfully added")
        else:
            return render_template("addcontact.html",msg="Contact not added")


@app.route("/deletecontact")
def delete():
    if session.get("email") is not None:
        email = session['email']
        con = Database("localhost", "root", "Test@123", "AddressBook")
        call = con.display_contacts(email)

        if call:
            contacts = call
            session["contacts"] = contacts
            return render_template("delete.html", contacts=contacts)
        else:
            return render_template("delete.html", msg="Error in getting contacts")

@app.route("/deletecontact_form", methods=['POST'])
def delete_form():
    if session.get("email") is not None:
        email = session['email']
        name = request.form['name']
        mobile = request.form['mobile']
        city = request.form['city']
        c = Contacts(name,mobile,city)
        con = Database("localhost", "root", "Test@123", "AddressBook")
        call = con.delete_contact(email,c)

        if call:
            return render_template("Profile.html", name=name, msg="Record has been deleted")
        else:
            return render_template("Profile.html", name=name, msg="record has not been deleted")


@app.route("/searchcontact")
def search():
    return render_template("search.html")

@app.route("/searchname",methods=["POST"])
def Searching():
    if session.get("email") is not None:

        email = session["email"]
        sub_str = request.form['string']

        con = Database("localhost", "root", "Test@123", "AddressBook")
        call = con.search_name(email)

        if call:
            contacts = call
            results = []
            for sub_list in contacts:
                sublist_contains_substring = any(sub_str in element for element in sub_list)
                if sublist_contains_substring:
                    results.append(sub_list)
            return render_template("results.html", contacts=results)
        else:
            return render_template("results.html", msg="Error in getting contacts")


@app.route("/updatecontact",methods=["POST"])
def update():
    if session.get("email") is not None:
        email = session["email"]
        name = request.form["name"]
        mobile = request.form["mobile"]
        city = request.form["city"]
        session["name"] = name
    return render_template("update.html",name=name,mobile=mobile,city=city)

@app.route("/update_form",methods=["POST"])
def updating():
    if session.get("email") and session.get("name") is not None:
        email = session["email"]
        ex_name = session["name"]

        name = request.form["name"]
        mobile = request.form["mobile"]
        city = request.form["city"]

        c = Contacts(name,mobile,city)
        con = Database("localhost", "root", "Test@123", "AddressBook")
        call = con.update(ex_name,email,c)

        if call:
            return render_template("update.html",msg="Contact Updated")
        else:
            return render_template("update.html",msg="Contact not updated")


@app.route("/logout")
def logout():
    try:
        session.clear()
        return render_template("login.html")
    except Exception as e:
        return render_template("login.html", msg=str(e))


if __name__ == "__main__":
    app.run()
