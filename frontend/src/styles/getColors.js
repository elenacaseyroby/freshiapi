const getColors = (lightMode) => {
  // lightMode: Bool
  // return object
  const colors = {
    background: {
      hex: lightMode ? '#ffffff' : '#242e36',
      opacity: '100%',
    },
    highContrast: {
      hex: lightMode ? '#242e36' : '#ffffff',
      opacity: '100%',
    },
    midContrast: {
      hex: lightMode ? '#667079' : '#e7ecf0',
      opacity: '100%',
    },
    lowContrast: {
      hex: lightMode ? '#f5f8fa' : '#667079',
      opacity: '100%',
    },
    highlight: {
      hex: lightMode ? '#e7ecf0' : '#f5f8fa',
      opacity: '100%',
    },
    interactiveFocus: {
      hex: lightMode ? '#cc3a16' : '#3d96ff',
      opacity: '100%',
    },
    error: {
      hex: '#ff3b30',
      opacity: '100%',
    },
    success: {
      hex: '#34c759',
      opacity: '100%',
    },
    info: {
      hex: '#0a7aff',
      opacity: '100%',
    },
    shadow: {
      hex: lightMode ? '#9b9a9a' : '#000000',
      opacity: '50%',
    },
  };
  return colors;
};

export default getColors;
