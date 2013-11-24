from icalendar import Calendar

import pytz
import datetime


week_days= {'MO':0,'TU':1,'WE':2,'TH':3,'FR':4,'SA':5,'SU':6}


#This is what will be used by the calendar view
class schedule_entry:
    def __init__(self):
        self.time = 0
        self.first_half_hour = 'free' 
        self.first_half_hour_description = None
        
        self.second_half_hour = 'free'
        self.second_half_hour_description = None



class calendar_entry:
    def __init__(self, start_date, end_date, summary, frequency, days, count, by_set_pos, interval, except_dates):
        tz = pytz.timezone('US/Mountain')
        
        self.summary = summary
        self.frequency = frequency
        self.count = count
        self.by_set_pos = by_set_pos
        self.interval = interval
        self.except_dates = except_dates
        
        self.days = []
        if len(days) > 0:
            for day in days:
                self.days.append(week_days[day])
             
        self.start_date = start_date
        self.end_date = end_date
        
        
        if type(self.start_date) == datetime.date:
            self.start_date = datetime.datetime(self.start_date.year, self.start_date.month, self.start_date.day)
        
        if type(self.end_date) == datetime.date:
            self.end_date = datetime.datetime(self.end_date.year, self.end_date.month, self.end_date.day)
        
        try:
            self.start_date = tz.normalize(self.start_date)
            self.start_date = self.start_date.replace(tzinfo=None)
            
        except:
            pass
        
        try:
            self.end_date = tz.normalize(self.end_date)
            self.end_date = self.end_date.replace(tzinfo=None)
        except:
            pass
        
        if self.except_dates:
            new_except_dates = []
            for except_date in self.except_dates:
                except_date = except_date.dt
                
                if type(except_date) == datetime.date:
                    except_date = datetime.datetime(except_date.year, except_date.month, except_date.day)
                try:
                    except_date = tz.normalize(except_date)
                    except_date = except_date.replace(tzinfo=None)
                except:
                    pass
                new_except_dates.append(except_date.date())
            self.except_dates = new_except_dates


class ics_calendar:

    def __init__(self):
        self.today = datetime.datetime.today()

    def load_calendar(self, ics_file):
        cal = Calendar.from_ical(open(ics_file).read())
        self.calendar_entries = []
    
        for component in cal.walk():
            try:
                if component.name == 'VEVENT':
                    if not 'DTSTART' in component.keys():
                        print "Error: No DTSTART found."
                        continue
                    if not 'DTEND' in component.keys():
                        print str(component)
                        print "Error: No DTEND found."
                        continue
                    
                    
                    summary = ''
                    frequency = ()
                    days = ()
                    count = None
                    by_set_pos = None
                    interval = None
                    except_days = None
                    
                    if 'SUMMARY' in component:
                        summary = component['SUMMARY']
                                    
                    if 'TRANSP' in component.keys():
                        if str(component['TRANSP']) == 'TRANSPARENT':
                            continue
                    
                    if 'RRULE' in component.keys():
                        frequency = component['RRULE']['FREQ']
                        days = component['RRULE']['BYDAY']
                        
                        if 'COUNT' in component['RRULE'].keys():
                            count = component['RRULE']['COUNT']
                            
                        if 'BYSETPOS' in component['RRULE'].keys():
                            by_set_pos = count = component['RRULE']['BYSETPOS']
                        
                        if 'INTERVAL' in component['RRULE'].keys():
                            interval = count = component['RRULE']['INTERVAL']
                    
                    if 'EXDATE' in component.keys():
                        except_days = component['EXDATE'].dts
                    
                    new_entry = calendar_entry(component['DTSTART'].dt, component['DTEND'].dt, summary, frequency, days, count, by_set_pos, interval, except_days)
                    self.calendar_entries.append(new_entry)
            
            except: #if we encounter an exception, just skip this entry
                raise
                    

    def get_todays_events(self):
        self.todays_events = []
        
        if len(self.calendar_entries) == 0:
            return 
        
        today_start = datetime.datetime(self.today.year, self.today.month, self.today.day,0,0,0)
        today_end = today_start + datetime.timedelta(days=1)
        
        #print "today start: " + str(today_start)
        #print "today end: " + str(today_end)
        #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
    

        for entry in self.calendar_entries:
            #print "start: " + str(entry.start_date)
            #print "end: " + str(entry.end_date)
            #print "summary: " + entry.summary
            #print "-----------------"
            cur_entry = entry
            
            if entry.except_dates: 
                print entry.except_dates
            
            if entry.except_dates and self.today.date() in entry.except_dates:
                continue
            
            if 'DAILY' in cur_entry.frequency:
                pass
            if 'WEEKLY' in cur_entry.frequency:
                
                if self.today > entry.start_date and self.today.weekday() in cur_entry.days:
                    if cur_entry.count and (self.today - entry.start_date).days/7 > cur_entry.count:
                        continue
                    
                    if cur_entry.interval and (self.today - entry.start_date).days/7 % cur_entry.interval[0] != 0:
                        continue                        
                            
                    cur_entry.start_date = datetime.datetime(self.today.year, self.today.month, self.today.day, 
                                                             cur_entry.start_date.hour, cur_entry.start_date.minute, cur_entry.start_date.second)
                    cur_entry.end_date = datetime.datetime(self.today.year, self.today.month, self.today.day, 
                                                           cur_entry.end_date.hour, cur_entry.end_date.minute, cur_entry.end_date.second)
            if 'MONTHLY' in cur_entry.frequency:
                if self.today > entry.start_date and cur_entry.by_set_pos and self.today.day/7+1 in cur_entry.by_set_pos:
                    if self.today.weekday() in cur_entry.days:
                        if cur_entry.count and (self.today - entry.start_date).days/30 > cur_entry.count:
                            continue

                        cur_entry.start_date = datetime.datetime(self.today.year, self.today.month, self.today.day, 
                                                                 cur_entry.start_date.hour, cur_entry.start_date.minute, cur_entry.start_date.second)
                        cur_entry.end_date = datetime.datetime(self.today.year, self.today.month, self.today.day, 
                                                               cur_entry.end_date.hour, cur_entry.end_date.minute, cur_entry.end_date.second)
        
            
            if entry.start_date > today_start and entry.end_date < today_end:
                self.todays_events.append(entry)
    
    def is_there_an_event_at_time(self,start_time, end_time):
        for calendar_entry in self.todays_events:

            if start_time >= calendar_entry.start_date and start_time < calendar_entry.end_date:
                return calendar_entry
        return None
    
    def generate_daily_schedule(self):
        half_hour = datetime.timedelta(minutes=30)
        
        #go from 8 to 5
        start_time = datetime.datetime(self.today.year, self.today.month, self.today.day, 9)
        end_time = datetime.datetime(self.today.year, self.today.month, self.today.day, 18)
        
        cur_time = start_time

        return_entries = []
        cur_entry = None
        last_summary = None        
        i = 0
        while cur_time < end_time:
            event = self.is_there_an_event_at_time(cur_time, cur_time+half_hour)
            
            
            if i == 0:
                cur_entry = schedule_entry()
                
                cur_entry.time = cur_time.hour
                if cur_entry.time > 12:
                    cur_entry.time -= 12
                    cur_entry.time = str(cur_entry.time) + " PM"
                else:
                    cur_entry.time = str(cur_entry.time) + " AM"  
                
                
                if event:
                    cur_entry.first_half_hour = 'busy'
                    if event.summary != last_summary:
                        cur_entry.first_half_hour_description = event.summary
                        last_summary = event.summary
                else: 
                    cur_entry.first_half_hour = 'free'
                    last_summary = None
                return_entries.append(cur_entry)
            else:
                if event:
                    cur_entry.second_half_hour = 'busy'
                    if event.summary != last_summary:
                        cur_entry.second_half_hour_description = event.summary
                        last_summary = event.summary
                else: 
                    cur_entry.second_half_hour = 'free'
                    last_summary = None

            #print cur_time.strftime("%H:%M") + "-",
            #print (cur_time+half_hour).strftime("%H:%M") + ": ",
            #print str(event != None)
            
            cur_time += half_hour
            
            i += 1
            if i > 1:
                i = 0
            
        return return_entries
        
    def get_todays_schedule(self, ics_file):
        self.load_calendar(ics_file)
        self.get_todays_events()
        #for e in self.todays_events:
        #    print str(e.start_date) + " - "  + str(e.end_date)
        return self.generate_daily_schedule()
        
        

if __name__ == "__main__":
    cal = ics_calendar()
    v = cal.get_todays_schedule('Nelson_Derek_Calendar.ics')
    for e in v:
        print e.time + ": " + e.first_half_hour + "," + e.second_half_hour + '   ',
        if e.first_half_hour_description:
            print e.first_half_hour_description,
        print ': ',
        if e.second_half_hour_description:
            print e.second_half_hour_description,
        
        print

