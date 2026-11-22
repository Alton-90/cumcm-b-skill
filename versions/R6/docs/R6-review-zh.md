# 对五项外部建议的批判性处理

## 结论
采纳审计无环顺序、版本化Schema、统一新写入路径、G4A/G4B拆分。采纳确定性机械检查，但拒绝“加几个脚本就能保证Codex不可绕过、验证真人身份或数学正确”的过度承诺。

1. 审计死锁：R5 completeness确实同时要求自身和未来QA；已删除两项依赖。consistency→completeness→QA按当前文件验证。不是所有局部审计都强制全链，只在最终提交按顺序执行。
2. Schema：17种受管理机器产物使用唯一逻辑Schema；三运行树是同步分发副本。移除5个过期schema模板和竞争的内嵌JSON样例。JSONL作为追加决策记录保留；Markdown仍承载推导/报告，通过report-binding绑定，不把所有科学内容强塞JSON。原始数据和任务指标不是流程状态，不强套统一研究Schema。
3. 门控：增加validate_gate、validate_workspace、freeze_results、check_staleness，共用gate_engine。程序重新检查当前文件、Schema、主/基线、决策源摘录、哈希、选择指纹、数值来源、报告及审计依赖。手写verdict不决定机械结果。它不是宿主权限隔离、CI拦截器或身份签名系统，同权限代理仍可能绕过；语义审查仍不可省略。
4. 路径：采用planning、methods/Qx、code/Qx/{python,matlab,reviews}、results/Qx、robustness/Qx、paper；额外明确data/raw与data/clean。数据画像与清洗数据本来就是不同产物，不能把二者混成一个目录。画像统一planning/data。旧文件只读迁移，不改既有训练工作区。
5. G4：G4A记录已判断的结果（包括失败），G4B要求submission、完成义务、当前稳健性PASS与可复算冻结。evidence_only仅作留存，不是完成。切换profile重新检查，不使用旧G4标签推断冻结完成。

## 重要实施边界
- 哈希变化是保守的字节级过期，不自动判断科学意义；格式变动也可能要求复核。未引用的文件不影响当前门控。
- 旧记录不能无损自动变成可信新证据。R6是破坏性契约升级，使用schema_version=2；需要迁移的新字段缺失时明确阻塞，不能编造来源和已执行状态。
- 冻结仅支持注册的选中方法JSON输出与RFC6901指针；表格先经实验代码转为可追溯指标JSON。旧快照归档保留，不宣称不可篡改存储。
- 第三方语义状态/用户导出记录的真实性不由同一写权限环境证明。程序PASS只证明机械检查通过。

## 验证
见R6-runtime-tests.json：合成端到端流程与负例，覆盖无环审计、缺失基线、伪PASS、过期引用、同时间戳内容修改、旧Schema、冻结篡改、G4A失败判断和CLI退出码。不等于完整赛题性能或独立代理行为评估。
