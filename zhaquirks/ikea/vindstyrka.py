"""IKEA of Sweden VINDSTYRKA Air quality sensor."""
import logging

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import QuirkBuilder
from zigpy.quirks.v2.homeassistant.sensor import SensorDeviceClass
import zigpy.types as t
from zigpy.zcl.foundation import (
    BaseAttributeDefs,
    ConfigureReportingResponseRecord,
    ZCLAttributeAccess,
    ZCLAttributeDef,
)

_LOGGER = logging.getLogger(__name__)


class VOCIndex(CustomCluster):
    """IKEA VOCIndex specific cluster."""

    cluster_id = 0xFC7E

    class AttributeDefs(BaseAttributeDefs):
        """Attribute definitions."""

        measured_value = ZCLAttributeDef(
            id=0x0000,
            type=t.Single,
            mandatory=True,
            access=(ZCLAttributeAccess.Read | ZCLAttributeAccess.Report),
        )

    @property
    def _is_manuf_specific(self):
        return False

    async def configure_reporting_multiple(
        self,
        attributes: dict[int | str, tuple[int, int, int]],
        manufacturer: int | None = None,
    ) -> list[ConfigureReportingResponseRecord]:
        """Foio"""
        _LOGGER.info(f"yey {attributes} {manufacturer}")


(
    QuirkBuilder("IKEA of Sweden", "VINDSTYRKA")
    .replaces(VOCIndex)
    .sensor(
        VOCIndex.AttributeDefs.measured_value.name,
        VOCIndex.cluster_id,
        device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
    )
    .add_to_registry()
)
