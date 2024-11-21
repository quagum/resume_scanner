import React, { useState } from 'react';
import axios from "axios";

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
            const response = await axios.post("/api/login", formData);
            console.log(response.data);
            setError("");
        } catch (err) {
            setError("Login Failed");
        }
    };
    return (
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
    );
};

export default Login;