document.addEventListener('DOMContentLoaded', function() {

    const app = Vue.createApp({
        methods: {
            deleteChatModal() {
                const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));

                document.getElementById('confirmModalContent').innerText = `EmotionAIとの会話を終了しますか？\n実行すると会話の履歴が削除されます。`;
                document.getElementById('confirmModalYes').onclick = () => {
                    window.location.href = `chat/delete`;
                };
                confirmModal.show();
            }
        }
    });

    const chat_page = app.mount('main');

    document.getElementById('delete_chat').addEventListener('click', function(event) {
        event.preventDefault();
        chat_page.deleteChatModal();
    });
    
});

