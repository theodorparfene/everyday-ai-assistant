// Send Chat Message
async function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const responseDiv = document.getElementById('response');

    if (!userInput.trim()) {
        alert("Please enter a question!");
        return;
    }

    responseDiv.textContent = "Thinking...";
    responseDiv.classList.add("loading");

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: userInput })
        });

        const data = await response.json();
        responseDiv.textContent = data.response || `Error: ${data.error}`;
    } catch (error) {
        responseDiv.textContent = `Error: ${error.message}`;
    } finally {
        responseDiv.classList.remove("loading");
    }
}