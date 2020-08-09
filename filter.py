from label import Label


class Filter:
    def __init__(self, service):
        self.service = service
        self.label_service = Label(service)
        self.filters = None

    def all_filters(self, cached=True):
        if not cached or self.filters is None:
            self.filters = self.service.users().settings().filters().list(userId='me').execute()
        return self.filters

    def create_filter(self, add_labels, remove_labels, senders):
        labels = add_labels + remove_labels
        label_ids = self.label_service.get_label_ids(labels)
        print('Label and label ids:', label_ids)
        from_emails = ' OR '.join(senders)
        add_label_ids = [label_ids[label_id] for label_id in add_labels]
        remove_label_ids = [label_ids[label_id] for label_id in remove_labels]
        print('Setting filter for from=%s add_labels=%s remove_labels=%s'
              % (from_emails, add_label_ids, remove_label_ids))

        new_filter = {
            'criteria': {
                'from': from_emails
            },
            'action': {
                'addLabelIds': add_label_ids,
                'removeLabelIds': remove_label_ids
            }
        }
        result = self._create_filter(new_filter)
        print('Created filter: %s' % result['id'])
        return result

    def update_filter(self, label, sender):
        """
        Update filter to add sender to the filter for the given label.
        Args:
            label: label to add for the sender's mails
            sender: from address
        """
        label_id = self.label_service.get_label_id(label)
        print('Label id: %s' % label_id)
        filter_object = self.get_filter(label_id)
        if filter_object is None:
            print('Filter not found for the label: %s' % label)
            return
        senders = filter_object['criteria']['from']
        if sender in senders:
            print('Filter already contains %s' % sender)
            return
        senders += ' OR %s' % sender
        filter_object['criteria']['from'] = senders
        self.delete_filter(filter_object['id'])
        result = self._create_filter(filter_object)
        print('Created filter with id: %s' % result['id'])
        return result

    def _create_filter(self, filter_object):
        return self.service.users().settings().filters().create(userId='me', body=filter_object).execute()

    def get_filter(self, label_id):
        filters = self.service.users().settings().filters().list(userId='me').execute()['filter']
        # next(_filter for _filter in filters
        #   if 'addLabelIds' in _filter['action'] and _filter['action']['addLabelIds'] == label_id)
        for _filter in filters:
            if label_id in _filter.get('action', {}).get('addLabelIds', []):
                return _filter

    def delete_filter(self, filter_id):
        result = self.service.users().settings().filters().delete(userId='me', id=filter_id).execute()
        print('Deleted filter:', result)
        return result
