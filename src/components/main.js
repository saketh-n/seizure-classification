import { useState } from "react";
import { apiUrl } from "../constants/constants";

export default function Header() {
  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);

  // Above this value we should consider this a seizure
  const predThreshold = 70;

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

  const pickHex = (color1, color2, percent) => {
    // Quash the gradient
    if (percent < predThreshold) {
      percent = percent / 3;
    }
    const w1 = percent / 100;
    const w2 = 1 - w1;
    var rgb = [
      Math.round(color1[0] * w1 + color2[0] * w2),
      Math.round(color1[1] * w1 + color2[1] * w2),
      Math.round(color1[2] * w1 + color2[2] * w2)
    ];
    return rgb;
  };
  const onFileChange = event => {
    setFile(event.target.files[0]);
  };

  const barGraphResults = results => {
    return results.map((res, index) => {
      let resToHeight = Math.round((res * 100) / 4) * 4;

      const red = [238, 75, 43];
      const green = [80, 200, 120];
      const mix = pickHex(red, green, resToHeight);
      const barcolor = "rgb(" + mix[0] + "," + mix[1] + "," + mix[2] + ")";

      if (resToHeight < 6) {
        // Min height so text displays on bar
        resToHeight = 6;
      }
      return (
        <h1
          className={`px-1 ml-1 w-16 text-center font-thin`}
          style={{
            backgroundColor: barcolor,
            height: `${resToHeight * 4}px`,
            opacity: 0.88,
            position: "relative",
            left: `${-20 * index}px`
          }}
          key={index}
        >
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
