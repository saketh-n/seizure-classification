import { useState, useEffect } from "react";
import { apiUrl } from "../constants/constants";
import BarChart from "../charts/barchart";
import Spectrogram from "./spectrogram";

export default function Header() {
  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);
  const [fileData, setFileData] = useState(null);
  let spectrogram = new Map();
  // TODO: when moving on from Dummy, remove this.
  spectrogram.set(
    "channel 1",
    "https://static-01.hindawi.com/articles/jam/volume-2014/261347/figures/261347.fig.001a.jpg"
  );
  spectrogram.set(
    "channel 2",
    "https://www.researchgate.net/profile/John-O-Toole/publication/43514277/figure/fig2/AS:614256932302896@1523461673601/A-frequency-domain-plot-of-newborn-EEG.png"
  );
  spectrogram.set(
    "channel 3",
    "https://www.biomedres.info/articles-images/biomedres-Single-channel-seizure-26-3-514-g002.png"
  );

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
      const data = new FormData();
      data.append("file", file);
      // TODO: Encrypt the passed data
      data.append("filedata", fileData);

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
          {
            // TODO: Make sure spectrogram data isn't empty.
          }
          {file && <Spectrogram data={spectrogram} />}
        </div>
        {result && <BarChart width={550} height={400} data={result} />}
      </div>
    </>
  );
}
