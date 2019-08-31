from flask import Flask
from flask import jsonify, render_template, request
import requests, json
from flask_sqlalchemy import SQLAlchemy
import flask_excel as excel


app = Flask(__name__)

excel.init_excel(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Transcendental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    Key = db.Column(db.String(50), nullable=False)
    Description = db.Column(db.String(2000), nullable=True)
    Video = db.Column(db.String(100), nullable=True)

class Composition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    composition_name = db.Column(db.String(80), nullable=False)
    composer = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(2000), nullable=True)
    vidlink = db.Column(db.String(100), nullable=True)
    # TODO: Add more entries here (hint: columns)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(1000), nullable=False)

db.create_all()

@app.route("/comments", methods=["GET"])
def inputcomment():
    dict_comments = []
    for comment in Comments.query.all():
        dict_comments.append(comment.__dict__)
    return render_template('comments.html', comments = dict_comments)


@app.route("/comments", methods=["POST"])
def commenting():
    email = request.form['email']
    username = request.form['username']
    comment = request.form['comment']
    print(username)


    comment1 = Comments(username = username, email = email, comment = comment)
    db.session.add(comment1)
    db.session.commit()

    
    return json.dumps({'status': 'Comment Successful'})

@app.route("/comments/delete", methods=["POST"])
def commentDelete():
    comment_id = request.form['comment_id']
    # Search for the comment
    delete_comment = Comments.query.filter_by(id=comment_id).first()
    # Delete the comment
    db.session.delete(delete_comment)
    # Save the Database
    db.session.commit()
    
    return json.dumps({'status': 'Comment Deleted'});

@app.route('/import', methods=['GET', 'POST'])
def do_import():
    # Clean Database and recreate database
    Composition.query.delete()

    if request.method == "POST":
        def init_func(row):
            composition = Composition(
                row['composition_name'], row['composer'], row['description'], row['vidlink']
                )
            composition.id = row['id']
            return composition
        request.save_to_database(
            field_name='file', session=db.session, table=Composition, initializers=[init_func])
                  

                  

    return'''
      <!doctype html>
      <title>Upload an excel file</title>
      <a href="javascript:history.back()">Go Back</a>
      <h1>Excel file upload (xls, xlsx, ods please)</h1>
      <form action="" method=post enctype=multipart/form-data> <p>
        <input type=file name=file><input type=submit value=Upload>
      </form>
'''




def __repr__(self):
    return '<Composition ' + self.composition_name + '>'

Liszt_Etudes = [
    {
        "Set": "Transcendental",
        "Etudes": ["Preludio in C major", "Fusees in A minor", "Paysage in F major", "Mazeppa in D minor", "Feux Follets in B flat Major","Vision G minor","Eroica E flat Major","Wilde Jagd in C minor","Ricordanza in A flat Major","Appassionata in F minor","Harmonies du Soir in D-flat Major","Chasse-niege in B-flat minor"]
    },
        
    {
        "Set": "Paganini",
        "Etudes": ["1 - based on N. Paganini's 5th and 6th caprices", "2 - based on Niccolo Paganini's 17th caprice", "3 - La campanella, based on Paganini's concerto in B minor", "4 - based on N. Paganini's 1st Caprice","5 - based on N. Paganini's 9th caprice","6 - based on N. Paganini's 24th caprice"]
    }  

]


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/compositions/etudes')
def compositionsetudes():
    return render_template('compositionsetudes.html', Liszt_Etudes = Liszt_Etudes)

@app.route('/compositions')
def compositions():
    #return render_template('compositions.html')
    dict_compositions = []
    for composition in Composition.query.all():
        dict_compositions.append(composition.__dict__)
    return render_template('compositions.html', compositions=dict_compositions)



@app.route('/biography')
def biography():
    return render_template('biography.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/transcendental/import', methods=['GET', 'POST'])
def do_import_transcendental():
    # Clean Database and recreate database
    Transcendental.query.delete()

    if request.method == "POST":
        def init_func(row):
            transcendental = Transcendental(
                row['id'], row['name'], row['Key'], row['Description'], row['Video']
                )
            transcendental.id = row['id']
            return transcendental
        request.save_to_database(
            field_name='file', session=db.session, table=Transcendental, initializers=[init_func])
    return'''
        <!doctype html>
        <title>Upload an excel file</title>
        <a href="javascript:history.back()">Go Back</a>
        <h1>Excel file upload (xls, xlsx, ods please)</h1>
        <form action="" method=post enctype=multipart/form-data> <p>
            <input type=file name=file><input type=submit value=Upload>
        </form>
    '''


def __repr__(self):
    return '<Transcendental ' + self.name + '>'

@app.route('/compositions/etudes/transcendental')
def transcendentaletudes():
    dict_transcendental = []
    for transcendental in Transcendental.query.all():
        dict_transcendental.append(transcendental.__dict__)
    return render_template('transcendental.html', Transcendentals=dict_transcendental)


if __name__ =="__main__":
  app.run(debug=True,port=5000)