from flask import Flask,render_template,request
import pickle
import numpy as np
top50=pickle.load(open(r'C:\Users\sarav\Downloads\top50.pkl','rb'))
pt=pickle.load(open(r'C:\Users\sarav\Downloads\pivot.pkl','rb'))
books=pickle.load(open(r'C:\Users\sarav\Downloads\books.pkl','rb'))
cosine_sim=pickle.load(open(r'C:\Users\sarav\Downloads\cosine_sim.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',book_name=list(top50['Book-Title'].values),
                            author=list(top50['Book-Author'].values),
                            image=list(top50['Image-URL-M'].values),
                            ratings=list(top50['Book-Rating'].values)) 

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    ind=np.where(pt.index==user_input)[0][0]
    items=sorted(list(enumerate(cosine_sim[ind])),key=lambda u:u[1],reverse=True)[1:11]
    data=[]
    pic=[]
    for ind,k in enumerate(items):
        item=[]
        temp_df = books[books['Book-Title'] == pt.index[k[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    print(data)
         
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
