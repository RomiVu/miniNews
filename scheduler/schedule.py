import time, datetime
import heapq
from collections import namedtuple, deque
import threading
from time import monotonic as _time



class Event(namedtuple('Event', 'time, interval, priority, action, kwargs')):
    __slots__ = []
    def __eq__(s, o): return (s.time, s.priority) == (o.time, o.priority)
    def __lt__(s, o): return (s.time, s.priority) <  (o.time, o.priority)
    def __le__(s, o): return (s.time, s.priority) <= (o.time, o.priority)
    def __gt__(s, o): return (s.time, s.priority) >  (o.time, o.priority)
    def __ge__(s, o): return (s.time, s.priority) >= (o.time, o.priority)


_sentinel = object()


class Scheduler:
    '''make a scheduled daemon'''
    def __init__(self, timefunc=_time, delayfunc=time.sleep):
        print(f'initing {datetime.datetime.now()}')
        self._queue = []
        self._lock = threading.RLock()
        self.timefunc = timefunc
        self.delayfunc = delayfunc
    
    def add_into_queue(self, interval, priority, action, kwargs_dict):
        '''every interval time run the ACTION'''
        event = Event(self.timefunc()+interval,interval, priority, action, kwargs_dict)
        with self._lock:
            heapq.heappush(self._queue, event)
    
    
    def add_into_queue_fixed(self, date_time, priority, action, kwargs_dict):
        '''every fixed time per day, run the ACTION'''
        pass
    
    def cancel(self, event):
        with self._lock:
            self._queue.remove(event)
            heapq.heapify(self._queue)
    
    def isEmpty(self):
        with self._lock:
            return not self._queue
    
    @property
    def queue(self):
        with self._lock:
            events = self._queue[:]
        return list(map(heapq.heappop, [events]*len(events)))

    def run(self, blocking=True):
        lock = self._lock
        q = self._queue
        delayfunc = self.delayfunc
        timefunc = self.timefunc
        pop, insert = heapq.heappop, heapq.heappush
        while True:
            with lock:
                if not q:
                    break
                time, interval, priority, action, kwargs = q[0]
                now = timefunc()
                if time > now:
                    delay = True
                else:
                    delay = False
                    pop(q)
                    insert(self._queue, Event(now+interval,interval, priority, action, kwargs))
            if delay:
                if not blocking:
                    return time - now
                delayfunc(time - now)
            else:
                action(kwargs)
                delayfunc(0)   # Let other threads run


    
