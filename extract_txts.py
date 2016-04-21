import sys
import csv
from datetime import datetime
import sqlite3

messages_query = ('select M.rowid, M.text, M.service, M.is_from_me, H.id as handle_id, M.date '
    'from message M inner join handle H on M.handle_id = H.rowid order by M.date')

iOS_epoch_offset = 978307200
encoding = 'utf_8'

def load_contacts(contacts_filename):

    phone_to_name = {}
    email_to_name = {}

    with open(contacts_filename, 'rb') as contacts_file:
        reader = csv.reader(contacts_file)
        reader.next() # Skip header row

        for row in reader:
            add_row_to_dict(row, phone_to_name, email_to_name)

        return (phone_to_name, email_to_name)


def add_row_to_dict(row, phone_dict, email_dict):
    name = row[0]
    phone = row[1]
    email = row[2]

    if phone:
        phone_dict[phone] = name
    if email:
        email_dict[email] = name
    if not phone and not email:
        print 'Contact record does not have phone or email \n %s' % row


def get_name_for_handle(handle, contacts):
    phone_dict = contacts[0]
    email_dict = contacts[1]

    if '@' in handle:
        return email_dict[handle] if handle in email_dict else None
    else:
        return phone_dict[handle] if handle in phone_dict else None


def get_texts_and_write_to_csv(database_filename, contacts, output_filename):
    texts = get_texts_from_database(database_filename);
    with open(output_filename, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(field_headers)
        for item in texts:
            converted_item = convert_fields_to_array(item, contacts)
            writer.writerow(converted_item)


field_headers = ['Service', 'Text', 'From Me', 'Handle', 'Converser', 'Timestamp']

def convert_fields_to_array(item, contacts):
    corrected_message_time = item['date'] + iOS_epoch_offset
    message_timestamp = datetime.fromtimestamp(corrected_message_time)
    message_text = item['text'] or ''
    handle_id = item['handle_id']
    converser = get_name_for_handle(handle_id, contacts)

    return [
        item['service'],
        message_text.encode(encoding),
        bool(item['is_from_me']),
        handle_id.encode(encoding),
        (converser or handle_id).encode(encoding),
        message_timestamp.isoformat()
    ]


def get_texts_from_database(database_filename):
    with sqlite3.connect(database_filename) as conn:
        # conn = sqlite3.connect(database_filename)
        conn.row_factory = sqlite3.Row
        
        c = conn.cursor()
        c.execute(messages_query)
        for item in c:
            yield item

    # conn.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: %s <database filename> <contacts csv filename> <output filename>' % sys.argv[0]
        sys.exit(-1)

    database_filename = sys.argv[1]
    contacts_csv_filename = sys.argv[2]
    output_csv_filename = sys.argv[3]

    contacts = load_contacts(contacts_csv_filename)
    get_texts_and_write_to_csv(database_filename, contacts, output_csv_filename)