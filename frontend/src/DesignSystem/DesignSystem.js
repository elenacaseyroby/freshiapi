import React from 'react';
import PropTypes from 'prop-types';
import getColors from '../styles/getColors';
import getFonts from '../styles/getFonts';
import getStyles from '../styles/getStyles';
import ColorSquare from './ColorSquare';

const DesignSystem = ({ media }) => {
  const { windowWidth, lightMode } = media;
  const colors = getColors(lightMode);
  const styles = getStyles(windowWidth);
  const fonts = getFonts(windowWidth);
  const indexMidpoint = Math.ceil(Object.keys(colors).length / 2) - 1;
  return (
    <div style={{
      ...styles.paddingTop,
      ...styles.paddingBottom,
      ...styles.grid
    }}
    >
      {/* fonts */}
      <div style={{
        ...styles.column,
        ...styles.marginRight,
        ...styles.marginBottom }}
      >
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
      <div style={{ ...styles.column }}>
        <div style={styles.grid}>
          <div style={{ ...styles.column, ...styles.marginRight }}>
            { Object.keys(colors).map((colorName, index) => {
              // put first half of colors in one column and
              // second half in another column.
              if (index > indexMidpoint) return null;
              const color = colors[colorName];
              return (
                <ColorSquare
                  name={colorName}
                  hex={color.hex}
                  opacity={color.opacity}
                  windowWidth={windowWidth}
                  lightMode={lightMode}
                />
              );
            }) }
          </div>
          <div style={styles.column}>
            { Object.keys(colors).map((colorName, index) => {
              // put first half of colors in one column and
              // second half in another column.
              if (index <= indexMidpoint) return null;
              const color = colors[colorName];
              return (
                <ColorSquare
                  name={colorName}
                  hex={color.hex}
                  opacity={color.opacity}
                  windowWidth={windowWidth}
                  lightMode={lightMode}
                />
              );
            }) }
          </div>
        </div>
      </div>
    </div>
  );
};

DesignSystem.propTypes = {
  media: PropTypes.shape({
    windowHeight: PropTypes.number.isRequired,
    windowWidth: PropTypes.number.isRequired,
    lightMode: PropTypes.bool.isRequired,
  }).isRequired,
};

export default DesignSystem;
