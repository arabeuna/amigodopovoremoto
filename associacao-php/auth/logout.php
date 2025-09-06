<?php
// Incluir configurações antes de iniciar sessão
require_once __DIR__ . '/../config/config.php';
session_start();
session_destroy();
header('Location: login.php');
exit;
?>