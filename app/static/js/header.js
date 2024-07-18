document.addEventListener('DOMContentLoaded', function() {
    const app = Vue.createApp({
        methods: {
            showLogoutModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
                document.getElementById('confirmModalContent').innerText = 'ログアウトしますか？';
                document.getElementById('confirmModalYes').onclick = () => {
                    window.location.href = "/logout";
                };
                confirmModal.show();
            }
        }
    });

    const header = app.mount('header');

    document.getElementById('logout').addEventListener('click', function(event) {
        event.preventDefault();
        header.showLogoutModal();
    });
});

