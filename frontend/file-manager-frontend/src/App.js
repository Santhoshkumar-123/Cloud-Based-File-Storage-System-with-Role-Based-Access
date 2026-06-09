import React, { useState } from "react";
import { jwtDecode } from "jwt-decode";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";

function App() {
  const [user, setUser] = useState(localStorage.getItem("token"));

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  if (!user) {
    return <Login setUser={setUser} />;
  }

  const decoded = jwtDecode(user);
  const role = decoded["cognito:groups"]
    ? decoded["cognito:groups"][0]
    : "Viewer";

  return <Dashboard role={role} logout={logout} />;
}

export default App;