import './App.css';
import React from 'react';
import $ from 'jquery';

function App() {

  const greeting = "Greeting";
  const [messages, setMessages] = React.useState([greeting]);
  const [userMessage, setUserMessage] = React.useState();

  const handleInputChange = event => {
    setUserMessage(event.target.value);
  }

  const handleSubmit = event => {
    $.ajax({
      type: "POST",
      url: "/get_output",
      contentType: "application/json",
      data: JSON.stringify({
          input_text: userMessage
      })
    }).done(response => {
      let updatedMessages = messages.concat(userMessage);
      updatedMessages = updatedMessages.concat(response);
      setMessages(updatedMessages);
    });

    event.preventDefault();
    setUserMessage("");
  };

  return (
    <div className="App">
      <header className="flex flex-row flex-center">
        <div className="center-element block title">
          Chatbot
        </div>
      </header>
      <div className="flex flex-row flex-column-expand content">
        <main className="flex flex-column messages">
          <List list={messages} />
        </main>
        <form
          className="flex flex-row flex-space-between"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            className="input-send"
            onChange={handleInputChange}
            value={userMessage || ""}
          />
          <button type="submit" className="button-send">Send</button>
        </form>
      </div>
    </div>
  );
}

const List = ({ list }) => {
  if (list !== undefined && list.length > 0) {
    return (
      <div>
        {list.map((item, index) =>
          <Item key={index} item={item} />
        )}
      </div>
    );
  } else {
    return (<></>);
  }
};

const Item = ({ item }) => (
  <div className="message">
    <p className="text">{item}</p>
  </div>
);

export default App;
