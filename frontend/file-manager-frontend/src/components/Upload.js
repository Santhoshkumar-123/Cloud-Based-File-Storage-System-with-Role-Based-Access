import React, { useState } from "react";
import axios from "axios";
import API from "../services/api";

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [tags, setTags] = useState("");

  const upload = async () => {
    if (!selectedFile) {
      alert("Please select a file");
      return;
    }

    try {
      // Step 1: Request presigned URL from backend
      const response = await API.post("/upload", {
        fileName: selectedFile.name,
        tags: tags ? tags.split(",").map(tag => tag.trim()) : []
      });

      console.log("UPLOAD RESPONSE:", response.data);

      // Handle REST API response structure
      let parsed;

      if (response.data.body) {
        parsed = JSON.parse(response.data.body);
      } else {
        parsed = response.data;
      }

      const uploadUrl = parsed.uploadUrl;

      if (!uploadUrl) {
        alert("Upload URL not received");
        return;
      }

      // Step 2: Upload file directly to S3
      await axios.put(uploadUrl, selectedFile, {
        headers: {
          "Content-Type": "application/octet-stream"
        }
      });

      alert("File uploaded successfully!");

      // Reset form
      setSelectedFile(null);
      setTags("");

    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed");
    }
  };

  return (
    <div>
      <h2>Upload File</h2>

      <input
        type="file"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />

      <input
        placeholder="Tags (comma separated)"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
      />

      <button onClick={upload}>Upload</button>
    </div>
  );
};

export default Upload;