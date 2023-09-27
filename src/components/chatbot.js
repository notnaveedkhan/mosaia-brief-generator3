import React, { useState, useEffect } from 'react'; 
import axios from 'axios';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => { 
    const fetchData = async () => {
      try {
        const result = await axios.post('/ask', {transcript: 'welcome_message'})
          .catch(error => console.error('API call failed:', error)); // Added catch clause
        console.log('Received response:', result.data); // Added log
        const botMessage = result.data.bot;
        console.log('Bot Message: ', botMessage); // Log botMessage
        setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: botMessage }]);
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }  
    fetchData();
  }, []);

  useEffect(() => {
    console.log('Current messages:', messages);
  }, [messages]);

  const sendMessage = () => {
    if (input.trim() === '') return;

    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await axios.post('/ask', { transcript: newMessages }, { withCredentials: true })
        .catch(error => console.error('API call failed:', error)); // Added catch clause
      console.log('Received response:', response.data); // Added log
      const botMessage = response.data.bot;
      console.log('Bot Message: ', botMessage); // Log botMessage
      setMessages((prevMessages) => {
        console.log('PrevMessages: ', prevMessages);
        console.log('New Message: ', botMessage);
        return [...prevMessages, { sender: 'bot', text: botMessage }];
      });
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="chatbot">
      <div className="messages">
        {messages.map((message, index) => {
          console.log('Rendering message:', message);
          return (
            <div key={index} className={`message ${message.sender}`}>
              {message.text}
            </div>
          );
        })}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send message123</button>
      </div>
    </div>
  );
};

export default Chatbot;
