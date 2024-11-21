import React from 'react';
import './styles/App.css';
import SignUp from './components/SignUp';
import Login from './components/Login';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Render the Sign Up component as landing page*/}
        <Route path="/" element={<SignUp />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
