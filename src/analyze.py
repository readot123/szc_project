"""Generate a compact descriptive analysis of hourly bike demand."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "raw" / "bike_sharing.csv"
OUTPUT_DIR = ROOT / "outputs"
REQUIRED_COLUMNS = {
    "season", "year", "hour", "holiday", "weekday", "weathersit",
    "temp", "humidity", "windspeed", "bikes_per_hour",
}


def load_data(path: Path = DATA_FILE) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    frame = frame.drop_duplicates().dropna(subset=list(REQUIRED_COLUMNS)).copy()
    if not frame["hour"].between(0, 23).all():
        raise ValueError("hour must be between 0 and 23")
    if (frame["bikes_per_hour"] < 0).any():
        raise ValueError("bikes_per_hour must be non-negative")
    return frame


def summarize(frame: pd.DataFrame) -> dict[str, int | float]:
    hourly = frame.groupby("hour")["bikes_per_hour"].mean()
    return {
        "records": int(len(frame)),
        "total_rides": int(frame["bikes_per_hour"].sum()),
        "average_rides_per_hour": round(float(frame["bikes_per_hour"].mean()), 2),
        "median_rides_per_hour": round(float(frame["bikes_per_hour"].median()), 2),
        "peak_hour": int(hourly.idxmax()),
        "peak_hour_average_rides": round(float(hourly.max()), 2),
    }


def save_chart(series: pd.Series, title: str, ylabel: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    series.plot(ax=ax, marker="o", color="#087E8B")
    ax.set(title=title, xlabel=series.index.name or "", ylabel=ylabel)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def run() -> dict[str, int | float]:
    frame = load_data()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    hourly = frame.groupby("hour")["bikes_per_hour"].agg(["mean", "median", "sum"])
    weekday = frame.groupby("weekday")["bikes_per_hour"].agg(["mean", "median", "sum"])
    weather = frame.groupby("weathersit")["bikes_per_hour"].mean()
    hourly.to_csv(OUTPUT_DIR / "hourly_demand.csv")
    weekday.to_csv(OUTPUT_DIR / "weekday_demand.csv")
    save_chart(hourly["mean"], "Average bike demand by hour", "Average rides", OUTPUT_DIR / "hourly_demand.png")
    save_chart(weather, "Average bike demand by weather", "Average rides", OUTPUT_DIR / "weather_demand.png")
    summary = summarize(frame)
    (OUTPUT_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    run()
