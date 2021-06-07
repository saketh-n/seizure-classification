import Header from "../components/header";
import Card from "../components/card";

const bgImg =
  "https://www.designbolts.com/wp-content/uploads/2012/12/Diamond-Eyes-White-Seamless-Textures.jpg";
const divStyle = {
  background: `url(${bgImg})`,
  backgroundPosition: "center",
  backgroundSize: "cover",
  backgroundRepeat: "no-repeat",
  width: "100vw",
  height: "100vh",
  backgroundBlendMode: "multiply"
};

export default function Works() {
  return (
    <div style={divStyle}>
      <Header pageName={"How It Works"} mode={"dark"} />
      <div className="pt-32">
        <h1 className="text-gray-700 font-sans text-6xl text-center">
          The Pipeline
        </h1>
        <div className="mt-16 flex flex-row">
          <Card
            imgSrc={"https://i.ibb.co/wdndpNn/data-upload.png"}
            title={"Data Upload"}
            paragraph="Using our tool clinicians can upload EEG (a method for recording
              neural activity) data. For now our tool only accepts EEG data encoded as
              an edf file"
          />
          <Card
            imgSrc={"https://i.ibb.co/NmLZXKq/preproc.png"}
            title={"Pre-Processing"}
            paragraph="Once the data is sent to the backend it is cleaned to reduce
            artifacts such as tremors or electrical interference. Then the data is downsampled,
             one reason being so that is the right shape for our model"
          />
          <Card
            imgSrc={"https://i.ibb.co/h9rBYjH/model.png"}
            title={"Model"}
            paragraph="In being passed through the model, the data undergoes a series
            of linear and non-linear transformations to create an appropriate output, namely
            the probability of seizure occurences in different time intervals"
          />
          <Card
            imgSrc={"https://i.ibb.co/sPjY4qw/results.png"}
            title={"Results"}
            paragraph="The resulting output is a group of time intervals where seizures 
            are thought to have occurred"
          />
        </div>
      </div>
    </div>
  );
}
