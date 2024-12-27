import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/" element={
              <div>
                <h1>Welcome to the Listing App</h1>
                <p>Please <a href="/login">Login</a> or <a href="/signup">Sign Up</a>.</p>
              </div>
            } />
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;
