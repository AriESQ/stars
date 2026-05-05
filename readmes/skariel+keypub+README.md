# KeyPub.sh

A verified directory for SSH public keys, connecting identities to keys without managing authentication. KeyPub.sh allows users to verify ownership of their email addresses and associate them with their SSH public keys, creating a trustworthy identity system focused on user privacy.

## Features

-  Verified registry linking SSH public keys to email addresses
-  Zero installation - works with your existing SSH setup
-  Privacy-focused: you control what information is public
-  Simple email verification process
-  Free public service
-  Perfect for SSH application developers - no need to build user verification systems

## Quick Start

```bash
# Register your key with your email
ssh keypub.sh register alice@example.com

# Verify your email with the code received
ssh keypub.sh confirm VERIFICATION-CODE

# Optional: Create an alias for easier usage
alias kp='ssh keypub.sh'
```

## Available Commands

- `register <email>` - Register your SSH key with an email address
- `confirm <code>` - Verify email with code from confirmation mail
- `whoami` - Show your registration details
- `allow <email>` - Grant email visibility to another user
- `deny <email>` - Revoke email visibility from user
- `get email from <fingerprint>` - Get email for key (if authorized)
- `unregister` - Remove your key from registry
- `help` - Show help message

## Use Cases

- Single verified identity for SSH-based applications
- Lightweight alternative to OAuth for CLI applications
- Central identity system that respects privacy
- Perfect for developers building SSH-based tools

## Development

The project is built in Go and uses SQLite for data storage. Key components:

- SSH server implementation using [`gliderlabs/ssh`](https://github.com/gliderlabs/ssh)
- Email verification using SMTP or Resend API
- Rate limiting with EWMA ([Exponentially Weighted Moving Average](https://dotat.at/@/2024-09-02-ewma.html))
- Privacy-focused permission system

You can read [INSTALL.md](INSTALL.md) for more info about installation guide

## License

MIT License - see [LICENSE](LICENSE) file for details

## Website

Visit [keypub.sh](https://keypub.sh) for more information.

---
Built with ❤️ for the SSH community
