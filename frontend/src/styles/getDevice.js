const getDevice = (windowWidth) => {
  if (windowWidth < 768) {
    return {
      name: 'mobile',
      normalizer: 1,
    };
  }
  if (windowWidth < 1024) {
    return {
      name: 'tablet',
      normalizer: 1.5,
    };
  }
  return {
    name: 'desktop',
    normalizer: windowWidth / 700,
  };
};

export default getDevice;
