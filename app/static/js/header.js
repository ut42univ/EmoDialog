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
            },

            showCreateModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
                const diaryBody = document.getElementById('diaryBody').value;

                document.getElementById('confirmModalContent').innerText = `以下の内容で日記を新規作成を実行しますか？\n\n${diaryBody}`;
                document.getElementById('confirmModalYes').onclick = () => {
                    document.getElementById('createDiaryForm').submit();
                };
                confirmModal.show();
            },

            showDeleteModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
                const diaryBody = document.getElementById('diaryBody').getAttribute('data-message');

                document.getElementById('confirmModalContent').innerText = `以下の内容の日記を削除しますか？\n\n${diaryBody}`;
                document.getElementById('confirmModalYes').onclick = () => {
                    window.location.href = "/delete";
                };
                confirmModal.show();
            },

            showEditModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));

                document.getElementById('confirmModalContent').innerText = 'Are you sure you want to edit this item?';
                document.getElementById('confirmModalYes').onclick = () => {
                    window.location.href = "/edit";
                };
                confirmModal.show();
            }
        }
    });

    const vm = app.mount('body');

    document.getElementById('logout').addEventListener('click', function(event) {
        event.preventDefault();
        vm.showLogoutModal();
    });

    document.getElementById('delete_diary').addEventListener('click', function(event) {
        event.preventDefault();
        vm.showDeleteModal();
    });

    document.getElementById('create_diary').addEventListener('click', function(event) {
        event.preventDefault();
        vm.showCreateModal();
    });

    
});

