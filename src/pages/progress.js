import { io } from "socket.io-client";
import { backend } from "../constants/constants";
import { useState, useEffect } from "react";
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

export default function Progress() {
  const history = useHistory();
  const [dataReceived, setDataReceived] = useState(false);
  const [numBins, setNumBins] = useState(0);
  const [counter, setCounter] = useState(0);

  useEffect(() => {
    // Component Did Mount
    const socket = io.connect(backend);
    // Add Event Handlers
    socket.on("dataReceipt", message => {
      // Handle Data Received Message
      setDataReceived(message.value);
    });

    socket.on("numberBins", message => {
      // Handle Number of Bins Message
      setNumBins(message.value);
    });

    socket.on("modelPass", message => {
      // Handle Model Pass Message
      setCounter(message.value);
    });

    socket.on("classificationComplete", message => {
      history.push(`/graph-${message.value}`);
    });

    return function cleanup() {
      // Component Did Unmount
      socket.close();
    };
  }, []);

  const secondHeaderText = () => {
    if (dataReceived) {
      return "Classifying ...";
    } else {
      return "Uploading ...";
    }
  };

  const percentage = () => {
    if (numBins) {
      return Math.floor((counter * 100) / numBins);
    }
    return 0;
  };

  const thirdHeaderText = () => {
    if (numBins) {
      return `(${counter} / ${numBins}) bins processed`;
    }
    return "";
  };

  return (
    <div style={divStyle} className="flex flex-row">
      <div className="mt-80 mx-48 w-4/5 bg-gray-200 rounded-xl mb-80">
        <h1 className="mt-12 text-center font-sans text-gray-700 text-3xl">
          Classification Progress:
        </h1>
        <div className="relative pt-1">
          <div className="mt-8 mx-8 overflow-hidden h-8 text-xs flex rounded bg-indigo-200">
            <div
              style={{ width: `${percentage()}%` }}
              className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-600"
            ></div>
          </div>
        </div>
        <h1 className="mt-8 text-center font-sans text-gray-700 text-3xl">
          {secondHeaderText()}
        </h1>
        <h1 className="mt-4 text-center font-sans text-gray-700 text-xl">
          {thirdHeaderText()}
        </h1>
      </div>
    </div>
  );
}
