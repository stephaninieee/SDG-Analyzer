from flask import Flask
from flask import render_template
from flask import request
import sys
sys.path.append("../code/")
import method1_fast
import pandas as pd

app = Flask(__name__)

@app.route('/')
@app.route('/page1.html')
def main():
    return render_template('page1.html')

@app.route('/page2.html')
def page2():
    return render_template('page2.html')


@app.route('/page3.html')
def page3():
    return render_template('page3.html')


@app.route("/req",methods=['POST'])
def req():
    input_text = request.form.get('input_text') #使用者輸入在這裡
    print(input_text)
    print(type(input_text))
    LANG = request.form.get('lang')
    print("Language:",LANG)
    all_kw_list = method1_fast.get_keywords(input_text, LANG)
    print("------------KEYWORDS EXTRACT------------")
    df = pd.DataFrame(all_kw_list, columns=['Keyword', 'Rate'])
    print(df)
    datas = method1_fast.get_similarity(all_kw_list, LANG)
    datas.append(0) #SDG17尚無法處理
    print("------------GET SIMILARITY------------")
    method1_fast.print_sdg_results(datas)
    # datas = [12,13,14,25,7,8,9,10,5,4,2,3,1,2,4,5,6] #SDG權重放這裡
    return render_template('page4.html', **locals())




if __name__ == '__main__':
    app.run()
