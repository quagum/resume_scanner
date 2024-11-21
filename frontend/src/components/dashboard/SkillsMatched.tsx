const SkillsMatched = () => {
  const skills = ['React', 'JavaScript', 'Tailwind CSS', 'TypeScript']; // Example data
  
  return (
    <div className="bg-white p-4 shadow rounded">
      <h2 className="text-xl font-semibold mb-4">Skills and Keywords Matched</h2>
      <ul className="list-disc pl-5 space-y-2">
        {skills.map((skill, index) => (
          <li key={index} className="text-gray-700">{skill}</li>
        ))}
      </ul>
    </div>
  );
};

export default SkillsMatched;
