import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000"; // Change this to your backend URL

// Function to submit a task (prompt)
export const submitTask = async (prompt) => {
  const response = await axios.post(`${API_BASE_URL}/submit`, { prompt });
  return response.data.task_id;
};

// Function to get task status
export const getTaskStatus = async (taskId) => {
  const response = await axios.get(`${API_BASE_URL}/status/${taskId}`);
  return response.data;
};
