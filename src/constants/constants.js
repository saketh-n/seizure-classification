export const apiUrl = "http://localhost:5000/result";
export const red = [238, 75, 43];
export const green = [80, 200, 120];
// Above this value we should consider this a seizure
export const predThreshold = 70;
export const msToS = 1000;
export const edfWindow = 100;
export const buttonStyle = isDisabled => {
  let enabledButton =
    "ml-32 bg-white p-5 shadow-lg bg-clip-padding bg-opacity-60 border border-gray-200 rounded-lg font-semibold w-40 hover:bg-blue-100";
  let disabledButton =
    "ml-32 bg-gray-200 p-5 shadow-lg bg-clip-padding bg-opacity-60 text-opacity-25 text-gray-800 border border-gray-200 rounded-lg font-semibold w-40";
  return isDisabled ? disabledButton : enabledButton;
};
