import { useEffect, useRef, useState } from 'react';
import './ChatWidget.css';

const initialMessages = [
  {
    sender: 'assistant',
    text: 'Hi! I can help you explore products or review your orders. Ask me anything about the store.',
  },
];

function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isOpen]);

  const addMessage = (sender, text) => {
    setMessages((prev) => [...prev, { sender, text }]);
  };

  const generateReply = async (question) => {
    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "query": question }),
      });

      const data = await response.json();

      console.log(data)

      if (!response.ok) {
        throw new Error(data.detail || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('Error calling query endpoint:', error);
      return 'Sorry, I could not reach the agent right now.';
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    addMessage('user', trimmed);
    setInput('');

    const reply = await generateReply(trimmed);
    addMessage('assistant', reply);
  };

  return (
    <div className={`chat-widget ${isOpen ? 'chat-widget--open' : ''}`}>
      <div className="chat-widget__header" onClick={() => setIsOpen((open) => !open)}>
        <span>Shopping AI</span>
        <button type="button" className="chat-widget__toggle">
          {isOpen ? '−' : '+'}
        </button>
      </div>

      {isOpen ? (
        <div className="chat-widget__panel">
          <div className="chat-widget__messages">
            {messages.map((message, index) => (
              <div
                key={`${message.sender}-${index}`}
                className={`chat-widget__message chat-widget__message--${message.sender}`}
              >
                {message.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <form className="chat-widget__form" onSubmit={handleSubmit}>
            <input
              className="chat-widget__input"
              type="text"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask about products or orders..."
            />
            <button className="chat-widget__send" type="submit">
              Send
            </button>
          </form>
        </div>
      ) : null}
    </div>
  );
}

export default ChatWidget;
