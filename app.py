from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    Description=db.Column(db.String(100),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)


@app.route('/',methods=['GET','POST'])
def adding_todo():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['Description']
        todo=Todo(title=title,Description=desc)
        if((len(title)==0) or(len(desc)==0)): #avoiding null entries
            return render_template("error.html")
        else: #if record entered is not null then that todo is entered into database
            db.session.add(todo)
            db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete_todo(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update_todo(sno):
    if(request.method=='POST'):
        title=request.form['title']
        Description=request.form['Description']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.Description=Description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)