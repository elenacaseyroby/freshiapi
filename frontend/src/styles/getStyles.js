import getDevice from './getDevice';

const getStyles = (windowWidth) => {
  const device = getDevice(windowWidth);
  const styles = {
    grid: {
      display: 'flex',
    },
    collapsableGrid: {
      display: device.name === 'mobile' ? 'block' : 'flex',
    },
    column: {
      flex: 1,
    },
    padding: {
      padding: 20 * device.normalizer,
    },
    paddingTop: {
      paddingTop: 20 * device.normalizer,
    },
    paddingBottom: {
      paddingBottom: 20 * device.normalizer,
    },
    paddingLeft: {
      paddingLeft: 20 * device.normalizer,
    },
    paddingRight: {
      paddingRight: 20 * device.normalizer,
    },
    marginRight: {
      marginRight: 10 * device.normalizer,
    },
    marginBottom: {
      marginBottom: 10 * device.normalizer,
    },
    marginTop: {
      marginTop: 10 * device.normalizer,
    },
    margin: {
      margin: 5 * device.normalizer,
    },
  };
  return styles;
};

export default getStyles;
