import React from 'react';
import { Search, MapPin } from 'lucide-react';

const SearchBar = () => {
  return (
    <div className="max-w-5xl mx-auto bg-white rounded-full shadow-[0_10px_40px_rgba(0,0,0,0.08)] p-3 flex items-center gap-2">
      <div className="flex-1 flex items-center gap-3 px-6">
        <Search className="w-5 h-5 text-[#CCCCCC]" />
        <input 
          type="text" 
          placeholder="Name or Specialty" 
          className="w-full outline-none text-gray-600 placeholder-[#CCCCCC] font-medium" 
        />
      </div>
      
      <div className="h-10 w-[1px] bg-[#EEEEEE]"></div>
      
      <div className="flex-1 flex items-center gap-3 px-6">
        <MapPin className="w-5 h-5 text-[#CCCCCC]" />
        <input 
          type="text" 
          placeholder="Location" 
          className="w-full outline-none text-gray-600 placeholder-[#CCCCCC] font-medium" 
        />
      </div>
      
      <button className="px-10 py-4 bg-[#FFDDC1] text-white rounded-full hover:bg-[#ffcfab] transition-colors font-bold text-sm uppercase">
        Search
      </button>
    </div>
  );
};

export default SearchBar;