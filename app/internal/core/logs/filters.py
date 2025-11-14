from logging import Filter, LogRecord


class RequestIdFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        req_id = getattr(record, 'req_id', '-')
        record.msg = f'{req_id} {record.msg}'
        return True


class ApSchedulerFilter(Filter):
    def filter(self, record):
        hidden_messages = [
            "Adding job tentatively -- it will be properly scheduled when the scheduler starts",
            "Added job \"fetch_urls\" to job store \"default\"",
            "Removed job start_fetch"
        ]
        
        mes = record.getMessage()
        return not any(msg in mes for msg in hidden_messages)
    