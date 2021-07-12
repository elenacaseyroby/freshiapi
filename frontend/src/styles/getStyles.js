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
    screenPadding: {
      padding: 33 * device.normalizer,
    },
    componentMargin: {
      margin: 15 * device.normalizer,
    }
  };
  return styles;
};

export default getStyles;
