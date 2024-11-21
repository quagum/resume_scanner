import ResumeFitScore from './ResumeFitScore';
import SkillsMatched from './SkillsMatched';
import ImprovementSuggestions from './ImprovementSuggestions';
import ResumeView from './ResumeView';

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col">
      <div className="flex-grow max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-10 gap-6">
        {/* Left Side - PDF Viewer */}
        <div className="lg:col-span-7 bg-white rounded-lg shadow-md overflow-hidden">
          <ResumeView />
        </div>

        {/* Right Side - Analysis Results */}
        <div className="lg:col-span-3 space-y-6 bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold mb-6">Resume Analysis Results</h1>
          <ResumeFitScore />
          <SkillsMatched />
          <ImprovementSuggestions />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
