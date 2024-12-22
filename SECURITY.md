# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of XRouter seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report a Security Vulnerability?

Please send an email to security@xrouter.ru with:

1. Description of the vulnerability
2. Steps to reproduce the issue
3. Potential impact
4. Any additional details that could help us address the issue

### What to Expect

1. **Initial Response**: We will acknowledge receipt of your vulnerability report within 24 hours.
2. **Status Updates**: We will provide status updates as we investigate.
3. **Resolution Timeline**: We aim to resolve critical issues within 7 days.

### Security Measures

XRouter implements several security measures:

1. **Authentication**:
   - API key validation
   - OAuth 2.0 with PKCE
   - JWT with 1-year expiration
   - Immediate token revocation on logout

2. **Data Protection**:
   - All data is encrypted in transit (HTTPS)
   - API keys are hashed in storage
   - No storage of provider credentials
   - No caching of model responses

3. **Rate Limiting**:
   - Per-key rate limits
   - DDoS protection
   - Automatic blocking of suspicious activity

4. **Monitoring**:
   - Real-time security monitoring
   - Automated vulnerability scanning
   - Regular security audits
   - Incident response procedures

### Security Best Practices

When using XRouter:

1. **API Keys**:
   - Keep your API keys secure
   - Don't commit keys to source control
   - Rotate keys periodically
   - Use separate keys for development/production

2. **OAuth Integration**:
   - Always use PKCE
   - Implement proper token storage
   - Handle token revocation
   - Validate tokens on critical operations

3. **Rate Limits**:
   - Implement retry with backoff
   - Monitor your usage
   - Set up alerts for unusual patterns
   - Contact support for limit increases

## Disclosure Policy

- We follow responsible disclosure principles
- Security issues are fixed in private repositories
- Patches are released before public disclosure
- Credit is given to security researchers

## Security Updates

Security updates will be released through:
1. GitHub Security Advisories
2. Email notifications to registered users
3. Changelog updates
4. Security advisory in our documentation

## Contact

For security issues: security@xrouter.ru
For general support: support@xrouter.ru