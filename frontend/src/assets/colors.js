const getColors = (lightMode) => {
  // lightMode: Bool
  // return object
  const colors = {
    background: lightMode ? '#ffffff' : '#242e36',
    highContrast: lightMode ? '#242e36' : '#ffffff',
    midContrast: lightMode ? '#667079' : '#e7ecf0',
    lowContrast: lightMode ? '#f5f8fa' : '#667079',
    highlight: lightMode ? '#e7ecf0' : '#f5f8fa',
    interactiveFocus: lightMode ? '#cc3a16' : '#3d96ff',
    error: '#ff3b30',
    success: '#34c759',
    info: '#0a7aff',
    shadow: lightMode ? '#9b9a9a' : '#000000', // opacity 50%
  };
  return colors;
};

export default getColors;
