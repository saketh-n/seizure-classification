export default function BinModifier(props) {
  const { binWidth, setBinWidth, binInterval, setBinInterval } = props;

  const handleBinWidth = event => {
    setBinWidth(event.target.value);
  };

  const handleBinInterval = event => {
    setBinInterval(event.target.value);
  };

  return (
    <>
      <div className="flex ml-8 mt-4">
        <h1 className="w-32 my-1">Bin Width (ms): </h1>
        <input
          min="10000"
          max="100000"
          type="number"
          className="w-24 rounded-lg py-1 px-2"
          value={binWidth}
          onChange={handleBinWidth}
        ></input>
      </div>
      <div className="flex ml-8 mt-4">
        <h1 className="w-32 my-1">Bin Interval (ms): </h1>
        <input
          min="500"
          type="number"
          className="w-24 rounded-lg py-1 px-2"
          value={binInterval}
          onChange={handleBinInterval}
        ></input>
      </div>
    </>
  );
}
