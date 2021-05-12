/********
 **
 **  SPDX-License-Identifier: MIT
 **
 **  Copyright (c) 2017-2021 James M. Putnam <putnamjm.design@gmail.com>
 **
 **/

/********
 **
 **  module.h: grafch modules
 **
 **/
#if !defined(GRAFCH_MODULE_H_)
#define GRAFCH_MODULE_H_

#include <csignal>
#include <ctime>
#include <functional>
#include <iostream>
#include <mutex>
#include <thread>
#include <utility>
#include <vector>

#include <getopt.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

namespace grafch {

/* abstract base class, threading and events */
class Module {
  enum class EventSource { NOEVENT, TIMER, NCS31X };
  typedef uint32_t EventId;
  typedef std::pair<EventSource, EventId> Event;
  typedef std::pair<bool, Event> CEvent;

  std::vector<Event> event_queue;
  std::mutex event_queue_lock;

  EventId event_id = 0;

 public: /* object model */
  std::thread* module;

  void init(void(*fn)()) {
    module = fn == nullptr ? nullptr : new std::thread(fn);
  }

  EventId event_notify(EventSource src) {
    event_queue_lock.lock();
    event_queue.push_back(Event{src, ++event_id});
    event_queue_lock.unlock();
    return event_id;
  }

  /** * check for event_queue_lock? **/
  CEvent find_event(EventId id) {
    for (auto event : event_queue)
      if (event.second == id)
        return CEvent{true, event};
    return CEvent{false, Event{EventSource::NOEVENT, 0}};
  }

  /** * check for event_queue_lock? **/
  std::vector<Event> find_event(EventSource src) {
    auto events = std::vector<Event>{};
    
    for (auto event : event_queue)
      if (event.first == src)
        events.push_back(event);
    return events;
  }

  /** * check for event_queue_lock? **/
  void consume_event(uint32_t id) {
    for (auto it = event_queue.begin(); it != event_queue.end(); )
      if (it->second == id) {
        event_queue.erase(it);
        break;
      }
  }

  virtual void Events() = 0;

  Module() { }

}; /* class Module */

} /* grafch namespace */

#endif /* GRAFCH_MODULE_H_ */
