<?php
if (!class_exists('Database')) {
    class Database {
        private $host = "localhost";
        private $db_name = "u367747531_python_db";
        private $username = "u367747531_admin";
        private $password = "Hudajokam354??";
        public $conn;

        public function getConnection() {
            $this->conn = null;

            try {
                $this->conn = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->db_name, $this->username, $this->password);
                $this->conn->exec("set names utf8");
            } catch (PDOException $exception) {
                echo "Connection error: " . $exception->getMessage();
            }

            return $this->conn;
        }
    }
}
?>
