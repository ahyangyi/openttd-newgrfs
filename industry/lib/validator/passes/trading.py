from industry.lib.economy import FreePort


def check_trading(economy):
    if economy.parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE"):
        assert any(isinstance(v, FreePort) for v in economy.graph.values())
