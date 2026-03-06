/**
 * Module: App
 * Purpose: Main application component, handles routing and authentication state.
 * Author: Developer_Agent
 * Created: 2026-02-27
 * Notes: Switches between LoginPage and TodoList based on login status.
 */

import React, { useState } from 'react';
import LoginPage from './components/LoginPage';
import TodoList from './components/TodoList';

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
    <div className="App">
      {is_logged_in ? (
        <TodoList />
      ) : (
        <LoginPage on_login_success={handle_login_success} />
      )}
    </div>
  );
}

export default App;
