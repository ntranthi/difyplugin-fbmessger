# Facebook Messenger Plugin for Dify

[![Test](https://github.com/[username]/dify-facebook-messenger/actions/workflows/test.yml/badge.svg)](https://github.com/[username]/dify-facebook-messenger/actions/workflows/test.yml)
[![Release](https://github.com/[username]/dify-facebook-messenger/actions/workflows/release.yml/badge.svg)](https://github.com/[username]/dify-facebook-messenger/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Dify plugin for integrating with Facebook Messenger. This plugin handles webhook events from Facebook Messenger and can send messages back to users.

## Features

- Facebook Messenger webhook handling
- Automatic message response
- Webhook verification
- Error handling and logging
- Request validation using Pydantic
- Type hints for better code maintainability

## Installation

### From GitHub Releases

1. Go to the [Releases](https://github.com/[username]/dify-facebook-messenger/releases) page
2. Download the latest `facebook-messenger-x.x.x.difypkg` file
3. Install the plugin through your Dify dashboard

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/[username]/dify-facebook-messenger.git
   cd dify-facebook-messenger
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the package:
   ```bash
   python build.py
   ```

4. The generated `facebook-messenger-x.x.x.difypkg` file can be installed through your Dify dashboard

## Configuration

The plugin requires the following configuration:

### Required Settings
- `page_access_token` (secret): Your Facebook Page Access Token
- `verify_token` (secret): Your webhook verification token (you choose this)

### Optional Settings
- `api_version` (string): Facebook Graph API version (default: "v18.0")

## Development

### Prerequisites
- Python 3.10 or higher
- pip for package management
- Facebook Page
- Facebook App with Messenger functionality enabled

### Setup for Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8
   ```

### Running Tests

```bash
pytest tests/
```

### Code Style

This project uses flake8 for code style checking:

```bash
flake8 .
```

### Creating a Release

1. Update version in `difypkg.json`
2. Create and push a new tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. GitHub Actions will automatically:
   - Build the package
   - Create a release
   - Upload the difypkg file

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions and support:
1. Check Facebook's [Messenger Platform documentation](https://developers.facebook.com/docs/messenger-platform)
2. Open an issue in the repository
3. Contact the Dify support team 