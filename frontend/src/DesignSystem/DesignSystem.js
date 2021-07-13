import React from 'react';
import PropTypes from 'prop-types';
import getColors from '../styles/getColors';
import getFonts from '../styles/getFonts';
import getStyles from '../styles/getStyles';
import getDevice from '../styles/getDevice';
import ColorSquare from './ColorSquare';

const DesignSystem = ({ media, toggleLightMode }) => {
  const { windowWidth, lightMode } = media;
  const colors = getColors(lightMode);
  const styles = getStyles(windowWidth);
  const fonts = getFonts(windowWidth);
  const device = getDevice(windowWidth);
  const indexMidpoint = Math.ceil(Object.keys(colors).length / 2) - 1;
  return (
    <div style={{
      ...styles.padding,
      display: 'block' }}
    >
      {/* header */}
      <div style={{
        /* row with space between start */
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        /* row with space between end */
        ...styles.marginBottom
      }}
      >
        <div style={{
          ...fonts.largeTitle,
          ...colors.interactiveFocus }}
        >
          Freshi
        </div>
        <button
          type="button"
          onClick={toggleLightMode}
          style={{
            backgroundColor: colors.background.color,
            color: colors.interactiveFocus.color,
            justifyContent: 'center',
            borderColor: colors.background.color,
            borderWidth: 0.3 * device.normalizer,
            borderRadius: 5 * device.normalizer,
            padding: 10 * device.normalizer,
            /* offset-x | offset-y | blur-radius| spread-radius | color */
            /* blur-radius: bigger number means bigger, lighter shadow */
            /* spread-radius: Positive values will cause the shadow to expand
            and grow bigger, negative values will cause the shadow to shrink. */
            boxShadow: `3px 3px 10px -2px ${colors.shadow.color}`,
            ...fonts.caption1 }}
        >
          {lightMode ? 'Dark Mode' : 'Light Mode'}
        </button>
      </div>
      <div style={{
        ...styles.collapsableGrid
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
              <>
                <div style={{
                  ...colors.highContrast,
                  ...fontStyle
                }}
                >
                  {font}
                </div>
                <div style={{
                  ...colors.highContrast,
                  ...fonts.caption1
                }}
                >
                  {fontStyle.usageNote}
                  <br />
                  Font Family: &nbsp;
                  {fontStyle.fontFamily}
                  <br />
                  Font Weight: &nbsp;
                  {fontStyle.fontWeight}
                  <br />
                  Font Size: &nbsp;
                  {Math.floor(fontStyle.fontSize)}
                  <br />
                  <br />
                  <br />
                </div>
              </>
            );
          })}
        </div>
        {/* colors */}
        <div style={{ ...styles.column }}>
          <div style={styles.collapsableGrid}>
            <div style={{ ...styles.column, ...styles.marginRight }}>
              { Object.keys(colors).map((colorName, index) => {
                // put first half of colors in one column and
                // second half in another column.
                if (index > indexMidpoint) return null;
                const color = colors[colorName];
                return (
                  <ColorSquare
                    name={colorName}
                    hex={color.color}
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
                    hex={color.color}
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
    </div>
  );
};

DesignSystem.propTypes = {
  media: PropTypes.shape({
    windowHeight: PropTypes.number.isRequired,
    windowWidth: PropTypes.number.isRequired,
    lightMode: PropTypes.bool.isRequired,
  }).isRequired,
  toggleLightMode: PropTypes.func.isRequired,
};

export default DesignSystem;
