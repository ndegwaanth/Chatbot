document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('userInput');
    const sendBtn = document.querySelector('.btn-send');
    const chatMessages = document.querySelector('.chatbot-messages');
    const typingIndicator = document.querySelector('.typing-indicator');
    
    // Initially hide typing indicator
    typingIndicator.style.display = 'none';
    
    // Function to add a new message
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'} animate__animated animate__fadeInUp`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = `<i class="fas ${isUser ? 'fa-user' : 'fa-robot'}"></i>`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<p>${content}</p><small>${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</small>`;
        
        if(!isUser) {
            messageDiv.appendChild(avatarDiv);
            messageDiv.appendChild(contentDiv);
        } else {
            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(avatarDiv);
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Send message function
    function sendMessage() {
        const message = userInput.value.trim();
        if(message) {
            addMessage(message, true);
            userInput.value = '';
            
            // Show typing indicator
            typingIndicator.style.display = 'flex';
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Simulate bot response after delay
            setTimeout(() => {
                typingIndicator.style.display = 'none';
                const responses = [
                    "I'm analyzing your request... Here's what I found!",
                    "Fascinating question! The answer is...",
                    "✨ According to my neural networks:",
                    "Let me crunch some numbers... Here's the result!",
                    "Great inquiry! My database suggests:"
                ];
                const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                addMessage(randomResponse);
            }, 2000);
        }
    }
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if(e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Quick action buttons
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.textContent.trim();
            addMessage(`You clicked: ${action}`, true);
            
            // Show typing indicator
            typingIndicator.style.display = 'flex';
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            setTimeout(() => {
                typingIndicator.style.display = 'none';
                addMessage(`I can help you with ${action.toLowerCase()}! What specifically do you need?`);
            }, 1500);
        });
    });
    
    // FAB button
    document.querySelector('.fab').addEventListener('click', function() {
        this.classList.toggle('animate__rotateIn');
        addMessage("You discovered a secret feature! What would you like to explore?");
    });
});