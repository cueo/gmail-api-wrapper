from googleapiclient import errors


class Label:
    def __init__(self, service):
        self.service = service
        self.labels = None

    def all_labels(self, cached=True):
        if not cached or self.labels is None:
            self.labels = self.service.users().labels().list(userId='me').execute()['labels']
        return self.labels

    def get_label_id(self, label):
        all_labels = self.all_labels()
        return next(_label for _label in all_labels if _label['name'] == label)['id']

    def get_label_ids(self, labels):
        labels = {label.lower() for label in labels}
        all_labels = self.all_labels()
        return {label['name']: label['id'] for label in all_labels if label['name'].lower() in labels}

    def create_label(self, name, message_visibility='show', label_visibility='labelShow'):
        label_object = {
            'messageListVisibility': message_visibility,
            'name': name,
            'labelListVisibility': label_visibility
        }
        try:
            label = self.service.users().labels().create(userId='me',
                                                         body=label_object).execute()
            print('Created label with id=%s' % label['id'])
            return label
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
