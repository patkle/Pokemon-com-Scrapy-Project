from spidermon import MonitorSuite
from spidermon.contrib.actions.telegram.notifiers import (
    SendTelegramMessageSpiderFinished,
    SendTelegramMessageSpiderRunning,
    SendTelegramMessageSpiderStarted,
)
from spidermon.contrib.scrapy.monitors import ErrorCountMonitor, ItemCountMonitor


class SpiderOpenMonitorSuite(MonitorSuite):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_monitors_finished_action(SendTelegramMessageSpiderStarted)


class SpiderCloseMonitorSuite(MonitorSuite):
    """Monitor suite which sends a Telegram message when the spider stops"""

    monitors = [
        ItemCountMonitor,
        ErrorCountMonitor,
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_monitors_finished_action(SendTelegramMessageSpiderFinished)


class CustomTelegramMessageSpiderRunning(SendTelegramMessageSpiderRunning):
    message_template = "telegram-periodic.jinja"


class PeriodicMonitorSuite(MonitorSuite):
    monitors = [ErrorCountMonitor]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_monitors_finished_action(CustomTelegramMessageSpiderRunning)
