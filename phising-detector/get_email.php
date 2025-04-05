<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

include_once 'inc/config.php';

$database = new Database();
$db = $database->getConnection();

try {
    // Koneksi ke database (pastikan Anda sudah mengatur koneksi $db sebelumnya)
    // Contoh: $db = new PDO('mysql:host=localhost;dbname=your_database', 'username', 'password');

    // Ambil semua data pengguna
    $query = "SELECT * FROM email";
    $stmt = $db->prepare($query);
    $stmt->execute();

    if ($stmt->rowCount() > 0) {
        // Ambil semua data pengguna
        $users = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode($users);
    } else {
        echo json_encode(["message" => "Tidak ada pengguna yang ditemukan"]);
    }
} catch (Exception $e) {
    echo json_encode([
        "message" => "Terjadi kesalahan saat mengambil data pengguna",
        "error" => $e->getMessage()
    ]);
}
?>