"""
ビジネスロジックモジュール
"""
from matplotlib import pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
import pandas as pd
import time
import io
 
 
def create_plt(data, plottype):
    
    data = data.replace(',', '\t').replace(' ', '\t')
    df = pd.read_csv(io.StringIO(data), sep='\t')
 
    # プロットマーカーの大きさ、色、透明度を変更
    print(plottype) 
    if plottype == 'scatter_matrix':
        scatter_matrix(df, diagonal='kde', color='#AAAAFF', edgecolors='#0000FF', alpha=0.5)
    else:
        plt.violinplot(df)
    # ファイル名
    filename = time.strftime('%Y%m%d%H%M%S') + ".png"
 
    # 保存先のパス
    save_path = "./static/result/" + filename
 
    # 表示用URL
    url = "result/" + filename
 
    # 保存処理を行う
    plt.savefig(save_path)
 
    # pltをclose
    plt.close()
 
    return url

def insert(con, title, data, img):
    """ INSERT処理 """
    cur = con.cursor()
    cur.execute('insert into results (title, data, img) values (?, ?, ?)', [title, data, img])
 
    pk = cur.lastrowid
    con.commit()
 
    return pk

def select(con, pk):
    """ 指定したキーのデータをSELECTする """
    cur = con.execute('select id, title, data, img, created from results where id=?', (pk,))
    return cur.fetchone()

def select_all(con):
    """ SELECTする """
    cur = con.execute('select id, title, data, img, created from results order by id desc')
    return cur.fetchall()

def delete(con, pk):
    """ 指定したキーのデータをDELETEする """
    cur = con.cursor()
    cur.execute('delete from results where id=?', (pk,))
    con.commit()