# Podcast player

A Home Assistant custom integration that allows you to stream the latest episode of any podcast to your speakers.

## Features

- Easy configuration through Home Assistant UI
- Automatically fetches the latest episode from any RSS feed
- One-click playback to any media player in Home Assistant
- Can be triggered manually or through automations

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add `https://github.com/taskinen/podcast-hacs` as a custom repository with category "Integration"
5. Search for "Podcast player" and install
6. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/podcast_hacs` folder from this repository
2. Copy it to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services → Add Integration
2. Search for "Podcast player"
3. Enter the RSS feed URL of your podcast
4. Select the media player entity where you want to play the podcast
5. Click Submit

## Usage

After configuration, you'll see a "Play Latest Episode" button in your integration. Click this button to:

1. Fetch the latest episode from the RSS feed
2. Automatically play it on your selected speaker

You can also use this button in automations to schedule podcast playback.

## Supported Platforms

- Any RSS feed with audio enclosures
- Any Home Assistant media player that supports URL playback

## Troubleshooting

- Make sure your RSS feed URL is valid and contains audio episodes
- Ensure your media player supports direct URL playback
- Check Home Assistant logs for detailed error messages

## Contributing

Issues and pull requests are welcome at https://github.com/taskinen/podcast-hacs

## License

This project is licensed under the Apache License 2.0.

## Author

Created by Timo Taskinen (timo.taskinen@iki.fi)