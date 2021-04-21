import { useState } from "react";

export default function Header() {
  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);

  const handleUpload = () => {
    if (file) {
      const data = new FormData();
      data.append("file", file);
      data.append("filename", file.name);

      // TODO: Eventually can get actual data not just filename. Encrypt it
      fetch("http://localhost:5000/result", {
        method: "POST",
        body: data
      })
        .then(res => res.json())
        .then(data => {
          setResult(data.result);
        });
    } else {
      window.alert("No data selected!");
    }
  };

  const onFileChange = event => {
    setFile(event.target.files[0]);
  };

  return (
    <>
      <div className="mt-32 flex justify-between">
        <div className="flex flex-col">
          <button
            className="ml-32 bg-white p-5 shadow-lg 
    bg-clip-padding bg-opacity-60 border border-gray-200
     rounded-lg font-semibold w-40"
            onClick={handleUpload}
          >
            Upload Data
          </button>
          <input
            className="ml-32 mt-8"
            type="file"
            onChange={onFileChange}
            accept=".edf"
          />
        </div>

        {result != null && (
          <h1 className="p-5 font-semibold">{`Result: ${result}`}</h1>
        )}
      </div>
    </>
  );
}
