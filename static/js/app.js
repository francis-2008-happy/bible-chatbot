document.addEventListener('DOMContentLoaded', function () {
    const questionInput = document.getElementById('question-input');
    const askButton = document.getElementById('ask-button');
    const chatHistory = document.getElementById('chat-history');
    const referencesContainer = document.getElementById('references');

    askButton.addEventListener('click', sendQuestion);
    questionInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendQuestion();
        }
    });

    function sendQuestion() {
        const question = questionInput.value.trim();
        if (!question) return;

        // Add user question to chat
        addMessage(question, 'user');
        questionInput.value = '';

        // Show loading indicator
        const loadingId = 'loading-' + Date.now();
        chatHistory.innerHTML += `
            <div id="${loadingId}" class="message assistant-message loading">
                Thinking...
            </div>
        `;
        chatHistory.scrollTop = chatHistory.scrollHeight;

        // Send to backend
        fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        })
            .then(response => response.json())
            .then(data => {
                // Remove loading indicator
                document.getElementById(loadingId).remove();

                // Add assistant response
                addMessage(data.answer, 'assistant');

                // Show references
                showReferences(data.reviews);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById(loadingId).remove();
                addMessage("Sorry, there was an error processing your question.", 'assistant');
            });
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender + '-message');

        if (sender === 'assistant') {
            const botName = document.createElement('div');
            botName.classList.add('bot-name');
            botName.textContent = data.bot_name || 'Assistant';
            messageDiv.appendChild(botName);
        }

        const messageText = document.createElement('div');
        messageText.classList.add('message-text');
        messageText.textContent = text;
        messageDiv.appendChild(messageText);

        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function showReferences(reviews) {
        referencesContainer.innerHTML = '';

        if (!reviews || reviews.length === 0) {
            referencesContainer.innerHTML = '<p>No references found</p>';
            return;
        }

        reviews.forEach((review, index) => {
            const referenceDiv = document.createElement('div');
            referenceDiv.classList.add('reference');

            // Extract title and content (adjust based on your actual review structure)
            let title = `Reference ${index + 1}`;
            let content = review;

            if (typeof review === 'object') {
                title = review.metadata?.title || title;
                content = review.page_content || content;
            }

            referenceDiv.innerHTML = `
                <h4>${title}</h4>
                <p>${content}</p>
            `;

            referencesContainer.appendChild(referenceDiv);
        });
    }
});


// About modal functionality
const aboutButton = document.getElementById('about-button');
const modal = document.getElementById('about-modal');
const span = document.getElementsByClassName('close')[0];

aboutButton.onclick = function () {
    modal.style.display = "block";
}

span.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}