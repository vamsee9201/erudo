import React, { useState } from 'react';
import axios from 'axios';

const AskQuestion = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    try {
      const res = await axios.post('http://your-backend-api.com/ask', {
        question: question,
      });
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
