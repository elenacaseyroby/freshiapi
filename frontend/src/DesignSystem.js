import React from 'react';
import getFonts from './styles/getFonts';

const DesignSystem = (windowWidth) => {
  const fonts = getFonts(windowWidth);
  return (
    <div>
      <div style={fonts.largeTitle}>largeTitle</div>
      <div style={fonts.title1}>title1</div>
      <div style={fonts.title2}>title2</div>
      <div style={fonts.title3}>title3</div>
      <div style={fonts.headline}>body</div>
      <div style={fonts.body}>body</div>
      <div style={fonts.callout}>callout</div>
      <div style={fonts.subhead}>subhead</div>
      <div style={fonts.footnote}>footnote</div>
      <div style={fonts.caption1}>caption1</div>
      <div style={fonts.caption2}>caption2</div>
    </div>
  );
};

export default DesignSystem;
