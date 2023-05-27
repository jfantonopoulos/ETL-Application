import plotly
plotly.tools.set_credentials_file(username='ploty_username', api_key='ploty_apikey')
import plotly.plotly as py
import plotly.graph_objs as go

import MySQLdb
import pandas as pd

conn = MySQLdb.connect(host="localhost", user="username", passwd="password", db="115congress")
cursor = conn.cursor()
query = """
SELECT party, tweet.time_stamp, tweet.likes AS likes, DATE_FORMAT(time_stamp,'%Y-%m') AS monthYear FROM politician 
INNER JOIN politician_tweets ON politician.id = politician_tweets.politician_id 
INNER JOIN tweet ON tweet.id = politician_tweets.tweet_id
WHERE tweet.username = politician.twitter_name AND YEAR(tweet.time_stamp) > 2015
GROUP BY monthYear, party ORDER BY time_stamp DESC;"""

cursor.execute(query);

rows = cursor.fetchall()

df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'party', 1: 'time_stamp', 2: 'likes', 3: 'monthYear'}, inplace=True)

repdf = df[(df['party'] == "Republican")]
demdf =  df[(df['party'] == "Democrat")]
indf =  df[(df['party'] == "Independent")]

trace1 = go.Bar(
	x=demdf['monthYear'],
	y=demdf['likes'],
	name="Democrats",
	marker=dict(
		color='rgba(0, 0, 255, 255)'
	),
    width=[0.8]
)

trace2 = go.Bar(
	x=repdf['monthYear'],
	y=repdf['likes'],
	name="Republicans",
	marker=dict(
		color='rgba(255, 0, 0, 255)'
	),
    width=[0.8]
)

trace3 = go.Bar(
    x=indf['monthYear'],
    y=indf['likes'],
    name="Independent",
    marker=dict(
        color='rgba(255, 255, 0, 255)'
    ),
    width=[0.8]
)

layout = go.Layout(
    title='Party Tweet Likes Over Time for the 115th Congress',
    xaxis=dict( title='Time', type="date" ),
    yaxis=dict( title='Likes' ),
    width=1024,
    height=756,
    barmode='group'
)
#layout["xaxis"]["autorange"] = "reversed";
data = [trace1, trace2, trace3]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='Party Tweet Likes Over Time for the 115th Congress')