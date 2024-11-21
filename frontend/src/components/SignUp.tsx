import React, { useState } from 'react';
import axios from "axios";
import "./styles/styles.css"; // General styles
import "./styles/signup.css"; // Page-specific styles


const SignUp: React.FC = () => {
    const [formData, setFormData] = useState({
        email: "", 
        password: "",
        confirmPassword: "",
        username: "", 

    });
    const [error, setError] = useState("");
    
    //Setting values for formData after user input
    const handleChange = (e = React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        //Validate passwords match
        if (formData.password !== formData.confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        //Prepare payload for backend
        const payload = {
            email: formData.email, 
            password: formData.password,
            username: formData.username,
        };

        //Using Axios to send to backend
        try {
            const response = await axios.post("/api/register", payload);
            console.log("Registration successful:", response.data);
            setError("");
        } catch (err) {
            setError("Registration failed")
        }
    };

    return (
        <div className="container">
            <div className="form-wrapper signup-wrapper">
                <h2>Sign Up</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={formData.email}
                        onChange={handleChange}
                    />
                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        value={formData.username}
                        onChange={handleChange}
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={formData.password}
                        onChange={handleChange}
                    />
                    <input
                        type="password"
                        name="confirmPassword"
                        placeholder="Confirm Password"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                    />
                    {error && <p>{error}</p>}
                    <button type="submit">Sign Up</button>
                </form>
                <div className="link">
                    <a href="/login">Already have an account? Login here</a> 
                </div>   
            </div>
        </div>
    );
};

export default SignUp;
