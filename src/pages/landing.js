import Header from "../components/header";
import { useHistory } from "react-router-dom";

const bgImg =
  "https://images.unsplash.com/photo-1558299797-bd840732a13e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1567&q=80";
const divStyle = {
  background: `url(${bgImg}) rgba(0, 0, 0, 0.65)`,
  backgroundPosition: "center",
  backgroundSize: "cover",
  backgroundRepeat: "no-repeat",
  width: "100vw",
  height: "100vh",
  backgroundBlendMode: "multiply"
};

export default function Landing() {
  const history = useHistory();
  return (
    <div style={divStyle}>
      <Header pageName={"Home"} mode={"light"} />
      <div className="pt-64">
        <h1 className="text-white font-sans text-6xl text-center">
          Automated Seizure Detection
        </h1>
        <h1 className="text-white font-sans text-lg text-center pt-8">
          By Saketh Nimmagadda, Robert Minneker, Devyansh Gupta
        </h1>
        <div className="ml-80">
          <button
            onClick={() => {
              history.push("/data-upload");
            }}
            className="ml-96 mt-8 text-gray-700 font-sans text-lg bg-indigo-400 rounded-full py-3 px-6 hover:text-gray-200 hover:shadow-lg focus:outline-none focus:shadow-none"
          >
            Get Started
          </button>
        </div>
      </div>
    </div>
  );
}
