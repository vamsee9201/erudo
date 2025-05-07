import React, { useState } from 'react';
import axios from 'axios';
// or use '*' for all origins (not secure for prod)


const AskQuestion = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    // start
    const myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

const raw = JSON.stringify({
  "question": "what did user_id 1 order?",
  "explanation_json": {
    "erudohq-dev.user_orders.orders": {
      "description": "This table stores information about each order placed by users.",
      "columns": {
        "order_id": "Unique identifier for each order.",
        "user_id": "Identifier for the user who placed the order. References the users table.",
        "product": "Name or identifier of the product ordered.",
        "amount": "Total monetary value of the order.",
        "order_date": "Date when the order was placed."
      }
    },
    "erudohq-dev.user_orders.users": {
      "description": "This table contains user profile information.",
      "columns": {
        "user_id": "Unique identifier for each user.",
        "name": "Full name of the user.",
        "email": "Email address of the user."
      }
    }
  }
});

const requestOptions = {
  method: "POST",
  mode: "cors",
  headers: myHeaders,
  body: raw,
  redirect: "follow"
};
let result = {};

  fetch("https://erudo-387613598631.us-central1.run.app/get-answer", requestOptions)
  .then((response) => response.json())
  .then((result) => {
    console.log(result);
    setResponse(result["answer"]);
  }
  )
  .catch((error) => console.error(error));

  
    // end
  };

  return (
    <div className="p-4">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question"
      />
      <button onClick={handleSubmit}>
        Submit
      </button>
      {response && <div>Answer: {response}</div>}
    </div>
  );
};

export default AskQuestion;

// handle submit function needs to call an api to get the answer
