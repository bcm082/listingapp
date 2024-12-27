import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
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
              <div>
                <h1 className="text-3xl font-bold">Welcome to the Listing App</h1>
                <p className="mt-4">Please <a href="/login" className="text-blue-500 hover:underline">Login</a> or <a href="/signup" className="text-blue-500 hover:underline">Sign Up</a>.</p>
              </div>
            } />
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;
