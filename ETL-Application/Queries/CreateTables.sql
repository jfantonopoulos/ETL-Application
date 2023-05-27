CREATE TABLE Tweet (
	id BIGINT UNSIGNED PRIMARY KEY NOT NULL,
	retweets INT UNSIGNED,
	url VARCHAR(255),
	fullname VARCHAR(100),
	replies INT UNSIGNED,
	time_stamp TIMESTAMP,
	likes INT UNSIGNED,
	username VARCHAR(50),
	txt MEDIUMTEXT,
	html LONGTEXT
);

CREATE TABLE politician (
	id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	fullName TEXT,
	party VARCHAR(20),
	twitter_name VARCHAR(50)
);

CREATE TABLE politician_tweets (
	tweet_id BIGINT UNSIGNED,
    politician_id BIGINT UNSIGNED,
    PRIMARY KEY(tweet_id, politician_id),
    FOREIGN KEY (tweet_id) REFERENCES tweet(id),
    FOREIGN KEY (politician_id) REFERENCES politician(id)
);