import React from 'react';
import { Viewer } from '@react-pdf-viewer/core';
import { Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';

const ResumeView: React.FC = () => {
  return (
    <div className="h-full w-full border bg-white shadow-md rounded">
      <h2 className="text-xl font-semibold p-4 border-b">Resume Preview</h2>
      <div className="h-[calc(100%-4rem)]">
        <Worker workerUrl="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js">
          <Viewer
            fileUrl="/resume.pdf"
            // No default layout plugin, just the basic viewer to hide toolbar
          />
        </Worker>
      </div>
    </div>
  );
};

export default ResumeView;
