document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const loginContainer = document.getElementById('login-container');
    const selectionContainer = document.getElementById('selection-container');
    const errorMessage = document.getElementById('error-message');
    const logoutBtn = document.getElementById('logout-btn');

    // Secure Hashed Credentials (SHA-256)
    // 'user' -> 04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb
    // 'user2685' -> 6370701198533b666a6a8f108f9ac1d73c52e825a09282247fb2572626e2552e
    const USER_HASH = '04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb';
    const PASS_HASH = '6370701198533b666a6a8f108f9ac1d73c52e825a09282247fb2572626e2552e';

    // Helper to calculate SHA-256 hash
    async function sha256(message) {
        const msgUint8 = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        return hashHex;
    }

    // Check if already logged in (using sessionStorage instead of localStorage for session-only persistence)
    if (sessionStorage.getItem('isLoggedIn') === 'true') {
        showSelectionScreen(false);
    }

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const inputUserHash = await sha256(username);
        const inputPassHash = await sha256(password);

        if (inputUserHash === USER_HASH && inputPassHash === PASS_HASH) {
            login();
        } else {
            showError('아이디 또는 비밀번호가 올바르지 않습니다.');
        }
    });

    logoutBtn.addEventListener('click', () => {
        logout();
    });

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
