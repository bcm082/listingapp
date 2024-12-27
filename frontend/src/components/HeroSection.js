import React from 'react';

function HeroSection() {
  return (
    <section className="bg-blue-500 text-white py-20">
      <div className="container mx-auto px-6">
        <h1 className="text-4xl font-bold mb-4">Welcome to Our App</h1>
        <p className="text-lg mb-6">Discover amazing features and seamless experiences.</p>
        <button className="bg-white text-blue-500 px-4 py-2 rounded">Get Started</button>
      </div>
    </section>
  );
}

export default HeroSection;
