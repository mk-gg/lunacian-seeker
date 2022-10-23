#app/main.py
import json
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home_view():
    return render_template(
        'profile.html', data=[])

@app.route("/result", methods=['GET', 'POST'])
def result():
    data = []
    error = None
    select = request.form.get('comp_select')
    
    resp = requests.get('https://ronin.rest/sm/resolveProfile/'+select)
    jsonResp = resp.json()
    
    if 'error' in jsonResp:
        return render_template('error.html',data=data,error=error)
    
    data.append(jsonResp)
    
    with open("Season0.json",'r', encoding="utf8") as jsonFile:
        dataResp = json.load(jsonFile)
        jsonData = dataResp["_items"]
        
    result = list(filter(lambda jsonData: jsonData['id'] == jsonResp["accountId"], jsonData))
    if not result:
        return render_template('error.html',data=data,error=error)
    else:
        data = data + result
    
        return render_template(
            'result.html', data=data)
    
if __name__== '__main__':
    app.run(debug=True)