from datetime import datetime,timedelta

from django.db import models

class ActiveCouponManager(models.Manager):
    def __init__(self, from_date=None, to_date=None):
        super(ActiveCouponManager, self).__init__()
        self.from_date = from_date
        self.to_date = to_date
        now = datetime.now
        if from_date and to_date:
            self.date_filters = (models.Q(**{'%s__isnull' % self.to_date: True}) |
                                 models.Q(**{'%s__gte' % self.to_date: now}),
                                 models.Q(**{'%s__isnull' % self.from_date: True}) |
                                 models.Q(**{'%s__lte' % self.from_date: now}))

        elif from_date:
            self.date_filters = (models.Q(**{'%s__isnull' % self.from_date: True}) |
                                 models.Q(**{'%s__lte' % self.from_date: now}),)
        elif to_date:
            self.date_filters = (models.Q(**{'%s__isnull' % self.to_date: True}) |
                                 models.Q(**{'%s__gte' % self.to_date: now}),)
        else:
            raise ValueError, "At least one date field is required"

    def get_query_set(self):
        """Retrieves items with publication dates according to self.date_filters
        """
        return super(ActiveManager, self).get_query_set().filter(*self.date_filters)

class EndsTodayCouponManager(models.Manager):
    def __init__(self, to_date=None):
        super(EndsTodayCouponManager, self).__init__()
        self.to_date = to_date
        now = datetime.now()
        start = datetime(now.year,now.month,now.day)
        end = start+timedelta(days=1)
        if to_date:
            self.date_filters = (models.Q(**{'%s__gte' % self.to_date: start}) &
                                 models.Q(**{'%s__lt' % self.to_date: end}) ,)
        else:
            raise ValueError, "At least one date field is required"

    def get_query_set(self):
        """Retrieves items with publication dates according to self.date_filters
        """
        return super(EndsTodayManager, self).get_query_set().filter(*self.date_filters)
