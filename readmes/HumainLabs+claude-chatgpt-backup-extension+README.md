# Download from Firefox Extension Page!

<a href="https://addons.mozilla.org/en-US/firefox/addon/humainlabs-claude-chat-backup/">https://addons.mozilla.org/en-US/firefox/addon/humainlabs-claude-chat-backup/</a>


# HumainLabs AI Chat Backup 💾

![TypeScript](https://img.shields.io/badge/TypeScript-4.0%2B-blue.svg) ![Firefox](https://img.shields.io/badge/Firefox-57%2B-orange.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Maintained by HumainLabs.ai](https://img.shields.io/badge/Maintained%20by-HumainLabs.ai-orange)

A powerful Firefox extension for backing up your conversations from Claude.ai and ChatGPT. Save complete conversation structures, including Claude's thinking process, in easy-to-use JSON format.

<p align="center">
  <img src="humainlabs.ai.png" alt="HumainLabs.ai logo" width="30%" />
  <br>
  <h3 align="center">HumainLabs.ai</h3>
  <h5 align="center">Cognitive Framework Engineering & <br>Research for AI Cognition</h5>
  <p align="center"><a href="https://humainlabs.ai" align="center">www.HumainLabs.ai</a></p>
</p>

## Download from Firefox Extension Page

<a href="https://addons.mozilla.org/en-US/firefox/addon/humainlabs-claude-chat-backup/">https://addons.mozilla.org/en-US/firefox/addon/humainlabs-claude-chat-backup/</a>

## 📋 Table of Contents

* Overview
* Features
* Installation
* Usage
* Technical Details
* FAQ
* License

## 🔍 Overview

HumainLabs AI Chat Backup redefines how users can preserve their AI interactions by enabling effortless exporting of complete conversation structures from both Claude.ai and ChatGPT. The extension provides a seamless way to download your conversations as structured JSON files, preserving all context including Claude's thinking process.

The application manages the entire backup process:

1. **Authentication** with the AI platforms using your existing cookies
2. **Fetching** complete conversation data through the official APIs
3. **Downloading** structured JSON files to your local device

This Firefox extension focuses exclusively on providing a lightweight yet powerful tool for backing up your valuable AI conversations.

## ✨ Features

| Feature                          | Description                                                                                |
| -------------------------------- | ------------------------------------------------------------------------------------------ |
| **Multi-Platform Support**       | Backup conversations from both Claude.ai and ChatGPT                                      |
| **Complete Data Structure**      | Preserves entire conversation history including Claude's thinking process                  |
| **Single Chat Backup**           | Export just your current conversation with one click                                       |
| **Bulk Backup (Claude only)**    | Download all Claude conversations at once                                                  |
| **Intuitive Interface**          | Clean, simple UI with platform-specific styling                                            |
| **Structured JSON Format**       | Easy to process with downstream tools and analysis                                         |
| **Privacy-Focused**              | Your data stays on your device, no third-party servers                                     |
| **Smart Filename Generation**    | Automatic timestamping and chat title inclusion for easy organization                      |

## 📥 Installation

### From Firefox Add-on Store
1. Download the extension from the [Firefox Addon Store](https://addons.mozilla.org/en-US/firefox/addon/claude-ai-chat-backup/)
2. Click on "Add to Firefox" to install the extension
3. No additional configuration needed - the extension works immediately

### As a Temporary Add-on (for development/testing)
1. Download or clone the repository to your local machine
2. Build the extension using `npm run build` (or use the pre-built files)
3. In Firefox, navigate to `about:debugging#/runtime/this-firefox`
4. Click on "Load Temporary Add-on..."
5. Navigate to the extension directory and select the `manifest.json` file
6. The extension will be loaded for the current session (will be removed when Firefox is closed)

## ⚠️ Prerequisites

Before using the extension, make sure you:

1. **Are logged in** to your [Claude.ai](https://claude.ai) account (for Claude backups)
2. **Are logged in** to your [ChatGPT](https://chatgpt.com) account (for ChatGPT backups)

The extension uses your existing authenticated sessions to access the APIs, so it **cannot work** if you're not already logged in.

## 🚀 Usage

### Claude.ai Backup

1. Navigate to [Claude.ai](https://claude.ai)
2. Click on the HumainLabs extension icon in your Firefox toolbar
3. Choose either:
   - "Backup Current Claude Chat" to save only the current conversation
   - "Backup All Claude Conversations" to save all your conversations

### ChatGPT Backup

1. Navigate to [ChatGPT](https://chatgpt.com) and open a conversation
2. Click on the HumainLabs extension icon in your Firefox toolbar
3. Click on "Backup Current ChatGPT Chat" to save the current conversation

For both services, you'll be prompted to choose where to save the JSON file. The file will be named with the chat title and timestamp.

### Sample Output Structure

```json
// Claude output includes separated thinking and response content
{
  "name": "Conversation Title",
  "uuid": "conversation-id",
  "tree_state": {
    "messages": [
      {
        "sender": "assistant",
        "content": [
          {
            "type": "thinking",
            "thinking": "This is Claude's thinking process..."
          },
          {
            "type": "text",
            "text": "This is Claude's visible response..."
          }
        ]
      }
    ]
  }
}
```

## 🔧 Technical Details

- **Built with**: WebExtensions API
- **Language**: TypeScript
- **Manifest**: Version 2
- **Required Permissions**:
  - `cookies`: For authentication with AI platforms
  - `downloads`: For saving files to your device
  - `https://claude.ai/*`: For Claude.ai API access
  - `https://chatgpt.com/*`: For ChatGPT API access

## ❓ FAQ

### Is this an official extension from Anthropic or OpenAI?
No, this is an unofficial extension created by HumainLabs.ai. It is not affiliated with, endorsed by, or connected to Anthropic (Claude) or OpenAI (ChatGPT) in any way.

### Who can access my data?
Your conversations stay between you, your device, and the respective AI service providers. The extension only facilitates downloading your own data.

### How do the downloaded JSON files differ?
The Claude downloads include the structured conversation data with separate sections for thinking and response content. The ChatGPT downloads preserve the original conversation structure provided by OpenAI's API.

### How secure is this extension?
The extension only requires the permissions needed to perform its functions. It doesn't send your data anywhere except back to your device as downloaded files.

### Will you be adding more features?
The extension focuses on doing one thing well: backing up your AI conversations. We may add support for more AI platforms in the future.

### I found a bug. Will you fix it?
If you find a bug that prevents the extension from performing its core backup functionality, please report it through our GitHub repository.

## 📄 License

This project is licensed under the MIT License.

---

Maintained with ❤️ by HumainLabs.ai
