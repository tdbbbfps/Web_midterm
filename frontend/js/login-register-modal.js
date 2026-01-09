export default {
    props: ['show_modal'],
    data() {
        return {
            is_logining: true,
            username: '',
            password: '',
            email: '',
            confirm_password: '',
            show_password: false,
            hint: ''
        };
    },
    methods: {
        async confirm() {
            this.hint = '';
            if (!this.is_logining && this.password !== this.confirm_password) {
                this.hint = "密碼不一致";
                return;
            }
            const url = `http://localhost:8000/api/user${this.is_logining ? '/login' : '/create'}`;
            const body = { username: this.username, password: this.password };
            if (!this.is_logining) body.email = this.email;
            try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });
                const data = await res.json();
                if (!res.ok) {
                    this.hint = data.detail || data.message || (this.is_logining ? "登入失敗" : "註冊失敗");
                } else {
                    if (this.is_logining && data.access_token) {
                        localStorage.setItem('token', data.access_token);
                        window.dispatchEvent(new Event('auth-change'));
                        this.hint = "登入成功";
                        setTimeout(() => this.close(), 500);
                    } else if (!this.is_logining) {
                        this.hint = "註冊成功，請登入";
                        this.is_logining = true;
                    }
                }
                console.log(data);
            } catch (e) {
                this.hint = `${this.is_logining ? "登入" : "註冊"}失敗：${e.message}`;
                console.error(e);
            }
        },
        close() {
            this.$emit('close');
            console.log("User close login-register modal.")
        }
    },
    template: `
    <div v-if="show_modal" class="login-register-modal">
        <div class="modal-content" style="position: relative;">
            <span @click="close" class="close-button">&times;</span>
            <h2>{{ is_logining ? "登入" : "註冊"}}</h2>
            <div class="form-group">
                <div v-if="!is_logining">
                    <label>信箱</label><input type="email" v-model="email">
                </div>
                <div>
                    <label>使用者名稱</label><input type="text" v-model="username">
                </div>
                <div>
                    <label>密碼</label><input :type="show_password ? 'text' : 'password'" v-model="password">
                </div>
                <div v-if="!is_logining">
                    <label>確認密碼</label><input :type="show_password ? 'text' : 'password'" v-model="confirm_password">
                </div>
                <div class="form-footer">
                    <p class="hint">{{ hint }}</p>
                    <button type="button" @click="show_password = !show_password" class="plain-text-button">{{ show_password ? "隱藏" : "顯示" }}密碼</button>
                </div>
                <button @click="confirm" class="btn-primary" style="width: 100%;">確認</button>
                <div style="text-align: center; margin-top: 4px;">
                    <button @click="is_logining = !is_logining" class="plain-text-button">切換{{ is_logining ? "註冊" : "登入"}}</button>
                </div>
            </div>
        </div>
    </div>
    `
}