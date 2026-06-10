# dlfetch skill

让 Claude 通过 `dlfetch` CLI 操作 THISDL(稻香湖学校)学习平台(thisdlstu.schoolis.cn):查任务、交作业、看课表、查 GPA 等。

## 这个目录里有什么

- `SKILL.md` — 给 Claude 的指令(怎么调用 dlfetch、有哪些命令、交作业流程、科目代码表)。
- `README.md` — 本文件,给人看的说明。

**这里故意不放源代码和 venv。** dlfetch 的源码只有一份,在开发仓库里(个人 Mac 上是 `~/PycharmProjects/THISDLMenu`,远程是 GitHub `THISDLAAIC/dlfetch`,`huangdihd/dlfetch` 为同步镜像)。skill 只是"指挥"已安装的 dlfetch,这样代码更新后 skill 自动跟进,不会出现两份代码不同步的问题。

## dlfetch 的运行方式(按优先级)

| 环境 | 运行方式 |
|------|----------|
| 个人 Mac | PATH 里的二进制 `~/.local/bin/dlfetch`(软链接指向仓库 `dist/dlfetch`) |
| 学校电脑(无管理员权限,跑不了二进制) | 源码运行:`~/dlfetch/.venv/bin/python ~/dlfetch/main.py <命令>`,终端里用 `dlfetch` alias |
| 没装过 | `zsh <(curl -fsSL https://raw.githubusercontent.com/huangdihd/dlfetch/master/install.sh)` —— clone 到 `~/dlfetch` + venv + alias,全程不需要管理员权限 |

## 凭据

- 首次运行时交互式输入用户名和密码(密码不回显)。
- 密码立即做 MD5 后丢弃明文,存入**系统钥匙串**(macOS Keychain,service 名 `dlfetch`);无钥匙串的环境回退到 `~/.dlfetch/credentials`(权限 0600)。不写任何环境变量,不进 `.zshrc`。
- 换账号或改密码后:`dlfetch logout` 清除已存凭据和会话,下次运行重新输入。
- 连续输错密码 5 次,账号会在当前网络下被临时锁定 10 分钟。

## 维护

- 改了代码后重新打包二进制(个人 Mac):仓库目录下 `.venv/bin/pyinstaller dlfetch.spec --noconfirm`,PATH 软链接自动生效。
- 学校电脑更新:`cd ~/dlfetch && git pull`。
