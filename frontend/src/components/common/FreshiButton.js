import React from 'react';
import PropTypes from 'prop-types';
import getFonts from '../../styles/getFonts';
import getDevice from '../../styles/getDevice';
import getColors from '../../styles/getColors';

const FreshiButton = ({
  label,
  onClick,
  backgroundColor,
  forgroundColor,
  media,
  style,
}) => {
  const { lightMode, windowWidth } = media;
  const device = getDevice(windowWidth);
  const fonts = getFonts(windowWidth);
  const colors = getColors(lightMode);
  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        backgroundColor,
        color: forgroundColor,
        borderColor: backgroundColor,
        borderWidth: 0.3 * device.normalizer,
        padding: 5 * device.normalizer,
        borderRadius: 5 * device.normalizer,
        /* offset-x | offset-y | blur-radius| spread-radius | color */
        /* blur-radius: bigger number means bigger, lighter shadow */
        /* spread-radius: Positive values will cause the shadow to expand
        and grow bigger, negative values will cause the shadow to shrink. */
        boxShadow: `3px 3px 10px -2px ${colors.shadow.color}`,
        ...fonts.callout,
        ...style,
      }}
    >
      {label}
    </button>
  );
};

FreshiButton.defaultProps = {
  style: {},
};

FreshiButton.propTypes = {
  label: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  backgroundColor: PropTypes.string.isRequired,
  forgroundColor: PropTypes.string.isRequired,
  media: PropTypes.shape({
    windowHeight: PropTypes.number.isRequired,
    windowWidth: PropTypes.number.isRequired,
    lightMode: PropTypes.bool.isRequired,
  }).isRequired,
  style: React.CSSProperties,
};

export default FreshiButton;
