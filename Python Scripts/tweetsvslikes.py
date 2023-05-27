import plotly
plotly.tools.set_credentials_file(username='ploty_username', api_key='ploty_apikey')
import plotly.plotly as py
import plotly.graph_objs as go

import MySQLdb
import pandas as pd

def getQuery(party):
	query = """
	SELECT politician.fullName, party, COUNT(*) AS tweets, SUM(tweet.likes) AS likes FROM politician 
	INNER JOIN politician_tweets ON politician.id = politician_tweets.politician_id 
	INNER JOIN tweet ON tweet.id = politician_tweets.tweet_id
	WHERE tweet.username = politician.twitter_name """
	query += "AND party = '" + party + "' ";
	query += "GROUP BY politician.fullName"
	return query


conn = MySQLdb.connect(host="localhost", user="username", passwd="password", db="115congress")
cursor = conn.cursor()

cursor.execute(getQuery("Democrat"));

rows = cursor.fetchall()

dfdem = pd.DataFrame( [[ij for ij in i] for i in rows] )
dfdem.rename(columns={0: 'fullName', 1: 'party', 2: 'tweets', 3: 'likes'}, inplace=True)

def makeTrace(traceDf, xIndex, yIndex, textIndex, name, mode, markerSize, markerColor, lineWidth):
	return go.Scatter(
			x=traceDf[xIndex],
			y=traceDf[yIndex],
			text=traceDf[textIndex],
			name=name,
			mode=mode,
			marker = dict(
				size = markerSize,
				color = markerColor,
				line = dict(
						width = lineWidth
					)
				)
		)

traceDem = makeTrace(dfdem, "likes", "tweets", "fullName", "Democrats", "markers", dfdem.tweets * 0.05, "rgba(125, 125, 255, 0.7)", 4)

cursor.execute(getQuery("Republican"));

rows = cursor.fetchall()
dfrep = pd.DataFrame( [[ij for ij in i] for i in rows] )
dfrep.rename(columns={0: 'fullName', 1: 'party', 2: 'tweets', 3: 'likes'}, inplace=True)
traceRep = makeTrace(dfrep, "likes", "tweets", "fullName", "Republicans", "markers", dfrep.tweets * 0.05, "rgba(255, 125, 125, 0.7)", 4)

cursor.execute(getQuery("Independent"));

rows = cursor.fetchall()
dfind = pd.DataFrame( [[ij for ij in i] for i in rows] )
dfind.rename(columns={0: 'fullName', 1: 'party', 2: 'tweets', 3: 'likes'}, inplace=True)
traceInd = makeTrace(dfind, "likes", "tweets", "fullName", "Independents", "markers", dfind.tweets * 0.05, "rgba(255, 255, 0, 0.7)", 4)

layout = go.Layout(
    title='Tweets vs Likes for the 115th Congress',
    xaxis=dict( title='Likes' ),
    yaxis=dict( title='Tweets' ),
    width=1024,
    height=756
)
data = [traceDem, traceRep, traceInd]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='Tweets vs Likes 115th Congress')