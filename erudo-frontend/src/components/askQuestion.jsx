import React, { useState } from 'react';
import axios from 'axios';

const AskQuestion = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    try {
      const res = await axios.post(
        'https://erudo-387613598631.us-central1.run.app/get-answer',
        {
          question: 'what did user_id 1 order?',
          explanation_json: {
            'erudohq-dev.user_orders.orders': {
              description: 'This table stores information about each order placed by users.',
              columns: {
                order_id: 'Unique identifier for each order.',
                user_id: 'Identifier for the user who placed the order. References the users table.',
                product: 'Name or identifier of the product ordered.',
                amount: 'Total monetary value of the order.',
                order_date: 'Date when the order was placed.'
              }
            },
            'erudohq-dev.user_orders.users': {
              description: 'This table contains user profile information.',
              columns: {
                user_id: 'Unique identifier for each user.',
                name: 'Full name of the user.',
                email: 'Email address of the user.'
              }
            }
          }
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      ;
      setResponse(res.data.answer); // adjust based on your API response structure
    } catch (error) {
      console.error(error);
      setResponse('An error occurred.');
    }
  };

  return (
    <div className="p-4">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question"
        className="border px-2 py-1 w-full mb-2"
      />
      <button onClick={handleSubmit} className="bg-blue-500 text-white px-4 py-1 rounded">
        Submit
      </button>
      {response && <div className="mt-4">Response: {response}</div>}
    </div>
  );
};

export default AskQuestion;
