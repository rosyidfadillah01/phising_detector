<?php
header('Content-Type: application/json');
require 'vendor/autoload.php';
require_once __DIR__ . '/inc/config.php'; // Pastikan menggunakan require_once untuk file ini

$request_method = $_SERVER['REQUEST_METHOD'];
$request_uri = $_SERVER['REQUEST_URI'];

// Pisahkan URI menjadi path dan query string
$uri_parts = explode('?', $request_uri, 2);
$path = $uri_parts[0];

if ($request_method === 'POST' && $path === '/ins_data') {
    require_once __DIR__ . '/insert_data.php';
} elseif ($request_method === 'GET' && $path === '/get_data') {
    require_once __DIR__ . '/get_data.php';
} elseif ($request_method === 'PUT' && $path === '/upd_data') {
    require_once __DIR__ . '/update_data.php';
}else {
    http_response_code(404); // Mengganti kode status menjadi 404 Not Found
    echo json_encode(array('message' => 'Selamat Datang Di REST API Python Phising Detector'));
}
?>
