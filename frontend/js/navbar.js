// Switch current active tab on navbar button click.
// TODO: Add chunk visibility. Active target chunk and disable the rest of chunks.
function switch_tab(tab_name) {
    const nav_links = document.querySelectorAll('.navbar-btn')
    nav_links.forEach(link => link.classList.remove('active'))

    const active_nav_link = document.getElementById(`nav-${tab_name}`)
    active_nav_link.classList.add('active')

    const tab_contents = document.querySelectorAll('.tab-content')
    tab_contents.forEach(content => content.classList.remove('active'))

    const active_tab_content = document.getElementById(`tab-${tab_name}`)
}
// Parse JTW token
function parse_jwt_token(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

function update_auth_ui() {
    const token = localStorage.getItem('token');
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const profileInfo = document.getElementById('profile-info');

    if (token) {
        const payload = parse_jwt_token(token);
        if (payload && payload.sub) {
            if (loginBtn) loginBtn.style.display = 'none';
            if (logoutBtn) logoutBtn.style.display = 'block';
            if (profileInfo) profileInfo.textContent = payload.sub;
        }
    } else {
        if (loginBtn) loginBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (profileInfo) profileInfo.textContent = '';
    }
}

function logout() {
    localStorage.removeItem('token');
    window.dispatchEvent(new Event('auth-change'));
}

window.addEventListener('auth-change', update_auth_ui);
document.addEventListener('DOMContentLoaded', () => {
    update_auth_ui();
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) logoutBtn.addEventListener('click', logout);
});