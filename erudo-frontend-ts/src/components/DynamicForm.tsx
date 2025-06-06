// DynamicForm.tsx
import React, { useState } from "react";


// why interface
interface Column {
  name: string;
  type: "text" | "number" | "email" | "textarea";
}


// why schema
interface Schema {
  table: string;
  columns: Column[];
}


// why interface
interface DynamicFormProps {
  schema: Schema;
  onSubmit: (formData: Record<string, string>) => void;
}



function DynamicForm({ schema, onSubmit }: DynamicFormProps) {
  // why the parameters are unpacked like this. what is the word for this?
  // ✅ Best Practice: Initialize state based on dynamic schema
  const [formData, setFormData] = useState<Record<string, string>>(
    Object.fromEntries(schema.columns.map(col => [col.name, ""]))
  );

  // ✅ Best Practice: Typed change handler using union type for input/textarea
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // ✅ Best Practice: Prevent default form submission behavior
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{schema.table}</h2>

      {schema.columns.map((col) => (
        <div key={col.name}>
          <label>{col.name}</label>
          {col.type === "textarea" ? (
            <textarea
              name={col.name}
              value={formData[col.name]}
              onChange={handleChange}
            />
          ) : (
            <input
              type={col.type}
              name={col.name}
              value={formData[col.name]}
              onChange={handleChange}
            />
          )}
        </div>
      ))}

      <button type="submit">Submit</button>
    </form>
  );
}

export default DynamicForm;
