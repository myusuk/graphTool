from flaskr import app
from flask import render_template, request, url_for, redirect
import os
import pandas as pd
import matplotlib.pyplot as plt


#PATH
UPLOAD_DIR = '/static/uploads'
PICTURE_DIR = '/static/picture'
BASE_DIR = os.path.dirname(__file__)
UPLOAD_PATH = BASE_DIR + UPLOAD_DIR
PICTURE_PATH = BASE_DIR + PICTURE_DIR

#htmnl表示
@app.route('/')
def index():
    global filelist
    filelist = os.listdir(UPLOAD_PATH)
    return render_template('index.html', filelist=filelist)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/draw')
def draw():
    global figlist
    figlist = os.listdir(PICTURE_PATH)
    return render_template('draw.html', filelist=filelist,  figlist=figlist)

#アップロード
@app.route('/form', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_name = file.filename
    file.save(os.path.join(UPLOAD_PATH + '/' + file_name))
    return redirect(url_for('index'))

#グラフ作成
@app.route('/draw', methods=['POST'])
def draw_graph():
    graph_file = request.form.get('sel') 
    data = pd.read_csv(UPLOAD_PATH + '/' +graph_file)
    
    data["購入月"] = pd.to_datetime(data["購入月"], format = "%Y年%m月")
    graph_data = pd.pivot_table(data, index = "購入月", columns="商品名", values="売り上げ金額", aggfunc="sum")
    
    Label_list = list(graph_data.columns.values)
    for L in Label_list:
        plt.plot(list(graph_data.index), graph_data[L], label=L)
    plt.legend()
    
    save_name = graph_file.replace('.csv', '')
    save_fig = PICTURE_PATH + '/' + save_name + ".jpg"
    plt.savefig(save_fig)
    
    return redirect(url_for('draw'))


