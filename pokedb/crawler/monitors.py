from spidermon import monitors
from spidermon.contrib.actions.discord.notifiers import SendDiscordMessageSpiderFinished
from spidermon.contrib.scrapy.monitors.suites import SpiderCloseMonitorSuite


@monitors.name("Pokemon count")
class CustomSpiderCloseMonitorSuite(SpiderCloseMonitorSuite):
    # monitors = [
    #     PokemonCountMonitor,
    # ]

    monitors_finished_actions = [
        SendDiscordMessageSpiderFinished,
    ]
