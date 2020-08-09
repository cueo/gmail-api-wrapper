from data import BASIC_SETTINGS_SCOPE, LABEL_SCOPE, TRANSACTION_SENDERS
from filter import Filter
from pprint import pprint

from label import Label

# If modifying these scopes, delete the file token.pickle.
from setup import authorize

SCOPES = [BASIC_SETTINGS_SCOPE, LABEL_SCOPE]

if __name__ == '__main__':
    service = authorize(SCOPES)

    label = Label(service)
    label.create_label('Transactions')
    pprint(label.all_labels())

    _filter = Filter(service)
    new_filter = _filter.create_filter(remove_labels=['INBOX'], add_labels=['Transactions'], senders=TRANSACTION_SENDERS)
    pprint(_filter.all_filters())
    _filter.delete_filter(new_filter['id'])
    pprint(_filter.all_filters(cached=False))
