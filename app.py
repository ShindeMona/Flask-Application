from flask import Flask
from datetime import datetime
from flask import make_response
from flask import request
from flask import Flask, render_template
from flask import abort
from flask import redirect
from flask.ext.bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap=Bootstrap(app)
@app.route('/')
def use():
   return render_template('sample.html',current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name,current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
import yaml

# data configuration
db=yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']= db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']= db['mysql_db']

mysql = MySQL(app)
@app.route('/insert',methods=['GET','POST'])
def index():
      if request.method == 'POST':
        searchDetails=request.form
        search2=searchDetails['search2']
        cur= mysql.connection.cursor()
        cur.execute("INSERT INTO search(search2) VALUES(%s)",(search2,))
        mysql.connection.commit()
        cur.close()
        return redirect('/search')
      return render_template('demo.html')

@app.route('/search')
def search():
       cur= mysql.connection.cursor()
       resultValue=cur.execute("SELECT * FROM search")
       if resultValue > 0:
           data=cur.fetchall()
           return render_template('search.html',data=data)
if __name__ == '__main__':
     app.run(debug=True)
