import React, { Component } from 'react';
import PropTypes from 'prop-types';
import getColors from '../../styles/getColors';
import getFonts from '../../styles/getFonts';
import getStyles from '../../styles/getStyles';
import FreshiButton from '../common/FreshiButton';

class PasswordReset extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const {
      match, media, lightMode,
    } = this.props;
    const { id, token } = match.params;
    const { windowWidth } = media;
    const colors = getColors(lightMode);
    const styles = getStyles(windowWidth);
    const fonts = getFonts(windowWidth);
    const host = window.location.origin;
    const currentRoute = `${host}/reset-password/${id}/${token}`;
    const deeplink = `freshi://${host}/reset-password?userId=${id}&authToken=${token}`;
    // when this page renders it will open the password reset page in the app automatically.
    // the deeplink specifies which screen in the app to direct to and what data to send.
    // in this case, user id and token.
    window.location = deeplink;
    return (
      <div style={{
        display: 'block',
        ...styles.padding,
        backgroundColor: colors.background.color,
      }}
      >
        <div style={{
          ...fonts.largeTitle,
          ...colors.interactiveFocus,
        }}
        >
          Freshi
        </div>
        <br />
        <div style={{
          ...fonts.headline,
          ...colors.highContrast,
        }}
        >
          To reset your password:
        </div>
        <div style={{
          ...fonts.body,
          ...colors.highContrast,
        }}
        >
          <br />
          1. Download the Freshi app on your iPhone or tablet.
          <br />
          2. Open the Freshi app on your iPhone or tablet.
          <br />
          3. On the same device, go to this url: &nbsp;
          <br />
          <div style={{
            ...styles.marginTop,
            ...styles.marginBottom,
          }}
          >
            <FreshiButton
              label="visit url"
              onClick={() => {
                window.open(
                  currentRoute,
                  '_blank', // open in a new window
                );
              }}
              backgroundColor={colors.background.color}
              forgroundColor={colors.interactiveFocus.color}
              media={media}
              style={{
                ...styles.marginRight,
              }}
            />
            <FreshiButton
              label="copy url"
              onClick={() => {
                navigator.clipboard.writeText(currentRoute);
              }}
              backgroundColor={colors.interactiveFocus.color}
              forgroundColor={colors.background.color}
              media={media}
            />
          </div>
          4. Reset your password and enjoy!
          <br />
          <br />
          If you still can&apos;t access your account,
          <br />
          send us an email and we&apos;ll be happy to help you out!
          <br />
          <div style={{
            ...styles.marginTop,
            ...styles.marginBottom,
          }}
          >
            <FreshiButton
              label="send email"
              onClick={() => {
                window.location.href = 'mailto: casey@freshi.io';
              }}
              backgroundColor={colors.background.color}
              forgroundColor={colors.interactiveFocus.color}
              media={media}
              style={{
                ...styles.marginRight,
              }}
            />
            <FreshiButton
              label="copy email"
              onClick={() => {
                navigator.clipboard.writeText('casey@freshi.io');
              }}
              backgroundColor={colors.interactiveFocus.color}
              forgroundColor={colors.background.color}
              media={media}
            />
          </div>
        </div>
      </div>
    );
  }
}

PasswordReset.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      id: PropTypes.number.isRequired,
      token: PropTypes.string.isRequired,
    }).isRequired,
  }).isRequired,
  media: PropTypes.shape({
    windowHeight: PropTypes.number.isRequired,
    windowWidth: PropTypes.number.isRequired,
    lightMode: PropTypes.bool.isRequired,
  }).isRequired,
  lightMode: PropTypes.bool.isRequired,
};

export default PasswordReset;
