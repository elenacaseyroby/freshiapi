import React from 'react';
import PropTypes from 'prop-types';

const LegalTemplate = ({
  body,
}) => (
  <div>
    {body}
  </div>
);

LegalTemplate.propTypes = {
  body: PropTypes.string.isRequired,
};

export default LegalTemplate;
