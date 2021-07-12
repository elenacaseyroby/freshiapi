import React from 'react';
import PropTypes from 'prop-types';

// eslint-disable-next-line react/prop-types
const DesignSystem = ({ media }) => {
  // eslint-disable-next-line react/prop-types
  const { fonts, colors } = media;
  console.log(colors);
  return (
    <div>
      {/* fonts */}
      <div>
        { Object.keys(fonts).map((font) => {
          const fontStyle = fonts[font];
          const style = {
            color: colors.highContrast,
            ...fontStyle
          };
          return (<div style={style}>{font}</div>);
        })}
      </div>
      {/* colors */}
      <div>
        { Object.keys(colors).map((color) => {
          const hex = colors[color];
          return (
            <div style={{ backgroundColor: hex }}>
              <div>
                {color}
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
    fonts: {
      headline: {
        fontFamily: 'Varela Round, sans-serif',
        fontWeight: 'normal',
        fontSize: 17,
      },
      body: {
        fontFamily: 'Roboto, sans-serif',
        fontWeight: 'normal',
        fontSize: 16,
      },
    },
    colors: {
      highContrast: '#000000',
      backgroundColor: '#ffffff',
    }
  }
};

DesignSystem.propTypes = {
  media: PropTypes.shape({
    fonts: PropTypes.objectOf(PropTypes.object).isRequired,
    colors: PropTypes.objectOf(PropTypes.object).isRequired
  }),
};

export default DesignSystem;
