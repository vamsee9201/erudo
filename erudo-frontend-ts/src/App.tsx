// App.tsx
import React from "react";
import DynamicForm from "./components/DynamicForm";

const schema = {
  table: "user_profile",
  columns: [
    { name: "first_name", type: "text" },
    { name: "age", type: "number" },
    { name: "email", type: "email" },
    { name: "bio", type: "textarea" }
  ]
};

function App() {
  const handleSubmit = (formData: Record<string, string>) => {
    console.log("Submitted:", formData);
  };

  return <DynamicForm schema={schema} onSubmit={handleSubmit} />;
}

export default App;
