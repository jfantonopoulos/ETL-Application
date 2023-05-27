import plotly
plotly.tools.set_credentials_file(username='ploty_username', api_key='ploty_apikey')
import plotly.plotly as py
import plotly.graph_objs as go

import MySQLdb
import pandas as pd
import operator

conn = MySQLdb.connect(host="localhost", user="username", passwd="password", db="115congress")
cursor = conn.cursor()
query = """
SELECT party, COUNT(*) AS tweetCount, DATE_FORMAT(time_stamp,'%Y-%m') AS shortDate, tweet.time_stamp FROM politician_tweets
INNER JOIN politician ON politician.id = politician_tweets.politician_id
INNER JOIN tweet ON politician_tweets.tweet_id = tweet.id
WHERE politician.twitter_name = tweet.username AND YEAR(tweet.time_stamp) > 2015
GROUP BY shortDate, party
ORDER BY time_stamp DESC;"""

cursor.execute(query)

rows = cursor.fetchall()

df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'party', 1: 'tweetCount', 2: 'shortDate', 3: 'time_stamp'}, inplace=True)

repdf = df[(df['party'] == "Republican")]
demdf =  df[(df['party'] == "Democrat")]
indf =  df[(df['party'] == "Independent")]

traceRep = go.Scatter(
	x=repdf['shortDate'],
	y=repdf['tweetCount'],
	name="Republicans",
    mode = 'lines+markers',
    connectgaps=True,
    line = dict(
    	width=4,
    	color='rgb(255, 0, 0)'
    )
)

traceDem = go.Scatter(
	x=demdf['shortDate'],
	y=demdf['tweetCount'],
    mode = 'lines+markers',
    name="Democrats",
    connectgaps=True,
    line = dict(
    	width=4,
    	color='rgb(0, 0, 255)'
    )
)

traceInd = go.Scatter(
	x=indf['shortDate'],
	y=indf['tweetCount'],
    mode = 'lines+markers',
    name="Independents",
    connectgaps=True,
    line = dict(
    	width=4,
    	color='rgb(255, 255, 0)'
    )
)

layout = go.Layout(
    title='Tweets over Time for the 115th Congress',
    xaxis=dict( title='Date', type="date"),
    yaxis=dict( title='Tweets' ),
    width=1024,
    height=756,
)
#layout["xaxis"]["autorange"] = "reversed";
data = [traceRep, traceDem, traceInd]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='Tweets over Time for the 115th Congress')