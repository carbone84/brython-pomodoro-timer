import time
from browser import document, alert, html
from browser.timer import clear_interval, set_interval
        
document <= html.AUDIO(id="audio", src="./cut_gkopeckak__bell.wav", type="audio/wav")

_timer = None
_alarm = None
counter = 0
timer_length = 0
audio = document['audio']
pom_min = document['pom-min']
pom_sec = document['pom-sec']
break_min = document['break-min']
break_sec = document['break-sec']
start_button = document['start-btn']
stop_button = document['stop-btn']
countdown = document['countdown']
pom_button = document['pomodoro']
break_button = document['break']

def show():
    global _timer, _alarm
    if countdown.text is '00:00':
        clear_interval(_timer)
        _timer = None
        calculate_countdown(timer_length)
        start_button.text = 'Start'
        stop_button.innerHTML = 'Stop ' + "&#128266;"
        if stop_button.text is not 'Stop':
            _alarm = set_interval(audio.play, 1000)
    else:
        calculate_countdown(counter - time.time())
        display_mins_secs()

def set_timer():
    global timer_length
    if document['pomodoro'].checked:
        timer_length = ((int(pom_min.value) if pom_min.value else 0) * 60) + (int(pom_sec.value) if pom_sec.value else 0)
    else: 
        timer_length = ((int(break_min.value) if break_min.value else 0) * 60) + (int(break_sec.value) if break_sec.value else 0)
    calculate_countdown(timer_length)
    display_mins_secs()
        
def calculate_countdown(time_left):
    countdown.text = time.strftime("%M:%S", time.gmtime(time_left))

def display_mins_secs():
    document['minute-1'].text = countdown.text[0]
    document['minute-2'].text = countdown.text[1]
    document['second-1'].text = countdown.text[3]
    document['second-2'].text = countdown.text[4]

def start_timer(e):
    global _timer, counter
    if _timer is None:
        set_timer()
        if timer_length == 0:
            alert("Time must be greater than 0")
        else:
            counter = time.time() + timer_length
            _timer = set_interval(show, 1000)
            start_button.text = 'Hold'
    elif _timer == 'hold': # restart
        # restart timer
        counter = time.time() + float((int(countdown.text[:2]) * 60) + int(countdown.text[3:]))
        _timer = set_interval(show, 1000)
        start_button.text = 'Hold'
    else: # hold
        clear_interval(_timer)
        _timer = 'hold'
        start_button.text = 'Restart'
        
def stop_timer(e):
    global _timer, _alarm
    clear_interval(_timer)
    _timer = None
    calculate_countdown(timer_length)
    display_mins_secs()
    start_button.text = 'Start'
    if stop_button.text is not 'Stop':
        stop_button.text = 'Stop'
        clear_interval(_alarm)

def display_time(e):
    set_timer()

start_button.bind('click', start_timer)
stop_button.bind('click', stop_timer)
pom_button.bind('click', display_time)
break_button.bind('click', display_time)