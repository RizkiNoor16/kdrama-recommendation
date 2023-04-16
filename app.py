import pandas as pd
import pickle
from flask import Flask, render_template, request

data = pd.read_csv('data/kdrama_list.csv')
model = pickle.load(open('similarity_model.pkl', 'rb'))

def get_recommendation(title, model=model, df=data):
    idx = df[df['Name'] == title].index[0]
    rec_score = list(enumerate(model[idx]))
    rec_score = sorted(rec_score, key=lambda x: x[1], reverse=True)
    rec_scores = rec_score[1:9]
    drama_indices = [i[0] for i in rec_scores]

    result = df[['Name', 'img url', 'Network']].iloc[drama_indices]
    recommended_names = result['Name'].tolist()
    recommended_img_urls = result['img url'].tolist()
    recomended_network = result['Network'].tolist()
    return recommended_names, recommended_img_urls, recomended_network

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def recommend():
    data_sorted = data.sort_values(by=['Name'])
    list_drama = data_sorted['Name'].values
    title = ''
    drama, poster, network = [], [], []
    status = False

    if request.method == 'POST':
        title = request.form['title']
        drama, poster, network = get_recommendation(title)
        status = True

    return render_template('index.html', title=title, drama=drama, poster=poster, list_drama=list_drama, status=status, network=network)

if __name__ == '__main__':
    app.debug = True
    app.run()