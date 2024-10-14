from dataclasses import dataclass, field

@dataclass
class OCV:
    rest_time: float = 0.0
    record_de: float = 0.0
    record_dt: float = 0.0

@dataclass
class CV:
    vs_init: list[bool] = field(default_factory=lambda: [False] * 5)
    v_step: list[float] = field(default_factory=lambda: [0.0] * 5)
    scan_rate: list[float] = field(default_factory=lambda: [0.0] * 5)
    scan_number: int = 2
    record_de: float = 0.0
    average_de: bool = False
    n_cycles: int = 0
    begin_i: float = 0.0
    end_i: float = 0.0

@dataclass
class CP:
    i_step: list[float] = field(default_factory=lambda: [0.0] * 100)
    vs_init: list[bool] = field(default_factory=lambda: [False] * 100)
    duration_step: list[float] = field(default_factory=lambda: [0.0] * 100)
    step_number: int = 0
    record_dt: float = 0.0
    average_di: float = 0.0
    n_cycles: int = 0

@dataclass
class CA:
    v_step: list[float] = field(default_factory=lambda: [0.0] * 100)
    vs_init: list[bool] = field(default_factory=lambda: [False] * 100)
    duration_step: list[float] = field(default_factory=lambda: [0.0] * 100)
    step_number: int = 0
    record_dt: float = 0.0
    average_di: float = 0.0
    n_cycles: int = 0

@dataclass
class VSCAN:
    vs_init: list[bool] = field(default_factory=lambda: [False] * 100)
    v_step: list[float] = field(default_factory=lambda: [0.0] * 100)
    scan_rate: list[float] = field(default_factory=lambda: [0.0] * 100)
    scan_number: int = 0
    record_de: float = 0.0
    n_cycles: int = 0
    begin_i: float = 0.0
    end_i: float = 0.0