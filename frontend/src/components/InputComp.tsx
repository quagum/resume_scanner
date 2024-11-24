import React from "react";
import FileInput from "./FileInput";
import JobInput from "./JobInput";
import "./style.css"; 

const ResumeJobInputForm: React.FC = () => {
  return (
    <div className="form-container">
      <h2>AI Powered Resume Analyzer</h2>
      <p> Upload your resume and the job posting, and let our advanced analyzer unlock your potential!</p>
      <div className="form-content">
        <div className="file-input-container">
          <FileInput label="Upload Resume:" />
        </div>
        <div className="job-input-container">
          <JobInput label="Enter Job Description:" softLimit={5000} hardLimit={7000} />
        </div>
      </div>
    </div>
  );
};

export default ResumeJobInputForm;
