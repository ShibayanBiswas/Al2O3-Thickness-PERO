from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactSpec:
    src: Path
    dst_rel: Path


def _ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def _copy(spec: ArtifactSpec, root_out: Path) -> None:
    if not spec.src.exists():
        return
    dst = root_out / spec.dst_rel
    _ensure_dir(dst.parent)
    shutil.copy2(spec.src, dst)


def _pick_one(base: Path, pattern: str) -> Path | None:
    hits = sorted(base.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return hits[0] if hits else None


def _short_target(name: str) -> str:
    n = name.lower().strip()
    if n.startswith("rct"):
        return "Rct"
    if n.startswith("ice"):
        return "Ice"
    if "reversible" in n or "capacity_mah_g" in n or "capacity" in n:
        return "Capacity"
    if "retention" in n:
        return "Retention"
    return "Target"


def build_specs(project_root: Path) -> list[ArtifactSpec]:
    outputs = project_root / "outputs"
    specs: list[ArtifactSpec] = []

    # Reports
    rep = outputs / "reports" / "summary_report.md"
    specs.append(ArtifactSpec(rep, Path("Reports") / "Summary Report.md"))

    # Models tables
    models_tables = outputs / "models" / "tables"
    for pat, name in [
        ("model_comparison*.csv", "Model Comparison.csv"),
        ("model_comparison*.xlsx", "Model Comparison.xlsx"),
        ("best_models*.csv", "Best Models.csv"),
        ("metrics__*.csv", "Metrics Per Model.csv"),
    ]:
        hit = _pick_one(models_tables, pat)
        if hit is not None:
            specs.append(ArtifactSpec(hit, Path("Models") / name))

    # EDA tables (audit + grouped summaries)
    eda_tables = outputs / "eda" / "tables"
    for pat, name in [
        ("data_audit*.csv", "Data Audit.csv"),
        ("thickness_value_counts*.csv", "Thickness Value Counts.csv"),
        ("grouped_by_thickness*.csv", "Grouped By Thickness.csv"),
        ("correlation_pearson*.csv", "Pearson Correlation.csv"),
        ("correlation_spearman*.csv", "Spearman Correlation.csv"),
    ]:
        hit = _pick_one(eda_tables, pat)
        if hit is not None:
            specs.append(ArtifactSpec(hit, Path("Eda") / "Tables" / name))

    # Explainability plots
    shap_dir = outputs / "explainability" / "plots" / "Shap"
    pdp_dir = outputs / "explainability" / "plots" / "PartialDependence"
    sens_dir = outputs / "explainability" / "plots" / "Sensitivity"

    if shap_dir.exists():
        for f in sorted(shap_dir.glob("shap_beeswarm__*.png")):
            t = f.stem.split("__", 1)[1]
            specs.append(ArtifactSpec(f, Path("Explainability") / "Shap" / f"Shap Beeswarm {_short_target(t)}.png"))
        for f in sorted(shap_dir.glob("shap_bar__*.png")):
            t = f.stem.split("__", 1)[1]
            specs.append(ArtifactSpec(f, Path("Explainability") / "Shap" / f"Shap Bar {_short_target(t)}.png"))
        for f in sorted(shap_dir.glob("shap_dependence__*.png")):
            t = f.stem.split("__", 1)[1]
            specs.append(ArtifactSpec(f, Path("Explainability") / "Shap" / f"Shap Dependence {_short_target(t)}.png"))
        # only sample one waterfall per target to keep repo small
        for f in sorted(shap_dir.glob("shap_waterfall__*__sample1.png")):
            t = f.stem.split("__", 2)[1]
            specs.append(ArtifactSpec(f, Path("Explainability") / "Shap" / f"Shap Waterfall {_short_target(t)}.png"))

    if pdp_dir.exists():
        for f in sorted(pdp_dir.glob("*.png")):
            t = f.stem.split("__", 1)[-1]
            specs.append(ArtifactSpec(f, Path("Explainability") / "Partial Dependence" / f"Partial Dependence {_short_target(t)}.png"))

    if sens_dir.exists():
        for f in sorted(sens_dir.glob("*.png")):
            t = f.stem.split("__", 1)[-1]
            specs.append(ArtifactSpec(f, Path("Explainability") / "Sensitivity" / f"Sensitivity {_short_target(t)}.png"))

    return specs


def main() -> int:
    project_root = Path(__file__).resolve().parent
    out_root = project_root / "artifacts"

    if out_root.exists():
        shutil.rmtree(out_root)
    _ensure_dir(out_root)

    specs = build_specs(project_root)
    for spec in specs:
        _copy(spec, out_root)

    # small manifest
    manifest = out_root / "Manifest.txt"
    rels = sorted([str(s.dst_rel).replace("\\", "/") for s in specs])
    manifest.write_text("\n".join(rels) + "\n", encoding="utf-8")
    print(f"Artifacts Exported: {len(specs)} Files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

