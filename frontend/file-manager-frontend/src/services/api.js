import axios from "axios";

const API = axios.create({
  baseURL: "https://4nhqci2v0e.execute-api.ap-south-1.amazonaws.com/dev",
  headers: {
    "Content-Type": "application/json"
  }
});

// Attach IdToken automatically
API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");

  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }

  return req;
});

export default API;