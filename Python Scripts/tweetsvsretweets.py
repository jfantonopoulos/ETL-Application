import plotly
plotly.tools.set_credentials_file(username='ploty_username', api_key='ploty_apikey')
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

import MySQLdb
import pandas as pd
import operator

conn = MySQLdb.connect(host="localhost", user="username", passwd="password", db="115congress")
cursor = conn.cursor()
query = '''
SELECT party, COUNT(*) AS tweetCount, retweets FROM politician_tweets
INNER JOIN politician ON politician.id = politician_tweets.politician_id
INNER JOIN tweet ON tweet.id = politician_tweets.tweet_id
WHERE politician.twitter_name = tweet.username
GROUP BY party
'''

cursor.execute(query);

rows = cursor.fetchall()

df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'party', 1: 'tweetCount', 2: 'retweets'}, inplace=True)

repdf = df[(df['party'] == "Republican")]
demdf =  df[(df['party'] == "Democrat")]
indf =  df[(df['party'] == "Independent")]

l=[]
y=[]
N= 53
c= ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

def makeTraces(dataFrame):
   y=[]
   color = 0;
   maxColor = 53;
   for i in range(int(dataFrame["retweets"])):
    y.append((14+i))
    trace0= go.Scatter(
        x= dataFrame['party'],
        y= y,
        mode= 'markers',
        marker= dict(size= 14,
                    line= dict(width=1),
                    color= c[color],
                    opacity= 0.3
                   ),name= y[i],
        text= dataFrame['party']) # The hover text goes here... 
    l.append(trace0);
    color += 1;
    if (color >= 53):
        color = 0

makeTraces(repdf)
makeTraces(demdf)
makeTraces(indf)


layout= go.Layout(
    title= 'Retweets vs likes Per Party for the 115th Congress',
    hovermode= 'closest',
    xaxis= dict(
        title= 'Party',
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
    ),
    yaxis=dict(
        title= 'Retweets',
        ticklen= 5,
        gridwidth= 2,
    ),
    showlegend= False
)
fig= go.Figure(data=l, layout=layout)
py.iplot(fig, filename='Retweets vs likes Per Party for the 115th Congress')