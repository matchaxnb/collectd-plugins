"""Collect sockstat data (currently only FRAG:)"""
import collectd

PLUGIN_NAME = "sockstat"


def parse_and_emit_frag(frag_line):
    assert frag_line.startswith("FRAG:")
    spl = frag_line.split(" ")
    assert len(spl) == 5 and spl[1] == "inuse" and spl[3] == "memory"
    res = {"inuse": int(spl[2]), "memory": int(spl[4])}
    for k, v in res.items():
        val = collectd.Values(
            type="gauge",
            plugin=PLUGIN_NAME,
            plugin_instance="",
            type_instance=k,
            values=[v],
        )
        val.dispatch()
        collectd.debug(f"DBUG: {val}")


def read_sockstat():
    l = []
    with open("/proc/net/sockstat", "r", encoding="utf-8") as fh:
        l = fh.readlines()
    # we might want to add extra metrics later on
    for line in l:
        if line.startswith("FRAG:"):
            parse_and_emit_frag(line)


def sockstat_callback(conf):
    collectd.register_read(read_sockstat, 15)


collectd.register_config(sockstat_callback)
