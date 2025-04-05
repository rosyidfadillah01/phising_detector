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
        isset($input['id']) &&
        isset($input['true_false'])
    ) {
        // Ambil data dari input
        $id = filter_var($input['id'], FILTER_SANITIZE_NUMBER_INT);
        $true_false = filter_var($input['true_false'], FILTER_VALIDATE_INT, FILTER_NULL_ON_FAILURE);

        // Validasi true_false
        if ($true_false === null || ($true_false !== 0 && $true_false !== 1)) {
            echo json_encode(["message" => "Parameter 'true_false' harus berupa 0 atau 1"]);
            exit;
        }

        // Mulai transaksi
        $db->beginTransaction();

        // 1. Update data di tabel email
        $query_update = "
            UPDATE `email` 
            SET `true_false` = :true_false 
            WHERE `id` = :id
        ";
        $stmt_update = $db->prepare($query_update);
        $stmt_update->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt_update->bindParam(':true_false', $true_false, PDO::PARAM_INT);
        
        // Eksekusi query
        if ($stmt_update->execute()) {
            // Commit transaksi jika berhasil
            $db->commit();
            echo json_encode(["message" => "Data berhasil diperbarui"]);
        } else {
            // Rollback jika eksekusi gagal
            $db->rollBack();
            echo json_encode(["message" => "Gagal memperbarui data"]);
        }
    } else {
        // Jika data tidak lengkap
        echo json_encode(["message" => "Data yang dikirim tidak lengkap"]);
    }
} catch (Exception $e) {
    // Rollback jika terjadi kesalahan
    $db->rollBack();
    echo json_encode([
        "message" => "Terjadi kesalahan saat memperbarui data",
        "error" => $e->getMessage()
    ]);
}
?>