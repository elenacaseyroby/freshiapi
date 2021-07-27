import React from 'react';
import PropTypes from 'prop-types';
import getColors from '../styles/getColors';
import getFonts from '../styles/getFonts';
import getDevice from '../styles/getDevice';
import getStyles from '../styles/getStyles';
import ColorSquare from './ColorSquare';
import FreshiButton from '../components/FreshiButton';

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
        alignItems: 'flex-start',
        /* row with space between end */
        ...styles.marginBottom
      }}
      >
        <div style={{ display: 'block' }}>
          <div style={{
            ...fonts.largeTitle,
            ...colors.interactiveFocus }}
          >
            Freshi
          </div>
          <div style={{
            ...fonts.title3,
            ...colors.interactiveFocus }}
          >
            design system
          </div>
        </div>
        <FreshiButton
          label={lightMode ? 'Dark Mode' : 'Light Mode'}
          onClick={toggleLightMode}
          backgroundColor={colors.background.color}
          forgroundColor={colors.interactiveFocus.color}
          media={media}
          // override padding
          style={{
            padding: 10 * device.normalizer
          }}
        />
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
              <div style={{
                ...styles.marginBottom }}
              >
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
                </div>
              </div>
            );
          })}
        </div>
        {/* colors & style */}
        <div style={{ ...styles.column }}>
          <div style={{
            ...styles.collapsableGrid,
            ...styles.marginBottom }}
          >
            {/* first column of colors */}
            <div style={{ ...styles.column, ...styles.marginRight }}>
              { Object.keys(colors).map((colorName, index) => {
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
            {/* second column of colors */}
            <div style={{ ...styles.column }}>
              { Object.keys(colors).map((colorName, index) => {
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
          {/* styles */}
          <div style={{
            display: 'block',
            ...styles.marginTop,
          }}
          >
            <div style={{
              ...fonts.headline,
              ...colors.highContrast }}
            >
              Global Styles
            </div>
            <div style={{
              ...fonts.body,
              ...colors.highContrast }}
            >
              padding: &nbsp;
              {Math.floor(styles.padding.padding)}
              <br />
              margin: &nbsp;
              {Math.floor(styles.margin.margin)}
              <br />
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
