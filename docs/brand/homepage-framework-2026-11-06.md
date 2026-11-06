# ROPureOEM 英文首页框架（Framework）

> 状态：框架稿（DRAFT），待用户审批；线上首页未动。
> 日期：2026-11-06。
> 流程：框架审批 → 内容撰写（配图到位）→ 上线搭建 → 桌面 + 移动端验证。SEO 不求快，慢慢打磨。

## 1. 这份框架回答什么

首页只做一件事：让品牌商 / 经销商在 30 秒内相信我们懂 OEM 流程、懂行业、懂他的问题，然后点进产品页或发询盘。

顺序按买家实际思考顺序排（不是按我们有什么排）：

能做我要的产品吗 → 能印我的品牌吗 → 多少钱、多少起订 → 能过我市场的法规吗 → 怎么保证质量 → 订单怎么走 → 选购前要知道什么 → 看视频 → 发询盘。

## 2. 参考：傅敏 watertechoem.com 英文首页（2026-11-06 实测）

实测结构（只借买家旅程逻辑，不照抄）：

- 顶栏："Source Manufacturer · Direct Supply Across Eurasia · Core Technology & Deep OEM/ODM Customization"；导航 Home / Products / News & Insights / OEM Supply / Contact Us；右上角 Inquiry Get Quote。
- 首屏 Hero：左侧大标题 "Water Purifier Manufacturer One-Stop OEM/ODM Customization" + 一站式文案 + "Request OEM Plan"；右侧两张卡：产品范围（RO、台式 / 厨下 / 冷热冰、超滤及滤芯耗材）与质量交付协同（样品确认、品牌包装、质检、出口文件、物流）。
- 认证条：CE、CB、UKCA、RoHS、REACH、EAC、SGS Tested、TÜV Tested。
- 工厂视频区："See the production floor, understand manufacturing capacity"，视频 + "Factory environment" 标签。
- 产品分类 4 卡：Under-Sink RO / Hot, Cold & Ice RO / Countertop RO / Filters, Parts and Consumables，各配图 + View Category。
- Popular Picks：筛选标签 + 8 张产品卡（图、名称、SKU、MOQ: 200、View Details / Ask Service）。
- 品牌与项目 3 栏：Product range and applications / OEM/ODM customization / Samples, quality and delivery，各配链接（Explore all products / View OEM process / Read the sourcing guide）。
- News & Insights：3 篇指南（中亚选购指南、滤芯采购参数、出货准备），配图 + 日期。
- 页脚：深色块，Online Inquiry（chat）、邮箱、Water-Treatment Supply Center、International Customer Service 四栏；其下 Company / Customer Care / Quick Access / Shop 链接栏；版权行。

需要说明的一点：2026-11-06 实测当日，watertechoem.com/en/ 首页正文里没有出现 "Start your water purifier project — tell us your target market, product type and quantity, let's discuss a suitable solution" 与 "Discuss OEM project" 这段收尾文案。第 10 节的收尾 CTA 以用户提供的截图口径为准写入框架，上线前以最终确认为准。

## 3. 设计铁律（首页先行，全站通用）

- 一节回答一个问题：一个编号、一个问题标题、一段简短回答、一张图、一个链接（下一步）。
- 不堆内容：不写长段落、不堆叠、不重复同一产品两遍；留白多、行短、标题清；移动端单列顺滑。
- 每节都视觉化：图 + 短文字，绝无纯文字板块；没有内容的板块不上线、不留空框。
- 每节末尾明确下一步：整页从浏览到询盘不断流，不留死胡同。
- 不编造：价格不公布；交期、认证只写已核实的内容（见第 6 节）；不写 NSF / PFAS / BPA / ACS / WRAS；不给证书原件；不提工厂名。

## 4. 板块顺序总览

| 序号 | 板块 | 回答的买家问题 | 下一步链接 |
| --- | --- | --- | --- |
| S1 | Hero 首屏 | 这是一家什么样的供应商？ | #q1 产品区、get-quote.html |
| S2 | Q1 产品范围 | 能做我要的产品吗？ | 各分类页 products/*.html |
| S3 | Q2 品牌定制 | 能印我的品牌吗？ | oem-odm.html |
| S4 | Q3 起订与样品 | 多少钱、多少起订？ | get-quote.html |
| S5 | Q4 市场法规 | 能过我市场的法规吗？ | certification.html |
| S6 | Q5 质量保证 | 怎么保证质量？ | oem-odm.html、about.html |
| S7 | Q6 订单流程 | 订单怎么走？ | oem-odm.html、get-quote.html |
| S8 | Q7 选购知识 | 选购前要知道什么？ | 3 个新建指南页 |
| S9 | 视频 | 眼见为实：产品长什么样？ | （视频本身；随后到 S10） |
| S10 | 收尾深色 CTA | 现在怎么开始？ | get-quote.html |

（页眉、页脚保持现状；页脚深色联系栏不变。）

## 5. 各板块细则

### S1 Hero（首屏）

- 目的：5 秒内讲清身份与入口。
- 内容：定位句（内容阶段写）+ 两个入口（看产品范围、Get a Quote）。
- 图：主视觉 1 张。现有可用：images/homepage-factory/purifier-assembly.webp（装配）或产品图组合。主视觉如不上镜，等用户提供品牌主视觉（缺料 M5）。
- 链接：#q1、get-quote.html。

### S2 Q1：能做我要的产品吗？

- 目的：按类型快速确认产品范围与定制维度（型号、流量、冷热、水龙头、滤芯组合）。
- 内容：按类型分卡，每卡一行短说明；类别以现有分类页为准（5 个）：Countertop（台式 RO）、Under-Sink（厨下 RO）、Faucet（龙头过滤）、Shower（花洒过滤）、Water Softening（软水）。冷热 / 冰与超滤是型号属性，在卡片文案中体现，不单独成类；如需单列，在内容阶段再定。同一产品在首页只出现一次。
- 图：每类 1 张代表产品图，来自 assets/products/*.png（45 张 1200×900 白底图已统一）或 assets/img/*.jpg。
- 链接：每卡 → 对应分类页（products/countertop.html、products/under-sink.html、products/faucet.html、products/shower.html、products/softener.html）；底部一个链接 → products.html（全部型号，58 个条目 / 62 个可订 SKU）。

### S3 Q2：能印我的品牌吗？

- 目的：讲清品牌定制的范围：logo、颜色、滤芯组合、水龙头、铭牌、说明书、彩盒、外箱。
- 内容：定制清单（一行一项，短句），不展开细节。
- 图：缺料 M1——品牌包装实拍（印 logo 的机身、彩盒、外箱），横图 1–2 张。本节不上没有图的版本。
- 链接：oem-odm.html。

### S4 Q3：多少钱、多少起订？

- 目的：讲清门槛与样品路径，不公布价格。
- 可写内容（已核实）：MOQ 200；样品 5–7 天发货；样品费按市场价，每型号低于 US $50；批量交期按型号与订单确认。
- 图：缺料 M2——样品套件实拍 1 张。过渡方案：CSS 三步示意图（询盘 → 样品 → 确认），仅作流程示意，不替代实拍。
- 链接：get-quote.html（主按钮）；样品与物流说明链到 oem-odm.html。

### S5 Q4：能过我市场的法规吗？

- 目的：按市场分开讲认证，不打包宣称全系列。
- 可写内容（按市场分开）：EU：CE、RoHS、REACH；UK：UKCA；CB 按型号确认；其他市场按型号确认。措辞统一为"按型号确认适用证书"。不写 NSF / PFAS / BPA / ACS / WRAS；不给证书原件；不提工厂名。
- 图：不需要照片。用 CSS 文字徽章 + 分市场小表呈现。
- 链接：certification.html。
### S6 Q5：怎么保证质量？

- 目的：用检查点证明品控：样品确认、检验、工厂、QC。
- 内容：检查点清单（样品确认 → 生产检验 → 出货前 QC），每点一句。
- 图：现有 images/homepage-factory/purifier-assembly.webp（装配）可用；缺料 M3——QC / 检测实拍（检测台、测试设备）1–2 张。
- 链接：oem-odm.html（流程与 QC）、about.html。

### S7 Q6：订单怎么走？

- 目的：把真实 OEM 流程摊开：询盘 → 选品 → 样品 → 品牌 / 包装确认 → 生产 → QC / 检验 → 运输 / 交付 → 售后。
- 可写内容：8 步时间线 + 已核实时间点（样品 5–7 天发货）与检查点（样品确认、QC、按市场分的认证）；其余时间只写"按型号与订单确认"，不编造数字。
- 图：CSS 横向时间线示意图 + 现有 images/homepage-factory/warehouse-dispatch.webp（仓库发运）、container-loading.webp（集装箱装载）。
- 链接：oem-odm.html；物流说明链到 oem-odm.html（shipping.html 待核实是否存在，见第 8 节）。

### S8 Q7：选购前要知道的知识（SEO 指南，短而有用）

- 目的：回答真正影响选型的三个问题，顺带做 SEO；首页只给摘要，详情进指南页。
- 三篇短指南（拟建，见第 9 节）：
  1. 按水质 / TDS 与流量选型
  2. 安装空间与按国家分的电压 / 插头
  3. 售后滤芯成本与维护
- 每篇首页只留：标题 + 一句话 + 1 张图。
- 图：示意图可用 CSS 画或产品图裁切；缺料 M4——安装场景实拍（厨房台面 / 厨下安装）1–2 张。
- 链接：各指南页（拟建 URL 见第 9 节）。

### S9 视频（已上线，保持）

- 内容：P90-1 产品视频（assets/video/p90-1-product.mp4，720×1280 竖版）全宽纯视频区，仅视频本身，无标题、无文字、无链接复制；id="videos" 不变，页脚 Videos 链接仍可达。
- 位置：S8 之后、S10 收尾 CTA 之前。
- 链接：本节不另设链接，看完视频自然进入 S10。

### S10 收尾深色 CTA（傅敏式，首页不"断尾"）

- 形式：深色整宽区块，放在 S9 之后、站内页脚之前。
- 文案（按用户提供的截图口径，上线前最终确认）：
  - 标题："Start your water purifier project"
  - 副文案："Tell us your target market, product type and quantity, and let's discuss a suitable solution."
  - 按钮："Discuss OEM project" → get-quote.html
- 其后才是现有站内页脚（联系方式 + 链接栏 + 版权行），页脚本身不改。

## 6. 首页能写的真实内容（信任清单，只能写这些）

- MOQ 200；样品 5–7 天发货；样品费按市场价，每型号低于 US $50；批量交期按型号与订单确认；电压 / 频率按目标国家配置；其余配置按订单确认。
- 认证按市场分开：EU：CE、RoHS、REACH；UK：UKCA；CB 按型号确认；其他按型号确认。不写 NSF / PFAS / BPA / ACS / WRAS；不给证书原件；不提工厂名。
- 目录口径：62 个可订 SKU；目录条目 58 个（两组系列合并：RP-W01 / RP-W02 / RP-W03 分体软水系列；RP-C05 / RP-C06 / RP-C14 气泡水系列；系列页已上线，重复页已改为重定向）。
- 17 张产品图的说明：引用仓库内真实原图 assets/img/*.jpg，以 4:3 白底画框 + 统一滤镜呈现；没有 AI 生成、没有抹除产品自带文字；放大后个别图仍可见产品自带小字，待用户提供干净新图后替换。

## 7. 现有素材清单（2026-11-06 盘点，可直接用）

- 产品图：assets/products/*.png 45 张（1200×900 白底）+ assets/img/*.jpg 17 张原图，共 62 款。
- 工厂 / 物流图：images/homepage-factory/ 下 3 张 webp——purifier-assembly.webp（装配）、warehouse-dispatch.webp（仓库发运）、container-loading.webp（集装箱装载）。目前首页未使用。
- 视频：assets/video/p90-1-product.mp4（P90-1，720×1280 竖版）。
- 品牌：public/brand/ 下 logo 文件。

## 8. 缺料清单（架构不为现有素材让路，等用户提供）

| 编号 | 用在哪 | 需要什么 | 要求 |
| --- | --- | --- | --- |
| M1 | S3 品牌定制 | 品牌包装实拍 1–2 张 | 印 logo 的机身、彩盒、外箱；横图；干净背景 |
| M2 | S4 起订样品 | 样品套件实拍 1 张 | 样品机 + 包装 |
| M3 | S6 质量保证 | QC / 检测实拍 1–2 张 | 检测台、测试设备 |
| M4 | S8 选购知识 | 安装场景实拍 1–2 张 | 厨房台面 / 厨下安装 |
| M5 | S1 首屏主视觉 | 品牌主视觉 1 张（可选） | 横图；没有则用现有装配图 + 产品图组合 |

- 素材要求：横图、干净背景、无其他品牌水印、无中文面板文字（有则先处理）；收到后放入 images/homepage/。
- 原则：缺料的板块不删、不改结构；可先以 CSS 示意图走内容审批，但不上线——等料齐了再上线该节。

另：以下页面在仓库根目录未找到，框架里不先假定它们存在，内容阶段再确认是否新建——shipping.html（物流）、quality-control.html（质检）、factory.html（工厂）、faqs.html（常见问题）。目前已确认存在的站内页：index.html、products.html、products/ 下分类页与详情页、oem-odm.html、certification.html、about.html、contact.html、get-quote.html。

## 9. 拟新增页面（内容阶段建，框架阶段只占位）

- 指南页 3 个（S8 链接目标），拟定 URL：
  - /guides/choose-by-water-quality.html（按水质 / TDS 与流量选型）
  - /guides/installation-voltage-plug.html（安装空间与按国家分的电压 / 插头）
  - /guides/after-sales-filter-cost.html（售后滤芯成本与维护）
- 每页：英文短指南 + 图 + 下一步链接（链回产品页 / get-quote.html）；建后加入 sitemap.xml；中文镜像按 scripts/build_bilingual.py 流程同步。
- SEO 不求快：指南页慢慢打磨，先上框架认可的 3 个主题，不一次性铺量。

## 10. 实施步骤（框架批准后）

1. 内容：逐节写英文短文案，配图按第 7–8 节落实（缺料等用户提供）。
2. 搭建：重建 index.html（保留 #videos 纯视频区与现有页眉页脚），首页问题区样式追加到 styles/components.css。
3. 指南页：新建 3 个指南页，更新 sitemap.xml，同步中文镜像。
4. 验证：桌面 + 移动端宽度逐节检查（留白、行短、每节一图一文一链、链接可达、无纯文字板块），再请用户终审上线。

## 11. 请用户审批（打勾确认）

- [ ] 板块顺序 S1–S10
- [ ] 7 个买家问题的顺序与问法
- [ ] S10 收尾深色 CTA 的文案与按钮（"Discuss OEM project"）
- [ ] 不设重复产品区（Popular Picks 式产品卡不上首页；产品只在 S2 按类型出现一次）
- [ ] 缺料 M1–M5：能否提供？大概什么时候？
- [ ] 指南页 3 个主题
- [ ] 第 8 节"未找到的页面"（shipping / quality-control / factory / faqs）是否需要新建

---

参考来源：watertechoem.com/en/（2026-11-06 实测）；ROPureOEM 仓库盘点（2026-11-06）：产品 62 款、工厂图 3 张、视频 1 个；已上线修复：视频区纯视频、17 张图恢复、两组系列合并与重定向（RP-W02 / RP-W03 / RP-C06 / RP-C14 → 系列页）。
