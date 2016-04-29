from FacebookUserNameCache import FacebookUserNameCache
from datetime import datetime
from bs4 import BeautifulSoup
import sys
import csv

my_name_forms = frozenset([
    'Andrew Brandon-Rumman',
    'Andrew Brandon Rumman',
    'Andrew Brandon',
    'Andrew Rumman Brandon',
    '1263360952@facebook.com'
])

html_date_format = '%A, %B %d, %Y at %I:%M%p %Z'
encoding = 'utf_8'

def get_soup_from_html(html_filename):
    with open(html_filename) as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        return soup


def parse_messages(soup, username_cache):
    message_objects = []
    threads = soup.find_all(class_='thread')
    for thread in threads:
        chat_name = get_chat_name(thread, username_cache)
        messages = thread.find_all(class_='message')
        parsed_messages = map(lambda message: parse_message(message, chat_name), messages)
        message_objects.extend(parsed_messages)

    print 'Parsed %d messages' % len(message_objects)
    print 'Looked up %d user names from Facebook API' % username_cache.get_stored_names_count()
    print '%d user names could not be found' % username_cache.get_missed_count()
    return message_objects


def get_chat_name(thread, username_cache):
    thread_name = thread.next.string.strip()
    thread_participants_array = parse_thread_name(thread_name, username_cache)
    chat_name =  ', '.join(thread_participants_array)
    return chat_name


def parse_thread_name(thread_name, username_cache):
    # Thread name is list of participants separated by commas
    participants = thread_name.split(', ')
    filtered_participants = []
    
    for participant in participants:
        if participant not in my_name_forms:
            user_id_index = participant.find('@facebook.com')
            if user_id_index > 0:
                facebook_id = participant[:user_id_index]
                participant_name = username_cache.get_name_for_id(facebook_id)
                if participant_name:
                    participant = participant_name

            filtered_participants.append(participant)

    return filtered_participants


def parse_message(message_div, chat_name):
    text = message_div.find_next_sibling().text
    user = message_div.find(class_='user').text
    time = message_div.find(class_='meta').text
    timestamp = datetime.strptime(time, html_date_format)

    return {
        'text': text,
        'sent_by_user': user,
        'from_me': bool(user in my_name_forms),
        'chat_name': chat_name,
        'timestamp': timestamp
    }


field_headers = ['Service', 'Text', 'From Me', 'Handle', 'Converser', 'Timestamp']

def write_to_csv(message_objects, output_filename):
    with open(output_filename, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(field_headers)
        for item in message_objects:
            converted_item = convert_message_object_to_csv_array(item)
            writer.writerow(converted_item)


def convert_message_object_to_csv_array(message):
    return [
        'Facebook',
        message['text'].encode(encoding),
        message['from_me'],
        message['chat_name'].encode(encoding),
        message['chat_name'].encode(encoding),
        message['timestamp'].isoformat()
    ]


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: %s <facebook html filename> <facebook access token filename> <output filename>' % sys.argv[0]
        sys.exit(-1)

    facebook_html_filename = sys.argv[1]
    facebook_access_token_filename = sys.argv[2]
    output_csv_filename = sys.argv[3]

    print 'Loading messages HTML file %s...' % facebook_html_filename
    soup = get_soup_from_html(facebook_html_filename)
    print 'Parsing messages from HTML...'
    username_cache = FacebookUserNameCache(facebook_access_token_filename)
    parsed_messages = parse_messages(soup, username_cache)
    print 'Writing to CSV file %s...' % output_csv_filename
    write_to_csv(parsed_messages, output_csv_filename)