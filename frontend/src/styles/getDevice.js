const getDevice = (windowWidth) => {
  const device = {
    name: 'desktop',
    normalizer: windowWidth / 1280,
  };
  if (windowWidth < 768) {
    device.name = 'mobile';
    return device;
  }
  if (windowWidth < 1024) {
    device.name = 'tablet';
    return device;
  }
  return device;
};

export default getDevice;
