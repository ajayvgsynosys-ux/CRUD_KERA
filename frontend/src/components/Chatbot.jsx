import { useState } from "react";

function Chatbot({ apiUrl }) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "bot",
      text: "Hello! Ask me anything about the employees.",
    },
  ]);
  const [loading, setLoading] = useState(false);

  async function sendMessage(event) {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || loading) {
      return;
    }

    setMessages((current) => [
      ...current,
      {
        id: Date.now(),
        sender: "user",
        text: trimmedMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: trimmedMessage,
        }),
      });

      if (!response.ok) {
        throw new Error("Chat request failed");
      }

      const data = await response.json();

      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          sender: "bot",
          text: data.response,
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          sender: "bot",
          text: "Unable to connect to the server. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card chatbot-card">
      <div className="card-header">
        <h2>Employee Assistant</h2>
        <p>Ask about names, ages, emails, or employee counts.</p>
      </div>

      <div className="chat-messages">
        {messages.map((item) => (
          <div
            key={item.id}
            className={`message-row ${
              item.sender === "user" ? "user-row" : "bot-row"
            }`}
          >
            <div
              className={`message ${
                item.sender === "user" ? "user-message" : "bot-message"
              }`}
            >
              <span className="message-label">
                {item.sender === "user" ? "You" : "Bot"}
              </span>
              <div className="message-text">{item.text}</div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row bot-row">
            <div className="message bot-message">
              <span className="message-label">Bot</span>
              <div className="message-text">Thinking...</div>
            </div>
          </div>
        )}
      </div>

      <form className="chat-form" onSubmit={sendMessage}>
        <input
          type="text"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Type your question..."
          disabled={loading}
        />

        <button type="submit" disabled={loading || !message.trim()}>
          Send
        </button>
      </form>
    </section>
  );
}

export default Chatbot;
