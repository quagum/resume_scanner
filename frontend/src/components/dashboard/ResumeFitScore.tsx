import ProgressBar from '../shared/ProgressBar';

const ResumeFitScore = () => {
  const fitScore = 78; // Example score
  
  return (
    <div className="bg-white p-4 shadow rounded">
      <h2 className="text-xl font-semibold mb-4">Resume Fit Score</h2>
      <div className="flex items-center space-x-4">
        <ProgressBar value={fitScore} />
        <span className="text-lg font-medium">{fitScore}%</span>
      </div>
    </div>
  );
};

export default ResumeFitScore;
