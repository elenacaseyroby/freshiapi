import React, { Component } from 'react';
import LegalTemplate from '../LegalTemplate/LegalTemplate';
// import PropTypes from 'prop-types';
// import getColors from '../../styles/getColors';
// import getFonts from '../../styles/getFonts';
// import getStyles from '../../styles/getStyles';
// import FreshiButton from '../common/FreshiButton';

class PrivacyPolicy extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div>
        <LegalTemplate body="<h1>body text here</h1>" />
      </div>
    );
  }
}

PrivacyPolicy.propTypes = {
};

export default PrivacyPolicy;
