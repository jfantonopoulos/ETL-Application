using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _115thCongressAnalyzer
{
    public class Tweet
    {
        public long id;
        public int retweets;
        public string url;
        public string fullname;
        public int replies;
        public string timestamp;
        public int likes;
        public string user;
        public string text;
        public string html;
    }

    public class Politician
    {
        public string name;
        public string party;
        public List<Tweet> tweets;
        public string twitterName;
        public Politician(string name, string party, List<Tweet> tweets, string twitterName)
        {
            this.name = name;
            this.party = party;
            this.tweets = tweets;
            this.twitterName = twitterName;
        }
    }

    /*
     * For reference
     * Words that need to be cleaned from names:
     * - Senator
     * - Sen.
     * - Sen
     * - Archive:
     * - , M.D.
     * - U.S.
     * 
     * Chuck Grassley's and Dan Sullivan's names do not have spaces and must be fixed manually.
     */

    class Program
    {
        static string dbUser = "username";
        static string dbPassword = "password";
        static string dbName = "115congress";

        static readonly List<string> WordsToClean = new List<string> { "Senator ", "Sen. ", "Sen ", "Archive: ", ", M.D.", "U.S. " };

        static string CleanName(string name)
        {
            string cleanedName = name;
            foreach(string word in WordsToClean)
            {
                cleanedName = cleanedName.Replace(word, "");
            }
            return cleanedName;
        }

        static void Main(string[] args)
        {
            var conn = DBConnection.Instance();
            conn.SetOptions(dbName, dbUser, dbPassword);
            if (conn.IsConnected())
            {
                List<Politician> politicians = new List<Politician>();
                Console.WriteLine("Enter folder path: ");
                string path = Console.ReadLine();
                DirectoryInfo dInfo = new DirectoryInfo($"{path}");
                foreach (DirectoryInfo dirInfo in dInfo.GetDirectories())
                {
                    foreach (FileInfo fileInfo in dirInfo.GetFiles("*.json"))
                    {
                        using (StreamReader reader = new StreamReader(fileInfo.Open(FileMode.Open), Encoding.ASCII))
                        {
                            string json = reader.ReadToEnd();
                            if (String.IsNullOrEmpty(json)) continue;
                            List<Tweet> tweets = JsonConvert.DeserializeObject<List<Tweet>>(json);
                            string twitterUserLower = fileInfo.Name.Replace("_twitter.json", "").ToLower();
                            string politicianName = tweets.FirstOrDefault(x => x.user.ToLower() == twitterUserLower).fullname;
                            string actualTwitterName = tweets.FirstOrDefault(x => x.user.ToLower() == twitterUserLower).user;
                            politicianName = CleanName(politicianName);
                            Politician politician = new Politician(politicianName, dirInfo.Name, tweets, actualTwitterName);
                            string insertPoliticianCmd = "INSERT INTO politician (fullName, party, twitter_name) VALUES (@fullName, @party, @twitter_name); SELECT last_insert_id();";
                            MySqlCommand cmd = new MySqlCommand(insertPoliticianCmd, conn.Connection);
                            cmd.Parameters.AddWithValue("@fullName", politician.name);
                            cmd.Parameters.AddWithValue("@party", politician.party);
                            cmd.Parameters.AddWithValue("@twitter_name", politician.twitterName);
                            int politicianId = Convert.ToInt32(cmd.ExecuteScalar());
                            foreach(Tweet tweet in politician.tweets)
                            {
                                string insertTweetCmd = "INSERT IGNORE INTO tweet (id, retweets, url, fullname, replies, time_stamp, likes, username, txt, html) VALUES (@id, @retweets, @url, @fullname, @replies, @timestamp, @likes, @username, @txt, @html);";
                                cmd = new MySqlCommand(insertTweetCmd, conn.Connection);
                                cmd.Parameters.AddWithValue("@id", tweet.id);
                                cmd.Parameters.AddWithValue("@retweets", tweet.retweets);
                                cmd.Parameters.AddWithValue("@url", tweet.url);
                                cmd.Parameters.AddWithValue("@fullname", tweet.fullname);
                                cmd.Parameters.AddWithValue("@replies", tweet.replies);
                                cmd.Parameters.AddWithValue("@timestamp", tweet.timestamp);
                                cmd.Parameters.AddWithValue("@likes", tweet.likes);
                                cmd.Parameters.AddWithValue("@username", tweet.user);
                                cmd.Parameters.AddWithValue("@txt", tweet.text);
                                cmd.Parameters.AddWithValue("@html", tweet.html);
                                cmd.ExecuteNonQuery();

                                string insertLinkCmd = "INSERT IGNORE INTO politician_tweets (tweet_id, politician_id) VALUES (@tweetId, @politicianId);";
                                cmd = new MySqlCommand(insertLinkCmd, conn.Connection);
                                cmd.Parameters.AddWithValue("@tweetId", tweet.id);
                                cmd.Parameters.AddWithValue("@politicianId", politicianId);
                                cmd.ExecuteNonQuery();
                            }
                            politicians.Add(politician);
                            Console.WriteLine($"[{DateTime.Now:t}] Exported {tweets.Count} tweets for {politician.name}.");
                        }
                    }
                }
            }
            conn.Close();
            Console.WriteLine($"[{DateTime.Now:t}] Done exporting data to database. Press any key to exit.");
            Console.ReadLine();
        }
    }
}
