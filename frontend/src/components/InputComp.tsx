import React from "react";
import FileInput from "./FileInput";
import TextAreaInput from "./JobInput";

const ResumeJobInputForm: React.FC = () => {
  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h2>Resume and Job Description Input</h2>
      <FileInput label="Upload Resume:" />
      <TextAreaInput label="Enter Job Description:" />
    </div>
  );
};

export default ResumeJobInputForm;
