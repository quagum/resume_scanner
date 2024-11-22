import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './styles/App.css';
import SignUp from './components/SignUp';
import Login from './components/Login';
import ResumeJobInputForm from "./components/InputComp";



const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Render the Login component as landing page*/}
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/inputForm" element={<ResumeJobInputForm />} />
      </Routes>
    </Router>
  );
};

export default App;