export default function Card(props) {
  const { imgSrc, paragraph, title } = props;
  return (
    <div className="mx-8 bg-gray-100 p-8 rounded-lg shadow-2xl">
      <h1 className="text-3xl text-gray-700 text-center font-sans">{title}</h1>
      <img src={imgSrc} alt="" className="mt-4 w-64 h-64 shadow-inner" />
      <p className="w-64 mt-4 font-sans text-gray-700">{paragraph}</p>
    </div>
  );
}
