import React, { useEffect, useState } from "react";
import API from "../services/api";

const FileList = ({ role }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  // =========================
  // Fetch Files
  // =========================
  const fetchFiles = async () => {
    try {
      setLoading(true);
      const response = await API.get("/files");

      // If your backend returns raw list
      setFiles(response.data || []);

    } catch (error) {
      console.error("Error fetching files:", error);
      setFiles([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  // =========================
  // Download File
  // =========================
  const handleDownload = async (fileId) => {
    try {
      const response = await API.post("/download", { fileId });

      const downloadUrl = response.data.downloadUrl;

      if (!downloadUrl) {
        alert("Download URL not received");
        return;
      }

      window.open(downloadUrl, "_blank");

    } catch (error) {
      console.error("Download failed:", error);
      alert("Download failed");
    }
  };

  // =========================
  // Delete File (Admin Only)
  // =========================
  const handleDelete = async (fileId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this file?"
    );

    if (!confirmDelete) return;

    try {
      await API.delete("/delete", {
        data: { fileId }
      });

      alert("File deleted successfully");

      // Refresh file list
      fetchFiles();

    } catch (error) {
      console.error("Delete failed:", error);
      alert("Delete failed");
    }
  };

  return (
    <div>
      <h3>Files</h3>

      {loading ? (
        <p>Loading files...</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>File Name</th>
              <th>Owner</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {files.length > 0 ? (
              files.map((file) => (
                <tr key={file.fileId}>
                  <td>{file.fileName}</td>
                  <td>{file.owner}</td>

                  <td>
                    <button
                      className="aws-button"
                      onClick={() => handleDownload(file.fileId)}
                    >
                      Download
                    </button>

                    {/* 🔐 Delete only visible for Admin */}
                    {role === "Admin" && (
                      <button
                        className="aws-button"
                        style={{
                          marginLeft: "8px",
                          backgroundColor: "#d13212"
                        }}
                        onClick={() => handleDelete(file.fileId)}
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3">No files available</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default FileList;