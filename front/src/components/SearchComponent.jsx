import React, { useState } from 'react';

const SearchComponent = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/discord-user/?discord_id=${query}&format=json`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      onSearch(data); // Llamar a la función de búsqueda con los datos obtenidos
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">Discord Style Search</h1>

      <div className="flex items-center justify-center mb-6">
        <form onSubmit={handleSubmit} className="relative w-2/3 flex">
          <input
            type="text"
            placeholder="Buscar"
            value={query}
            onChange={handleChange}
            className="flex-grow py-4 pl-12 pr-4 text-gray-200 bg-gray-700 border border-gray-600 rounded-lg text-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <svg className="absolute w-8 h-8 text-gray-400 left-4 top-3" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M12.9 14.32a8 8 0 111.41-1.41l5.29 5.3a1 1 0 01-1.42 1.4l-5.3-5.29zM8 14a6 6 0 100-12 6 6 0 000 12z" clipRule="evenodd"></path>
          </svg>
          <button
            type="submit"
            className="ml-4 py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          >
            Buscar
          </button>
        </form>
      </div>
    </div>
  );
};

export default SearchComponent;
