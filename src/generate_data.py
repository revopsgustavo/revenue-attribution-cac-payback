from __future__ import annotations

from revenue_attribution_pipeline import DB, generate_data


if __name__ == "__main__":
    frames = generate_data()
    print(
        f"Generated {len(frames['leads'])} leads, "
        f"{len(frames['opportunities'])} opportunities and "
        f"{len(frames['customers'])} customers."
    )
    print(f"SQLite database generated at {DB}")
