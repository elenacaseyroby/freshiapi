const getDevice = (windowWidth) => {
  // normalizer used to scale text and images
  // for responsive rendering.
  if (windowWidth < 768) {
    return {
      name: 'mobile',
      textNormalizer: 1,
      normalizer: 1,
      description: 'Screens smaller than 768px.'
    };
  }
  if (windowWidth < 1024) {
    return {
      name: 'tablet',
      textNormalizer: 1,
      normalizer: windowWidth / 768,
      description: 'Screens larger than 768px and smaller than 1024 px.'
    };
  }
  return {
    name: 'desktop',
    textNormalizer: windowWidth / 1024 < 1.5 ? windowWidth / 1024 : 1.5,
    normalizer: windowWidth / 768,
    description: 'Screens larger than 1024 px.'
  };
};

export default getDevice;
