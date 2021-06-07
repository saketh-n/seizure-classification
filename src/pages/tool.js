import { useState, useEffect } from "react";
import { apiUrl, wasCached } from "../constants/constants";
import { useHistory } from "react-router-dom";

const bgImg = "https://designwoop.com/uploads/2012/05/17580-1024x768.jpg";
const divStyle = {
  background: `url(${bgImg})`,
  backgroundPosition: "center",
  backgroundSize: "cover",
  backgroundRepeat: "no-repeat",
  width: "100vw",
  height: "100vh",
  backgroundBlendMode: "multiply"
};

export default function Tool() {
  const [threshold, setThreshold] = useState(50);
  const [binWidth, setBinWidth] = useState(null);
  const [binSpacing, setBinSpacing] = useState(null);
  const [file, setFile] = useState(null);
  const [fileData, setFileData] = useState(null);
  const history = useHistory();

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
    const data = new FormData();
    data.append("filename", file.name);
    fetch(wasCached, {
      method: "POST",
      body: data
    })
      .then(res => res.json())
      .then(data => {
        if (data.result) {
          history.push(`/graph-${file.name}`);
        } else {
          const newData = new FormData();
          newData.append("filename", file.name);
          newData.append("file", file);
          // TODO: Encrypt the passed data
          newData.append("filedata", fileData);
          newData.append("binWidth", binWidth);
          newData.append("binInterval", binSpacing);
          newData.append("threshold", threshold);

          fetch(apiUrl, {
            method: "POST",
            body: newData
          });
          history.push("/loading");
        }
      });
  };

  const handleSlider = event => {
    setThreshold(event.target.value);
  };

  const handleBinWidth = event => {
    setBinWidth(event.target.value);
  };

  const handleBinSpacing = event => {
    setBinSpacing(event.target.value);
  };

  const onFileChange = event => {
    setFile(event.target.files[0]);
  };

  const uploadEnabled = () => {
    return (
      file &&
      binWidth &&
      binSpacing &&
      binWidth >= 1 &&
      binWidth <= 30 &&
      binSpacing >= 500 &&
      binSpacing <= 20000 &&
      binSpacing % 500 === 0
    );
  };
  const uploadStyle = () => {
    if (uploadEnabled()) {
      return "mt-12 w-4/5 text-gray-700 bg-indigo-400 font-sans mx-12 p-8 rounded-lg text-3xl hover:text-gray-200 hover:shadow-xl focus:outline-none focus:shadow-none";
    }
    return "mt-12 w-4/5 text-gray-200 bg-opacity-90 bg-indigo-200 font-sans mx-12 p-8 rounded-lg text-3xl ";
  };

  const chooseFile = () => {
    if (!file) {
      return (
        <p className="font-sans text-gray-700 w-64 text-center pt-8 ml-24">
          Drag and drop to upload or{" "}
          <label
            for="file-upload"
            class="custom-file-upload"
            className="text-indigo-400 hover:text-white"
          >
            browse
          </label>
          <input
            id="file-upload"
            type="file"
            style={{ display: "none" }}
            accept=".edf"
            onChange={onFileChange}
          />{" "}
          to choose a file
        </p>
      );
    } else {
      return (
        <>
          <p className="font-sans text-gray-700 w-64 text-center text-2xl ml-24 pt-4">
            {file.name} is Selected.
          </p>
          <p className="font-sans text-gray-700 w-64 text-center mt-2 ml-24">
            Choose a new{" "}
            <label
              for="file-upload"
              class="custom-file-upload"
              className="text-indigo-400 hover:text-white"
            >
              file
            </label>
            <input
              id="file-upload"
              type="file"
              style={{ display: "none" }}
              accept=".edf"
              onChange={onFileChange}
            />{" "}
          </p>
        </>
      );
    }
  };

  return (
    <div style={divStyle} className="flex flex-row">
      <div className="pt-80 pl-32">
        <h1 className="text-gray-700 font-sans text-6xl">
          Classify your EEG data
        </h1>
        <h1 className="text-gray-700 font-sans text-3xl mt-8 ml-16">
          Currently only supporting edf files
        </h1>
      </div>
      <div className="mt-48 ml-16 w-1/3 bg-gray-200 rounded-xl mb-32">
        {/* File Upload */}
        <div className="mx-12 mt-8 bg-gray-300 shadow-inner h-24 rounded-lg">
          {chooseFile()}
        </div>
        <input
          placeholder="Bin Width (Seconds)"
          className="mt-12 mx-12 w-4/5 px-8 py-4 rounded-lg shadow-inner focus:outline-none font-sans
          text-gray-700"
          min="1"
          max="30"
          step="1"
          type="number"
          value={binWidth}
          onChange={handleBinWidth}
        ></input>
        <input
          placeholder="Bin Spacing (Milliseconds)"
          className="mt-8 mx-12 w-4/5 px-8 py-4 rounded-lg shadow-inner focus:outline-none font-sans
          text-gray-700"
          min="500"
          max="20000"
          step="500"
          type="number"
          value={binSpacing}
          onChange={handleBinSpacing}
        ></input>
        <h1 className="mt-8 text-center text-gray-700">
          Seizure Probability Threshold: {threshold / 100}
        </h1>
        <input
          className="mt-8 mx-12 w-4/5"
          type="range"
          min="1"
          max="99"
          value={threshold}
          onChange={handleSlider}
        ></input>
        <button
          className={uploadStyle()}
          disabled={!uploadEnabled()}
          onClick={handleUpload}
        >
          Upload Data
        </button>
      </div>
    </div>
  );
}
