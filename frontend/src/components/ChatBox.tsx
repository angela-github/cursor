import React, { useState } from 'react';

interface ChatBoxProps {
  onSearch: (query: string) => void;
}

const ChatBox: React.FC<ChatBoxProps> = ({ onSearch }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(message);
    setMessage('');
  };

  return (
    <div className="w-1/3 p-4 border-l">
      <h2 className="text-xl font-bold mb-4">Chat</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          className="w-full p-2 border rounded"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter your request..."
          rows={4}
        />
        <button
          type="submit"
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatBox;

