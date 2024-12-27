import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/" element={
              <div>
                <h1>Welcome to the App</h1>
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
