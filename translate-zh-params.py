#!/usr/bin/env python3
"""Translate English parameter values in zh/products/*.html to Chinese.
Only touches text nodes (content between > and <); never touches tags/attributes.
Run with --dry-run to preview counts, without it to apply.
"""
import re, glob, sys, collections

TRANSLATIONS = [
    ("Municipal tap water; 4–38°C; 0.4–0.8 MPa", "市政自来水；4–38°C；0.4–0.8 MPa"),
    ("Municipal tap water; 4–38°C", "市政自来水；4–38°C"),
    ("Municipal tap water", "市政自来水"),
    ("Tool-free pull-out change; replace the complete RO cartridge at end of life", "免工具抽拉换芯；到期整支 RO 滤芯更换"),
    ("Instant heating at the faucet; adjustable temperature", "龙头即热；温度可调"),
    ("Instant heating; configuration by order", "即热；按订单配置"),
    ("Instant heating", "即热"),
    ("≥2000 ppb; manufacturer claim, not a third-party test report", "≥2000 ppb；厂家宣称，非第三方检测报告"),
    ("≥45.42 L/min at 0.2 MPa; 1-inch pipes", "≥45.42 L/min（0.2 MPa 下）；1 英寸管"),
    ("≥45.42 L/min at 0.2 MPa", "≥45.42 L/min（0.2 MPa 下）"),
    ("≥50% at 15 L/min; 2 ±0.3 ppm feed", "≥50%（15 L/min 时）；进水 2 ±0.3 ppm"),
    ("≥189 tonnes (source test water)", "≥189 吨（源水测试）"),
    ("360 × 175 × 320 mm / 405 × 172 × 311.5 mm; by tank configuration", "360 × 175 × 320 mm / 405 × 172 × 311.5 mm；按水箱配置"),
    ("398 × 114 × 303.5 mm; length includes cartridges", "398 × 114 × 303.5 mm；长度含滤芯"),
    ("0.9 m³ at 340 ppm hardness", "0.9 m³（硬度 340 ppm）"),
    ("20 L/h at ≥90°C / 2.5–3 L/h at ≤10°C", "20 L/h（≥90°C）/ 2.5–3 L/h（≤10°C）"),
    ("20 L/h at ≥90°C", "20 L/h（≥90°C）"),
    ("2200 W; 18 L/h at ≥90°C", "2200 W；18 L/h（≥90°C）"),
    ("150 / 300 / 500 mL / continuous", "150 / 300 / 500 mL / 不限量"),
    ("ACF / vitamin C + ACF / scale-inhibition media + KDF + ACF", "ACF / 维生素 C + ACF / 阻垢介质 + KDF + ACF"),
    ("Ceramic + GAC / CTO / UF + GAC", "陶瓷 + GAC / CTO / UF + GAC"),
    ("Ceramic + GAC / CTO", "陶瓷 + GAC / CTO"),
    ("Ceramic + GAC", "陶瓷 + GAC"),
    ("Ceramic + ACF", "陶瓷 + ACF"),
    ("Ceramic", "陶瓷"),
    ("PPC/post-carbon composite + RO", "PPC/后置碳复合 + RO"),
    ("PPC + RO + post-carbon", "PPC + RO + 后置碳"),
    ("PP+C + RO + post-carbon", "PP+C + RO + 后置碳"),
    ("PCB + RO + post-carbon", "PCB + RO + 后置碳"),
    ("PP &amp; carbon fiber + RO + post-carbon", "PP + 碳纤维 + RO + 后置碳"),
    ("PAC composite + RO + natural mineralization", "PAC 复合 + RO + 天然矿化"),
    ("No RO", "无 RO"),
    ("PP & carbon fiber + RO + post-carbon", "PP + 碳纤维 + RO + 后置碳"),
    ("PCC composite pre-filter + RO", "PCC 复合前置滤芯 + RO"),
    ("PP / PP + calcium sulphite / carbon block", "PP / PP + 亚硫酸钙 / 炭块"),
    ("PP + carbon + 60 g KDF", "PP + 炭 + 60 g KDF"),
    ("PP + vitamin C aroma cartridge", "PP + 维 C 香薰滤芯"),
    ("PP cotton + vitamin C cartridge", "PP 棉 + 维 C 滤芯"),
    ("Pleated cotton + activated carbon", "折叠棉 + 活性炭"),
    ("Vitamin C + PP cotton", "维 C + PP 棉"),
    ("PC + ABS; silicone sealing ring", "PC + ABS；硅胶密封圈"),
    ("ABS; painted finish", "ABS；喷漆"),
    ("Food-grade reinforced PP", "食品级增强 PP"),
    ("Grooved PP sediment", "沟槽 PP 沉淀滤芯"),
    ("Dual-chip semiconductor cooling; 6°C", "双芯片半导体制冷；6°C"),
    ("Dual water / recirculation / heating", "双出水/循环/加热"),
    ("Direct drinking / produce washing", "直饮/洗菜"),
    ("Digital display / heated", "数字显示/加热"),
    ("Raw / filtered water selection", "原水/净水切换"),
    ("Raw water 6 L; waste water 2.5 L", "原水 6 L；废水 2.5 L"),
    ("Replaceable; configuration by order", "可更换；按订单配置"),
    ("Aerator option; configuration by order", "起泡器可选；按订单配置"),
    ("Configurable to target country", "按目标国家配置"),
    ("No plumbing installation required", "免安装"),
    ("Integrated faucet filter", "一体式龙头过滤器"),
    ("Split faucet filter", "分体式龙头过滤器"),
    ("Inline shower prefilter", "管路式淋浴前置过滤器"),
    ("Portable handheld shower filter", "便携式手持淋浴过滤器"),
    ("Side-access cartridges", "侧插式滤芯"),
    ("Snap-fit replacement", "卡扣式更换"),
    ("Stainless steel", "不锈钢"),
    ("Thick-film instant heat", "厚膜即热"),
    ("Water-driven turbine LED", "水驱动涡轮 LED"),
    ("Ultrasonically welded as one unit", "超声波焊接一体"),
    ("Two cartridges; five stages", "两支滤芯；五级"),
    ("Five-in-one RO with mineral stage", "五合一 RO，带矿化"),
    ("Composite pre/post filter + RO", "复合前后置滤芯 + RO"),
    ("Compressor; 3.0 L/h", "压缩机制冷；3.0 L/h"),
    ("Compressor; 5–10°C", "压缩机制冷；5–10°C"),
    ("5-in-1 composite RO cartridge", "五合一复合 RO 滤芯"),
    ("6 adjustable temperature programs", "6 档温度程序"),
    ("6-stage version available", "六级版本可选"),
    ("10-inch large-diameter", "10 英寸大直径"),
    ("270° rotation", "270° 旋转"),
    ("360° rotation", "360° 旋转"),
    ("360° stepless adjustment", "360° 无级调节"),
    ("2: pre-filter + RO", "2 支：前置滤芯 + RO"),
    ("4 stages; no RO", "四级；无 RO"),
    ("2.7 L; removable", "2.7 L；可拆卸"),
    ("2-5 µm (ceramic)", "2–5 µm（陶瓷）"),
    ("3-6 months", "3–6 个月"),
    ("Approximately 3 months", "约 3 个月"),
    ("Approx. 3 seconds", "约 3 秒"),
    ("Class I", "I 类"),
    ("None / 0.8 L", "无/0.8 L"),
    ("None", "无"),
    ("RO purification", "RO 净化"),
    ("SPE electrolysis", "SPE 电解"),
    ("Wall / countertop", "壁挂/台式"),
    ("按订单确认（Confirmed per order）", "按订单确认"),
]
# Longest first so longer phrases win over their substrings.
TRANSLATIONS.sort(key=lambda x: -len(x[0]))

text_re = re.compile(r'>([^<]+)<')
dry = '--dry-run' in sys.argv
counts = collections.Counter()
files_changed = []

for path in sorted(glob.glob('zh/products/*.html')):
    s = open(path, encoding='utf-8').read()
    def repl(m):
        t = m.group(1)
        for en, zh in TRANSLATIONS:
            if en in t:
                n = t.count(en)
                counts[en] += n
                t = t.replace(en, zh)
        return '>' + t + '<'
    new = text_re.sub(repl, s)
    if new != s:
        files_changed.append(path)
        if not dry:
            open(path, 'w', encoding='utf-8').write(new)

print(f"Files changed: {len(files_changed)}")
print(f"Total replacements: {sum(counts.values())}")
for en, n in counts.most_common():
    zh = dict(TRANSLATIONS)[en]
    print(f"  {n:4d}  {en!r} -> {zh!r}")
if dry:
    print("DRY RUN - no files written")
else:
    print("Applied.")
    for f in files_changed:
        print("  ", f)
