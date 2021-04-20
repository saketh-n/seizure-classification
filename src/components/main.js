import { useState } from "react";

export default function Header() {
  const [result, setResult] = useState(null);

  const handleUpload = () => {
    // TODO: pass input to the model
    fetch("http://localhost:5000/result")
      .then(res => res.json())
      .then(data => {
        setResult(data.result);
      });
  };

  return (
    <>
      <div className="mt-32 flex justify-between">
        <button
          className="ml-32 bg-white p-5 shadow-lg 
    bg-clip-padding bg-opacity-60 border border-gray-200
     rounded-lg font-semibold"
          onClick={handleUpload}
        >
          Upload Data
        </button>
        {result != null && (
          <h1 className="p-5 font-semibold">{`Result: ${result}`}</h1>
        )}
      </div>
    </>
  );
}
