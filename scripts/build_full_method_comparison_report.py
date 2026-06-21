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


def fmt_pct(value: str) -> str:
    try:
        return f"{float(value) * 100:.2f}%"
    except (TypeError, ValueError):
        return "n/a"


def fmt_num(value: str) -> str:
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "n/a"


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def git_head(path: Path) -> str:
    if not (path / ".git").exists():
        return "not_cloned"
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "incomplete_clone"


def proxy_rows() -> tuple[dict[str, str] | None, dict[str, str] | None]:
    rows_2024 = read_csv(PROJECT_ROOT / "experiments" / "trade_validation" / "trade_validation_summary.csv")
    rows_2026 = read_csv(PROJECT_ROOT / "experiments" / "trade_validation_2026_ytd" / "trade_validation_summary.csv")
    best_2024 = next((row for row in rows_2024 if row["model"] == "rd_agent_quant" and row["variant"] == "raw"), None)
    best_2026 = next((row for row in rows_2026 if row["model"] == "rd_agent_quant" and row["variant"] == "raw"), None)
    return best_2024, best_2026


def build_report() -> str:
    best_2024, best_2026 = proxy_rows()
    doubleadapt_repo = PROJECT_ROOT / "external_repos" / "SJTU-DMTai__qlib"
    rdagent_repo = PROJECT_ROOT / "external_repos" / "microsoft__RD-Agent"
    env = {
        "python": subprocess.run(["python", "--version"], capture_output=True, text=True, check=False).stdout.strip(),
        "torch": has_module("torch"),
        "qlib": has_module("qlib"),
        "higher": has_module("higher"),
        "mlflow": has_module("mlflow"),
        "jinja2": has_module("jinja2"),
    }

    lines: list[str] = []
    lines.append("# 完整版方法与融合加强版对比状态")
    lines.append("")
    lines.append("本报告把当前最佳可运行 proxy、两篇参考论文的完整版方法，以及拟定的完整版融合加强方法，放到同一个交易协议下比较：CSI300、H5 score、Top30 等权多头、日频调仓、单边 10 bps 换手成本。")
    lines.append("")
    lines.append("## 当前可执行结果")
    lines.append("")
    lines.append("| 方法 | 实现口径 | 2023-2024 累计净收益 | 2023-2024 年化收益 | Sharpe | MDD | 2026 YTD 累计净收益 | 状态 |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---|")
    if best_2024 and best_2026:
        lines.append(
            "| RD-Agent-Quant / DoubleAdapt-family H5 Top30 | 本地 proxy：Ridge + 个股残差自适应 | "
            f"{fmt_pct(best_2024['cum_return'])} | {fmt_pct(best_2024['ann_return'])} | {fmt_num(best_2024['sharpe'])} | "
            f"{fmt_pct(best_2024['mdd'])} | {fmt_pct(best_2026['cum_return'])} | 已完成 |"
        )
    else:
        lines.append("| RD-Agent-Quant / DoubleAdapt-family H5 Top30 | 本地 proxy | n/a | n/a | n/a | n/a | n/a | 缺少 summary |")
    lines.append("| Official DoubleAdapt | SJTU-DMTai qlib incremental 官方实现 | pending | pending | pending | pending | pending | 运行环境阻塞 |")
    lines.append("| Official RD-Agent-Quant | Microsoft RD-Agent(Q) 因子-模型协同优化 | pending | pending | pending | pending | pending | 仓库/环境/LLM 编排阻塞 |")
    lines.append("| RDA-DoubleAdapt full fusion | RD-Agent(Q) 因子/模型 + DoubleAdapt 官方在线适配 | pending | pending | pending | pending | pending | 等待两个完整版上游输出 |")
    lines.append("")

    lines.append("## 运行环境审计")
    lines.append("")
    lines.append(f"- Python: `{env['python'] or 'unknown'}`")
    lines.append(f"- DoubleAdapt 仓库：`{git_head(doubleadapt_repo)}`，路径 `external_repos/SJTU-DMTai__qlib`")
    lines.append(f"- RD-Agent 仓库：`{git_head(rdagent_repo)}`，路径 `external_repos/microsoft__RD-Agent`")
    for package in ["torch", "qlib", "higher", "mlflow", "jinja2"]:
        lines.append(f"- `{package}` 可用：`{env[package]}`")
    lines.append("")
    lines.append("官方 DoubleAdapt 需要 fork 版 Qlib 运行时，并要求 `torch==1.9.0` 和 `higher==0.2.1`。当前机器只暴露 Python 3.14，且 PyTorch/Qlib 运行栈未安装。因此现在不能诚实地报告官方 DoubleAdapt 完整版结果。")
    lines.append("")
    lines.append("官方 RD-Agent-Quant 需要 Microsoft RD-Agent 应用栈、Qlib quant 场景配置、LLM API 凭据，以及因子/模型迭代运行。本地 RD-Agent 克隆当前不完整，因此还没有官方 RD-Agent(Q) score 输出。")
    lines.append("")

    lines.append("## 标准 Score 接口")
    lines.append("")
    lines.append("每个完整版方法进入统一交易对比前，必须先导出一个 CSV：")
    lines.append("")
    lines.append("```text")
    lines.append("date,symbol,score")
    lines.append("2023-01-03,SH600000,-0.00123")
    lines.append("```")
    lines.append("")
    lines.append("可以额外提供 `label`，但推荐让 `scripts/run_score_trade_validation.py` 从本地 panel 统一拼接 H5 标签，确保每个方法使用相同标签和成本协议。")
    lines.append("")

    lines.append("## 复现实验命令")
    lines.append("")
    lines.append("回测官方 DoubleAdapt score 文件：")
    lines.append("")
    lines.append("```powershell")
    lines.append("python scripts\\run_score_trade_validation.py `")
    lines.append("  --scores experiments\\official_scores\\doubleadapt_official_h5.csv `")
    lines.append("  --panel data\\processed\\cn_a_share\\csi300_2018_2024\\panel.csv `")
    lines.append("  --stock-basic data\\raw\\tushare\\csi300_2018_2024\\stock_basic.csv `")
    lines.append("  --method doubleadapt_official `")
    lines.append("  --horizon 5 --topk 30 --cost-bps 10")
    lines.append("```")
    lines.append("")
    lines.append("回测 RD-Agent(Q) score 文件：")
    lines.append("")
    lines.append("```powershell")
    lines.append("python scripts\\run_score_trade_validation.py `")
    lines.append("  --scores experiments\\official_scores\\rd_agent_quant_official_h5.csv `")
    lines.append("  --panel data\\processed\\cn_a_share\\csi300_2018_2024\\panel.csv `")
    lines.append("  --stock-basic data\\raw\\tushare\\csi300_2018_2024\\stock_basic.csv `")
    lines.append("  --method rd_agent_quant_official `")
    lines.append("  --horizon 5 --topk 30 --cost-bps 10")
    lines.append("```")
    lines.append("")
    lines.append("回测完整版融合 score 文件：")
    lines.append("")
    lines.append("```powershell")
    lines.append("python scripts\\run_score_trade_validation.py `")
    lines.append("  --scores experiments\\official_scores\\rda_doubleadapt_full_h5.csv `")
    lines.append("  --panel data\\processed\\cn_a_share\\csi300_2018_2024\\panel.csv `")
    lines.append("  --stock-basic data\\raw\\tushare\\csi300_2018_2024\\stock_basic.csv `")
    lines.append("  --method rda_doubleadapt_full `")
    lines.append("  --horizon 5 --topk 30 --cost-bps 10")
    lines.append("```")
    lines.append("")

    lines.append("## 完整版融合定义")
    lines.append("")
    lines.append("融合加强版不应是几个 proxy 输出的简单平均。真正的完整版定义是：")
    lines.append("")
    lines.append("1. 在相同 CSI300 train/valid 切分上运行 RD-Agent(Q) 因子-模型协同优化。")
    lines.append("2. 导出 RD-Agent(Q) 的日频 H5 股票 score。")
    lines.append("3. 把这些 score 或 RD-Agent 选出的模型 embedding 接入 DoubleAdapt 官方 online adapter。")
    lines.append("4. 导出适配后的 H5 score：`rda_doubleadapt_full_h5.csv`。")
    lines.append("5. 用同一成本模型验证 raw 和行业/规模中性化 Top30 组合。")
    lines.append("")

    lines.append("## 判定规则")
    lines.append("")
    lines.append("在至少一个官方方法产出可比 score 文件之前，当前 proxy 仍是研究基线。融合方法只有在 raw 和 neutral 两个版本上都能扣 10 bps 后超过当前 proxy，且没有显著抬高回撤或换手时，才算真正通过。")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    out = PROJECT_ROOT / "docs" / "reports" / "full_method_fusion_comparison.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_report(), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
