import React, { Component } from 'react';
import PropTypes from 'prop-types';
import LegalTemplate from '../LegalTemplate/LegalTemplate';
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
    const { media } = this.props;
    const body = `<h2>END USER LICENSE AGREEMENT</h2>
    <h3>Last updated February 10, 2021</h3>
    
    <p>
    Freshi is licensed to You (End-User) by Freshi, located at 515 Decatur Street Apt 2F, Brooklyn, New York 11233, United States (hereinafter: Licensor), for use only under the terms of this License Agreement.
    
    By downloading the Application from the Apple AppStore, and any update thereto (as permitted by this License Agreement), You indicate that You agree to be bound by all of the terms and conditions of this License Agreement, and that You accept this License Agreement.
    
    The parties of this License Agreement acknowledge that Apple is not a Party to this License Agreement and is not bound by any provisions or obligations with regard to the Application, such as warranty, liability, maintenance and support thereof. Freshi, not Apple, is solely responsible for the licensed Application and the content thereof.
    
    This License Agreement may not provide for usage rules for the Application that are in conflict with the latest App Store Terms of Service. Freshi acknowledges that it had the opportunity to review said terms and this License Agreement is not conflicting with them.
    
    All rights not expressly granted to You are reserved.
    </p>
    
    <h2>1. THE APPLICATION</h2>
    <p>
    Freshi (hereinafter: Application) is a piece of software created to provide a social media for food lovers to contribute, share, and distribute, and disseminate recipes, guidelines, dietary information, meal photos et all, and to empower users to better understand and educate 
    </p>`;
    return (
      <div>
        <LegalTemplate body={body} media={media} />
      </div>
    );
  }
}

PrivacyPolicy.propTypes = {
  media: PropTypes.shape({
    windowWidth: PropTypes.number.isRequired,
    lightMode: PropTypes.bool.isRequired,
  }).isRequired,
};

export default PrivacyPolicy;
