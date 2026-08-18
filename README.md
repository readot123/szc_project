# 共享单车数据分析

一个小而完整的数据分析项目：从 Hugging Face 下载共享单车小时数据，完成数据校验、清洗、指标汇总和可视化。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py
python src/analyze.py
pytest
```

运行结果写入 `outputs/`：

- `summary.json`：核心指标（总骑行量、小时均值、高峰时段等）
- `hourly_demand.csv`：分时需求
- `weekday_demand.csv`：分星期需求
- `hourly_demand.png`：24 小时需求曲线
- `weather_demand.png`：不同天气下的平均需求

## 数据来源

- Hugging Face 数据集：[`supersam7/bike_sharing`](https://huggingface.co/datasets/supersam7/bike_sharing)
- 文件：`bike_sharing.csv`（17,379 条小时级记录）
- 许可：MIT

原始数据不会提交进 Git；下载脚本会计算 SHA-256 并把来源元数据写入 `data/raw/dataset_metadata.json`，便于复现与审计。

## 版本策略

- `v0.1.0`：仓库初始化
- `v0.2.0`：可复现数据下载与校验
- `v1.0.0`：完整分析、可视化、测试与 CI

功能通过 `feature/data-pipeline` 和 `feature/analysis` 分支开发，并使用非快进合并保留分支历史。
