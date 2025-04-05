<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");

include_once 'inc/config.php';

$database = new Database();
$db = $database->getConnection();

try {
    // Ambil data JSON dari request body
    $input = json_decode(file_get_contents("php://input"), true);

    // Validasi apakah semua parameter yang dibutuhkan ada
    if (
        isset($input['url']) &&
        isset($input['true_false'])
    ) {
        // Ambil data dari input
        $url = filter_var(trim($input['url']), FILTER_SANITIZE_URL);
        $true_false = filter_var($input['true_false'], FILTER_VALIDATE_BOOLEAN, FILTER_NULL_ON_FAILURE);

        // Validasi format URL
        if (!filter_var($url, FILTER_VALIDATE_URL)) {
            echo json_encode(["message" => "URL tidak valid"]);
            exit;
        }

        // Validasi panjang URL
        if (strlen($url) > 2048) {
            echo json_encode(["message" => "URL terlalu panjang"]);
            exit;
        }

        // Validasi true_false
        if ($true_false === null) {
            echo json_encode(["message" => "Parameter 'true_false' harus berupa boolean"]);
            exit;
        }

        // Mulai transaksi
        $db->beginTransaction();

        // 1. Masukkan data ke tabel web
        $query_web = "
            INSERT INTO `web`(`url`, `true_false`) 
            VALUES (:url, :true_false)
        ";
        $stmt_web = $db->prepare($query_web);
        $stmt_web->bindParam(':url', $url);
        $stmt_web->bindParam(':true_false', $true_false, PDO::PARAM_BOOL); // Menambahkan tipe parameter untuk true_false
        
        // Eksekusi query
        if ($stmt_web->execute()) {
            // Commit transaksi jika berhasil
            $db->commit();
            echo json_encode(["message" => "Data berhasil ditambahkan"]);
        } else {
            // Rollback jika eksekusi gagal
            $db->rollBack();
            echo json_encode(["message" => "Gagal menambahkan data"]);
        }
    } else {
        // Jika data tidak lengkap
        echo json_encode(["message" => "Data yang dikirim tidak lengkap"]);
    }
} catch (Exception $e) {
    // Rollback jika terjadi kesalahan
    $db->rollBack();
    echo json_encode([
        "message" => "Terjadi kesalahan saat menambahkan data",
        "error" => $e->getMessage()
    ]);
}
?>