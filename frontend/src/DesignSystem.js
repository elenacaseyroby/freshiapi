import React from 'react';
import getFonts from './styles/getFonts';

// eslint-disable-next-line react/prop-types
const DesignSystem = ({ media }) => {
  // eslint-disable-next-line react/prop-types
  const fonts = getFonts(media.windowWidth);
  return (
    <div>
      {/* fonts */}
      <div>
        { Object.keys(fonts).map((key) => {
          const style = fonts[key];
          return (<div style={style}>{key}</div>);
        })}
      </div>
    </div>
  );
};

export default DesignSystem;
