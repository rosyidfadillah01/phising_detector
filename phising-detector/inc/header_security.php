<?php
// Ambil user agent dari pengguna
$user_agent = $_SERVER['HTTP_USER_AGENT'];

// Tentukan nilai Sec-Ch-Ua berdasarkan user agent
if (strpos($user_agent, 'Firefox') !== false) {
    $sec_ch_ua = 'Chromium;v=92, Firefox;v=92';
} elseif (strpos($user_agent, 'Chrome') !== false) {
    $sec_ch_ua = 'Chromium;v=92, Chrome;v=92';
} else {
    $sec_ch_ua = 'Chromium;v=92';
}

// Atur header Sec-Ch-Ua
header("Sec-Ch-Ua: $sec_ch_ua");

// Atur header User-Agent
header("User-Agent: $user_agent");

// Set header Sec-Fetch-Site
header("Sec-Fetch-Site: same-site");

// Set header Sec-Fetch-Mode
header("Sec-Fetch-Mode: cors");

// Set header Sec-Fetch-Dest
header("Sec-Fetch-Dest: empty");
?>
