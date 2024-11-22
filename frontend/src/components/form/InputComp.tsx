import React from "react";
import FileInput from "./FileInput";
import JobInput from "./JobInput";
import CheckToken from '../CheckToken';

const ResumeJobInputForm: React.FC = () => {
  CheckToken()
  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h2>Resume and Job Description Input</h2>
      <FileInput label="Upload Resume:" />
      <JobInput label="Enter Job Description:" softLimit={5000} hardLimit = {7000}/>
    </div>
  );
};

export default ResumeJobInputForm;
