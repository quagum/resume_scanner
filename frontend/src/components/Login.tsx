import React, { useState } from 'react';
import axios from "axios";
import "../styles/styles.css"; // General styles
import "../styles/login.css"; // Page-specific styles

const Login: React.FC = () => {
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [error, setError] = useState("");

    //Setting values for formData after user input 
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    //Using Axios to send to backend
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://localhost:8000/api/login", formData);
            //Check to see if JWT token is received from backend. If so, store in localStorage.
            if (response.data.token) {
                localStorage.setItem("jwtToken", response.data.token);
                alert("Login successful!")
                setError("");

                //Redirect to the dashboard
                window.location.href = "/dashboard";
            } else {
                alert("Login failed: No token returned.");
                setError("Login failed: No token returned.");
            }
        } catch (err) {
            alert("Failed to login. Please try again.");
            setError("Login Failed");
        }
    };
    return (
        <div className="container">
            <div className="form-wrapper login-wrapper">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <input 
                        type="email"
                        name="email"
                        placeholder="Email"
                        onChange={handleChange}
                    />
                    <input 
                        type="password"
                        name="password"
                        placeholder="Password"
                        onChange={handleChange}
                    />
                    {error && <p>{error}</p>}
                    <button type="submit">Login</button>
                </form>
                <div className="link">
                    <a href="/signup">Don't have an account? Sign up</a>
                </div>
            </div>
        </div>
    );
};

export default Login;