# -*- coding: utf-8 -*-
"""
Template HTML pour le tableau de bord de monitoring.
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Shadow V1 – Monitoring</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: #0b0e14;
            color: #e6edf3;
            padding: 24px;
            transition: background 0.3s, color 0.3s;
        }
        body.light {
            background: #f0f4f9;
            color: #1a1f2e;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 16px;
        }
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .header h1 i {
            color: #58a6ff;
        }
        .header-actions {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        .btn {
            background: #1e2633;
            border: none;
            color: #e6edf3;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: 0.2s;
        }
        .btn:hover {
            background: #2d3748;
        }
        body.light .btn {
            background: #dce3ed;
            color: #1a1f2e;
        }
        body.light .btn:hover {
            background: #c5cedc;
        }
        .ping-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
        }
        .ping-badge.ok {
            background: #1a6b3a;
            color: #8bdd9e;
        }
        .ping-badge.error {
            background: #6b1a1a;
            color: #f28b8b;
        }
        body.light .ping-badge.ok {
            background: #d4edda;
            color: #155724;
        }
        body.light .ping-badge.error {
            background: #f8d7da;
            color: #721c24;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 28px;
        }
        .widget {
            background: #151c26;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #252e3b;
            transition: 0.2s;
        }
        .widget:hover {
            border-color: #58a6ff;
            transform: translateY(-2px);
        }
        body.light .widget {
            background: #ffffff;
            border-color: #dce3ed;
        }
        .widget .value {
            font-size: 32px;
            font-weight: 700;
            margin-top: 6px;
        }
        .widget .label {
            font-size: 14px;
            color: #8b949e;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .widget .label i {
            font-size: 18px;
        }
        body.light .widget .label {
            color: #5a6579;
        }
        .charts {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 28px;
        }
        .chart-card {
            background: #151c26;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #252e3b;
        }
        .chart-card h3 {
            font-size: 16px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .chart-card h3 i {
            color: #58a6ff;
        }
        body.light .chart-card {
            background: #ffffff;
            border-color: #dce3ed;
        }
        .chart-card canvas {
            max-height: 240px;
            max-width: 100%;
        }
        .logs-card {
            background: #151c26;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #252e3b;
            margin-bottom: 28px;
        }
        body.light .logs-card {
            background: #ffffff;
            border-color: #dce3ed;
        }
        .logs-card .log-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }
        .log-container {
            background: #0b0e14;
            border-radius: 8px;
            padding: 16px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 1px solid #252e3b;
        }
        body.light .log-container {
            background: #f0f4f9;
            border-color: #dce3ed;
        }
        .log-container .log-line {
            padding: 2px 0;
            border-bottom: 1px solid #1e2633;
            color: #b0c4d9;
        }
        body.light .log-container .log-line {
            border-bottom-color: #dce3ed;
            color: #1a2a3a;
        }
        .log-container .log-line .time {
            color: #58a6ff;
        }
        .log-container .log-line .level-info {
            color: #8bdd9e;
        }
        .log-container .log-line .level-warning {
            color: #f5c542;
        }
        .log-container .log-line .level-error {
            color: #f28b8b;
        }
        .refresh-info {
            color: #8b949e;
            font-size: 13px;
            margin-top: 10px;
            text-align: right;
        }
        @media (max-width: 768px) {
            .charts {
                grid-template-columns: 1fr;
            }
            .grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 480px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 22px;
            }
        }
    </style>
</head>
<body>

    <div class="container">
        <!-- EN-TÊTE -->
        <div class="header">
            <h1><i class="fas fa-robot"></i> Shadow V1</h1>
            <div class="header-actions">
                <span id="pingBadge" class="ping-badge"><i class="fas fa-circle"></i> Chargement...</span>
                <button class="btn" id="themeToggle"><i class="fas fa-moon"></i> Thème</button>
                <button class="btn" id="refreshBtn"><i class="fas fa-sync-alt"></i> Rafraîchir</button>
            </div>
        </div>

        <!-- WIDGETS STATS -->
        <div class="grid" id="statsGrid">
            <div class="widget"><div class="label"><i class="fas fa-users"></i> Utilisateurs</div><div class="value" id="statUsers">-</div></div>
            <div class="widget"><div class="label"><i class="fas fa-comment"></i> Messages</div><div class="value" id="statMessages">-</div></div>
            <div class="widget"><div class="label"><i class="fas fa-terminal"></i> Commandes</div><div class="value" id="statCommands">-</div></div>
            <div class="widget"><div class="label"><i class="fas fa-clock"></i> Uptime</div><div class="value" id="statUptime">-</div></div>
        </div>

        <!-- GRAPHIQUES -->
        <div class="charts">
            <div class="chart-card">
                <h3><i class="fas fa-chart-line"></i> Activité (7 derniers jours)</h3>
                <canvas id="activityChart"></canvas>
            </div>
            <div class="chart-card">
                <h3><i class="fas fa-chart-pie"></i> Utilisation des modèles</h3>
                <canvas id="modelsChart"></canvas>
            </div>
        </div>

        <!-- LOGS -->
        <div class="logs-card">
            <div class="log-header">
                <h3><i class="fas fa-list-ul"></i> Logs en temps réel</h3>
                <span style="color:#8b949e;font-size:13px;">⏳ Mise à jour toutes les 3s</span>
            </div>
            <div id="logContainer" class="log-container">Chargement des logs...</div>
            <div class="refresh-info">Dernière mise à jour : <span id="lastUpdate">-</span></div>
        </div>
    </div>

    <script>
        // ===== Variables =====
        let chartActivity = null;
        let chartModels = null;
        let uptimeStart = Date.now();

        // ===== DOM =====
        const pingBadge = document.getElementById('pingBadge');
        const logContainer = document.getElementById('logContainer');
        const lastUpdateSpan = document.getElementById('lastUpdate');

        // ===== Thème =====
        document.getElementById('themeToggle').addEventListener('click', function() {
            document.body.classList.toggle('light');
            const icon = this.querySelector('i');
            if (document.body.classList.contains('light')) {
                icon.className = 'fas fa-sun';
                this.innerHTML = '<i class="fas fa-sun"></i> Clair';
            } else {
                icon.className = 'fas fa-moon';
                this.innerHTML = '<i class="fas fa-moon"></i> Thème';
            }
        });

        // ===== Rafraîchir =====
        document.getElementById('refreshBtn').addEventListener('click', fetchAll);

        // ===== Fetch tout =====
        async function fetchAll() {
            await Promise.all([fetchStats(), fetchPing(), fetchLogs(), fetchUptime()]);
            lastUpdateSpan.textContent = new Date().toLocaleTimeString();
        }

        // ===== Statistiques =====
        async function fetchStats() {
            try {
                const res = await fetch('/stats');
                const data = await res.json();
                document.getElementById('statUsers').textContent = data.users || 0;
                document.getElementById('statMessages').textContent = data.messages || 0;
                document.getElementById('statCommands').textContent = data.commands || 0;
            } catch (e) { console.error('Stats error:', e); }
        }

        // ===== Ping =====
        async function fetchPing() {
            try {
                const res = await fetch('/ping');
                const data = await res.json();
                const badge = document.getElementById('pingBadge');
                if (data.status === 'ok') {
                    badge.className = 'ping-badge ok';
                    badge.innerHTML = `<i class="fas fa-circle"></i> Connecté (${data.ping} ms)`;
                } else {
                    badge.className = 'ping-badge error';
                    badge.innerHTML = `<i class="fas fa-circle"></i> Hors ligne`;
                }
            } catch (e) {
                document.getElementById('pingBadge').className = 'ping-badge error';
                document.getElementById('pingBadge').innerHTML = `<i class="fas fa-circle"></i> Erreur`;
            }
        }

        // ===== Logs =====
        async function fetchLogs() {
            try {
                const res = await fetch('/logs');
                const text = await res.text();
                const lines = text.split('\\n').filter(l => l.trim());
                let html = '';
                for (const line of lines) {
                    let levelClass = '';
                    if (line.includes('ERROR')) levelClass = 'level-error';
                    else if (line.includes('WARNING')) levelClass = 'level-warning';
                    else levelClass = 'level-info';
                    const timeMatch = line.match(/^(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})/);
                    let formatted = line;
                    if (timeMatch) {
                        const time = timeMatch[1];
                        const rest = line.slice(time.length);
                        formatted = `<span class="time">${time}</span>${rest}`;
                    }
                    html += `<div class="log-line ${levelClass}">${formatted}</div>`;
                }
                document.getElementById('logContainer').innerHTML = html || 'Aucun log disponible.';
                document.getElementById('logContainer').scrollTop = document.getElementById('logContainer').scrollHeight;
            } catch (e) {
                document.getElementById('logContainer').textContent = 'Erreur de chargement des logs.';
            }
        }

        // ===== Uptime =====
        function fetchUptime() {
            const diff = Math.floor((Date.now() - uptimeStart) / 1000);
            const h = String(Math.floor(diff / 3600)).padStart(2, '0');
            const m = String(Math.floor((diff % 3600) / 60)).padStart(2, '0');
            const s = String(diff % 60).padStart(2, '0');
            document.getElementById('statUptime').textContent = `${h}h ${m}m ${s}s`;
        }

        // ===== Graphiques =====
        async function fetchCharts() {
            try {
                const res = await fetch('/charts_data');
                let data = { activity: [], models: {} };
                try {
                    data = await res.json();
                } catch (e) {
                    data = { activity: [12, 19, 3, 5, 2, 3, 15], models: { 'GPT-20B': 45, 'Gemini': 30, 'Llama-70B': 25 } };
                }

                // Activité
                const ctx1 = document.getElementById('activityChart').getContext('2d');
                if (chartActivity) chartActivity.destroy();
                chartActivity = new Chart(ctx1, {
                    type: 'line',
                    data: {
                        labels: ['J-6', 'J-5', 'J-4', 'J-3', 'J-2', 'Hier', 'Aujourd\\'hui'],
                        datasets: [{
                            label: 'Messages',
                            data: data.activity,
                            borderColor: '#58a6ff',
                            backgroundColor: 'rgba(88,166,255,0.1)',
                            fill: true,
                            tension: 0.3,
                            pointBackgroundColor: '#58a6ff'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } } }
                    }
                });

                // Modèles
                const ctx2 = document.getElementById('modelsChart').getContext('2d');
                if (chartModels) chartModels.destroy();
                const labels = Object.keys(data.models);
                const values = Object.values(data.models);
                const colors = ['#58a6ff', '#8bdd9e', '#f5c542', '#f28b8b', '#9b59b6'];
                chartModels = new Chart(ctx2, {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: colors.slice(0, labels.length),
                            borderWidth: 2,
                            borderColor: '#151c26'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom', labels: { color: '#e6edf3' } } }
                    }
                });
                if (document.body.classList.contains('light')) {
                    chartModels.options.plugins.legend.labels.color = '#1a1f2e';
                    chartActivity.options.scales.y.grid.color = 'rgba(0,0,0,0.05)';
                }
            } catch (e) { console.error('Charts error:', e); }
        }

        // ===== Init =====
        function init() {
            fetchAll();
            fetchCharts();
            setInterval(() => {
                fetchAll();
                fetchUptime();
            }, 3000);
            setInterval(fetchCharts, 60000);
        }
        window.onload = init;
    </script>
</body>
</html>
"""
