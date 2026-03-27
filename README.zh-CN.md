<div align="center">
<img src="assets/bioclaw_logo.jpg" width="300">

# Bioclaw_Skills_Hub
### [Bioclaw](https://github.com/Runchuan-BU/BioClaw) 生物信息学与组学工作流精选技能库

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Bioclaw_Skills_Hub** 是一个面向生物信息学、组学分析与计算生物学的开源可复用技能集合。

本项目围绕真实分析任务进行组织，而非孤立的工具罗列，便于 AI 智能体、工作流系统和科研助手进行浏览、复用与二次开发。

</div>

## 目录

- [概述](#概述)
- [库中内容](#库中内容)
- [仓库结构](#仓库结构)
- [主要领域](#主要领域)
- [项目价值](#项目价值)
- [项目状态](#项目状态)
- [使用方式](#使用方式)
- [设计原则](#设计原则)
- [许可证](#许可证)

## 概述

生物信息学工作流往往分散在大量零散的提示词集合、工具专项笔记和一次性智能体指令中。

**Bioclaw_Skills_Hub** 将这些模式整合到一个结构更为一致的仓库中。项目目标是提供一个更易于维护、路由和复用的技能库，覆盖多种组学场景，包括转录组学、单细胞分析、表观基因组学、宏基因组学、蛋白质组学、结构生物学及通用生物信息学。

## 库中内容

- 面向常见组学工作流的任务导向型技能
- 按主要分析领域对技能进行分类的分类体系
- 针对高价值工作流（如 ChIP-seq、ATAC-seq、差异表达分析、宏基因组学、蛋白质组学、结构生物学、单细胞分析）的深度参考资料
- 为 BioClaw 等智能体系统构建轻量运行时技能包的基础框架

## 仓库结构

```text
Bioclaw_Skills_Hub/
├── skills/
│   ├── transcriptomics/                # 转录组学
│   ├── single-cell-and-spatial/        # 单细胞与空间组学
│   ├── epigenomics-and-regulation/     # 表观基因组学与基因调控
│   ├── genomics-and-variation/         # 基因组学与变异分析
│   ├── metagenomics-and-microbiome/    # 宏基因组学与微生物组
│   ├── proteomics-and-metabolomics/    # 蛋白质组学与代谢组学
│   ├── multi-omics-and-systems/        # 多组学与系统生物学
│   ├── core-bioinformatics/            # 核心生物信息学
│   └── .../
├── catalog/
├── scripts/
└── .github/workflows/
```

## 主要领域

- 转录组学
- 单细胞与空间组学
- 表观基因组学与基因调控
- 基因组学与变异分析
- 宏基因组学与微生物组
- 蛋白质组学与代谢组学
- 多组学与系统生物学
- 核心生物信息学

## 项目价值

- 通过整合到清晰的组学分类体系中，减少多个小型技能集合之间的重复冗余。
- 在保持顶层类别简洁的同时，允许细粒度的专项叶子技能存在。
- 既可作为独立的公开技能库单独使用，也可作为下游智能体技能包的来源仓库。

## 项目状态

本仓库将持续迭代与扩展。

如果本项目对你有所帮助，欢迎给项目点个 Star ⭐。

## 致谢

本仓库的灵感来源于以下早期技能集合：[claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)、[OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills)、[claude-for-life-sciences-skills](https://www.anthropic.com/news/claude-for-life-sciences) 以及 [bioSkills](https://github.com/GPTomics/bioSkills)。

本项目在上述工作的基础上进行了重组与精炼，形成一个更统一、更面向组学领域的技能库结构。

## 使用方式

- 浏览 `skills/` 目录，以工作流为导向寻找入口。
- 使用 `catalog/` 目录，获取精简的分类体系与来源映射。
- 直接复用单个叶子技能，或为生产级智能体环境筛选出更小的子集。

## 设计原则

- 按用户面向的分析目标对技能分组，而非单纯按工具包名称归类。
- 保持叶子技能的可操作性，便于路由。
- 将宏观工作流指导与深度技术参考分离。
- 便于从较大的公开库中派生出更小、高信噪比的运行时技能包。

## 许可证

本项目基于 [MIT 许可证](LICENSE) 发布。
