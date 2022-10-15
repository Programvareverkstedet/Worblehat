import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import FrontPage from './FrontPage';
import BooksPage from './Books';
import NavBar from './components/NavBar';


function App() {
  return (
    <div className="App">¨
    <NavBar />
      <Router>
      <Routes>
        {/* Sett opp en navbar ellerno */}

        <Route path="/" element={<FrontPage />} />
        <Route path="/books" element={<BooksPage />} />
      </Routes>
      </Router>
    </div>
  );
}

export default App;
