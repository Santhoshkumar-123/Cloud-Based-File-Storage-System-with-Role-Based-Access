import React, { useEffect, useState } from "react";
import API from "../services/api";

const History = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await API.get("/history");

      const data = response.data;

      setHistory(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error fetching history:", error);
      setHistory([]);
    }
  };

  return (
    <div>
      <h2>Download History</h2>

      {history.length === 0 && <p>No download history</p>}

      {history.map(item => (
        <div key={item.historyId}>
          File: {item.fileId} — {new Date(item.downloadedAt * 1000).toLocaleString()}
        </div>
      ))}
    </div>
  );
};

export default History;