// ✅ TS version
import { useState } from 'react';
// ❌ JSX version had: import axios from 'axios'; (but it was unused)

const AskQuestion = () => {
  // ✅ TS: useState<string> gives type safety for inputs and responses
  // ❌ JSX: const [question, setQuestion] = useState('');
  const [question, setQuestion] = useState<string>('');
  const [response, setResponse] = useState<string>('');

  const handleSubmit = async () => {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    // ✅ TS: requestBody is typed as a generic object (Record<string, unknown>)
    // ❌ JSX: used a raw JSON.stringify(...) inline
    const requestBody: Record<string, unknown> = {
      question: question || "what did user_id 1 order?", // use fallback
      explanation_json: {
        "erudohq-dev.user_orders.orders": {
          description: "This table stores information about each order placed by users.",
          columns: {
            order_id: "Unique identifier for each order.",
            user_id: "Identifier for the user who placed the order. References the users table.",
            product: "Name or identifier of the product ordered.",
            amount: "Total monetary value of the order.",
            order_date: "Date when the order was placed."
          }
        },
        "erudohq-dev.user_orders.users": {
          description: "This table contains user profile information.",
          columns: {
            user_id: "Unique identifier for each user.",
            name: "Full name of the user.",
            email: "Email address of the user."
          }
        }
      }
    };

    try {
      const res = await fetch("https://erudo-387613598631.us-central1.run.app/get-answer", {
        method: "POST",
        mode: "cors",
        headers: myHeaders,
        body: JSON.stringify(requestBody),
        redirect: "follow"
      });

      // ✅ TS: typed response as an object with `answer: string`
      // ❌ JSX: no type declared, just .then((result) => ...)
      const data: { answer: string } = await res.json();
      console.log(data);
      setResponse(data.answer);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  return (
    <div className="p-4">
      <input
        type="text"
        value={question}
        // ✅ TS: typed the event as React.ChangeEvent<HTMLInputElement>
        // ❌ JSX: (e) => setQuestion(e.target.value)
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuestion(e.target.value)}
        placeholder="Ask a question"
        className="border p-2 mr-2"
      />
      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Submit
      </button>
      {/* ✅ Same as JSX, conditional rendering of response */}
      {response && <div className="mt-4">Answer: {response}</div>}
    </div>
  );
};

export default AskQuestion;
