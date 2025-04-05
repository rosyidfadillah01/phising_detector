<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *"); // Mengizinkan semua asal
header("Access-Control-Allow-Methods: GET"); // Mengizinkan metode GET

include_once 'inc/config.php';

$database = new Database();
$db = $database->getConnection();

try {
    // Ambil semua data dari tabel web
    $query_web = "SELECT url FROM web where true_false = 1";
    $stmt_web = $db->prepare($query_web);
    $stmt_web->execute();

    $response = []; // Array untuk menyimpan respons

    if ($stmt_web->rowCount() > 0) {
        // Ambil semua data pengguna dari tabel web
        $urls = $stmt_web->fetchAll(PDO::FETCH_ASSOC);
        $response["urls"] = $urls;
    } else {
        $response["urlS"] = ['DATA KOSONG !!!']; // Jika tidak ada pengguna, kembalikan array kosong
    }

    // Ambil semua data dari tabel email
    $query_email = "SELECT email FROM email where true_false = 1"; // Pastikan tabel email ada
    $stmt_email = $db->prepare($query_email);
    $stmt_email->execute();

    if ($stmt_email->rowCount() > 0) {
        // Ambil semua data dari tabel email
        $emails = $stmt_email->fetchAll(PDO::FETCH_ASSOC);
        $response["emails"] = $emails;
    } else {
        $response["emails"] = []; // Jika tidak ada email, kembalikan array kosong
    }

    // Kembalikan respons dalam format JSON
    echo json_encode($response);
} catch (Exception $e) {
    echo json_encode([
        "message" => "Terjadi kesalahan saat mengambil data",
        "error" => $e->getMessage()
    ]);
}
?>