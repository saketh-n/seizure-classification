import { useState } from "react";

// TODO: Spectrogram takes in a map of channels to images, and generates based on that
// This way can integrate w/ what Devyansh does
export default function Spectogram(props) {
  const { data } = props;
  const channels = Array.from(data.keys());
  const [channel, setChannel] = useState(channels[0]);
  // TODO: replace this with actual EEG image
  const [imgUrl, setUrl] = useState(data.get(channels[0]));

  const handleChange = event => {
    setChannel(event.target.value);
    setUrl(data.get(event.target.value));
  };

  const channelOptions = () => {
    // c for channel [to avoid name conflict]
    return channels.map((c, i) => {
      return (
        <option value={c} key={i}>
          {c}
        </option>
      );
    });
  };

  return (
    <>
      <select className="mt-8 ml-8" value={channel} onChange={handleChange}>
        {channelOptions()}
      </select>
      {}
      <img src={imgUrl} alt="ex EEG" className="ml-8 mt-8" />
    </>
  );
}
