import React, { useState } from "react";
import axios from "axios";
import "../../styles/styles.css"; // Import global styles
import "../../styles/form/file_input.css"


interface JobInputProps {
  label: string;
  softLimit: number; // character count soft limit for character count warning
  hardLimit: number; // character count hard limit restriction
}

const JobInput: React.FC<JobInputProps> = ({ label }) => {
  const [text, setText] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false); 

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (e.target.value.length <= 7000) {
      setText(e.target.value);
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true); // show
    try {
      const response = await axios.post(
        "http://localhost:8000/api/job-description",
        {
          job_description: text,
        }
      );
      alert(response.data.message);
    } catch (error) {
      console.error(error);
      alert("Failed to submit the job description. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="input-container">
      <label className="input-label">{label}</label>
      {isLoading ? (
        <div className="spinner-container">
          <div className="spinner"></div>
          <p>Submitting... Please Wait.</p>
        </div>
      ) : (
        <div>
          <textarea
            className="input-textarea"
            rows={5}
            value={text}
            onChange={handleChange}
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
      )}
    </div>
  );
};

export default JobInput;
