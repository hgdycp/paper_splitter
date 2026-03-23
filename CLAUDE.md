# CLAUDE.md - 试卷分割系统项目规范

## 项目概述

试卷分割系统 - 使用 OCR 和图像处理技术自动分割试卷 PDF。

## Git 提交规范

采用 Angular 提交规范格式：

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Type 类型

| Type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构（不是修复也不是新功能） |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖更新 |

### Scope 范围

使用模块名或功能名：

- `pdf` - PDF 处理模块
- `image` - 图像处理模块
- `detector` - 题目检测模块
- `splitter` - 分割输出模块
- `config` - 配置相关
- `docs` - 文档相关
- `ci` - CI/CD 相关

### Subject 规范

- 简洁，不超过 50 字符
- 使用中文描述
- 动词开头（添加、修复、优化、改进等）
- 不以句号结尾

### 示例

```
feat(detector): 添加答题区域检测功能

fix(pdf): 修复多页 PDF 转换时内存泄漏问题

docs: 更新开发指南中的工作栈说明

refactor(image): 重构图像预处理逻辑
```

### 提交检查

提交前确保：
- [ ] 代码通过测试 `pytest tests/`
- [ ] 没有临时调试代码
- [ ] 提交信息符合规范

---

## 分支管理规范

### 禁止事项

- **严禁** 直接 push 到 `master` / `main` 分支
- **严禁** 在 `master` / `main` 分支直接提交代码

### 分支流程

1. **创建功能分支**

```bash
git checkout -b feat/detector-optimization
```

2. **在分支上开发并提交**

```bash
git add .
git commit -m "feat(detector): 优化题目检测算法"
```

3. **推送到远程**

```bash
git push -u origin feat/detector-optimization
```

4. **创建 Pull Request**（通过 GitHub 网页）

5. **等待 Code Review 后合并**

### 分支命名规范

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 功能分支 | `feat/<功能名>` | `feat/detector-optimization` |
| 修复分支 | `fix/<问题描述>` | `fix/pdf-memory-leak` |
| 文档分支 | `docs/<更新内容>` | `docs/api-reference` |
| 重构分支 | `refactor/<模块名>` | `refactor/image-processor` |

### 紧急修复

如需紧急修复生产问题，可使用：

```bash
git checkout -b hotfix/critical-bug
# 修复后直接合并到 master，但需通知团队
```
