import React from 'react';
import PropTypes from 'prop-types';
import getFonts from '../styles/getFonts';
import getColors from '../styles/getColors';
import getDevice from '../styles/getDevice';
import getStyles from '../styles/getStyles';

const getColorSquareStyles = ({ windowWidth, lightMode }) => {
  const fonts = getFonts(windowWidth);
  const colors = getColors(lightMode);
  const styles = {
    text: {
      ...colors.highContrast,
      ...fonts.caption1
    },
  };
  return styles;
};

const ColorSquare = ({
  name,
  hex,
  opacity,
  windowWidth,
  lightMode,
}) => {
  const styles = getColorSquareStyles({ windowWidth, lightMode });
  const device = getDevice(windowWidth);
  const colors = getColors(lightMode);
  const globalStyles = getStyles(windowWidth);
  const sideLength = device.name === 'desktop' ? 50 * device.normalizer : 100;
  return (
    <div style={{
      ...globalStyles.grid,
      ...globalStyles.marginBottom }}
    >
      {/* color block */}
      <div style={{
        maxWidth: sideLength,
        minWidth: sideLength,
        minHeight: sideLength,
        maxHeight: sideLength,
        backgroundColor: hex,
        borderRadius: 5 * device.normalizer,
        /* offset-x | offset-y | blur-radius| spread-radius | color */
        /* blur-radius: bigger number means bigger, lighter shadow */
        /* spread-radius: Positive values will cause the shadow to expand
        and grow bigger, negative values will cause the shadow to shrink. */
        boxShadow: `3px 3px 10px -2px ${colors.shadow.color}`,
        borderColor: hex,
        ...globalStyles.column,
        ...globalStyles.marginRight,
        // borderColor: colors.highContrast,
        // borderWidth: 1 * device.normalizer,
      }}
      />
      {/* label */}
      <div style={{ ...globalStyles.column }}>
        <div style={styles.text}>{name}</div>
        <div style={styles.text}>{hex}</div>
        <div style={styles.text}>{opacity}</div>
      </div>
    </div>
  );
};

ColorSquare.propTypes = {
  name: PropTypes.string.isRequired,
  hex: PropTypes.string.isRequired,
  opacity: PropTypes.string.isRequired,
  windowWidth: PropTypes.number.isRequired,
  lightMode: PropTypes.bool.isRequired
};

export default ColorSquare;
