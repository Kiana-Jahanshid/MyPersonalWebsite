from flask import Flask , render_template , request , redirect,session as flask_session, url_for , make_response , flash
from sqlmodel import Field , SQLModel ,Session , select , create_engine 
from pydantic import BaseModel
import bcrypt
from werkzeug.datastructures import MultiDict 



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

class LoginModel(BaseModel):
    username : str
    password : str
    confirm_password : str

class User(SQLModel , table=True):
    id : int = Field(default=None , primary_key=True)
    username : str = Field(index=True)
    password : str 
    city : str
    first_name : str 
    last_name : str 
    email : str 
    age : int 
    country : str 


app = Flask(import_name="__init__" , template_folder="" , static_folder="static")
app.secret_key = "my_secret"

engine = create_engine(url="sqlite:///db/database.db" , echo=True)
SQLModel.metadata.create_all(engine)




@app.route("/")
def root():
    return  render_template("templates/index.html" )


@app.route("/contact")
def contact():
    return render_template("templates/contact.html" )


@app.route("/blog" )
def blog(): 
    if flask_session.get("user_id"):
        return render_template("templates/blog.html" )
    else :
        flash("You have to login, to use blog page ⛔" , "info")
        return redirect(url_for("login"))



@app.route("/register" , methods=["GET","POST"])
def register():
    if request.method == "GET" :
        return  render_template("templates/register.html")
    elif request.method == "POST" :
        try:
            register_data = RegisterModel(username=request.form["username"]  , city= request.form["city"]  ,country= request.form["country"] , first_name= request.form["firstname"] , last_name= request.form["lastname"] , email= request.form["email"] , age= request.form["age"] ,password= request.form['password'], confirm_password= request.form["confirm_password"])#validating attributes type
            # print(register_data)
        except:
            flash("Type Error! One of your input was wrong" , "danger")
            return redirect(url_for("register"))
        if register_data.confirm_password == register_data.password :
            with Session(engine) as db_session : 
                query = select(User).where(User.username ==  request.form["username"] )
                result = db_session.exec(query).first()
            if not result :
                password_byte = register_data.password.encode("utf-8")
                hashed_password = bcrypt.hashpw(password_byte , bcrypt.gensalt())
                with Session(engine) as db_session :
                    new_user = User(username= request.form["username"] ,password=hashed_password , city= request.form["city"] ,country= request.form["country"] , first_name= request.form["firstname"] , last_name= request.form["lastname"] , email= request.form["email"] , age= request.form["age"] ) # create a user object
                    db_session.add(new_user) 
                    db_session.commit()
                    db_session.refresh(new_user)
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
            register_login_data = LoginModel(username= request.form["username"] , password= request.form["password"] , confirm_password= request.form["confirm_password"])# if email & pass types are correct , user will be navigated to upload page
        except:
            flash("type error")
            return  redirect(url_for("login"))
        with Session(engine) as db_session :
            query = select(User).where(User.username == register_login_data.username ) #    User.password == register_login_data.password)
            user = db_session.exec(query).first()
        if  request.form["confirm_password"] ==  request.form["password"] :
            
            if user :
                byte_password = register_login_data.password.encode("utf-8")
                if bcrypt.checkpw(byte_password , user.password):  
                    flask_session["username"]  =  register_login_data.username
                    flash("You logged in successfully 🎉" , "success")
                    flask_session["user_id"] = user.id
                    return redirect(url_for("root")) 
                else:
                    flash("Password is INCORRECT" , "danger")
                    return redirect(url_for("login"))
            else :
                flash("Username is INCORRECT" , "danger")
                return redirect(url_for("login"))
        else :
            flash("Confirm-password doesn't match with password ,Try again ..." , "warning")
            return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if flask_session.get("user_id"):
        flask_session.pop("user_id")
        flash("You logged out successfully" , "success")
        return redirect(url_for("root"))
    else:
        return redirect(url_for("root"))


# HOW TO RUN 
# flask --app app run --debug
