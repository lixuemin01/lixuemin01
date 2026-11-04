#!/usr/bin/env python3
"""Generate paper-style figures for the 藏经阁 document."""
from pathlib import Path
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon, Arc
from matplotlib.lines import Line2D
import numpy as np

OUT = Path("/workspace/docs/zangjingge/assets")
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": ["WenQuanYi Micro Hei", "Droid Sans Fallback", "DejaVu Sans"],
    "font.size": 11,
    "axes.unicode_minus": False,
    "figure.facecolor": "#F7F4EE",
    "savefig.facecolor": "#F7F4EE",
    "savefig.dpi": 180,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.28,
})

NAVY = "#1B365D"
TEAL = "#2A9D8F"
AMBER = "#C9A227"
CORAL = "#C45C26"
SLATE = "#4A5568"
INK = "#1A1A1A"
PAPER = "#F7F4EE"
WHITE = "#FFFdf8"
CARD = "#FFFFFF"
SOFT = "#E8E2D6"
BLUE = "#3D6B99"
GREEN = "#3D7A5A"
PURPLE = "#6B4C8A"


def rounded(ax, x, y, w, h, fc, ec=NAVY, lw=1.2, r=0.08, z=2, alpha=1.0):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.012,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, alpha=alpha,
    )
    ax.add_patch(p)
    return p


def text(ax, x, y, s, **kw):
    defaults = dict(ha="center", va="center", color=INK, zorder=5)
    defaults.update(kw)
    ax.text(x, y, s, **defaults)


def arrow(ax, x1, y1, x2, y2, color=NAVY, lw=1.6, style="-|>", rad=0):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=12, lw=lw,
        color=color, connectionstyle=f"arc3,rad={rad}", zorder=4,
    ))


def setup(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def caption(fig, s):
    fig.text(0.5, 0.01, s, ha="center", va="bottom", fontsize=9, color=SLATE, style="italic")


# ---------- Fig 01 three-layer contract ----------
def fig01():
    fig, ax = plt.subplots(figsize=(12.4, 8.0))
    setup(ax, (0, 12.4), (0, 8.0))
    text(ax, 6.2, 7.68, "企业级大模型系统的三层契约栈", fontsize=16, color=NAVY, weight="bold")
    text(ax, 6.2, 7.28, "契约先于智能：每一层只对外暴露可验证的承诺，而不是模型本身", fontsize=10, color=SLATE)

    layers = [
        (5.15, "#1B365D", WHITE, "L1  应用契约层  Application Contract",
         "Spring Boot / Spring AI / 领域服务\n接口签名 · SLO · 鉴权 · 幂等 · 审计\n确定性 RPC 与概率性推理的边界闸门"),
        (3.20, "#2A9D8F", WHITE, "L2  编排契约层  Orchestration Contract",
         "RAG 知识总线 · Tool 注册表 · Agent 工作流\n检索召回率 · 工具超时 · 回滚语义\n把非确定性推理约束进可编排的步骤"),
        (1.25, "#C45C26", WHITE, "L3  推理契约层  Inference Contract",
         "vLLM / SGLang · Prefill/Decode · 并行与通信\nTTFT · TPS · KV Cache 上限 · 失败降级\n把 GPU 物理事实翻译成应用可消费的 SLA"),
    ]
    for y, color, tc, title, body in layers:
        rounded(ax, 0.45, y, 7.55, 1.78, WHITE, color, 2.0, 0.1)
        rounded(ax, 0.45, y, 0.18, 1.78, color, color, 0, 0.02)
        text(ax, 4.3, y + 1.32, title, fontsize=13, color=color, weight="bold")
        text(ax, 4.3, y + 0.62, body, fontsize=10, color=INK, linespacing=1.45)

    # right side: crossing arrows / contracts
    rounded(ax, 8.25, 1.25, 3.75, 5.68, WHITE, NAVY, 1.4, 0.1)
    text(ax, 10.12, 6.55, "跨层不变量", fontsize=12, color=NAVY, weight="bold")
    items = [
        ("I1", "请求必须可追踪", "trace_id 贯穿三层"),
        ("I2", "输出必须可校验", "schema / 引用 / 工具结果"),
        ("I3", "失败必须可降级", "规则引擎 / 缓存 / 人工"),
        ("I4", "成本必须可计量", "token · GPU 秒 · 检索次数"),
        ("I5", "数据必须可隔离", "租户 · 密级 · 不出域"),
    ]
    for i, (k, t, d) in enumerate(items):
        yy = 5.65 - i * 0.88
        rounded(ax, 8.5, yy - 0.32, 3.25, 0.76, SOFT, NAVY, 0.8, 0.08)
        text(ax, 8.95, yy + 0.08, k, fontsize=10, color=CORAL, weight="bold", ha="left")
        text(ax, 10.35, yy + 0.18, t, fontsize=10, color=INK, weight="bold")
        text(ax, 10.35, yy - 0.12, d, fontsize=9, color=SLATE)

    caption(fig, "图 1  三层契约栈：应用层承诺接口语义，编排层承诺步骤可控，推理层承诺物理 SLA")
    fig.savefig(OUT / "fig01-three-layer-contract.png")
    plt.close()


# ---------- Fig 02 dual track ----------
def fig02():
    fig, ax = plt.subplots(figsize=(12.4, 6.8))
    setup(ax, (0, 12.4), (0, 6.8))
    text(ax, 6.2, 6.5, "同一业务请求的双轨执行：确定性主路径 + 概率性辅路径", fontsize=15, color=NAVY, weight="bold")

    # client
    rounded(ax, 0.3, 2.9, 1.7, 1.1, NAVY, NAVY, 0, 0.1)
    text(ax, 1.15, 3.45, "客户端\n工单 / 告警", color=WHITE, fontsize=11, weight="bold")

    # gateway
    rounded(ax, 2.4, 2.9, 1.9, 1.1, TEAL, TEAL, 0, 0.1)
    text(ax, 3.35, 3.45, "契约网关\n路由 / 脱敏", color=WHITE, fontsize=11, weight="bold")
    arrow(ax, 2.0, 3.45, 2.4, 3.45)

    # two tracks
    rounded(ax, 4.8, 4.55, 3.6, 1.7, WHITE, GREEN, 1.8, 0.1)
    text(ax, 6.6, 5.85, "确定性轨道  Deterministic", fontsize=11, color=GREEN, weight="bold")
    text(ax, 6.6, 5.25, "告警收敛 · CMDB 查询 · 工单状态机\nSQL / REST / 规则引擎 · 可回放", fontsize=9.5)
    text(ax, 6.6, 4.78, "承诺：相同输入 → 相同输出", fontsize=9, color=GREEN)

    rounded(ax, 4.8, 0.65, 3.6, 1.7, WHITE, CORAL, 1.8, 0.1)
    text(ax, 6.6, 1.95, "概率性轨道  Probabilistic", fontsize=11, color=CORAL, weight="bold")
    text(ax, 6.6, 1.35, "根因假设 · 处置建议 · 报告草稿\nRAG / Agent / LLM · 需校验", fontsize=9.5)
    text(ax, 6.6, 0.88, "承诺：输出可被证据约束", fontsize=9, color=CORAL)

    arrow(ax, 4.3, 3.7, 4.8, 5.2)
    arrow(ax, 4.3, 3.2, 4.8, 1.7)

    # merge
    rounded(ax, 8.9, 2.7, 3.15, 1.5, WHITE, NAVY, 1.8, 0.1)
    text(ax, 10.47, 3.75, "校验与合流", fontsize=12, color=NAVY, weight="bold")
    text(ax, 10.47, 3.2, "Schema 校验 · 引用核对\n规则否决 · 人工确认闸门", fontsize=9.5)
    arrow(ax, 8.4, 5.4, 9.3, 4.05)
    arrow(ax, 8.4, 1.5, 9.3, 2.85)

    rounded(ax, 8.9, 0.55, 3.15, 0.85, NAVY, NAVY, 0, 0.1)
    text(ax, 10.47, 0.97, "对外只发布已校验结果", color=WHITE, fontsize=11, weight="bold")
    arrow(ax, 10.47, 2.7, 10.47, 1.4)

    caption(fig, "图 2  双轨合流：LLM 永远不直接改生产状态；确定性系统负责落地，概率系统只提供假设与草案")
    fig.savefig(OUT / "fig02-dual-track.png")
    plt.close()


# ---------- Fig 03 RAG as data system ----------
def fig03():
    fig, ax = plt.subplots(figsize=(12.6, 7.0))
    setup(ax, (0, 12.6), (0, 7.0))
    text(ax, 6.3, 6.68, "把 RAG 当成数据系统，而不是 Prompt 技巧", fontsize=15, color=NAVY, weight="bold")

    # offline
    rounded(ax, 0.25, 3.55, 12.1, 2.85, WHITE, NAVY, 1.2, 0.08)
    text(ax, 1.35, 6.05, "离线知识总线", fontsize=11, color=NAVY, weight="bold", ha="left")
    boxes = [
        (0.5, 3.85, "源系统\n工单/手册\n拓扑/日志"),
        (2.55, 3.85, "解析与\n结构化\nPDF/HTML"),
        (4.6, 3.85, "语义切分\n+ 元数据\n租户/密级"),
        (6.65, 3.85, "多路嵌入\n稠密+稀疏"),
        (8.7, 3.85, "索引写入\n向量/BM25\n图谱"),
        (10.55, 3.85, "质量门禁\n召回评测\n漂移告警"),
    ]
    for i, (x, y, t) in enumerate(boxes):
        rounded(ax, x, y, 1.85, 1.85, SOFT if i < 5 else "#F4E6D8", NAVY, 1.1, 0.08)
        text(ax, x + 0.92, y + 0.92, t, fontsize=9.5, linespacing=1.35)
        if i < 5:
            arrow(ax, x + 1.85, y + 0.92, boxes[i + 1][0], y + 0.92)

    # online
    rounded(ax, 0.25, 0.45, 12.1, 2.85, WHITE, TEAL, 1.2, 0.08)
    text(ax, 1.35, 2.95, "在线问答总线", fontsize=11, color=TEAL, weight="bold", ha="left")
    boxes2 = [
        (0.5, 0.75, "意图改写\n多查询\nHyDE"),
        (2.55, 0.75, "混合检索\n向量+关键词\n图谱邻域"),
        (4.6, 0.75, "重排序\nCross-Encoder\n时效加权"),
        (6.65, 0.75, "证据打包\n引用编号\n冲突检测"),
        (8.7, 0.75, "受约束生成\n必须引用\n禁无中生有"),
        (10.55, 0.75, "答案校验\n引用存在?\n工具结果?"),
    ]
    for i, (x, y, t) in enumerate(boxes2):
        rounded(ax, x, y, 1.85, 1.85, "#E4F0EC" if i < 5 else "#F4E6D8", TEAL, 1.1, 0.08)
        text(ax, x + 0.92, y + 0.92, t, fontsize=9.5, linespacing=1.35)
        if i < 5:
            arrow(ax, x + 1.85, y + 0.92, boxes2[i + 1][0], y + 0.92, color=TEAL)

    caption(fig, "图 3  RAG 全链路：离线管质量，在线管约束。生成只是最后 10% 的工作")
    fig.savefig(OUT / "fig03-rag-data-system.png")
    plt.close()


# ---------- Fig 04 agent as saga ----------
def fig04():
    fig, ax = plt.subplots(figsize=(12.4, 6.6))
    setup(ax, (0, 12.4), (0, 6.6))
    text(ax, 6.2, 6.28, "把 Agent 循环看成带补偿的分布式事务（Saga）", fontsize=15, color=NAVY, weight="bold")

    steps = [
        (0.35, "感知", "告警归一\n上下文装载", TEAL),
        (2.7, "规划", "拆子任务\n选工具图", BLUE),
        (5.05, "行动", "调用工具\n写副作用", CORAL),
        (7.4, "观察", "解析结果\n更新信念", AMBER),
        (9.75, "提交/补偿", "校验闸门\n回滚或升级", NAVY),
    ]
    for x, title, body, c in steps:
        rounded(ax, x, 3.55, 2.15, 2.15, WHITE, c, 2.0, 0.1)
        text(ax, x + 1.07, 5.25, title, fontsize=13, color=c, weight="bold")
        text(ax, x + 1.07, 4.45, body, fontsize=10, linespacing=1.4)
        rounded(ax, x + 0.25, 3.72, 1.65, 0.38, c, c, 0, 0.06)
        text(ax, x + 1.07, 3.91, "可重试 / 可审计", color=WHITE, fontsize=8.5)
    for i in range(4):
        arrow(ax, steps[i][0] + 2.15, 4.62, steps[i + 1][0], 4.62)

    # loop back
    arrow(ax, 10.82, 3.55, 10.82, 2.55, color=SLATE)
    arrow(ax, 10.82, 2.55, 1.42, 2.55, color=SLATE, style="-")
    arrow(ax, 1.42, 2.55, 1.42, 3.55, color=SLATE)
    text(ax, 6.2, 2.78, "未达停止条件：带着新观察重新规划（有预算上限）", fontsize=9.5, color=SLATE)

    rounded(ax, 0.35, 0.35, 11.7, 1.7, WHITE, NAVY, 1.2, 0.08)
    text(ax, 6.2, 1.68, "副作用隔离原则", fontsize=12, color=NAVY, weight="bold")
    text(ax, 6.2, 0.95,
         "读工具可自动重试；写工具必须幂等键 + 补偿动作。LLM 只提出“调用意图”，真正的变更由确定性适配器执行。\n"
         "超时、幻觉参数、越权工具一律视为事务失败，进入补偿或人工升级，而不是继续让模型“再试一次”。",
         fontsize=9.5, linespacing=1.45)

    caption(fig, "图 4  Agent ≠ 聊天循环。它是一个有预算、有补偿、有闸门的长事务")
    fig.savefig(OUT / "fig04-agent-saga.png")
    plt.close()


# ---------- Fig 05 prefill decode ----------
def fig05():
    fig, ax = plt.subplots(figsize=(12.6, 7.1))
    setup(ax, (0, 12.6), (0, 7.1))
    text(ax, 6.3, 6.78, "推理的两种物理状态：Prefill 算力受限，Decode 访存受限", fontsize=15, color=NAVY, weight="bold")

    # left prefill
    rounded(ax, 0.3, 0.55, 5.9, 5.9, WHITE, TEAL, 1.6, 0.1)
    text(ax, 3.25, 6.05, "Prefill  ·  写入 KV Cache", fontsize=13, color=TEAL, weight="bold")
    text(ax, 3.25, 5.55, "一次吃完整 Prompt · GEMM 矩阵乘 · Compute-bound", fontsize=9.5, color=SLATE)

    # matrix of tokens
    tokens = ["告警", "BGP", "抖动", "AS65001", "接口"]
    for i, tok in enumerate(tokens):
        for j in range(i + 1):
            c = TEAL if j == i else SOFT
            tc = WHITE if j == i else INK
            rounded(ax, 0.7 + j * 1.0, 4.55 - i * 0.72, 0.9, 0.58, c, TEAL, 0.8, 0.06)
            text(ax, 1.15 + j * 1.0, 4.84 - i * 0.72, tokens[j], fontsize=8, color=tc)
    text(ax, 3.25, 1.35, "复杂度约 O(S²) Attention + O(S) FFN\nKV 写入量 ∝ 层数 × 序列长 × 头维", fontsize=9.5)
    text(ax, 3.25, 0.82, "优化点：切分、并行 GEMM、CUDA Graph", fontsize=9, color=TEAL)

    # right decode
    rounded(ax, 6.4, 0.55, 5.9, 5.9, WHITE, CORAL, 1.6, 0.1)
    text(ax, 9.35, 6.05, "Decode  ·  读取 KV Cache", fontsize=13, color=CORAL, weight="bold")
    text(ax, 9.35, 5.55, "每步只产 1 个 token · GEMV 向量乘 · Memory-bound", fontsize=9.5, color=SLATE)

    hist = ["告警", "BGP", "抖动", "AS65001", "接口", "邻居"]
    for i, tok in enumerate(hist):
        rounded(ax, 6.75 + (i % 3) * 1.7, 4.55 - (i // 3) * 0.85, 1.5, 0.68,
                SOFT if i < 5 else CORAL, CORAL, 0.9, 0.06)
        text(ax, 7.5 + (i % 3) * 1.7, 4.89 - (i // 3) * 0.85, tok,
             fontsize=9, color=WHITE if i == 5 else INK)
    text(ax, 9.35, 2.55, "每步必须把全部权重从 HBM 搬一遍\n再读完整历史 KV，只追加 1 行", fontsize=9.5)
    text(ax, 9.35, 1.55, "瓶颈是带宽不是算力：H100 HBM ≈ 3.35 TB/s\n单步有效算力利用率常常 < 10%", fontsize=9.5)
    text(ax, 9.35, 0.82, "优化点：连续批处理、投机解码、量化、PD 分离", fontsize=9, color=CORAL)

    caption(fig, "图 5  Prefill 与 Decode 是两种完全不同的系统问题，混在一张卡上调度会互相伤害")
    fig.savefig(OUT / "fig05-prefill-decode.png")
    plt.close()


# ---------- Fig 06 parallelism ----------
def fig06():
    fig, ax = plt.subplots(figsize=(12.6, 7.0))
    setup(ax, (0, 12.6), (0, 7.0))
    text(ax, 6.3, 6.7, "三种并行：它们解决的不是同一个瓶颈", fontsize=15, color=NAVY, weight="bold")

    panels = [
        (0.25, "张量并行 TP", TEAL,
         "切权重，不切请求",
         "每层 2 次 AllReduce\n要求 NVLink 级互联\n唯一能降低单请求延迟",
         "节点内 · 延迟敏感"),
        (4.35, "流水线并行 PP", AMBER,
         "切层，请求分段走",
         "Stage 间 P2P 传激活\n跨节点友好，但有气泡\n降延迟能力弱，提吞吐",
         "跨节点 · 吞吐型"),
        (8.45, "专家并行 EP", CORAL,
         "切专家，token 路由",
         "All-to-All 不规则小包\n负载不均衡是主敌\nMoE 模型的必选项",
         "机内+机间 · 拓扑敏感"),
    ]
    for x, title, c, slogan, body, tag in panels:
        rounded(ax, x, 0.55, 3.9, 5.8, WHITE, c, 1.8, 0.1)
        rounded(ax, x, 5.55, 3.9, 0.8, c, c, 0, 0.06)
        text(ax, x + 1.95, 5.95, title, color=WHITE, fontsize=14, weight="bold")
        text(ax, x + 1.95, 5.15, slogan, fontsize=11, color=c, weight="bold")

        # mini diagram
        if title.startswith("张量"):
            for i in range(4):
                rounded(ax, x + 0.35 + i * 0.85, 3.55, 0.75, 1.15, SOFT, c, 1.0, 0.06)
                text(ax, x + 0.72 + i * 0.85, 4.12, f"G{i}", fontsize=10, color=c, weight="bold")
            text(ax, x + 1.95, 3.25, "X 广播 → 各算一块 → 规约", fontsize=9, color=SLATE)
        elif title.startswith("流水"):
            for i, lab in enumerate(["L1-8", "L9-16", "L17-24", "L25-32"]):
                rounded(ax, x + 0.55, 4.35 - i * 0.55, 2.8, 0.45, SOFT, c, 0.9, 0.05)
                text(ax, x + 1.95, 4.57 - i * 0.55, f"Stage{i}  {lab}", fontsize=9)
            text(ax, x + 1.95, 2.35, "气泡沿下游传播", fontsize=9, color=SLATE)
        else:
            for i, lab in enumerate(["专家A", "专家B", "专家C", "专家D"]):
                rounded(ax, x + 0.4 + (i % 2) * 1.6, 3.7 - (i // 2) * 0.85, 1.45, 0.7, SOFT, c, 0.9, 0.06)
                text(ax, x + 1.12 + (i % 2) * 1.6, 4.05 - (i // 2) * 0.85, lab, fontsize=10)
            text(ax, x + 1.95, 2.35, "token 按路由 All-to-All", fontsize=9, color=SLATE)

        text(ax, x + 1.95, 1.55, body, fontsize=10, linespacing=1.45)
        rounded(ax, x + 0.45, 0.72, 3.0, 0.4, c, c, 0, 0.05)
        text(ax, x + 1.95, 0.92, tag, color=WHITE, fontsize=9.5)

    caption(fig, "图 6  TP 换延迟，PP 换规模，EP 换稀疏算力。跨节点做 TP 几乎总是错的")
    fig.savefig(OUT / "fig06-parallelism.png")
    plt.close()


# ---------- Fig 07 comm stack ----------
def fig07():
    fig, ax = plt.subplots(figsize=(12.4, 7.0))
    setup(ax, (0, 12.4), (0, 7.0))
    text(ax, 6.2, 6.7, "一次 AllReduce 穿过的软件-硬件栈", fontsize=15, color=NAVY, weight="bold")

    layers = [
        (5.35, NAVY, "框架层  vLLM / SGLang / TensorRT-LLM", "决定何时通信：层边界、CUDA Graph、自定义 AR 开关"),
        (4.25, TEAL, "通信库  NCCL / RCCL / HCCL / MSCCL++", "决定用什么实现：算法 + 协议选择"),
        (3.15, BLUE, "算法层  Ring / Tree / NVLS / PAT / One-shot", "决定数据怎么走：步数、带宽、同步次数的取舍"),
        (2.05, AMBER, "协议层  LL / LL128 / Simple", "决定小包还是大包：Decode 几乎总在延迟区"),
        (0.95, CORAL, "互连层  NVLink / NVSwitch / IB RDMA / RoCE / PCIe", "决定物理上限：带宽可差 1～2 个数量级"),
    ]
    for y, c, title, desc in layers:
        rounded(ax, 0.4, y, 7.5, 0.95, WHITE, c, 1.6, 0.08)
        rounded(ax, 0.4, y, 0.16, 0.95, c, c, 0, 0.02)
        text(ax, 4.2, y + 0.62, title, fontsize=12, color=c, weight="bold")
        text(ax, 4.2, y + 0.28, desc, fontsize=9.5, color=SLATE)

    rounded(ax, 8.15, 0.95, 3.9, 5.35, WHITE, NAVY, 1.3, 0.1)
    text(ax, 10.1, 5.9, "α–β 成本模型", fontsize=12, color=NAVY, weight="bold")
    text(ax, 10.1, 5.35, "T = 步数·α + 数据量/带宽", fontsize=10.5, color=INK)
    text(ax, 10.1, 4.7, "D 很大 → 选 Ring（带宽）\nD 很小 → 选 Tree / One-shot", fontsize=10, linespacing=1.4)
    text(ax, 10.1, 3.85, "Prefill 包：数 MB\nDecode 包：16–512 KB", fontsize=10, linespacing=1.4)
    rounded(ax, 8.4, 2.35, 3.4, 1.05, SOFT, NAVY, 0.8, 0.08)
    text(ax, 10.1, 2.87, "Decode 几乎全在 α 区\n步数比带宽更致命", fontsize=10, color=CORAL, weight="bold")
    rounded(ax, 8.4, 1.15, 3.4, 1.0, "#F4E6D8", CORAL, 0.8, 0.08)
    text(ax, 10.1, 1.65, "PCIe 不做 TP\nIB 适合 PP / KV 搬运", fontsize=10)

    caption(fig, "图 7  上三层可替换，最底层是物理事实。调优顺序应当自上而下，而不是先改网卡")
    fig.savefig(OUT / "fig07-comm-stack.png")
    plt.close()


# ---------- Fig 08 speculative decoding ----------
def fig08():
    fig, ax = plt.subplots(figsize=(12.6, 6.8))
    setup(ax, (0, 12.6), (0, 6.8))
    text(ax, 6.3, 6.48, "投机解码：用一次昂贵前向，验证多个便宜草稿", fontsize=15, color=NAVY, weight="bold")

    # left conventional
    rounded(ax, 0.25, 0.5, 5.85, 5.6, WHITE, SLATE, 1.3, 0.1)
    text(ax, 3.17, 5.7, "常规自回归", fontsize=13, color=SLATE, weight="bold")
    ys = [4.85, 3.95, 3.05, 2.15]
    labs = ["搬权重 → 生成「邻居」", "搬权重 → 生成「振荡」", "搬权重 → 生成「导致」", "搬权重 → 生成「丢包」"]
    for y, lab in zip(ys, labs):
        rounded(ax, 0.55, y, 5.25, 0.72, SOFT, SLATE, 0.9, 0.06)
        text(ax, 3.17, y + 0.36, lab, fontsize=10)
        if y != ys[-1]:
            arrow(ax, 3.17, y, 3.17, y - 0.18, color=SLATE, lw=1.1)
    text(ax, 3.17, 1.35, "4 个 token = 4 次目标模型前向", fontsize=10, color=CORAL)
    text(ax, 3.17, 0.85, "每次都把整模从 HBM 搬一遍", fontsize=9.5, color=SLATE)

    # right spec
    rounded(ax, 6.5, 0.5, 5.85, 5.6, WHITE, TEAL, 1.6, 0.1)
    text(ax, 9.42, 5.7, "投机解码", fontsize=13, color=TEAL, weight="bold")
    rounded(ax, 6.8, 4.55, 5.25, 0.78, "#E4F0EC", TEAL, 0.9, 0.06)
    text(ax, 9.42, 4.94, "草稿模型串行猜：邻居 / 振荡 / 导致", fontsize=10)
    rounded(ax, 6.8, 3.15, 5.25, 1.15, TEAL, TEAL, 0, 0.08)
    text(ax, 9.42, 3.72, "目标模型一次前向并行验证", color=WHITE, fontsize=11, weight="bold")
    text(ax, 9.42, 3.35, "接受最长前缀 + 白嫖 1 个 bonus token", color=WHITE, fontsize=9.5)

    # accept chips
    acc = [("邻居", True), ("振荡", True), ("丢包", False), ("+导致", True)]
    for i, (lab, ok) in enumerate(acc):
        c = GREEN if ok else CORAL
        rounded(ax, 7.0 + i * 1.25, 2.15, 1.12, 0.7, c, c, 0, 0.06)
        text(ax, 7.56 + i * 1.25, 2.5, lab, color=WHITE, fontsize=9)
    text(ax, 9.42, 1.55, "拒绝点之后草稿全部作废，从残差分布重采", fontsize=9.5, color=SLATE)
    text(ax, 9.42, 0.95, "小 batch Decode 收益最大，大 batch 会被连续批处理吃掉", fontsize=9, color=SLATE)

    caption(fig, "图 8  投机解码不改变输出分布（拒绝采样保证无损），它改变的是 HBM 搬运次数")
    fig.savefig(OUT / "fig08-speculative.png")
    plt.close()


# ---------- Fig 09 NOC-Pilot architecture ----------
def fig09():
    fig, ax = plt.subplots(figsize=(13.0, 7.6))
    setup(ax, (0, 13.0), (0, 7.6))
    text(ax, 6.5, 7.28, "案例系统 NOC-Pilot：网络故障智能处置平台逻辑架构", fontsize=15, color=NAVY, weight="bold")

    # top channels
    chans = ["告警总线", "工单系统", "ChatOps", "值班大屏"]
    for i, c in enumerate(chans):
        rounded(ax, 0.4 + i * 3.15, 6.35, 2.95, 0.6, NAVY, NAVY, 0, 0.06)
        text(ax, 1.87 + i * 3.15, 6.65, c, color=WHITE, fontsize=11, weight="bold")

    rounded(ax, 0.4, 4.85, 12.2, 1.3, WHITE, TEAL, 1.4, 0.08)
    text(ax, 6.5, 5.85, "L1 应用契约  ·  Spring Boot 领域服务", fontsize=11, color=TEAL, weight="bold")
    for i, t in enumerate(["告警归一", "权限与租户", "处置闸门", "审计归档", "SLO 路由"]):
        rounded(ax, 0.65 + i * 2.38, 5.0, 2.2, 0.55, SOFT, TEAL, 0.9, 0.05)
        text(ax, 1.75 + i * 2.38, 5.27, t, fontsize=10)

    rounded(ax, 0.4, 2.85, 12.2, 1.75, WHITE, AMBER, 1.4, 0.08)
    text(ax, 6.5, 4.3, "L2 编排契约  ·  知识总线 + Agent 运行时", fontsize=11, color=AMBER, weight="bold")
    for i, t in enumerate(["拓扑 RAG", "手册 RAG", "根因 Agent", "变更 Agent", "报告 Agent"]):
        rounded(ax, 0.65 + i * 2.38, 3.05, 2.2, 0.9, "#FBF3DC", AMBER, 0.9, 0.05)
        text(ax, 1.75 + i * 2.38, 3.5, t, fontsize=10, weight="bold")

    rounded(ax, 0.4, 0.45, 12.2, 2.15, WHITE, CORAL, 1.4, 0.08)
    text(ax, 6.5, 2.25, "L3 推理契约  ·  混合推理平面", fontsize=11, color=CORAL, weight="bold")
    inf = [
        (0.65, "边侧小模型\n脱敏/分类/路由"),
        (3.03, "私有 32B\n故障推理"),
        (5.41, "私有 72B\n复杂规划"),
        (7.79, "公有云 LLM\n非敏感润色"),
        (10.17, "规则引擎\n永久降级路径"),
    ]
    for x, t in inf:
        rounded(ax, x, 0.65, 2.2, 1.25, "#F8E8DC", CORAL, 0.9, 0.05)
        text(ax, x + 1.1, 1.27, t, fontsize=10, linespacing=1.35)

    caption(fig, "图 9  NOC-Pilot 并不是“一个大模型包打天下”，而是三层契约叠在已有网管系统之上")
    fig.savefig(OUT / "fig09-nocpilot.png")
    plt.close()


# ---------- Fig 10 capability map ----------
def fig10():
    fig, ax = plt.subplots(figsize=(12.4, 7.0))
    setup(ax, (0, 12.4), (0, 7.0))
    text(ax, 6.2, 6.65, "Java 后端工程师的能力迁移：不是转行，是加一层物理直觉", fontsize=14.5, color=NAVY, weight="bold")

    cols = [
        (0.3, "你已经会的", NAVY, [
            "接口契约与版本治理",
            "超时 / 重试 / 熔断",
            "幂等与分布式事务",
            "可观测性与容量规划",
            "多租户与权限模型",
            "CI/CD 与灰度发布",
        ]),
        (4.3, "需要改写的", TEAL, [
            "同步 RPC → 流式长任务",
            "精确断言 → 统计评测",
            "Schema 校验 → 证据校验",
            "QPS 容量 → Token/GPU 容量",
            "缓存 key=请求 → 语义缓存",
            "单元测试 → 回归集+人工抽检",
        ]),
        (8.3, "需要新学的", CORAL, [
            "Prefill / Decode 两种瓶颈",
            "KV Cache 与上下文预算",
            "TP / PP / EP 选型边界",
            "RAG 作为数据质量工程",
            "Agent 的副作用隔离",
            "混合路由与成本函数",
        ]),
    ]
    for x, title, c, items in cols:
        rounded(ax, x, 0.5, 3.8, 5.8, WHITE, c, 1.6, 0.1)
        rounded(ax, x, 5.5, 3.8, 0.8, c, c, 0, 0.06)
        text(ax, x + 1.9, 5.9, title, color=WHITE, fontsize=14, weight="bold")
        for i, it in enumerate(items):
            yy = 4.85 - i * 0.75
            rounded(ax, x + 0.25, yy - 0.22, 3.3, 0.58, SOFT, c, 0.8, 0.06)
            text(ax, x + 1.9, yy + 0.07, it, fontsize=10.5)

    caption(fig, "图 10  转型的最小充分集：工程肌肉保留，评测语言改写，补上推理层物理常识")
    fig.savefig(OUT / "fig10-capability-map.png")
    plt.close()


# ---------- Fig 11 cost latency ----------
def fig11():
    fig, ax = plt.subplots(figsize=(11.2, 6.6))
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(WHITE)

    # synthetic but plausible Pareto of routing strategies
    xs = np.array([420, 880, 1450, 2100, 3200, 4800])  # cost per 1k tickets, CNY
    ys = np.array([6.8, 4.1, 2.6, 1.9, 1.45, 1.15])  # p95 end-to-end minutes
    labels = [
        "仅规则引擎",
        "边侧 8B",
        "私有 32B",
        "混合路由\n(生产采用)",
        "私有 72B\n全量",
        "公有云\n旗舰模型",
    ]
    colors = [SLATE, BLUE, TEAL, CORAL, AMBER, PURPLE]
    ax.plot(xs, ys, color=SOFT, lw=2, zorder=1)
    for x, y, lab, c in zip(xs, ys, labels, colors):
        ax.scatter([x], [y], s=90, color=c, zorder=3, edgecolors=NAVY, linewidths=0.6)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(8, 8 if "混合" not in lab else -22),
                    fontsize=9, color=INK)
    # highlight chosen
    ax.scatter([2100], [1.9], s=220, facecolors="none", edgecolors=CORAL, linewidths=2.0, zorder=4)

    ax.set_xlabel("每千张故障单综合成本（元，含 GPU / API / 人工复核）", fontsize=11, color=INK)
    ax.set_ylabel("端到端 P95 处置建议时延（分钟）", fontsize=11, color=INK)
    ax.set_title("路由策略的成本-时延帕累托前沿（NOC-Pilot 预生产压测，脱敏）", fontsize=13, color=NAVY, pad=12, weight="bold")
    ax.grid(True, color=SOFT, lw=0.8)
    for spine in ax.spines.values():
        spine.set_color(SOFT)
    ax.tick_params(colors=SLATE)
    fig.text(0.5, 0.01, "图 11  最优解通常不是最强模型。混合路由把简单单留给小模型，把复杂单留给大模型",
             ha="center", fontsize=9, color=SLATE, style="italic")
    fig.savefig(OUT / "fig11-cost-latency.png")
    plt.close()


# ---------- Fig 12 kv cache ----------
def fig12():
    fig, ax = plt.subplots(figsize=(11.4, 6.4))
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(WHITE)

    methods = ["MHA", "GQA", "MQA", "MLA", "CLA(k=2)", "INT8 KV", "INT4 KV"]
    mem = np.array([100, 25, 12.5, 7, 50, 50, 25])
    colors = [NAVY, TEAL, BLUE, CORAL, AMBER, GREEN, PURPLE]
    bars = ax.bar(methods, mem, color=colors, width=0.62, edgecolor=NAVY, linewidth=0.5)
    for b, v in zip(bars, mem):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.8, f"{v:g}%", ha="center", fontsize=10, color=INK)

    ax.set_ylabel("相对 KV Cache 显存占用（以 MHA=100%）", fontsize=11)
    ax.set_title("降低 Decode 访存瓶颈的结构与量化手段对比（同序列长度）", fontsize=13, color=NAVY, pad=12, weight="bold")
    ax.set_ylim(0, 118)
    ax.grid(True, axis="y", color=SOFT, lw=0.8)
    for spine in ax.spines.values():
        spine.set_color(SOFT)
    ax.tick_params(colors=SLATE)
    fig.text(0.5, 0.01, "图 12  GQA 是当前开源模型的主流折中；MLA 把 KV 压到潜空间，是长上下文的结构性解法",
             ha="center", fontsize=9, color=SLATE, style="italic")
    fig.savefig(OUT / "fig12-kv-memory.png")
    plt.close()


# ---------- Fig 13 hybrid routing ----------
def fig13():
    fig, ax = plt.subplots(figsize=(12.4, 6.8))
    setup(ax, (0, 12.4), (0, 6.8))
    text(ax, 6.2, 6.48, "混合推理路由：按密级、难度、预算把请求送进不同平面", fontsize=14.5, color=NAVY, weight="bold")

    rounded(ax, 0.3, 2.7, 2.3, 1.5, NAVY, NAVY, 0, 0.1)
    text(ax, 1.45, 3.45, "入站请求\n+ 密级标签", color=WHITE, fontsize=11, weight="bold")

    rounded(ax, 3.0, 2.55, 2.6, 1.8, TEAL, TEAL, 0, 0.1)
    text(ax, 4.3, 3.45, "路由器\n难度分类\n成本预算", color=WHITE, fontsize=11, weight="bold")
    arrow(ax, 2.6, 3.45, 3.0, 3.45)

    targets = [
        (6.1, 5.15, GREEN, "规则 / 缓存\n命中即返回"),
        (6.1, 3.35, BLUE, "边侧 8B\n分类与抽取"),
        (6.1, 1.55, AMBER, "私有 32B/72B\n敏感推理"),
        (9.4, 5.15, PURPLE, "公有云 LLM\n非敏感生成"),
        (9.4, 3.35, CORAL, "人工坐席\n高风险升级"),
        (9.4, 1.55, SLATE, "拒绝服务\n超预算 / 越权"),
    ]
    for x, y, c, t in targets:
        rounded(ax, x, y, 2.7, 1.2, WHITE, c, 1.6, 0.08)
        text(ax, x + 1.35, y + 0.6, t, fontsize=10, color=c, weight="bold", linespacing=1.35)

    arrow(ax, 5.6, 3.9, 6.1, 5.75, color=GREEN)
    arrow(ax, 5.6, 3.45, 6.1, 3.95, color=BLUE)
    arrow(ax, 5.6, 3.0, 6.1, 2.15, color=AMBER)
    arrow(ax, 5.6, 3.7, 9.4, 5.75, color=PURPLE, rad=0.12)
    arrow(ax, 5.6, 3.2, 9.4, 3.95, color=CORAL, rad=-0.05)
    arrow(ax, 5.6, 2.85, 9.4, 2.15, color=SLATE, rad=-0.12)

    caption(fig, "图 13  路由是架构决策，不是运维开关。密级永远优先于效果，预算永远优先于“再调一次大模型”")
    fig.savefig(OUT / "fig13-hybrid-routing.png")
    plt.close()


# ---------- Fig 14 observability ----------
def fig14():
    fig, ax = plt.subplots(figsize=(12.4, 6.6))
    setup(ax, (0, 12.4), (0, 6.6))
    text(ax, 6.2, 6.25, "AI 服务可观测性：把黑盒拆成三条可对齐的时间线", fontsize=15, color=NAVY, weight="bold")

    rows = [
        (4.55, TEAL, "应用时间线", "HTTP 延迟 · 闸门通过率 · 人工升级率 · 用户点赞/点踩"),
        (3.15, AMBER, "编排时间线", "检索命中 · 重排分数 · 工具次数 · 循环步数 · 补偿触发"),
        (1.75, CORAL, "推理时间线", "TTFT · TPOT · KV 占用 · 接受长度 · GPU 利用率 · 排队"),
    ]
    for y, c, title, body in rows:
        rounded(ax, 0.4, y, 11.6, 1.2, WHITE, c, 1.6, 0.08)
        rounded(ax, 0.4, y, 2.4, 1.2, c, c, 0, 0.04)
        text(ax, 1.6, y + 0.6, title, color=WHITE, fontsize=12, weight="bold")
        text(ax, 7.4, y + 0.6, body, fontsize=11)

    rounded(ax, 0.4, 0.35, 11.6, 1.15, NAVY, NAVY, 0, 0.08)
    text(ax, 6.2, 0.92, "对齐键：trace_id  +  request_id  +  model_name  +  tenant_id。没有对齐键的指标不能上生产。",
         color=WHITE, fontsize=11)

    caption(fig, "图 14  用户感知的慢，可能发生在检索、工具、排队或 Decode。三条时间线对不上就无法定责")
    fig.savefig(OUT / "fig14-observability.png")
    plt.close()


if __name__ == "__main__":
    for fn in [
        fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08,
        fig09, fig10, fig11, fig12, fig13, fig14,
    ]:
        fn()
        print("wrote", fn.__name__)
    print("done", list(OUT.glob("*.png")))
