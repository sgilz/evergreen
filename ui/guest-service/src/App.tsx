import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar';
import CreateChain from './pages/CreateChain';
import Home from './pages/Home';

function App() {
  if (!localStorage.getItem('theme')) localStorage.setItem('theme', 'dark');

  return (
    <div className="relative flex flex-col w-full h-full">
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create-chain" element={<CreateChain />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
