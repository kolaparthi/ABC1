from pprint import pformat, pprint
import logging
class PasswordMaskingFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.args, dict):
            record.args = self.sanitize_dict(record.args)
        else:
            record.args = tuple(self.sanitize_dict(i) for i in record.args)

        return True

    @staticmethod
    def sanitize_dict(d):
        if not isinstance(d, dict):
            return d

        if any(i for i in d.keys() if 'password' in i):
            d = d.copy()

            for k, v in d.items():
                if 'password' in k:
                    d[k] = '*** PASSWORD ***'

        return d

class CustomFormatter(logging.Formatter):
    def format(self, record):
        res = super(CustomFormatter, self).format(record)

        if hasattr(record, 'request'):
            filtered_request = PasswordMaskingFilter.sanitize_dict(record.request)
            res += '\n\t' + pformat(filtered_request, indent=4).replace('\n', '\n\t')
        return res


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("afsf")
logger.addFilter(PasswordMaskingFilter())

for handler in logger.root.handlers:
    handler.setFormatter(CustomFormatter(handler.formatter._fmt))

logging.info('This is a simple message')
fake_request = {'path': 'd:///Srini/pyth/', 'method': 'GET', 'username': 'test_user', 'password': 's00p3r s3kr1t'}
logging.info('basic request request: %(method)s %(path)s', fake_request)
logging.info('Dumped request: %r', fake_request)
logging.info('extra request: %(method)s %(path)s', fake_request, extra={'request': fake_request})