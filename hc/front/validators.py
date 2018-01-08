from croniter import croniter
from django.core.validators import ValidationError

class CronScheduleValidator(object):
    error_message = "Invalid cron input"
    def __call__(self, cron_schedule):
        try:
            croniter(cron_schedule)
        except:
            raise ValidationError(message=self.error_message)