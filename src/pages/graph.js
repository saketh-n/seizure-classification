import { useParams, useHistory } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiUrl } from "../constants/constants";
import BarChart from "../charts/barchart";

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

export default function Graph() {
  const { filename } = useParams();
  const history = useHistory();
  const [channels, setChannels] = useState([]);
  const [channel, setChannel] = useState(null);
  const [results, setResults] = useState(null);
  const [seizureBins, setSeizureBins] = useState([]);
  const [binCounter, setBinCounter] = useState(0);

  useEffect(() => {
    // Component Did Mount
    const data = new FormData();
    data.append("filename", filename);
    fetch(apiUrl, {
      method: "POST",
      body: data
    })
      .then(res => res.json())
      .then(data => {
        setResults(data.results);
        setChannels(data.channels);
        setSeizureBins(data.seizureBins);
      });
  }, []);

  const commonPathTfrRaw = (chan, binN, file, type) => {
    console.log(binN);
    console.log(chan);
    return `http://localhost:5000/saved_plots/${file}_tfr_raw_spd/${file}_bn${binN}_${chan}_${type}.png`;
  };

  const getTfr = (chan, binN, file) => {
    return commonPathTfrRaw(chan, binN, file, "tfr");
  };

  const getRaw = (chan, binN, file) => {
    return commonPathTfrRaw(chan, binN, file, "raw");
  };

  const channelOptions = () => {
    return channels.map((c, i) => (
      <option value={c} key={i}>
        {c}
      </option>
    ));
  };

  const dataWindow = () => {
    let window = [];
    let binNum = seizureBins[binCounter];
    window.push(results[binNum]);
    if (binNum > 0) {
      window.unshift(results[binNum - 1]);
      //setXStart((binNum - 1) * 5);
    }
    if (binNum > 1) {
      window.unshift(results[binNum - 2]);
      //setXStart((binNum - 2) * 5);
    }
    if (binNum < results.length - 1) {
      window.push(results[binNum + 1]);
      //setXEnd((binNum + 1) * 5);
    }
    if (binNum < results.length - 2) {
      window.push(results[binNum + 2]);
      //setXEnd((binNum + 2) * 5);
    }
    return window;
  };

  const handleChannel = event => {
    setChannel(event.target.value);
  };

  return (
    <div style={divStyle} className="flex flex-row">
      <div className="w-4/5 mt-32 bg-gray-200 mx-48 mb-32 rounded-lg">
        <h1 className="text-gray-700 font-sans text-4xl text-center mt-8">
          {filename.toUpperCase()} Visualized
        </h1>
        <div className="flex justify-center">
          <h1 className="mt-12 mr-4 text-gray-700 font-sans">Channels</h1>
          <select
            name="channel"
            className="w-48 p-1 mt-12 rounded-lg"
            value={channel}
            onChange={handleChannel}
          >
            {channelOptions()}
          </select>
        </div>

        <div className="py-8 mt-4 mx-8 flex flex-row bg-gray-100 rounded-lg">
          <div className="w-96 h-72 bg-white rounded-lg mx-12">
            <h1 className="text-center text-gray-700 font-sans mt-1">
              Seizure Probabilities
            </h1>
            {results && (
              <BarChart
                data={dataWindow()}
                binWidth={30000}
                binInterval={15000}
                width={240}
                height={240}
                xStart={(seizureBins[binCounter] - 2) * 5}
                xEnd={(seizureBins[binCounter] + 2) * 5}
              />
            )}
          </div>
          <img
            alt=""
            src={getTfr(channel, seizureBins[binCounter], filename)}
            className="w-80 h-72 bg-white rounded-lg mx-12"
          />
          <img
            alt=""
            src={getRaw(channel, seizureBins[binCounter], filename)}
            className="w-80 h-72 bg-white rounded-lg mx-12"
          />
        </div>
        <div className="flex justify-center mt-8">
          <button
            onClick={() => {
              let prevBin = binCounter - 1;
              if (prevBin <= seizureBins.length) {
                prevBin = seizureBins.length - 1;
              }
              setBinCounter(prevBin);
            }}
            className="py-4 px-12 bg-indigo-400 text-gray-700 font-sans mx-16 rounded-lg hover:text-gray-200 hover:shadow-lg focus:outline-none focus:shadow-none"
          >
            {"< Prev"}
          </button>
          <button
            onClick={() => {
              let nextBin = binCounter + 1;
              if (nextBin === seizureBins.length) {
                nextBin = 0;
              }
              setBinCounter(nextBin);
            }}
            className="py-4 px-12 bg-indigo-400 text-gray-700 font-sans mx-16 rounded-lg hover:text-gray-200 hover:shadow-lg focus:outline-none focus:shadow-none"
          >
            {"Next >"}
          </button>
        </div>
        <button
          onClick={() => {
            history.push("/data-upload");
          }}
          className="mt-2 py-4 px-12 bg-indigo-400 text-gray-700 font-sans mx-16 rounded-lg hover:text-gray-200 hover:shadow-lg focus:outline-none focus:shadow-none"
        >
          {"Re-Classify"}
        </button>
      </div>
    </div>
  );
}
