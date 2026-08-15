/**
 * AUTH FASTAPI - FRONTEND SPA CONTROLLER
 */

document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = window.location.origin;

    // State Variables
    let currentUser = localStorage.getItem('username') || null;
    let jwtToken = localStorage.getItem('jwt_token') || null;
    let tempToken2FA = null;

    // DOM Elements - Navigation & Auth
    const apiStatusPill = document.getElementById('api-status');
    const userNavPill = document.getElementById('user-nav');
    const navUsername = document.getElementById('nav-username');
    const btnLogout = document.getElementById('btn-logout');

    const authSection = document.getElementById('auth-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const authForms = document.querySelectorAll('.auth-form');
    
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    // DOM Elements - Dashboard
    const dashUsername = document.getElementById('dash-username');
    const jwtTokenDisplay = document.getElementById('jwt-token-display');
    const btnCopyToken = document.getElementById('btn-copy-token');
    const status2faBadge = document.getElementById('2fa-status-badge');

    const btnSetup2FA = document.getElementById('btn-setup-2fa');
    const setup2FADisplay = document.getElementById('2fa-setup-display');
    const qrCodeImg = document.getElementById('qr-code-img');
    const totpSecretDisplay = document.getElementById('totp-secret-display');
    const btnCopySecret = document.getElementById('btn-copy-secret');
    const totpVerifyCode = document.getElementById('totp-verify-code');
    const btnVerify2FA = document.getElementById('btn-verify-2fa');

    const btnTestProtected = document.getElementById('btn-test-protected');
    const protectedResponseOutput = document.getElementById('protected-response-output');

    const logActionInput = document.getElementById('log-action-input');
    const btnAddLog = document.getElementById('btn-add-log');
    const btnRefreshLogs = document.getElementById('btn-refresh-logs');
    const logsTableBody = document.getElementById('logs-table-body');

    // DOM Elements - 2FA Modal
    const modal2FA = document.getElementById('modal-2fa');
    const form2FALogin = document.getElementById('form-2fa-login');
    const modalTotpCode = document.getElementById('modal-totp-code');
    const btnCancel2FA = document.getElementById('btn-cancel-2fa');

    // --- 1. INITIALIZATION & HEALTH CHECK ---
    checkApiHealth();
    checkAuthSession();

    async function checkApiHealth() {
        try {
            const res = await fetch(`${API_BASE}/health`);
            if (res.ok) {
                const data = await res.json();
                if (data.status === 'ok') {
                    apiStatusPill.classList.add('online');
                    apiStatusPill.querySelector('.status-text').textContent = 'API Online';
                }
            }
        } catch (err) {
            apiStatusPill.classList.remove('online');
            apiStatusPill.querySelector('.status-text').textContent = 'API Offline';
        }
    }

    function checkAuthSession() {
        if (jwtToken && currentUser) {
            showDashboard();
        } else {
            showAuth();
        }
    }

    function showAuth() {
        authSection.classList.remove('hidden');
        dashboardSection.classList.add('hidden');
        userNavPill.classList.add('hidden');
    }

    function showDashboard() {
        authSection.classList.add('hidden');
        dashboardSection.classList.remove('hidden');
        userNavPill.classList.remove('hidden');

        navUsername.textContent = currentUser;
        dashUsername.textContent = currentUser;
        jwtTokenDisplay.value = jwtToken;

        // Fetch Protected Data & Logs on Load
        testProtectedEndpoint(false);
        loadUserLogs();
    }

    // --- 2. TAB SWITCHING ---
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            authForms.forEach(f => f.classList.remove('active'));

            btn.classList.add('active');
            const targetForm = document.getElementById(btn.dataset.tab);
            if (targetForm) targetForm.classList.add('active');
        });
    });

    // --- 3. AUTHENTICATION FLOWS ---

    // Register User
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('reg-username').value.trim();
        const password = document.getElementById('reg-password').value;

        try {
            const res = await fetch(`${API_BASE}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();
            if (res.ok) {
                showToast('Usuário cadastrado com sucesso! Faça login.', 'success');
                registerForm.reset();
                // Switch to Login Tab
                document.querySelector('[data-tab="login-form"]').click();
                document.getElementById('login-username').value = username;
            } else {
                showToast(data.detail || 'Erro ao criar conta.', 'error');
            }
        } catch (err) {
            showToast('Falha na comunicação com o servidor.', 'error');
        }
    });

    // Login User
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value;

        try {
            const res = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();

            if (res.ok) {
                // Check if 2FA is required
                if (data.temp_token) {
                    tempToken2FA = data.temp_token;
                    currentUser = username;
                    open2FAModal();
                } else if (data.access_token) {
                    // Direct login success
                    setSession(data.access_token, username);
                    showToast(`Bem-vindo novamente, ${username}!`, 'success');
                    loginForm.reset();
                }
            } else {
                showToast(data.detail || 'Credenciais inválidas.', 'error');
            }
        } catch (err) {
            showToast('Erro de conexão ao tentar fazer login.', 'error');
        }
    });

    // 2FA Modal Flow
    function open2FAModal() {
        modal2FA.classList.remove('hidden');
        modalTotpCode.value = '';
        modalTotpCode.focus();
    }

    function close2FAModal() {
        modal2FA.classList.add('hidden');
        tempToken2FA = null;
    }

    btnCancel2FA.addEventListener('click', close2FAModal);

    form2FALogin.addEventListener('submit', async (e) => {
        e.preventDefault();
        const code = modalTotpCode.value.trim();

        if (!tempToken2FA || !code) return;

        try {
            const res = await fetch(`${API_BASE}/login/2fa`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    temp_token: tempToken2FA,
                    code: code
                })
            });

            const data = await res.json();

            if (res.ok && data.access_token) {
                close2FAModal();
                setSession(data.access_token, currentUser);
                showToast('Autenticação 2FA realizada com sucesso!', 'success');
                loginForm.reset();
            } else {
                showToast(data.detail || 'Código TOTP incorreto.', 'error');
            }
        } catch (err) {
            showToast('Erro ao validar o código 2FA.', 'error');
        }
    });

    // Logout
    btnLogout.addEventListener('click', () => {
        clearSession();
        showToast('Sessão encerrada.', 'success');
    });

    function setSession(token, username) {
        jwtToken = token;
        currentUser = username;
        localStorage.setItem('jwt_token', token);
        localStorage.setItem('username', username);
        showDashboard();
    }

    function clearSession() {
        jwtToken = null;
        currentUser = null;
        tempToken2FA = null;
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('username');
        showAuth();
    }

    // --- 4. DASHBOARD ACTIONS ---

    // Copy Token
    btnCopyToken.addEventListener('click', () => {
        if (jwtTokenDisplay.value) {
            navigator.clipboard.writeText(jwtTokenDisplay.value);
            showToast('Token JWT copiado para a área de transferência!', 'success');
        }
    });

    // Setup 2FA
    btnSetup2FA.addEventListener('click', async () => {
        try {
            const res = await fetch(`${API_BASE}/2fa/setup`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${jwtToken}`,
                    'Content-Type': 'application/json'
                }
            });

            const data = await res.json();

            if (res.ok) {
                setup2FADisplay.classList.remove('hidden');
                qrCodeImg.src = `data:image/png;base64,${data.qr_code_base64}`;
                totpSecretDisplay.value = data.secret;
                status2faBadge.className = 'badge badge-warning';
                status2faBadge.innerHTML = '<i class="ri-refresh-line"></i> Em Configuração';
                showToast('QR Code 2FA gerado! Escaneie no seu app autenticador.', 'success');
            } else {
                showToast(data.detail || 'Erro ao gerar 2FA.', 'error');
            }
        } catch (err) {
            showToast('Falha na requisição de 2FA.', 'error');
        }
    });

    // Copy Secret
    btnCopySecret.addEventListener('click', () => {
        if (totpSecretDisplay.value) {
            navigator.clipboard.writeText(totpSecretDisplay.value);
            showToast('Chave secreta copiada!', 'success');
        }
    });

    // Verify 2FA Setup
    btnVerify2FA.addEventListener('click', async () => {
        const code = totpVerifyCode.value.trim();
        if (!code) {
            showToast('Digite o código de 6 dígitos.', 'error');
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/2fa/verify`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${jwtToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code })
            });

            const data = await res.json();

            if (res.ok) {
                status2faBadge.className = 'badge badge-success';
                status2faBadge.innerHTML = '<i class="ri-shield-check-line"></i> Ativo & Protegido';
                showToast('2FA verificado e ativado com sucesso!', 'success');
                totpVerifyCode.value = '';
            } else {
                showToast(data.detail || 'Código inválido.', 'error');
            }
        } catch (err) {
            showToast('Erro ao verificar TOTP.', 'error');
        }
    });

    // Test Protected Route
    btnTestProtected.addEventListener('click', () => testProtectedEndpoint(true));

    async function testProtectedEndpoint(notify = true) {
        try {
            const res = await fetch(`${API_BASE}/protected`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${jwtToken}`
                }
            });

            const data = await res.json();
            protectedResponseOutput.textContent = JSON.stringify(data, null, 2);

            if (res.ok) {
                if (notify) showToast('Requisição /protected autorizada!', 'success');
            } else {
                if (res.status === 401) {
                    clearSession();
                    showToast('Sessão expirada. Faça login novamente.', 'error');
                } else if (notify) {
                    showToast('Acesso negado ao endpoint.', 'error');
                }
            }
        } catch (err) {
            protectedResponseOutput.textContent = `// Erro: ${err.message}`;
        }
    }

    // Load User Logs
    btnRefreshLogs.addEventListener('click', loadUserLogs);

    async function loadUserLogs() {
        try {
            const res = await fetch(`${API_BASE}/logs`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${jwtToken}`
                }
            });

            if (res.ok) {
                const logs = await res.json();
                renderLogsTable(logs);
            }
        } catch (err) {
            console.error('Erro ao carregar logs:', err);
        }
    }

    function renderLogsTable(logs) {
        if (!logs || logs.length === 0) {
            logsTableBody.innerHTML = `<tr><td colspan="3" class="text-center muted">Nenhum log registrado ainda.</td></tr>`;
            return;
        }

        logsTableBody.innerHTML = logs.map(log => `
            <tr>
                <td>#${log.id}</td>
                <td><strong>${escapeHtml(log.action)}</strong></td>
                <td>${log.timestamp ? formatDate(log.timestamp) : 'Agora'}</td>
            </tr>
        `).join('');
    }

    // Add New Log
    btnAddLog.addEventListener('click', async () => {
        const action = logActionInput.value.trim();
        if (!action) {
            showToast('Escreva a ação do log.', 'error');
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/logs`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${jwtToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ action })
            });

            const data = await res.json();

            if (res.ok) {
                showToast('Log de ação registrado!', 'success');
                logActionInput.value = '';
                loadUserLogs();
            } else {
                showToast(data.detail || 'Erro ao salvar log.', 'error');
            }
        } catch (err) {
            showToast('Erro ao enviar log.', 'error');
        }
    });

    // --- 5. TOAST NOTIFICATIONS & HELPERS ---
    function showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const iconClass = type === 'success' ? 'ri-checkbox-circle-fill' : 'ri-error-warning-fill';
        toast.innerHTML = `<i class="${iconClass}"></i> <span>${escapeHtml(message)}</span>`;

        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 4000);
    }

    function escapeHtml(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
        );
    }

    function formatDate(dateStr) {
        try {
            const d = new Date(dateStr);
            return d.toLocaleString('pt-BR');
        } catch {
            return dateStr;
        }
    }
});
