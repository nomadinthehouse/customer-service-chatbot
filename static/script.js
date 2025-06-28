// Get references to DOM elements
const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");

// Function to add messages to the chatbox
function addMessage(content, sender) {
    const message = document.createElement("div"); // Create a new div for the message
    message.classList.add("message", sender); // Add "message" and "user" or "bot" class
    message.innerText = content; // Set the message content
    chatbox.appendChild(message); // Add the message to the chatbox
    chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom of the chatbox
  }

// Function to send user input to the backend
async function sendMessage() {
  const message = userInput.value.trim();
  if (message === "") return;

  // Add user message to the chatbox
  addMessage(message, "user");

  // Clear the input field
  userInput.value = "";

  try {
    // Send the message to the Flask backend
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    // Parse and display the chatbot's response
    const data = await response.json();
    if (data.reply) {
      addMessage(data.reply, "bot");
    } else if (data.error) {
      addMessage("Error: " + data.error, "bot");
    }
  } catch (error) {
    addMessage("Error: Unable to connect to the server.", "bot");
  }
}

// Event listeners
sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});