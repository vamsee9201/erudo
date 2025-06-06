import React, {useState} from 'react';

interface FormData {
    name: string;
    email: string;
    message: string;
}

interface MyFormProps {
    onSubmit: (data:FormData) => void;
}

function MyForm({onSubmit}:MyFormProps) {

    const [formData,setFormData] = useState<FormData>({
        name:"",
        email:"",
        message:""
    })

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) => {
        const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    }

    return (
        <form onSubmit={handleSubmit}>
          <div>
            <label>Name:</label>
            <input name="name" value={formData.name} onChange={handleChange} />
          </div>
    
          <div>
            <label>Email:</label>
            <input name="email" value={formData.email} onChange={handleChange} />
          </div>
    
          <div>
            <label>Message:</label>
            <textarea name="message" value={formData.message} onChange={handleChange} />
          </div>
    
          <button type="submit">Submit</button>
        </form>
      );



    
}

export default MyForm;