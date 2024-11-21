import React from "react";
import '@testing-library/jest-dom';
import { render, screen, fireEvent } from "@testing-library/react";
import {describe, expect, jest, test} from '@jest/globals';
import axios from "axios"
import "@testing-library/jest-dom";
import SignUp from "./components/SignUp"

describe("SignUp Form", () => {
    test("renders all form fields", () => {
        render(<SignUp />);

        //Check if input fields are present
        expect(screen.getPlaceholderText("Email")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Username")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Password")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Confirm Password")).toBeInTheDocument();

        //Check if the Sign Up button is present
        expect(screen.getByRole("button", { name: "Sign Up" })).toBeInTheDocument();
    });

    test("shows error if passwords do not match", () => {
        render(<SignUp />);
            
            //Simulate user input
            fireEvent.change(screen.getByPlaceholderText("Password"), {
                target: { value: "password123" },
            });

            fireEvent.change(screen.getByPlaceholderText("Confirm Password"), {
                target: { value: "notpassword123" },
            });

            //Simulate form submission
            fireEvent.click(screen.getByRole("button", { name: "Sign Up" }));

            //Check for error message
            expect(screen.getByText("Passwords do not match.")).toBeInTheDocument();
    });

    test("submits the form with correct data", async () => {

        const data = { message: "Registration successful" };

        //Mock Axios POST request
        axios.post = jest.fn();
        axios.post.mockImplementationOnce(() => 
            Promise.resolve({ data })
        );

        render(<SignUp />);

        //Simulate user input
        fireEvent.change(screen.getByPlaceholderText("Email"), {
            target: { value: "user@example.com" },
        });

        fireEvent.change(screen.getByPlaceholderText("Username"), {
            target: { value: "user123" },
        });

        fireEvent.change(screen.getByPlaceholderText("Password"), {
            target: { value: "password123" },
        });

        fireEvent.change(screen.getByPlaceholderText("Confirm Password"), {
            target: { value: "password123" },
        });

        //Simulate form submission
        fireEvent.click(screen.getByRole("button", { name: "Sign Up"}));

        //Ensure Axios POST was called with the correct data
        expect(axios.post).toHaveBeenCalledWith("/api/register", {
            email: "user@example.com", 
            username: "user123",
            password: "password123"
        });

        //Ensure the mock resolved successfully 
        expect(await screen.findByText("")).toBeInTheDocument();
    });
});