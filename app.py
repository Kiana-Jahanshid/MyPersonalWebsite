from flask import Flask , render_template , request , redirect,session as flask_session, url_for , make_response , flash
from pydantic import BaseModel
import bcrypt
from datetime import datetime
import json
from database import fetch_all_users , fetch_user , fetch_comments , add_comment_to_db , add_user_to_db , relative_time_from_string

class RegisterModel(BaseModel):
    username : str 
    password : str
    city : str
    country : str
    first_name : str
    last_name : str
    email : str
    age : int 
    confirm_password : str
    joined_time : str

class LoginModel(BaseModel):
    username : str
    password : str

class CommentsModel(BaseModel):
    username : str
    user_id : int 
    comment : str



app = Flask(import_name="__init__" , template_folder="" , static_folder="static")
app.secret_key = "my_secret"



@app.route("/")
def root():
    return  render_template("templates/index.html" )


@app.route("/contact")
def contact():
    return render_template("templates/contact.html" )


@app.route("/blog" )
def blog(): 
    if flask_session.get("user_id"):
        all_comments = fetch_comments()
        return render_template("templates/blog.html"  , all_comments=all_comments)
    else :
        flash("You have to login, to use blog page ⛔" , "info")
        return redirect(url_for("login"))



@app.route("/register" , methods=["GET","POST"])
def register():
    if request.method == "GET" :
        return  render_template("templates/register.html")
    elif request.method == "POST" :
        try:
            register_data = RegisterModel(username=request.form["username"]  , city= request.form["city"]  ,country= request.form["country"] , first_name= request.form["firstname"] , last_name= request.form["lastname"] , email= request.form["email"] , age= request.form["age"] ,password= request.form['password'], confirm_password= request.form["confirm_password"] , joined_time=str(datetime.now()))#validating attributes type
            # print(register_data)
        except:
            flash("Type Error! One of your input was wrong" , "danger")
            return redirect(url_for("register"))
        if register_data.confirm_password == register_data.password :
            user = fetch_user(register_data.username)
            if not user :
                password_byte = register_data.password.encode("utf-8")
                hashed_password = bcrypt.hashpw(password_byte , bcrypt.gensalt())
                add_user_to_db(register_data.username ,  hashed_password , register_data.city , register_data.country , register_data.first_name , register_data.last_name , register_data.email , register_data.age , register_data.joined_time)
                flash("your registration compleated successfully🎉" , "success")
                return  redirect(url_for("login"))
            else:
                flash("This username is already taken ❌,Choose another one" , "danger")
                return  redirect(url_for("register"))
        else :
            flash("confirm-password doesnt match with password ❌, try again ... " , "warning")
            return  redirect(url_for("register"))



@app.route("/login" , methods=["GET" , "POST"]) 
def login():
    if request.method == "GET" :
        return  render_template("templates/login.html")
    elif request.method == "POST" : 
        try :            
            register_login_data = LoginModel(username= request.form["username"] , password= request.form["password"])# if email & pass types are correct , user will be navigated to upload page
        except:
            flash("type error")
            return  redirect(url_for("login"))
        user = fetch_user(register_login_data.username)
        if user :
            byte_password = register_login_data.password.encode("utf-8")
            if bcrypt.checkpw(byte_password , user.password ):  
                flask_session["username"]  =  register_login_data.username
                flask_session["user_id"] = user.id
                flash("You logged in successfully 🎉" , "success")
                return redirect(url_for("root")) 
            else:
                flash("Password is INCORRECT ❌" , "danger")
                return redirect(url_for("login"))
        else :
            flash("Username is INCORRECT ❌" , "danger")
            return redirect(url_for("login"))
            

@app.route("/logout")
def logout():
    if flask_session.get("user_id"):
        flask_session.pop("user_id")
        flash("You logged out successfully" , "success")
        return redirect(url_for("root"))
    else:
        flash("You are not not logged in yet ! " , "warning")
        render_template("templates/index.html")


@app.route("/admin" , methods=["GET" , "POST"])
def pannel_admin():
    if flask_session.get("user_id"):
        users , user_count = fetch_all_users()
        for user in users :
            joined_time = str(user.joined_time)
            parsed_time = datetime.strptime(joined_time, '%Y-%m-%d %H:%M:%S.%f')
            formatted_time = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
            user.joined_time = relative_time_from_string(formatted_time)  
        comments = fetch_comments()
        return  render_template("templates/admin.html" , username= flask_session.get("username") , users=users , user_count=user_count , comments=comments)
    else :
        flash("first login to website to access admin pannel ⛔")
        return redirect(url_for("login"))


@app.route("/add_comment" , methods=["POST"])
def comments():
    if flask_session.get("user_id") :
        comment = request.form["text"]
        comment_model = CommentsModel(username=flask_session.get("username") , user_id=flask_session.get("user_id") , comment=comment)
        comment = comment[3:-4]
        add_comment_to_db(comment_model.user_id , comment_model.username , comment)
        return redirect(url_for("blog"))
    else :
        flash("first you have to login ⛔" , "danger")
        return redirect(url_for("login"))


@app.route("/api" , methods=["GET" ,"POST"])
def send_personal_info():
    info = {"Fisrtname" : "kiana",
            "lastname"  : "jahanshid",
            "job" : "programmer to be ", 
            "age" : "30" , 
            "degree" : "master of science"}
    jsonformat = json.dumps(info , indent=1)
    jsonformat = json.loads(jsonformat)
    return render_template("templates/info.html" , json=jsonformat)




# HOW TO RUN 
# flask --app app run --debug

