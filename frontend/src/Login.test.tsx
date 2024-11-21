import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import {describe, expect, jest, test} from '@jest/globals';
import axios from "axios"
import "@testing-library/jest-dom";
import Login from "./Login"

describe("Login Form", () => {
    test("renders all form fields", () => {
        render(<Login />);

        //Check if input fields are present
        expect(screen.getPlaceholderText("Email")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Password")).toBeInTheDocument();

        //Check if the Login button is present
        expect(screen.getByRole("button", { name: "Login" })).toBeInTheDocument();
    });

    test("submits the form with correct data", async () => {

        const data = { message: "Registration successful" };

        //Mock Axios POST request
        axios.post = jest.fn();
        axios.post.mockImplementationOnce(() => 
            Promise.resolve({ data })
        );

        render(<Login />);

        //Simulate user input
        fireEvent.change(screen.getByPlaceholderText("Email"), {
            target: { value: "user@example.com" },
        });

        fireEvent.change(screen.getByPlaceholderText("Password"), {
            target: { value: "password123" },
        });

        //Simulate form submission
        fireEvent.click(screen.getByRole("button", { name: "Login"}));

        //Ensure Axios POST was called with the correct data
        expect(axios.post).toHaveBeenCalledWith("/api/login", {
            email: "user@example.com", 
            password: "password123"
        });

        //Ensure the mock resolved successfully 
        expect(await screen.findByText("")).toBeInTheDocument();
    });
});