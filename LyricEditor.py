import sublime
import sublime_plugin
import time
import datetime
import re
from functools import partial

status = {
    'idle': 'doing nothing',
    'tagging': 'tagging...',
    'pause': 'paused...',
    'playing': 'playing...',
    'done': 'done',
}
settings = None

def log(line):
    if settings and settings.get('debug', False):
        print(line)

def view():
    return sublime.active_window().active_view()

def status_message(name):
    return '[lyric editor] ' + status.get(name)

def set_status(name):
    if name not in status.keys():
        name = 'idle'
    log('set status to:%s' % name)
    return view().set_status('lyric editor', status_message(name))

def get_status():
    message = view().get_status('lyric editor')
    for s in status:
        if status_message(s) == message:
            return s
    return None

class Timer():
    _start = None
    _pause = None

    def reset(self):
        self._start = None
        self._pause = None

    def start(self):
        self._start = time.time()
        self._pause = None
        log('timer: start %s' % self._start)

    def start_at(self, at):
        self._start = time.time() - float(at)
        self._pause = None
        log('timer: start at %s' % self._start)

    def started(self):
        return self._start is not None

    def delta(self):
        return time.time() - self._start

    def pause(self):
        # multiple pause only count once
        if not self._pause:
            self._pause = time.time()
            log('timer: pause at %s' % self._pause)

    def resume(self):
        if not self._pause:
            sublime.error_message('already running')
            return False

        self._start = time.time() - (self._pause - self._start)
        self._pause = None

t = Timer()
def timer():
    return globals()['t']

def plugin_loaded():
    globals()['settings'] = sublime.load_settings('LyricEditor.sublime-settings')
    set_status('idle')

class LyricInsertMetaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        metas = settings.get('meta', {})
        log('meta:%s' % metas)

        snippet = ''
        i = 1
        for name, placeholder in metas.items():
            snippet += '[%s: ${%d:%s}]\n' % (name, i, placeholder)
            i += 1

        if snippet:
            v = view()
            v.run_command('move_to', {'to': 'bof'})
            v.run_command('insert_snippet', {'contents': snippet})

def toggle_distraction_free(on):
    options = {
        'line_numbers': False,
        'gutter': True,
        'draw_centered': True,
        'scroll_past_end': True,
        'highlight_line': True
    }
    settings = view().settings()
    if not on:
        for o in options:
            settings.erase(o)
    else:
        for o, v in options.items():
            settings.set(o, v)


class StartAtInputHandler(sublime_plugin.TextInputHandler):
    pattern = re.compile(r'^\d+:\d\d(.\d\d)?$')

    def initial_text(self):
        tags = []
        view().find_all(r'^\[(\d+:\d\d\.\d\d.*)\]', 0, '$1', tags)
        return tags.pop() if tags else '00:00.00'

    def placeholder(self):
        return 'something like 55:42.31'

    def validate(self, text):
        return bool(self.pattern.match(text))

    def preview(self, text):
        if text == '':
            return None
        if self.pattern.match(text):
            return text
        return 'invalid'

class LyricStartAtCommand(sublime_plugin.TextCommand):
    def run(self, edit, start_at):
        minutes, seconds = start_at.split(':')
        timer().start_at(int(minutes) * 60 + float(seconds))
        toggle_distraction_free(True)
        set_status('tagging')

    def input(self, args):
        return StartAtInputHandler()

    def input_description(self):
        return 'Set Start Time'

class LyricStartCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if (timer().started()):
            reset = sublime.ok_cancel_dialog('Tagging already started, reset timer?', 'Reset')
            if not reset:
                return False
        toggle_distraction_free(True)
        timer().start()
        set_status('tagging')

def make_tag():
    passed = timer().delta()
    minutes, seconds = divmod(passed, 60)
    return '[%.2d:%05.2f]' % (minutes, seconds)

class LyricTagAndNextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print('status:%s' % get_status())

        v = view()
        if get_status() == 'pause':
            timer().resume()
            set_status('tagging')

        if get_status() != 'tagging':
            sublime.error_message("[lyric editor]: please start first")
            return False

        # find next non tag line
        pattern = r'^(?!\[.+:.*\]).*$'
        if settings.get('skip_empty_line', True):
            log('skip empty line')
            pattern = r'^(?!\[.+:.+\]).+$'
        next_line = v.find(pattern, 0)
        log('next line:%s' % next_line)

        if next_line.a < 0:
            sublime.message_dialog("Tagging complete")
            set_status('done')
            timer().reset()
            toggle_distraction_free(False)
        else:
            v.sel().clear()
            v.sel().add(next_line.a)
            v.insert(edit, next_line.a, make_tag())

class LyricPauseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        timer().pause()
        set_status('pause')

class LyricResumeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        timer().resume()
        set_status('tagging')

class LyricOffsetCommand(sublime_plugin.TextCommand):
    def run(self, edit, updown='up'):
        log('--offseting--')
        v = view()
        step = float(settings.get('offset_step', 0.5))
        sels = v.sel()

        tag_pattern = re.compile(r'^\[(\d+:\d\d\.\d\d)\]')
        for s in sels:
            for line in v.lines(s):
                log('  line:%s' % v.substr(line))
                match = tag_pattern.match(v.substr(line))
                if not match:
                    continue

                tag = match.group(1)
                log('  old tag:%s' % tag)
                minute, second = tag.split(':')
                if updown == 'up':
                    second = float(second) + step
                else:
                    second = float(second) - step

                minute_plus, new_second = divmod(second, 60)
                new_minute = float(minute) + minute_plus
                new_tag = '%.2d:%05.2f' % (new_minute, new_second)
                log('  new tag:%s' % new_tag)

                v.replace(edit, sublime.Region(line.a+1, line.a+len(tag)+1), new_tag)

class LyricPlayCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if get_status() == 'playing':
            sublime.error_message('Already playing...')
            return False

        v = view()

        tags = []
        tag_regions = v.find_all(r'^\[(\d+:\d\d\.\d\d)\]', 0, '$1', tags)
        log('tags:%s' % tags)
        if not tags:
            sublime.error_message('No time tag found')
            return False

        v.set_read_only(True)
        toggle_distraction_free(True)
        set_status('playing')
        i = 0
        for tag in tags:
            minutes, seconds = tag.split(':')
            timeout = (int(minutes)*60 + float(seconds)) * 1000
            log('timeout:%s' % timeout)

            is_last = (len(tags) - 1) == i
            roll = partial(self.highlight, v, tag_regions[i].a, is_last)
            sublime.set_timeout_async(
                partial(
                    self.highlight,
                    v,
                    partial(
                        v.run_command,
                        'lyric_roll_next',
                        {'pos': tag_regions[i].a, 'is_last': is_last}
                        )
                    ),
                timeout)
            i += 1

    def highlight(self, v, roll):
        if v.is_valid():
            roll()

class EscapePlayContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, op, operand, match_all):
        if not key.startswith('lyric_editor'):
            return None
        return get_status() == 'playing'

class LyricRollNextCommand(sublime_plugin.TextCommand):
    def run(self, edit, pos, is_last):
        if not get_status() == 'playing':
            return False

        log('pos:%s' % pos)
        log('is_last:%s' % is_last)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pos, pos))
        self.view.show_at_center(pos)

        if is_last:
            set_status('done')
            toggle_distraction_free(False)
            self.view.set_read_only(False)
