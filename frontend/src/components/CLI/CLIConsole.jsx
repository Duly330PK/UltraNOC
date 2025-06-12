import React, { useState } from "react";
const CLIConsole = () => {
  const [log, setLog] = useState([]);
  const [input, setInput] = useState("");

  const handleInput = (e) => {
    if (e.key === "Enter") {
      setLog([...log, input]);
      setInput("");
    }
  };

  return (
    <div className="cli-console">
      <pre>{log.join("\n")}</pre>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleInput}
        placeholder="Type command..."
      />
    </div>
  );
};
export default CLIConsole;
