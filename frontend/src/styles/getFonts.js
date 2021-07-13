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
      fontSize: 45 * device.textNormalizer,
      usageNote: 'Use for one short title at very top of page. Ex. "Freshi".',
    },
    title1: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 40 * device.textNormalizer,
      usageNote: 'Use for one prominant title on page. Ex. "About Us".',
    },
    title2: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 35 * device.textNormalizer,
      usageNote: 'Use for subtitle on page. Ex. "Beginnings", "Building the App", "Freshi Today"',
    },
    title3: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 25 * device.textNormalizer,
      usageNote: 'Use for subtitles of subtitles... you get the picture.',
    },
    headline: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 20 * device.textNormalizer,
      usageNote: 'Use for titles on page with many sections with titles, or subtitle of subtitle of subtitle.',
    },
    subhead: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 15 * device.textNormalizer,
      usageNote: 'Use for subtitles of headlines.',
    },
    body: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 13 * device.textNormalizer,
      usageNote: 'Use for body text.',
    },
    footnote: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 12 * device.textNormalizer,
      usageNote: 'Use for footnotes.',
    },
    caption1: {
      fontFamily: round,
      fontWeight: 'normal',
      fontSize: 11 * device.textNormalizer,
      usageNote: 'Use for captions.',
    },
    caption2: {
      fontFamily: regular,
      fontWeight: 'normal',
      fontSize: 11 * device.textNormalizer,
      usageNote: 'Use for captions.',
    },
  };
  return fonts;
};

export default getFonts;
