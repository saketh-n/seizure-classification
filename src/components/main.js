import { useState, useEffect } from "react";
import { apiUrl, buttonStyle } from "../constants/constants";
import BarChart from "../charts/barchart";
import BinModifier from "./binmodifier";

export default function Header() {
  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);
  const [fileData, setFileData] = useState(null);
  // Following are in ms
  const [binWidth, setBinWidth] = useState(10000);
  const [binInterval, setBinInterval] = useState(5000);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.addEventListener("load", event => {
        setFileData(event.target.result);
      });
      reader.readAsBinaryString(file);
      // wait for setFileData to go through
      setTimeout(() => {}, 100);
    }
  }, [file]);

  const handleUpload = () => {
    if (file) {
      if (!binWidth || binWidth < 10000 || binWidth > 100000) {
        window.alert(
          "Bin Width cannot be empty and must be a value between (10000 - 100000)"
        );
      } else if (!binInterval || binInterval < 500) {
        // TODO: lower this min to 50, and make it scrollable, rn looks disgusting lol
        window.alert(
          "Bin Interval cannot be empty and must be a value greater than 500"
        );
      } else {
        const data = new FormData();
        data.append("file", file);
        // TODO: Encrypt the passed data
        data.append("filedata", fileData);
        data.append("filename", file.name);
        data.append("binWidth", binWidth);
        data.append("binInterval", binInterval);
        setLoading(true);
        fetch(apiUrl, {
          method: "POST",
          body: data
        })
          .then(res => res.json())
          .then(data => {
            setResult(data.result);
            setLoading(false);
          });
      }
    } else {
      window.alert("No data selected!");
    }
  };

  const onFileChange = event => {
    setFile(event.target.files[0]);
  };

  const loadBarChart = () => {
    const edfLength =
      (binInterval * (result.length - 1)) / 1000 + binWidth / 1000;
    console.log(edfLength);
    return (
      <BarChart
        width={550}
        height={400}
        data={result}
        binWidth={binWidth}
        binInterval={binInterval}
        edfLength={edfLength}
      />
    );
  };

  return (
    <>
      <div className="mt-32 flex">
        <div className="flex flex-col">
          <button
            className={buttonStyle(loading)}
            disabled={loading}
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
          {
            // TODO: Make sure spectrogram data isn't empty.
          }
          {file && (
            <>
              <BinModifier
                binWidth={binWidth}
                setBinWidth={setBinWidth}
                binInterval={binInterval}
                setBinInterval={setBinInterval}
              />
            </>
          )}
        </div>
        {loading && <h1>Loading...</h1>}
        {result && !loading && loadBarChart()}
      </div>
    </>
  );
}
