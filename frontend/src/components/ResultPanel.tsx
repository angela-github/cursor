import React from 'react';
import { Pokemon } from '../types/Pokemon';

interface ResultPanelProps {
  result: Pokemon | null;
  isPosting: boolean;
}

const ResultPanel: React.FC<ResultPanelProps> = ({ result, isPosting }) => {
  if (isPosting) {
    return (
      <div className="w-2/3 p-4">
        <h2 className="text-xl font-bold mb-4">Create a Post</h2>
        {/* TODO: Implement post creation form */}
        <p>Implement post creation form here</p>
      </div>
    );
  }

  return (
    <div className="w-2/3 p-4">
      <h2 className="text-xl font-bold mb-4">Search Result</h2>
      {result ? (
        <div>
          <h3 className="text-lg font-semibold">{result.name}</h3>
          <img src={result.image} alt={result.name} className="my-2" />
          <p>{result.description}</p>
          {/* Add more details as needed */}
        </div>
      ) : (
        <p>No result to display</p>
      )}
    </div>
  );
};

export default ResultPanel;

