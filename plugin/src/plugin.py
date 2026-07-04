from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label

class OpenTunnelMain(Screen):
    skin = """
    <screen name="OpenTunnelMain" position="center,center" size="600,400" title="OpenTunnel">
        <widget name="status" position="50,50" size="500,40" font="Regular;24" />
        <widget name="info" position="50,120" size="500,40" font="Regular;20" />
    </screen>
    """

    def init(self, session):
        Screen.init(self, session)

        self["status"] = Label("Status: DISCONNECTED")
        self["info"] = Label("SSH Tunnel Manager - OpenTunnel")

        self["actions"] = ActionMap(["OkCancelActions"], {
            "ok": self.connect,
            "cancel": self.close
        }, -1)

    def connect(self):
        self["status"].setText("Status: CONNECTING...")
        # اینجا بعداً موتور SSH اضافه می‌کنیم

def main(session, **kwargs):
    session.open(OpenTunnelMain)

def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="OpenTunnel",
            description="SSH Tunnel Manager for Enigma2",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            fnc=main
        )
    ]
