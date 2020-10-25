import './App.css';
import React from 'react';
import $ from 'jquery';

function App() {

  const greeting = "Greeting";
  const [messages, setMessages] = React.useState([
    {
      text: greeting,
      sender: "bot"
    }
  ]);
  const [userMessage, setUserMessage] = React.useState();

  const handleInputChange = event => {
    setUserMessage(event.target.value);
  }

  const handleSubmit = event => {
    if (!userMessage) {
      event.preventDefault();
      return;
    }

    let updatedMessages = messages.concat({
      text: userMessage,
      sender: "user"
    });
    setMessages(updatedMessages);

    $.ajax({
      type: "POST",
      url: "/get_output",
      contentType: "application/json",
      data: JSON.stringify({
          input_text: userMessage
      })
    }).done(response => {
      updatedMessages = updatedMessages.concat({
        text: response,
        sender: "bot"
      });
      setMessages(updatedMessages);
    });

    event.preventDefault();
    setUserMessage("");
  };

  React.useEffect(() => {
    const element = document.getElementById("messages");
    element.scrollTop = element.scrollHeight;
  }, [messages]);

  return (
    <div className="App">
      <header className="flex flex-row flex-center">
        <div className="center-element block title">
          Chatbot
        </div>
      </header>
      <div className="flex flex-column-expand container content">
        <main id="messages" className="flex messages">
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
      <>
        {list.map((item, index) =>
          <Item key={index} item={item} />
        )}
      </>
    );
  } else {
    return (<></>);
  }
};

const Item = ({ item }) => {
  return (
    <div className="message">
      <span className={`text ${item.sender}`}>{item.text}</span>
    </div>
  );
};

export default App;
