<?php
// Incluir configurações antes de iniciar sessão
require_once __DIR__ . '/../config/config.php';
session_start();
require_once '../config/database.php';
verificarLogin();

// Processar formulário de cadastro/edição
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nome = $_POST['nome'] ?? '';
    $descricao = $_POST['descricao'] ?? '';
    $categoria = $_POST['categoria'] ?? '';
    $idade_minima = $_POST['idade_minima'] ?? null;
    $idade_maxima = $_POST['idade_maxima'] ?? null;
    $status = $_POST['status'] ?? 'ativa';
    
    if (isset($_POST['id']) && !empty($_POST['id'])) {
        // Editar atividade
        $stmt = $pdo->prepare("UPDATE atividades SET nome = ?, descricao = ?, categoria = ?, idade_minima = ?, idade_maxima = ?, status = ? WHERE id = ?");
        $stmt->execute([$nome, $descricao, $categoria, $idade_minima, $idade_maxima, $status, $_POST['id']]);
        $mensagem = "Atividade atualizada com sucesso!";
    } else {
        // Cadastrar nova atividade
        $stmt = $pdo->prepare("INSERT INTO atividades (nome, descricao, categoria, idade_minima, idade_maxima, status) VALUES (?, ?, ?, ?, ?, ?)");
        $stmt->execute([$nome, $descricao, $categoria, $idade_minima, $idade_maxima, $status]);
        $mensagem = "Atividade cadastrada com sucesso!";
    }
}

// Buscar atividades
$busca = $_GET['busca'] ?? '';
$categoria_filtro = $_GET['categoria'] ?? '';

$sql = "SELECT * FROM atividades WHERE 1=1";
$params = [];

if ($busca) {
    $sql .= " AND nome LIKE ?";
    $params[] = "%$busca%";
}

if ($categoria_filtro) {
    $sql .= " AND categoria = ?";
    $params[] = $categoria_filtro;
}

$sql .= " ORDER BY nome";

$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$atividades = $stmt->fetchAll();

// Buscar atividade para edição
$atividadeEdicao = null;
if (isset($_GET['editar'])) {
    $stmt = $pdo->prepare("SELECT * FROM atividades WHERE id = ?");
    $stmt->execute([$_GET['editar']]);
    $atividadeEdicao = $stmt->fetch();
}

// Excluir atividade
if (isset($_GET['excluir'])) {
    $stmt = $pdo->prepare("DELETE FROM atividades WHERE id = ?");
    $stmt->execute([$_GET['excluir']]);
    header('Location: atividades.php');
    exit;
}

// Buscar categorias para o filtro
$stmt = $pdo->query("SELECT DISTINCT categoria FROM atividades WHERE categoria IS NOT NULL ORDER BY categoria");
$categorias = $stmt->fetchAll(PDO::FETCH_COLUMN);
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestão de Atividades - Associação Amigo do Povo</title>
    <link href="../assets/css/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-blue-600 text-white p-4">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-xl font-bold">Associação Amigo do Povo</h1>
            <div class="space-x-4">
                <a href="dashboard.php" class="hover:text-blue-200">Dashboard</a>
                <a href="alunos.php" class="hover:text-blue-200">Alunos</a>
                <a href="atividades.php" class="text-blue-200 font-semibold">Atividades</a>
                <a href="turmas.php" class="hover:text-blue-200">Turmas</a>
                <a href="matriculas.php" class="hover:text-blue-200">Matrículas</a>
                <a href="relatorios.php" class="hover:text-blue-200">Relatórios</a>
                <a href="../auth/logout.php" class="hover:text-blue-200">Sair</a>
            </div>
        </div>
    </nav>

    <div class="container mx-auto p-6">
        <h2 class="text-3xl font-bold text-gray-800 mb-8">Gestão de Atividades</h2>
        
        <?php if (isset($mensagem)): ?>
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
                <?= htmlspecialchars($mensagem) ?>
            </div>
        <?php endif; ?>
        
        <!-- Formulário de Cadastro/Edição -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <h3 class="text-xl font-bold text-gray-800 mb-4">
                <?= $atividadeEdicao ? 'Editar Atividade' : 'Cadastrar Nova Atividade' ?>
            </h3>
            
            <form method="POST" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <?php if ($atividadeEdicao): ?>
                    <input type="hidden" name="id" value="<?= $atividadeEdicao['id'] ?>">
                <?php endif; ?>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Nome da Atividade</label>
                    <input type="text" name="nome" required 
                           value="<?= $atividadeEdicao['nome'] ?? '' ?>"
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Categoria</label>
                    <select name="categoria" 
                            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">Selecione uma categoria</option>
                        <option value="Esporte" <?= ($atividadeEdicao['categoria'] ?? '') === 'Esporte' ? 'selected' : '' ?>>Esporte</option>
                        <option value="Arte" <?= ($atividadeEdicao['categoria'] ?? '') === 'Arte' ? 'selected' : '' ?>>Arte</option>
                        <option value="Educação" <?= ($atividadeEdicao['categoria'] ?? '') === 'Educação' ? 'selected' : '' ?>>Educação</option>
                        <option value="Música" <?= ($atividadeEdicao['categoria'] ?? '') === 'Música' ? 'selected' : '' ?>>Música</option>
                        <option value="Dança" <?= ($atividadeEdicao['categoria'] ?? '') === 'Dança' ? 'selected' : '' ?>>Dança</option>
                        <option value="Artesanato" <?= ($atividadeEdicao['categoria'] ?? '') === 'Artesanato' ? 'selected' : '' ?>>Artesanato</option>
                        <option value="Outros" <?= ($atividadeEdicao['categoria'] ?? '') === 'Outros' ? 'selected' : '' ?>>Outros</option>
                    </select>
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Idade Mínima</label>
                    <input type="number" name="idade_minima" min="0" max="100"
                           value="<?= $atividadeEdicao['idade_minima'] ?? '' ?>"
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Idade Máxima</label>
                    <input type="number" name="idade_maxima" min="0" max="100"
                           value="<?= $atividadeEdicao['idade_maxima'] ?? '' ?>"
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                
                <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
                    <textarea name="descricao" rows="3" 
                              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"><?= $atividadeEdicao['descricao'] ?? '' ?></textarea>
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
                    <select name="status" 
                            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="ativa" <?= ($atividadeEdicao['status'] ?? 'ativa') === 'ativa' ? 'selected' : '' ?>>Ativa</option>
                        <option value="inativa" <?= ($atividadeEdicao['status'] ?? '') === 'inativa' ? 'selected' : '' ?>>Inativa</option>
                    </select>
                </div>
                
                <div class="md:col-span-2">
                    <button type="submit" 
                            class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <?= $atividadeEdicao ? 'Atualizar Atividade' : 'Cadastrar Atividade' ?>
                    </button>
                    <?php if ($atividadeEdicao): ?>
                        <a href="atividades.php" class="ml-4 bg-gray-500 text-white px-6 py-2 rounded-md hover:bg-gray-600 inline-block">
                            Cancelar
                        </a>
                    <?php endif; ?>
                </div>
            </form>
        </div>
        
        <!-- Filtros -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <form method="GET" class="flex flex-wrap gap-4">
                <input type="text" name="busca" placeholder="Buscar por nome..." 
                       value="<?= htmlspecialchars($busca) ?>"
                       class="flex-1 min-w-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                
                <select name="categoria" 
                        class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">Todas as categorias</option>
                    <?php foreach ($categorias as $cat): ?>
                        <option value="<?= htmlspecialchars($cat) ?>" <?= $categoria_filtro === $cat ? 'selected' : '' ?>>
                            <?= htmlspecialchars($cat) ?>
                        </option>
                    <?php endforeach; ?>
                </select>
                
                <button type="submit" class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700">
                    Filtrar
                </button>
                <a href="atividades.php" class="bg-gray-500 text-white px-6 py-2 rounded-md hover:bg-gray-600">
                    Limpar
                </a>
            </form>
        </div>
        
        <!-- Lista de Atividades -->
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-800">Lista de Atividades (<?= count($atividades) ?>)</h3>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
                <?php foreach ($atividades as $atividade): ?>
                    <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div class="flex justify-between items-start mb-2">
                            <h4 class="text-lg font-semibold text-gray-800"><?= htmlspecialchars($atividade['nome']) ?></h4>
                            <span class="px-2 py-1 text-xs rounded-full <?= $atividade['status'] === 'ativa' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800' ?>">
                                <?= ucfirst($atividade['status']) ?>
                            </span>
                        </div>
                        
                        <?php if ($atividade['categoria']): ?>
                            <p class="text-sm text-blue-600 mb-2"><?= htmlspecialchars($atividade['categoria']) ?></p>
                        <?php endif; ?>
                        
                        <?php if ($atividade['descricao']): ?>
                            <p class="text-sm text-gray-600 mb-3"><?= htmlspecialchars($atividade['descricao']) ?></p>
                        <?php endif; ?>
                        
                        <?php if ($atividade['idade_minima'] || $atividade['idade_maxima']): ?>
                            <p class="text-xs text-gray-500 mb-3">
                                Idade: 
                                <?php if ($atividade['idade_minima'] && $atividade['idade_maxima']): ?>
                                    <?= $atividade['idade_minima'] ?> a <?= $atividade['idade_maxima'] ?> anos
                                <?php elseif ($atividade['idade_minima']): ?>
                                    A partir de <?= $atividade['idade_minima'] ?> anos
                                <?php elseif ($atividade['idade_maxima']): ?>
                                    Até <?= $atividade['idade_maxima'] ?> anos
                                <?php endif; ?>
                            </p>
                        <?php endif; ?>
                        
                        <div class="flex space-x-2">
                            <a href="?editar=<?= $atividade['id'] ?>" 
                               class="text-blue-600 hover:text-blue-900 text-sm font-medium">Editar</a>
                            <a href="?excluir=<?= $atividade['id'] ?>" 
                               onclick="return confirm('Tem certeza que deseja excluir esta atividade?')"
                               class="text-red-600 hover:text-red-900 text-sm font-medium">Excluir</a>
                        </div>
                    </div>
                <?php endforeach; ?>
                
                <?php if (empty($atividades)): ?>
                    <div class="col-span-full text-center py-8 text-gray-500">
                        Nenhuma atividade encontrada.
                    </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</body>
</html>