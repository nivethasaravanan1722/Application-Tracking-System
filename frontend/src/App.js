import React from 'react';
import ResumeUpload from './components/ResumeUpload';

import Example from './components/Navbar';

function App() {
  return (
    <div>
      <Example />
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <ResumeUpload />
      </div>
    </div>
  
  );
}

export default App;
