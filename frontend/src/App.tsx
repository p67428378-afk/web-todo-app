import React from 'react';
import LeaveApplicationForm from './components/LeaveApplicationForm';
import LeaveStatusDashboard from './components/LeaveStatusDashboard';

function App() {
  return (
    <div className="App">
      <h1>Employee Leave Portal</h1>
      <LeaveApplicationForm />
      <LeaveStatusDashboard />
    </div>
  );
}

export default App;
