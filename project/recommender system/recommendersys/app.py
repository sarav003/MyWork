from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
top50=pickle.load(open(r'C:\Users\sarav\Downloads\top50.pkl','rb'))
pt=pickle.load(open(r'C:\Users\sarav\Downloads\pivot.pkl','rb'))
books=pickle.load(open(r'C:\Users\sarav\Downloads\books.pkl','rb'))
cosine_sim=pickle.load(open(r'C:\Users\sarav\Downloads\cosine_sim.pkl','rb'))
amaz=pickle.load(open(r'C:\Users\sarav\Downloads\amaz_data.pkl','rb'))
cont_cos_sim=pickle.load(open(r'C:\Users\sarav\Downloads\cont_cos_sim.pkl','rb'))
df=pickle.load(open(r'C:\Users\sarav\Downloads\final.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',book_name=list(top50['Book-Title'].values),
                            author=list(top50['Book-Author'].values),
                            image=list(top50['Image-URL-M'].values),
                            ratings=list(top50['Book-Rating'].values)) 

@app.route('/colab')
def recommend_rate():
    return render_template('colab.html')

@app.route('/recommend_books',methods=['post'])
def recommend_boo_rate():
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
         
    return render_template('colab.html',data=data)

@app.route('/content')
def recommend_cont():
    return render_template('content.html')

@app.route('/recommend_content',methods=['post'])
def recommend_boo_cont():
    content_input=request.form.get('content_input')
    indices = pd.Series(amaz['Title'])
    idx = indices[indices == content_input].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_5_indices = list(score_series.iloc[1:6].index)
    da=[]
    for i in top_5_indices:
      recommended_movies=[]
      temp_df=(df[df['Title']==df.index[i]])
      recommended_movies.append(list(df['Title'])[i])
      recommended_movies.append(list(df['authors'])[i])
      recommended_movies.append(list(df['image'])[i])
      recommended_movies.append(list(df['review/score'])[i])
      da.append(recommended_movies)
    
    return render_template('content.html',dta=da)

if __name__ == '__main__':
    app.run(debug=True)
