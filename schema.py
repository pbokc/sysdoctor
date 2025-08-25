from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ProcInfo:
    # drss_per_min is a process' resident set size (RSS) change per minute
    pid: int; name: str; cpu: float; rss: int; drss_per_min: int = 0

@dataclass
class Snapshot:
    t: float
    cpu_total: float
    mem_total: int
    mem_avail: int
    swap_used: int
    disk_rbps: int
    disk_wbps: int
    net_recv_bps: int
    net_sent_bps: int
    procs: List[ProcInfo]
