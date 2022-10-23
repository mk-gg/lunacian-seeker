#app/main.py
import json
from flask import Flask, render_template, request
import requests
from bisect import bisect

app = Flask(__name__)

def grade(score, breakpoints=[2,3, 4, 5, 6, 11, 21, 51, 101, 201, 501, 1001, 20001], grades=[600,400,384, 307.20, 245.76, 196.608, 157.286, 110.100, 77.070, 53.949, 21.580, 8.632, 1.726, 0]):
    i = bisect(breakpoints, score)
    return grades[i]

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
        result.append(grade(result[0]['topRank']))
        data = data + result

        return render_template(
            'result.html', data=data)
    
if __name__== '__main__':
    app.run(debug=True)