import getDevice from './getDevice';

const getStyles = (windowWidth) => {
  const device = getDevice(windowWidth);
  const styles = {
    grid: {
      display: device.name === 'mobile' ? 'block' : 'flex',
    },
    column: {
      flex: 1,
    },
    paddingTop: {
      paddingTop: 50 * device.normalizer,
    },
    paddingBottom: {
      paddingBottom: 50 * device.normalizer,
    },
    marginRight: {
      marginRight: 10 * device.normalizer,
    },
    marginBottom: {
      marginBottom: 10 * device.normalizer,
    },
    margin: {
      margin: 5 * device.normalizer,
    },
  };
  return styles;
};

export default getStyles;
