import { useState } from "react";
import { apiUrl } from "../constants/constants";

export default function Header() {
  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);

  const handleUpload = () => {
    if (file) {
      const data = new FormData();
      data.append("file", file);
      data.append("filename", file.name);

      // TODO: Eventually can get actual data not just filename. Encrypt it
      fetch(apiUrl, {
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

  const barGraphResults = results => {
    return results.map((res, index) => {
      let resToHeight = Math.round((res * 100) / 4) * 4;
      // To display something at least
      if (resToHeight === 0) {
        resToHeight++;
      }
      // TODO: Update to full gradient
      let barcolor = "green-200";
      if (res > 0.25 && res < 0.5) {
        barcolor = "green-400";
      } else if (res >= 0.5 && res < 0.75) {
        barcolor = "red-200";
      } else if (res > 0.75) {
        barcolor = "red-400";
      }
      console.log(barcolor);
      return (
        <h1 className={`bg-${barcolor} h-${resToHeight} p-1 ml-1`} key={index}>
          {res.toFixed(2)}
        </h1>
      );
    });
  };

  return (
    <>
      <div className="mt-32 flex">
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
        {result && (
          <div className="flex flex-col">
            <div className="flex items-end">{barGraphResults(result)}</div>
            <h1 className="mt-3 font-semibold">
              Seizure Probability at 2 second Intervals
            </h1>
          </div>
        )}
      </div>
    </>
  );
}
