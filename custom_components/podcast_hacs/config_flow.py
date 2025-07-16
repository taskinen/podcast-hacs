"""Config flow for Podcast HACS integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
import feedparser

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required("rss_url"): str,
    vol.Required("speaker_entity"): selector.EntitySelector(
        selector.EntitySelectorConfig(
            domain=["media_player"]
        )
    ),
})


class PodcastHacsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Podcast HACS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        # Validate RSS feed URL
        try:
            feed = await self.hass.async_add_executor_job(
                feedparser.parse, user_input["rss_url"]
            )
            if not feed.entries:
                errors["rss_url"] = "invalid_rss_url"
        except Exception:
            errors["rss_url"] = "cannot_connect"

        # Validate speaker entity exists
        if user_input["speaker_entity"] not in self.hass.states.async_entity_ids("media_player"):
            errors["speaker_entity"] = "invalid_speaker"

        if not errors:
            return self.async_create_entry(
                title=f"Podcast: {feed.feed.get('title', 'Unknown')}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )