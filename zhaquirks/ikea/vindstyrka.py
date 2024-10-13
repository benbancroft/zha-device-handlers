"""IKEA of Sweden VINDSTYRKA Air quality sensor."""

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import QuirkBuilder
from zigpy.quirks.v2.homeassistant.sensor import SensorDeviceClass
import zigpy.types as t
from zigpy.zcl.foundation import (
    BaseAttributeDefs,
    ReportingConfig,
    ZCLAttributeAccess,
    ZCLAttributeDef,
)


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


(
    QuirkBuilder("IKEA of Sweden", "VINDSTYRKA")
    .replaces(VOCIndex)
    .sensor(
        VOCIndex.AttributeDefs.measured_value.name,
        VOCIndex.cluster_id,
        device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        reporting_config=ReportingConfig(
            min_interval=0, max_interval=60, reportable_change=1
        ),
    )
    .add_to_registry()
)
