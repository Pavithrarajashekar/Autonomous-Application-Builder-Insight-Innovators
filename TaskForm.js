import React, { useState } from "react";
import { submitTask } from "../utils/api";

const TaskForm = ({ setTaskId }) => {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    const taskId = await submitTask(prompt);
    setTaskId(taskId);
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter a prompt..."
      />
      <button type="submit">Submit</button>
    </form>
  );
};

export default TaskForm;
