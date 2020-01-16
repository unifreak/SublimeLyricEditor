# Lyric Editor (for LRC file)

LRC (LyRiCs 的缩写) 是用于同步滚动歌曲歌词的文件格式. 具体见 [维基百科](https://zh.wikipedia.org/zh/LRC%E6%A0%BC%E5%BC%8F).

Lyric Editor 插件让 sublime text 编辑器支持 lrc 歌词编辑

## 特性

- 指定打标签开始时间点.
- 自动生成时间标签.
- 调整偏移量.
- 播放歌词.
- 暂停 / 继续.

## 安装



使用 `Package Control` 安装:

1. 打开命令面板 (command pallete), 运行 `Package Control: Install Pacakge`.
2. 搜索 `Lyric Editor` 并安装.

另一种方式是直接通过克隆源码安装:

1. 进入 sublime text 的包目录.
2. 运行 `git clone https://github.com/UniFreak/SublimeLyricEditor.git`.

## 使用

### 命令

以下是 Lyric Editor 提供的一些命令及其简介:

- `Insert Meta Info`: 插入一个 snippet, 用于编辑歌词元信息 (名称, 作者, 专辑等等...)
- `Start`: 从 00:00.00 开始计时.
- `Start At`: 从指定时间点开始计时.
- `Tag and Next`: 为下一句歌词打标签.
- `Pause / Resume`: 暂停 / 继续计时.
- `Play`: 播放歌词.

### 一般流程

打开歌词文件, 用你喜欢的播放器开始播放歌曲.

调出命令面板, 运行 `Lyric Editor: Start` 命令, 开始标签计时.

当听到对应歌词时, 快捷键 `ctrl+alt+j` 运行 `Tag and Next` 命令. Lyric Editor 会定位到第一个未
打标签的歌词, 计算时间并为其打上时间标签.

重复以上步骤, 直到 Lyric Editor 找不多更多歌词为止.

标签打完之后, 你可以微调一下偏移量. 快捷键 `ctrl+alt+[` 或 `ctrl+alt+]` 会减小/增加当前行歌词
的时间. 如果有多行选中, 则选中的所有行都会偏移.

现在, 可以运行 `Lyric Editor: Play` 命令来播放, 以歌词是否同步. Lyric Editor 会像某些音乐播放器
似的, 在对应的时间滚动到相应的歌词行上.

### 暂停 / 继续

打标签的时候, 可以使用快捷键 `ctrl+alt+space` 来暂停或继续标签计时器.

### 在指定时间点开始打标签

打标签时, 有时可能乱了节奏 (比如去上厕所的时候, 忘了暂停计时器). 这种时候也不必从头开始打标签.
运行 `Lyric Editor: Start At` 命令, Lyric Editor 会找到最后一个时间标签作为默认, 弹出输入框.
你可以输入自己想要的时间点, 或者使用默认值, 继续开始打标签.

### 插入元数据

运行 `Lyric Editor: Insert Meta Info`, 会生成一个 snippet 并插入到文件开头. 用 tab 移动到
各个位置, 以便编辑诸如歌名, 专辑名, 作者等信息.

## 配置

以下是支持的所有配置及其默认值:

```js
{
    "debug": false, // 是否打印调试 log
    "skip_empty_line": false, // 打标签时, 是否跳过空行
    "offset_step": 0.5, // 调整偏移量时, 每次偏移量的大小. 以秒为单位
    "meta": { // 元信息 snippet
        "ar" : "Lyrics artist",
        "al" : "Album",
        "ti" : "Lyrics (song) title",
        "au" : "Creator of the Songtext",
        "by" : "Creator of the LRC file",
    }
}
```

通过菜单 `Preferences -> Package Settings -> LyricEditor -> Settings - User`, 可以打开用户配置文件, 以更改配置.
