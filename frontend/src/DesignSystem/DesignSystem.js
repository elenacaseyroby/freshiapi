import React from 'react';
import PropTypes from 'prop-types';
import getColors from '../styles/getColors';
import getFonts from '../styles/getFonts';
import getStyles from '../styles/getStyles';

const DesignSystem = ({ media }) => {
  const { windowWidth, lightMode } = media;
  const colors = getColors(lightMode);
  const styles = getStyles(windowWidth);
  const fonts = getFonts(windowWidth);
  return (
    <div style={styles.grid}>
      {/* fonts */}
      <div style={{ ...styles.column, ...styles.componentMargin }}>
        { Object.keys(fonts).map((font) => {
          const fontStyle = fonts[font];
          return (
            <div style={{
              color: colors.highContrast.hex,
              ...fontStyle
            }}
            >
              {font}
            </div>
          );
        })}
      </div>
      {/* colors */}
      <div style={{ ...styles.column, ...styles.componentMargin }}>
        { Object.keys(colors).map((colorName) => {
          const color = colors[colorName];
          return (
            <div style={{ backgroundColor: color.hex }}>
              <div>
                {colorName}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

DesignSystem.defaultProps = {
  media: {
    windowHeight: 600,
    windowWidth: 400,
    deviceName: 'mobile',
    deviceNormalizer: 1,
    lightMode: true,
  }
};

DesignSystem.propTypes = {
  media: PropTypes.shape({
    windowHeight: PropTypes.number.isRequired,
    windowWidth: PropTypes.number.isRequired,
    deviceName: PropTypes.string.isRequired,
    deviceNormalizer: PropTypes.number.isRequired,
    lightMode: PropTypes.bool.isRequired,
  }),
};

export default DesignSystem;
