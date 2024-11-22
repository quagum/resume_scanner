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
    <div className="input-container">
      <label className="input-label">{label}</label>
      <textarea
        className="input-textarea"
        rows={5}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter the job description here..."
      />
      <div
        className={`char-counter ${
          text.length > 5000 ? "char-counter-exceeded" : ""
        }`}
      >
        {text.length} / 5000 characters
      </div>
      <button className="submit-button" onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
};


export default TextAreaInput;
