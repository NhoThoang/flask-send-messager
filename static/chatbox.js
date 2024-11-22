// Để đóng/mở chat box
function toggleChat() {
    const chatBox = document.getElementById('chat-box');
    chatBox.style.display = chatBox.style.display === 'none' ? 'flex' : 'none';
}

// Gửi tin nhắn (tạm thời hiển thị trong ô chat)
function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const messageContent = document.getElementById('chat-content');

    if (messageInput.value.trim()) {
        const newMessage = document.createElement('div');
        newMessage.classList.add('message');
        newMessage.textContent = messageInput.value;
        messageContent.appendChild(newMessage);
        messageContent.scrollTop = messageContent.scrollHeight; // Di chuyển đến tin nhắn mới nhất
    }

    messageInput.value = ''; // Xóa nội dung input sau khi gửi
}
