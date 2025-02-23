import React from "react";

function AppGenerator({ response }) {
  return (
    <div>
      <h2>{response.app_name}</h2>
      <p>{response.description}</p>

      {response.code && (
        <pre>
          <code>{response.code}</code>
        </pre>
      )}
    </div>
  );
}

export default AppGenerator;
