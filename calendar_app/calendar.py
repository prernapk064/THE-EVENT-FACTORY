from collections import defaultdict
from datetime import datetime
from . models import Event
import calendar


class Calendar(calendar.HTMLCalendar):
    def __init__(self, year, month):
        self.year = year
        self.month = month
        super().__init__()

    # Here we are adding the events of each day just by spliting the main
    # HTML into left and right and in center we are adding that event

    def Modify_HTML(self,hash_table,week_day):
       modified = calendar.HTMLCalendar.formatmonth(self, self.year, self.month)
       for day in range(1,32):
          make_modified = ''
          try:
              n = '<td class="{}">{}'.format(week_day[day],day)
              left,right = modified.split(n)
              make_modified = left +  n + '<div class="t">' + hash_table[day] +'</div>' + right
              modified = make_modified
          except:
                 pass
       return modified

    # Finding the events falling in this month's each day
    def Active_day(self):
        all_events = Event.objects.filter(start_at__year=self.year,start_at__month=self.month)
        week_day = {i.start_at.day:i.start_at.strftime("%a").lower() for i in all_events}
        hash_table = defaultdict(str)
        for festv in all_events:
            common_day = festv.start_at.day
            hash_table[common_day] += '<li><a style="color:red;background-color:#ede6e6" href="{}" class="added">{}<br> at {}</a></li>'.format(festv.event_url,festv.title,festv.start_at.strftime("%I:%M %p").lower())
        return self.Modify_HTML(hash_table,week_day)



# if i say to convert this: 2022-07-01 into string , u can use strf to convert datetime object intop string with your own format ex: make 2022-07-01 datetime object to "2022-07-01" but in  this format-> mm-day-year
# convert this  string "2022-07-01" into datetime object
# strp is vice-VSTART
# strf(current_date, "%m-%d-%Y %H:%M ") -> "07-01-2022 10:50 am"