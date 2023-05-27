import plotly
plotly.tools.set_credentials_file(username='ploty_username', api_key='ploty_apikey')
import plotly.plotly as py
import plotly.graph_objs as go

import MySQLdb
import pandas as pd

conn = MySQLdb.connect(host="localhost", user="username", passwd="password", db="115congress")
cursor = conn.cursor()

query = """
	SELECT party, SUM(replies + likes + retweets) AS interactions FROM politician 
	INNER JOIN politician_tweets ON politician.id = politician_tweets.politician_id 
	INNER JOIN tweet ON tweet.id = politician_tweets.tweet_id
	WHERE tweet.username = politician.twitter_name GROUP BY party"""

colors = ['rgba(0, 0, 255, 255)', 'rgba(255, 255, 0, 255)', 'rgba(255, 0, 0, 255)']

cursor.execute(query);

rows = cursor.fetchall()

df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'party', 1: 'interactions'}, inplace=True)

layout = go.Layout(
    title='Party Interactions for the 115th Congress',
    width=1024,
    height=756
)

trace = go.Pie(labels=df['party'], 
	values=df['interactions'],
	marker=dict(colors=colors, 
		line=dict(color='rgba(0, 0, 0, 255)', 
			width=1)))


fig = go.Figure(data=[trace], layout=layout)

py.iplot(fig, filename="Interactions for the 115th Congress")