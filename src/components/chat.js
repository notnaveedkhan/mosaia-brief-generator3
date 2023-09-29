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
        const result = await axios.post('/ask', { transcript: 'welcome_message' })
          .catch(error => console.error('API call failed:', error)); // Added catch clause
        const botMessage = result.data.bot;
        setMessages((prevMessages) => {
        const newArr = botMessage.split("<br/>").map((value)=> {
          return {sender: 'bot', text: value}
        });
        return [...prevMessages, ...newArr];
          // return [...prevMessages, {sender: 'bot', text: botMessage}]
        });
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
      var result = response.data.result;
      if (result) {
        setDraft({ header: (result.rough ? 'Draft Project Overview Brief' : ''), text: (result.rough || '') })
        setImproved({ header: (result.brief ? '' : ''), text: (result.brief || '') })
        setProposed({ header: (result.proposed ? 'Proposed Project Overview Brief' : ''), text: (result.proposed || '') })
      } else {
        setDraft({header: '', text: ''});
        setImproved({header: '', text: ''});
        setProposed({header: '', text: ''});
      }
      setMessages((prevMessages) => {
        const newArr = botMessage.split("<br/>").map((value)=> {
          return {sender: 'bot', text: value}
        });
        return [...prevMessages, ...newArr];
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
          <div className="messages" ref={ref}>
            {messages.map((message, index) => {
              return (
                <div key={index * 1000} className={`message ${message.sender}`}>
                  {message.sender === 'bot' ?
                    <div dangerouslySetInnerHTML={{ __html: message.text }} /> :
                    message.text
                  }
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
        <div><h2>{proposed.header}</h2><div dangerouslySetInnerHTML={{ __html: proposed.text }} /></div>
        {improved.text && proposed.text && <hr style={{marginTop:'2rem'}}/>}
        <div><h2>{improved.header}</h2><div dangerouslySetInnerHTML={{ __html: improved.text }} /></div>
        {draft.text && improved.text && <hr style={{marginTop:'2rem'}}/>}
        <div><h2>{draft.header}</h2><div dangerouslySetInnerHTML={{ __html: draft.text }} /></div>
      </div>
    </div>
  );
};

export default Chatbot;
