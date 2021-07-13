const getColors = (lightMode) => {
  // lightMode: Bool
  // return object
  const colors = {
    background: {
      color: lightMode ? '#ffffff' : '#242e36',
      opacity: '100%',
    },
    highContrast: {
      color: lightMode ? '#242e36' : '#ffffff',
      opacity: '100%',
    },
    midContrast: {
      color: lightMode ? '#667079' : '#e7ecf0',
      opacity: '100%',
    },
    lowContrast: {
      color: lightMode ? '#f5f8fa' : '#667079',
      opacity: '100%',
    },
    highlight: {
      color: lightMode ? '#e7ecf0' : '#f5f8fa',
      opacity: '100%',
    },
    interactiveFocus: {
      color: lightMode ? '#cc3a16' : '#3d96ff',
      opacity: '100%',
    },
    error: {
      color: '#ff3b30',
      opacity: '100%',
    },
    success: {
      color: '#34c759',
      opacity: '100%',
    },
    info: {
      color: '#0a7aff',
      opacity: '100%',
    },
    shadow: {
      color: lightMode ? '#9b9a9a' : '#000000',
      opacity: '50%',
    },
  };
  return colors;
};

export default getColors;
