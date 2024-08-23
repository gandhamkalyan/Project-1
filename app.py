from flask import Flask,render_template,request
import sqlite3
import pickle



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact',methods = ['POST','GET'])
def contactus():
    if request.method == 'POST':
        name = request.form.get('name')
        ph_no = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        conn = sqlite3.connect('YTDatabase.db')
        cur = conn.cursor()

        cur.execute(f'''
INSERT INTO CONTACT VALUES("{name}",{ph_no},"{email}","{address}")
                    ''')
        
        conn.commit()
        return render_template('greetings.html')
        
    else:
        return render_template('contactus.html')
    

@app.route('/analytical')
def analytical():
    return render_template('analytical.html')

@app.route('/predictor',methods = ['GET','POST'])
def like_predictor():
    if request.method == 'POST':
        views = request.form.get('views')
        dislike = request.form.get('dislikes')
        comment = request.form.get('comments')
        genre = request.form.get('genre')

        with open('model.pickle', 'rb') as model_file:
            model = pickle.load(model_file)

        pred = model.predict([[float(views),float(dislike),float(comment),float(genre)]])
        return render_template('result.html',pred = str(round(pred[0])))

    else:
        return render_template('likepredictor.html')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5055)