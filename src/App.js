/**
 * Module: App
 * Purpose: Main application component, handles routing and authentication state.
 * Author: Developer_Agent
 * Created: 2026-02-27
 * Notes: Uses react-router-dom for navigation between login and to-do list.
 */

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import TodoList from './components/TodoList';

/**
 * PrivateRoute component to protect routes that require authentication.
 * @param {object} props - The component props.
 * @param {JSX.Element} props.children - Child components to render if authenticated.
 * @param {boolean} props.is_authenticated - Authentication status.
 * @returns {JSX.Element}
 */
const PrivateRoute = ({ children, is_authenticated }) => {
  return is_authenticated ? children : <Navigate to="/login" />;
};

/**
 * App component serves as the main container and router for the application.
 * It manages the simulated authentication state.
 * @returns {JSX.Element}
 */
function App() {
  const [is_logged_in, set_is_logged_in] = useState(false);

  const handle_login_success = () => {
    set_is_logged_in(true);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<LoginPage on_login_success={handle_login_success} />} />
          <Route
            path="/todo"
            element={
              <PrivateRoute is_authenticated={is_logged_in}>
                <TodoList />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<Navigate to="/login" />} /> {/* Redirect any unknown routes to login */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
