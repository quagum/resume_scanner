import React, { useState } from "react";
import axios from "axios";
import "./style.css";

interface TextAreaInputProps {
  label: string;
}

const TextAreaInput: React.FC<TextAreaInputProps> = ({ label }) => {
  const [text, setText] = useState<string>("");

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/job-description", {
        job_description: text
      });
      alert(response.data.message);
    } catch (error) {
      console.error(error);
      alert("Failed to submit the job description. Please try again.");
    }
  };

  return (
    <div>
      <label>{label}</label>
      <textarea
        rows={5}
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ width: "100%", marginTop: "5px" }}
      />
      <button onClick={handleSubmit} style={{ marginTop: "10px" }}>
        Submit
      </button>
    </div>
  );
};

export default TextAreaInput;
