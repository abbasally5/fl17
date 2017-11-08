
from flask import Flask
from flask import jsonify, request, render_template, send_file

from nlu import get_nlu
from datetime import datetime as dt
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
          as Features
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)
MSG_FILE = "chat.csv" 
TEMP_FILE = "temp.txt"

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        #print('get')
        #return render_template("dashboard.html", data=data, layout=layout)
        return render_template("dashboard.html")
    if request.method == "POST":
        data = request.get_json()
        #print("data: {}".format(data))
        text = data['text']
        add_to_chat(text)
        return jsonify({'success': 'success'})

@app.route("/data", methods=["GET", "POST"])
def msg_data():
    if request.method == "GET":
        sent = get_sentiment()
        get_analysis(sent)
        #print(sent)
        #return 'OK', 200
        return send_file('static/plot.png', mimetype='image/png')

def get_chat():
    #print('in get_chat')
    msgs = [] 

    with open(MSG_FILE, 'r') as f:
        for line in f:
            #print(line)
            csv = line.strip().split(",")
            if len(csv) > 1:
                msgs.append((csv[0], ",".join(csv[1:])))

    return msgs

def put_chat(msgs):

    with open(MSG_FILE, "w") as f:
        for m in msgs:
            f.write("{0},{1}\n".format(m[0], m[1]))

def add_to_chat(msg):

    msgs = get_chat()
    now = dt.now() 
    msgs.append((now.isoformat(), msg))
    put_chat(msgs)

def get_msgs_by_date(date):
    pass

def get_sentiment():

    msgs = get_chat()
    dates = []
    msgs_by_date = {}
    sentiment = {}

    for m in msgs:
        date = m[0].split("T")[0]
        if date in msgs_by_date:
            msgs_by_date[date].append(m)
        else:
            msgs_by_date[date] = [m]
            dates.append(date)

    dates.sort() 

    for d in dates:
        msgs_on_day = [m[1] for m in msgs_by_date[d]]

        """
        with open(TEMP_FILE, "w") as f:
            for m in msgs_on_day:
                f.write(m[1])
        """
        # do sentiment
        txt = "".join(msgs_on_day)
        try:
            resp = get_nlu(txt)
            #print(d)
            #print(resp)
            sentiment[d] = resp
        except Exception as e:
            pass
    
    return sentiment

def get_analysis(sent):
    x = []
    anger = []
    fear = []
    sadness = []
    joy = []
    #print("sent: {}".format(sent))
    for date, resp in sent.items():
        x.append(date)
        emotions = resp[u'emotion'][u'document'][u'emotion']
        anger.append(emotions[u'anger'])
        fear.append(emotions[u'fear'])
        sadness.append(emotions[u'sadness'])
        joy.append(emotions[u'joy'])

    fig = plt.figure()
    fig.suptitle('Sentiment Over Time')
    ax = fig.add_subplot(111)
    ax.plot(x,anger)
    ax.plot(x,fear)
    ax.plot(x,sadness)
    ax.plot(x,joy)
    ax.set_xlabel("Date")
    ax.set_ylabel("Level of Emotion")
    ax.legend(['Anger', 'Fear', 'Sadness', 'Joy'], loc='upper left')
    fig.savefig('static/plot.png')
    

        
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
