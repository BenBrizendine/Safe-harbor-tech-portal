// Tech Portal Authentication
// Note: User list to be configured later

const VALID_USERS = {
    'ben': 'tech2026',
    'admin': 'safeharbor-admin'
    // More techs added later
};

function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value.trim().toLowerCase();
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('errorMessage');
    
    // Validate credentials
    if (VALID_USERS[username] && VALID_USERS[username] === password) {
        // Create session token
        const sessionToken = btoa(username + ':' + Date.now());
        const sessionData = {
            username: username,
            token: sessionToken,
            loginTime: Date.now()
        };
        
        // Store in localStorage
        localStorage.setItem('tech_session', JSON.stringify(sessionData));
        
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    } else {
        // Show error
        errorDiv.textContent = 'Invalid username or password';
        errorDiv.style.display = 'block';
        
        // Clear password field
        document.getElementById('password').value = '';
        document.getElementById('password').focus();
    }
}

// Check if already logged in
function checkExistingSession() {
    const session = localStorage.getItem('tech_session');
    if (session) {
        try {
            const sessionData = JSON.parse(session);
            const now = Date.now();
            const sessionAge = now - sessionData.loginTime;
            
            // Session valid for 12 hours
            if (sessionAge < 12 * 60 * 60 * 1000) {
                window.location.href = 'dashboard.html';
            } else {
                // Session expired
                localStorage.removeItem('tech_session');
            }
        } catch (e) {
            localStorage.removeItem('tech_session');
        }
    }
}

// Run on page load
checkExistingSession();
