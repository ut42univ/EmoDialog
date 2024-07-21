document.addEventListener('DOMContentLoaded', function() {

    const app = Vue.createApp({
        methods: {
            showSignUpModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
                const username = document.getElementById('username').value;

                document.getElementById('confirmModalContent').innerText = `EmoDialogへようこそ、${username}さん。\nユーザー登録を続けますか？`;
                document.getElementById('confirmModalYes').onclick = () => {
                    document.getElementById('sign_up_form').submit();
                };
                confirmModal.show();
            }
        }
    });

    const vm = app.mount('main');

    document.getElementById('sign_up').addEventListener('click', function(event) {
        event.preventDefault();
        vm.showSignUpModal();
    });
    
});

