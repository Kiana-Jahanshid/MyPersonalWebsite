from flask import Flask , render_template , request

app = Flask(import_name="__init__" , template_folder="" , static_folder="static")


# here our GOAL is to design a website
# so we have to return HTML format ( not json and etc ....)
@app.route("/")
def root():
    name = "kiki"
    x="8"
    return  render_template("templates/index.html" , name=name , x=x)


@app.route("/contact")
def contact():
    x = 20
    return render_template("templates/contact.html" , x=x)


@app.route("/blog" )
def blog():
    x=9 
    return render_template("templates/blog.html" , x=x)

@app.route("/login")
def login():
    x= 0
    return render_template("templates/login.html" , x=x )



# HOW TO RUN 
# flask --app init run --debug


# put html files in templates folder


# create virtual environmets :
'''
> mkdir myproject
> cd myproject
> py -3 -m venv .venv
> .venv/Scripts/activate
$ pip install Flask

'''


# because LIARA supports flask , SO we dont need to write Dockerfile
# https://docs.liara.ir/cicd/github/