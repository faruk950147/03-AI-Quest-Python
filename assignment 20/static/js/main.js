
document.addEventListener("DOMContentLoaded", function () {

    // Elements
    const chatApp = document.getElementById("chat-app");
    const contacts = document.querySelectorAll(".contact");

    const chatName = document.getElementById("chatName");
    const chatStatus = document.getElementById("chatStatus");
    const headerAvatar = document.getElementById("headerAvatar");

    const messages = document.getElementById("messages");
    const messageInput = document.getElementById("messageInput");

    const sendBtn = document.getElementById("sendBtn");
    const searchInput = document.getElementById("search");
    const backBtn = document.getElementById("backBtn");

    // Active contact
    let activeContact = document.querySelector(".contact.active");

    // Store conversations
    const conversations = {};

    // Initial conversation
    contacts.forEach(contact => {
        const name = contact.dataset.name;

        if (contact === activeContact) {
            conversations[name] = messages.innerHTML;
        } else {
            conversations[name] = "";
        }
    });


    // Get current time
    function getCurrentTime() {

        return new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        });

    }


    // Get initials
    function getInitials(name) {

        return name
            .split(" ")
            .map(word => word.charAt(0))
            .join("")
            .toUpperCase();

    }


    // Update chat header
    function updateHeader(contact) {

        const name = contact.dataset.name;
        const status = contact.dataset.status;

        chatName.textContent = name;

        chatStatus.textContent = status;

        chatStatus.className = status === "Online"
            ? "text-success"
            : "text-secondary";

        // Update avatar
        headerAvatar.textContent = getInitials(name);

        // Remove previous online indicator
        const oldOnline = headerAvatar.querySelector(".online");

        if (oldOnline) {
            oldOnline.remove();
        }

        // Add online indicator
        if (status === "Online") {

            const online = document.createElement("div");

            online.className = "online";

            headerAvatar.appendChild(online);

        }

    }


    // Create message
    function createMessage(text, type) {

        const message = document.createElement("div");

        message.className = `message ${type}`;

        const bubble = document.createElement("div");

        bubble.className = "bubble";

        // Safe text rendering
        bubble.appendChild(
            document.createTextNode(text)
        );

        const time = document.createElement("span");

        time.className = "time";

        time.textContent = getCurrentTime();

        if (type === "sent") {
            time.textContent += " ✓✓";
        }

        bubble.appendChild(time);

        message.appendChild(bubble);

        return message;

    }


    // Select contact
    function selectContact(contact) {

        if (!contact) return;

        // Save previous conversation
        if (activeContact) {

            conversations[activeContact.dataset.name] =
                messages.innerHTML;

        }

        // Update active contact
        contacts.forEach(item => {
            item.classList.remove("active");
        });

        contact.classList.add("active");

        activeContact = contact;

        // Update header
        updateHeader(contact);

        // Load conversation
        const name = contact.dataset.name;

        messages.innerHTML = conversations[name] || "";

        // Open mobile chat
        chatApp.classList.add("chat-open");

        // Scroll bottom
        messages.scrollTop = messages.scrollHeight;

    }


    // Contact click
    contacts.forEach(contact => {

        contact.addEventListener("click", function () {

            selectContact(this);

        });

    });


    // Update contact last message
    function updateContactMessage(text) {

        if (!activeContact) return;

        const lastMessage =
            activeContact.querySelector(".last-message");

        const timeElement =
            activeContact.querySelector("small");

        lastMessage.textContent = text;

        timeElement.textContent = getCurrentTime();

    }


    // Send message
    function sendMessage() {

        const text = messageInput.value.trim();

        if (!text || !activeContact) return;

        // Create message
        const message = createMessage(text, "sent");

        // Add to chat
        messages.appendChild(message);

        // Save conversation
        conversations[activeContact.dataset.name] =
            messages.innerHTML;

        // Update contact preview
        updateContactMessage(text);

        // Clear input
        messageInput.value = "";

        // Scroll to bottom
        messages.scrollTop = messages.scrollHeight;

        messageInput.focus();

    }


    // Send button
    sendBtn.addEventListener("click", sendMessage);


    // Enter key
    messageInput.addEventListener("keydown", function (event) {

        if (event.key === "Enter" && !event.shiftKey) {

            event.preventDefault();

            sendMessage();

        }

    });


    // Search contacts
    searchInput.addEventListener("input", function () {

        const searchValue = this.value.trim().toLowerCase();

        contacts.forEach(contact => {

            const name =
                contact.dataset.name.toLowerCase();

            contact.style.display =
                name.includes(searchValue) ? "flex" : "none";

        });

    });


    // Mobile back button
    backBtn.addEventListener("click", function () {

        chatApp.classList.remove("chat-open");

    });


    // Initial scroll
    messages.scrollTop = messages.scrollHeight;

});
