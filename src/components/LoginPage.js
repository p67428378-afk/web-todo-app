/**
 * Module: LoginPage
 * Purpose: React component for a dummy login page.
 * Author: Developer_Agent
 * Created: 2026-02-27
 * Notes: Simulates login and navigates to the to-do list using react-router-dom.
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * LoginPage component provides a simulated login interface.
 * @param {object} props - The component props.
 * @param {function} props.on_login_success - Callback function for successful login simulation.
 * @returns {JSX.Element}
 */
const LoginPage = ({ on_login_success }) => {
  const [email, set_email] = useState('');
  const [username, set_username] = useState('');
  const [password, set_password] = useState('');
  const navigate = useNavigate();

  const handle_login = (event) => {
    event.preventDefault();
    // Simulate successful login
    console.log('Simulating login with:', { email, username, password });
    on_login_success();
    navigate('/todo'); // Navigate to the to-do list page
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Login</h2>
        <form onSubmit={handle_login}>
          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-700 text-sm font-bold mb-2">
              Email:
            </label>
            <input
              type="email"
              id="email"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={email}
              onChange={(e) => set_email(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="username" className="block text-gray-700 text-sm font-bold mb-2">
              Username:
            </label>
            <input
              type="text"
              id="username"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={username}
              onChange={(e) => set_username(e.target.value)}
              required
            />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">
              Password:
            </label>
            <input
              type="password"
              id="password"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
              value={password}
              onChange={(e) => set_password(e.target.value)}
              required
            />
          </div>
          <div className="flex items-center justify-center">
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
