from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN, PRODUCT_COORDINATORS
from .entity import AldesProductDataUpdateCoordinator, AldesProductEntity

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinators = hass.data[DOMAIN][entry.entry_id][PRODUCT_COORDINATORS]
    
    async_add_entities(
        [
            AldesProductEntityModeSelect(coordinator) for coordinator in coordinators
        ] + [
            AldesProductOutsideTempSensor(coordinator) for coordinator in coordinators  # Aggiungi il sensore per la temperatura esterna
        ]
    )

class AldesProductEntityModeSelect(AldesProductEntity, SelectEntity):

    _attr_icon = "mdi:tune"
    _attr_unit_of_measurement = None
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: AldesProductDataUpdateCoordinator) -> None:
        super().__init__(coordinator, 'Mode Selector')

        self._attr_options = coordinator.product.get_display_modes()

    @property
    def current_option(self) -> str:
        return self.coordinator.product.get_display_mode()

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.product.maybe_set_mode_from_display(option)
        await self.coordinator.async_request_refresh()


# Nuova classe per il sensore della temperatura esterna (AIR_OUTSIDE_TPT)
class AldesProductOutsideTempSensor(AldesProductEntity, SensorEntity):

    _attr_icon = "mdi:thermometer"

    def __init__(self, coordinator: AldesProductDataUpdateCoordinator) -> None:
        super().__init__(coordinator, 'Outside Air Temperature')

    @property
    def native_value(self):
        return self.coordinator.product.air_outside_tpt  # Restituisce il valore della temperatura esterna

    @property
    def native_unit_of_measurement(self):
        return "°C"
