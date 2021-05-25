export default function BinModifier(props) {
  const { binWidth, binInterval } = props;

  const handleChange = event => {
    // Grabs setBinInterval, setBinWidth from props
    // Done this way to avoid redundancy and make code
    // more extensible in future
    props[`set${event.target.name}`](event.target.value);
  };

  return (
    <>
      <div className="flex ml-8 mt-4">
        <h1 className="w-32 my-1">Bin Width (ms): </h1>
        <input
          min="1000"
          max="100000"
          step="1000"
          type="number"
          className="w-24 rounded-lg py-1 px-2"
          name="BinWidth"
          value={binWidth}
          onChange={handleChange}
        ></input>
      </div>
      <div className="flex ml-8 mt-4">
        <h1 className="w-32 my-1">Bin Interval (ms): </h1>
        <input
          min="500"
          type="number"
          className="w-24 rounded-lg py-1 px-2"
          name="BinInterval"
          value={binInterval}
          onChange={handleChange}
        ></input>
      </div>
    </>
  );
}
