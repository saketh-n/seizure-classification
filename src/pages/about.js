import Header from "../components/header";

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

export default function About() {
  return (
    <div style={divStyle}>
      <Header pageName={"About"} mode={"dark"} />
      <div className="pt-64">
        <h1 className="text-gray-700 font-sans text-6xl text-center">About</h1>
        <div className="ml-36">
          <h1 className="text-gray-700 font-sans text-lg text-center pt-8 w-1/3 ml-96">
            Our tool enables the automated detection of seizures in EEG data.
            Currently we are only supporting edf files
          </h1>
        </div>
      </div>
    </div>
  );
}
