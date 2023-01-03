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
    return render_template('index.html',book_name=list(df['Title'].values),
                            author=list(df['authors'].values),
                            image=list(df['image'].values),
                            ratings=list(df['review/score'].values)) 

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
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
    
    return render_template('recommend.html',dta=da)


if __name__ == '__main__':
    app.run(debug=True)
