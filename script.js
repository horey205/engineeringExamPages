document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const loginContainer = document.getElementById('login-container');
    const selectionContainer = document.getElementById('selection-container');
    const errorMessage = document.getElementById('error-message');
    const logoutBtn = document.getElementById('logout-btn');

    // Hardcoded credentials as requested (Caution: Client-side JS is not secure for real authentication)
    const VALID_USER = 'user';
    const VALID_PASS = 'user2685';

    // Check if already logged in (using sessionStorage instead of localStorage for session-only persistence)
    if (sessionStorage.getItem('isLoggedIn') === 'true') {
        showSelectionScreen(false);
    }

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (validateCredentials(username, password)) {
            login();
        } else {
            showError('아이디 또는 비밀번호가 올바르지 않습니다.');
        }
    });

    logoutBtn.addEventListener('click', () => {
        logout();
    });

    function validateCredentials(user, pass) {
        return user === VALID_USER && pass === VALID_PASS;
    }

    function login() {
        sessionStorage.setItem('isLoggedIn', 'true');
        showError(''); // Clear error
        showSelectionScreen(true);
    }

    function logout() {
        sessionStorage.removeItem('isLoggedIn');
        showLoginScreen();
    }

    function showSelectionScreen(animate) {
        if (animate) {
            loginContainer.style.opacity = '0';
            setTimeout(() => {
                loginContainer.classList.add('hidden');
                selectionContainer.classList.remove('hidden');
                // Trigger reflow to restart animations if needed, or just let CSS animations run
            }, 500);
        } else {
            loginContainer.classList.add('hidden');
            selectionContainer.classList.remove('hidden');
        }
    }

    function showLoginScreen() {
        selectionContainer.classList.add('hidden');
        loginContainer.classList.remove('hidden');
        loginContainer.style.opacity = '1';
        
        // Clear inputs
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        if (msg) {
            errorMessage.classList.add('visible');
            // Shake animation for card
            const card = document.querySelector('.login-card');
            card.animate([
                { transform: 'translateX(0)' },
                { transform: 'translateX(-10px)' },
                { transform: 'translateX(10px)' },
                { transform: 'translateX(0)' }
            ], {
                duration: 400,
                easing: 'ease-in-out'
            });
        } else {
            errorMessage.classList.remove('visible');
        }
    }
});
