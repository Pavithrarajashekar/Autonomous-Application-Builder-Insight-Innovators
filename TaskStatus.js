import React, { useEffect, useState } from "react";
import { getTaskStatus } from "../utils/api";

const TaskStatus = ({ taskId }) => {
  const [status, setStatus] = useState("Pending...");
  const [result, setResult] = useState("");

  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(async () => {
      const data = await getTaskStatus(taskId);
      setStatus(data.status);

      if (data.status === "SUCCESS") {
        setResult(data.result);
        clearInterval(interval);
      }
    }, 3000); // Check every 3 seconds

    return () => clearInterval(interval);
  }, [taskId]);

  return (
    <div className="task-status">
      <h3>Task Status: {status}</h3>
      {result && (
        <div>
          <h4>Result:</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default TaskStatus;
