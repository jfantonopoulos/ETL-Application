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
SELECT politician.party, AVG((tweet.retweets)/tweet.replies) AS retweet_ratio, 
AVG((tweet.likes + tweet.retweets)/tweet.replies) AS likes_retweet_ratio,
CONCAT('Ratioed Tweets: ', COUNT(*)) as ratioedTweets FROM politician
INNER JOIN politician_tweets ON politician_id = politician.id
INNER JOIN tweet ON tweet.id = politician_tweets.tweet_id
WHERE politician.twitter_name = tweet.username AND ((tweet.retweets + tweet.likes) < tweet.replies OR tweet.retweets < tweet.replies)
GROUP BY politician.party;"""

partyColors = dict(
	Republican=dict(color='rgb(255, 0, 0)', order=1),
	Democrat=dict(color='rgb(0, 0, 255)', order=2),
	Independent=dict(color='rgb(255, 255, 0)', order=3)
)

cursor.execute(query);

rows = cursor.fetchall()

df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'party', 1: 'retweet_ratio', 2: 'likes_retweet_ratio', 3: 'ratioedTweets'}, inplace=True)
sorted(partyColors.iteritems(), key=lambda (x, y): y['order'])
sortedColors = []
for x in sorted(list(partyColors.values()), key=lambda (x): x['order']):
	sortedColors.append(x['color'])
trace1 = go.Bar(
	x=df['party'],
	y=df['retweet_ratio'],
	text=df["ratioedTweets"],
	name="Ratioed Tweets via Retweets",
	marker=dict(
		color=sortedColors
	),
	width=[0.8, 0.8, 0.5]
)



layout = go.Layout(
    title='Average Ratio of Ratioed Tweets for the 115th Congress',
    xaxis=dict( title='Party'),
    yaxis=dict( title='Ratio' ),
    width=1024,
    height=756,
)

data = [trace1]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='Average Ratio of Ratioed Tweets for the 115th Congress')