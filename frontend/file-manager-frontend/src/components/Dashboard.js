import React from "react";
import Upload from "./Upload";
import FileList from "./FileList";
import History from "./History";

const Dashboard = ({ role, logout }) => {

  return (
    <div>
      <h1>File Manager</h1>
      <h3>Role: {role}</h3>

      {/* Upload only for Admin & Editor */}
      {(role === "Admin" || role === "Editor") && <Upload />}

      {/* ✅ Pass role here */}
      <FileList role={role} />

      <History />

      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default Dashboard;