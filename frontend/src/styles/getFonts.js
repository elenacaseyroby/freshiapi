import getDevice from './getDevice';

const getFonts = (windowWidth) => {
  const device = getDevice(windowWidth);
  // Can't bold varela round.
  const round = 'Varela Round, sans-serif';
  // Can bold roboto.
  const regular = 'Roboto, sans-serif';
  const fonts = {
    largeTitle: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 99 * device.normalizer,
    },
    title1: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 81 * device.normalizer,
    },
    title2: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 63 * device.normalizer,
    },
    title3: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 57 * device.normalizer,
    },
    headline: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 51 * device.normalizer,
    },
    body: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 48 * device.normalizer,
    },
    callout: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 45 * device.normalizer,
    },
    subhead: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 42 * device.normalizer,
    },
    footnote: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 36 * device.normalizer,
    },
    caption1: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 33 * device.normalizer,
    },
    caption2: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 33 * device.normalizer,
    },
  };
  return fonts;
};

export default getFonts;
