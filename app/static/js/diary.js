document.addEventListener('DOMContentLoaded', function() {

    const app = Vue.createApp({
        methods: {
            showEditModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
                const diaryBody = document.getElementById('diary_body').getAttribute('value');
                const diaryId = document.getElementById("diary_id").getAttribute('value');

                document.getElementById('confirmModalContent').innerText = `以下の日記の編集を行いますか？\n\n${diaryBody}`;
                document.getElementById('confirmModalYes').onclick = () => {
                    window.location.href = `${diaryId}/edit`;
                };
                confirmModal.show();
            },

            showDeleteModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
                const diaryBody = document.getElementById('diary_body').getAttribute('value');
                const diaryId = document.getElementById("diary_id").getAttribute('value');

                document.getElementById('confirmModalContent').innerText = `以下の日記を削除しますか？\n\n${diaryBody}`;
                document.getElementById('confirmModalYes').onclick = () => {
                    window.location.href = `${diaryId}/delete`;
                };
                confirmModal.show();
            
            }
        }
    });

    const diary_page = app.mount('main');

    document.getElementById('edit_diary').addEventListener('click', function(event) {
        event.preventDefault();
        diary_page.showEditModal();
    });

    document.getElementById('delete_diary').addEventListener('click', function(event) {
        event.preventDefault();
        diary_page.showDeleteModal();
    });
    
});

