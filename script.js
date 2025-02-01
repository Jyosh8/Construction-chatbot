// Function to send a message
function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    // Display user message
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="message user">You: ${userInput}</div>`;

    // Send message to backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        chatBox.innerHTML += `
            <div class="message bot">
                Bot: ${data.response}
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
    })
    .catch(error => console.error('Error:', error));

    // Clear input
    document.getElementById('user-input').value = '';
}

// Function to send a clickable option
function sendOption(tag) {
    const chatBox = document.getElementById('chat-box');
    const options = document.getElementById('options');
    options.style.display = 'none'; // Hide options after selection

    // Send the selected option to the backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: tag }), // Send the tag (e.g., 'build_new_home')
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        chatBox.innerHTML += `
            <div class="message bot">
                Bot: ${data.response}
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
    })
    .catch(error => console.error('Error:', error));
}

// Add event listener for the Enter key
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage(); // Call the sendMessage function
    }
});

// Disable Send button when input is empty
document.getElementById('user-input').addEventListener('input', function () {
    const sendButton = document.getElementById('send-button');
    sendButton.disabled = this.value.trim() === '';
});

// Emoji picker functionality
const emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾'];

function toggleEmojiPicker() {
    const emojiContainer = document.getElementById('emoji-container');
    if (emojiContainer.style.display === 'none') {
        emojiContainer.style.display = 'block';
        loadEmojis();
    } else {
        emojiContainer.style.display = 'none';
    }
}

function loadEmojis() {
    const emojiContainer = document.getElementById('emoji-container');
    emojiContainer.innerHTML = emojis.map(emoji => `
        <span style="cursor: pointer; font-size: 20px; margin: 5px;" onclick="insertEmoji('${emoji}')">${emoji}</span>
    `).join('');
}

function insertEmoji(emoji) {
    const userInput = document.getElementById('user-input');
    userInput.value += emoji;
    userInput.focus();
}
