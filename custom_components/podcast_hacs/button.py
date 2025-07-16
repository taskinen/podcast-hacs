"""Button platform for Podcast HACS integration."""
import logging
from typing import Any

import feedparser
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    config_data = hass.data[DOMAIN][config_entry.entry_id]
    
    async_add_entities([
        PodcastPlayButton(
            config_entry.entry_id,
            config_data["rss_url"],
            config_data["speaker_entity"],
            hass
        )
    ])


class PodcastPlayButton(ButtonEntity):
    """Button to play the latest podcast episode."""

    def __init__(self, entry_id: str, rss_url: str, speaker_entity: str, hass: HomeAssistant) -> None:
        """Initialize the button."""
        self._entry_id = entry_id
        self._rss_url = rss_url
        self._speaker_entity = speaker_entity
        self._hass = hass
        self._attr_name = "Play Latest Episode"
        self._attr_unique_id = f"{entry_id}_play_button"
        self._attr_icon = "mdi:play"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Podcast Player",
            manufacturer="Podcast HACS",
            model="RSS Player",
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            # Parse RSS feed to get latest episode
            feed = await self._hass.async_add_executor_job(
                feedparser.parse, self._rss_url
            )
            
            if not feed.entries:
                raise HomeAssistantError("No episodes found in RSS feed")
            
            latest_episode = feed.entries[0]
            
            # Find the audio URL from enclosures
            audio_url = None
            for enclosure in latest_episode.get("enclosures", []):
                if enclosure.get("type", "").startswith("audio/"):
                    audio_url = enclosure.get("href")
                    break
            
            # If no enclosure found, try links
            if not audio_url:
                for link in latest_episode.get("links", []):
                    if link.get("type", "").startswith("audio/"):
                        audio_url = link.get("href")
                        break
            
            if not audio_url:
                raise HomeAssistantError("No audio URL found in latest episode")
            
            # Play the episode on the specified speaker
            await self._hass.services.async_call(
                "media_player",
                "play_media",
                {
                    "entity_id": self._speaker_entity,
                    "media_content_id": audio_url,
                    "media_content_type": "music",
                },
                blocking=True,
            )
            
            _LOGGER.info(
                "Playing latest episode '%s' on %s",
                latest_episode.get("title", "Unknown"),
                self._speaker_entity,
            )
            
        except Exception as err:
            _LOGGER.error("Error playing podcast episode: %s", err)
            raise HomeAssistantError(f"Failed to play podcast: {err}") from err