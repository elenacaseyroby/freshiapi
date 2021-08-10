import React from 'react';
import PropTypes from 'prop-types';
import getStyles from '../../styles/getStyles';

import './LegalTemplateColorsLight.css';
import './LegalTemplate.css';

const LegalTemplate = ({
  body,
  media,
}) => {
  // wrap the body in the legaltemplate class so that the styles
  // for this page don't have side effects on other pages.
  const legalTemplateBody = `<div class="legaltemplate">${body}</div>`;
  const styles = getStyles(media.windowWidth);
  return (
    <div style={{
      ...styles.paddingRight,
      ...styles.paddingLeft,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-start',
      minHeight: media.windowHeight,
    }}
    >
      <div dangerouslySetInnerHTML={{ __html: legalTemplateBody }} />
    </div>
  );
};

LegalTemplate.propTypes = {
  body: PropTypes.string.isRequired,
  media: PropTypes.shape({
    windowWidth: PropTypes.number.isRequired,
    windowHeight: PropTypes.number.isRequired,
    lightMode: PropTypes.bool.isRequired,
  }).isRequired,
};

export default LegalTemplate;
