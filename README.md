# gmail-api-wrapper
A Gmail API wrapper to perform manually exhaustive tasks, such as creating filters for some common senders, eg: add Transactions label to all such emails.

## Prerequisite
1. Go to Gmail API developer guide [here](https://developers.google.com/gmail/api/quickstart/python) and click on the button "Enable the Gmail API".
2. Download the generated `credentials.json` file into the directory.
3. On the first run, the app will need to authorize itself. Just follow the instructions in the link that opens up in your browser.

## How to use

### Authorize the app
>Required before doing anything else.
```python
from data import READONLY_SCOPE
from setup import authorize

scopes = [READONLY_SCOPE]

service = authorize(scopes)
```
Choose from following available scopes:
* `READONLY_SCOPE`
* `LABEL_SCOPE`
* `BASIC_SETTINGS_SCOPE`

### Print all labels
```python
from data import READONLY_SCOPE
from label import Label
from setup import authorize

scopes = [READONLY_SCOPE]

service = authorize(scopes)
label = Label(service)
print(label.all_labels())
```

### Create a label
```python
from data import LABEL_SCOPE
from label import Label
from setup import authorize

scopes = [LABEL_SCOPE]

service = authorize(scopes)
label = Label(service)
label.create_label('Shopping')
``` 

### Create a filter
```python
from data import BASIC_SETTINGS_SCOPE
from filter import Filter
from setup import authorize

scopes = [BASIC_SETTINGS_SCOPE]

service = authorize(scopes)
filter = Filter(service)
filter.create_filter(add_labels=['Shopping'], remove_labels=['INBOX'], senders=['noreply@amazon.com', 'noreply@myntra.com'])
```

#### Create filter with populated data
```python
from data import TRANSACTION_SENDERS

label.create_label('Transactions')
filter.create_filter(add_labels=['Transactions'], remove_labels=['INBOX'], senders=TRANSACTION_SENDERS)
``` 
