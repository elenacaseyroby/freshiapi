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
      fontSize: 33 * device.normalizer,
    },
    title1: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 27 * device.normalizer,
    },
    title2: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 21 * device.normalizer,
    },
    title3: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 19 * device.normalizer,
    },
    headline: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 17 * device.normalizer,
    },
    body: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 16 * device.normalizer,
    },
    callout: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 15 * device.normalizer,
    },
    subhead: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 14 * device.normalizer,
    },
    footnote: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 12 * device.normalizer,
    },
    caption1: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 11 * device.normalizer,
    },
    caption2: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 11 * device.normalizer,
    },
  };
  return fonts;
};

export default getFonts;
