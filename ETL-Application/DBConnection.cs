using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _115thCongressAnalyzer
{
    public class DBConnection
    {
        private DBConnection() { }

        private string databaseName = String.Empty;

        public string DatabaseName { get { return databaseName; } set { databaseName = value; } }

        public string User { get; set; }
        public string Password { get; set; }

        public MySqlConnection connection = null;

        public MySqlConnection Connection { get { return connection; } }

        private static DBConnection instance = null;
        public static DBConnection Instance()
        {
            if (instance == null)
                instance = new DBConnection();
            return instance;
        }

        public void SetOptions(string dbName, string user, string password)
        {
            databaseName = dbName;
            User = user;
            Password = password;
        }

        public bool IsConnected()
        {
            if (Connection == null)
            {
                if (String.IsNullOrEmpty(databaseName))
                    return false;

                string connString = $"Server=localhost; database={databaseName}; UID={User}; password={Password}";
                connection = new MySqlConnection(connString);
                connection.Open();
            }

            return true;
        }

        public void Close()
        {
            connection.Close();
        }
    }
}
