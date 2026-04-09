"""
Frictionshift: computational implementation for platform economics / digital markets analysis.

Frictionshift refers to the strategic relocation of transaction costs and barriers across different stages of the customer journey to maximize extraction while maintaining the perception of low friction. Platforms create "free" entry points but impose significant costs at exit or intermediate stages (e.g., free signup with expensive cancellation fees, or low advertised prices with hidden final costs). This module provides a reproducible calculator that validates the canonical channels, normalizes each series, computes a weighted index, and supports simple counterfactual policy simulation. The design is intentionally transparent so researchers can inspect how the concept moves from definition to code. Typical uses include comparative diagnostics, notebook-based scenario testing, and integration into empirical pipelines where consistent measurement matters as much as prediction.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# Frictionshift channels track the observable anatomy of the canonical definition.
TERM_CHANNELS = [
    "entry_friction_relief",  # Entry friction relief mitigates exposure when it is high.
    "mid_journey_friction",  # Mid journey friction captures a distinct economic channel.
    "exit_friction",  # Exit friction captures a distinct economic channel.
    "hidden_fee_intensity",  # Hidden fee intensity captures a distinct economic channel.
    "switching_penalty",  # Switching penalty captures a distinct economic channel.
    "cancellation_cost",  # Cancellation cost captures a distinct economic channel.
    "transparency_level",  # Transparency level mitigates exposure when it is high.
]

# Weighted channels preserve the repository's existing score logic.
WEIGHTED_CHANNELS = [
    "entry_friction_relief",
    "mid_journey_friction",
    "exit_friction",
    "hidden_fee_intensity",
    "switching_penalty",
    "cancellation_cost",
    "transparency_level",
]

# Default weights encode the relative economic importance of each weighted channel.
DEFAULT_WEIGHTS: dict[str, float] = {
    "entry_friction_relief": 0.14,  # Entry friction relief mitigates exposure when it is high.
    "mid_journey_friction": 0.16,  # Mid journey friction captures a distinct economic channel.
    "exit_friction": 0.2,  # Exit friction captures a distinct economic channel.
    "hidden_fee_intensity": 0.16,  # Hidden fee intensity captures a distinct economic channel.
    "switching_penalty": 0.14,  # Switching penalty captures a distinct economic channel.
    "cancellation_cost": 0.12,  # Cancellation cost captures a distinct economic channel.
    "transparency_level": 0.08,  # Transparency level mitigates exposure when it is high.
}


class FrictionshiftCalculator:
    """
    Compute Frictionshift index scores from tabular data.

    Parameters
    ----------
    weights : dict[str, float] | None
        Optional weights overriding DEFAULT_WEIGHTS. Keys must match
        WEIGHTED_CHANNELS and values must sum to 1.0.
    """

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        # Alternative weights are useful for robustness checks across specifications.
        self.weights = weights or DEFAULT_WEIGHTS.copy()

        # Exact key matching prevents silent omission of economically relevant channels.
        if set(self.weights) != set(WEIGHTED_CHANNELS):
            raise ValueError(f"Weights must include exactly these channels: {WEIGHTED_CHANNELS}")

        # Unit-sum weights keep the index interpretable across datasets.
        if abs(sum(self.weights.values()) - 1.0) >= 1e-6:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def _normalise(series: pd.Series) -> pd.Series:
        """
        Return min-max normalized values on the unit interval.
        """
        lo = float(series.min())
        hi = float(series.max())
        if hi == lo:
            # Degenerate channels should not create spurious variation.
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - lo) / (hi - lo)

    def calculate_frictionshift(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute normalized channels, composite scores, and qualitative bands.
        """
        # Full channel validation keeps the score tied to the canonical definition.
        missing = [channel for channel in TERM_CHANNELS if channel not in df.columns]
        if missing:
            raise ValueError(f"Missing Frictionshift channels: {missing}")

        out = df.copy()
        for channel in TERM_CHANNELS:
            out[f"{channel}_norm"] = self._normalise(out[channel])

        # Positive channels intensify the mechanism while negative channels offset it.
        out["frictionshift_index"] = (
            + self.weights["mid_journey_friction"] * out["mid_journey_friction_norm"]
            + self.weights["exit_friction"] * out["exit_friction_norm"]
            + self.weights["hidden_fee_intensity"] * out["hidden_fee_intensity_norm"]
            + self.weights["switching_penalty"] * out["switching_penalty_norm"]
            + self.weights["cancellation_cost"] * out["cancellation_cost_norm"]
            + self.weights["entry_friction_relief"] * (1.0 - out["entry_friction_relief_norm"])
            + self.weights["transparency_level"] * (1.0 - out["transparency_level_norm"])
        )

        # Three bands keep the metric usable in audits, papers, and dashboards.
        out["frictionshift_band"] = pd.cut(
            out["frictionshift_index"],
            bins=[-np.inf, 0.33, 0.66, np.inf],
            labels=["low", "moderate", "high"],
        )
        return out

    def simulate_policy(self, df: pd.DataFrame, channel: str, reduction: float = 0.2) -> pd.DataFrame:
        """
        Simulate a policy shock that reduces one observed channel.
        """
        if channel not in TERM_CHANNELS:
            raise ValueError(f"Unknown Frictionshift channel: {channel}")
        if reduction < 0.0 or reduction > 1.0:
            raise ValueError("reduction must be between 0.0 and 1.0")

        # Counterfactual shocks translate reforms into score movements.
        df_policy = df.copy()
        df_policy[channel] = df_policy[channel] * (1 - reduction)
        return self.calculate_frictionshift(df_policy)


if __name__ == "__main__":
    sample = pd.read_csv("frictionshift_dataset.csv")
    calc = FrictionshiftCalculator()
    print(calc.calculate_frictionshift(sample)[["frictionshift_index", "frictionshift_band"]].head(10).to_string(index=False))

    scenario = calc.simulate_policy(sample, channel="entry_friction_relief", reduction=0.15)
    print("\nPolicy Scenario Mean Index:")
    print(float(scenario["frictionshift_index"].mean()))
