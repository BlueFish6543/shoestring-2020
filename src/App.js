import './App.css';
import React from 'react';
import $ from 'jquery';

function App() {
  $.ajax({
      type: "POST",
      url: "/get_output",
      contentType: "application/json",
      data: JSON.stringify({
          input_text: "Hello",
          startup: true
      })
  }).done(output => {
      console.log(output);
  });

  return (
    <div className="App">
      <p>Test</p>
    </div>
  );
}

export default App;
