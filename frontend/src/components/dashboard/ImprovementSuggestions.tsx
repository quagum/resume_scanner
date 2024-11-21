const ImprovementSuggestions = () => {
  const suggestions = [
    'Include more action verbs.',
    'Highlight key achievements.',
    'Focus on relevant keywords.',
  ]; // Example data

  return (
    <div className="bg-white p-4 shadow rounded">
      <h2 className="text-xl font-semibold mb-4">Improvement Suggestions</h2>
      <ul className="list-disc pl-5 space-y-2">
        {suggestions.map((suggestion, index) => (
          <li key={index} className="text-gray-700">{suggestion}</li>
        ))}
      </ul>
    </div>
  );
};

export default ImprovementSuggestions;
