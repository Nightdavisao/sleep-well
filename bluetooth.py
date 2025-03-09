from gi.repository import Gio, GLib

bus_type = Gio.BusType.SYSTEM
bus_name = 'org.bluez'
object_path = '/org/bluez/hci0'

BLUEZ_SERVICE = 'org.bluez'

class BTDevice():
    def __init__(self, device_mac):
        self.device_mac = device_mac
        self.device_path = self._get_device_path()
        self.device = Gio.DBusProxy.new_for_bus_sync(
            bus_type,
            Gio.DBusProxyFlags.NONE,
            None,
            bus_name,
            self.device_path,
            BLUEZ_SERVICE + '.Device1',
            None
        )
        
    def _get_device_path(self):
        return f'{object_path}/dev_{self.device_mac.replace(":", "_")}' 
    
    def get_property(self, property_name):
        device = Gio.DBusProxy.new_for_bus_sync(
            Gio.BusType.SYSTEM,
            Gio.DBusProxyFlags.NONE,
            None,
            BLUEZ_SERVICE,
            self.device_path,
            "org.freedesktop.DBus.Properties",
            None
        )

        value = device.call_sync(
            "Get",
            GLib.Variant("(ss)", ("org.bluez.Device1", property_name)),
            Gio.DBusCallFlags.NONE,
            -1,
            None
        )

        return value.unpack()[0]
    
    def is_connected(self):
        return self.get_property('Connected')
    
    def connect_device(self):
        self.device.Connect()
        
    def disconnect_device(self):
        self.device.Disconnect()