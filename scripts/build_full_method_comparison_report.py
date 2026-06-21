"""Build the current full-method comparison report."""

from __future__ import annotations

import csv
import importlib.util
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def row(path: str, method: str, variant: str = "raw") -> dict[str, str] | None:
    rows = read_csv(PROJECT_ROOT / path)
    return next((item for item in rows if item.get("method", item.get("model")) == method and item.get("variant") == variant), None)


def fmt_pct(value: str | None) -> str:
    try:
        return f"{float(value or '') * 100:.2f}%"
    except ValueError:
        return "n/a"


def fmt_num(value: str | None) -> str:
    try:
        return f"{float(value or ''):.2f}"
    except ValueError:
        return "n/a"


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def git_head(path: Path) -> str:
    if not (path / ".git").exists():
        return "not_cloned"
    result = subprocess.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "incomplete_clone"


def table_row(name: str, route: str, data: dict[str, str] | None, status: str) -> str:
    if data is None:
        return f"| {name} | {route} | n/a | n/a | n/a | n/a | n/a | n/a | {status} |"
    return (
        f"| {name} | {route} | {data.get('days', 'n/a')} | {fmt_pct(data.get('cum_return'))} | "
        f"{fmt_pct(data.get('ann_return'))} | {fmt_num(data.get('sharpe'))} | {fmt_pct(data.get('mdd'))} | "
        f"{fmt_pct(data.get('avg_turnover'))} | {status} |"
    )


def build_report() -> str:
    best_full = row("experiments/trade_validation/trade_validation_summary.csv", "rd_agent_quant")
    best_2026 = row("experiments/trade_validation_2026_ytd/trade_validation_summary.csv", "rd_agent_quant")
    proxy_overlap = row("experiments/full_method_comparison/rd_agent_quant_proxy_overlap_trade_validation_summary.csv", "rd_agent_quant_proxy_overlap")
    official_da = row("experiments/full_method_comparison/doubleadapt_official_core_trade_validation_summary.csv", "doubleadapt_official_core")
    fusion = row("experiments/full_method_comparison/rda_doubleadapt_core_fusion_trade_validation_summary.csv", "rda_doubleadapt_core_fusion")
    official_da_neutral = row("experiments/full_method_comparison/doubleadapt_official_core_trade_validation_summary.csv", "doubleadapt_official_core", "industry_size_neutral")
    fusion_neutral = row("experiments/full_method_comparison/rda_doubleadapt_core_fusion_trade_validation_summary.csv", "rda_doubleadapt_core_fusion", "industry_size_neutral")

    env_python = subprocess.run(["python", "--version"], capture_output=True, text=True, check=False).stdout.strip() or "unknown"
    lines = [
        "# 完整版方法与融合加强版对比状态",
        "",
        "交易协议固定为 CSI300、H5 score、Top30 等权多头、日频调仓、单边 10 bps 换手成本。官方 DoubleAdapt core 已在本地跑通；RD-Agent 官方应用栈仍未跑通，因此当前融合版是“RD-Agent-Quant proxy score + 官方 DoubleAdapt core score”的可执行融合。由于官方 DoubleAdapt core 从 2023-04-04 起才有在线适配输出，公平比较同时列出 419 天重叠区间。",
        "",
        "## 交易结果",
        "",
        "| 方法 | 实现路径 | 天数 | 累计净收益 | 年化收益 | Sharpe | MDD | 平均换手 | 状态 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
        table_row("当前最佳 RD-Agent-Quant / DoubleAdapt-family", "本地 proxy：Ridge + 个股残差自适应", best_full, "2023-2024 全区间基线"),
        table_row("当前最佳 proxy 重叠区间", "同一 proxy，限制到 2023-04-04 至 2024-12-31", proxy_overlap, "用于和官方 core 公平比较"),
        table_row("Official DoubleAdapt core", "SJTU-DMTai Qlib incremental DoubleAdapt 核心训练循环", official_da, "已跑通，但单独表现弱"),
        table_row("RDA-DoubleAdapt core fusion", "0.75 proxy daily z-score + 0.25 official DoubleAdapt core daily z-score", fusion, "已跑通，raw 超过重叠 proxy"),
        "",
        f"- 2026 YTD 当前最佳 proxy raw 累计净收益：{fmt_pct(best_2026.get('cum_return') if best_2026 else None)}，年化：{fmt_pct(best_2026.get('ann_return') if best_2026 else None)}，Sharpe：{fmt_num(best_2026.get('sharpe') if best_2026 else None)}。",
        f"- Official DoubleAdapt core neutral：累计 {fmt_pct(official_da_neutral.get('cum_return') if official_da_neutral else None)}，年化 {fmt_pct(official_da_neutral.get('ann_return') if official_da_neutral else None)}，Sharpe {fmt_num(official_da_neutral.get('sharpe') if official_da_neutral else None)}。",
        f"- Fusion neutral：累计 {fmt_pct(fusion_neutral.get('cum_return') if fusion_neutral else None)}，年化 {fmt_pct(fusion_neutral.get('ann_return') if fusion_neutral else None)}，Sharpe {fmt_num(fusion_neutral.get('sharpe') if fusion_neutral else None)}。",
        "",
        "## 结论",
        "",
        "1. 官方 DoubleAdapt core 单独不适合直接作为当前 A 股 Top30 交易策略：raw 年化只有 1.20%，Sharpe 0.11，neutral 为负，且平均换手约 25%，明显弱于现有最佳 proxy。",
        "2. 融合版有增益，但增益主要发生在 2024 年，2023 年重叠段仍为负。419 天重叠区间 raw 从 proxy 的 37.23% 累计净收益提升到 50.45%，Sharpe 从 1.47 提升到 2.00，MDD 从 -13.68% 收窄到 -10.92%。",
        "3. neutral 融合提升很小：累计净收益从 31.08% 到 32.76%，Sharpe 从 1.28 到 1.39，说明新增信号仍含有行业/规模或市场状态暴露，不能直接认定为稳健 alpha。",
        "4. 现阶段不能声称“完整版融合加强版全面通过”。可以把 fusion 作为下一轮候选，但需要在 2026 YTD、滚动权重、不同 TopK/成本和行业规模中性约束下继续验证。",
        "",
        "## 环境审计",
        "",
        f"- Python: `{env_python}`",
        "- DoubleAdapt 专用环境: `.venv-doubleadapt`，Python 3.9，torch/higher/mlflow/qlib 依赖已补齐到可运行官方 core。",
        f"- DoubleAdapt fork: `{git_head(PROJECT_ROOT / 'external_repos' / 'SJTU-DMTai__qlib')}` at `external_repos/SJTU-DMTai__qlib`。",
        f"- RD-Agent repo: `{git_head(PROJECT_ROOT / 'external_repos' / 'microsoft__RD-Agent')}` at `external_repos/microsoft__RD-Agent`。",
        f"- 当前默认 Python 可见依赖: torch={has_module('torch')}, qlib={has_module('qlib')}, higher={has_module('higher')}, mlflow={has_module('mlflow')}。",
        "",
        "## 复现命令",
        "",
        "导出当前最佳 proxy 逐股 score：",
        "",
        "```powershell",
        "python scripts\\export_paper_proxy_scores.py --model rd_agent_quant --panel data\\processed\\cn_a_share\\csi300_2018_2024\\panel.csv --out experiments\\official_scores\\rd_agent_quant_proxy_h5_scores.csv --horizon 5 --lookback 20",
        "```",
        "",
        "运行官方 DoubleAdapt core：",
        "",
        "```powershell",
        ".venv-doubleadapt\\Scripts\\python.exe scripts\\run_official_doubleadapt_core.py --out experiments\\official_scores\\doubleadapt_official_core_h5.csv --max-train-tasks 12 --max-valid-tasks 4 --task-train-days 60 --task-test-days 20 --patience 2",
        "```",
        "",
        "生成融合 score 并回测：",
        "",
        "```powershell",
        "python scripts\\blend_score_files.py --left experiments\\official_scores\\rd_agent_quant_proxy_h5_scores.csv --right experiments\\official_scores\\doubleadapt_official_core_h5.csv --out experiments\\official_scores\\rda_doubleadapt_core_fusion_h5.csv --left-weight 0.75 --right-weight 0.25",
        "python scripts\\run_score_trade_validation.py --scores experiments\\official_scores\\rda_doubleadapt_core_fusion_h5.csv --panel data\\processed\\cn_a_share\\csi300_2018_2024\\panel.csv --stock-basic data\\raw\\tushare\\csi300_2018_2024\\stock_basic.csv --method rda_doubleadapt_core_fusion --horizon 5 --topk 30 --cost-bps 10 --test-start 2023-01-03 --test-end 2024-12-31",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    out = PROJECT_ROOT / "docs" / "reports" / "full_method_fusion_comparison.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_report(), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
