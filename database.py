
from sqlmodel import Field , SQLModel ,Session , select , create_engine
from datetime import datetime

class User(SQLModel , table=True):
    __tablename__ = "users"
    id : int = Field(default=None , primary_key=True)
    username : str = Field(index=True)
    password : str 
    city : str
    first_name : str 
    last_name : str 
    email : str 
    age : int 
    country : str 
    joined_time : str

class Comment(SQLModel , table=True):
    __tablename__ = "comments"
    id : int = Field(default=None , primary_key=True) 
    username : str
    user_id : int = Field(foreign_key="users.id")
    text : str
    time_stamp : datetime = Field(default_factory=datetime.now)




engine = create_engine(url="sqlite:///db/database.db" , echo=True)
SQLModel.metadata.create_all(engine)


def fetch_user(username):
    with Session(engine) as db_session:
        user = select(User).where(User.username == username)
        user = db_session.exec(user).first()
        return user 
    

def fetch_all_users():
    with Session(engine) as db_session :
        users = select(User)
        users = list(db_session.exec(users))
        users_count = Session(engine).query(User).count()
        return users , users_count

def fetch_comments():
    with Session(engine) as db_session :
        comments_and_usernames = select(Comment.username , Comment.text)
        comments_and_usernames = list(db_session.exec(comments_and_usernames))
        return comments_and_usernames
    
def add_user_to_db(username ,  hashed_password ,city , country ,first_name , last_name , email , age , joined_time):
    with Session(engine) as db_session:
        new_user = User(username=username ,password=hashed_password  , city=city, country=country , first_name= first_name , last_name=last_name , email=email , age=age  ,joined_time=joined_time )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)


def add_comment_to_db( user_id , comment , username ):
    with Session(engine) as db_session:
        new_comment = Comment(user_id=user_id ,username=username, text=comment)
        db_session.add(new_comment)
        db_session.commit()
        db_session.refresh(new_comment)


def relative_time_from_string(time_string):
    parsed_time = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()
    time_difference = current_time - parsed_time
    seconds = time_difference.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minutes ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hours ago"
    else:
        days = int(seconds // 86400)
        return f"{days} days ago"