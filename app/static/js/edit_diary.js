document.addEventListener('DOMContentLoaded', function() {

    const app = Vue.createApp({
        methods: {
            showCreateModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
                const diaryBody = document.getElementById('diaryBody').value;

                document.getElementById('confirmModalContent').innerText = `以下の内容で日記の編集を反映しますか？\n\n${diaryBody}`;
                document.getElementById('confirmModalYes').onclick = () => {
                    document.getElementById('editDiaryForm').submit();
                };
                confirmModal.show();
            }
        }
    });

    const vm = app.mount('main');

    document.getElementById('edit_diary').addEventListener('click', function(event) {
        event.preventDefault();
        vm.showCreateModal();
    });
    
});

