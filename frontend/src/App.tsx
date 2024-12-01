import React, { useState } from 'react';
import ChatBox from './components/ChatBox';
import ResultPanel from './components/ResultPanel';
import { Pokemon } from './types/Pokemon';

const App: React.FC = () => {
  const [searchResult, setSearchResult] = useState<Pokemon | null>(null);
  const [isPosting, setIsPosting] = useState<boolean>(false);

  const handleSearch = async (query: string) => {
    try {
      const response = await fetch('http://192.168.1.176:8880/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      if (data.found) {
        setSearchResult(data.pokemon);
      } else {
        setIsPosting(true);
      }
    } catch (error) {
      console.error('Error:', error);
      // Handle the error appropriately (e.g., show an error message to the user)
    }
  };

  return (
    <div className="flex h-screen">
      <ResultPanel result={searchResult} isPosting={isPosting} />
      <ChatBox onSearch={handleSearch} />
    </div>
  );
};

export default App;

