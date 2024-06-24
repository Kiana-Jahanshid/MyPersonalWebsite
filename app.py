from flask import Flask , render_template , request , redirect,session , url_for , make_response
from sqlmodel import Field , SQLModel ,Session , select , create_engine 
from pydantic import BaseModel
import bcrypt
import time
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

engine = create_engine(url="sqlite:///./database.db" , echo=True)
SQLModel.metadata.create_all(engine)



def auth(email , password):
    # if email == "k.jhnshid@gmail.com" and password == "1234" :
    #     return True
    # else :
    #     return False
    return True



@app.route("/")
def root():
    return  render_template("templates/index.html" )


@app.route("/contact")
def contact():
    return render_template("templates/contact.html" )


@app.route("/blog" )
def blog(): 
    return render_template("templates/blog.html" )



@app.route("/register" , methods=["GET","POST"])
def register():
    if request.method == "GET" :
        return  render_template("templates/register.html")
    elif request.method == "POST" :
        try:
            register_data = RegisterModel(username=request.form["username"]  , city= request.form["city"]  ,country= request.form["country"] , first_name= request.form["firstname"] , last_name= request.form["lastname"] , email= request.form["email"] , age= request.form["age"] ,password= request.form['password'], confirm_password= request.form["confirm_password"])#validating attributes type
            print(register_data)
            print(request.form["username"])
        except:
            print("type error")
            return redirect(url_for("register"))
        if register_data.confirm_password == register_data.password :
            joined_time = time.time()
            print(joined_time)
            with Session(engine) as db_session : 
                query = select(User).where(User.username ==  request.form["username"] )
                result = db_session.exec(query).first()
            if not result :
                print(register_data.password)
                password_byte = register_data.password.encode("utf-8")
                hashed_password = bcrypt.hashpw(password_byte , bcrypt.gensalt())
                print(hashed_password)
                with Session(engine) as db_session :
                    new_user = User(username= request.form["username"] ,password=hashed_password , city= request.form["city"] ,country= request.form["country"] , first_name= request.form["firstname"] , last_name= request.form["lastname"] , email= request.form["email"] , age= request.form["age"] ) # create a user object
                    db_session.add(new_user) 
                    db_session.commit()
                    db_session.refresh(new_user)
                    print("your registration compleated successfully🎉")
                    return  redirect(url_for("login"))
            else:
                print("This username is already taken , choose another one")
                return  redirect(url_for("register"))
        else :
            print("confirm password doesnt match with password , try again ... ")
            return  redirect(url_for("register"))



@app.route("/login" , methods=["GET" , "POST"]) 
def login():
    if request.method == "GET" :
        return  render_template("templates/login.html")
    elif request.method == "POST" : 
        try :            
            register_login_data = LoginModel(username= request.form["username"] , password= request.form["password"] , confirm_password= request.form["confirm_password"])# if email & pass types are correct , user will be navigated to upload page
        except:
            print("type error")
            return  redirect(url_for("login"))
        with Session(engine) as db_session :
            query = select(User).where(User.username == register_login_data.username ) #    User.password == register_login_data.password)
            result = db_session.exec(query).first()
        if  request.form["confirm_password"] ==  request.form["password"] :
            
            if result :
                byte_password = register_login_data.password.encode("utf-8")
                if bcrypt.checkpw(byte_password , result.password):  
                    session["username"]  =  register_login_data.username
                    print("you logged in successfully 🎉")
                    return redirect(url_for("root")) 
                else:
                    print("password is incorrect")
                    return redirect(url_for("login"))
            else :
                print("username is incorrect")
                return redirect(url_for("login"))
        else :
            print("confirm password doesnt match with password , try again ... ")
            return redirect(url_for("login"))







# HOW TO RUN 
# flask --app app run --debug
