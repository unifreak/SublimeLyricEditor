# Lyric Editor (for LRC file)

_中文请见 [这里](https://github.com/UniFreak/SublimeLyricEditor/blob/master/README.cn.md "中文 README")_

LRC (short for LyRiCs) is a computer file format that synchronizes song lyrics with an audio file ([Wikipedia Link](https://en.wikipedia.org/wiki/LRC_(file_format)).

Lyric Editor turns sublime text editor into a, well, lrc/lyric editor.

## Features

- Start at specified time point.
- Generate time tag.
- Adjust offset.
- Play lyrics.
- Pause / resume.

## Install

Using `Package Control`:

1. Open Command Pallete, and run `Package Control: Install Package`.
2. Search for `Lyric Editor` and install.

Or by cloning source from github:

1. Browse into your sublime text's package folder.
2. Run `git clone https://github.com/UniFreak/SublimeLyricEditor.git`.

## Usage

### Commands

Here are commands that Lyric Editor provide, with some description:

- `Insert Meta Info`: insert a snippet to help you generate id tags.
- `Start`: start timer at 00:00.00.
- `Start At`: start timer at specified point.
- `Tag and Next`: tag untagged line and move to next.
- `Pause / Resume`: pause / resume timer.
- `Play`: play lyrics, will rolling to each line according to its time tag.

### Typical Workflow

Open lyric file, start playing song with chosen music player.

Fire up command pallete, and run `Lyric Editor: Start` command, to start calc timing.

When you hear the lyric singing , press `ctrl+alt+j` to run `Tag and Next` command.
Lyric Editor will locate the first untagged line, calc time, and tag it.

You can keep tagging untill Lyric Editor can no longer find any line.

After tagging done, you may want to do some offset adjustment. You can do this by
press `ctrl+alt+[` or `ctrl+alt+]`. Lyric Editor will decrease/increase current
line's tag time. If you have multiple lines selected, all selected line will be adjusted.

Now, you may run `Lyric Editor: Play` command to preview your work.
Lyric Editor will roll to each tagged line according to its tag time, just like some
music players do. While playing lyrics, you can press `esc` to abort play

### Pause / Resume

While tagging, You can press `ctrl+alt+space` to pause/resume timer at any time

### Start At Specific Time

If for some reason, you've lost the track (for instance, forget to pause when go for a drink), and don't want
restart all over again. You can do this by start timer at a specific point, and begin your work
from there. Just run `Lyric Editor: Start At` command, Lyric Editor will find the last time tag
as default, and show a input dialog, offering oppotunity for you to change, if the last time tag
is not what you desired

### Insert Meta Info

You can run `Lyric Editor: Insert Meta Info` to generate some infomation about the
lyric's song title, album name, etc. Lyric Editor will insert a snippet at file beginning,
tag through to put in the correct infomation.

## Config

Here are the default configurations:

```js
{
    "debug": false, // show debug log
    "skip_empty_line": false, // skip empty line when tagging
    "offset_step": 0.5, // set offset step, by seconds
    "meta": { // meta info snippet items. you can add your own id tag here
        "ar" : "Lyrics artist",
        "al" : "Album",
        "ti" : "Lyrics (song) title",
        "au" : "Creator of the Songtext",
        "by" : "Creator of the LRC file",
    }
}
```

To add or change config, follow menu `Preferences -> Package Settings -> LyricEditor -> Settings - User`, and put configs there.
