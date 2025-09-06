<?php
// Teste do index sem banco de dados
require_once __DIR__ . '/config/config.php';
session_start();

echo "Configuração carregada com sucesso<br>";
echo "Sessão iniciada<br>";

// Se o usuário já está logado, redireciona para o dashboard
if (isset($_SESSION['user_id'])) {
    echo "Usuário logado, redirecionando para dashboard<br>";
    // header('Location: pages/dashboard.php');
    // exit;
} else {
    echo "Usuário não logado, redirecionando para login<br>";
    // header('Location: auth/login.php');
    // exit;
}
?>