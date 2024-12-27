import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
import HeroSection from './components/HeroSection';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="bg-white min-h-screen flex flex-col items-center justify-center text-gray-800 p-5 shadow-md">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/" element={
              <main>
                <HeroSection />
              </main>
            } />
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;
