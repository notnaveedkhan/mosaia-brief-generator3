import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [draft, setDraft] = useState({ header: '', text: '' });
  const [improved, setImproved] = useState({ header: '', text: '' });
  const [proposed, setProposed] = useState({ header: '', text: '' });
  const ref = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await axios.post('/ask', {transcript: 'welcome_message'})
          .catch(error => console.error('API call failed:', error)); // Added catch clause
        // console.log('Received response:', result.data); // Added log
        const botMessage = result.data.bot;
        // console.log('Bot Message: ', botMessage); // Log botMessage
        setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: botMessage }]);
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }  
    fetchData();
  }, []);

  useEffect(() => {
    if (ref) {
      ref.current.addEventListener('DOMNodeInserted', event => {
        const { currentTarget: target } = event;
        target.scroll({ top: target.scrollHeight, behavior: 'smooth' });
      });
    }
  }, [messages]);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
    setInput('');
    try {
      const response = await axios.post('/ask', { transcript: newMessages }, { withCredentials: true })
        .catch(error => console.error('API call failed:', error)); // Added catch clause
      var botMessage = response.data.bot;
      if (newMessages.length >= 16) {
        const msg_list = botMessage.split('&&');
        botMessage = msg_list[0];
        setDraft({header: (msg_list[0] ? 'Draft Project Overview Brief' : ''), text: (msg_list[0] || '')})
        setImproved({header: (msg_list[2] ? 'Improved Project Overview Brief' : ''), text: (msg_list[2] || '')})
        setProposed({header: (msg_list[3] ? 'Proposed Project Overview Brief' : ''), text: (msg_list[3] || '')})
      } else {
        setDraft({header: 'hello world', text: 'I can do it.'});
        setImproved({header: '', text: ''});
        setProposed({header: '', text: ''});
      }
      setMessages((prevMessages) => {
        return [...prevMessages, { sender: 'bot', text: botMessage }];
      });
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
      <div className="container">
    <div className="left-panel">
      <h1>Save Hours on Project Briefs</h1>
      <h2>We use AI to build them in minutes</h2>
      <div className="chatbot">
        <div className="head">ChatBot</div>
        <div className="messages" ref = {ref}>
          {messages.map((message, index) => {
            return (
              <div key={index * 1000} className={`message ${message.sender}`}>
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
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
    <div className="right-panel">
      <div><h2>{proposed.header}</h2>{proposed.text}</div>
      <div><h2>{improved.header}</h2>{improved.text}</div>
      <div><h2>{draft.header}</h2>{draft.text}</div>
    </div>
  </div>
);
};

export default Chatbot;
